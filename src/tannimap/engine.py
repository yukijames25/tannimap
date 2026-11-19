"""Check courses against the rules: which category each credit counts toward, what is short, and why.

Two scenarios are computed: "now" (passed courses only) and "plan" (also courses in progress and
planned). Every credit that does not count says why (a cap, a limit, a course that never counts),
with the handbook page, because "why is my shortfall 42 and not 32?" is what students cannot work out.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

from .model import (FAILED, IN_PROGRESS, PASSED, PLANNED, WITHDRAWN, Category, Course, Rules, norm,
                    overflow_edges)

SCENARIOS = {"now": (PASSED,), "plan": (PASSED, IN_PROGRESS, PLANNED)}
STATUS_ORDER = {PASSED: 0, IN_PROGRESS: 1, PLANNED: 2}
EPS = 1e-9


@dataclass
class Item:
    course: Course
    credits: float
    via: str = ""           # category id it overflowed from, if any


@dataclass
class Dropped:
    course: Course
    credits: float
    reason: str
    page: str = ""


@dataclass
class CatResult:
    cat: Category
    counted: float = 0.0
    items: list = field(default_factory=list)       # Item counted here (including from children)
    dropped: list = field(default_factory=list)     # Dropped: credits that count nowhere because of this category
    moved_out: list = field(default_factory=list)   # (to_id, credits, course)
    conditions: list = field(default_factory=list)  # (name, have, min, page)
    same_group: tuple | None = None                  # (name, best_key, have, min, ok, details, page)
    required: list = field(default_factory=list)     # (requirement, course or None, note)
    alternatives: list = field(default_factory=list)  # dicts from _alternative

    @property
    def shortfall(self) -> float:
        return max(0.0, self.cat.min - self.counted)

    child_shortfall: float = 0.0   # sum of the children's shortfalls (set by run_scenario)

    @property
    def problems(self) -> list:
        return [t for _k, t in self.problem_items]

    @property
    def problem_items(self) -> list:
        """(key, text): the key names the problem without its amount, to compare scenarios."""
        out = []
        if self.cat.counts and self.shortfall > EPS and self.shortfall > self.child_shortfall + EPS:
            out.append(("short", f"{_n(self.shortfall)}単位不足"))
        out += [(f"cond:{n}", f"{n}: {_n(m - h)}単位不足") for n, h, m, _p in self.conditions if h + EPS < m]
        if self.same_group and not self.same_group[4]:
            name, key, have, need, _ok, conds, _p = self.same_group
            where = f"最も近い「{key}」で{_n(have)}単位" if key else "該当する科目なし"
            lack = "、".join(f"{n} {_n(m - h)}単位" for n, h, m in conds if h + EPS < m)
            out.append(("group", f"{name}（{_n(need)}単位以上）を満たしていない — {where}" + (f"、不足: {lack}" if lack else "")))
        if self.alternatives and not any(a["ok"] for a in self.alternatives):
            best = max(self.alternatives, key=lambda a: (a["progress"], -len(a["missing"])))
            others = [a["name"] for a in self.alternatives if a is not best]
            out.append(("alt", f"どの方法も満たしていない。最も近いのは「{best['name']}」で、{'；'.join(best['missing'])}"
                        + (f"（ほかの方法: {'・'.join(others)}）" if others else "")))
        out += [(f"req:{req}", f"必修「{req}」が{note}") for req, c, note in self.required if c is None or note]
        return out


@dataclass
class Scenario:
    name: str
    cats: dict                      # id -> CatResult
    total: float
    unmatched: list                 # courses no category takes
    not_counted: list               # (course, category) for counts=False categories
    out_of_scope: list = field(default_factory=list)  # (course, category) for out_of_scope categories


def _n(x: float) -> str:
    return str(int(x)) if abs(x - round(x)) < EPS else f"{x:g}"


def _order(r: Rules) -> list:
    """Categories so that children come before parents and overflow sources before targets."""
    deps: dict[str, set] = {c.id: set() for c in r.walk()}
    for c in r.walk():
        for ch in c.children:
            deps[c.id].add(ch.id)
    for a, b in overflow_edges(r):
        deps[b].add(a)
    out, state = [], {}

    def visit(cid, path):
        if state.get(cid) == 2:
            return
        if state.get(cid) == 1:
            raise ValueError("categories depend on each other in a circle: " + " → ".join(path + [cid]))
        state[cid] = 1
        for d in sorted(deps[cid], key=lambda x: list(r.by_id).index(x)):
            visit(d, path + [cid])
        state[cid] = 2
        out.append(r.by_id[cid])

    for c in r.walk():
        visit(c.id, [])
    return out


def _pools(r: Rules):
    """Order in which categories claim courses: children before their parent, siblings in file order."""
    def rec(cs):
        for c in cs:
            yield from rec(c.children)
            if c.match is not None:
                yield c
    return list(rec(r.categories))


def assign(r: Rules, courses: list) -> tuple[dict, list]:
    """Each course goes to the first category (children first) whose match takes it."""
    pools = _pools(r)
    taken: dict[str, list] = {c.id: [] for c in r.walk()}
    unmatched = []
    for c in courses:
        hit = next((p for p in pools if p.match.hits(c)), None)
        if hit is None:
            unmatched.append(c)
        else:
            taken[hit.id].append(c)
    return taken, unmatched


def _name_key(cat: Category, c: Course) -> str:
    """What counts as "the same course" for per_name_max."""
    if cat.per_name_key:
        m = re.search(unicodedata.normalize("NFKC", cat.per_name_key), unicodedata.normalize("NFKC", c.name))
        if m:
            return norm(m.group(1))
    return norm(c.name)


def _sort_key(it: Item):
    c = it.course
    return (STATUS_ORDER.get(c.status, 9), str(c.year), str(c.term), c.row)


def run_scenario(r: Rules, courses: list, name: str) -> Scenario:
    keep = SCENARIOS[name]
    pool = [c for c in courses if c.status in keep and c.credits > 0]
    taken, unmatched = assign(r, pool)
    incoming: dict[str, list] = {c.id: [] for c in r.walk()}
    results: dict[str, CatResult] = {}
    not_counted, out_scope = [], []
    for cat in _order(r):
        res = CatResult(cat)
        results[cat.id] = res
        if cat.out_of_scope:
            out_scope += [(c, cat) for c in taken[cat.id]]
            continue
        if not cat.counts:
            not_counted += [(c, cat) for c in taken[cat.id]]
            continue
        items = []
        for ch in cat.children:
            items += [Item(i.course, i.credits, i.via) for i in results[ch.id].items] if results[ch.id].cat.counts else []
        items += [Item(c, c.credits) for c in taken[cat.id]]
        items += incoming[cat.id]
        items.sort(key=_sort_key)
        used_limit = {id(lim): 0.0 for lim in cat.limits}
        moved = {id(lim): 0.0 for lim in cat.limits}
        moved_max = 0.0
        per_name: dict[str, float] = {}
        for it in items:
            room, binding = it.credits, None
            capped_name = cat.per_name_max is not None and not (cat.per_name_exclude and cat.per_name_exclude.hits(it.course))
            name_key = _name_key(cat, it.course) if capped_name else ""
            if capped_name:
                left = cat.per_name_max - per_name.get(name_key, 0.0)
                if left < room - EPS:
                    room, binding = max(0.0, left), "name"
            for lim in cat.limits:
                if lim.match.hits(it.course):
                    left = lim.max - used_limit[id(lim)]
                    if left < room - EPS:
                        room, binding = max(0.0, left), lim
            if cat.max is not None:
                left = cat.max - res.counted
                if left < room - EPS:
                    room, binding = max(0.0, left), cat
            take = min(it.credits, room)
            if take > EPS:
                res.items.append(Item(it.course, take, it.via))
                res.counted += take
                if capped_name:
                    per_name[name_key] = per_name.get(name_key, 0.0) + take
                for lim in cat.limits:
                    if lim.match.hits(it.course):
                        used_limit[id(lim)] += take
            rest = it.credits - take
            if rest <= EPS:
                continue
            if binding == "name":
                res.dropped.append(Dropped(it.course, rest, f"{cat.name}では同じ授業科目は{_n(cat.per_name_max)}単位まで"
                                                            "。卒業単位に含まれない", cat.page))
                continue
            if binding is cat:
                to, cap, page, why = cat.overflow_to, cat.overflow_max, cat.page, f"{cat.name}は{_n(cat.max)}単位までしか算入されない"
                already = moved_max
            else:
                to, cap, page, why = binding.overflow_to, binding.overflow_max, binding.page or cat.page, \
                    f"{cat.name}のうち「{binding.name}」は{_n(binding.max)}単位まで"
                already = moved[id(binding)]
            send = 0.0
            if to:
                send = rest if cap is None else max(0.0, min(rest, cap - already))
                if send > EPS:
                    incoming[to].append(Item(it.course, send, cat.id))
                    res.moved_out.append((to, send, it.course))
                    if binding is cat:
                        moved_max += send
                    else:
                        moved[id(binding)] += send
            lost = rest - send
            if lost > EPS:
                tail = f"（{r.by_id[to].name}へは{_n(cap)}単位まで）" if to and cap is not None else ""
                res.dropped.append(Dropped(it.course, lost, why + tail + "。卒業単位に含まれない", page))
        _check(cat, res, courses, keep)
        res.child_shortfall = sum(results[ch.id].shortfall for ch in cat.children if ch.counts)
    total = sum(results[c.id].counted for c in r.categories if c.counts)
    return Scenario(name, results, total, unmatched, not_counted, out_scope)


def _same_group(sg, items: list, page: str) -> tuple:
    """(name, best key, credits in it, min, ok, [(condition, have, min)], page)."""
    pat = re.compile(unicodedata.normalize("NFKC", sg.key_pattern))
    groups: dict[str, list] = {}
    for i in items:
        m = pat.search(unicodedata.normalize("NFKC", i.course.name))
        if m:
            groups.setdefault(m.group(1), []).append(i)
    best = None
    for key, its in groups.items():
        have = sum(i.credits for i in its)
        conds = [(c.name, sum(i.credits for i in its if c.match.hits(i.course)), c.min) for c in sg.conditions]
        ok = have + EPS >= sg.min and all(h + EPS >= m for _x, h, m in conds)
        # closest first: satisfied, then least missing, then most credits
        missing = max(0.0, sg.min - have) + sum(max(0.0, m - h) for _x, h, m in conds)
        score = (ok, -missing, have)
        if best is None or score > best[0]:
            best = (score, key, have, ok, conds)
    if best is None:
        return (sg.name, None, 0.0, sg.min, False, [], sg.page or page)
    _s, key, have, ok, conds = best
    return (sg.name, key, have, sg.min, ok, conds, sg.page or page)


def _alternative(alt, items: list, page: str) -> dict:
    conds = [(c.name, sum(i.credits for i in items if c.match.hits(i.course)), c.min, c.page or alt.page or page)
             for c in alt.conditions]
    sg = _same_group(alt.same_group, items, alt.page or page) if alt.same_group else None
    missing = [f"{n} {_n(m - h)}単位不足" for n, h, m, _p in conds if h + EPS < m]
    if sg and not sg[4]:
        name, key, have, need, _ok, sconds, _p = sg
        lack = [f"{n} {_n(m - h)}" for n, h, m in sconds if h + EPS < m]
        where = f"最も近い「{key}」で{_n(have)}単位" if key else "該当する科目なし"
        missing.append(f"{name}（{_n(need)}単位以上）に届かない — {where}" + (f"、不足: {'、'.join(lack)}" if lack else ""))
    return {"name": alt.name, "ok": not missing, "missing": missing, "page": alt.page or page,
            "progress": sum(h for _n2, h, _m, _p in conds) + (sg[2] if sg else 0)}


def _check(cat: Category, res: CatResult, all_courses: list, keep: tuple):
    for cond in cat.conditions:
        have = sum(i.credits for i in res.items if cond.match.hits(i.course))
        res.conditions.append((cond.name, have, cond.min, cond.page or cat.page))
    if cat.same_group:
        res.same_group = _same_group(cat.same_group, res.items, cat.page)
    if cat.alternatives:
        alts = [_alternative(a, res.items, cat.page) for a in cat.alternatives]
        res.alternatives = alts
    for req in cat.required:
        hit = next((i.course for i in res.items if _req_hit(req, i.course)), None)
        if hit is not None:
            note = "" if hit.status == PASSED else ("履修中" if hit.status == IN_PROGRESS else "予定のみ")
            note = "" if keep != (PASSED,) and hit.status in keep else note
            res.required.append((req, hit, note))
            continue
        later = next((c for c in all_courses if _req_hit(req, c) and c.status in (IN_PROGRESS, PLANNED)), None)
        failed = next((c for c in all_courses if _req_hit(req, c) and c.status in (FAILED, WITHDRAWN)), None)
        if later is not None:  # outside this scenario: registered or planned, just not earned yet
            res.required.append((req, None, "履修中（まだ修得していない）" if later.status == IN_PROGRESS
                                 else "予定のみ（まだ登録していない）"))
        elif failed is not None:
            res.required.append((req, None, "不合格のまま（再履修が必要）"))
        else:
            res.required.append((req, None, "未修得・未登録"))


def _req_hit(req: str, c: Course) -> bool:
    if req.startswith("re:"):
        return re.search(unicodedata.normalize("NFKC", req[3:]), unicodedata.normalize("NFKC", c.name)) is not None
    return norm(req) == norm(c.name)


# ---- GPA / progression / JASSO --------------------------------------------
def gpa(r: Rules, courses: list) -> dict:
    if not r.gpa_points:
        return {"gpa": None, "points": 0.0, "credits": 0.0, "used": 0, "skipped": [], "no_scale": True}
    pts = {norm(k): v for k, v in r.gpa_points.items()}
    excl = {norm(x) for x in r.gpa_exclude}
    num = den = 0.0
    used, skipped = [], []
    for c in courses:
        if c.status not in (PASSED, FAILED) or c.credits <= 0:
            continue
        g = norm(c.grade)
        if g in excl or g not in pts:
            skipped.append(c)
            continue
        num += pts[g] * c.credits
        den += c.credits
        used.append(c)
    return {"gpa": round(num / den, 2) if den else None, "points": num, "credits": den,
            "used": len(used), "skipped": [(c.name, c.grade) for c in skipped]}


def _year_of_study(c: Course, entry_year: int | None):
    try:
        return int(str(c.year).strip()[:4]) - entry_year + 1 if entry_year else None
    except ValueError:
        return None


def progression(r: Rules, sc: Scenario, courses: list, entry_year: int | None, keep: tuple) -> list:
    """Each line is (label, have, need); have is None when it cannot be judged (ok is then None too)."""
    out = []
    for p in r.progression:
        lines = []
        if "min_total" in p:
            lines.append(("合計（卒業単位に数える単位）", sc.total, float(p["min_total"])))
        for cid, m in (p.get("categories") or {}).items():
            lines.append((r.by_id[cid].name, sc.cats[cid].counted, float(m)))
        iy = p.get("in_year")
        if iy:
            year, need = int(iy["year"]), float(iy["min"])
            label = f"{year}年次に修得した単位"
            if entry_year is None:
                lines.append((label + "（入学年度が必要）", None, need))
            else:
                have = sum(c.credits for c in courses
                           if c.status in keep and _year_of_study(c, entry_year) == year)
                lines.append((label, have, need))
        ok = None if any(h is None for _x, h, _m in lines) else all(h + EPS >= m for _x, h, m in lines)
        out.append({"name": str(p.get("name", "進級要件")), "page": str(p.get("page", "")),
                    "note": str(p.get("note", "")), "lines": lines, "ok": ok})
    return out


def unseen_labels(r: Rules, courses: list) -> list:
    """(category, label) for labels in the rules that no course in the transcript has.

    A misspelled or guessed 区分 name silently counts as 0 credits, so the student must see these."""
    seen = {norm(c.label) for c in courses if c.label}
    out = []
    for cat in r.walk():
        if cat.match is None:
            continue
        for lab in cat.match.labels:
            if norm(lab) not in seen:
                out.append((cat, lab))
    return out


def jasso(r: Rules, courses: list, sc_now: Scenario, years_enrolled: float | None) -> dict | None:
    """JASSO grant scholarship: warning at <=70% of the standard credits, cancellation at <=60%.

    standard = credits needed to graduate / standard years x years enrolled (how universities state it).
    Only the credit criterion can be judged here; GPA rank and attendance need university data.
    """
    if not (r.standard_years and years_enrolled):
        return None
    standard = r.total_min / r.standard_years * years_enrolled
    earned_all = sum(c.credits for c in courses if c.status == PASSED)
    out = {"standard": standard, "counted": sc_now.total, "earned_all": earned_all}
    for key, have in (("counted", sc_now.total), ("earned_all", earned_all)):
        ratio = have / standard if standard else 0
        out[key + "_ratio"] = ratio
        out[key + "_level"] = "廃止の基準（6割以下）" if ratio <= 0.6 + EPS else \
            "警告の基準（7割以下）" if ratio <= 0.7 + EPS else "基準より上"
    return out


def check(r: Rules, courses: list, years_enrolled: float | None = None, entry_year: int | None = None) -> dict:
    now = run_scenario(r, courses, "now")
    plan = run_scenario(r, courses, "plan")
    return {"now": now, "plan": plan, "gpa": gpa(r, courses),
            "progression_now": progression(r, now, courses, entry_year, SCENARIOS["now"]),
            "progression_plan": progression(r, plan, courses, entry_year, SCENARIOS["plan"]),
            "jasso": jasso(r, courses, now, years_enrolled), "unseen_labels": unseen_labels(r, courses)}
