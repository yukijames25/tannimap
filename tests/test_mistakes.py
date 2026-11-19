"""The university's own answer key: every example in TUFS's 「起こりうる単位修得ミスについて」(言語文化学部)
must come out the way the university says (2016年度以降入学者の規則)."""
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))

from tannimap.engine import check  # noqa: E402
from tannimap.model import IN_PROGRESS, PASSED, PLANNED, Course, load_rules  # noqa: E402

with open(os.path.join(HERE, "data", "tufs_lc_from_mistakes.json"), encoding="utf-8") as fh:
    RULES_JSON = json.load(fh)


def rules(**patch):
    data = json.loads(json.dumps(RULES_JSON))
    for cid, change in patch.items():
        for c in data["categories"]:
            if c["id"] == cid:
                c.update(change)
    return load_rules(data)


def C(name, credits, label="", status=PASSED):
    C.row += 1
    return Course(name=name, credits=credits, label=label, grade="A" if status == PASSED else "", status=status, row=C.row)


C.row = 0


def problems(result, cid, scenario="plan"):
    return result[scenario].cats[cid].problems


class Language(unittest.TestCase):
    def test_glip_b_missing(self):  # 例1: 英語A 6, B 0 -> Bが2単位不足
        res = check(rules(), [C("GLIP英語A1", 2), C("GLIP英語A2", 2), C("GLIP英語A3", 2)])
        p = " ".join(problems(res, "gengo"))
        self.assertIn("GLIP英語で履修", p)
        self.assertIn("GLIP英語B 2単位不足", p)

    def test_glip_a_missing(self):  # 例2: 英語A 2, B 4 -> Aが2単位不足
        res = check(rules(), [C("GLIP英語A1", 2), C("GLIP英語B1", 2), C("GLIP英語B2", 2)])
        self.assertIn("GLIP英語A 2単位不足", " ".join(problems(res, "gengo")))

    def test_glip_ok(self):
        res = check(rules(), [C("GLIP英語A1", 2), C("GLIP英語A2", 2), C("GLIP英語B1", 2)])
        self.assertEqual(problems(res, "gengo"), [])

    def test_second_language_b_short(self):  # 例3: ○○語A 5, B 1 -> Bが1単位不足
        res = check(rules(), [C("教養外国語フランス語A1", 3), C("教養外国語フランス語A2", 2), C("教養外国語フランス語B1", 1)])
        p = " ".join(problems(res, "gengo"))
        self.assertIn("教養外国語で履修", p)
        self.assertIn("フランス語", p)
        self.assertIn("中級（B） 1", p)

    def test_two_languages_do_not_add_up(self):  # 例4: ○○語A 4 + ××語B 2 -> ひとつの言語で6単位が必要
        res = check(rules(), [C("教養外国語フランス語A1", 4), C("教養外国語ドイツ語B1", 2)])
        p = " ".join(problems(res, "gengo"))
        self.assertIn("ひとつの言語で6単位", p)
        self.assertIn("フランス語」で4単位", p)

    def test_one_language_ok(self):
        res = check(rules(), [C("教養外国語フランス語A1", 4), C("教養外国語フランス語B1", 2)])
        self.assertEqual(problems(res, "gengo"), [])


class Overflow(unittest.TestCase):
    def test_regional_basics_excess_goes_to_related_since_2016(self):
        res = check(rules(), [C("地域基礎1", 4, "地域基礎"), C("地域基礎2", 4, "地域基礎")])
        self.assertEqual(res["now"].cats["chiiki_kiso"].counted, 6)
        self.assertEqual(res["now"].cats["kanren"].counted, 2)

    def test_regional_basics_excess_lost_before_2016(self):  # 2013-2015年度入学者
        r = rules(chiiki_kiso={"overflow": None})
        data = json.loads(json.dumps(RULES_JSON))
        for c in data["categories"]:
            if c["id"] == "chiiki_kiso":
                del c["overflow"]
        res = check(load_rules(data), [C("地域基礎1", 4, "地域基礎"), C("地域基礎2", 4, "地域基礎")])
        self.assertEqual(res["now"].cats["kanren"].counted, 0)
        dropped = res["now"].cats["chiiki_kiso"].dropped
        self.assertEqual(sum(d.credits for d in dropped), 2)
        del r

    def test_sports_three_credits(self):  # スポーツ3単位: 1単位は関連へ、残り1単位は算入されない
        res = check(rules(), [C("スポーツA", 1, "スポーツ・身体文化"), C("スポーツB", 1, "スポーツ・身体文化"),
                              C("スポーツC", 1, "スポーツ・身体文化")])
        now = res["now"]
        self.assertEqual(now.cats["sports"].counted, 1)
        self.assertEqual(now.cats["kanren"].counted, 1)
        self.assertEqual(sum(d.credits for d in now.cats["sports"].dropped), 1)
        self.assertIn("関連科目へは1単位まで", now.cats["sports"].dropped[0].reason)

    def test_teacher_training_never_counts(self):  # 教職科目を関連科目に含めて計算している
        res = check(rules(), [C("教育原論", 2, "教職"), C("情報技法I", 2, "情報技法"), C("関連科目X", 2, "関連")])
        self.assertEqual(res["now"].cats["kanren"].counted, 2)
        self.assertEqual(len(res["now"].not_counted), 2)


class GeneralEducation(unittest.TestCase):
    def test_world_liberal_arts_by_area(self):
        cs = [C("現代社会論", 2, "世界教養ア"), C("哲学入門", 2, "世界教養イ"), C("文学入門", 2, "世界教養イ"),
              C("芸術論", 2, "世界教養イ"), C("国際関係A", 2, "世界教養ア"), C("国際関係B", 2, "世界教養ア"),
              C("現地研修", 4, "世界教養エ")]
        res = check(rules(), cs)
        p = " ".join(problems(res, "sekai"))
        self.assertIn("区分ウ（世界から日本を見る）: 2単位不足", p)
        self.assertNotIn("区分ア", p)
        self.assertNotIn("単位不足 ", p.split("区分ウ")[0])  # total 16 is reached


class CourseSpecific(unittest.TestCase):
    def test_introduction_2016(self):  # 例1: 言語・情報4, 総合文化0, GC2 -> 総合文化が2単位不足
        res = check(rules(), [C("導入a", 4, "導入（言語・情報）"), C("導入b", 2, "導入（GC）")])
        p = problems(res, "dounyu")
        self.assertTrue(any("総合文化コース開講: 2単位不足" in x for x in p), p)

    def test_survey_courses(self):
        # 例1: 所属6（指定外6）, 他4（指定4） -> 指定科目が2単位不足
        res = check(rules(), [C("言語統計論", 6, "概論（所属コース）"), C("言語教育学概論A", 2, "概論（他コース）"),
                              C("言語教育学概論B", 2, "概論（他コース）")])
        self.assertEqual([x for x in problems(res, "gairon")], ["指定科目: 2単位不足"])
        # 例3: 所属2（指定2）, 他8（指定8） -> 所属コース開講科目が2単位不足
        res = check(rules(), [C("言語学概論A", 2, "概論（所属コース）"), C("文化・文学概論A", 2, "概論（他コース）"),
                              C("文化・文学概論B", 2, "概論（他コース）"), C("思想文化概論A", 2, "概論（他コース）"),
                              C("思想文化概論B", 2, "概論（他コース）")])
        self.assertEqual(problems(res, "gairon"), ["所属コースの開講科目: 2単位不足"])
        # 二重に数えてよい例: 所属6（指定6）, 他4（指定外） -> 満たす
        res = check(rules(), [C("言語学概論A", 2, "概論（所属コース）"), C("言語学概論B", 2, "概論（所属コース）"),
                              C("音声学概論A", 2, "概論（所属コース）"), C("概論X", 4, "概論（他コース）")])
        self.assertEqual(problems(res, "gairon"), [])

    def test_electives_other_course_cap(self):
        # 例2: 所属4, 他12 -> 他コースは10までしか含まれず、16に2単位不足
        res = check(rules(), [C("講義所属", 4, "選択（所属コース）"), C("講義他", 12, "選択（他コース）"),
                              C("卒業論文演習A", 2, "卒業論文"), C("卒業論文演習B", 2, "卒業論文"), C("卒業論文", 4, "卒業論文")])
        sc = res["now"]
        self.assertEqual(sc.cats["sentaku"].counted, 4 + 10 + 8)
        self.assertEqual(sum(d.credits for d in sc.cats["sentaku"].dropped), 2)
        self.assertIn("他コース開講の講義・演習」は10単位まで", sc.cats["sentaku"].dropped[0].reason)

    def test_other_faculty_electives_are_related(self):
        # 例3: 所属6, 他6, 国際社会学部の選択4 -> 選択は12で4単位不足、他学部の4は関連科目へ
        res = check(rules(), [C("講義所属", 6, "選択（所属コース）"), C("講義他", 6, "選択（他コース）"),
                              C("国際社会X", 4, "国際社会学部選択")])
        sc = res["now"]
        self.assertEqual(sc.cats["sentaku"].shortfall, 4)
        self.assertEqual(sc.cats["kanren"].counted, 4)

    def test_thesis_courses_must_all_be_registered(self):  # 卒論演習Aだけ登録 -> B と 卒業論文 が不足
        res = check(rules(), [C("卒業論文演習A", 2, "卒業論文", IN_PROGRESS)])
        p = problems(res, "sentaku")
        self.assertIn("必修「卒業論文演習B」が未修得・未登録", p)
        self.assertIn("必修「卒業論文」が未修得・未登録", p)
        self.assertNotIn("必修「卒業論文演習A」が未修得・未登録", p)
        now = problems(res, "sentaku", "now")
        self.assertIn("必修「卒業論文演習A」が履修中（まだ修得していない）", now)

    def test_planned_courses_close_the_gap(self):
        cs = [C("講義所属", 6, "選択（所属コース）"), C("講義他", 4, "選択（他コース）"),
              C("講義所属2", 6, "選択（所属コース）", PLANNED)]
        res = check(rules(), cs)
        self.assertEqual(res["now"].cats["sentaku"].shortfall, 6)
        self.assertEqual(res["plan"].cats["sentaku"].shortfall, 0)


if __name__ == "__main__":
    unittest.main()
