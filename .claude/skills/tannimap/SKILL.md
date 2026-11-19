---
name: tannimap
description: Check a Japanese university student's grades and course plan against their OWN handbook (便覧・履修要項・履修の手引き・卒業要件チェックシート). Use when a student asks "この単位で卒業できる？", "履修登録の前に何が足りないか", "留年しないか", "GPA", "給付奨学金の単位の基準", or shares a handbook PDF and a transcript (成績表). Turns the handbook's graduation requirements into a rules file with page references, then runs the checker.
---

# tannimap — 自分の便覧で、自分の単位を照らし合わせる

学生が困っているのは「規則が無い」ことではなく、**自分の便覧の規則を自分の成績に当てはめられない**こと。
規則は便覧に書いてあり、成績はポータルにある。あなた（AI）の仕事は、その間をつなぐ規則ファイルを**便覧のページを根拠に**作り、学生に確かめてもらってから照合すること。

実行: このリポジトリなら `PYTHONPATH=src python -m tannimap ...`（PowerShell: `$env:PYTHONPATH="src"`）。インストール済みなら `tannimap ...`。

## 守ること（いちばん大事）

- **「卒業できます」とは言わない。** 出すのは「便覧の規則（p.○）に照らした目安」と「学務に聞くこと」。判定するのは大学（教授会）。
- **規則を推測で埋めない。** 便覧に書いていないこと（上限・振替・算入しない科目）は書かない。分からない点は `ask_office` に入れる。
- **すべての区分に `page` を付ける。** 学生が便覧のどこで確かめればいいか分からない規則は、信用できない。
- 成績は個人情報。外部に送らない。必要な範囲だけ読む。

## 手順

1. **何を照らし合わせるか確かめる**
   大学・学部・学科・コース・**入学年度**（規則は入学年度で変わる）。
   便覧の「卒業要件」「卒業所要単位」の表のページと、その注意書き（※印）のページ。チェックシートがあればそれも。
   成績表（ポータルの CSV、または成績の表をコピーしたもの）。履修登録前なら、取る予定の科目も。

2. **先に成績表を見る**: `区分`（科目区分）の列にどんな文字列が出てくるかを書き出す。
   規則の `match.labels` は**成績表に実際に出てくる区分名**に合わせる（便覧の表記と違うことが多い）。
   区分が無い成績表なら、科目名（`names` / `name_patterns`）で分ける。

3. **便覧の要件表を規則ファイルにする**（形式は下の「規則ファイル」）。
   - 表を上から読み、区分の入れ子を `children` にする。最低単位 → `min`。
   - 注意書きを1つずつ規則にする。次の言い回しに注意:

   | 便覧の言い回し | 規則 |
   |---|---|
   | 「○単位以上」「必要単位数」 | `min` |
   | 「修得上限○単位」「○単位まで卒業所要単位に含める」 | `max`（超えた分は数えない） |
   | 「必修単位数を超えて修得した単位は、○○科目に含めることができる」 | `max` ＋ `overflow: {"to": "○○のid"}`（上限があれば `overflow.max`） |
   | 「卒業所要単位に含めない」（教職・資格科目など） | `"counts": false` の区分 |
   | 「A を○単位、B を○単位含めて計○単位」 | `min` ＋ `conditions` |
   | 「他学科・他コースの科目は○単位まで」 | `limits` |
   | 「いずれか1つの言語で○単位」 | `same_group`（科目名から言語名を取り出す正規表現） |
   | 「A で履修する場合は…、B で履修する場合は…」 | `alternatives` |
   | 「○○は必ず修得」「必修科目」（個別の科目名がある） | `required` |
   | 「春学期のみ登録できる」 | `term_only` |
   | 「3年次までに○単位」「進級要件」 | `progression` |
   | 入学年度で扱いが違う | その学生の入学年度の扱いだけを書き、`notes` に差を書く |

   - 2つの区分に同時に入りうる科目は、より具体的な区分を先（兄弟の中で前）に書く。科目は最初に当てはまった区分に入る。

4. **検査する**: `tannimap validate rules.json` — エラーを直す。warning も読んで、便覧と食い違っていないか確かめる。

5. **学生に確かめてもらう（省略しない）**: `tannimap explain rules.json` の出力を見せ、
   「便覧の p.○ と見比べて、違うところがあれば教えてください」と頼む。直したら 4 からやり直す。

6. **照らし合わせる**:
   ```
   tannimap check rules.json grades.csv [--plan plan.csv] [--years 在学年数]
   ```
   - `■ 規則にない区分の科目` が出たら、規則の `match` を推測で足さない。便覧で区分を確かめるか、学生に聞く。
   - 履修登録前の相談なら `--plan`（評価欄が空の表）で「予定どおり取れば足りるか」を見る。

7. **伝える**: 予定込みでも残る問題 → 修得すれば解消するもの → 数に入らない単位（理由とページ）→ 学務に聞くこと、の順に。
   不足の数字の理由（上限で数えられない単位、算入しない科目）を、便覧のページとともに説明する。
   最後に、判定は大学が行うことを一言添える。

## 規則ファイル（JSON）

```json
{
  "schema": "tannimap/1",
  "university": "○○大学", "faculty": "○○学部", "entry_years": "2024年度",
  "source": {"title": "2024年度 履修の手引き", "url": "", "checked": "2026-04-01"},
  "total": {"min": 124, "page": "12"},
  "standard_years": 4,
  "grading": {"pass": ["S","A","B","C","認定"], "fail": ["D","F"],
              "gpa": {"S":4,"A":3,"B":2,"C":1,"D":0,"F":0}, "gpa_exclude": ["認定"]},
  "categories": [
    {"id": "kyoyo", "name": "教養科目", "min": 30, "page": "12", "children": [
      {"id": "eigo", "name": "英語", "min": 4, "max": 6, "overflow": {"to": "jiyu", "max": 2},
       "page": "13", "match": {"labels": ["英語"]}}
    ]},
    {"id": "senmon", "name": "専門科目", "min": 60, "page": "14",
     "match": {"label_patterns": ["^専門"]},
     "required": ["卒業研究"], "term_only": {"卒業研究": "春学期のみ登録可"},
     "conditions": [{"name": "専門必修", "min": 20, "match": {"labels": ["専門必修"]}}],
     "limits": [{"name": "他学科の科目", "max": 10, "match": {"labels": ["他学科"]}}]},
    {"id": "jiyu", "name": "自由科目", "max": 20, "page": "15", "match": {"labels": ["自由"]}},
    {"id": "kyoshoku", "name": "教職科目", "counts": false, "page": "16", "match": {"labels": ["教職"]}}
  ],
  "progression": [{"name": "3年→4年", "min_total": 90, "categories": {"senmon": 30}, "page": "17"}],
  "ask_office": ["便覧に書いていないが確かめたいこと"],
  "notes": ["入学年度による違いなど"]
}
```

- `match`: `labels`（区分名と完全一致）、`label_patterns`（区分の正規表現）、`names`（科目名と完全一致）、`name_patterns`（科目名の正規表現）、`exclude_names` / `exclude_patterns`。全角・半角と空白の違いは無視して比べる。
- 子を持たない区分には `match` が必要。親の単位は子の合計（＋親自身の `match`）。
- `same_group`: `{"name": "ひとつの言語で6単位", "key_pattern": "^教養外国語(.+?)[AB]", "min": 6, "conditions": [{"name": "中級", "min": 2, "match": {"name_patterns": ["B$"]}}]}`
- `alternatives`: `[{"name": "英語で履修", "conditions": [...]}, {"name": "第二外国語で履修", "same_group": {...}}]` — どれか1つを満たせばよい。
- `required` は科目名。表記ゆれがあるなら `"re:^卒業研究"` のように正規表現で。
- `grading` は成績表の評語に合わせる。知らない評語があると読み込みが止まる（推測で合否を決めないため）。

`tannimap template rules` で記入用のひな形、`tannimap template grades` で成績表のひな形が出る。
