# 検証C: 「0ユーザーで終わる個人開発のマーケティングを肩代わりする AI スキル」は作る価値があるか

調査日: 2026-11-19
表記: **[事実]** は出典で確認した内容、**[推測]** は私の解釈や推論。URL は各項目の末尾に付けた。
注意: Reddit・Indie Hackers・Stack Overflow の個別ページは取得が拒否された（403 など）ものが多く、その場合は検索結果の要約から引いている。そのことは各所に書いた。X の投稿は検索ツールでは直接調べられなかった（§1-4）。

---

## 結論（先に）

**今は作らない。** まず2週間、手作業で試す（§5）。その結果が基準を超えたら、狭い形でだけ作る。
（最初の版では「形を変えて作る」としていた。ユーザーから「本当に困りごとを解決するのか疑問」と指摘があり、**本物の痛みの証拠**、つまり他の開発者が繰り返す不満と、自分で回避策を作っている人を最も重く見て評価し直した。§0 を参照。）

**痛みの判定（要点）:**
- 「個人開発は誰にも使われない」という**大きな痛み**は本物で、証拠は強い（英語圏）。ただし最大の原因は宣伝ではなく、誰も欲しがっていないこと。
- 「探して答える」型の**回避策を自作する人**は、英語圏（Reddit）にはとても多い。日本語圏では見つからなかった。日本語圏で自作されているのは**告知の自動化**（Zenn 記事を X に自動投稿、複数サイトへの同時投稿）だけ。
- **今回の狭い形（日本語の個人開発 OSS が答えになる質問を探して返信する）を求める声は、1件も見つからなかった。** 痛みの証拠は**弱い**。
- 対象ユーザーの第一号であるユーザー自身が、2026-11-19 に「masume は宣伝しない」と決めている。これも、この痛みが強くないことを示す。

以下は最初の版の要点（事実はそのまま有効）。

1. **困りごとは本物。ただし半分は「マーケティング」ではなく「誰も欲しがっていない」問題。** 失敗した約80社の分析では、致命的な失敗の 56% がマーケティング関連だった。ただしその最大要因はプロダクト・マーケット・フィット（PMF）の欠如だった（§1-1）。
2. **英語圏は飽和している。** マーケティングスキル集の最大手は 61.4k スター、53 スキル。開発者ツール向けの GTM スキル集もある（first-50-users、research-the-market、know-if-its-working）。Reddit で見込み客を探すツールは「11か月で競合100社」と言われるほど多い（§2）。
3. **空いているのは「日本語 × 個人開発 OSS × その道具がまさに答えになる質問を探す × 人が確認して投稿 × GitHub の数字で効果を測る」の組み合わせだけ。** 日本語版のスキルは 0〜2 スターのものしか見つからなかった。知恵袋・teratail・Qiita・Zenn の質問を探して返信を下書きするツールは見つからなかった（§3）。
4. **危険も大きい。** HN は AI が書いた・AI が手を入れたコメントを明文で禁じている。X はキーワード検索だけを根拠にした自動返信を禁じている。Zenn は宣伝が主目的の記事を避けるよう求めている。awesome リストは AI スパムで投稿受付を止め始めた（§4）。
5. **追い風ばかりでもない。** Stack Overflow の質問数はピークから 70% 以上減った。人が困りごとを公開の Q&A に書かず AI に聞くようになったため、「質問を探して答える」チャネル自体が細っている（§4-6）。

**いちばん狭い、まだ空いている形（作るならこれ。ただし痛みの証拠は弱い）:**
「日本語の個人開発 OSS 向けに、その道具が**直接の答えになる**日本語の質問や Issue（teratail、Qiita/Zenn、GitHub Issues、スタック・オーバーフロー日本語版、知恵袋は読むだけ）を探す。開示付きの返信を1件ずつ下書きし、**投稿は人が手でする**。GitHub traffic の参照元とスター数で、どの返信が効いたかを測る」Claude Code スキル。
ただし**作る前に**、masume と kanjiframe で2週間、手作業で同じことをやる（§5）。質問が見つからなければ、それ自体が「この2つには需要が見えない」という結果になる。

---

## 0. 痛みの証拠の強さ（いちばん重く見る部分）

ユーザーの疑問「本当に困りごとを解決するのか」に答えるため、証拠を3段階に分けて評価した。広い痛みと狭い痛みで、強さはまったく違う。

| 痛み | 不満の声 | 自分で回避策を作る人 | 判定 |
|---|---|---|---|
| A. 個人開発が誰にも使われない（広い） | 多い（§1-3 で9つの論点） | 多い（下記） | **強い**。ただし原因の半分以上は PMF |
| B. 宣伝が嫌い・面倒 | 英語圏の IH に多数、日本語は少数。割合の調査はない | 告知の自動化ツールを作る人はいる（日本語圏も） | **中**。逸話のみ |
| C. 「自分の OSS が答えになる日本語の質問」を探すのが大変（今回の狭い形） | **0件**見つからない | **0件**見つからない | **弱い・未確認** |

### 0-1. 英語圏: 回避策を自作する人がとても多い（痛み A・「探す」部分）
- **[事実]** Reddit で顧客を探すツールを「自分が困ったから作った」という投稿が IH に多数ある。「手作業が遅く、2回シャドウバンされたので作った」「機会を逃すのにうんざりして作った」「Reddit スレッドを探す小さなツールを作った、役に立つか」など。 — [IH: finds customers on reddit before your competitors do](https://www.indiehackers.com/post/i-built-a-tool-that-finds-customers-on-reddit-before-your-competitors-do-bf7b1c9003), [IH: tired of missing opportunities](https://www.indiehackers.com/post/i-built-a-tool-to-find-reddit-leads-for-saas-founders-because-i-was-tired-of-missing-opportunities-7186d5d115), [IH: small tool to find relevant reddit threads](https://www.indiehackers.com/post/i-built-a-small-tool-to-find-relevant-reddit-threads-is-this-useful-for-founders-9ed7978a1a), [IH: find people already talking about problems your product solves](https://www.indiehackers.com/post/i-built-a-tool-to-find-people-already-talking-about-problems-your-product-solves-dbca80a1cb), [IH: from manually searching reddit to automating it](https://www.indiehackers.com/post/from-manually-searching-reddit-to-automating-it-how-i-built-leadsfromurl-as-a-solo-founder-RMbfofpubJn8kaEKdyBc)
- **[事実]** GummySearch（1人で作った Reddit 調査ツール）は「13万5千人以上の創業者・マーケター・投資家が頼った」と閉鎖の告知に書いている。 — [GummySearch: The Final Chapter](https://gummysearch.com/final-chapter/)
- **[事実]** Reddit マーケティングツールで「4か月で MRR $30K」という作者本人の主張がある（未検証）。 — [IH: Reddit marketing tool to 30k MRR in 4 months](https://www.indiehackers.com/post/how-i-built-a-reddit-marketing-tool-to-30k-mrr-in-4-months-with-0-spent-on-marketing-470f39b763)
- **[事実]** marketingskills は 61.4k スター。cro スキルは skills.sh で 92,775 インストールという数字がある。 — [marketingskills](https://github.com/coreyhaines31/marketingskills), [skillselion ガイド](https://skillselion.com/guides/marketing-skills-claude-code)
- **[推測]** 英語圏では痛み A に対し、人がお金と時間を払っている。痛みは本物。ただしそのぶん、すでに解決策で埋まっている。

### 0-2. 反対の証拠: 道具では解決しなかった例
- **[事実]** 「開発者マーケティングを自動化するツールを作ったが、まだ反応がない。何が足りない？」という IH 投稿がある。 — [IH: built a tool to automate my dev marketing, no real traction yet](https://www.indiehackers.com/post/built-a-tool-to-automate-my-dev-marketing-no-real-traction-yet-what-am-i-missing-38af8a0203)
- **[事実]** 「誰も頼んでいない製品のユーザー探しについて、誰も教えてくれなかったこと」という投稿がある。 — [IH: finding users for a product nobody asked for](https://www.indiehackers.com/post/what-nobody-told-me-about-finding-users-for-a-product-nobody-asked-for-70e96e97be)
- **[事実]** 「この種のスクリプトを動かして Reddit から永久 BAN された」という作者の報告がある（検索要約から）。また「初期はどんな道具より、コミュニティで直接話す方が効く」というコメントもある。 — [IH: finds your first customers by searching reddit threads](https://www.indiehackers.com/post/i-built-a-tool-that-finds-your-first-customers-by-searching-reddit-threads-with-real-buying-intent-playbook-e54c60036b), [IH: commenting on reddit threads changed how I get customers](https://www.indiehackers.com/post/i-know-this-sounds-dumb-but-commenting-on-reddit-threads-changed-how-i-get-customers-96d566cd5a)
- **[事実]** Failory の分析では、マーケティングの失敗の半分以上は PMF の欠如だった（§1-1）。 — [Failory](https://www.failory.com/blog/startup-mistakes)
- **[推測]** 「誰にも使われない」の多くは、探す道具や返信の下書きでは治らない。

### 0-3. 日本語圏: 自作されているのは「告知の自動化」だけ
- **[事実]** 日本語圏で見つかった自作の回避策は、Zenn の記事公開を GitHub Actions と X API で X に自動告知する仕組み、Zenn・Qiita・ポートフォリオへの自動公開パイプライン、Zenn・Qiita 連携ツールなど。どれも「自分から発信する」ためのもの。 — [Zenn: Zenn 更新を X に自動告知](https://zenn.dev/irongeneral21/articles/zenn-x-autotweet), [dev.to: Notion から Qiita・Zenn への自動公開](https://dev.to/norinori1/i-built-an-auto-publishing-pipeline-from-notion-to-qiita-zenn-and-my-portfolio-4f68), [Zenn: Zenn 自動公開パイプライン](https://zenn.dev/saytooy_arch/articles/14-zenn-auto-publish-pipeline), [Zenn: Zenn・Qiita 連携ツール](https://zenn.dev/shun1997/articles/zenn-qiita-integration-tools), [multi-platform-publisher](https://github.com/pipipi-dev/multi-platform-publisher)
- **[事実]** 「自分の道具を必要としている人の質問を探す」ために自作した、という日本語の記事やリポジトリは見つからなかった（§2-5 の GitHub 検索、上記の Web 検索）。
- **[事実]** 日本語の不満は、Zenn の「よいものを作れば売れるはず、を超えていけ」のような**助言記事**が中心で、本人の「使われない」という一人称の嘆きは少数だった。X は検索できなかった（§1-4）。 — [Zenn neko](https://zenn.dev/neko/articles/1fc06017d7e244), [Zenn yuto_tradenote](https://zenn.dev/yuto_tradenote/articles/5134cd017d44748cfb27)
- **[推測]** 日本語圏で空いているのは、需要がまだ満たされていないからではなく、**需要が見えないから**かもしれない。どちらなのかは、今回の資料では区別できない。

### 0-4. いちばん近い当事者（ユーザー自身）の行動
- **[事実]** ユーザーは 2026-11-19、masume について「ポートフォリオとして置き、宣伝はしない」と決めた（プロジェクトメモ）。
- **[推測]** 対象ユーザーそのものの立場で、宣伝の道具がなくて困っているのではなく、宣伝する理由が弱いから宣伝しなかった。これは痛み C が弱いことを示す、最も身近な証拠。

### 0-5. 判定
- **[推測]** 痛み A（広い）は強いが、英語圏はすでに埋まっている。原因の多くは道具では治らない。
- **[推測]** 痛み C（今回の狭い形）は、不満も回避策も見つからなかった。**証拠ははっきり弱い。** 「空いている」は「欲しい人がいる」の証拠にはならない。
- **[推測]** だから「作る」の前に、2週間の手作業テスト（§5）で「答えるべき質問が実在するか」と「ユーザー自身が続けたいと思うか」を確かめる。どちらかが No なら作らない。

---

## 1. 困りごとは本物か、どのくらい大きいか

### 1-1. 数字のある資料
- **[事実]** Failory が失敗したスタートアップの創業者に行ったインタビュー（83社）では、「致命的なマーケティングの失敗は他の致命的な失敗をすべて合わせたより多い（56% 対 44%）」。83社中46社が、失敗の主な理由にマーケティングの問題を挙げた。最も多い失敗理由は PMF の欠如で、マーケティングの失敗の半分以上を占めた。 — [Failory: startup mistakes](https://www.failory.com/blog/startup-mistakes)
  - **[推測]** 「マーケティングの失敗」の中身の半分は「欲しがる人がいない」。宣伝が上手くなっても救えない層が大きい。
- **[事実]** Product Hunt のローンチ 5,639 件（票数が分かるもの）を分析した投稿では、中央値は3票、11.5%（651件）は0票だった（Indie Hackers の個人分析、ページ本体は取得できず検索要約から）。 — [IH: the median indie launch last week got 3 upvotes](https://www.indiehackers.com/post/the-median-indie-launch-last-week-got-3-upvotes-d1c2406a1f)
- **[事実]** 2024年9月時点で、Product Hunt で featured になるのはローンチの約10%という集計がある（二次資料）。 — [awesome-directories の PH ガイド（scour.ing 経由）](https://scour.ing/p/https://awesome-directories.com/blog/product-hunt-launch-guide-2025-algorithm-changes)
- **[事実]** 2016年の GitHub 約1,700万リポジトリの分析では、80% のリポジトリがスター0、99% がスター13以下だった（古いデータ）。 — [arXiv 1603.00431 On GitHub's Programming Languages](https://arxiv.org/pdf/1603.00431)
- **[事実]** App Store の「ゾンビアプリ」（ランキングに一度も載らないアプリ）は、2014年6月時点で 79.6%（Adjust 調べ）。ダウンロード数そのものではなく、Apple は個別のダウンロード数を公開していない。 — [Engadget 2012](https://www.engadget.com/2012-08-06-app-store-growing-populated-with-never-downloaded-zombie-apps.html), [Statista: 90% of all iOS apps are zombies](https://www.statista.com/chart/amp/5715/90-of-all-ios-apps-are-zombies)
- **[事実]** 「個人開発者が集客を課題とする割合」を測った日本語の調査は見つからなかった。開発者がマーケティングを嫌う割合を測った調査も見つからなかった（検索した範囲）。
- **[事実]** 20人の個人開発者を対象にした小さな定性調査（ベンダーのページ）では、個人開発者は従来のマーケティングから離れているが、主な理由は思想ではなく「お金がない・うまくいかない」からだという。 — [Perspective.ai: Solo Dev Journey](https://getperspective.ai/published/page/689cc9369dd5959e7783dcc5)

### 1-2. 「AI で作るのが簡単になり、売れない作品が増えた」という主張
- **[事実]** 「AI で出荷はほぼ無料になり、ボトルネックは注目を集めることに移った」「バイブコーディングは作ることを民主化したが、売ることは民主化しなかった」という論調のブログが多数ある。「1日20万件以上のバイブコーディング案件が作られる」という数字も出回るが、出典は確認できなかった。 — [dev.to: Your vibe-coded side hustle has no customers](https://dev.to/mrclaw207/your-vibe-coded-side-hustle-has-no-customers-and-its-not-because-of-the-code-4217), [IH: the bottleneck flipped](https://www.indiehackers.com/post/the-bottleneck-flipped-and-most-indie-hackers-we-havent-noticed-d64a3723b7), [vantaige: Everyone's Vibe-Coding. Nobody's Getting Customers](https://vantaige.io/blog/vibe-coding-no-customers-ai-marketing-fix-2026)
- **[推測]** この論調を書いているのは AI マーケティングツールの売り手が多い。「需要がある」証拠であると同時に「売り手が多い」証拠でもある。

### 1-3. 繰り返し出てくる不満（別々の論点ごとに数えた）
数は投稿の件数ではなく、**別々の論点の数**。出典は英語（IH、dev.to、HN 由来）と日本語（Zenn、CodeZine）。

| # | 不満 | 主な出典 |
|---|---|---|
| 1 | 作ったが見つけてもらえない。ダウンロードが数十しかない | [Zenn: よいもの作ったら売れるはずを超えていけ](https://zenn.dev/neko/articles/1fc06017d7e244), [Zenn: 半年で1万DLのiOSアプリ](https://zenn.dev/yuto_tradenote/articles/5134cd017d44748cfb27) |
| 2 | 「良いものを作れば口コミで広がる」と思い込んでいた | 同上 [Zenn neko](https://zenn.dev/neko/articles/1fc06017d7e244), [arte: 最初の100人](https://arte.itlibra.com/ja/articles/indie-dev-first-100-users) |
| 3 | マーケティングが嫌い、面倒、作る方が楽しい | [IH: but I really hate marketing](https://www.indiehackers.com/post/but-i-really-hate-marketing-c66aafd96c), [IH: why do you hate marketing](https://www.indiehackers.com/post/why-do-you-hate-marketing-5d4d653d2a), [IH: why so much hate for marketing](https://www.indiehackers.com/post/why-so-much-hate-for-marketing-987801e04c), [Heavybit: Why Do Developers Hate Marketing](https://www.heavybit.com/library/article/developer-marketing-mistakes) |
| 4 | どこにユーザーがいるか、どのチャネルを使えばいいか分からない | [IH: biggest marketing challenges](https://www.indiehackers.com/post/what-are-your-biggest-marketing-challenges-as-an-indie-hacker-2578eb4d51), [IH: why do indie developers find it so hard to promote](https://www.indiehackers.com/post/why-do-indie-developers-always-find-it-so-hard-to-promote-their-products-54d9ce5f00) |
| 5 | ローンチしたが反応ゼロ（HN 1点・0コメント・0登録など） | [IH: launched on HN to zero signups](https://www.indiehackers.com/post/i-built-a-saas-in-9-days-for-200-launched-on-hn-to-zero-signups-heres-what-actually-happened-87c39638c6), [IH: tired of building apps that get 0 users](https://www.indiehackers.com/post/tired-of-building-apps-that-get-0-users-i-was-too-heres-what-i-m-testing-to-fix-it-bbc654110c) |
| 6 | 宣伝したらスパム扱い・アカウント停止になった | [IH: I got 4 reddit accounts banned](https://www.indiehackers.com/post/i-got-4-reddit-accounts-banned-before-i-figured-this-out-c223ec73d6) |
| 7 | 作る前に需要を確かめなかった | [Zenn: 個人開発の落とし穴](https://zenn.dev/pikum/articles/pikum-personal-development-mistake), [coconala: 作る前に需要を測る](https://coconala.com/blogs/3938407/786146), [Failory](https://www.failory.com/blog/startup-mistakes) |
| 8 | リリースして満足して終わる | [CodeZine 18249](https://codezine.jp/article/detail/18249) |
| 9 | マーケティングの資料が物販や BtoB SaaS 向けばかりで、個人開発に合わない | [Zenn neko](https://zenn.dev/neko/articles/1fc06017d7e244) |

- **[事実]** 9つの別々の論点を確認。日本語の出典は 2・7・8・9 が中心で、Zenn の記事が多い。
- **[事実]** IH には「indie hackers はマーケティングをめったに好まず、できれば避けて作る方に逃げる」というコメントがある（検索要約から）。 — [IH: why do you hate marketing](https://www.indiehackers.com/post/why-do-you-hate-marketing-5d4d653d2a)
- **[事実]** 反対の見方もある。Heavybit は「開発者が嫌っているのはマーケティング全般ではなく広告とスパムだ」と書いている。 — [Heavybit](https://www.heavybit.com/library/article/developer-marketing-mistakes)
- **[推測]** 「宣伝が嫌い」の多くは「売り込みが嫌い」。役に立つ答えを書くことには抵抗が少ない。だから「質問に答える」形のほうが、作者が実際に続けられる見込みが高い。

### 1-4. 調べきれなかったこと
- **[事実]** X の「#個人開発 誰にも使われない」等の投稿は検索ツールで拾えなかった。note の記事もほとんど出てこなかった。日本語の不満の量は、Zenn の記事数からの推測にとどまる。
- **[事実]** Reddit（r/SideProject など）の個別投稿は取得が拒否されたため、件数は数えていない。

---

## 2. すでにあるもの

### 2-1. AI エージェント向けマーケティングスキル（GitHub、スター数は 2026-11-19 に `gh` で取得）

| リポジトリ | スター | 内容 | 足りない点 |
|---|---|---|---|
| coreyhaines31/marketingskills | 61,415 | 53 スキル。launch、directory-submissions（スタートアップ・SaaS・AI・MCP のディレクトリ）、analytics、attribution、community-marketing、prospecting、ai-seo、copywriting など。無料・MIT | 日本語や Qiita・Zenn の記述は見つからなかった（コード検索で0件）。「その問題を質問している人を探す」スキルはない |
| alirezarezvani/claude-skills | 30,123 | 410 スキルの総合集。マーケティングも含む | 汎用 |
| irinabuht12-oss/marketing-skills | 8,283 | 49 スキル。広告・SEO・AI での見つかりやすさなど | 広告寄り |
| nowork-studio/notfair-plugin | 4,263 | SEO・GEO | 検索流入向け |
| Jakeschincariol/founder-skill | 4,218 | ローンチ前に事業を試す 11 スキル | 検証寄り |
| ericosiu/ai-marketing-skills | 3,854 | 成長実験、アウトバウンド、SEO | 企業寄り |
| gooseworks-ai/goose-skills | 1,328 | 14 のマーケティングプレイブック、動画広告。旧 GTM ライブラリは 2026-10-23 に削除 | ブランド向け |
| emotixco/claude-skills-founder | 878 | 製品概要、競合、価格、GTM 計画 | 計画どまり |
| **AIDevGTM/gtm-cofounder** | **341**（skills.sh で 3.5K インストール） | **開発者ツールと AI 製品向け**。research-the-market（ユーザーがすでに話している場所と、知らない人が自分の言葉で問題を書いている投稿を探す。場所ごとの自己宣伝ルールも調べる）、09-first-50-users（「問題について投稿した人に個人的に DM」）、15-know-if-its-working（スターやページビューではなく継続率で測る）、10-launch-it。週次の GitHub Actions で traffic を記録 | **英語のみ**（README に日本語の記述なし）。戦略と計画が中心で、毎日「今日答えるべき質問」を出して返信を下書きし、結果を返信ごとに追う実行の部分は薄い |
| yoanbernabeu/producthunt-skills | 25 | Product Hunt ローンチ用 31 スキル | PH 専用 |
| mihir-kanzariya/community-engage | 5 | Reddit・X・PH・HN・IH・LinkedIn・Discord で `/engage-reddit` などを実行して返信。デスクトップ自動操作の MCP（OpenOwl）で投稿まで行う | 投稿まで自動化するため、HN や X の規則に触れる危険が高い（§4） |

出典: [marketingskills](https://github.com/coreyhaines31/marketingskills), [claude-skills](https://github.com/alirezarezvani/claude-skills), [irinabuht12-oss/marketing-skills](https://github.com/irinabuht12-oss/marketing-skills), [notfair-plugin](https://github.com/nowork-studio/notfair-plugin), [founder-skill](https://github.com/Jakeschincariol/founder-skill), [ai-marketing-skills](https://github.com/ericosiu/ai-marketing-skills), [goose-skills](https://github.com/gooseworks-ai/goose-skills), [claude-skills-founder](https://github.com/emotixco/claude-skills-founder), [gtm-cofounder](https://github.com/AIDevGTM/gtm-cofounder)（[METRICS.md](https://github.com/AIDevGTM/gtm-cofounder/blob/main/METRICS.md)）, [producthunt-skills](https://github.com/yoanbernabeu/producthunt-skills), [community-engage](https://github.com/mihir-kanzariya/community-engage)

- **[事実]** スキル市場のページには、Reddit の悩みを探して返信を下書きするスキル、Google 1ページ目に出る Reddit スレッドを探すスキル（RedditRank）、HN を Algolia API で探すスキル（hn-prospecting など）が複数載っている（検索要約から。各リポジトリの中身は確認していない）。 — [openskillindex: redditlens](https://openskillindex.com/skills/0xmassi-redditlens-redditlens), [openskillindex: hn-prospecting](https://openskillindex.com/skills/clawdbot-skills-hn-prospecting), [claudeskills.info: community-signals](https://claudeskills.info/skills/gooseworks-ai/goose-skills/community-signals/), [dev.to: Claude Code skill that finds customers on Reddit](https://dev.to/newan2001/i-built-a-claude-code-skill-that-finds-customers-not-competitors-on-reddit-linkedin-4h82)
- **[推測]** 英語圏では「スキル」の形でも、(a) の問題を探す機能はすでにある。作っても先行品との違いを出しにくい。

### 2-2. Reddit・X で見込み客を探すツール（ソーシャルリスニング）
- **[事実]** GummySearch（Reddit 調査、利用者約13〜14万人という二次情報）は、Reddit の Data API の商用ライセンスを得られず、2025年11月に新規受付を止めて閉鎖に向かった。 — [GummySearch is now closed](https://gummysearch.com/closing-time/), [Failory newsletter: When Reddit Pulls Over](https://newsletter.failory.com/p/when-reddit-pulls-over)
- **[事実]** Reddit は 2025年11月に「Responsible Builder Policy」を発表した。公開 API へのアクセスは事前承認制になり、自分で申し込んですぐ使う方式は閉じた（r/redditdev のスレッドのミラーから。公式文面は未確認）。 — [r/redditdev: Introducing the Responsible Builder Policy（ミラー）](https://r.datuan.dev/r/redditdev/comments/1oug31u/introducing_the_responsible_builder_policy_new/nobt04v)
- **[事実]** 後継・類似の SaaS が多数ある。RedLurk（Gemini で「困っている」兆候を検出し、人間らしい返信を下書き）、IntentLoom（購買意図を採点し返信を下書き）、LeadsFromURL（AI 返信案、カルマ稼ぎ機能）、Grabbit（「AI 返信も自動投稿もしない。それをやるツールはアカウントを BAN させる」と明言。人が全返信を承認）、Kunaii、ParseStream、LeadSynth（自称 MRR $500・250人以上）、ThreadMiner。 — [PH: RedLurk](https://www.producthunt.com/products/redlurk/reviews), [IntentLoom](https://similarlabs.com/p/intentloom), [IH: LeadsFromURL](https://www.indiehackers.com/post/from-manually-searching-reddit-to-automating-it-how-i-built-leadsfromurl-as-a-solo-founder-RMbfofpubJn8kaEKdyBc), [IH: Grabbit](https://www.indiehackers.com/product/grabbit), [IH: LeadSynth](https://www.indiehackers.com/post/leadsynth-stop-missing-customers-who-are-actively-searching-for-your-solution-863fd9bdad), [Peerlist: ThreadMiner](https://peerlist.io/abbasliumd/project/threadminer--ai-lead-finder-for-saas)
- **[事実]** IH には「Reddit で顧客を探すツールを作ったら、11か月後に100以上の競合に囲まれた」という題の投稿がある（本文は 403 で取得できず、題名のみ確認）。 — [IH: 11 months later I'm surrounded by 100 competitors](https://www.indiehackers.com/post/built-a-tool-to-find-customers-on-reddit-11-months-later-im-surrounded-by-100-competitors-f7f4400def)
- **[事実]** Leado のスレッドでは「難しいのは投稿を探すことより、宣伝っぽくない返信を書くこと」というコメントがある（検索要約から）。 — [IH: Leado](https://www.indiehackers.com/product/leado-co)
- **[事実]** OSS と MCP もある。ivucicev/redsignal（31スター、自前ホスト、AI で雑音を除いて返信下書き）、Ritik-bhaiya/reddit-research-skills（15スター、人が判断する前提）、Reddit Research MCP、mypracticaltools Reddit MCP（Apify 経由のリード監視）、Gorilla MCP（Reddit・X・YouTube・TikTok、2スター）。 — [redsignal](https://github.com/ivucicev/redsignal), [reddit-research-skills](https://github.com/Ritik-bhaiya/reddit-research-skills), [claudemarket: reddit-research-mcp](https://claudemarket.ai/mcp/king-of-the-grackles/reddit-research-mcp), [glama: Reddit MCP Server](https://glama.ai/mcp/servers/mypracticaltools/Reddit-MCP-Server/tools/reddit_lead_monitor), [Enterprise DNA: Gorilla MCP](https://enterprisedna.co/directories/mcp/opusforge-gorilla-mcp)
- **[事実]** キーワード通知: F5Bot は無料（Reddit・HN・Lobsters をメール通知）。Syften は月 $19.95〜$99.95 程度（出典で値段が違う。Reddit・HN・X・YouTube・PH）。Octolens は年払いで月 $159〜（HN・GitHub・Stack Overflow・DEV も対象。開発者ツール向けで、API・MCP が全プランに付く）。 — [getairefs: F5Bot alternatives](https://getairefs.com/blog/f5bot-alternatives-2026/), [getairefs: Syften alternatives](https://getairefs.com/blog/syften-alternatives-2026/), [Octolens pricing](https://octolens.com/pricing), [Octolens dev-monitoring](https://octolens.com/dev-monitoring)
- **[事実]** ReplyGuy は「Reddit で製品を宣伝する AI」をうたい、議論に製品を自然に混ぜ込む。Reddit の広報は 404 Media に「スパムまたはコンテンツ操作で規則違反」と答えた。紹介されたアカウントの大半は BAN された。 — [404 Media: AI is poisoning Reddit](https://www.404media.co/ai-is-poisoning-reddit-to-promote-products-and-game-google-with-parasite-seo/), [NewsBytes](https://www.newsbytesapp.com/news/science/reddit-flooded-with-spammy-products-thanks-to-ai/story), [PH: ReplyGuy](https://www.producthunt.com/posts/replyguy)

### 2-3. ディレクトリ登録・ローンチ・LP・SEO・X 予約投稿
- **[事実]** ディレクトリ一括登録: ListingBott は約100ディレクトリで $299（$499 からの割引表示、2026年10月時点）。SaaSCity は100件 $99、ListingSaaS は100件 $99。順位や流入は保証されない。 — [gappsy: ListingBott review](https://www.gappsy.com/tools/listingbott/), [SaaSCity: directory submission services compared](https://saascity.io/blog/directory-submission-services-compared-2026), [SoftwareSuggest: ListingSaaS](https://www.softwaresuggest.com/listingsaas)
- **[事実]** marketingskills の `directory-submissions` は MCP のディレクトリも対象にしている（無料）。 — [marketingskills](https://github.com/coreyhaines31/marketingskills)
- **[事実]** X の予約投稿: Typefully（無料〜月 $39 程度）、Hypefury（月 $19〜$65 程度）。値段は出典によって違う。 — [wearefounders: Hypefury vs Typefully 2026](https://www.wearefounders.uk/hypefury-vs-typefully-2026-which-x-tool-is-worth-paying-for/), [socialrails: Typefully pricing](https://socialrails.com/blog/typefully-pricing)
- **[事実]** LP の文章、SEO、Product Hunt ローンチは marketingskills（copywriting、programmatic-seo、launch）と producthunt-skills が無料で扱っている。 — 上記リポジトリ

### 2-4. OSS をどう広めるか
- **[事実]** zenika-open-source/promote-open-source-project（865スター、日本語版あり）は広め方のチェックリスト。道具ではない。 — [promote-open-source-project](https://github.com/zenika-open-source/promote-open-source-project)
- **[事実]** awesome リストに PR を出すエージェントスキルがある（関連する一覧を探して評価し、PR か Issue を下書き・提出する。中身は未確認）。 — [skillsmp: awesome-lists skill](https://skillsmp.com/skills/rustykuntz-clideck-skills-awesome-lists-skill-md)
- **[事実]** ただし awesome リスト側は閉じ始めている。sindresorhus/awesome-nodejs（67.6k スター）の説明文は「スパムと低品質な投稿が多すぎるため、投稿は一時停止」。awesome-electron、awesome-chatgpt も同様。 — [awesome-nodejs](https://github.com/sindresorhus/awesome-nodejs), [awesome-electron](https://github.com/sindresorhus/awesome-electron), [awesome-chatgpt](https://github.com/sindresorhus/awesome-chatgpt)
- **[事実]** 2026年11月5日の記事「Awesome リポジトリはもう awesome ではない」によると、1人が6つのバイブコーディング製サイトを宣伝するために100件以上の PR を複数の一覧に出した。awesome-javascript の管理者は、AI で低品質な PR が約4倍になったと HN で書いている。 — [Erik Gahner: awesome repositories are no longer awesome](https://erikgahner.github.io/posts/2026/awesome-repositories-are-no-longer-awesome/), [HN の議論](https://news.ycombinator.com/item?id=50377821), [zeli 要約](https://zeli.app/story/50377821)
- **[事実]** tldraw は AI 生成の低品質な PR の増加を理由に、外部からの PR を一時停止した。 — [AlternativeTo: tldraw pauses external contributions](https://alternativeto.net/news/2026/1/tldraw-pauses-external-contributions-citing-rise-in-low-quality-ai-code-and-pull-requests)

### 2-5. 日本語のもの
- **[事実]** GitHub を日本語と英語で探した範囲では、日本語の個人開発マーケティング用スキルは次の程度だった: magicalyellow2/marketingskills_jp（0スター）、ronantakizawa/japanese-copywriting（2スター、日本語コピー）、okazaky/copywriting-15-patterns-skill（0スター）、chloe-sy-park/humanize-ja（0スター、AI 文章を自然にする）、agarichan/note-skill（0スター、note 執筆〜投稿）。ほかは Zenn・Qiita・dev.to への同時投稿ツール（pipipi-dev/multi-platform-publisher 3スター など）。 — [marketingskills_jp](https://github.com/magicalyellow2/marketingskills_jp), [japanese-copywriting](https://github.com/ronantakizawa/japanese-copywriting), [humanize-ja](https://github.com/chloe-sy-park/humanize-ja), [note-skill](https://github.com/agarichan/note-skill), [multi-platform-publisher](https://github.com/pipipi-dev/multi-platform-publisher)
- **[事実]** 日本の作品紹介サイト: AI PICKS（個人開発者が作品を掲載でき、無料バッジあり）、Tsukutta（AI で作ったアプリの投稿サイト）。 — [AI PICKS ショーケース例](https://aipicks.jp/showcase/ontama-portfolio), [aipicks: Tsukutta](https://aipicks.jp/tool/tsukutta)
- **[事実]** 日本語のソーシャルリスニングは法人向けが中心。SocialDog は無料プランあり（X 1アカウント、上位は月 19,800円）、SignalHive は月 8,800円から（月1,000件まで検知）、Buzz Finder は月 80,000円から。 — [boxil: SocialDog](https://boxil.jp/service/8168/?categoryId=417), [aipicks: SignalHive](https://aipicks.jp/tool/signalhive), [ASPIC: Buzz Finder](https://www.aspicjapan.org/asu/service/10278)
- **[推測]** 「知恵袋・teratail・Qiita・Zenn・日本語の GitHub Issues から、自分の OSS が答えになる質問を探して返信を下書きする」道具は、日本語でも英語でも見つからなかった。ただし見つからない理由の一部は、その市場が小さいからだと思われる（§4-6）。

---

## 3. 空いているのはどこか

| 領域 | 英語圏 | 日本語圏 | 判定 |
|---|---|---|---|
| (a) 問題を抱えた人を探し、宣伝っぽくない返信を下書き | **飽和**。SaaS は100以上、OSS・スキル・MCP も多数（§2-2） | **見つからない**（§2-5） | 日本語なら空いている |
| (b) 日本語チャネル（Zenn・Qiita・note・はてブ・X・知恵袋・teratail） | — | 同時投稿ツールと文章スキルだけ。質問を探す道具はない | 空いているが、各チャネルの規則が厳しい（§4） |
| (c) SaaS ではなく OSS 開発者ツール | 戦略は gtm-cofounder、実行の一部（ディレクトリ・ローンチ）は marketingskills が無料で扱う。awesome リストは閉じ始めた | 日本語の OSS 向けはない | 日本語の実行部分だけ空いている |
| (d) 効いたかを測って改善 | gtm-cofounder が GitHub traffic を週次で記録し、継続率で測るよう指導。marketingskills に analytics・attribution | なし | 「どの返信・記事から何スター来たか」を1件ずつ結びつける部分は、どちらでも薄い |

- **[事実]** GitHub の REST API で、リポジトリの閲覧数・クローン数・参照元を取得できる。期間は過去14日分のみ。 — [GitHub Docs: REST API endpoints for repository traffic](https://docs.github.com/en/rest/metrics/traffic)
- **[推測]** (d) を (a) とつなぐ（「この返信を出した → 参照元に teratail が出た → スターが1増えた」と記録する）部分は、どの先行品も正面から扱っていない。ただし 14 日で消えるので、自分で記録を残す必要がある。
- **[推測]** 新しいチャネルとして「AI エージェントに見つけてもらう」もある（MCP レジストリ、skills.sh、Claude プラグインマーケット）。masume は AI エージェント向けの道具なので、人の Q&A より効く可能性がある。ただし marketingskills の `directory-submissions` と `ai-seo` がすでに一部を扱っている。

---

## 4. 危険

### 4-1. プラットフォームの規則（確認できたもの）
- **Hacker News [事実]** 公式ガイドラインに「生成した文章や AI が手を入れた文章を投稿しない。HN は人間同士の会話の場」とある。投稿についても「自動で投稿しない」。宣伝は「主な目的にしない」「自分のものを出すのはときどきなら可」。 — [HN Guidelines](https://news.ycombinator.com/newsguidelines.html)
  - **[推測]** HN では AI の下書きをそのまま使えない。道具ができるのは「探す」と「要点を示す」までで、文章は人が書く必要がある。
- **X [事実]** 自動化ルールで「キーワード検索だけを根拠に自動返信を送ることは不可」。大量で攻撃的な、頼まれていない返信・メンションも不可（検索結果の要約から。help.x.com 本体は 403）。 — [X Automation rules](https://help.x.com/en/rules-and-policies/x-automation), [X Developer Policy](https://docs.x.com/developer-guidelines)
- **Reddit [事実]** 「自己宣伝は活動の10%まで」は公式の規則ではなく慣習で、サブレディットの規則のほうが厳しい。AI 生成コンテンツの扱いもサブレディットごとに違う（Cornell・NYU の研究）。2025年11月から API は事前承認制（§2-2）。ReplyGuy のアカウントは BAN された（§2-2）。 — [redship: Reddit self-promotion rules](https://redship.io/blog/reddit-self-promotion-rules), [arXiv 2410.11698 AI Rules? Reddit community policies](https://arxiv.org/abs/2410.11698)
- **Zenn [事実]** ガイドライン: 「製品や採用の宣伝が主目的の投稿は避けてください」。宣伝は記事末尾の固定メッセージ程度が望ましい。生成 AI の利用は禁止していないが、正確さを確かめずに投稿すること、フォロワーやスコアのために記事を乱造することは避ける。 — [Zenn ガイドライン](https://zenn.dev/guideline)
  - **[推測]** 「masume の紹介記事」ではなく「方眼紙に AI で書き込むと何が壊れるか」という技術記事に仕立て、末尾で触れる形なら規則に沿う。
- **Qiita [事実]** 公式のコミュニティガイドラインの本文は取得できなかった。2019年に「プログラミングと関係ない記事」と判断されて限定公開にされた体験談がある。 — [Zenn: Qiita で限定公開にされた体験](https://zenn.dev/yumainaura/articles/qiita-2019-05-13t08_20_44-09_00-)
- **Yahoo!知恵袋 [事実]** 利用ルールのページでは、違反すると投稿削除・一時利用停止・利用停止がありうる。鳥取県の削除申出マニュアルには、通報理由として「商用・宣伝目的の投稿」が載っている。宣伝を禁じる具体的な条文は取得できなかった。 — [知恵袋 利用ルール違反への対応](https://support.yahoo-net.jp/PccChiebukuro/s/article/H000008115), [鳥取県 削除申出マニュアル（Yahoo!）](https://www.pref.tottori.lg.jp/secure/1415810/sakujyomanyual_yahoo.pdf), [総務省資料（ヤフー）](https://www.soumu.go.jp/main_content/000734922.pdf)
  - **[推測]** 知恵袋は「読んで需要を確かめる」だけに使い、自分の道具へのリンク付き回答はしないのが安全。
- **Stack Overflow [事実]** 自分の製品に触れるなら所属の開示が必須。関連する良い回答の一部が自分の製品なら可。だが投稿の多くが自分の製品の話だとスパム扱い。「解決できる」と言うだけでなく解決方法を示すこと。 — [Stack Overflow Help: promotion（Teams 版の同文）](https://stackoverflowteams.com/help/promotion)
- **ステマ規制 [事実]** 2023年10月1日から、事業者の広告と分からない表示（第三者に頼んだ投稿を含む）は景品表示法の不当表示。規制対象は広告主の事業者。 — [ECのミカタ: ステマ規制開始](https://ecnomikata.com/ecnews/40259/), [NRI 用語解説](https://www.nri.com/jp/knowledge/glossary/stealth_marketing.html)
  - **[推測]** 無料の個人 OSS の作者が自分で答えるのは「事業者の広告」に当たりにくい。ただ、有料化した場合や他人に投稿を頼む機能を付けた場合は問題になる。どちらにしても「作者です」と書くのが安全。

### 4-2. 「AI が書いた宣伝」は嫌われるか
- **[事実]** HN は AI コメントを禁じた（上記）。awesome リストや OSS の PR は AI スロップで閉じ始めた（§2-4）。ReplyGuy の返信は「ほとんどの人は AI だと分かる」と PH で言われた。 — [PH: ReplyGuy](https://www.producthunt.com/posts/replyguy)
- **[事実]** CodeZine の記事では、書き手と読み手のコストが逆転し、読み手を考えない「AI スロップ」が量産されていると取り上げている。 — [CodeZine 29652](https://codezine.jp/article/detail/29652)
- **[推測]** 「AI がマーケティングを肩代わり」と打ち出すと、それ自体が嫌われる理由になる。打ち出し方は「あなたの道具が本当に役立つ質問だけを探し、あなたが自分で答える」にすべき。

### 4-3. 倫理的で効く形
1. **投稿は必ず人が手でする。** 道具は投稿 API を持たない（HN・X の自動化規則にも当たらない）。
2. **「その道具が答えそのもの」の質問だけを選ぶ。** 道具を使わなくても質問に答え切る。リンクは最後に1つ、「作者です」と書く。
3. **チャネルごとの規則表を内蔵する。** HN は AI 文章不可なので下書きを出さず要点だけ。知恵袋は読むだけ。Zenn は技術記事として書き、宣伝は末尾に。
4. **量を制限する。** 1日数件まで。同じ文面を使い回さない。
5. **見つからないことも結果として扱う。** 「答えるべき質問が1か月に0件」なら、宣伝ではなく需要の問題だと伝える（Failory の PMF の指摘に対応）。
6. **結果を記録する。** 返信の URL、日付、反応（いいね・ベストアンサー・返信）、その後14日の参照元とスターを残す。

### 4-4. 市場そのものの危険
- **[推測]** 先行品（marketingskills、gtm-cofounder）が日本語に対応すれば、空きはすぐ埋まる。差別化できるのは日本語チャネルの規則と探し方の知識だけで、守りは薄い。
- **[推測]** 個人開発者はお金を払わない（Perspective.ai の「お金がない」と同じ）。製品として売るより、無料の OSS スキル＋Zenn 記事（それ自体が自分の実績になる）が現実的。

### 4-5. 自分の2つの道具にとっての危険
- **[推測]** kanjiframe の利用者（メインフレームの日本語データを扱う技術者）は少なく、公開の場で質問しにくい（社内データ・社内ネットワーク）。EBCDIC の日本語の文字化けを検索しても、teratail・知恵袋・Stack Overflow の質問は1回の検索では出てこなかった。出てきたのは IBM、HULFT、TmaxSoft の文書だった。 — [IBM Support](https://www.ibm.com/support/pages/node/6510042), [HULFT ASCII/EBCDIC 変換](https://www.hulft.com/help/en-us/HULFT-V8/COM-CNV/Content/HULFT_CNV/outline/ASCII_EBCDIC_Cnv.htm), [TmaxSoft: EBCDIC→ASCII conversion issues](https://docs.tmaxsoft.com/en/openframe_common/MVS_7.1/migration-guide/appendix-ebcdic-to-ascii-conversion-Issues-mvs.html)
- **[事実]** PyPI の `ebcdic` パッケージは cp290 などを提供するが、日本語の2バイト部分は対象外と説明されている（検索要約から）。 — [PyPI: ebcdic](https://pypi.python.org/pypi/ebcdic)
  - **[推測]** つまり kanjiframe の「答えになる場所」は質問サイトより、Python で cp930/cp939 を扱う GitHub Issues や、AWS の EBCDIC 変換ガイドのような既存資料の周辺にありそう。 — [AWS Prescriptive Guidance: EBCDIC を Python で変換](https://docs.aws.amazon.com/zh_tw/prescriptive-guidance/latest/patterns/convert-and-unpack-ebcdic-data-to-ascii-on-aws-by-using-python.html)
- **[事実]** 方眼紙の結合セルを openpyxl で扱う難しさは Zenn に書かれている。 — [Zenn: openpyxl で方眼紙を HTML に変換](https://zenn.dev/collabostyle/articles/d6e32c3d96b2ec)

### 4-6. 質問サイトが細っている
- **[事実]** Stack Overflow の質問数はピークから約70%減り、2025年5月に2009年初めの水準まで落ちた。2025年12月は 6,866 件という報道もある。最も急に減ったのは ChatGPT 公開後。 — [Pragmatic Engineer: Stack Overflow is almost dead](https://blog.pragmaticengineer.com/stack-overflow-is-almost-dead), [dbreunig: StackOverflow's decline](https://www.dbreunig.com/2025/05/16/stackoverflow-s-decline.html), [lavx: question volume plummets](https://news.lavx.hu/article/stack-overflow-s-paradox-question-volume-plummets-to-2008-levels-while-revenue-doubles-post-chatgpt)
- **[推測]** 困っている人は公開の場で聞かず AI に聞く。そうなると (a) の「質問を探す」は年々効きにくくなる。AI エージェントに見つけてもらう（MCP レジストリ、skills.sh、README の書き方）と組み合わせるべき。

---

## 5. 実際の道具で試せるか（masume・kanjiframe）

### 5-1. 出発点（2026-11-19 に `gh api` で確認）
- **[事実]** yukijames25/masume: スター0、フォーク0、閲覧0、クローン0、参照元なし。topics は ai-agents・claude-code・excel・mcp など8つ。PyPI には未公開。 — [masume](https://github.com/yukijames25/masume)
- **[事実]** yukijames25/kanjiframe: スター0、閲覧0、クローン0、topics なし。PyPI には未公開。 — [kanjiframe](https://github.com/yukijames25/kanjiframe)
- **[事実]** 2つとも今日作られたリポジトリ。masume には Zenn 記事がすでにある。なお 2026-11-19 にユーザーは「masume はポートフォリオとして置き、宣伝はしない」と決めている（プロジェクトメモより）。試すかどうかは改めて決める必要がある。

### 5-2. 作る前の手作業テスト（2週間、推奨）
道具を作らず、Claude Code で同じことを手で行う。

| 週 | やること | 記録すること |
|---|---|---|
| 0日目 | 下準備。kanjiframe に topics を付ける。2つとも PyPI に公開（インストール数を測るため）。MCP レジストリ・skills.sh に登録（masume）。`gh api .../traffic` の値を毎日保存する仕組みを作る（14日で消えるため） | 出発点の数字 |
| 1〜2週 | 毎日15分。日本語の質問・Issue・記事を探す。masume は「方眼紙 AI 入力」「openpyxl 結合セル 書き込み」「Excel 申請書 Claude」など。kanjiframe は「cp930 Python」「EBCDIC 漢字 変換」「COBOL コピー句 Python」など。英語の GitHub Issues も対象 | 見つかった候補数、そのうち「この道具がまさに答え」と人が判断した数（適合率） |
| 1〜2週 | 適合したものにだけ、道具なしでも成り立つ答えを手で書き、末尾に「作者です」とリンク | 返信数、反応（いいね・ベストアンサー・返事）、削除・警告の有無 |
| 2週の終わり | 参照元（`traffic/popular/referrers`）で teratail・qiita・zenn・github.com が出たか。スター・クローン・PyPI インストール（pypistats）・知らない人からの Issue | 返信1件あたりの訪問者、スター、インストール |

### 5-3. 成功・失敗の基準（案、[推測]）
- **続ける:** 2週間で、2つ合わせて「まさに答えになる」質問が 5件以上見つかり、そのうち1件以上から知らない人の訪問（参照元）かスター・Issue が来る。
- **形を変える:** 質問は見つかるが反応がない → 質問サイトより、AI エージェント経由（MCP レジストリ、README、skills.sh）と技術記事に力を移す。
- **やめる:** 2週間で、適合する質問がほぼ0件 → 「探して答える」型は、日本語の小さな OSS には効かない。宣伝ではなく需要の問題。この結果自体を Zenn 記事にできる。
- **[推測]** 比べる相手として、1回だけの施策（Zenn 記事、MCP レジストリ登録、PyPI 公開）の参照元も同じ期間に記録しておく。そうすれば「返信の効果」と「一度きりの掲載の効果」を分けられる。

### 5-4. 数週間で測れる数字
- 見つけた候補の数、適合率（人が「答えになる」と判断した割合）
- 投稿した返信数、反応、削除や警告の件数（0件であるべき）
- GitHub: ユニーク訪問者、参照元ごとの訪問、クローン、スター、知らない人の Issue・PR
- PyPI: 1週間あたりのダウンロード数（公開後。ボットや CI を含むので参考値）
- skills.sh や MCP レジストリのインストール数（masume）
- **最終的な指標:** 知らない人が実際に使ったという証拠（Issue、質問、「使えた」の返事）。スターは参考程度（gtm-cofounder も「スターやページビューは見栄えの数字」としている）

---

## 6. 判定

**今は作らない。** 2週間の手作業テスト（§5）を通過した場合にだけ、下の狭い形で作る。
理由: 痛み C（今回の狭い形）を求める不満も、自分で作った回避策も見つからなかった。いちばん近い当事者であるユーザー自身も宣伝しないと決めた（§0）。広い痛み A は強いが、英語圏は埋まっていて、原因の多くは道具では治らない。

**テストを通過する条件（両方必要）:**
1. 2つの OSS で「まさに答えになる」日本語の質問・Issue が2週間で5件以上ある。
2. ユーザー自身が、2週間たっても毎日15分の作業を続けたいと思っている（続けたくないなら、道具にしても使わない）。

- **作らないもの:** 英語の Reddit・X のリード探し（競合100以上、API 規制あり）。自動投稿（HN・X の規則違反、BAN、評判の悪化）。「AI がマーケティングを全部やる」総合スキル（marketingskills 61k スターが無料で配っている）。
- **いちばん狭い、まだ空いている形:**
  **「日本語の個人開発 OSS の作者向け Claude Code スキル。自分の道具が直接の答えになる日本語の質問・Issue・記事を探し、チャネルごとの規則に沿った開示付きの返信を1件ずつ下書きする（HN では要点だけ、知恵袋は読むだけ）。投稿は人が手でする。GitHub traffic と PyPI の数字を毎日保存し、どの返信が訪問とスターにつながったかを記録する。質問が見つからなければ『需要が見えない』と伝える」**
- **空いている理由 [推測]:** 英語の先行品は日本語のチャネルと規則を扱わない。日本語の先行品は文章作成と同時投稿だけ。どちらも、返信1件ごとに効果を測っていない。
- **空きが続かない理由 [推測]:** 先行品が日本語に対応すれば埋まる。市場は小さく、お金を払う人も少ない。だから**売る製品ではなく、自分の2つの OSS で効果を示す無料のスキルと記事**として作るのが妥当。結果がよければ、その記録自体がいちばんの宣伝になる。
