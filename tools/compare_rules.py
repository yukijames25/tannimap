"""Do two rules files give the same verdicts? Run both on many random transcripts and compare.

    python tools/compare_rules.py KEY.json OTHER.json [--n 300] [--seed 1]

Category ids and names may differ between the two files, so only id-free results are compared:
credits counted toward graduation (now / with plan), the graduation shortfall, credits that count
nowhere, whether everything is satisfied, and each progression requirement's pass/fail.
The random transcripts use the 区分 labels that appear in KEY.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from tannimap.engine import EPS, check  # noqa: E402
from tannimap.model import FAILED, IN_PROGRESS, PASSED, PLANNED, Course, load_rules  # noqa: E402


def labels_of(rules) -> list:
    out = []
    for c in rules.walk():
        if c.match:
            out += c.match.labels
    return sorted(set(out))


def required_names(rules) -> list:
    return sorted({x for c in rules.walk() for x in c.required if not x.startswith("re:")})


NAMES_BY_LABEL: dict = {}  # label -> course names seen in the student's files (when only a few exist)


def random_transcript(rng, labels, required) -> list:
    courses, row = [], 0
    for lab in labels:
        fixed = NAMES_BY_LABEL.get(lab)
        n = rng.choice([0, 1, 1, 2]) if fixed else rng.choice([0, 0, 1, 1, 2, 3, 4, 6])
        for _ in range(n):
            row += 1
            status = rng.choices([PASSED, FAILED, IN_PROGRESS, PLANNED], [70, 6, 8, 16])[0]
            name = rng.choice(fixed) if fixed else f"{lab}科目{row}"
            courses.append(Course(name=name, credits=rng.choice([1, 2, 2, 2, 4]), label=lab,
                                  grade={PASSED: "A", FAILED: "F"}.get(status, ""), status=status, row=row))
    for req in required:
        if rng.random() < 0.85:
            row += 1
            owner = next((c for c in RULES_CACHE["key"].walk() if req in c.required), None)
            lab = owner.match.labels[0] if owner and owner.match and owner.match.labels else ""
            courses.append(Course(name=req, credits=2, label=lab, grade="A", status=rng.choice([PASSED, PASSED, PLANNED]),
                                  row=row))
    return courses


RULES_CACHE: dict = {}


def verdict(rules, courses) -> dict:
    res = check(rules, courses)
    out = {}
    for sc in ("now", "plan"):
        s = res[sc]
        dropped = sum(d.credits for cr in s.cats.values() for d in cr.dropped) + sum(c.credits for c, _ in s.not_counted)
        problems = any(cr.problems for cr in s.cats.values() if cr.cat.counts) or rules.total_min - s.total > EPS
        out[sc] = {"counted": round(s.total, 2), "short": round(max(0, rules.total_min - s.total), 2),
                   "not_counted": round(dropped, 2), "unmatched": round(sum(c.credits for c in s.unmatched), 2),
                   "all_ok": not problems}
    # progression requirements are matched by the year transition in their name ("3年→4年")
    out["progression"] = {_transition(p["name"]): p["ok"] for p in res["progression_now"]}
    return out


def _transition(name: str) -> str:
    import re
    m = re.search(r"(\d)\s*年\D{0,3}?(\d)\s*年", name)
    return f"{m.group(1)}->{m.group(2)}" if m else name


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("key")
    ap.add_argument("other")
    ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--labels-from", nargs="*", default=[],
                    help="use only the 区分 labels found in these transcripts (what the rule writer could see)")
    a = ap.parse_args()
    with open(a.key, encoding="utf-8") as fh:
        key = load_rules(fh.read())
    with open(a.other, encoding="utf-8") as fh:
        other = load_rules(fh.read())
    RULES_CACHE["key"] = key
    rng = random.Random(a.seed)
    labels, required = labels_of(key), required_names(key)
    if a.labels_from:
        from tannimap.cli import _read
        from tannimap.transcript import parse_transcript
        seen, names = set(), {}
        for path in a.labels_from:
            for c in parse_transcript(_read(path), key, default_status=PLANNED):
                seen.add(c.label)
                names.setdefault(c.label, set()).add(c.name)
        labels = [x for x in labels if x in seen]
        # a 区分 that holds only a couple of specific courses (e.g. two required ones) keeps those names
        req = set(required)
        for lab, ns in names.items():
            if len(ns) <= 2 and ns & req:
                NAMES_BY_LABEL[lab] = sorted(ns)
    fields = ["counted", "short", "not_counted", "unmatched", "all_ok"]
    agree = {f"{sc}.{f}": 0 for sc in ("now", "plan") for f in fields}
    agree["progression"] = 0
    agree["everything"] = 0
    examples = []
    for i in range(a.n):
        courses = random_transcript(rng, labels, required)
        vk, vo = verdict(key, courses), verdict(other, courses)
        same_all = True
        for sc in ("now", "plan"):
            for f in fields:
                ok = vk[sc][f] == vo[sc][f]
                agree[f"{sc}.{f}"] += ok
                same_all &= ok
        common = set(vk["progression"]) & set(vo["progression"])
        prog_ok = bool(common) and all(vk["progression"][t] == vo["progression"][t] for t in common)
        agree["progression"] += prog_ok
        same_all &= prog_ok
        agree["everything"] += same_all
        if not same_all and len(examples) < 5:
            examples.append({"case": i, "key": vk, "other": vo})
    print(json.dumps({"transcripts": a.n, "agreement": {k: round(v / a.n, 3) for k, v in agree.items()},
                      "first_differences": examples}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
