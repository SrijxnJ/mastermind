"""Post-build fixes for keyword-rule misfiles. Usage: python3 -I fix_categories.py LIBRARY_DIR"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
LIB = sys.argv[1]
from assemble_meta import CAT  # noqa: E402
cat = json.load(open(os.path.join(LIB, "catalog.json")))
moves = 0
for e in cat:
    new = None
    if e["category"] == "typing" and re.search(r"keypress-\d+", e["source_file"] or ""):
        new = "keyboard"
    elif e["category"] == "gaming" and "casino" in e["source_url"]:
        new = "cash-register" if re.search(r"chip", e["source_file"], re.I) else "foley-cards-dice"
    if not new or e["featured"]:
        continue
    src = os.path.join(LIB, e["file"])
    dst_dir = os.path.join(LIB, "sfx", new)
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, os.path.basename(src))
    os.replace(src, dst)
    e["file"] = os.path.relpath(dst, LIB)
    e["category"] = new
    e["id"] = f"{new}/{os.path.splitext(os.path.basename(dst))[0]}"
    e["use_when"], e["pairs_with_transition"], e["niches"] = CAT[new][0], CAT[new][1], CAT[new][2]
    e["subtype"] = None
    moves += 1
cat.sort(key=lambda e: (e["category"], not e["featured"], e.get("featured_rank") or 999, e["file"]))
json.dump(cat, open(os.path.join(LIB, "catalog.json"), "w"), indent=1, ensure_ascii=False)
print(moves, "moved")
