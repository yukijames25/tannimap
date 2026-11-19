# 日本の大学生向け 既存ツール・サービスの地図と、個人開発者が狙える未解決領域

調査日: 2026-11-19。対象は日本の大学生向けのみ。GitHub の数値（スター数、最終 push 日）は 2026-11-19 に `gh search repos` / `gh api` で取得した。
注意: App Store / Google Play の低評価レビュー本文は、ストアページの取得制約でほとんど取れなかった。「レビューでの不満」は根拠が薄い（各 Gaps に明記）。

## 時間割・課題管理アプリ と LMS（manaba / Moodle / WebClass）向け非公式ツールの現状と不満

### Takeaway
時間割アプリはレッドオーシャン。Penmark（評価4.6・約1.3万件、2026年11月も更新中）を筆頭に、汎用の時間割アプリが多数ある。一方、LMS（manaba 等）の課題を集約するツールは「大学ごと・個人ごと」の小さな拡張機能やボットがばらばらにあるだけで、維持されているものは少ない。代表格の Twin:te 系や manaba-enhanced は archived か、2023〜2024年から更新が止まっている。

### Cited Findings
**時間割アプリ（商用）**
- Penmark: App Store 評価 4.6／約1.3万件。最新版 4.41.14 は取得時点で「13時間前」更新（前版 4.41.13 は 10/30）。機能は、公式シラバス連携の時間割作成、授業レビュー、授業ごとのトークルームとファイル共有、課題・出欠・メモ管理、バイト・就活も入るカレンダー、掲示板、学割クーポン、ウィジェット。無料で、課金項目の表示はなかった — [App Store Penmark](https://apps.apple.com/JP/app/id1440444406)
- Penmark への指摘レビュー（2020/04/15）: 解約・退会がすぐできない点と、大学メール入力を求められる点への不安。開発元は「メールで退会可能。アプリ内退会は予定。必要なのはメールアドレスだけで、学生ポータルのパスワードは不要」と返信している — [App Store Penmark](https://apps.apple.com/JP/app/id1440444406)
- app-liv の比較表では、Penmark のリマインダー・オフライン機能などの欄が「-」になっている（非対応か未記載かは不明） — [app-liv](https://app-liv.jp/5134435/?from_genre=1673)
- 他にも汎用の時間割アプリが多数ある（orinas、じかんわり表、Simple Timetable 2、学生用 時間割 シンプル ToDo管理 など） — [orinas](https://apps.apple.com/us/app/id1497999588)、[じかんわり表](https://apps.apple.com/us/app/%E3%81%98%E3%81%8B%E3%82%93%E3%82%8F%E3%82%8A%E8%A1%A8-%E5%A4%A7%E5%AD%A6%E7%94%9F%E3%81%AE%E6%99%82%E9%96%93%E5%89%B2%E3%82%A2%E3%83%97%E3%83%AA-%E6%8E%88%E6%A5%AD%E7%AE%A1%E7%90%86/id1582687349?l=ko)、[Simple Timetable 2](https://apps.apple.com/us/app/id931454913)
- Orario: 2019年時点で「Orario for 京大」が KULASIS の ID とパスワードを入力させて時間割を取得していた。京大情報環境機構は 2017年頃から認知し、2017年5月に注意喚起。これをきっかけに、2018年11月に公式の「KULASIS アプリ」を作った — [京都大学 学生質問回答 2019](https://www.kyoto-u.ac.jp/sites/default/files/embed/jaeducation-campusclimaildocuments2019a0330.pdf)
- Orario の 2025〜2026年時点の提供状況は、検索では確認できなかった（「終了」の告知も「継続」の証拠も見つからない）。
- 京大の公式 KULASIS アプリは時間割表示とシラバス確認ができる。学生からは「PC版の時間割は曜日と時限の並びが一般的な形と逆」という不満が出ており、大学は改修候補として検討すると回答 — [KULASIS 案内](https://www.z.k.kyoto-u.ac.jp/freshman-guide/kulasis)、[京大 学生質問回答](https://www.kyoto-u.ac.jp/sites/default/files/inline-files/202104216-b3729423c68b9b299df37d7c246115b6.pdf)
- 横浜国大は「大学名を一部冠したアプリは本学と関係ない。ログインIDやパスワードを入力しないように」と注意喚起している — [横浜国立大学 ハンドブック](https://www.ynu.ac.jp/campus/guide/handbook/pdf/ori_09.pdf)

**manaba 向け非公式ツール（Chrome 拡張・OSS）**
- manaba-enhanced（筑波大向け、41★）: archived、最終 push 2025-01-16 — [GitHub](https://github.com/manaba-enhanced-for-tsukuba/manaba-enhanced)
- Manaba Report Integration（Twin:te、15★）: 課題の提出状況を Google Tasks / Trello / GitHub Projects へ同期する。最終 push 2023-10-12（約3年更新なし） — [GitHub](https://github.com/twin-te/manaba-report-integration)、[Chrome Web Store](https://chrome.google.com/webstore/detail/manaba-report-integration/detail/manaba-report-integration/gbcijpgbppbphpikpdohpgmpcgdemnai)
- modern-manaba（14★、manaba の UI を変える）: 最終 push 2024-07-16 — [GitHub](https://github.com/itsu-dev/modern-manaba)
- manaba_R_incremented（立命館 manaba+R 向け、27★）: 最終 push 2022-09-05 — [GitHub](https://github.com/ygkn/manaba_R_incremented)
- manaba-attend（筑波大の出席カード提出 CLI、11★）: 最終 push 2021-04-30 — [GitHub](https://github.com/shuuji3/manaba-attend)
- Manaba Plus（Firefox、未提出課題の残り時間で色分け）、manabadge（筑波、未提出数バッジ）、未提出課題を隠す拡張（筑波）、小樽商大向けハイライト拡張もある — [Manaba Plus](https://addons.mozilla.org/hr/firefox/addon/manaba-plus)、[manabadge](https://chrome.google.com/webstore/detail/manabadge-for-tsukuba/llngngnaoofnfekodekfgobkabdlfmbp)、[hide-unsubmitted](https://github.com/ktchnm/chrome-extension-hide-unsubmitted-reports)、[shodaimanabahighlight](https://chrome.google.com/webstore/detail/shodaimanabahighlight/dbiedhjfponkhcehojameaacnpkfebff)
- 2026年11月にも、個人用の manaba 課題通知ツールが次々に作られている: manaba-reminder-bot（Discord 通知）、manaba-task-notifier（Spring Boot + Web Push、授業課題らしい）、manaba2timetree（TimeTree 連携）。いずれも 0★ — [manaba-reminder-bot](https://github.com/yamamomonn1010/manaba-reminder-bot)、[manaba-task-notifier](https://github.com/ponzunop/manaba-task-notifier)、[manaba2timetree](https://github.com/R-1930/manaba2timetree)

**WebClass / 学務システム**
- webclass-deadline-calendar（2026-11-17）や tcu-webclass-visual（東京都市大の WebClass 用拡張、2026-11-18）など、新しい個人ツールはあるが 0★ — [webclass-deadline-calendar](https://github.com/sekido-kibi/webclass-deadline-calendar)、[tcu-webclass](https://github.com/CYLIU2003/tcu-webclass-visual-theme-aware)
- 静岡大 学務情報システム（Gakujo）の非公式クライアントは複数ある（GakujoGUI 系、gakujo-go、gakujo-google-calendar）が、最終 push はいずれも 2022〜2023年 — [gakujo-go](https://github.com/szpp-dev-team/gakujo-go)、[gakujo-google-calendar](https://github.com/earlgray283/gakujo-google-calendar)、[GakujoGUI-WPF](https://github.com/nharu-0630/GakujoGUI-WPF)
- 電通大の addonuec（学務情報システムの不便を解消する拡張）: 最終 push 2021-09 — [GitHub](https://github.com/meditq/addonuec)

### Inferences
- （推測）「時間割を作る」こと自体は Penmark と汎用アプリで足りている。足りないのは、LMS ごとにばらばらの課題締切を集めて、手元のカレンダーに確実に流すこと。manaba だけでも同じ目的のボットや拡張が毎学期のように作られては放置されており、これは需要が強いのに定番ツールがないことを示している。
- （推測）大学のパスワードを預かる型（Orario 型）は大学から注意喚起されるので、信頼を得にくい。ブラウザ拡張のように「学生自身のログイン済みブラウザの中だけで動き、外部サーバーにデータを送らない」作りなら、この懸念を避けやすい。
- （推測）manaba の UI 改善系拡張が放置される主な理由は、作者の卒業と manaba 側の DOM 変更だと思われる（直接の証拠はない）。

### Gaps
- Penmark・その他時間割アプリの Google Play / App Store の低評価レビュー本文（2024〜2026年）は取得できなかった。検索結果にもレビュー本文は出なかった。
- Google Classroom 連携の時間割アプリの有無は調べきれていない。
- Chrome 拡張の利用者数（Web Store のユーザー数）は取得していない。
- Moodle 向けの日本の大学独自ツールは、GitHub 検索（日本語クエリ）でヒットしなかった。

## 就活管理（マイナビ等アプリ、ワンキャリア、管理アプリ、Notion/スプシ、ES管理、AI ES添削）の現状と不満、まだ無い機能

### Takeaway
AI による ES 作成・添削は明確なレッドオーシャン。少なくとも10種類の無料・サブスク型サービスが並んでいる。就活管理アプリも、個人開発の小さなアプリが大量にある。一方で「自分の過去 ES・面接ログを手元に置き、企業ごとの設問へ使い回しを提案し、締切と選考段階を一元管理する」ローカル型のツールは、目立つものが見つからなかった。

### Cited Findings
- AI ES 添削の比較記事に載っているもの: ES Maker（無料＋月額、GPT-4ベース）、AI就活サポたくん（LINE、無料）、キャリアチケット（AI＋アドバイザー）、就活AI（登録不要・無料、誤字チェック）、ES添削くん（月額）、ESの達人（月額、通過ES閲覧）、digmee（LINE、月額）、ESアドバイザー（回数課金）、ChatGPT — [CREX 2025年版](https://crexgroup.com/ja/shukatsu/self-pr-es/entry-sheet-ai-review-tools/)
- 同記事が挙げる AI 添削の弱点: 企業ごとの意図をくめず文章が画一的になる、情報が古い・誤る、ES の個人情報が学習に使われるおそれ（個人情報は「削除してから入力する」よう推奨）、そのまま使うと面接で深掘りされたとき答えられない — [CREX](https://crexgroup.com/ja/shukatsu/self-pr-es/entry-sheet-ai-review-tools/)
- 「就活ノート+AI」は、企業ごとの ES・TODO 管理、文字数カウント、AI 生成・添削ができる。App Store 評価 4.5 だが 8件しかない — [App Store 就活ノート](https://apps.apple.com/jp/app/%E5%B0%B1%E6%B4%BB%E3%83%8E%E3%83%BC%E3%83%88-ai%E3%81%A7es%E4%BD%9C%E6%88%90-%E6%B7%BB%E5%89%8A-%E5%B0%B1%E8%81%B7%E6%B4%BB%E5%8B%95%E8%A8%98%E9%8C%B2-%E7%AE%A1%E7%90%86%E3%82%A2%E3%83%97%E3%83%AA/id6479209123?l=en-US)
- 就活サイトは、Google スプレッドシートで一覧管理し、Google カレンダーで締切管理する方法を勧めている — [外資就活ドットコム](https://gaishishukatsu.com/archives/e8d9a0489a764d3da290f0e29848e584)
- 就活アプリ選びの不安として「多すぎて選べない」「悪質求人・個人情報流出が心配」「無料と有料の違いが不明」が挙げられている（調査データではなく筆者の整理） — [lifestyle.assist-all](https://lifestyle.assist-all.co.jp/?p=10908)
- 人による添削の相場: スキルマーケットは1,000円〜、コーチングは10万円〜 — [coconala マガジン](https://coconala.com/magazine/520)
- 「ES添削・面接対策」アプリ（App Store id1667756722）は、2026-11-19 に JP ストアで 404 だった。配信終了の可能性があるが、確認はできていない — [App Store](https://apps.apple.com/jp/app/id1667756722)
- GitHub の「就活 管理」リポジトリは 2026年だけで十数件ある（Next.js、PWA、SQL+Python TUI、HTML+Claude API など）が、ほぼすべて 0〜1★。ポートフォリオ用の個人作品が中心 — 例: [shukatsu-kanri (HTML+Claude API)](https://github.com/Ayumu1217/shukatsu-kanri)、[queryvault](https://github.com/saki-nya1539/queryvault)、[app-simple-job-hunting-management (PWA)](https://github.com/sato-weba/app-simple-job-hunting-management)

### Inferences
- （推測）AI ES 添削は、ナビサイトや人材会社が無料で出す「集客装置」になっている。個人開発者が単体の添削サービスで勝つのは難しい。
- （推測）残っている隙間は、汎用の添削ではなく次の3つ。(1) 自分の過去 ES・ガクチカ・面接の質問ログを再利用できる形で手元に貯めること。(2) 企業ごとの選考フローや締切を、マイナビ・ワンキャリア・企業マイページにまたがって一元化すること。(3) ES を外部サーバーに出さないこと（プライバシー不安への対応）。マイページが企業ごとに分かれている問題は、既存アプリでは解決していないように見える（直接の証拠は未取得）。
- （推測）Claude Code スキルや MCP の形で「企業別の ES・面接コーチ」を作る個人ユーザーはすでにいる。ただ、公開されて一般化したものは見つからなかった（次の AI エージェントの項を参照）。

### Gaps
- マイナビ・リクナビ・ワンキャリアの各アプリの低評価レビュー本文は取得できなかった（ツールの呼び出し回数の上限）。
- Notion テンプレートの普及度（ダウンロード数など）のデータはない。
- 2026年の AI ES 添削サービスの最新料金比較は見つからなかった（見つかった記事は 2025年版）。

## 扶養・年収の壁チェッカー、奨学金シミュレーター、家計簿、シフト管理の現状と、2025〜2026年の制度変更への追従

### Takeaway
制度は 2025年・2026年と2年続けて変わり、壁の数字が増えて複雑になった。税は 123万／150万／188万（2025年）から 136万／159万／197万（2026年分）へ、健保の被扶養者は 19〜22歳で150万円未満、勤労学生は合計所得89万円。一方、ストアの扶養アプリには「103万の壁」という古い名前のものが残っており、追従は不十分に見える。GitHub にも 2026年の個人製「扶養メーター」がいくつかあるだけで、決定版はない。

### Cited Findings
- 2025年分: 特定扶養控除（63万円）が満額になるのは学生本人の給与収入 123万円まで。新設の特定親族特別控除は 150万円まで満額、188万円で0になる — [freee（最終更新 2026/09/15）](https://www.freee.co.jp/kb/kb-payroll/university-student-dependent-deduction/)
- 2026年分（2026・2027年の所得税）: 特定扶養控除は給与収入 136万円まで。特定親族特別控除は 159万円まで満額（63万円）、159万超〜164万円で61万円、段階的に減って 194万超〜197万円で3万円、197万円超で0 — [freee](https://www.freee.co.jp/kb/kb-payroll/university-student-dependent-deduction/)
- 勤労学生控除（2026年分）: 合計所得金額 89万円以下（給与のみなら約163万円）。所得税27万円・住民税26万円の控除 — [freee](https://www.freee.co.jp/kb/kb-payroll/university-student-dependent-deduction/)
- 健康保険の被扶養者: 12/31時点で19歳以上23歳未満なら「年収150万円未満」（学生かどうかは問わない）。2026年4月からは労働契約上の収入で判定する — [freee](https://www.freee.co.jp/kb/kb-payroll/university-student-dependent-deduction/)
- 出典ごとに数字が食い違う。2026年の非課税ラインを「160万→178万」とし、その内訳を「基礎控除104万＋給与所得控除74万」とする記事と、「99万＋79万」とする記事がある。親の控除について「159万の壁」と書く記事もある — [SmartHR mag](https://mag.smarthr.jp/hr/labor/nenshu-no-kabe/)、[financial-field](https://financial-field.com/tax/entry-413039)、[マネーフォワード](https://media.moneyforward.com/articles/10508)（Web 検索の要約経由。各記事の本文は未確認）
- 「160万円の壁：2025年12月から適用」と書く紹介記事もある（公的資料で照合していない） — [habitto](https://www.habitto.com/blogs/baito-dai-kanri-app-kyuryo-keisan-shift/)
- ストアには「103万の壁 ‑ 扶養の壁を超えないように毎月の収入を管理」というアプリが残っている。名前は旧制度のままで、2025年改正への追従は説明文から確認できない — [App Store](https://apps.apple.com/jp/app/103%E4%B8%87%E3%81%AE%E5%A3%81-%E6%89%B6%E9%A4%8A%E3%81%AE%E5%A3%81%E3%82%92%E8%B6%85%E3%81%88%E3%81%AA%E3%81%84%E3%82%88%E3%81%86%E3%81%AB%E6%AF%8E%E6%9C%88%E3%81%AE%E5%8F%8E%E5%85%A5%E3%82%92%E7%AE%A1%E7%90%86/id1586405774)
- 「シフト手帳 byGMO」は、シフトから給料を自動計算して扶養の範囲を把握する用途で紹介されている — [habitto](https://www.habitto.com/blogs/baito-dai-kanri-app-kyuryo-keisan-shift/)
- GitHub の扶養系個人ツール: fuyo-meter（大学生向け、SwiftUI、2026-08）、扶養メーター（時給防衛隊、2026-06）、baito-app（シフト→収入・扶養上限、2026-11）、work-income-tracker（2025-07）、kakutei-fuyou-navi（フリーランス向け、ブラウザ内保存）。いずれも 0★ — [fuyo-meter](https://github.com/peipay0603/fuyo-meter)、[fuyou-meter](https://github.com/Aynyan2828/fuyou-meter)、[baito-app](https://github.com/kantantantanmen/baito-app)、[work-income-tracker](https://github.com/yuta2422/work-income-tracker)、[kakutei-fuyou-navi](https://github.com/keilovesnow2-design/kakutei-fuyou-navi)
- 奨学金（JASSO）: 所得連動返還方式から定額返還方式への変更は貸与中だけ。定額→所得連動は返還開始後もできる。2026年10月〜2027年9月の返還月額を算出するため、扶養に関する申告書とマイナンバーの提出を求めている（期限 2026/6/12）。子の数に応じた控除もある — [JASSO 2025満期](https://www.jasso.go.jp/news/2025mankihenko.html)、[JASSO お知らせ](https://www.jasso.go.jp/news/1216294_1579.html)
- GitHub の奨学金シミュレーター系はほぼない。Laravel 製は 2022年で止まっている。自治体の給付金・奨学金 DB（shien-db、2026-07）や学振DC採用解析（2025-09）がある程度 — [LaravelScholarship](https://github.com/JunyaSatou/LaravelScholarship)、[shien-db](https://github.com/mukkuryo629-byte/shien-db)、[gakushin_kaiseki](https://github.com/YoheiOhto/gakushin_kaiseki)

### Inferences
- （推測）扶養チェッカーは「アプリは多いが、正しい最新値を持つものが少ない」領域。税（親の控除の3段階）、本人の所得税・住民税、勤労学生控除、健保150万円、勤務先の社保加入（週20時間など）は別々の壁で、これらを同時に月次で見られるツールは確認できなかった。毎年制度が変わるので、定数を年度ごとに差し替えやすい OSS（データファイル＋出典URL付き）にする価値がある。
- （推測）奨学金については、JASSO 公式に返還シミュレーションがある（ページ自体は今回未取得）。ただ「定額か所得連動か」「繰上返還」「減額返還」の比較をローカルで回せる個人向けツールは見当たらなかった。

### Gaps
- JASSO 公式の返還シミュレーターの仕様と、2025〜2026年に改修されたかどうかは未確認。
- 2026年の基礎控除の正確な額（95万・99万・104万など出典で異なる）は、国税庁の一次資料で確認していない。報告書には国税庁リンクで確定させる必要がある。
- 健保150万円特例の施行日（2025年10月とされることが多い）は一次資料で確認していない。
- 家計簿アプリ（Zaim、マネーフォワード ME 等）の学生向け機能と低評価レビューは調べていない。
- 扶養アプリのストアレビューは取得できなかった。

## GitHub 上の日本の学生向け OSS（卒業要件チェッカー、履修計画、シラバス検索、大学別の非公式ツール）の量と放置状況

### Takeaway
数はかなり多いが、ほぼすべてが「1大学・1学部・1学年カリキュラム」専用で、スターは 0〜10 程度。大学をまたいで使える汎用の卒業要件・履修計画エンジンは見当たらない。中規模の学生団体プロジェクト（Twin:te、manaba-enhanced）も archived か停滞している。

### Cited Findings
- 卒業要件チェッカー（2025〜2026年に更新があるもの）: 琉球大（2件）、神戸大 国際人間科学部（教員免許要件込み）、筑波大 mast/klis（8★）、筑波大 心理学類、阪大 経済、和歌山大 経済、AIU、共創情報コース、汎用をうたう tanni_simulator（3★）、syllabus-manager — [graduation-requirements-checker](https://github.com/ore-orange/graduation-requirements-checker)、[kokutan](https://github.com/youjyoutepu-source/kokutan)、[Graduation-Checker](https://github.com/Mimori256/Graduation-Checker)、[tanni_simulator](https://github.com/Rerurate514/tanni_simulator)、[osaka-university-credit-checker](https://github.com/sea2896-code/osaka-university-credit-checker)、[aiu-risyu](https://github.com/kirishio1019-jpg/aiu-risyu)、[syllabus-manager](https://github.com/slopejp/syllabus-manager)
- 電通大 uec-fulfilled（学務システム上で必要単位を一発確認するブックマークレット、10★、2026-02） — [GitHub](https://github.com/trpfrog/uec-fulfilled)
- 履修組み支援: 筑波 coins23 向け alx（8★、2026-11-18 更新） — [GitHub](https://github.com/arata-nvm/alx)
- シラバス検索（非公式）: 広島大 momiji2（2026-08）、INIAD syllahub（2026-03）、高専シラバス一括DL CLI（7★、2025-04）、UEC CampusSquare 取得 CLI（2023）、UNIPA スクレイパ（2018）、kstm-su（2018） — [momiji2](https://github.com/swawa-yu/momiji2)、[syllahub](https://github.com/imoken777/syllahub)、[fetch-kosen-syllabus](https://github.com/BonyChops/fetch-kosen-syllabus)、[dump-uec-campussquare-syllabus](https://github.com/nakanokurenai/dump-uec-campussquare-syllabus)、[UNIPA-Scrapar](https://github.com/unotovive/UNIPA-Scrapar)
- 筑波大 KdB パーサ: twinkle-parser（10★、2026-11-17 更新）と twinte-parser（15★、2023 停止） — [twinkle-parser](https://github.com/nandenjin/twinkle-parser)、[twinte-parser](https://github.com/twin-te/twinte-parser)
- Twin:te: フロントエンド（40★）は archived（最終 2024-04）。Android は 2026-09 に push、LP は 2026-10 に push。プロジェクトが続いているかは不明 — [twinte-front](https://github.com/twin-te/twinte-front)、[twinte-android](https://github.com/twin-te/twinte-android)
- 時間割を iCal に変換する twincal2（筑波 Twins、12★）: 2017年で停止 — [GitHub](https://github.com/gam0022/twincal2)
- codeforjapan/StudyAtHome（おうちで時間割、31★）: 2026-11 にも push がある（主に小中高向けと思われる） — [GitHub](https://github.com/codeforjapan/StudyAtHome)

### Inferences
- （推測）OSS は筑波・電通・静岡・京大など、情報系の学生が多い大学に偏っている。ほかの大学には空白がある。
- （推測）卒業要件は大学ごとに大きく違うので、OSS は乱立して放置されやすい。「要件を宣言的なデータファイル（YAML 等）で書き、成績 CSV や PDF を読んで判定する汎用エンジン」にして、各大学の要件ファイルを学生が持ち寄る形にすれば、1大学専用で終わる問題を避けられる可能性がある。
- （推測）放置の典型的なパターン: 作者の卒業、学務システムの更新（UNIPA→新システム等）、大学側の DOM 変更。

### Gaps
- GitHub 検索で「moodle 大学」「シラバス 大学」「時間割 大学」「履修 大学」のように語を組み合わせるとヒット0件になり、検索漏れがある。網羅的な件数は出していない。
- 各リポジトリの利用者数（実際に使われているか）は分からない。

## AI エージェント向け（MCP サーバー、Claude/ChatGPT スキル、GPTs）で学生向けのもの

### Takeaway
日本の大学向け MCP サーバーは数件しかない（manaba-mcp 1★、ZEN大シラバス MCP 6★、慶應SFCシラバス MCP 4★）。海外では Moodle MCP が複数あり、最大 209★。日本の LMS（manaba・WebClass・各大学の学務システム）、就活、扶養計算向けの公開 MCP やスキルはほぼ空白。

### Cited Findings
- raspi0124/manaba-mcp: 1★、最終 push 2026-04-23 — [GitHub](https://github.com/raspi0124/manaba-mcp)
- sifue/zen-syllabus-mcp: ZEN大学シラバスの MCP。6★、最終 push 2025-04-13。「フロントエンドエンジニアになるためのオススメ科目」といった履修相談の例が紹介されている — [GitHub](https://github.com/sifue/zen-syllabus-mcp)、[LobeHub](https://lobehub.com/ja/mcp/sifue-zen-syllabus-mcp)
- Koyach/sfc-syllabus-mcp: 慶應SFCシラバス検索 MCP。4★、最終 push 2026-04-11 — [GitHub](https://github.com/Koyach/sfc-syllabus-mcp)
- 海外の Moodle MCP: Faixiang/Moodle-MCP（209★、読み取り専用、2026-11）、loyaniu/moodle-mcp（58★）、G36maid/moodle-mcp（30★）、IsaacAnwar/moodle-mcp（学生自身の Moodle を読み取り専用で接続、2026-11）、matheussilvano/moodle-mcp（学生のアカウントを Claude Code に接続） — [Faixiang](https://github.com/Faixiang/Moodle-MCP)、[loyaniu](https://github.com/loyaniu/moodle-mcp)、[IsaacAnwar](https://github.com/IsaacAnwar/moodle-mcp)、[matheussilvano](https://github.com/matheussilvano/moodle-mcp)
- GitHub 検索「就活 mcp」「大学 mcp」は 0件 — （2026-11-19 の gh search repos の結果）
- 就活 × LLM の個人作品は「HTML + Claude API の就活管理ツール」程度（1★） — [shukatsu-kanri](https://github.com/Ayumu1217/shukatsu-kanri)

### Inferences
- （推測）Moodle MCP が 200★ を超えるのは、Moodle に公式の Web Service API があるからだと思われる。manaba・WebClass・UNIPA・CampusSquare には学生が使える公開 API がないので、MCP を作るにはスクレイピング（とログイン情報）が必要になり、配布しにくい。だから日本の LMS 向け MCP は少ないと考えられる。
- （推測）ログインが不要な公開データには、規約リスクの低い MCP の余地がある。具体的には、公開シラバス、学年暦、JASSO・国税庁の制度値、企業の公開採用情報。シラバス MCP が ZEN大・SFC の2件しかないので、ほとんどの大学は未開拓。
- （推測）GPTs ストアの日本の学生向け GPTs（ES 添削 GPT 等）は存在が予想されるが、今回は一次確認できていない。

### Gaps
- ChatGPT GPTs ストアの日本の学生向け GPTs の件数と評価は調べられなかった（検索結果に出なかった）。
- Claude スキル・プラグインの公開マーケットで学生向けのものは未調査。
- manaba-mcp の README（認証方式、スクレイピングかどうか）は取得できなかった。

## 学生向けツールで個人開発者が失敗しやすい点

### Takeaway
失敗パターンは4つ。(1) 大学のパスワードを預かると大学から公式に注意喚起される（京大・横国の例）。(2) 大学ごとにシステムが違うので、1校専用で終わり作者の卒業とともに放置される。(3) 大学が公式アプリを出すと存在意義を失う（京大は非公式アプリをきっかけに公式アプリを作った）。(4) 収益化が難しく、大手が無料で出すもの（Penmark、ナビ系の AI 添削）と正面から競合する。

### Cited Findings
- 京大は、ECS-ID とパスワードを入力させる非公式アプリ（Orario 等）に 2017年から注意喚起している。学生から「住所や両親の氏名が載った KULASIS の情報を第三者企業が取れる」という懸念も出ている。大学は配信停止要請まではしていない — [京大 2019 回答](https://www.kyoto-u.ac.jp/sites/default/files/embed/jaeducation-campusclimaildocuments2019a0330.pdf)
- 京大は、非公式アプリが出回ったことをきっかけに、2018年11月に公式「KULASIS アプリ」を作成した — [同上](https://www.kyoto-u.ac.jp/sites/default/files/embed/jaeducation-campusclimaildocuments2019a0330.pdf)
- 横浜国大は、大学名を冠した非公式アプリに ID・パスワードを入力しないよう注意喚起している — [横国 ハンドブック](https://www.ynu.ac.jp/campus/guide/handbook/pdf/ori_09.pdf)
- 非公式アプリの開発者は「大学とは無関係」「問い合わせは開発者へ」と明記している（中央大向け Chuinfo、大学食堂アプリ（非公式）） — [Chuinfo](https://apps.apple.com/hn/app/chuinfo-%E4%B8%AD%E5%A4%AE%E5%A4%A7%E7%94%9F%E5%90%91%E3%81%91%E9%9D%9E%E5%85%AC%E5%BC%8F%E3%82%A2%E3%83%97%E3%83%AA/id6670358906)、[大学食堂アプリ](https://apps.apple.com/us/app/%E5%A4%A7%E5%AD%A6%E9%A3%9F%E5%A0%82%E3%82%A2%E3%83%97%E3%83%AA-%E9%9D%9E%E5%85%AC%E5%BC%8F/id6480020544)
- 学生開発者がアプリ開発での技術選定と挑戦を発表している（Speaker Deck） — [akidon0000](https://speakerdeck.com/akidon0000/da-xue-sheng-xiang-keahurinokai-fa-nioite-rekasitosi-tuteitaji-shu-wocai-yong-sitali-you-xue-sheng-kai-fa-zhe-notiao-zhan)（内容は未取得）
- Penmark はパスワードを求めず、大学メールだけを求める方式をとっている。それでも「大学メール入力が不安」というレビューがある — [App Store Penmark](https://apps.apple.com/JP/app/id1440444406)
- archived や長期停止の例: manaba-enhanced（archived 2025-01）、twinte-front（archived 2024-04）、Gakujo 系（2022〜2023）、twincal2（2017） — 前掲の GitHub リンク

### Inferences
- （推測）規約・個人情報リスクが最も低いのは次の設計: 外部サーバーなし（ローカル／ブラウザ内保存）、大学のパスワードを扱わない（学生自身がログインしたブラウザの中で動く拡張機能、または学生が自分でダウンロードした CSV・PDF・ICS を読み込む方式）、公開データだけを使う。
- （推測）1大学専用で終わる問題への対策: 大学固有の部分（セレクタや要件定義）をデータファイルに分け、コミュニティが追加できるようにする。

### Gaps
- 大学から削除・停止を正式に求められた具体的事例は見つからなかった。
- manaba（朝日ネット）の利用規約で自動取得が禁止されているかは、一次資料で確認していない。
- 個人開発の学生アプリの収益化・失敗談（Zenn/note の開発記）は今回ほぼ取得できなかった。

## 個人開発者が軽量ソフトで埋められる隙間（候補一覧）

### Takeaway
レッドオーシャン: 時間割作成アプリ、AI ES 添削、汎用の就活管理アプリ、汎用家計簿。ブルーオーシャン寄り: LMS 横断の締切集約（ローカル・ICS 出力）、制度値を年度ごとに差し替えられる「年収の壁」統合チェッカー、汎用の卒業要件エンジン、公開シラバス・制度値の MCP、ローカル保存の ES・面接ログ再利用ツール。

### Cited Findings
- 根拠は上の各セクションの出典を参照。特に重要なもの: manaba 課題ツールが乱立・放置されている（[manaba-enhanced archived](https://github.com/manaba-enhanced-for-tsukuba/manaba-enhanced)、[manaba-report-integration 2023停止](https://github.com/twin-te/manaba-report-integration)）、2026年の壁の数字（[freee](https://www.freee.co.jp/kb/kb-payroll/university-student-dependent-deduction/)）、旧名「103万の壁」アプリ（[App Store](https://apps.apple.com/jp/app/103%E4%B8%87%E3%81%AE%E5%A3%81-%E6%89%B6%E9%A4%8A%E3%81%AE%E5%A3%81%E3%82%92%E8%B6%85%E3%81%88%E3%81%AA%E3%81%84%E3%82%88%E3%81%86%E3%81%AB%E6%AF%8E%E6%9C%88%E3%81%AE%E5%8F%8E%E5%85%A5%E3%82%92%E7%AE%A1%E7%90%86/id1586405774)）、日本の大学向け MCP が3件しかないこと（[manaba-mcp](https://github.com/raspi0124/manaba-mcp)、[zen-syllabus-mcp](https://github.com/sifue/zen-syllabus-mcp)、[sfc-syllabus-mcp](https://github.com/Koyach/sfc-syllabus-mcp)）。

### Inferences
以下はすべて推測（市場検証はしていない）。形式と、既存ツールとの違いを併記する。

1. **年収の壁 統合チェッカー（単一 HTML、端末内保存）**: 月ごとのバイト収入を入力すると、親の特定扶養控除と特定親族特別控除（年度別テーブル）、本人の所得税・住民税、勤労学生控除、健保の被扶養者150万円、勤務先の社保（週20時間等）を同時に判定し、「あと月いくらまで」を出す。制度値は出典 URL 付きの JSON で年度ごとに差し替える。既存ツールとの違い: 旧名アプリの残存、記事ごとの数字の食い違い、0★個人アプリの乱立。Python CLI 版や MCP 版にも展開しやすい。
2. **LMS 締切 → ICS 変換（ブラウザ拡張、外部送信なし）**: manaba・WebClass・Moodle などの未提出課題ページを、学生自身のログイン済みブラウザで読み、.ics ファイルとして出力するか購読用 URL を出さずにダウンロードさせる。大学ごとのセレクタは設定ファイルで追加できるようにする。既存ツールとの違い: Twin:te 連携は2023年に停止、個人ボットは Discord 依存でパスワード保存型が多い。
3. **汎用 卒業要件エンジン（Python CLI ＋ 単一 HTML）**: 要件を YAML で宣言し、学生が成績表の CSV・PDF を読み込むと、不足単位を区分別に表示する。大学・学部ごとの要件ファイルは PR で集める。既存ツールとの違い: 1学部専用のチェッカーが10件以上散らばっている。
4. **公開シラバス MCP の汎用化**: シラバスの公開ページ（ログイン不要）を取り込み、履修相談に答える MCP サーバーやスキル。現状は ZEN大・SFC の2件のみ。サイトの規約（robots・利用規約）を大学ごとに確認する必要がある。
5. **就活 ES・面接ログのローカル再利用ツール（Claude Code スキル／MCP、ローカル Markdown・SQLite）**: 過去の ES 回答、ガクチカの素材、面接で聞かれた質問を手元に貯め、新しい設問に近い過去回答と文字数調整案を出す。締切と選考段階の一覧も持つ。既存ツールとの違い: AI 添削は集客型のクラウドサービスで、個人情報の不安がある。管理アプリは 0★ の個人作品が乱立している。
6. **奨学金 返還方式比較（単一 HTML）**: 定額と所得連動、繰上返還、減額返還・返還期限猶予を、自分の想定年収で並べて比較する。JASSO 公式のシミュレーターとの違いは要確認（未調査のため、作る前に検証が必要）。
7. **非推奨（レッドオーシャン）**: 時間割アプリ単体、AI ES 添削単体、汎用家計簿。

### Gaps
- 上の各候補について、実際の学生が今どう困っているか（一次インタビュー、SNS の声）は未検証。ユーザーのメモにある方針「作る前に検証」に従い、候補ごとに学生の声を集める必要がある。
- 候補2・4 は、各大学・LMS の利用規約を確認していない。
