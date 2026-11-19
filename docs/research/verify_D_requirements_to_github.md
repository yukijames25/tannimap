# 検証D: 「要件を言えば、調査→設計→実装→テスト→GitHub公開までAIが一気通貫でやるツール」は作る価値があるか

調査日: 2026-11-19
表記: **[事実]** は出典で確認した内容、**[推測]** は私の解釈や推論。URL は各項目の末尾に付けた。
GitHub のスター数は 2026-11-19 に GitHub API（`gh api repos/<owner>/<repo>`）で取得した値。
注意: 価格は 2026 年に各社が何度も改定しており、二次情報同士で食い違いが多い。価格の数字は「目安」として読むこと。

---

## 結論（先に）

**一気通貫ツールとしては作らない。** 理由は次の4つ。

1. **中核（要件→リポジトリ/PR）はすでに大手が無料〜月20ドル程度で出している。** GitHub は 2025-09 から「New repository」画面にプロンプト欄を置き、Copilot がリポジトリを作って最初のコードをドラフト PR で出す（§1）。Lovable / Bolt / v0 / Spark もアプリを GitHub に同期する。Claude Code・Codex・Jules・Devin・Cursor・Kiro も、Issue や依頼から PR を出す。
2. **「要件→設計→タスク→実装」の型も飽和している。** Spec Kit（約15万スター）、OpenSpec（約7.5万）、BMAD（約5.6万）、Taskmaster（約2.8万）がある。日本語にも cc-sdd（約3.8千）がある（§2）。
3. **「作る前に価値を確かめる」も、すでに部品がある。** BMAD の Analyst（市場調査・競合・ブリーフ）、Spec Kit の assess 拡張（go/kill の判定）、Claude Code 用の検証スキル（startup-skill 約1.3千、slavingia/skills 約1.1万）がある（§3a）。ただし、どれも需要そのものは確定できない。人と話すことを AI では置き換えられない。
4. **大手の更新が速すぎる。** Claude Code は直近30日で20リリース、Spec Kit は12リリースあった。プロンプトとワークフローを組み合わせただけのツールは、数か月で本体に吸収される可能性が高い（§5）。

**それでも残る狭い空白:** 「公開前の個人情報チェック」だけは、まだ手薄。対象は、git 履歴の全コミットの作者名とメール、Co-Authored-By、Office/PDF のメタデータ（docProps の作成者）、ファイル内に残った `C:\Users\<本名>` のようなパス。秘密鍵の検出は gitleaks や GitHub push protection で埋まっている。ところが「本名や個人メールが履歴とファイルのメタデータに残る」問題をまとめて見るツールは、スター数が数個〜数百の小さなものしか見つからなかった（§3c）。
**ただし、需要のシグナルも弱い。** 事故の報告や統計は見つからず、見つかったのは「設定方法」の記事ばかり（§4）。空白があるのは「海が小さいから」の可能性がある。
→ 作るなら、**単体の製品ではなく、無料の Claude Code スキル/CLI（gitleaks と mat2 系をまとめるもの）と記事のセット**にとどめる。その前に需要を測る（§6）。

---

## 1. 既存ツール: 要件から GitHub リポジトリ/PR まで（2025〜2026年）

### 1-1. 一覧

| ツール | 要件→公開リポジトリまで行くか | 人間に残るもの | 価格（目安） |
|---|---|---|---|
| **GitHub Copilot（cloud agent／旧 coding agent）** | **行く。** 新規リポジトリ作成画面のプロンプト欄から、リポジトリ作成とドラフト PR まで。Issue をアサインすると PR | PR のレビュー・マージ、公開判断 | Pro/Pro+/Business/Enterprise。2026-06-01 から AI Credits 制（1クレジット=0.01ドル） |
| **GitHub Spark** | **行く。** 自然言語でアプリを作り、1クリックでリポジトリを作成。双方向同期 | 公開判断、品質確認 | プレビュー。1プロンプト=4 premium requests（旧課金） |
| **Claude Code ＋ GitHub Actions** | ローカルの Claude Code は git 操作ができる。Action は Issue/PR で @claude と書くと実装・コミット・PR | ワークフローの設定、API キー、マージ | Claude のサブスクまたは API 従量課金＋Actions 分 |
| **OpenAI Codex（cloud）** | 既存リポジトリに対して PR、ブランチ、コミットを作る | レビュー、マージ | ChatGPT プランに込み（Plus 20ドル〜、Pro 100/200ドル）。2026-04 からトークン制 |
| **Google Jules** | 既存リポジトリを VM に clone し、計画を立てて PR を出す | レビュー、マージ | 無料枠あり。Google AI Pro/Ultra に同梱（0〜125ドル/月） |
| **Devin（Cognition）** | 既存リポジトリに PR | レビュー | 2026-04 に Core を廃止。Free/Pro（20ドル）/Max/Teams。Enterprise は ACU 制 |
| **Cursor cloud agents（旧 background agents）** | 既存リポジトリに PR | レビュー | Pro 20ドル〜。クレジット消費が分かりにくいと不満あり |
| **Kiro（AWS）** | IDE は spec 駆動。autonomous agent は Issue に `kiro` ラベルを付けるだけで PR | レビュー。社内実績でもマージ率は37% | Free 0ドル〜Power 200ドル/月（クレジット制） |
| **Replit Agent** | アプリ生成とデプロイ。GitHub 連携あり（エクスポートに Replit 固有ファイルが混ざるという声あり） | 公開判断 | Core 約20ドル/月、Pro 100ドル |
| **Lovable** | 生成と GitHub 双方向同期（全プラン）。公開時に自動セキュリティスキャン | 公開判断 | 約20〜25ドル/月〜 |
| **Bolt.new** | GitHub 双方向同期 | 公開判断 | （価格は未確認） |
| **v0（Vercel）** | GitHub 同期。ブランチと PR 経由でマージし、main へ直接 push しない | ブランチ保護下でのマージ | （価格は未確認） |
| **OpenHands / Cline / Aider** | OSS のエージェント。git 操作はできる | 設定、モデル代 | 本体は無料（OSS）。モデル API 代は別 |
| **MetaGPT（MGX）** | 1行の要件から、ユーザーストーリー、**競合分析**、要件、API、文書を出す。リポジトリはローカルに作る | GitHub 公開は自分で | OSS。商用版は MGX |
| **gpt-engineer** | 「Lovable の前身」。最終 push は 2025-05 | — | OSS |

### 1-2. 根拠
- **[事実]** GitHub changelog（2025-09-30）「Start your new repository with Copilot coding agent」: 新規リポジトリ作成時のプロンプト欄から coding agent が作業を始め、"Copilot will open a draft pull request, write the requested code, and then request a review from you." 対象は Copilot Pro / Pro+ / Business / Enterprise。 — https://github.blog/changelog/2025-09-30-start-your-new-repository-with-copilot-coding-agent/
- **[事実]** coding agent は1セッション=1 premium request（旧課金）。Actions 分も消費する。 — https://github.blog/changelog/2025-07-10-github-copilot-coding-agent-now-uses-one-premium-request-per-session/ , https://docs.github.com/en/billing/concepts/product-billing/github-copilot-premium-requests
- **[事実]** 2026-06-01 から premium requests が GitHub AI Credits の使用量課金に変わった。 — https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/ , https://roboin.io/article/en/2026/04/28/github-copilot-moves-to-credit-based-billing/
- **[事実（二次情報）]** coding agent は 2026-04 に「Copilot cloud agent」へ改名されたとされる（GitHub 公式では未確認）。 — https://dev.to/mr_manushukla/copilot-cloud-agent-in-2026-reasoning-levels-comment-triggers-and-the-ai-credit-math-behind-them-3jil
- **[事実]** Spark: 1クリックでリポジトリ作成、双方向同期、1プロンプト=4 premium requests、パブリックプレビュー。 — https://docs.github.com/en/billing/concepts/product-billing/github-spark
- **[事実]** Claude Code GitHub Actions: Issue/PR コメントで @claude と書くと、解析・実装・コミット push まで行う。`/install-github-app` で設定する。 — https://code.claude.com/docs/en/github-actions , https://github.com/anthropics/claude-code-action （約1.0万スター）
- **[事実]** Codex の cloud agent はコンテナでタスクを実行し、PR・コミット・ブランチを作る。ChatGPT 各プランに含まれ、2026-04-02 からトークン制。 — https://www.eesel.ai/blog/codex-pricing , https://automationatlas.io/answers/chatgpt-codex-pricing-explained-2026/
- **[事実]** Jules は VM に clone して PR を出す。単独の課金はなく Google AI のプランに同梱。 — https://www.morphllm.com/comparisons/jules-google-coding-agent , https://dev.to/dmaxdev/google-jules-review-the-async-coding-agent-worth-20month-4no
- **[事実（二次情報）]** Devin は 2026-04 に Core/Team を廃止し、Free/Pro/Max/Teams に移行した。 — https://fast.io/resources/devin-ai-core-plan/ , https://www.usecarly.com/blog/devin-pricing
- **[事実（二次情報）]** Cursor の Pro 20ドル / Pro+ 60ドル / Ultra 200ドル。cloud agent は Pro 以上。料金の仕組みはフォーラムでも質問が続いている。 — https://dev.to/rahulxsingh/cursor-pricing-in-2026-hobby-pro-pro-ultra-teams-and-enterprise-plans-explained-4b89 , https://forum.cursor.com/t/what-is-the-pricing-structure-for-using-cloud-agents/156843
- **[事実]** Kiro の料金: Free 0ドル（50クレジット）、Pro 20ドル、Pro+ 40ドル、Pro Max 100ドル、Power 200ドル、Teams 20ドル/席。 — https://kiro.dev/pricing/
- **[事実]** Kiro autonomous agent: Issue に `kiro` ラベルか `/kiro` コメントでタスクになり、PR を作る。AWS 自身のブログでは、94 PR のうちマージは35（37%）、56（60%）がレビュー待ち。 — https://kiro.dev/docs/autonomous-agent/github/ , https://kiro.dev/blog/tackling-technical-debt-at-scale-with-autonomous-mode/
- **[事実]** Lovable は全プランで GitHub と双方向同期できる（1ブランチのみ）。 — https://docs.lovable.dev/features/labs （検索結果の要約）, https://coddy.tech/build/vs/lovable
- **[事実]** Bolt は GitHub 双方向同期。 — https://bolt.new/blog/github-hackathon , https://support.bolt.new/integrations/git
- **[事実]** v0 はブランチと PR 経由でマージし、main に直接 push しない。 — https://api2.v0.dev/docs/github , https://v0.app/faq
- **[事実（二次情報）]** Replit Core 約20ドル/月。エクスポートに Replit 固有ファイルが混ざるという不満がある。 — https://nhimg.org/replit-agent-guide , https://costbench.com/software/developer-tools/replit/hidden-costs/
- **[事実]** MetaGPT: "takes a one line requirement as input and outputs user stories / competitive analysis / ..."。商用版は MGX（2025-02-19 公開）。約7.1万スター、最終 push は 2026-01。 — https://github.com/FoundationAgents/MetaGPT
- **[事実]** スター数: OpenHands 約9.4万、Cline 約7.2万、Aider 約5.0万（最終 push 2026-05）、gpt-engineer 約5.5万（最終 push 2025-05、説明文は "Precursor to lovable.dev"）、ChatDev 約3.5万。 — https://github.com/OpenHands/OpenHands , https://github.com/cline/cline , https://github.com/Aider-AI/aider , https://github.com/AntonOsika/gpt-engineer , https://github.com/OpenBMB/ChatDev
- **[推測]** 「要件→新規リポジトリ→PR」は GitHub 自身が標準機能にしている。この部分で個人が差をつける余地はない。人間に残っているのは次の3つ。(1) 何を作るかの判断、(2) PR のレビューとマージ、(3) 公開してよいかの判断（秘密・個人情報・ライセンス）。

---

## 2. 仕様駆動（SDD）・プロセス型フレームワーク

| 名前 | スター数 | カバー範囲 | カバーしないもの |
|---|---|---|---|
| **GitHub Spec Kit** | 150,631 | constitution → specify → plan → tasks → implement（＋ converge）。拡張で bug と **assess**（intake/research/define/shape/decide）。日本語 README あり | ユーザーテスト、公開前チェック、プライバシー |
| **OpenSpec** | 75,257 | AI コーディング支援向けの SDD | （README 未精読） |
| **BMAD-METHOD** | 55,541 | Analyst（ブレスト、**市場調査**、競合、ブリーフ）→ PM（PRD）→ UX → アーキテクチャ → 開発 → Test Architect。Founder モジュール（価格、資金調達） | 実ユーザーでのテスト、GitHub 公開、プライバシー |
| **Taskmaster（claude-task-master）** | 28,374 | PRD をタスクに分解（最終 push 2026-04 で鈍化） | 検証、公開 |
| **Kiro（IDE）** | 4,484（Issue 用リポジトリ） | requirements → design → tasks、hooks | 同上 |
| **cc-sdd（日本製）** | 3,774 | Kiro 互換の SDD を Claude Code / Codex / Cursor / Copilot などで使える。日本語対応 | 同上 |
| **CoDD（日本製）** | 113 | 要件聞き取り → 設計 → 実装/テスト → 整合性検査 → deploy | 需要検証、ユーザーテスト、プライバシー |

- **[事実]** スター数は上表（GitHub API、2026-11-19）。 — https://github.com/github/spec-kit , https://github.com/Fission-AI/OpenSpec , https://github.com/bmad-code-org/BMAD-METHOD , https://github.com/eyaltoledano/claude-task-master , https://github.com/kirodotdev/Kiro , https://github.com/gotalab/cc-sdd , https://github.com/yohey-w/codd-dev
- **[事実]** Spec Kit の README には SDD のコマンド群と、assess 拡張（idea を「追う価値があるか」の証拠を集める）が載っている。拡張とプリセットの仕組みがある。 — https://github.com/github/spec-kit
- **[事実（二次情報）]** assess の decide 段階は go / needs-clarification / kill で判定し、結果を `.specify/assessments/<slug>/decision.md` に残す。 — https://skillsmp.com/creators/mnriem/spec-kit-copilot-plugin-demo/github-skills-speckit-assess-decide
- **[事実]** BMAD の Analyst（Mary）は、市場調査（競争環境、顧客ニーズ、トレンド）、ドメイン調査、技術調査、プロダクトブリーフを担当する。 — https://www.mintlify.com/bmad-code-org/BMAD-METHOD/reference/agents/analyst , https://claudemarketplaces.com/skills/bmad-code-org/bmad-method/bmad-market-research
- **[事実]** cc-sdd は「日本語対応・Kiro 互換の国産 SDD ツール」として紹介されている。2026-10 の比較記事では「日本語で新規開発するなら cc-sdd」。 — https://gigazine.net/news/20251108-cc-sdd/ , https://www.issoh.co.jp/tech/details/8732/
- **[事実]** CoDD は elicit → generate → implement → dag verify → deploy まで回す。記事は需要検証、ユーザーテスト、プライバシーを扱っていない。 — https://zenn.dev/shio_shoppaize/articles/codd-v2-17-milestone
- **[事実]** Böckeler（martinfowler.com、2025-10）は、SDD の意味はまだ定まっていないと指摘している。調べたツールはどれも spec-first で、spec-as-source を明確に目指すのは Tessl だけ。 — https://www.martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
- **[推測]** SDD 系は「作り方」の型としては飽和している。カバーしていないのは主に3つ。(1) 実ユーザー（または代理ユーザー）での検証と計測、(2) 公開前のプライバシーチェック、(3) 公開後のローンチ（記事・告知）。市場調査は BMAD と Spec Kit assess が「AI による机上調査」としては既に持っている。

---

## 3. 空白はどこか

### 3a. 作る前に「作る価値があるか」を確かめる → **机上調査は埋まっている。本物の需要確認は道具では埋まらない**
- **[事実]** Claude Code などで使える検証スキルが多数ある。startup-skill（約1.3千スター、8段階の検証レポートと go/no-go）、slavingia/skills（約1.1万スター、validate-idea を含む）、ideaprobe（0スター）、alinaqi/ideavalidator（15スター）。 — https://github.com/ferdinandobons/startup-skill , https://github.com/slavingia/skills , https://claudemarketplaces.com/skills/slavingia/skills/validate-idea , https://claudemarketplaces.com/plugins/alinaqi-ideavalidator
- **[事実]** vibe-check skill（"Stop your AI from building the wrong app"）は、Reddit やレビューサイトの不満と照合し、no-go 判定も出す。作者によれば 460+ スター。 — https://www.producthunt.com/p/vibe-check-6/vibe-check-skill
- **[事実]** Zenn（2026-08-06）は、「AI が大きく減らしたのは実装の不確実性。課題と需要の有無は、AI に質問しても確定できない」と書いている。インタビュー、LP、手動代行、予約販売を勧める。 — https://zenn.dev/agepan/articles/ai-indie-demand-validation
- **[推測]** 「Web で不満を集めて go/no-go を出す」機能はすでにコモディティ。足りないのは道具ではなく、人と話すという行動のほう。ツールにしても差がつかない。

### 3b. 代理ユーザーでのテストと計測 → **研究と SaaS はある。コーディングエージェントのワークフローへの組み込みは薄い。効果は疑わしい**
- **[事実]** 合成ユーザーの SaaS（Synthetic Users ほか）や研究（UXAgent: CHI 2025、UXCascade: Adobe/ETH 2026）がある。 — https://aimultiple.com/synthetic-users , https://www.arxiv.org/pdf/2601.15777
- **[事実]** Userbrain の実験（2026-04）では、AI エージェントは整った道筋をたどり、実ユーザーは迷ったり諦めたりした。 — https://www.userbrain.com/blog/synthetic-users-experiment/
- **[事実]** AI ペルソナには「実ユーザーなら却下するアイデアを肯定しがち」という傾向が記録されている、という警告がある。 — https://www.theysaid.io/blog/synthetic-user-testing-guide , https://bottlerocketstudios.com/insights/insights-posts/the-synthetic-user-problem-why-ai-personas-cant-replace-real-research-participants
- **[推測]** 「代理ユーザーテストを指標付きで回す」を開発フローに組み込むこと自体は珍しい。ただし代理テストで分かるのは「使い方の詰まり（UX のバグ）」までで、「欲しいかどうか」は分からない。売りにすると誤解を招く。

### 3c. 公開前チェック → **秘密鍵は埋まっている。個人情報（履歴とメタデータ）は手薄**
秘密鍵（埋まっている）:
- **[事実]** gitleaks 約3.1万スター、trufflehog 約3.0万スター。 — https://github.com/gitleaks/gitleaks , https://github.com/trufflesecurity/trufflehog
- **[事実]** GitHub は 2024-03 から、公開リポジトリへの push で secret scanning push protection を既定で有効にしている（ユーザー単位。バイパスは可能）。 — https://github.blog/changelog/2024-03-11-secret-scanning-and-push-protection-are-enabled-by-default-on-new-public-repositories/ , https://docs.github.com/en/code-security/concepts/secret-security/push-protection
- **[事実]** Claude Code には `/security-review` コマンドと GitHub Action がある。 — https://support.claude.com/en/articles/11932705-automated-security-reviews-in-claude-code , https://github.com/anthropics/claude-code-security-review
- **[事実]** Lovable は公開時に自動でセキュリティスキャンをする。Replit は公開前スキャンと、重大な脆弱性があれば公開をブロックする設定を持つ。 — https://www.createwith.com/tool/lovable/updates/lovable-launches-automatic-security-scanning-before-every-publish , https://docs.replit.com/replit-workspace/workspace-features/security-scanner

個人情報（手薄）:
- **[事実]** GitHub の「個人メールを含む push をブロック」設定は、**最新のコミット1件の author email** が、アカウントに登録された非公開メールかどうかしか見ない（"we'll check the most recent commit"）。 — https://docs.github.com/en/account-and-profile/how-tos/email-preferences/blocking-command-line-pushes-that-expose-your-personal-email-address
- **[推測]** つまり次のものは素通りする。(1) 過去のコミット、(2) committer 欄、(3) 本名の author 名、(4) GitHub に登録していない別のメール、(5) Co-Authored-By トレーラー、(6) ファイル内のメタデータ。
- **[事実]** git config で名前やメールを変えても、過去のコミットは変わらない（GitHub 日本語ドキュメント）。 — https://docs.github.com/ja/enterprise-server@3.0/get-started/getting-started-with-git/setting-your-username-in-git
- **[事実]** gitleaks は秘密鍵を探すツールで、作者メールを「問題」としては検出しない（出力に表示されるだけ）。 — https://trevorlasn.com/blog/your-repo-is-a-leaky-ship-probably （検索結果の要約）
- **[事実]** 個人情報向けのツールは小さいものしかない。leak-sweep（3スター、"Scan your GitHub repos for leaked personal information"）、dmeta（43スター、Office のメタデータ除去）、mat2（394スター、docx/xlsx/pptx/PDF/画像に対応。ただし作者自身が「複雑な形式の全メタデータを確実に検出する方法はない」と書いている）。 — https://github.com/26zl/leak-sweep , https://github.com/openscilab/dmeta , https://github.com/jvoisin/mat2
- **[事実]** xlsx/docx の作成者は docProps/core.xml、会社名は app.xml に入る。コメントや変更履歴の作者は本文の XML に入る。 — https://pypi.org/project/DMeta/ , https://abacktools.com/tools/file/forensics/document-metadata-remover
- **[事実]** Excel は保存時に作成者や会社名を自動で書き込む。Office には「ドキュメント検査」がある（手動）。 — https://www.fmworld.net/cs/azbyclub/qanavi/jsp/qacontents.jsp?PID=3109-6354
- **[事実]** Claude Code は既定でコミットに Co-Authored-By を付ける。`attribution` 設定で消せるが、設定が効かないという報告もある。 — https://github.com/anthropics/claude-code/issues/22585 , https://dev.classmethod.jp/articles/claude-code-attribution-setting/
- **[推測]** 「全コミットの名前とメール ＋ トレーラー ＋ Office/PDF/画像のメタデータ ＋ 本文中のローカルパスや本名」を、公開の直前にまとめて見るツールは見当たらない。ここが一番はっきりした空白。

### 3d. 日本語ワークフロー → **SDD 層は埋まっている。日本語特有の公開前チェックは見当たらない**
- **[事実]** 日本語の SDD には cc-sdd と CoDD があり、Spec Kit にも日本語 README がある（§2）。
- **[事実]** 日本語の記事は「noreply アドレスに設定しよう」という設定方法が中心。ある記事は、メールアドレスだけで悪用できることは限られるとして、緊急度を「中程度」と見ている。 — https://zenn.dev/airrnot1106/articles/aed5f156e508db , https://zenn.dev/n4mlz/articles/e8e140a00e729f , https://blog.serverworks.co.jp/git-mail
- **[推測]** 日本語特有の論点はある。漢字の本名がコミットの author や Excel 方眼紙の作成者欄に残ること、`C:\Users\<ローマ字の本名>` がログやスクリーンショットに写ることなど。ただし、これを困りごととして訴える声は今回見つからなかった。

---

## 4. 需要のシグナル（不満の声）

| 不満 | 強さ | 根拠 |
|---|---|---|
| 「AI で作ったが誰も要らなかった」 | **強い** | Indie Hackers、Reddit r/AI_Agents、Zenn に多数 |
| 「AI 経由で秘密鍵が漏れた」 | **強い（定量データあり）** | GitGuardian、Apiiro |
| 「エージェントが雑な PR やリポジトリを作る」 | **強い** | OSS の AI PR 禁止の動き、METR、Linux Foundation 調査 |
| 「コミットや Office のメタデータで本名やメールが漏れた」 | **弱い** | 設定方法の記事のみ。事故の報告や統計は見つからなかった |

- **[事実]** Indie Hackers「tired of building apps that get 0 users」。Product Hunt のコメントでは「最近の Reddit の投稿は、作ったのにユーザーがいない、という不満ばかり」とされている。 — https://www.indiehackers.com/post/tired-of-building-apps-that-get-0-users-i-was-too-heres-what-i-m-testing-to-fix-it-bbc654110c , https://bittide.aicompass.dev/article/b443346d-3362-4d1d-b4ea-c62df419bb07
- **[事実]** Zenn では「AI 駆動で Web アプリを3つほどリリースしたが反応はない」「服装提案アプリの開発を止めた」といった体験談がある。 — https://zenn.dev/agepan/articles/ai-indie-demand-validation と同じ検索で見つかった記事群（https://zenn.dev/nir_nmttg/articles/9f686b0e418a87 ほか）
- **[事実]** GitGuardian（State of Secrets Sprawl 2026）: 2025年に公開 GitHub へ新たに漏れた秘密は 2,865万件（前年比+34%）。AI サービスの秘密は 127.5万件（+81%）。Claude Code が関わったコミットの漏洩率は 3.2%、全体の基準は 1.5%。ただし著者は「単純なツールの欠陥ではない」と注記している。 — https://blog.gitguardian.com/the-state-of-secrets-sprawl-2026/
- **[事実（二次情報）]** Apiiro（2026-11）は、AI エージェントが書いたファイルの中から、公開リポジトリ 1,994 件で実在の秘密 2,539 件を見つけた。`.claude/settings.local.json` の公開コピー 104,185 件のうち 1,122 件に秘密が入っていた。 — https://fourweekmba.com/ai-most-of-2-539-leaked-secrets-sat-in-a-claude-code-file/
- **[事実]** METR（2026-03）: SWE-bench Verified でテストに通った AI の PR のうち、約半分はメンテナがマージしない。 — https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/
- **[事実（二次情報）]** Ghostty と tldraw は AI の PR を制限、または外部 PR を閉鎖した。Linux Foundation の調査では、受け取る PR の約25%が低品質な AI 生成と推定されている。RedMonk は77組織のポリシーを分類した。 — https://redmonk.com/kholterhoff/?p=434 , https://aicybr.com/blog/linux-foundation-ai-generated-pr-survey-maintainer-policy-guide , https://www.popularai.org/p/ai-generated-pull-requests-open-source-maintainers
- **[事実]** 公開コミットのメールが収集されうることは、研究で示されている（arXiv 1908.05354、NDSS 2025）。 — https://ar5iv.labs.arxiv.org/html/1908.05354 , https://www.ndss-symposium.org/wp-content/uploads/2025-613-paper.pdf
- **[推測]** 声が大きい不満ほど、大手がすでに手を打っているか、道具では解けない。秘密鍵は大手が手当て済み。「誰も要らない」は道具で解けない。「雑な PR」は大手各社のレビュー機能が狙っている。一方、手薄なプライバシーは、声も小さい。

---

## 5. リスク

- **[事実]** リリースの速さ（2026-10-20〜11-19 の30日間、GitHub API）: Claude Code 20回、Spec Kit 12回、Codex 8回（stable のみ）。 — https://github.com/anthropics/claude-code/releases , https://github.com/github/spec-kit/releases , https://github.com/openai/codex/releases
- **[事実]** 大手はすでに「公開ゲート」を自前で持っている。GitHub の push protection、Lovable と Replit の公開時スキャン、Claude Code の `/security-review`（§3c）。
- **[推測]** 一気通貫ツールの中身は「プロンプト ＋ スキル ＋ gh コマンドの順番」になる。これは Claude Code の skills/plugins、Spec Kit の拡張/プリセット、BMAD のモジュールで、誰でも同じものを組める。差別化が残らず、本体のアップデート1回で吸収される。
- **[推測]** プライバシーチェックも安泰ではない。GitHub が「最新1コミットだけ」を「全コミット」に広げる、あるいは Anthropic が `/security-review` に PII チェックを足せば、その日に不要になる。ただ、Office のメタデータまで見るのは大手の優先度が低く、比較的長く残りそうだ。
- **[推測]** 個人開発者に残る差別化は、①日本語と日本の業務ファイル（Excel 方眼紙、Shift_JIS、本名の漢字）への特化、②「実際にこの手順で作って公開した」実績と記事、くらい。①は市場が小さく、②はツールではなくコンテンツの価値になる。

---

## 6. 判定と、最も狭い「まだ空いている」版

### 判定: **一気通貫ツールは作らない。狭い版だけ「需要を測ってから」作る**

| 案 | 判定 | 理由 |
|---|---|---|
| 要件→GitHub 公開の一気通貫 | **作らない** | Copilot の新規リポジトリ用プロンプト、Spark、Lovable などと正面から重なる |
| SDD の型（要件→設計→タスク） | **作らない** | Spec Kit 15万、BMAD 5.6万、日本語なら cc-sdd |
| 作る前の価値検証スキル | **作らない** | BMAD、Spec Kit assess、startup-skill、vibe-check が既にある。本物の需要確認は道具では解けない |
| 代理ユーザーテスト＋計測 | **記事のネタとしてのみ** | 珍しいが効果に疑問がある。UX の詰まりは見つかるが、需要は分からない |
| **公開前の個人情報ゲート** | **条件付きで作る（小さく、無料で）** | 唯一はっきりした空白。ただし需要シグナルは弱い |

### 最も狭い版（もし作るなら）
`git push` や `gh repo create --public` の直前に走る、Claude Code スキル兼 CLI。対象は次のとおり。
1. **全コミット**の author/committer の名前・メールと Co-Authored-By を一覧にする。noreply 以外と、本名らしきものに印を付ける。
2. 追跡されている docx/xlsx/pptx/PDF/画像のメタデータを読む（作成者、最終更新者、会社名、コメント作者、GPS など）。除去は mat2 か dmeta に任せる。
3. 本文中の `C:\Users\<name>`、`/home/<name>`、メールアドレス、電話番号を検出する（Presidio などの PII 検出系。約1.2万スター: https://github.com/data-privacy-stack/presidio ）。
4. 秘密鍵は自前で作らず、gitleaks を呼ぶ。
5. 履歴の書き換え（git filter-repo）は**提案にとどめ、自動では実行しない**。

### 作る前に確かめること（customer-first）
- **[推測]** 需要の測り方の案。公開されている日本語の個人リポジトリから無作為に N 件選び、「xlsx/docx の作成者欄に人名が入っている割合」と「noreply 以外のメールでコミットしている割合」を**集計値だけ**数える（個人名は保存も公開もしない）。割合が高ければ、記事として「あなたのリポジトリにも本名が残っている」と示す根拠になる。低ければ作らない。
- **[推測]** 先に記事を出し（チェック手順と、10行程度のスクリプト）、反応（いいね、スター、問い合わせ）を見てからツール化する順番が、§4 で見た「誰も要らなかった」を避ける一番安い方法。

---

## 付録: 未確認・弱い点
- Bolt.new と v0 の 2026 年の価格は確認していない。
- OpenSpec は README を精読していない（スター数のみ）。
- X（旧 Twitter）は検索できる道具がなく、調べていない。Reddit も二次的な引用だけ。
- Copilot の「cloud agent」への改名は二次情報のみで、GitHub 公式の changelog では確認できなかった。
- Apiiro の数字は二次サイト（FourWeekMBA）経由で、原文は未確認。
