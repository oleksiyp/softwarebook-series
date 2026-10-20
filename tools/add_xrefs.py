"""Add cross-book link badges to a book's chapter sources.

    python3 tools/add_xrefs.py <xref.yml> <self-key> <file.md>... [--write]

After every "the X book's Chapter/Section/Figure N" (or "Chapter/Section N of the X book") it adds
{% include xref.html to="x:N" %}; the first plain "the X book" in each file gets one to the book.
Code blocks, headings and existing badges are left alone. Prints what it would do without --write.
"""
import re
import sys

NAMES = {"Architecture": "architecture", "Products": "products", "Software": "software",
         "Resilience": "resilience", "Operations": "operations"}
args = [a for a in sys.argv[1:] if a != "--write"]
write = "--write" in sys.argv
keys = set(re.findall(r'^"([^"]+)":', open(args[0]).read(), re.M))
selfkey, files = args[1], args[2:]
BOOK = r"(Architecture|Products|Software|Resilience|Operations)"
LOC = r"(Chapters?|Sections?|Figures?|Appendix)(?: (\d+(?:\.\d+)?))?"
A = re.compile(r"the " + BOOK + r" book's " + LOC)
B = re.compile(r"(Chapter|Section) (\d+(?:\.\d+)?) of the " + BOOK + r" book")
BARE = re.compile(r"the " + BOOK + r" book\b")
TAG = '{{% include xref.html to="{}" %}}'


def target(book, kind, num):
    k = NAMES[book]
    if kind.startswith("Appendix"):
        cand = [f"{k}:a"]
    elif kind.startswith("Figure") and num:
        cand = [f"{k}:f{num.split('.')[0]}"]
    elif num:
        cand = [f"{k}:{num}", f"{k}:{num.split('.')[0]}"]
    else:
        cand = []
    for c in cand + [k]:
        if c in keys:
            return c, c != (cand[0] if cand else k)
    return None, True


total = fallbacks = 0
for f in files:
    lines = open(f).read().split("\n")
    seen = set()   # books already linked in this file
    fence = False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            fence = not fence
            continue
        if fence or line.startswith("#") or "include xref.html" in line:
            continue
        edits = []  # (position, tag)
        for m in A.finditer(line):
            if NAMES[m.group(1)] == selfkey:
                continue
            key, fb = target(m.group(1), m.group(2), m.group(3))
            edits.append((m.end(), key, m.group(0), fb))
        for m in B.finditer(line):
            if NAMES[m.group(3)] == selfkey:
                continue
            key, fb = target(m.group(3), m.group(1), m.group(2))
            edits.append((m.end(), key, m.group(0), fb))
        located = {e[1].split(":")[0] for e in edits if e[1]}
        for m in BARE.finditer(line):
            k = NAMES[m.group(1)]
            if k == selfkey or k in seen or k in located:
                continue
            if any(m.start() <= e[0] <= m.end() + 40 for e in edits):
                continue
            edits.append((m.end(), k, m.group(0), False))
            seen.add(k)
        seen |= located
        for pos, key, what, fb in sorted(edits, reverse=True):
            if not key:
                print(f"  NO TARGET {f}:{i+1}: {what}")
                continue
            line = line[:pos] + TAG.format(key) + line[pos:]
            total += 1
            fallbacks += fb
            if fb:
                print(f"  fallback {f}:{i+1}: {what} -> {key}")
        lines[i] = line
    if write:
        open(f, "w").write("\n".join(lines))
print(f"{total} badges ({fallbacks} to a coarser target){'' if write else ' — dry run'}")
