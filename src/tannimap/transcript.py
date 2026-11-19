"""Read a transcript (成績表) or a course plan: CSV, TSV, or a table copied from the portal.

Columns are found by their header names, which differ by university:
    科目名 / 授業科目名 / 科目 / course      区分 / 科目区分 / 分類 / category
    単位 / 単位数 / 単位数(修得) / credits    評価 / 成績 / 評語 / grade
    年度 / year    学期 / 期 / term    状態 / status (履修中・予定 …)
"""
from __future__ import annotations

import csv
import io
import re
import unicodedata

from .model import FAILED, IN_PROGRESS, PASSED, PLANNED, WITHDRAWN, Course, Rules, norm


class TranscriptError(ValueError):
    pass


ALIASES = {
    "name": ["科目名", "授業科目名", "授業科目", "科目", "授業名", "科目名称", "course", "coursename", "subject", "title"],
    "label": ["区分", "科目区分", "分類", "授業科目区分", "科目群", "系列", "category", "group", "type"],
    "credits": ["単位", "単位数", "修得単位", "修得単位数", "単位数(修得)", "credits", "credit", "units"],
    "grade": ["評価", "成績", "評語", "評点", "grade", "result"],
    "year": ["年度", "修得年度", "履修年度", "year"],
    "term": ["学期", "期", "開講期", "履修期", "term", "semester"],
    "status": ["状態", "ステータス", "履修状況", "status"],
}
IN_PROGRESS_WORDS = ["履修中", "登録済", "登録中", "受講中", "inprogress", "registered", "taking"]
PLANNED_WORDS = ["予定", "計画", "履修予定", "登録予定", "plan", "planned"]
WITHDRAWN_WORDS = ["放棄", "取消", "取り消し", "辞退", "w", "withdrawn", "中止"]


def _header_map(row: list) -> dict:
    found = {}
    for i, cell in enumerate(row):
        h = norm(cell)
        for key, names in ALIASES.items():
            if key in found:
                continue
            if any(h == norm(n) for n in names):
                found[key] = i
    return found


def _split(text: str) -> list:
    lines = [ln for ln in text.replace("\r\n", "\n").replace("\r", "\n").split("\n") if ln.strip()]
    if not lines:
        return []
    sample = "\n".join(lines[:20])
    if "\t" in sample:
        return [ln.split("\t") for ln in lines]
    try:
        return list(csv.reader(io.StringIO("\n".join(lines))))
    except csv.Error as e:
        raise TranscriptError(f"could not read the table: {e}") from None


def _status(grade: str, status_cell: str, r: Rules | None) -> str:
    s, g = norm(status_cell), norm(grade)
    for words, st in ((PLANNED_WORDS, PLANNED), (IN_PROGRESS_WORDS, IN_PROGRESS), (WITHDRAWN_WORDS, WITHDRAWN)):
        if s and any(norm(w) == s or norm(w) in s for w in words):
            return st
        if g and any(norm(w) == g for w in words):
            return st
    if not g:
        return IN_PROGRESS
    passes = [norm(x) for x in (r.grading_pass if r else [])]
    fails = [norm(x) for x in (r.grading_fail if r else [])]
    if g in fails:
        return FAILED
    if g in passes:
        return PASSED
    if re.fullmatch(r"\d+(\.\d+)?", g):  # a numeric score: 60 and above usually passes
        return PASSED if float(g) >= 60 else FAILED
    raise TranscriptError(f"unknown grade {grade!r}: add it to grading.pass or grading.fail in the rules")


def parse_transcript(text: str, rules: Rules | None = None, default_status: str | None = None) -> list:
    """Courses from a table. default_status="planned" reads a plan where the grade column is empty."""
    rows = _split(unicodedata.normalize("NFKC", text.lstrip("﻿")))
    head_at, cols = None, {}
    for i, row in enumerate(rows[:15]):
        m = _header_map(row)
        if "name" in m and "credits" in m:
            head_at, cols = i, m
            break
    if head_at is None:
        raise TranscriptError("no header row with a course name column (科目名) and a credits column (単位数) "
                              "in the first 15 lines")
    courses = []
    for n, row in enumerate(rows[head_at + 1:], start=head_at + 2):
        def cell(key):
            i = cols.get(key)
            return row[i].strip() if i is not None and i < len(row) else ""
        name = cell("name")
        if not name or norm(name) in ("合計", "計", "小計", "total"):
            continue
        raw = cell("credits")
        if not raw:
            continue
        try:
            credits = float(raw)
        except ValueError:
            raise TranscriptError(f"line {n}: credits {raw!r} is not a number") from None
        grade = cell("grade")
        status = cell("status")
        if default_status == PLANNED and not grade and not status:
            st = PLANNED
        else:
            st = _status(grade, status, rules)
        courses.append(Course(name=name, credits=credits, label=cell("label"), grade=grade, status=st,
                              year=cell("year"), term=cell("term"), row=n))
    if not courses:
        raise TranscriptError("the table has a header but no course rows")
    return courses
