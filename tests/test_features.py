"""Behaviour added after the stand-in tests (each test names the finding it guards)."""
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))

from tannimap.engine import check  # noqa: E402
from tannimap.model import FAILED, PASSED, PLANNED, Course, RulesError, load_rules  # noqa: E402
from tannimap.report import explain, text_report  # noqa: E402
from tannimap.transcript import TranscriptError, parse_transcript  # noqa: E402


def data(name):
    with open(os.path.join(HERE, "data", name), encoding="utf-8") as fh:
        return json.load(fh)


def C(name, credits, label, status=PASSED, year="2025", grade="優"):
    C.row += 1
    return Course(name=name, credits=credits, label=label, grade=grade if status == PASSED else "", status=status,
                  year=year, row=C.row)


C.row = 0

BASE = {"schema": "tannimap/1", "total": {"min": 10, "page": "1"},
        "categories": [{"id": "a", "name": "A", "min": 4, "page": "1", "match": {"labels": ["A"]}},
                       {"id": "b", "name": "B", "min": 6, "page": "2", "match": {"labels": ["B"]}}]}


class Round1(unittest.TestCase):
    def test_no_gpa_without_the_universitys_points(self):  # round 1: GPA on someone else's scale
        r = load_rules(BASE)
        res = check(r, [C("x", 2, "A", grade="A")])
        self.assertIsNone(res["gpa"]["gpa"])
        self.assertIn("計算していません", text_report(r, res, [C("x", 2, "A", grade="A")]))

    def test_credits_in_a_year_of_study(self):  # round 1: 「1年次に8単位以上」
        d = dict(BASE, progression=[{"name": "1年→2年", "in_year": {"year": 1, "min": 4}, "page": "3"}])
        r = load_rules(d)
        cs = [C("x", 2, "A", year="2024"), C("y", 2, "B", year="2025")]
        self.assertIsNone(check(r, cs)["progression_now"][0]["ok"])  # entry year unknown: cannot judge
        self.assertFalse(check(r, cs, entry_year=2024)["progression_now"][0]["ok"])
        self.assertTrue(check(r, cs, entry_year=2023)["progression_now"][0]["ok"] is False)
        cs.append(C("z", 2, "A", year="2024"))
        self.assertTrue(check(r, cs, entry_year=2024)["progression_now"][0]["ok"])

    def test_labels_never_seen_are_reported(self):  # round 1: a guessed 区分 name silently counts 0
        r = load_rules(BASE)
        cs = [C("x", 4, "A")]
        res = check(r, cs)
        self.assertEqual([lab for _c, lab in res["unseen_labels"]], ["B"])
        self.assertIn("成績表に一度も出てこない区分名", text_report(r, res, cs))

    def test_progression_unknown_key_is_an_error(self):
        with self.assertRaises(RulesError):
            load_rules(dict(BASE, progression=[{"name": "x", "min_totl": 3}]))

    def test_explain_shows_questions_and_notes(self):
        r = load_rules(dict(BASE, ask_office=["Qを確認"], notes=["N"]))
        out = explain(r)
        self.assertIn("Qを確認", out)
        self.assertIn("N", out)


class Round2(unittest.TestCase):
    def test_out_of_scope_is_not_waste(self):  # round 2: excluded 専門科目 looked like wasted credits
        d = json.loads(json.dumps(BASE))
        d["categories"][1]["out_of_scope"] = True
        d["total"]["min"] = 4
        r = load_rules(d)
        cs = [C("x", 4, "A"), C("y", 6, "B")]
        res = check(r, cs)
        out = text_report(r, res, cs)
        self.assertIn("今回は照合していない区分", out)
        self.assertNotIn("卒業単位に含まれない単位", out)
        self.assertEqual(res["plan"].total, 4)

    def test_same_course_by_key(self):  # round 2: 心理学A and 心理学B as the same 授業科目
        d = json.loads(json.dumps(BASE))
        d["categories"][0].update({"per_name_max": 2, "per_name_key": "^(心理学)"})
        r = load_rules(d)
        res = check(r, [C("心理学A", 2, "A"), C("心理学B", 2, "A"), C("社会学", 2, "A")])
        self.assertEqual(res["now"].cats["a"].counted, 4)
        self.assertEqual(res["now"].cats["a"].dropped[0].course.name, "心理学B")

    def test_kagawa_answer_key(self):
        r = load_rules(data("kagawa_edu_2025.json"))
        cs = [C("心理学", 2, "学問基礎（文系）", year="2025"), C("心理学", 2, "学問基礎（文系）", year="2026"),
              C("物理学P", 2, "学問基礎（理系）"), C("物理学P", 2, "学問基礎（理系）"), C("教育学", 2, "学問基礎（文系）"),
              C("数学A", 2, "学問基礎（理系）", FAILED, grade="不可")]
        sc = check(r, cs)["now"]
        self.assertEqual(sc.cats["kiso"].counted, 6)  # 心理学 once, 物理学P twice (lab courses are exempt)
        self.assertEqual(len(sc.not_counted), 1)       # 教育学
        out = text_report(r, check(r, cs), cs)
        self.assertIn("数学A", out.split("■ 不合格の科目")[1])

    def test_unknown_grade_stops(self):  # never guess pass/fail
        r = load_rules(data("kagawa_edu_2025.json"))
        with self.assertRaises(TranscriptError):
            parse_transcript("科目名,区分,単位数,評価\nx,主題科目,2,A", r)


class Round3(unittest.TestCase):
    def test_progression_needs_specific_courses(self):
        r = load_rules(data("kumamoto_pu_mgmt_2023.json"))
        cs = [C("基礎総合管理学I", 2, "基礎総合管理"), C("基礎総合管理学II", 2, "基礎総合管理"),
              C("基礎総合管理学演習", 1, "基礎総合管理"), C("専門演習I", 2, "専門演習")]
        cs += [C(f"基幹{i}", 2, "基幹（共通）") for i in range(16)]
        res = check(r, cs, entry_year=2024)
        self.assertFalse(res["progression_now"][0]["ok"])  # プレゼミナール is missing
        cs.append(C("プレゼミナール", 1, "キャリアデザイン", PLANNED))
        res = check(r, cs, entry_year=2024)
        self.assertFalse(res["progression_now"][0]["ok"])
        self.assertTrue(res["progression_plan"][0]["ok"])
        self.assertIsNone(check(r, cs)["progression_now"][0]["ok"])  # "2年次までに" needs the entry year

    def test_until_year_counts_only_early_courses(self):  # round 3: 「2年次までに39単位」
        r = load_rules(data("kumamoto_pu_mgmt_2023.json"))
        need = ["プレゼミナール", "基礎総合管理学I", "基礎総合管理学II", "基礎総合管理学演習", "専門演習I"]
        cs = [C(n, 1, "基礎総合管理", year="2023") for n in need]
        cs += [C(f"基幹{i}", 2, "基幹（共通）", year="2023") for i in range(17)]
        self.assertTrue(check(r, cs, entry_year=2023)["progression_now"][0]["ok"])
        late = [C(n, 1, "基礎総合管理", year="2023") for n in need] +                [C(f"基幹{i}", 2, "基幹（共通）", year="2025") for i in range(17)]
        self.assertFalse(check(r, late, entry_year=2023)["progression_now"][0]["ok"])  # earned in 3rd year: too late

    def test_name_patterns_that_match_nothing_are_reported(self):  # round 3: guessed 「新熊本学」 pattern
        r = load_rules(data("kumamoto_pu_mgmt_2023.json"))
        cs = [C("地域づくり入門", 2, "地域理解とリーダーシップ")]
        res = check(r, cs)
        self.assertIn("shinkumamoto", [c.id for c in res["empty_pools"]])
        self.assertIn("科目名の条件に当てはまる科目が1つもない", text_report(r, res, cs))

    def test_other_faculty_cap_and_course_counted_elsewhere(self):
        r = load_rules(data("kumamoto_pu_mgmt_2023.json"))
        cs = [C(f"他{i}", 2, "他学部開講") for i in range(7)] + [C("基礎総合管理実践", 2, "基礎総合管理")]
        sc = check(r, cs)["now"]
        self.assertEqual(sc.cats["tenkai"].counted, 10)
        self.assertEqual(sum(d.credits for d in sc.cats["tenkai"].dropped), 4)
        self.assertEqual(sc.cats["kikan_bunya"].counted, 2)
        self.assertEqual(sc.cats["kiso"].counted, 0)


if __name__ == "__main__":
    unittest.main()
