"""tannimap command line.

    tannimap check   rules.json grades.csv [--plan plan.csv] [--years 2] [--format text|md|json]
    tannimap explain rules.json          # the rules restated with pages, to check against the handbook
    tannimap validate rules.json         # errors and suspicious points in a rules file
    tannimap template rules              # an empty rules file to fill in
    tannimap template grades             # a grades table to fill in
"""
from __future__ import annotations

import argparse
import json
import sys

from . import __version__
from .engine import check
from .model import PLANNED, RulesError, load_rules
from .report import explain, json_report, text_report, validate
from .transcript import TranscriptError, parse_transcript

RULES_TEMPLATE = {
    "schema": "tannimap/1",
    "university": "○○大学", "faculty": "○○学部 ○○学科", "entry_years": "2024年度",
    "source": {"title": "2024年度 履修案内", "url": "", "checked": "YYYY-MM-DD"},
    "total": {"min": 124, "page": "12"},
    "standard_years": 4,
    "grading": {"pass": ["S", "A", "B", "C", "認定"], "fail": ["D", "F"],
                "gpa": {"S": 4, "A": 3, "B": 2, "C": 1, "D": 0, "F": 0}, "gpa_exclude": ["認定"]},
    "categories": [
        {"id": "kyoyo", "name": "教養科目", "min": 30, "page": "12", "children": [
            {"id": "eigo", "name": "英語", "min": 4, "max": 6, "page": "13",
             "overflow": {"to": "jiyu", "max": 2}, "match": {"labels": ["英語"]}},
            {"id": "kyoyo_sonota", "name": "教養その他", "min": 0, "page": "13", "match": {"labels": ["教養"]}}]},
        {"id": "senmon", "name": "専門科目", "min": 60, "page": "14", "match": {"label_patterns": ["^専門"]},
         "required": ["卒業研究"], "term_only": {"卒業研究": "春学期のみ登録可"},
         "conditions": [{"name": "専門必修", "match": {"labels": ["専門必修"]}, "min": 20, "page": "14"}],
         "limits": [{"name": "他学科の科目", "match": {"name_patterns": ["^他学科"]}, "max": 10, "page": "14"}]},
        {"id": "jiyu", "name": "自由科目", "min": 0, "max": 20, "page": "15", "match": {"labels": ["自由"]}},
        {"id": "kyoshoku", "name": "教職科目", "counts": False, "page": "16", "match": {"labels": ["教職"]}},
    ],
    "progression": [{"name": "3年→4年", "min_total": 90, "page": "17"}],
    "ask_office": [],
    "notes": [],
}
GRADES_TEMPLATE = "科目名,区分,単位数,評価,年度,学期\n英語I,英語,1,A,2024,春\n卒業研究,専門必修,4,,2026,通年\n"


def _read(path: str) -> str:
    with open(path, "rb") as fh:
        raw = fh.read()
    for enc in ("utf-8-sig", "cp932"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    raise TranscriptError(f"{path}: neither UTF-8 nor Shift_JIS")


def main(argv=None) -> int:
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(prog="tannimap", description="自分の便覧の規則で、自分の成績と履修計画を照らし合わせる",
                                 epilog=__doc__.split("\n\n", 1)[1], formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", action="version", version=f"tannimap {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("check", help="成績（と履修予定）を規則と照らし合わせる")
    p.add_argument("rules")
    p.add_argument("grades", help="成績表（CSV / TSV / ポータルからコピーした表）")
    p.add_argument("--plan", action="append", default=[], help="履修予定の表（評価欄が空なら予定として読む）")
    p.add_argument("--years", type=float, help="在学年数（給付奨学金の単位の基準を目安で出す）")
    p.add_argument("--format", choices=["text", "md", "json"], default="text")
    p = sub.add_parser("explain", help="規則を日本語で言い直す（便覧と見比べて確かめる）")
    p.add_argument("rules")
    p = sub.add_parser("validate", help="規則ファイルの誤りと怪しい点")
    p.add_argument("rules")
    p = sub.add_parser("template", help="記入用のひな形")
    p.add_argument("kind", choices=["rules", "grades"])
    a = ap.parse_args(argv)
    try:
        if a.cmd == "template":
            print(json.dumps(RULES_TEMPLATE, ensure_ascii=False, indent=2) if a.kind == "rules" else GRADES_TEMPLATE, end="")
            return 0
        rules = load_rules(_read(a.rules))
        if a.cmd == "validate":
            warns = validate(rules)
            print(f"OK: {sum(1 for _ in rules.walk())} categories, total {rules.total_min:g}")
            for w in warns:
                print(f"warning: {w}")
            return 1 if warns else 0
        if a.cmd == "explain":
            print(explain(rules))
            return 0
        courses = parse_transcript(_read(a.grades), rules)
        for path in a.plan:
            courses += parse_transcript(_read(path), rules, default_status=PLANNED)
        result = check(rules, courses, a.years)
        if a.format == "json":
            print(json.dumps(json_report(rules, result), ensure_ascii=False, indent=2))
        else:
            out = text_report(rules, result, courses)
            print(out if a.format == "text" else "```\n" + out + "\n```")
        bad = result["plan"].unmatched or any(res.problems for res in result["plan"].cats.values() if res.cat.counts) \
            or rules.total_min > result["plan"].total
        return 1 if bad else 0
    except (OSError, RulesError, TranscriptError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
