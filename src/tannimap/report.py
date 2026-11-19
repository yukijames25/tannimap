"""Human-readable output (Japanese) and JSON."""
from __future__ import annotations

import unicodedata

from .engine import EPS, Scenario, _n
from .model import IN_PROGRESS, PLANNED, Category, Rules

DISCLAIMER = ("これは便覧の規則をもとにした目安です。卒業・進級の判定は大学（教授会）が行います。"
              "気になる点は「学務に聞くこと」を持って学務・指導教員に確認してください。")


def _w(s: str) -> int:
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in s)


def _pad(s: str, width: int) -> str:
    return s + " " * max(0, width - _w(s))


def _p(page: str) -> str:
    """"12" -> （p.12）; a description such as "チェックシート 3年→4年の列" is shown as is."""
    if not page:
        return ""
    return f"（p.{page}）" if page[:1].isdigit() else f"（{page}）"


def _prog_line(n, h, m) -> str:
    if n.startswith("「"):  # a required course: shown as 修得 / 未修得
        return f"{n} {'修得' if h and h >= m else '未修得'}"
    return f"{n} {'?' if h is None else _n(h)}/{_n(m)}"


def _ok(ok) -> str:
    return "判定できない" if ok is None else "満たしている" if ok else "満たしていない"


def _in_progression(r: Rules, c: Category) -> bool:
    return any(c.id in (p.get("categories") or {}) for p in r.progression)


def _depth(c: Category) -> int:
    d = 0
    while c.parent is not None:
        d, c = d + 1, c.parent
    return d


def title(r: Rules) -> str:
    who = " ".join(x for x in (r.university, r.faculty) if x)
    years = f"（{r.entry_years}入学）" if r.entry_years else ""
    return f"{who}{years}  卒業に必要な単位 {_n(r.total_min)}{_p(r.total_page)}"


def table(r: Rules, now: Scenario, plan: Scenario) -> list:
    rows = [("区分", "必要", "修得済", "予定込み", "不足(予定込み)")]
    for c in r.walk():
        if c.out_of_scope:
            name = "  " * _depth(c) + c.name + "（今回は照合しない）"
            a = sum(x.credits for x, cat in now.out_of_scope if cat.id == c.id)
            b = sum(x.credits for x, cat in plan.out_of_scope if cat.id == c.id)
            rows.append((name, "-", _n(a), _n(b), "-"))
            continue
        if not c.counts:
            name = "  " * _depth(c) + c.name + "（算入されない）"
            a = sum(x.credits for x, cat in now.not_counted if cat.id == c.id)
            b = sum(x.credits for x, cat in plan.not_counted if cat.id == c.id)
            rows.append((name, "-", _n(a), _n(b), "-"))
            continue
        a, b = now.cats[c.id], plan.cats[c.id]
        flag = " !" if b.problem_items else ""
        name = "  " * _depth(c) + c.name + flag
        need = _n(c.min) + (f"〜{_n(c.max)}" if c.max is not None and c.max != c.min else "")
        rows.append((name, need, _n(a.counted), _n(b.counted), _n(b.shortfall) if b.shortfall > EPS else "0"))
    rows.append(("合計", _n(r.total_min), _n(now.total), _n(plan.total), _n(max(0, r.total_min - plan.total))))
    widths = [max(_w(row[i]) for row in rows) for i in range(5)]
    out = []
    for k, row in enumerate(rows):
        out.append("  ".join(_pad(row[0], widths[0]) if i == 0 else " " * (widths[i] - _w(row[i])) + row[i]
                             for i in range(5)))
        if k == 0:
            out.append("-" * (sum(widths) + 8))
    return out


def problem_items(r: Rules, sc: Scenario) -> list:
    """(key, text) for every problem; the key ignores amounts so scenarios can be compared."""
    out = []
    for c in r.walk():
        res = sc.cats[c.id]
        if not c.counts:
            continue
        for key, p in res.problem_items:
            extra = ""
            if key.startswith("req:") and key[4:] in c.term_only:
                extra = f"　※{c.term_only[key[4:]]}"
            out.append((f"{c.id}/{key}", f"{c.name}: {p}{_p(c.page)}{extra}"))
    if r.total_min - sc.total > EPS:
        out.append(("total", f"合計: {_n(r.total_min - sc.total)}単位不足{_p(r.total_page)}"))
    return out


def problems(r: Rules, sc: Scenario) -> list:
    return [t for _k, t in problem_items(r, sc)]


def _when(c) -> str:
    tag = {IN_PROGRESS: "履修中", PLANNED: "予定"}.get(c.status, "")
    year = f"{c.year}年度" if c.year else ""
    inner = "・".join(x for x in (year, tag) if x)
    return f"（{inner}）" if inner else ""


def dropped(sc: Scenario) -> list:
    out = []
    for res in sc.cats.values():
        for d in res.dropped:
            out.append(f"{d.course.name}{_when(d.course)} {_n(d.credits)}単位: {d.reason}{_p(d.page)}")
    for c, cat in sc.not_counted:
        note = f"。{cat.note}" if cat.note else ""
        out.append(f"{c.name} {_n(c.credits)}単位: 「{cat.name}」は卒業単位に含まれない{note}{_p(cat.page)}")
    return out


def moved(sc: Scenario, r: Rules) -> list:
    out = []
    for res in sc.cats.values():
        for to, cr, course in res.moved_out:
            out.append(f"{course.name} {_n(cr)}単位: {res.cat.name}の超過分として「{r.by_id[to].name}」に算入{_p(res.cat.page)}")
    return out


def text_report(r: Rules, result: dict, courses: list) -> str:
    now, plan = result["now"], result["plan"]
    L = [title(r), ""]
    n_prog = sum(1 for c in courses if c.status == IN_PROGRESS)
    n_plan = sum(1 for c in courses if c.status == PLANNED)
    L.append(f"修得済 {sum(1 for c in courses if c.status == 'passed')}科目・履修中 {n_prog}科目・予定 {n_plan}科目を読みました。")
    L.append("")
    L += table(r, now, plan)
    L.append("")
    items_now, items_plan = problem_items(r, now), problem_items(r, plan)
    L.append("■ 予定どおり修得しても残る問題" if (n_prog or n_plan) else "■ 足りないもの")
    L += [f"  ! {p}" for _k, p in items_plan] or ["  （なし）"]
    if n_prog or n_plan:
        plan_keys = {k for k, _p in items_plan}
        solved = [p for k, p in items_now if k not in plan_keys]
        if solved:
            L.append("")
            L.append("■ 今は足りないが、履修中・予定の科目を修得すれば解消するもの")
            L += [f"  - {p}" for p in solved]
    mv = moved(plan, r)
    if mv:
        L.append("")
        L.append("■ 別の区分に振り替えて数えた単位")
        L += [f"  - {x}" for x in mv]
    dr = dropped(plan)
    if dr:
        L.append("")
        L.append("■ 卒業単位に含まれない単位（修得しても数に入らない）")
        L += [f"  - {x}" for x in dr]
    fails = [c for c in courses if c.status == "failed"]
    if fails:
        L.append("")
        L.append("■ 不合格の科目（単位にならない。必修なら再履修が必要）")
        for c in fails:
            label = c.label or "区分なし"
            year = f"・{c.year}年度" if c.year else ""
            L.append(f"  - {c.name}（{label}・{_n(c.credits)}単位・{c.grade}{year}）")
    if plan.out_of_scope:
        L.append("")
        L.append("■ 今回は照合していない区分（数に入らないという意味ではない）")
        names = {}
        for c, cat in plan.out_of_scope:
            names[cat.name] = names.get(cat.name, 0.0) + c.credits
        L += [f"  - {k}: {_n(v)}単位（予定込み）" for k, v in names.items()]
    if plan.unmatched:
        L.append("")
        L.append("■ 規則にない区分の科目（どこに数えるか不明。学務に確認）")
        L += [f"  ? {c.name}（区分: {c.label or '空欄'}）{_n(c.credits)}単位" for c in plan.unmatched]
    unseen = result.get("unseen_labels") or []
    important = [(c, lab) for c, lab in unseen if c.min > 0 or _in_progression(r, c)]
    if important:
        L.append("")
        L.append("■ 成績表に一度も出てこない区分名（名前が実際と違うと、その区分は黙って0単位になる。成績表の表記と見比べる）")
        L += [f"  ? 「{lab}」（{c.name}）" for c, lab in important]
    g = result["gpa"]
    L.append("")
    if g.get("no_scale"):
        L.append("■ GPA: 規則に評語ごとの点数（grading.gpa）がないので計算していません")
    elif g["gpa"] is not None:
        skipped = f"、{len(g['skipped'])}科目は評価が数値にならないため除外" if g["skipped"] else ""
        L.append(f"■ GPA {g['gpa']:.2f}（{g['used']}科目・{_n(g['credits'])}単位で計算{skipped}）")
    has_plan = bool(n_prog or n_plan)
    for p, q in zip(result["progression_now"], result["progression_plan"]):
        L.append(f"■ {p['name']}: {_ok(p['ok'])}（修得済）" + (f"／{_ok(q['ok'])}（予定込み）" if has_plan else "")
                 + f"{_p(p['page'])}{('　' + p['note']) if p['note'] else ''}")
        src = q if has_plan else p
        L.append("    " + "、".join(_prog_line(n, h, m) for n, h, m in src["lines"])
                 + ("（予定込み）" if has_plan else ""))
    j = result["jasso"]
    if j:
        L.append(f"■ 給付奨学金の単位の基準（目安）: 標準 {_n(round(j['standard'], 1))}単位に対し、"
                 f"卒業単位に数えた修得 {_n(j['counted'])}単位（{j['counted_ratio']:.0%}・{j['counted_level']}）、"
                 f"修得した全単位 {_n(j['earned_all'])}単位（{j['earned_all_ratio']:.0%}・{j['earned_all_level']}）。"
                 "GPAの順位と出席率は大学のデータが必要なので判定していません。")
    asks = list(r.ask_office)
    if plan.unmatched:
        asks.append("規則にない区分の科目（上の「?」）が、どの区分に数えられるか")
    if any(res.dropped for res in plan.cats.values()):
        asks.append("「卒業単位に含まれない」とした単位の扱いが、この理解で正しいか")
    if asks:
        L.append("")
        L.append("■ 学務に聞くこと")
        L += [f"  - {a}" for a in asks]
    if r.notes:
        L.append("")
        L.append("■ 便覧の注意書き")
        L += [f"  - {x}" for x in r.notes]
    L.append("")
    L.append(DISCLAIMER)
    return "\n".join(L)


def json_report(r: Rules, result: dict) -> dict:
    def sc(s: Scenario):
        return {
            "total": s.total, "total_min": r.total_min,
            "categories": [{"id": c.id, "name": c.name, "min": c.min, "max": c.max, "counts": c.counts,
                            "counted": s.cats[c.id].counted, "shortfall": s.cats[c.id].shortfall if c.counts else 0,
                            "problems": s.cats[c.id].problems if c.counts else [], "page": c.page,
                            "conditions": [{"name": n, "have": h, "min": m, "page": p} for n, h, m, p in s.cats[c.id].conditions],
                            "required": [{"course": q, "found": bool(x), "note": note} for q, x, note in s.cats[c.id].required],
                            "dropped": [{"course": d.course.name, "credits": d.credits, "reason": d.reason, "page": d.page}
                                        for d in s.cats[c.id].dropped]}
                           for c in r.walk()],
            "unmatched": [{"course": c.name, "label": c.label, "credits": c.credits} for c in s.unmatched],
            "not_counted": [{"course": c.name, "credits": c.credits, "category": cat.id} for c, cat in s.not_counted],
            "problems": problems(r, s),
        }
    return {"title": title(r), "now": sc(result["now"]), "plan": sc(result["plan"]), "gpa": result["gpa"],
            "progression": result["progression_now"], "jasso": result["jasso"], "disclaimer": DISCLAIMER}


def _sg_text(sg) -> str:
    sub = "、".join(f"{x.name} {_n(x.min)}単位以上" for x in sg.conditions)
    return (f"{sg.name}: 同じグループ（科目名の {sg.key_pattern} の部分が同じもの）で{_n(sg.min)}単位以上"
            f"{'（うち ' + sub + '）' if sub else ''}{_p(sg.page)}")


def canonical(r: Rules, result: dict) -> dict:
    """Everything the browser version must reproduce exactly (used by the parity test)."""
    def sc(s: Scenario):
        return {"total": round(s.total, 4),
                "cats": {c.id: [round(s.cats[c.id].counted, 4), s.cats[c.id].problems] for c in r.walk() if c.counts},
                "problems": problems(r, s), "dropped": dropped(s), "moved": moved(s, r),
                "unmatched": [c.name for c in s.unmatched]}
    g = result["gpa"]
    return {"now": sc(result["now"]), "plan": sc(result["plan"]),
            "gpa": [g["gpa"], g["used"], round(g["credits"], 4), len(g["skipped"])],
            "progression": [[p["name"], p["ok"], [[n, h, m] for n, h, m in p["lines"]], q["ok"]]
                            for p, q in zip(result["progression_now"], result["progression_plan"])],
            "unseen": [[c.id, lab] for c, lab in result["unseen_labels"]]}


def explain(r: Rules) -> str:
    """The rules restated in plain Japanese with pages, for the student to check against the handbook."""
    L = [title(r)]
    if r.source:
        L.append("出典: " + "、".join(f"{k}: {v}" for k, v in r.source.items()))
    L.append("")
    for c in r.walk():
        ind = "  " * _depth(c)
        if not c.counts:
            L.append(f"{ind}- {c.name}: 卒業単位に含まれない{_p(c.page)}")
            continue
        parts = [f"{_n(c.min)}単位以上" if c.min else "最低単位なし"]
        if c.max is not None:
            parts.append(f"算入は{_n(c.max)}単位まで")
        if c.overflow_to:
            cap = f"{_n(c.overflow_max)}単位まで" if c.overflow_max is not None else "上限なし"
            parts.append(f"超過分は「{r.by_id[c.overflow_to].name}」へ（{cap}）")
        L.append(f"{ind}- {c.name}: {'、'.join(parts)}{_p(c.page)}")
        if c.match:
            m = c.match
            what = []
            if m.labels:
                what.append("区分 " + "・".join(m.labels))
            if m.label_patterns:
                what.append("区分が " + " / ".join(m.label_patterns) + " に合う")
            if m.names:
                what.append("科目 " + "・".join(m.names))
            if m.name_patterns:
                what.append("科目名が " + " / ".join(m.name_patterns) + " に合う")
            if m.exclude_names or m.exclude_patterns:
                what.append("ただし " + "・".join(m.exclude_names + m.exclude_patterns) + " を除く")
            L.append(f"{ind}    対象: {'、'.join(what)}")
        for x in c.required:
            when = f"（{c.term_only[x]}）" if x in c.term_only else ""
            L.append(f"{ind}    必修: {x[3:] + '（パターン）' if x.startswith('re:') else x}{when}")
        for x in c.conditions:
            L.append(f"{ind}    条件: {x.name} {_n(x.min)}単位以上{_p(x.page)}")
        for x in c.limits:
            ov = f"、超過分は「{r.by_id[x.overflow_to].name}」へ" if x.overflow_to else ""
            L.append(f"{ind}    上限: {x.name}は{_n(x.max)}単位まで{ov}{_p(x.page)}")
        if c.out_of_scope:
            L.append(f"{ind}    （今回は照合しない区分）")
        if c.per_name_max is not None:
            ex = ""
            if c.per_name_exclude:
                ex = "（" + "・".join(c.per_name_exclude.names + c.per_name_exclude.name_patterns + c.per_name_exclude.labels) + " を除く）"
            L.append(f"{ind}    同じ授業科目は{_n(c.per_name_max)}単位まで{ex}")
        if c.same_group:
            L.append(f"{ind}    {_sg_text(c.same_group)}")
        for k, alt in enumerate(c.alternatives):
            head = "次のどれかを満たす:" if k == 0 else ""
            if head:
                L.append(f"{ind}    {head}")
            parts = [f"{x.name} {_n(x.min)}単位以上" for x in alt.conditions]
            if alt.same_group:
                parts.append(_sg_text(alt.same_group))
            L.append(f"{ind}      ({k + 1}) {alt.name}: {'、'.join(parts)}{_p(alt.page)}")
        if c.note:
            L.append(f"{ind}    注: {c.note}")
    for p in r.progression:
        cats = "、".join(f"{r.by_id[k].name} {v}" for k, v in (p.get("categories") or {}).items())
        tot = f"合計 {p['min_total']}" if "min_total" in p else ""
        iy = p.get("in_year")
        yr = f"{iy['year']}年次に{iy['min']}単位" if iy else ""
        req = ("必修 " + "・".join(p.get("required"))) if p.get("required") else ""
        L.append(f"- 進級: {p.get('name', '')} {'、'.join(x for x in (tot, cats, yr, req) if x)}{_p(str(p.get('page', '')))}")
    if r.ask_office:
        L.append("")
        L.append("学務に聞くこと（規則ファイルを作るときに分からなかった点）:")
        L += [f"  - {a}" for a in r.ask_office]
    if r.notes:
        L.append("")
        L.append("注意書き:")
        L += [f"  - {x}" for x in r.notes]
    return "\n".join(L)


def validate(r: Rules) -> list:
    """Warnings that don't stop a check but suggest the rules were transcribed wrongly."""
    warn = []
    for c in r.walk():
        if not c.page:
            warn.append(f"{c.id}: page がない（便覧のどこに書いてあるか分からないと、学生が確かめられない）")
        if c.children and c.counts:
            kids = sum(ch.min for ch in c.children if ch.counts)
            if kids > c.min + EPS and c.min:
                warn.append(f"{c.id}: 子の最低単位の合計 {_n(kids)} が自分の最低単位 {_n(c.min)} より多い")
        if c.max is not None and c.max + EPS < c.min:
            warn.append(f"{c.id}: max {_n(c.max)} が min {_n(c.min)} より小さい")
    tops = sum(c.min for c in r.categories if c.counts)
    if tops > r.total_min + EPS:
        warn.append(f"最上位の区分の最低単位の合計 {_n(tops)} が卒業単位 {_n(r.total_min)} より多い")
    if not r.total_page:
        warn.append("total: page がない")
    return warn
