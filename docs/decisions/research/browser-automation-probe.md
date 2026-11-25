# ブラウザの中で自動で確かめる手段の確かめ（#299）

[#299](https://github.com/jj1xgo/findsummits/issues/299)「ブラウザの中で自動で確かめる手段を決める」の確かめの記録。決定は [ADR-OPS-010](../ADR-OPS-010-browser-automation-without-npm.md)。ブラウザの版を上げたときに同じ確かめをやり直せるよう、道具を `browser-automation-probe/` に置く。

確かめた日: 2026-11-15。場所: Linux のホスト（Debian testing、x86_64）。どのブラウザもヘッドレスで、毎回新しいプロファイルで起動した。

## 道具

| ファイル | 役目 |
|---|---|
| `browser-automation-probe/probe.html` | 道具が `file://` で開くページ。ダウンロードのボタン、ファイルの選択、`storage` イベントの控え、4×4 の Canvas、入力の受け口、フレーム時間の測り方、`https://probe.invalid/` への `fetch` を持つ |
| `browser-automation-probe/upload.json` | ファイルの選択に渡すファイル |
| `browser-automation-probe/cdp_probe.js` | Chrome・Brave をヘッドレスで起動し、Chrome DevTools Protocol で 9 つの能力を確かめる |
| `browser-automation-probe/bidi_probe.js` | Firefox をヘッドレスで起動し、WebDriver BiDi で 9 つの能力を確かめる |

どちらの道具も、Node.js の組み込みの `fetch` と `WebSocket` だけを使う（npm のパッケージも、chromedriver・geckodriver も使わない）。ブラウザはプロセスのグループで起動し、終わりにグループごと止める。

## 確かめたこと

| # | 能力 | 要るところ |
|---|---|---|
| 1 | `file://` で開く | 作業用ビューアの UT・IT・ST（テスト方針書 §4。作業用ビューアは `file://` で開く） |
| 2 | 通信の記録と、応答・失敗の注入（`fetch` の要求を止めて応答を返す、失敗させる） | LLD 9.2 の UT（タイルの 404・失敗、待ち時間の上限、公開用の 5 本と `site.json` の応答）、ST の通信の記録 |
| 3 | Canvas の画素を読む | LLD 9.2 の UT（等高線・点の描画）、ST の画素の照合 |
| 4 | ファイル選択に渡す | LLD 9.2 の UT（除外判断ファイルの読み込み） |
| 5 | ダウンロードの中身を取る | LLD 9.2 の UT（申請書・ZIP・除外判断ファイルの保存）、ST のダウンロードの記録 |
| 6 | 2 つのタブで localStorage と `storage` イベントを共有する | LLD 9.2 の UT（別の画面での変更の読み直し） |
| 7 | フレーム間隔の実測をテストのコードが読む（ページの中の `performance.now()` と `requestAnimationFrame` で測った、操作の無いときの値。補助の値） | ST の測定（`ST-NFR-010-01`。正式な値は開発者ツールのパフォーマンス計測で、層で同じ値を読めるかは確かめていない。ADR-OPS-010 の Decision 2） |
| 8 | メモリの値をテストのコードが読む（JS ヒープと、プロセスのグループの RSS の和。補助の値） | ST の測定（`ST-NFR-002-02`。記録だけの値。正式な値はタブのメモリの最大で、ブラウザのタスクマネージャで人が読む。ADR-OPS-010 の Decision 2） |
| 9 | 実際の入力を送る（押す・動かす・離す） | ST の連続操作の測定（`ST-NFR-010-01`。地図を動かす） |

能力 1〜6 は LLD 9.2 の画面の関数（HLD 3.7.3・3.8.3 の「置き場」が「画面」の 28 個）と、[#284](https://github.com/jj1xgo/findsummits/issues/284) のコメント（LLD 9.1 の各回から 9.2 への伝言）から挙げた。7〜9 は、ST の「ブラウザの測定」の段落がこの Issue に送った測定の分。

## 結果

版は `node --version`・`google-chrome --version`・`brave-browser --version`・`firefox --version` の値（Brave の Chrome DevTools Protocol の `Browser` は `Chrome/157.0.8103.79` を返すので、Brave の版は `--version` の値を書く）。Node.js は v24.22.2。

| # | Chrome 157.0.8103.78 | Brave 157.1.99.57 | Firefox 160.0（安定版） |
|---|---|---|---|
| 1 | 通った | 通った | 通った |
| 2 | 通った（`ok.txt` は注入した 200 と本文 `hello`、`fail.txt` は `TypeError`。2 つの要求を記録した） | 通った（同じ） | 通った（同じ） |
| 3 | 通った（`[255, 0, 0, 255]`） | 通った（同じ） | 通った（同じ） |
| 4 | 通った（`DOM.setFileInputFiles`） | 通った（同じ） | 通った（`input.setFiles`） |
| 5 | 通った（`Browser.setDownloadBehavior`） | 通った（同じ） | 通った（`browser.setDownloadBehavior`） |
| 6 | 通った | 通った | 通った |
| 7 | 通った（200 ms で 14 フレーム、最長 16.8 ms） | 通った（14 フレーム、最長 16.8 ms） | 通った（14 フレーム、最長 17.1 ms） |
| 8 | 通った（`Performance.getMetrics` の `JSHeapUsedSize` 984164、RSS の和 2286976 KiB） | 通った（980616、1249344 KiB） | 通った（JS ヒープは読めない。RSS の和 1384328 KiB） |
| 9 | 通った（`Input.dispatchMouseEvent`。`pointerdown` 1・`pointermove` 2・`pointerup` 1） | 通った（同じ） | 通った（`input.performActions`。同じ） |

- 能力 8 の RSS の和は、起動したプロセスのグループの `/proc/<pid>/status` の `VmRSS` を足したもの。ブラウザ全体の値で、タブだけの値ではなく、プロセスの間で共有するページを重ねて数えるので、実際の使用量より上に偏る。そのため、`ST-NFR-002-02` の正式な値（タブのメモリの最大）にはしない。JS ヒープを読む命令は Chrome DevTools Protocol にだけあり、WebDriver BiDi には無い。
- 走らせた後に、起動したブラウザのプロセスが残っていないことを `ps` で確かめた。

## 比べた結果

決める前の試し（2026-11-15、一時の場所で行い、道具はリポジトリに置いていない）で、能力 1〜6 を次のとおり確かめた。

| | Chrome 157.0.8103.78 | Brave 157.1.99.57 | Firefox 153.5.1 ESR |
|---|---|---|---|
| 自前（npm なし） | 6 つとも通った | 6 つとも通った | 6 つとも通った |
| WebdriverIO 10.2.0 | 6 つとも通った | 6 つとも通った（ダウンロードは BiDi の `browser.setDownloadBehavior` が要る） | 6 つとも通った |

- Firefox 153.5.1 ESR の試しで、WebDriver BiDi の `browserVersion` は `153.5.1` で、`esr` を含まなかった（`firefox --version` は `153.5.1esr` を含む）。チャンネルは `firefox --version` で見分ける。
- Firefox 153.5.1 ESR は、その後に安定版を入れたときに外れたので、上の「結果」の表では走らせ直していない。ESR は対応ブラウザの版でない（HLD の DEC130「JavaScript はモジュールを使わない ES2020」は安定版の最新）。
- WebdriverIO は、入れると 140 個のパッケージが入り、npm 12.2.0 が geckodriver・edgedriver の install script を止めた（`allowScripts`）。ドライバは実行のときにネットから取る。`newWindow` の後に操作の対象のタブが切り替わらず、明示的に `switchToWindow` が要った。Brave の後に、セッションを閉じても node が終わらなかった。

## 外した候補

- Playwright: 公式文書（<https://playwright.dev/docs/browsers>）に「Playwright doesn't work with the branded version of Firefox since it relies on patches.」「Playwright doesn't work with the branded version of Safari since it relies on patches.」とある。実物の Firefox・Safari を動かせず、テスト方針書 3.1 の「対象環境のブラウザで行う」を満たさない。

## CI のランナーのブラウザ

GitHub Actions の Ubuntu 24.04 のランナーの一覧（<https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md>、2026-11-15 に確かめた）には、Google Chrome 157.0.8103.50 と Mozilla Firefox 160.0 がある。Brave は無い。Node.js は 22.23.4 が既定で、24.22.2 がキャッシュにある。

## 注意点

- `/usr/bin/brave-browser` はラッパーのスクリプトで、起動した子のプロセスに `kill` を送っても、ブラウザの本体が残った。道具はプロセスのグループで起動し（`spawn` の `detached: true`）、グループごと止める（`process.kill(-pid)`）。
- Firefox は `--remote-debugging-port` で起動すると、標準エラー出力に `WebDriver BiDi listening on ws://127.0.0.1:<port>` と出る（Chrome DevTools Protocol は出ない）。接続先は `ws://127.0.0.1:<port>/session`。
- Firefox は `--no-remote` と新しいプロファイルで起動する（開いている Firefox に渡さないため）。
- `file://` のページから `https://` へ `fetch` するので、注入する応答には `Access-Control-Allow-Origin` の見出しを付ける。
- Debian testing には ESR でない Firefox のパッケージが無い（`firefox-esr` だけ。unstable には `firefox` がある）。安定版は Mozilla 公式の APT リポジトリ（`packages.mozilla.org`）から入れた。入れると `firefox-esr` は外れた。

## やり直すとき

ブラウザの版を上げたとき（または Node.js を上げたとき）は、リポジトリの根で次を走らせる。どのコマンドも、作業ディレクトリをリポジトリの外に新しく作って渡す。道具は能力ごとの合否を出力の `checks` に出し、9 つとも期待どおりなら終了コード 0、そうでなければ 1 で終わる。

```bash
node docs/decisions/research/browser-automation-probe/cdp_probe.js google-chrome "$(mktemp -d)"
node docs/decisions/research/browser-automation-probe/cdp_probe.js brave-browser "$(mktemp -d)"
node docs/decisions/research/browser-automation-probe/bidi_probe.js /usr/lib/firefox/firefox "$(mktemp -d)"
```

作業ディレクトリが空でなければ、道具は止まる（前回のダウンロードを今回の結果と取り違えないため）。道具は全体 90 秒・1 つの命令 15 秒で打ち切り、打ち切り・例外・SIGINT・SIGTERM のときも起動したブラウザのグループを止める（2026-11-15 に、途中で SIGTERM を送って、`error` が `SIGTERM` の JSON が出てブラウザが残らないことを Brave と Firefox で確かめた）。走らせた後に、`ps -eo pid,pgid,cmd` で起動したブラウザが残っていないことを確かめ、作業ディレクトリを消す。

## 確かめていないこと

- Safari と safaridriver（この機械には無い。[#338](https://github.com/jj1xgo/findsummits/issues/338)「Safari（Mac）で #197 の確かめ用のページを測る」の機会に確かめる）。
- Windows・macOS での Chrome・Brave・Firefox。
- ヘッドありの起動。
- 開発者ツールの計測と同じ時間の値を層で読むこと（`ST-NFR-010-01` のフレーム時間・内訳・入力の処理時間・画面が変わるまでの時間、`ST-NFR-008-01` の操作から画面が変わるまで・ダウンロードの開始までの時間。Chrome DevTools Protocol の `Tracing` などで取れるか。能力 7 は操作の無いときのフレーム間隔、能力 9 は入力のイベントの数だけを確かめた）。
- `ST-NFR-002-02` のタブが落ちたことを層で知ること。
- https の配信先を開くこと（公開用ビューアのケース）。
- CI のランナーの上で道具を走らせること。
