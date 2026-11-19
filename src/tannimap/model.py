"""Rules (from a university handbook) and courses (from a transcript), and how they match."""
from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass, field

SCHEMA = "tannimap/1"


class RulesError(ValueError):
    """The rules file is malformed."""


def norm(text) -> str:
    """Normalise for matching: NFKC (Ａ→A, ２→2), no spaces, lower-case Latin."""
    s = unicodedata.normalize("NFKC", str(text or ""))
    return re.sub(r"\s+", "", s).lower()


# ---- courses ---------------------------------------------------------------
PASSED, FAILED, IN_PROGRESS, PLANNED, WITHDRAWN = "passed", "failed", "in_progress", "planned", "withdrawn"
STATUSES = (PASSED, FAILED, IN_PROGRESS, PLANNED, WITHDRAWN)


@dataclass
class Course:
    name: str
    credits: float
    label: str = ""          # the 科目区分 printed on the transcript
    grade: str = ""
    status: str = PASSED
    year: str = ""
    term: str = ""
    row: int = 0             # line in the input, for messages

    @property
    def key(self) -> str:
        return f"{self.name}#{self.row}"


# ---- matching --------------------------------------------------------------
@dataclass
class Match:
    labels: list = field(default_factory=list)          # exact 区分 names
    label_patterns: list = field(default_factory=list)  # regex on 区分
    names: list = field(default_factory=list)           # exact course names
    name_patterns: list = field(default_factory=list)   # regex on course name
    exclude_names: list = field(default_factory=list)
    exclude_patterns: list = field(default_factory=list)

    @classmethod
    def parse(cls, d, where: str) -> "Match | None":
        if d is None:
            return None
        if not isinstance(d, dict):
            raise RulesError(f"{where}: match must be an object")
        unknown = set(d) - {"labels", "label_patterns", "names", "name_patterns", "exclude_names", "exclude_patterns"}
        if unknown:
            raise RulesError(f"{where}: unknown match keys {sorted(unknown)}")
        m = cls(**{k: _strs(v, f"{where}.{k}") for k, v in d.items()})
        for p in m.label_patterns + m.name_patterns + m.exclude_patterns:
            try:
                re.compile(unicodedata.normalize("NFKC", p))
            except re.error as e:
                raise RulesError(f"{where}: bad pattern {p!r}: {e}") from None
        if not (m.labels or m.label_patterns or m.names or m.name_patterns):
            raise RulesError(f"{where}: match needs labels, label_patterns, names or name_patterns")
        return m

    def hits(self, c: Course) -> bool:
        name, label = norm(c.name), norm(c.label)
        if any(norm(x) == name for x in self.exclude_names):
            return False
        if any(_search(p, c.name) for p in self.exclude_patterns):
            return False
        return (any(norm(x) == label for x in self.labels) and bool(label)) \
            or any(_search(p, c.label) for p in self.label_patterns) \
            or any(norm(x) == name for x in self.names) \
            or any(_search(p, c.name) for p in self.name_patterns)


def _search(pattern: str, text: str) -> bool:
    return re.search(unicodedata.normalize("NFKC", pattern), unicodedata.normalize("NFKC", text or "")) is not None


def _strs(v, where):
    if isinstance(v, str):
        return [v]
    if not isinstance(v, list) or not all(isinstance(x, str) for x in v):
        raise RulesError(f"{where}: must be a string or a list of strings")
    return v


# ---- rules -----------------------------------------------------------------
@dataclass
class Condition:
    name: str
    match: Match
    min: float
    page: str = ""


@dataclass
class Limit:
    name: str
    match: Match
    max: float
    overflow_to: str = ""
    overflow_max: float | None = None
    page: str = ""


@dataclass
class SameGroup:
    """"6 credits in ONE language": courses are grouped by a key taken from their name."""
    name: str
    key_pattern: str          # regex with one group, e.g. "教養外国語(.+?)[AB]"
    min: float
    conditions: list = field(default_factory=list)
    page: str = ""


@dataclass
class Alternative:
    """One way of meeting a category; the category is met if ANY alternative is."""
    name: str
    conditions: list = field(default_factory=list)
    same_group: "SameGroup | None" = None
    page: str = ""


@dataclass
class Category:
    id: str
    name: str
    min: float = 0
    max: float | None = None          # credits counted here at most
    overflow_to: str = ""             # where credits above max go
    overflow_max: float | None = None
    match: Match | None = None
    counts: bool = True               # False: matched courses never count toward graduation
    required: list = field(default_factory=list)   # course names / patterns that must be passed
    conditions: list = field(default_factory=list)
    limits: list = field(default_factory=list)
    same_group: SameGroup | None = None
    alternatives: list = field(default_factory=list)
    page: str = ""
    note: str = ""
    term_only: dict = field(default_factory=dict)  # course -> "春学期のみ登録可" etc.
    per_name_max: float | None = None   # 「同一授業科目は1授業2単位まで」: credits per course name
    per_name_exclude: Match | None = None
    children: list = field(default_factory=list)
    parent: "Category | None" = None


@dataclass
class Rules:
    university: str
    faculty: str
    entry_years: str
    total_min: float
    total_page: str
    categories: list
    grading_pass: list
    grading_fail: list
    gpa_points: dict
    gpa_exclude: list
    standard_years: int | None
    progression: list
    ask_office: list
    notes: list
    source: dict
    by_id: dict

    def walk(self):
        """Categories depth-first, parents before children."""
        def rec(cs):
            for c in cs:
                yield c
                yield from rec(c.children)
        yield from rec(self.categories)


def _num(v, where, allow_none=False):
    if v is None and allow_none:
        return None
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise RulesError(f"{where}: must be a number")
    if v < 0:
        raise RulesError(f"{where}: must not be negative")
    return float(v)


def _page(d) -> str:
    p = d.get("page", "")
    return "" if p is None else str(p)


CAT_KEYS = {"id", "name", "min", "max", "overflow", "match", "counts", "required", "conditions", "limits",
            "same_group", "alternatives", "page", "note", "term_only", "children", "per_name_max", "per_name_exclude"}


def _conditions(lst, where) -> list:
    return [Condition(name=str(x.get("name", f"条件{i + 1}")), match=Match.parse(x.get("match"), f"{where}[{i}]"),
                      min=_num(x.get("min"), f"{where}[{i}].min"), page=_page(x))
            for i, x in enumerate(lst or [])]


def _same_group(sg, where) -> "SameGroup | None":
    if not sg:
        return None
    try:
        pat = re.compile(unicodedata.normalize("NFKC", sg["key_pattern"]))
    except (KeyError, re.error) as e:
        raise RulesError(f"{where}: key_pattern missing or invalid ({e})") from None
    if pat.groups < 1:
        raise RulesError(f"{where}: key_pattern needs one (group) for the key")
    return SameGroup(name=str(sg.get("name", "同一グループ")), key_pattern=sg["key_pattern"],
                     min=_num(sg.get("min"), f"{where}.min"), page=_page(sg),
                     conditions=_conditions(sg.get("conditions"), f"{where}.conditions"))


def _category(d, where, parent=None) -> Category:
    if not isinstance(d, dict):
        raise RulesError(f"{where}: a category must be an object")
    unknown = set(d) - CAT_KEYS
    if unknown:
        raise RulesError(f"{where}: unknown keys {sorted(unknown)} (allowed: {sorted(CAT_KEYS)})")
    if not d.get("id") or not d.get("name"):
        raise RulesError(f"{where}: id and name are required")
    where = f"category {d['id']}"
    ov = d.get("overflow") or {}
    c = Category(
        id=str(d["id"]), name=str(d["name"]),
        min=_num(d.get("min", 0), f"{where}.min"),
        max=_num(d.get("max"), f"{where}.max", True),
        overflow_to=str(ov.get("to", "")) if ov else "",
        overflow_max=_num(ov.get("max"), f"{where}.overflow.max", True) if ov else None,
        match=Match.parse(d.get("match"), where),
        counts=bool(d.get("counts", True)),
        required=_strs(d.get("required", []), f"{where}.required"),
        page=_page(d), note=str(d.get("note", "")),
        term_only={str(k): str(v) for k, v in (d.get("term_only") or {}).items()},
        per_name_max=_num(d.get("per_name_max"), f"{where}.per_name_max", True),
        per_name_exclude=Match.parse(d.get("per_name_exclude"), f"{where}.per_name_exclude"),
        parent=parent,
    )
    if c.overflow_to and c.max is None:
        raise RulesError(f"{where}: overflow needs max (the credits kept here)")
    c.conditions = _conditions(d.get("conditions"), f"{where}.conditions")
    for i, x in enumerate(d.get("alternatives", [])):
        alt = Alternative(name=str(x.get("name", f"方法{i + 1}")), page=_page(x),
                          conditions=_conditions(x.get("conditions"), f"{where}.alternatives[{i}].conditions"),
                          same_group=_same_group(x.get("same_group"), f"{where}.alternatives[{i}].same_group"))
        if not alt.conditions and alt.same_group is None:
            raise RulesError(f"{where}.alternatives[{i}]: needs conditions or same_group")
        c.alternatives.append(alt)
    for i, x in enumerate(d.get("limits", [])):
        lo = x.get("overflow") or {}
        c.limits.append(Limit(name=str(x.get("name", f"上限{i + 1}")),
                              match=Match.parse(x.get("match"), f"{where}.limits[{i}]"),
                              max=_num(x.get("max"), f"{where}.limits[{i}].max"),
                              overflow_to=str(lo.get("to", "")) if lo else "",
                              overflow_max=_num(lo.get("max"), f"{where}.limits[{i}].overflow.max", True) if lo else None,
                              page=_page(x)))
    c.same_group = _same_group(d.get("same_group"), f"{where}.same_group")
    c.children = [_category(x, f"{where}.children[{i}]", c) for i, x in enumerate(d.get("children", []))]
    if not c.children and c.match is None:
        raise RulesError(f"{where}: a category without children needs match (which courses belong to it)")
    return c


DEFAULT_PASS = ["S", "A+", "A", "B", "C", "秀", "優", "良", "可", "合", "合格", "認", "認定", "P"]
DEFAULT_FAIL = ["D", "F", "不可", "否", "不合格", "×", "E", "X"]
DEFAULT_GPA = {"S": 4, "A+": 4, "A": 3, "B": 2, "C": 1, "D": 0, "F": 0, "秀": 4, "優": 3, "良": 2, "可": 1, "不可": 0}


def load_rules(data) -> Rules:
    if isinstance(data, (str, bytes)):
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            raise RulesError(f"rules file is not valid JSON: line {e.lineno}: {e.msg}") from None
    if not isinstance(data, dict):
        raise RulesError("rules must be a JSON object")
    if data.get("schema", SCHEMA) != SCHEMA:
        raise RulesError(f"unknown schema {data.get('schema')!r}; expected {SCHEMA}")
    total = data.get("total") or {}
    if "min" not in total:
        raise RulesError("total.min (credits needed to graduate) is required")
    cats = [_category(x, f"categories[{i}]") for i, x in enumerate(data.get("categories") or [])]
    if not cats:
        raise RulesError("categories is empty")
    g = data.get("grading") or {}
    r = Rules(
        university=str(data.get("university", "")), faculty=str(data.get("faculty", "")),
        entry_years=str(data.get("entry_years", "")),
        total_min=_num(total["min"], "total.min"), total_page=_page(total),
        categories=cats,
        grading_pass=_strs(g.get("pass", DEFAULT_PASS), "grading.pass"),
        grading_fail=_strs(g.get("fail", DEFAULT_FAIL), "grading.fail"),
        # no default scale: a GPA on someone else's points would look right and be wrong
        gpa_points={str(k): float(v) for k, v in g["gpa"].items()} if g.get("gpa") else None,
        gpa_exclude=_strs(g.get("gpa_exclude", ["認", "認定", "合", "合格", "P", "否", "不合格"]), "grading.gpa_exclude"),
        standard_years=int(data["standard_years"]) if data.get("standard_years") else None,
        progression=list(data.get("progression") or []),
        ask_office=_strs(data.get("ask_office", []), "ask_office"),
        notes=_strs(data.get("notes", []), "notes"),
        source=dict(data.get("source") or {}),
        by_id={},
    )
    for c in r.walk():
        if c.id in r.by_id:
            raise RulesError(f"duplicate category id {c.id!r}")
        r.by_id[c.id] = c
    for c in r.walk():
        targets = [(c.overflow_to, f"category {c.id}.overflow")] + \
                  [(lim.overflow_to, f"category {c.id}.limits[{lim.name}].overflow") for lim in c.limits]
        for t, where in targets:
            if t and t not in r.by_id:
                raise RulesError(f"{where}: no category with id {t!r}")
            if t and not r.by_id[t].counts:
                raise RulesError(f"{where}: cannot overflow into {t!r}, which does not count")
    _check_cycles(r)
    for i, p in enumerate(r.progression):
        unknown = set(p) - {"name", "min_total", "categories", "in_year", "page", "note"}
        if unknown:
            raise RulesError(f"progression[{i}]: unknown keys {sorted(unknown)} "
                             "(allowed: name, min_total, categories, in_year, page, note)")
        for cid in (p.get("categories") or {}):
            if cid not in r.by_id:
                raise RulesError(f"progression[{i}]: no category with id {cid!r}")
        iy = p.get("in_year")
        if iy is not None and (not isinstance(iy, dict) or "year" not in iy or "min" not in iy):
            raise RulesError(f"progression[{i}].in_year: write {{\"year\": 1, \"min\": 8}} (credits earned in that year of study)")
    return r


def overflow_edges(r: Rules):
    for c in r.walk():
        if c.overflow_to:
            yield c.id, c.overflow_to
        for lim in c.limits:
            if lim.overflow_to:
                yield c.id, lim.overflow_to


def _check_cycles(r: Rules):
    graph: dict[str, set] = {}
    for a, b in overflow_edges(r):
        graph.setdefault(a, set()).add(b)
    seen, stack = set(), set()

    def visit(n, path):
        if n in stack:
            raise RulesError("overflow goes round in a circle: " + " → ".join(path + [n]))
        if n in seen:
            return
        stack.add(n)
        for m in graph.get(n, ()):
            visit(m, path + [n])
        stack.discard(n)
        seen.add(n)

    for n in list(graph):
        visit(n, [])
