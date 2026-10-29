"""Builds the Master Mind: one knowledge graph from the Brain, the researcher and the library.

Inputs (any missing file is skipped):
  brain/data/atoms.json          knowledge atoms merged from every lesson
  brain/research/trends.json     the researcher's latest findings
  library/catalog.json           CC0 sound effects
  library/memes/memes.json       meme sounds and formats
  library/transitions/transitions.json
Outputs:
  mastermind/data.json           graph data (atoms + embedding neighbours)
  mastermind/index.html          the interactive page (template + data)
  wiki/                          the generated wiki (index, topics, pathways, niches, sources, clashes)

Run:  .venv/bin/python mastermind/build.py
Embeddings: fastembed BAAI/bge-small-en-v1.5 on CPU (a small sentence-embedding neural network).
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]          # social-media-manager/
MM = ROOT / "mastermind"
WIKI = ROOT / "wiki"
REPO_BLOB = "https://github.com/SrijxnJ/mastermind/blob/main/"

FAMILIES = {
    "content": {"label": "Content", "topics": ["hooks", "story", "ideas"]},
    "visual": {"label": "Visual craft", "topics": ["editing", "effects", "transitions", "text", "colour"]},
    "sound": {"label": "Sound", "topics": ["sound"]},
    "filming": {"label": "Filming", "topics": ["filming"]},
    "strategy": {"label": "Strategy", "topics": ["brand", "growth", "business", "process", "ai-tools"]},
}
TOPIC_LABEL = {
    "hooks": "Hooks", "story": "Story & scripts", "ideas": "Ideas", "editing": "Editing & pacing",
    "effects": "Effects", "transitions": "Transitions", "text": "Text & fonts", "colour": "Colour",
    "sound": "Sound", "filming": "Filming", "brand": "Brand", "growth": "Growth",
    "business": "Business", "process": "Process", "ai-tools": "AI & tools",
}
STAGES = ["idea", "script", "film", "edit", "sound", "graphics", "publish", "analyse", "monetise", "mindset"]
STAGE_LABEL = {s: s.capitalize() for s in STAGES}
FORMATS = [
    ("reel30", "Reel · 30 s"), ("reel60", "Reel · 60 s"), ("reel90", "Long reel · 60 s–3 min"),
    ("yt-short", "YouTube Short"), ("yt-long", "YouTube long-form"), ("carousel", "Carousel"),
    ("story", "Story"), ("podcast", "Podcast"),
]
NICHES = ["all", "gym", "tech", "gaming", "travel"]


def load(rel):
    p = ROOT / rel
    if not p.exists():
        print(f"  (skip: {rel} not found)")
        return None
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError as e:
        print(f"  (skip: {rel} is not valid JSON yet: {e})")
        return None


def _valid(path):
    try:
        json.loads(path.read_text())
        return True
    except (json.JSONDecodeError, OSError):
        print(f"  (skip: {path.name} is not valid JSON yet)")
        return False


def embed(texts):
    from fastembed import TextEmbedding
    model = TextEmbedding("BAAI/bge-small-en-v1.5")
    v = np.array(list(model.embed(texts)), dtype=np.float32)
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def main():
    brain = load("brain/data/atoms.json")
    if not brain:
        sys.exit("atoms.json is required")
    research = load("brain/research/trends.json") or {}
    approaches = (load("brain/data/approaches.json") or {}).get("dimensions", [])
    catalog = load("library/catalog.json") or []
    memes = load("library/memes/memes.json") or []
    transitions = load("library/transitions/transitions.json") or []
    if isinstance(memes, dict):
        memes = memes.get("memes", [])
    if isinstance(transitions, dict):
        transitions = transitions.get("transitions", [])
    if isinstance(catalog, dict):
        catalog = catalog.get("sounds", catalog.get("items", []))

    # Lessons ingested after the big extraction arrive as brain/data/atoms_<id>.json; merge them in.
    for extra in sorted((ROOT / "brain/data").glob("atoms_*.json")):
        x = json.loads(extra.read_text())
        if x.get("source") and x["source"]["id"] not in {s["id"] for s in brain["sources"]}:
            brain["sources"].append(x["source"])
        known = {a["id"] for a in brain["atoms"]}
        brain["atoms"] += [a for a in x.get("atoms", []) if a["id"] not in known]
        cids = {c["id"] for c in brain["clashes"]}
        brain["clashes"] += [c for c in x.get("clashes", []) if c["id"] not in cids]
        print(f"  merged {extra.name}")

    atoms = brain["atoms"]
    ids = [a["id"] for a in atoms]
    print(f"atoms: {len(atoms)}")

    # Neural linking: embed every atom, connect each to its closest neighbours.
    vec = embed([f"{a['title']}. {a['text']} {a.get('how', '')}" for a in atoms])
    sim = vec @ vec.T
    np.fill_diagonal(sim, -1)
    top1 = sim.max(axis=1)
    threshold = float(np.percentile(top1, 25))            # weakest quarter of best matches sets the floor
    for i, a in enumerate(atoms):
        order = np.argsort(-sim[i])[:5]
        a["nb"] = [ids[j] for j in order if sim[i, j] >= threshold][:4] or [ids[order[0]]]
        a["nbs"] = [round(float(sim[i, j]), 3) for j in order if ids[j] in a["nb"]]
    print(f"neighbour threshold: {threshold:.3f}")

    # Trends: link each to the atoms that support it.
    trends = research.get("trends", [])
    if trends:
        tv = embed([f"{t.get('name','')}. {t.get('what','')} {t.get('hook','')} {t.get('edit','')} {t.get('sound','')}" for t in trends])
        ts = tv @ vec.T
        for i, t in enumerate(trends):
            t["atoms"] = [ids[j] for j in np.argsort(-ts[i])[:6]]

    # Library items: link memes and transitions to their nearest atoms too.
    for group in (memes, transitions):
        if group:
            gv = embed([" ".join(str(x.get(k, "")) for k in ("name", "what", "meaning", "use_when", "when", "timing")) for x in group])
            gs = gv @ vec.T
            for i, x in enumerate(group):
                x["atoms"] = [ids[j] for j in np.argsort(-gs[i])[:3]]

    # Approaches: each option is wired to the atoms that support it (given ids + nearest by embedding).
    known = set(ids)
    opts = [(d, o) for d in approaches for o in d.get("options", [])]
    if opts:
        ov = embed([f"{d['name']}: {o['name']}. {o.get('what','')} {o.get('looks_like','')}" for d, o in opts])
        osim = ov @ vec.T
        for i, (d, o) in enumerate(opts):
            given = [a for a in o.get("atoms", []) if a in known]
            near = [ids[j] for j in np.argsort(-osim[i])[:4] if ids[j] not in given]
            o["atoms"] = given + near[: max(0, 5 - len(given))]

    topic_count = defaultdict(int)
    for a in atoms:
        topic_count[a["topic"]] += 1
    topics = [{"id": t, "label": TOPIC_LABEL[t], "family": f, "n": topic_count[t]}
              for f, fam in FAMILIES.items() for t in fam["topics"]]

    page_atoms = [{
        "id": a["id"], "t": a["title"], "x": a["text"], "h": a.get("how", ""), "tp": a["topic"],
        "st": a["stage"], "f": a["formats"], "n": a["niches"], "s": a["sources"], "c": a.get("clashes", []),
        "ev": a.get("evidence", "stated"), "q": a.get("quote", ""), "nb": a["nb"],
    } for a in atoms]

    data = {
        "meta": {"updated": brain.get("updated"), "trendsUpdated": research.get("updated"),
                 "counts": {"atoms": len(atoms), "sources": len(brain["sources"]),
                            "clashes": sum(1 for c in brain["clashes"] if c.get("status", "open") == "open"),
                            "trends": len(trends), "sfx": len(catalog), "memes": len(memes),
                            "transitions": len(transitions), "links": sum(len(a["nb"]) for a in atoms),
                            "dimensions": len(approaches), "options": sum(len(d.get("options", [])) for d in approaches)}},
        "families": {k: v["label"] for k, v in FAMILIES.items()},
        "topics": topics, "stages": STAGES, "formats": [{"id": i, "label": l} for i, l in FORMATS],
        "niches": NICHES, "sources": brain["sources"], "atoms": page_atoms, "clashes": brain["clashes"],
        "tools": brain.get("tools", []), "trends": trends, "audio": research.get("trending_audio", []),
        "gaps": research.get("brain_gaps", []),
        "approaches": approaches,
        "learn": [json.loads(f.read_text()) for f in sorted((ROOT / "brain/learn").glob("*.json")) if _valid(f)],
        "ideas": {f.stem: json.loads(f.read_text()) for f in sorted((ROOT / "brain/ideas").glob("*.json")) if _valid(f)},
        "viral": {f.stem: json.loads(f.read_text()) for f in sorted((ROOT / "brain/research/viral").glob("*.json")) if _valid(f)},
        "library": {"sfx": catalog, "memes": memes, "transitions": transitions},
        "blob": REPO_BLOB,
    }
    # Local semantic index for query.py: one vector per atom, approach option and trend.
    keys = [f"atom:{a['id']}" for a in atoms]
    vecs = [vec]
    if opts:
        keys += [f"approach:{d['id']}/{o['id']}" for d, o in opts]; vecs.append(ov)
    if trends:
        keys += [f"trend:{t['id']}" for t in trends]; vecs.append(tv)
    np.savez_compressed(MM / "vectors.npz", keys=np.array(keys), vecs=np.vstack(vecs).astype(np.float16))

    (MM / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))
    tpl = (MM / "template.html").read_text()
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    (MM / "index.html").write_text(tpl.replace("/*__DATA__*/null", payload))
    print(f"page: {(MM / 'index.html').stat().st_size/1024:.0f} KB")

    write_wiki(brain, atoms, trends, memes, transitions, catalog, research, approaches)


# ---------------------------------------------------------------- wiki

def atom_line(a, by_id, depth="../"):
    src = ", ".join(f"[{s}]({depth}sources/{s}.md)" for s in a["sources"])
    cl = " ".join(f"⚠ [{c}]({depth}clashes.md#{c.lower()})" for c in a.get("clashes", []))
    rel = ", ".join(f"[{by_id[n]['title']}]({depth}topics/{by_id[n]['topic']}.md#{n})" for n in a["nb"])
    out = [f"### {a['title']}", f"<a id=\"{a['id']}\"></a>", "", a["text"]]
    if a.get("how"):
        out.append(f"\n**How:** {a['how']}")
    if a.get("quote"):
        out.append(f"\n> {a['quote']}")
    meta = f"\n`{a['stage']}` · formats: {', '.join(a['formats'])} · niches: {', '.join(a['niches'])} · {a.get('evidence','stated')} · from {src}"
    out.append(meta + (f" · {cl}" if cl else ""))
    out.append(f"\nRelated: {rel}\n")
    return "\n".join(out)


def write_wiki(brain, atoms, trends, memes, transitions, catalog, research, approaches=()):
    by_id = {a["id"]: a for a in atoms}
    for d in ("topics", "pathways", "niches", "sources"):
        (WIKI / d).mkdir(parents=True, exist_ok=True)
    gen = "<!-- Generated by mastermind/build.py from brain/data/atoms.json. Edit the atoms, not this page. -->\n\n"

    # topics
    for f, fam in FAMILIES.items():
        for t in fam["topics"]:
            ta = [a for a in atoms if a["topic"] == t]
            body = [gen + f"# {TOPIC_LABEL[t]}\n", f"Family: **{fam['label']}** · {len(ta)} ideas · [index](../index.md)\n"]
            for st in STAGES:
                group = [a for a in ta if a["stage"] == st]
                if group:
                    body.append(f"\n## {STAGE_LABEL[st]}\n")
                    body += [atom_line(a, by_id) for a in group]
            (WIKI / "topics" / f"{t}.md").write_text("\n".join(body))

    # pathways: format × niche, ordered by stage
    for fid, flabel in FORMATS:
        fa = [a for a in atoms if fid in a["formats"]]
        body = [gen + f"# Pathway: {flabel}\n",
                f"Everything the Brain knows that applies to **{flabel}**, in the order you'd use it. "
                f"{len(fa)} ideas. Niche sections list only the extra, niche-specific ideas. [index](../index.md)\n"]
        for st in STAGES:
            group = [a for a in fa if a["stage"] == st and "all" in a["niches"]]
            if group:
                body.append(f"\n## {STAGE_LABEL[st]}\n")
                body += [f"- **[{a['title']}](../topics/{a['topic']}.md#{a['id']})**: {a['text']}"
                         + (f" ⚠ {', '.join(a['clashes'])}" if a.get("clashes") else "") for a in group]
        for n in NICHES[1:]:
            group = [a for a in fa if n in a["niches"]]
            nt = [t for t in trends if t.get("niche") == n and fid in t.get("formats", [])]
            if group or nt:
                body.append(f"\n## {n.capitalize()} extras\n")
                body += [f"- **[{a['title']}](../topics/{a['topic']}.md#{a['id']})** ({a['stage']}): {a['text']}" for a in group]
                body += [f"- 🔥 Trend: **{t['name']}** (heat {t.get('heat','?')}/5): {t.get('what','')}" for t in nt]
        (WIKI / "pathways" / f"{fid}.md").write_text("\n".join(body))

    # niches
    for n in NICHES[1:]:
        na = [a for a in atoms if n in a["niches"]]
        nt = [t for t in trends if t.get("niche") == n]
        nm = [m for m in memes if n in (m.get("niches") or m.get("niche") or [])]
        ntr = [x for x in transitions if n in (x.get("niches") or x.get("niche") or [])]
        body = [gen + f"# Niche: {n.capitalize()}\n", "[index](../index.md)\n", f"\n## Niche-specific ideas ({len(na)})\n"]
        body += [f"- **[{a['title']}](../topics/{a['topic']}.md#{a['id']})** ({a['stage']}): {a['text']}" for a in na]
        if nt:
            body.append(f"\n## Trends right now ({len(nt)})\n")
            for t in nt:
                needs = ", ".join(f"{x['item']} ({x['status']})" for x in t.get("needs", []))
                body.append(f"- **{t['name']}** · heat {t.get('heat','?')}/5 · {', '.join(t.get('formats', []))}: {t.get('what','')}\n  - Needs: {needs}")
        if nm:
            body.append(f"\n## Memes ({len(nm)})\n")
            body += [f"- **{m.get('name')}**: {m.get('meaning', m.get('what',''))} Timing: {m.get('timing', '')}" for m in nm]
        if ntr:
            body.append(f"\n## Transitions ({len(ntr)})\n")
            body += [f"- **{x.get('name')}**: {x.get('when', x.get('what',''))}" for x in ntr]
        (WIKI / "niches" / f"{n}.md").write_text("\n".join(body))

    # sources
    for s in brain["sources"]:
        sa = [a for a in atoms if s["id"] in a["sources"]]
        link = f"[{s.get('file')}](../../brain/{s['file']})" if s.get("file") else ""
        body = [gen + f"# {s['id']}: {s.get('title','')}\n",
                f"{s.get('creator','')} · {s.get('kind','')} · {s.get('url','')} · notes: {link}\n",
                f"**Core lesson:** {s.get('summary','')}\n", f"\n## Ideas from this source ({len(sa)})\n"]
        body += [f"- **[{a['title']}](../topics/{a['topic']}.md#{a['id']})** · {a['topic']}: {a['text']}" for a in sa]
        (WIKI / "sources" / f"{s['id']}.md").write_text("\n".join(body))

    # approaches: one page per dimension, options side by side
    (WIKI / "approaches").mkdir(parents=True, exist_ok=True)
    idx = [gen + "# Approaches\n", "Every style choice as a menu. Each dimension lists the options the sources use, what each is good and weak at, and what a reel made that way looks like. Clashes live here as options, not problems. [index](../index.md)\n"]
    for fam in FAMILIES:
        ds = [d for d in approaches if d.get("family") == fam]
        if ds:
            idx.append(f"\n## {FAMILIES[fam]['label']}\n")
            idx += [f"- [{d['name']}]({d['id']}.md): {d.get('question','')} ({' · '.join(o['name'] for o in d['options'])})" for d in ds]
    (WIKI / "approaches" / "index.md").write_text("\n".join(idx) + "\n")
    for d in approaches:
        body = [gen + f"# {d['name']}\n", f"**{d.get('question','')}** · [all approaches](index.md)" + (f" · clashes: {', '.join(d.get('clashes', []))}" if d.get("clashes") else "") + "\n"]
        for o in d["options"]:
            bf = o.get("best_for", {})
            body += [f"\n## {o['name']}\n<a id=\"{o['id']}\"></a>\n", o.get("what", ""),
                     f"\n**Looks like:** {o.get('looks_like','')}",
                     "\n**Good at:** " + "; ".join(o.get("good_at", [])),
                     "\n**Weak at:** " + "; ".join(o.get("weak_at", [])),
                     f"\n**Best for:** formats {', '.join(bf.get('formats', []))} · niches {', '.join(bf.get('niches', []))} · goals {', '.join(bf.get('goals', []))} · effort {o.get('effort','?')}",
                     f"\n**How:** {o.get('how','')}",
                     "\n**Backed by:** " + ", ".join(f"[{by_id[a]['title']}](../topics/{by_id[a]['topic']}.md#{a})" for a in o.get("atoms", []) if a in by_id)
                     + " · sources " + ", ".join(o.get("sources", []))]
        if d.get("mixes"):
            body.append(f"\n## Mixing\n{d['mixes']}")
        if d.get("pick_by"):
            body.append(f"\n## Rule of thumb\n{d['pick_by']}")
        (WIKI / "approaches" / f"{d['id']}.md").write_text("\n".join(body) + "\n")

    # clashes
    body = [gen + "# Clashes\n", "Open disagreements between sources. We resolve these together after the knowledge dump. [index](index.md)\n"]
    for c in brain["clashes"]:
        side = [a for a in atoms if c["id"] in a.get("clashes", [])]
        body.append(f"\n## {c['id']}\n<a id=\"{c['id'].lower()}\"></a>\n\n**{c.get('topic','')}** · {c.get('status','open')}\n\n- A: {c.get('a','')}\n- B: {c.get('b','')}")
        if side:
            body.append("- Ideas involved: " + ", ".join(f"[{a['title']}](topics/{a['topic']}.md#{a['id']})" for a in side))
    (WIKI / "clashes.md").write_text("\n".join(body))

    # index
    tc = defaultdict(int)
    for a in atoms:
        tc[a["topic"]] += 1
    lines = [gen + "# Srijan's Social Media Wiki\n",
             f"Updated {brain.get('updated')} · **{len(atoms)} ideas** from **{len(brain['sources'])} sources** · "
             f"{len(brain['clashes'])} clashes · {len(trends)} live trends · {len(catalog)} sound effects · {len(memes)} memes · {len(transitions)} transitions\n",
             "How this wiki works: [SCHEMA.md](SCHEMA.md) · change history: [log.md](log.md) · interactive map: [Master Mind](../mastermind/index.html)\n",
             "\n## Pathways (pick a format)\n"]
    for fid, flabel in FORMATS:
        lines.append(f"- [{flabel}](pathways/{fid}.md): {sum(1 for a in atoms if fid in a['formats'])} ideas")
    lines.append("\n## Topics\n")
    for f, fam in FAMILIES.items():
        lines.append(f"- **{fam['label']}**: " + " · ".join(f"[{TOPIC_LABEL[t]}](topics/{t}.md) ({tc[t]})" for t in fam["topics"]))
    lines.append("\n## Niches\n")
    lines.append(" · ".join(f"[{n.capitalize()}](niches/{n}.md)" for n in NICHES[1:]))
    lines.append("\n## Sources\n")
    lines += [f"- [{s['id']}](sources/{s['id']}.md): {s.get('title','')} ({s.get('creator','')})" for s in brain["sources"]]
    lines.append("\n## Elsewhere\n")
    lines += [f"- [Approaches](approaches/index.md): {len(approaches)} style dimensions, {sum(len(d['options']) for d in approaches)} options", "- [Clashes](clashes.md)", "- [Researcher brief](../brain/research/RESEARCHER.md) and [latest trends](../brain/research/trends.json)",
              "- [Library: sounds, memes, transitions, mixing](../library/README.md)", "- [Parked tools](../brain/PARKED.md)"]
    gaps = research.get("brain_gaps", [])
    if gaps:
        lines.append("\n## Known gaps (from the researcher)\n")
        lines += [f"- **{g.get('topic')}**: {g.get('why')}" for g in gaps]
    (WIKI / "index.md").write_text("\n".join(lines) + "\n")
    print(f"wiki: {sum(1 for _ in WIKI.rglob('*.md'))} pages")


if __name__ == "__main__":
    main()
