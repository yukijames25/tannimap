"""The browser version (web/index.html) must give exactly the same results as the Python version."""
import json
import os
import random
import shutil
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "src"))

from tannimap.engine import check  # noqa: E402
from tannimap.model import PLANNED, load_rules  # noqa: E402
from tannimap.report import canonical, text_report  # noqa: E402
from tannimap.transcript import parse_transcript  # noqa: E402

NODE = shutil.which("node")


def _read(*p):
    with open(os.path.join(ROOT, *p), encoding="utf-8") as fh:
        return fh.read()


def random_cases(rules_text: str, n: int, seed: int) -> list:
    r = load_rules(rules_text)
    labels = sorted({x for c in r.walk() if c.match for x in c.match.labels})
    required = sorted({x for c in r.walk() for x in c.required if not x.startswith("re:")})
    rng = random.Random(seed)
    grades = r.grading_pass[:4] + r.grading_fail[:1] + [""]
    cases = []
    for _ in range(n):
        g = ["科目名,区分,単位数,評価,年度"]
        p = ["科目名,区分,単位数"]
        k = 0
        for lab in labels:
            for _ in range(rng.choice([0, 1, 1, 2, 3, 5])):
                k += 1
                if rng.random() < 0.15:
                    p.append(f"科目{k},{lab},{rng.choice([1, 2, 4])}")
                else:
                    g.append(f"科目{k},{lab},{rng.choice([1, 2, 2, 4])},{rng.choice(grades)},"
                             f"{rng.choice([2024, 2025, 2026])}")
        for req in required:
            if rng.random() < 0.7:
                g.append(f"{req},,2,{r.grading_pass[0]},2026")
        g.append(f"謎の科目,未知の区分,2,{r.grading_pass[0]},2025")
        cases.append({"rules": rules_text, "grades": "\n".join(g), "plan": "\n".join(p) if len(p) > 1 else "",
                      "years": rng.choice([None, 2, 3]), "entry_year": rng.choice([None, 2024])})
    return cases


def python_side(case):
    try:
        r = load_rules(case["rules"])
        courses = parse_transcript(case["grades"], r)
        if case.get("plan"):
            courses += parse_transcript(case["plan"], r, default_status=PLANNED)
        res = check(r, courses, case.get("years"), case.get("entry_year"))
        return {"ok": canonical(r, res), "text": text_report(r, res, courses)}
    except Exception as e:  # noqa: BLE001
        return {"error": f"{type(e).__name__}: {e}"}


@unittest.skipUnless(NODE, "node is not installed")
class WebParity(unittest.TestCase):
    def test_same_results(self):
        cases = []
        for path in (("tests", "data", "tufs_lc_from_mistakes.json"), ("tests", "data", "hosei_jinkan_2022.json"),
                     ("tests", "data", "kagawa_edu_2025.json"), ("tests", "data", "kumamoto_pu_mgmt_2023.json")):
            cases += random_cases(_read(*path), 60, seed=len(cases) + 7)
        cases.append({"rules": _read("examples", "tufs_rules.json"), "grades": _read("examples", "grades.csv"),
                      "plan": _read("examples", "plan.csv"), "years": 2, "entry_year": 2024})
        p = subprocess.run([NODE, os.path.join(HERE, "web_parity.mjs")], input=json.dumps(cases, ensure_ascii=False),
                           capture_output=True, text=True, encoding="utf-8", check=True)
        js = json.loads(p.stdout)
        self.assertEqual(len(js), len(cases))
        for i, (case, out) in enumerate(zip(cases, js)):
            py = python_side(case)
            self.assertNotIn("error", py, f"case {i}: python failed: {py.get('error')}")
            self.assertNotIn("error", out, f"case {i}: js failed: {out.get('error')}")
            self.assertEqual(py["ok"], out["ok"], f"case {i} differs")
            self.assertEqual(py["text"], out["text"], f"case {i}: report text differs")


if __name__ == "__main__":
    unittest.main()
