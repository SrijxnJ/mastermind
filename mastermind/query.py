"""Semantic search over the Master Mind, for ideating locally (no deployment).

  .venv/bin/python mastermind/query.py "30 s gym reel hook ideas" [-k 12] [--kind atom|approach|trend]

Prints the closest ideas, approach options and trends, using the same embedding model as build.py.
Run build.py first; it writes vectors.npz and data.json next to this file.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from fastembed import TextEmbedding

MM = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("-k", type=int, default=12)
    ap.add_argument("--kind", choices=["atom", "approach", "trend"])
    args = ap.parse_args()

    idx = np.load(MM / "vectors.npz")
    keys, vecs = idx["keys"], idx["vecs"].astype(np.float32)
    data = json.loads((MM / "data.json").read_text())
    atoms = {a["id"]: a for a in data["atoms"]}
    dims = {d["id"]: d for d in data.get("approaches", [])}
    trends = {t["id"]: t for t in data.get("trends", [])}

    q = np.array(list(TextEmbedding("BAAI/bge-small-en-v1.5").embed([args.query])))[0]
    q /= np.linalg.norm(q)
    order = np.argsort(-(vecs @ q))
    shown = 0
    for i in order:
        kind, ref = str(keys[i]).split(":", 1)
        if args.kind and kind != args.kind:
            continue
        score = float(vecs[i] @ q)
        if kind == "atom":
            a = atoms[ref]
            print(f"[{ref}] {score:.2f} · {a['tp']}/{a['st']} · {a['t']}: {a['x']}" + (f"  ⚠ {' '.join(a['c'])}" if a["c"] else ""))
        elif kind == "approach":
            d, o = ref.split("/", 1)
            opt = next(x for x in dims[d]["options"] if x["id"] == o)
            print(f"[A:{ref}] {score:.2f} · {dims[d]['name']} → {opt['name']}: good at {', '.join(opt.get('good_at', []))}")
        else:
            t = trends[ref]
            print(f"[{ref}] {score:.2f} · trend ({t.get('niche')}, heat {t.get('heat')}) {t['name']}")
        shown += 1
        if shown >= args.k:
            break


if __name__ == "__main__":
    main()
