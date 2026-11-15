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
- 道具が要る能力は 9 つ: `file://` で開く、通信の記録と応答・失敗の注入、Canvas の画素を読む、ファイル選択に渡す、ダウンロードの中身を取る、2 つのタブで localStorage と `storage` イベントを共有する、応答時間とフレーム時間の実測を読む、タブのメモリを読む、実際の入力を送る。
- 計算の要素の単体テストは、Node.js に同梱の `node:test` で回していて、ほかのパッケージが要らない（概要設計書の [DEC131](../30_HLD.md#4134-設計判断)「バイト列の処理は名前付き script 要素に置く」）。リポジトリに npm の依存は無い。

確かめの記録は [`research/browser-automation-probe.md`](research/browser-automation-probe.md)。Chrome 157・Brave 157・Firefox 160.0 で、9 つの能力がどれも通った。ただし、能力 7 で確かめたのは操作の無いときのフレーム間隔を読むことまでで、システムテストの `ST-NFR-010-01` が求める入力の処理時間と画面が変わるまでの時間は確かめていない（Decision 7）。

## Decision

1. **道具**: テストのコードは、Chrome・Brave を Chrome DevTools Protocol で、Firefox を WebDriver BiDi で動かす自前の薄い層を使う。層は Node.js の組み込みの `fetch` と `WebSocket` で話し、npm のパッケージとブラウザのドライバ（chromedriver・geckodriver）を使わない。テストの枠組みは `node:test` のまま。ADR-OPS-007 の Decision 6 が #299 に送った道具の決定を、本 ADR で行う。道具の名前はテスト方針書 §4 に書く。
2. **読み方**: フレーム時間は、ページの中の `performance.now()` と `requestAnimationFrame` で測った値を読む。実際の入力は、Chrome・Brave は `Input.dispatchMouseEvent`、Firefox は `input.performActions` で送る。タブのメモリは、概要設計書の 5.2.2 の 4「測り方」と `ST-NFR-002-02` の定義（処理の始まりから終わりまでのタブのメモリの最大を、ブラウザのタスクマネージャで測る）のままとし、本 ADR では変えない。記録だけの値なので、どのブラウザでも人がタスクマネージャ（Safari は OS の道具）で読んで記録してよい（テスト方針書 3.1）。層で読める値（Chrome・Brave の Chrome DevTools Protocol の `Performance.getMetrics` の `JSHeapUsedSize` と、起動したプロセスのグループの RSS の和）は、タブのメモリとは測る対象が違う（RSS の和はブラウザ全体で、共有のページを重ねて数える）ので、正式な値にしない。
3. **どこで回すか**: push・プルリクエストの CI では Chrome と Firefox で回す（GitHub Actions の Ubuntu のランナーにある）。手元では、入っているもの（Chrome・Brave・Firefox）で回す。Firefox は安定版を対象の版とする。Safari は持ち主の Mac で人が補う。
4. **ブラウザが無いとき**: 実行ファイルが見つからないブラウザのケースは、not run と明示して飛ばし、テストの実行は失敗にしない（ブラウザの無いコンテナと、CI の Brave のため）。見つかったのに起動・接続に失敗したら、テストの失敗にする（起動の失敗が not run に紛れないため）。CI では Chrome と Firefox が無ければ失敗にする。走らせたブラウザの版とチャンネルを出力に出す。正式な実行で飛ばした組み合わせと、ESR の Firefox で回した結果は、テスト方針書 5.4 の未実施として記録する（ESR は安定版で再実施する）。
5. **人が補う操作（Safari）**: 手順書のとおり人が画面を操作し、手順書の読み取りの文を開発者ツールのコンソールで実行して値の JSON を保存する。テストのコードがその JSON を期待と照合する（ADR-OPS-007 の Decision 2 の「手順の一部を人が行うこと」）。読み取りの文で読めない記録だけの値（タブのメモリ）は、Decision 2 のとおり人が読んで記録する。
6. **プロセスの扱い**: 層はブラウザを毎回新しいプロファイルで、プロセスのグループとして起動し、終わりにグループごと止める（Brave の起動のコマンドはラッパーで、子のプロセスへの `kill` が本体に届かなかった）。
7. **決めないこと**: 層の置き場とファイル名、ブラウザのコマンド名と差し替えの方法、CI で「無ければ失敗」にする印、not run の出し方は、詳細設計書の 9.2 で決める。CI へのつなぎ込み（`make test` の段、Node.js 24 の指定）と `make test` のターゲットは、実装の段で行う。ヘッドありで起動するか、https の配信先を開くこと、入力の処理時間と画面が変わるまでの時間（`ST-NFR-010-01`。入力と測りを結んだ値）を層で読めるかは確かめていないので、結合テストとシステムテストのテストのコードを書くときに確かめる。

## Alternatives

- **Playwright**: 公式文書（<https://playwright.dev/docs/browsers>）に「Playwright doesn't work with the branded version of Firefox since it relies on patches.」「Playwright doesn't work with the branded version of Safari since it relies on patches.」とある。実物の Firefox・Safari を動かせず、テスト方針書 3.1 の「対象環境のブラウザで行う」を満たさないので外した。
- **WebdriverIO（W3C WebDriver の道具）**: Chrome・Brave・Firefox で、能力 1〜6 は自前と同じく通った（2026-11-15）。Mac では safaridriver で Safari を動かせる見込みがある。ただし、入れると 140 個のパッケージが入り、npm 12 が geckodriver・edgedriver の install script を止め、ドライバを実行のときにネットから取る。リポジトリに初めて npm の依存と lockfile を入れ、その更新を保守することになる。持ち主が不採用とした（2026-11-15）。
- **すべて手動**: ADR-OPS-007 の Decision 1 の定義に反する（合否をコードが判定できるケースを手動にする）。不採用。

## Consequences

- 2 つのプロトコルの層を自分たちで保守する。Chrome DevTools Protocol はブラウザの版で変わりうるので、版を上げたときは調査の記録の「やり直すとき」の手順で確かめ直す。WebDriver BiDi は W3C の標準。
- CI では Brave を回さない。Brave の結果は手元の実行で取る。
- Safari は人が補う。safaridriver で自動にできるかは、[#338](https://github.com/jj1xgo/findsummits/issues/338)「Safari（持ち主の Mac）で #197 の確かめ用のページを測る」の機会に確かめる。
- Firefox は安定版（160.0）で確かめた。ESR（153.5.1）では、決める前の試しで能力 1〜6 だけを確かめた。
- ブラウザを起動するので、`make test` の時間が延びる。
- 結合テスト仕様書には、開発者ツールで要求や応答を照合するのに `（手動）` の付いたケース（`IT-CMP7-EXT3-01` など）が残っている。その判定し直し（[#300](https://github.com/jj1xgo/findsummits/issues/300)「IT の手動のケースを、自動と手動の新しい分け方で判定し直す」）は、本 ADR の層を前提に行う。
- ブラウザの無い環境（コンテナなど）では、画面のテストはすべて not run になる。そこで単体テストや試し書きを回すかは、詳細設計書の 9.2 を書くときに決める。
- テスト方針書 §4、環境定義の「開発環境」、概要設計書 3.7.3 の「画面」の段落、システムテスト仕様書の「ブラウザの中で確かめるケース」と「ブラウザの測定」の段落を、本 ADR に合わせて直した。ADR-OPS-007 の Consequences に、本 ADR で決めたことを追記した。
