# ADR-OPS-010: ブラウザの中で自動で確かめる手段は、npm を使わない自前の薄い層にする

| 項目 | 内容 |
|---|---|
| 状態 | 採用・未実装 |
| 決定日 | 2026-11-15 |

---

## Context

[ADR-OPS-007](ADR-OPS-007-automated-or-manual-by-who-judges.md) は、ブラウザの中の値（表示する要素と文字、ブラウザに保存した値、ダウンロードしたファイル、通信の記録、Canvas の画素の値、応答時間やフレーム時間の実測）をコードで読み、仕様から導いた期待値と照合できるケースを自動とした。そのため、テストのコードが対象環境のブラウザで画面を動かして値を読む手段が要る。ADR-OPS-007 の Decision 6 は、ブラウザを動かす道具を方針書でも ADR-OPS-007 でも名指しせず、[#299](https://github.com/jj1xgo/findsummits/issues/299)「ブラウザの中で自動で確かめる手段を決める」で決めるとしていた。

2026-11-15 に、詳細設計書の 9.2（`index.html` の画面の要素）を書く前にこれを決めることにした。画面の要素の関数（概要設計書 3.7.3・3.8.3 の「置き場」が「画面」の 28 個）は DOM・地図・localStorage に触れ、単体テストを回す手段が無いと、その単体テストも、仕様だけから実装とテストを書かせる試し書きも回せないため。

- 対象のブラウザは、Chrome・Firefox・Safari・Brave の安定版の最新で、デスクトップの版（概要設計書の [DEC130](../30_HLD.md#4134-設計判断)「JavaScript はモジュールを使わない ES2020」）。テスト方針書 3.1 は、画面の自動のケースを対象環境のブラウザで行うとしている。
- 道具が要る能力は 9 つ: `file://` で開く、通信の記録と応答・失敗の注入、Canvas の画素を読む、ファイル選択に渡す、ダウンロードの中身を取る、2 つのタブで localStorage と `storage` イベントを共有する、フレーム間隔の実測を読む、メモリの値を読む（補助の値）、実際の入力を送る。
- 計算の要素の単体テストは、Node.js に同梱の `node:test` で回していて、ほかのパッケージが要らない（概要設計書の [DEC131](../30_HLD.md#4134-設計判断)「バイト列の処理は名前付き script 要素に置く」）。リポジトリに npm の依存は無い。

確かめの記録は [`research/browser-automation-probe.md`](research/browser-automation-probe.md)。Chrome 157・Brave 157・Firefox 160.0 で、9 つの能力がどれも通った。ただし、能力 7 で確かめたのは操作の無いときのフレーム間隔を読むことまでで、能力 8 で読んだのはタブのメモリでなく補助の値（Decision 2）である。システムテストの `ST-NFR-008-01` の応答時間と `ST-NFR-010-01` の入力の処理時間・画面が変わるまでの時間は確かめていない（Decision 7）。

## Decision

1. **道具**: テストのコードは、Chrome・Brave を Chrome DevTools Protocol で、Firefox を WebDriver BiDi で動かす自前の薄い層を使う。層は Node.js の組み込みの `fetch` と `WebSocket` で話し、npm のパッケージとブラウザのドライバ（chromedriver・geckodriver）を使わない。テストの枠組みは `node:test` のまま。ADR-OPS-007 の Decision 6 が #299 に送った道具の決定を、本 ADR で行う。道具の名前はテスト方針書 §4 に書く。
2. **読み方**: 時間とメモリの測り方は、概要設計書とシステムテスト仕様書の定義のままとし、本 ADR では変えない。フレーム時間と内訳は 5.10.2 の 3「測り方」・4「内訳の測り方」（開発者ツールのパフォーマンス計測）、単発の操作の時間は 5.8.2 の 5「測り方」、タブのメモリは 5.2.2 の 4「測り方」（処理の始まりから終わりまでのタブのメモリの最大を、ブラウザのタスクマネージャで測る。道具の細かい使い方は ST の手順で決める）と、それぞれの ST のケース（`ST-NFR-010-01`・`ST-NFR-008-01`・`ST-NFR-002-02`）による。層で同じ値を読めるか（Chrome DevTools Protocol の `Tracing` などで開発者ツールの計測と同じ値を取れるか。WebDriver BiDi には相当する命令が無い）は確かめていない（Decision 7）。タブのメモリは記録だけの値なので、人が読んで記録してよい（テスト方針書 3.1）。層で読めると確かめた値（ページの中の `performance.now()` と `requestAnimationFrame` で測ったフレーム間隔、Chrome・Brave の `Performance.getMetrics` の `JSHeapUsedSize`、起動したプロセスのグループの RSS の和）は補助の値で、正式な値にしない（rAF の間隔はメインスレッドから見たフレームの間隔で、合成を含む計測とは対象が違う。RSS の和はブラウザ全体で、共有のページを重ねて数える）。実際の入力は、Chrome・Brave は `Input.dispatchMouseEvent`、Firefox は `input.performActions` で送る。
3. **どこで回すか**: push・プルリクエストの CI では Chrome と Firefox で回す（GitHub Actions の Ubuntu のランナーにある）。手元では、入っているもの（Chrome・Brave・Firefox）で回す。Firefox は安定版を対象の版とする。Safari は Mac で人が補う。
4. **ブラウザが無いとき**: 実行ファイルが見つからないブラウザのケース（見つかるかは起動の前に確かめる）は、not run と明示して飛ばし、テストの実行は失敗にしない（ブラウザの無いコンテナと、CI の Brave のため）。見つかったのに起動・接続に失敗したら、テストの失敗にする（起動の失敗が not run に紛れないため）。CI では Chrome と Firefox が無ければ失敗にする。走らせたブラウザの版とチャンネルを出力に出す（Firefox の WebDriver BiDi の `browserVersion` は ESR でも `esr` を含まない〈153.5.1 ESR で `153.5.1`〉ので、チャンネルは `firefox --version` の出力〈ESR なら `153.5.1esr`〉で見分ける）。正式な実行で飛ばした組み合わせと、ESR の Firefox で回した結果は、テスト方針書 5.4 の未実施として記録する（ESR は安定版で再実施する）。
5. **人が補う操作（Safari）**: 手順書のとおり人が画面を操作し、手順書の読み取りの文を開発者ツールのコンソールで実行して値の JSON を保存する。読み取りの文は JSON に `navigator.userAgent` を含め、テストのコードは Safari とその版であることを照らしてから、JSON を期待と照合する（ADR-OPS-007 の Decision 2 の「手順の一部を人が行うこと」）。照合のケースには Safari の組み合わせも並べ、JSON が無ければ not run と出す。正式な実行で Safari を補わなかった組み合わせは、テスト方針書 5.4 の未実施として記録する。読み取りの文で読めない記録だけの値（タブのメモリ）は、本 ADR の Decision 2 のとおり人が読んで記録する。どのテストのレベル（単体・結合・システム）とどの機会に Safari を補うかは、詳細設計書の 9.2 と、結合テスト・システムテストの仕様書で決める。
6. **プロセスの扱い**: 層はブラウザを毎回新しいプロファイルで、プロセスのグループとして起動し、終わりにグループごと止める（Brave の起動のコマンドはラッパーで、子のプロセスへの `kill` が本体に届かなかった）。例外・時間切れ（全体と 1 つの命令ごと）・中断のシグナルのときもグループを止め、止まったことを確かめる（SIGTERM で止まらなければ SIGKILL）。接続先は、起動したブラウザ自身が知らせるもの（Chrome・Brave はそのプロファイルの `DevToolsActivePort`、Firefox は標準エラー出力の `WebDriver BiDi listening on` の行。どちらもポート 0 で起動）から取り、ほかのブラウザにつながない。
7. **決めないこと**: 層の置き場とファイル名、ブラウザのコマンド名と差し替えの方法、CI で「無ければ失敗」にする印、not run の出し方は、詳細設計書の 9.2 で決める。CI へのつなぎ込み（`make test` の段、Node.js 24 の指定）と `make test` のターゲットは、実装の段で行う。ヘッドありで起動するか、https の配信先を開くこと、開発者ツールの計測と同じ時間の値（`ST-NFR-010-01` のフレーム時間・内訳・入力の処理時間・画面が変わるまでの時間と、`ST-NFR-008-01` の操作から画面が変わるまで・ダウンロードの開始までの時間）を層で読めるか、`ST-NFR-002-02` のタブが落ちたことを層で知れるかは確かめていないので、結合テストとシステムテストのテストのコードを書くときに確かめる。

## Alternatives

- **Playwright**: 公式文書（<https://playwright.dev/docs/browsers>）に「Playwright doesn't work with the branded version of Firefox since it relies on patches.」「Playwright doesn't work with the branded version of Safari since it relies on patches.」とある。実物の Firefox・Safari を動かせず、テスト方針書 3.1 の「対象環境のブラウザで行う」を満たさないので外した。
- **WebdriverIO（W3C WebDriver の道具）**: Chrome・Brave・Firefox で、能力 1〜6 は自前と同じく通った（2026-11-15）。Mac では safaridriver で Safari を動かせる見込みがある。ただし、入れると 140 個のパッケージが入り、npm 12 が geckodriver・edgedriver の install script を止め、ドライバを実行のときにネットから取る。リポジトリに初めて npm の依存と lockfile を入れ、その更新を保守することになる。jj1xgo が不採用とした（2026-11-15）。
- **すべて手動**: ADR-OPS-007 の Decision 1 の定義に反する（合否をコードが判定できるケースを手動にする）。不採用。

## Consequences

- 2 つのプロトコルの層を自分たちで保守する。Chrome DevTools Protocol はブラウザの版で変わりうるので、版を上げたときは調査の記録の「やり直すとき」の手順で確かめ直す。WebDriver BiDi は W3C の標準。
- CI では Brave を回さない。Brave の結果は手元の実行で取る。
- Safari は人が補う。safaridriver で自動にできるかは、[#338](https://github.com/jj1xgo/findsummits/issues/338)「Safari（Mac）で #197 の確かめ用のページを測る」の機会に確かめる。
- Firefox は安定版（160.0）で確かめた。ESR（153.5.1）では、決める前の試しで能力 1〜6 だけを確かめた。
- ブラウザを起動するので、`make test` の時間が延びる。
- 結合テスト仕様書には、開発者ツールで要求や応答を照合するのに `（手動）` の付いたケース（`IT-CMP7-EXT3-01` など）が残っている。その判定し直し（[#300](https://github.com/jj1xgo/findsummits/issues/300)「IT の手動のケースを、自動と手動の新しい分け方で判定し直す」）は、本 ADR の層を前提に行う。
- ブラウザの無い環境（コンテナなど）では、画面のテストはすべて not run になる。そこで単体テストや試し書きを回すかは、詳細設計書の 9.2 を書くときに決める。
- テスト方針書 §4、環境定義の「開発環境」、概要設計書 3.7.3 の「画面」の段落、システムテスト仕様書の「ブラウザの中で確かめるケース」と「ブラウザの測定」の段落を、本 ADR に合わせて直した。ADR-OPS-007 の Consequences に、本 ADR で決めたことを追記した。
