"""Resolve merge conflicts in markdown files whose hunks are table rows.

Rows are keyed by their first cell; when both sides have a row, the longer
(more detailed) one wins. Order: our rows, with their new rows inserted after
the last row that precedes them on their side. Non-table hunks are left alone
(exit 1 if any remain).
"""
import re
import sys


def key(row):
    cells = row.split("|")
    return cells[1].strip() if len(cells) > 2 else row


def merge(ours, theirs):
    out = list(ours)
    index = {key(r): i for i, r in enumerate(out)}
    last = -1
    for r in theirs:
        k = key(r)
        if k in index:
            i = index[k]
            if len(r) > len(out[i]):
                out[i] = r
            last = i
        else:
            out.insert(last + 1, r)
            last += 1
            index = {key(x): j for j, x in enumerate(out)}
    return out


def main(path):
    lines = open(path).read().split("\n")
    result, i, unresolved = [], 0, 0
    while i < len(lines):
        if lines[i].startswith("<<<<<<< "):
            m = next(j for j in range(i, len(lines)) if lines[j] == "=======")
            e = next(j for j in range(m, len(lines)) if lines[j].startswith(">>>>>>> "))
            ours, theirs = lines[i + 1:m], lines[m + 1:e]
            if all(l.lstrip().startswith("|") for l in ours + theirs if l.strip()):
                result += merge([l for l in ours if l.strip()], [l for l in theirs if l.strip()])
            else:
                result += lines[i:e + 1]
                unresolved += 1
            i = e + 1
        else:
            result.append(lines[i])
            i += 1
    open(path, "w").write("\n".join(result))
    return unresolved


if __name__ == "__main__":
    bad = sum(main(p) for p in sys.argv[1:])
    sys.exit(1 if bad else 0)
