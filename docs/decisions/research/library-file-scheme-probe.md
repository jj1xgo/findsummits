# ライブラリの書き込みの可否と file:// での動きの確かめ（#197）

[#197](https://github.com/jj1xgo/findsummits/issues/197)「CMP7 の実装の前にライブラリの版を決め、ブラウザでの動きを確かめる」の確かめの記録。版を上げるとき（HLD の DEC12・DEC129）に同じ確かめをやり直せるよう、道具を `library-file-scheme-probe/` に置く。

## 道具

| ファイル | 役目 |
|---|---|
| `library-file-scheme-probe/fetch_libs.sh` | 版を固定した URL から `build/probe-libs/` へライブラリを取り、`sha384`・`sha512` を出す。公開の値があれば照合する |
| `library-file-scheme-probe/write_check.js` | Node.js で、候補ごとに申請書と一覧の XLSX と ZIP の見本を作る（`build/probe-libs/` のファイルを読み、npm は使わない） |
| `library-file-scheme-probe/expected.json` | 見本の中身と期待（セルの値と型、表示形式、結合、固定、シートの名前と順、ZIP の時刻） |
| `library-file-scheme-probe/read_check.py` | openpyxl と `zipfile` で読み返し、項目ごとに判定する。2 つ目からの出力先とはバイト列を比べる（決定性） |
| `library-file-scheme-probe/test_read_check.py` | `read_check.py` の判定の試験 |
| `library-file-scheme-probe/site/` | ブラウザで開く確かめ用のページ一式（P1〜P15 の `index.html`、`a/`・`b/`、Canvas の読み返しの `selftest.html`） |
| `library-file-scheme-probe/build_site.sh` | `site/` を `build/probe-site/` に組み立て、`file://` で開くための `probe.zip` を作る |
| `library-file-scheme-probe/headless_probe.js` | Chrome・Brave をヘッドレスで起動し、DevTools Protocol から手順どおりにページを開いて結果の JSON を集める |
| `library-file-scheme-probe/summarize.py` | `headless_probe.js` の出力や貼った JSON を、1 行 1 項目に並べる |
| `library-file-scheme-probe/png_decode_check.js` | 地理院の標高タイルの PNG を、Canvas を通さずに `DecompressionStream` で復号し、Canvas の読み出しと比べる値を出す |

やり直すときは、リポジトリのルートで次を走らせる。

```bash
P=docs/decisions/research/library-file-scheme-probe
bash $P/fetch_libs.sh
TZ=Asia/Tokyo node $P/write_check.js build/probe-out/tokyo-1
sleep 3
TZ=Asia/Tokyo node $P/write_check.js build/probe-out/tokyo-2
TZ=UTC node $P/write_check.js build/probe-out/utc-1
venv/bin/python3 $P/read_check.py build/probe-out/tokyo-1 build/probe-out/tokyo-2 build/probe-out/utc-1
```

## 版と配布元

2026-11-08 に取得した（`fetch_libs.sh`）。どれも HTTP 200。

| ライブラリ | 版 | URL | sha384 | 公開の値との照合 |
|---|---|---|---|---|
| Leaflet（JS） | 1.9.4 | `https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.js` | `sha384-cxOPjt7s7Iz04uaHJceBmS+qpjv2JkIHNVcuOrM+YHwZOmJGBXI00mdUXEq65HTH` | 公式の `sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=` と一致 |
| Leaflet（CSS） | 1.9.4 | `https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css` | `sha384-sHL9NAb7lN7rfvG5lfHpm643Xkcjzp4jFvuavGOndn6pjVqS6ny56CAt3nsEVT4H` | 公式の `sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=` と一致 |
| JSZip | 3.10.2 | `https://cdn.jsdelivr.net/npm/jszip@3.10.2/dist/jszip.min.js` | `sha384-DdGlNq+wVXAn83gXqwyeFHB7iyXy6L0rLrNzgDmhKWPjiJLg9vj6qosYmZmkMfQ+` | cdnjs の `sha512-/ICos1xr6gGjsbC2d7Z6D0hmKAnNbkCv5Pp803Q75xgHowbEcgI4CVOHMHUux/ZorCuod6dzuJOjfNoCKV0tRw==` と一致 |
| SheetJS CE | 0.20.3 | `https://cdn.sheetjs.com/xlsx-0.20.3/package/dist/xlsx.full.min.js` | `sha384-EnyY0/GSHQGSxSgMwaIPzSESbqoOLSexfnSMN2AP+39Ckmn92stwABZynq1JyzdT` | 公開の値なし |
| ExcelJS | 4.4.0 | `https://cdn.jsdelivr.net/npm/exceljs@4.4.0/dist/exceljs.min.js` | `sha384-Pqp51FUN2/qzfxZxBCtF0stpc9ONI6MYZpVqmo8m20SoaQCzf+arZvACkLkirlPz` | cdnjs の `sha512-dlPw+ytv/6JyepmelABrgeYgHI0O+frEwgfnPdXDTOIZz+eDgfW07QXG02/O8COfivBdGNINy+Vex+lYmJ5rxw==` と一致 |
| xlsx-js-style | 1.2.0 | `https://cdn.jsdelivr.net/npm/xlsx-js-style@1.2.0/dist/xlsx.bundle.js` | `sha384-OUW9euuUyxyHcAhTqbhI+Iyb8LMssXt/cpz0yXhs9UWG2/R/uaWdakx/4cfww7Vb` | 公開の値なし |

陰性の対照（ブラウザの P8）に使う `https://cdn.jsdelivr.net/npm/jszip@3.10.2/dist/jszip.js` の sha384 は `sha384-PGSB/GCx599IN8vJ55Jk+jamWFQGq+F7ND2oXE5JTGw4NXfSl02bP7CIj00eH7Ew`。

一次資料（2026-11-08 に読んだ）:

- SheetJS: 最新は 0.20.3（<https://docs.sheetjs.com/docs/getting-started/installation/standalone>「The current version is 0.20.3.」）。配布元は cdn.sheetjs.com で、npm の `xlsx` は 0.18.5 のまま、jsDelivr の 0.20.3 は 404。セルの書式は「SheetJS Pro offers cell / text styling, conditional formatting and additional styling options.」（<https://docs.sheetjs.com/docs/api/write-options>）。表示形式は `z`（<https://docs.sheetjs.com/docs/csf/features/nf>）、文書のプロパティは `Props`（<https://docs.sheetjs.com/docs/csf/features/props>）。
- ExcelJS: 固定は `views` の `state: 'frozen'`、結合は `mergeCells`、表示形式は `numFmt`、折り返しは `alignment.wrapText`、文書のプロパティは `workbook.created`（<https://github.com/exceljs/exceljs> の README）。4.4.0 は 2023-10-19、MIT。
- xlsx-js-style: 1.2.0 は 2022-04-05、Apache-2.0、土台は SheetJS 0.18.5（<https://github.com/gitbrent/xlsx-js-style>）。
- JSZip: `generateAsync` の `compression` は `STORE` と `DEFLATE`（<https://stuk.github.io/jszip/documentation/api_jszip/generate_async.html>）。エントリの時刻は UTC の getter で書く（<https://github.com/Stuk/jszip/issues/369>、open）。3.10.2 は 2026-09-08、MIT または GPL-3.0。
- Leaflet: 安定版は 1.9.4、2.0 は beta（<https://leafletjs.com/download.html>）。

## 書き込みの可否

2026-11-08 にホストの Node.js 24.21.0 で作り、openpyxl 3.1.5 で読み返した。候補は (a) SheetJS CE、(b) SheetJS CE で書いた後に JSZip で `xl/worksheets/sheet1.xml` の `<sheetView>` に `<pane xSplit="0" ySplit="5" topLeftCell="A6" activePane="bottomLeft" state="frozen"/>` を書き足したもの、(c) ExcelJS、(d) xlsx-js-style。4 つとも Node.js の `require` で読めた。

要件の列は、申請書の値と型・結合・`A6` での固定・シート `Sheet1` の 1 枚、一覧の値と型・表示形式・シートの名前と順・出典の `A1`。参考の列は `B3` の折り返し（HLD 4.11.1 は見出しの書式を対象外にしている）。「値と型」は、null と空文字のセル（DEC112）を XML に要素が無いことで見た。

| 項目 | (a) SheetJS CE | (b) SheetJS CE＋pane | (c) ExcelJS | (d) xlsx-js-style |
|---|---|---|---|---|
| 申請書のシート `Sheet1` | 一致 | 一致 | 一致 | 一致 |
| 申請書の結合（6 か所） | 書ける | 書ける | 書ける | 書ける |
| 申請書の `A6` での固定 | **書けない** | 書ける | 書ける | **書けない** |
| 申請書の値と型（null と空文字はセルを置かない、E・H 列は表示形式の無い数） | 一致 | 一致 | 一致 | 一致 |
| 申請書の表示形式 | 一致 | 一致 | 一致 | 一致 |
| 一覧のシートの名前と順・出典の `A1` | 一致 | 一致 | 一致 | 一致 |
| 一覧の値と型（真偽値は文字列、整数は表示形式なし） | 一致 | 一致 | 一致 | 一致 |
| 一覧の表示形式（`0.00000000`・`0.00`・`0.0`） | 一致 | 一致 | 一致 | 一致 |
| 文書のプロパティ（作成日時・更新日時）を書かないとき | 書かない | 書かない | **今の時刻を書く** | 書かない |
| 作成日時を固定値で書くとき | 書ける | 書ける | 書ける | 書ける |
| 決定性（同じ TZ で 3 秒あけた 2 回、TZ を替えた 2 回） | 一致 | 一致 | **不一致**（`docProps/core.xml` の中身と、全エントリの時刻） | 一致 |
| 参考: `B3` の折り返し | 書けない | 書けない | 書ける | 書ける |

気づいたこと:

- (b) は、JSZip で書き戻すときに `createFolders: false` を付けないと、JSZip が `xl/`・`xl/worksheets/` のフォルダのエントリを今の時刻で足し、決定性が崩れた（付けると一致した）。
- (a)(b)(d) の XLSX のエントリの時刻は空（`unzip -l` で `1980-00-00`）。(b) は JSZip で書き戻すと `2107-11-30` に見える。中身の判定には響かない。
- (c) は作成日時・更新日時を固定値にしても、XLSX の中のエントリの時刻が今の時刻になるので、バイト列は決定的にならない。

ZIP（JSZip 3.10.2）:

| 見本 | `TZ=Asia/Tokyo` | `TZ=UTC` |
|---|---|---|
| 圧縮 | DEFLATE | DEFLATE |
| 現地時刻 `2026-11-08 12:34:56` をそのまま `date` に渡す | `(2026, 11, 8, 3, 34, 56)`（UTC の時刻が入り、9 時間ずれる） | `(2026, 11, 8, 12, 34, 56)` |
| `t - t.getTimezoneOffset()*60000` に補正して渡す | `(2026, 11, 8, 12, 34, 56)` | `(2026, 11, 8, 12, 34, 56)` |

DEC124 の「端末の現地時刻として書く」は、補正して渡せば満たせる。

## `file://` と `http://localhost` での動き

`https://` の置き場（Cloudflare Pages）はやめた（持ち主の判断、2026-11-08。リモートの端末からでは wrangler login の許可の戻り先が届かなかった）。代わりに、2026-11-10 にホストの `python3 -m http.server`（`127.0.0.1:8197`）から `build/probe-site/` を配信し、`http://localhost:8197/` で測った（持ち主の判断、2026-11-10）。localhost は安全なコンテキストなので `https://` に近いが、本物の `https://` の配信ではない。

測った組み合わせ:

- 2026-11-08: Chrome 157 と Brave（どちらもヘッドレス、新しいプロファイル）の `file://`。`library-file-scheme-probe/headless_probe.js` から、「保存する → `a/` → `b/` → 確かめる → 見本を落とす」の後、同じプロファイルで起動し直して「確かめる」。
- 2026-11-10: 同じ道具と手順で、Chrome と Brave（ヘッドレス）の `http://localhost`。
- 2026-11-10: 持ち主がホストの画面で、Firefox 153.0（ESR、既定の設定）と Brave（Chrome/157、持ち主のプロファイル、Shields は既定）を操作した。`http://localhost` は「確かめる」だけ。`file://` は `probe.zip` を展開して Ctrl+O で開き、「保存する → `a/` → `b/` → `index.html` で確かめる」の後、ブラウザを完全に終了して開き直し「確かめる」。結果の JSON は持ち主が貼った。
- not run: Safari（持ち主の Mac が要る。[#338](https://github.com/jj1xgo/findsummits/issues/338) で行う）、本物の `https://` の配信。

### ブラウザでのやり直しの手順

1. リポジトリのルートで `bash docs/decisions/research/library-file-scheme-probe/build_site.sh` を走らせ、`build/probe-site/` を作る。
2. `http://localhost` の回: `cd build/probe-site && python3 -m http.server 8197 --bind 127.0.0.1` で配信し、`http://localhost:8197/` を開いて「確かめる」を押し、JSON を写す。
3. `file://` の回: `build/probe-site/probe.zip` を展開し、展開した `findsummits-probe-197/index.html` をそのブラウザの「ファイルを開く」で開く。
   1. 「保存する」を押す → `a/index.html` を開く → `b/index.html` を開いて、値が見えたかを記録する → `index.html` で「確かめる」を押し、JSON を写す（閉じる前）。
   2. ブラウザを完全に終了して開き直し、`index.html` で「確かめる」を押して JSON を写す（閉じた後。「保存する」は押さない）。
   3. 「見本を落とす」で落ちた `probe-samples.zip` を展開し、`read_check.py` にかける。Mac では Finder で中のファイルの変更日が 12:34 に見えるかも見る。
4. Mac で ZIP が開けない（「壊れている」「開発元を確認できない」）ときは、Finder の右クリックの「開く」か、ターミナルの `xattr -d com.apple.quarantine <フォルダ>` を使う。Safari が ZIP を自動で展開したときは、その展開されたフォルダを使う。
5. `selftest.html` を開き、出た `diff=` の数を記録する（0 でなければ、Canvas の読み出しに手が入っている）。
6. Chrome・Brave は、手順 2・3 を `headless_probe.js` でも行える（使い方はファイルの先頭）。

### `file://`

| ID | 確かめること | Chrome（ヘッドレス） | Brave（ヘッドレス） | Firefox（画面あり） | Brave（画面あり） |
|---|---|---|---|---|---|
| P1 | データファイルを普通の script で読む | 通った | 通った | 通った | 通った |
| P2 | `fetch` でデータファイルを読む | 通らない（`Failed to fetch`） | 通らない | 通らない（`NetworkError`） | 通らない（`Failed to fetch`） |
| P3 | XMLHttpRequest で読む | 通らない（`error`） | 通らない | 通らない（`error`） | 通らない（`error`） |
| P4 | モジュールの script が実行される | 通らない | 通らない | 通らない | 通らない |
| P5 | Leaflet の CSS と JavaScript を SRI 付きで読む | 通った | 通った | 通った | 通った |
| P8 | 違えたハッシュの JSZip が読まれない（陰性の対照） | 通った（`error`、`JSZip` は無い） | 通った | 通った | 通った |
| P6 | JSZip を SRI 付きで足して読む | 通った | 通った | 通った | 通った |
| P7 | SheetJS と ExcelJS を SRI 付きで足して読む | 通った | 通った | 通った | 通った |
| P9a | localStorage に書いて読み返す | 通った | 通った | 通った | 通った |
| P9b | 閉じて開き直した後に、保存した値が残る | 残った | 残った | 残った | 残った |
| P10 | `a/` が書いた値が `b/` と `index.html` から見える | 見えた（両方） | 見えた（両方） | **見えない（両方）** | 見えた（両方） |
| P11・P12 | 地理院の DEM10b・DEM5a・DEM1a の画素を `fetch` と `img` の両方で読む | 通った | 通った（画素は Chrome と同じ） | 通った（画素は Chrome と同じ） | 通った（画素は Chrome と同じ） |
| P13 | 基準点のタイルを読む | 通った（18 点） | 通った | 通った（18 点） | 通った（18 点） |
| P14 | データの無い範囲の 4 つが 404 | 4 つとも 404 | 4 つとも 404 | 4 つとも 404 | 4 つとも 404 |
| P15 | 見本を作って落とす | 落ちた。読み返しは Node.js の結果と同じ判定 | 落ちた | 押していない | 押していない |

### `http://localhost`

| ID | Chrome（ヘッドレス） | Brave（ヘッドレス） | Firefox（画面あり） | Brave（画面あり） |
|---|---|---|---|---|
| P1〜P8 | 全部 通った（P2〜P4 も通る） | 全部 通った | 全部 通った | 全部 通った |
| P9a | 通った | 通った | 通った | 通った |
| P9b・P10 | 残った・見えた | 残った・見えた | 測っていない（保存も `a/` もしていない） | 測っていない |
| P11・P12 | 通った | **通ったが画素に雑音** | 通った（画素は Chrome と同じ） | **通ったが画素に雑音** |
| P13・P14 | 18 点・4 つとも 404 | 同じ | 同じ | 同じ |
| P15 | 落ちた。読み返しは `file://` の回と同じ判定（違うのは ExcelJS の作成日時・更新日時だけ） | 落ちた | 押していない | 押していない |

P11・P12 の画素（タイルの真ん中の RGBA と、全画素の値の合計）:

| タイル | Chrome・Firefox（どちらの配信でも）と Brave の `file://` | Brave ヘッドレスの localhost | Brave 画面ありの localhost |
|---|---|---|---|
| `dem_png/10/909/403` | `0,0,64,255`、26716656 | `1,0,65,255`、26716782 | `0,1,65,255`、26716778 |
| `dem5a_png/15/29105/12903` | `0,1,36,255`、22799732 | `1,0,36,255`、22799774 | `0,1,36,255`、22799770 |
| `dem1a_png/17/116421/51613` | `128,0,0,255`、21981456 | `129,1,0,255`、21981568 | `128,0,0,255`、21981570 |

`fetch` と `img` の経路は、どのブラウザでも同じ値だった。

## 見込みと違った行

- **Brave の `http://localhost` の P11・P12**: Shields（既定）が Canvas の読み出しに雑音を入れた（指紋採取を防ぐ機能による値のずらしと見られる）。値は起動ごとに違い、R の 1 のずれは標高で 655.36 m に当たる（地理院の PNG 標高タイルは R×2^16＋G×2^8＋B を 0.01 m 単位で表す）。`file://` では雑音は無かった。`https://` で配信する公開用ビューア（DEC164）の等高線オーバーレイが、既定の Shields の Brave で崩れる見込みが高い（本物の `https://` では not run）。見直す DEC: DEC159（とあわせて、等高線の処理の節と、DEC130 の Brave の扱い）。
- **Firefox の `file://` の P10**: 別のフォルダのページ（`a/`・`b/`）と `index.html` の間で localStorage を共有しなかった（既定の `security.fileuri.strict_origin_policy` による、フォルダかファイルを単位とするオリジンと見られる。どちらの単位かは測っていない）。同じページを開き直した後には値が残った（P9b）。作業用ビューアを別のフォルダに置き直して開くと、Firefox では前の保存が見えない。見直す DEC: DEC136・DEC138。

## 見込みと違った行の扱い

- **Brave の Canvas の雑音**（持ち主の判断、2026-11-10）: 標高タイルの PNG を Canvas を通さずに復号する。Brave は対応に残し、Shields は既定のままで等高線が正しく出る。HLD の DEC194 に書いた。
  - 確かめ 1: 雑音は自分で書いた画素の読み返しでも入る。`library-file-scheme-probe/site/selftest.html`（256×256 の既知の画素を `putImageData` で書いて `getImageData` で読み返し、違う値を数える）で、画面ありの Brave の `http://localhost` では 262144 個の値のうち 278 個が違い、ヘッドレスの Chrome では 0 個だった。
  - 確かめ 2: P11 の 3 つのタイルは、どれも 256×256、8 ビットの RGB（カラータイプ 2）、インターレースなしで、チャンクは IHDR・IDAT・IEND だけだった。`library-file-scheme-probe/png_decode_check.js`（Node.js 24.21.0）で `DecompressionStream("deflate")` と行のフィルタを戻す処理だけで復号すると、真ん中の画素と全画素の値の合計が、3 つとも Chrome の Canvas の読み出し（上の表の左の列）と一致した。
  - 初めは「既知の画素で自己診断し、ずれていたら等高線を描かずに知らせる」と決めたが、確かめ 2 の後に替えた（既定の Brave で等高線が出ないため）。
- **Firefox の `file://` の localStorage の分け方**（持ち主の判断、2026-11-10）: Firefox は対応に残し、挙動は変えない。作業用ビューアは `$DATA_DIR/results/merged_viewer.html` に書かれ、そこから開く限り前の世代からの引き継ぎは働く。別のフォルダへ写して開くと Firefox では前の保存が見えない（除外台帳と申請に戻した記録は除外判断 JSON で持ち越せる。名前と根拠の下書きは持ち越せない）。HLD の DEC136 に書いた。反対に Chrome と Brave は、フォルダが違っても localStorage を 1 つにまとめるので、別の `$DATA_DIR` のビューアの世代も引き継ぎの候補に入る。これも DEC136 に書いた。

## XLSX の方式の比較

(a) と (d) は申請書の `A6` での固定が書けず、要件で落ちた（「書き込みの可否」）。残る 2 つを比べる。

| 項目 | (b) SheetJS CE＋JSZip で pane を書き足す | (c) ExcelJS |
|---|---|---|
| 要件の列（値と型・結合・固定・シート・表示形式・出典の `A1`） | 全部満たす | 全部満たす |
| 参考: `B3` の折り返し | 書けない（HLD 4.11.1 の対象外） | 書ける |
| 文書のプロパティ | 書かなければ書かない。固定値でも書ける | 書かなくても今の時刻を書く。固定値なら書ける |
| 決定性（[NFR-003](../../20_SRS.md#nfr-003-再現性決定論的出力)） | 一致（JSZip の書き戻しに `createFolders: false` が要る） | **不一致**（`docProps/core.xml` と全エントリの時刻に今の時刻が入る） |
| ライセンス | Apache-2.0（SheetJS CE 0.20.3。配布元の `package.json`）、MIT または GPL-3.0（JSZip） | MIT |
| 最後の版の日付 | SheetJS CE 0.20.3 は 2024-07-18（SheetJS の git のタグ `v0.20.3`）、JSZip 3.10.2 は 2026-09-08 | 4.4.0 は 2023-10-19 |
| 大きさ | `xlsx.full.min.js` 951904 バイト（JSZip 97781 バイトは申請エビデンス ZIP のためにどちらでも読む） | `exceljs.min.js` 947702 バイト（JSZip はどちらでも読む） |
| 配布元 | cdn.sheetjs.com（jsDelivr の 0.20.3 は 404）。JSZip は jsDelivr | jsDelivr |
| SRI の公開の値 | SheetJS は無い（自分で取った sha384 を使う）。JSZip は cdnjs と一致 | cdnjs と一致 |
| `file://` での読み込み（P7） | Chrome・Brave・Firefox で通った（Safari は not run） | 同じ |
| ライブラリの名前の書き直し | 要らない（DEC129 の 3 つのまま） | 要る（SRS 12 か所・HLD・LLD・IT・ST と、SRS の改訂の ADR） |
| 実装の手間 | pane の XML を書き足す処理を自分で持つ（`<sheetView>` の中の 1 要素） | 決定性のために、`docProps/core.xml` と ZIP のエントリの時刻を JSZip で読み直して書き直す処理が要る |

決めた方式（持ち主の判断、2026-11-10）: (b)。SheetJS CE 0.20.3 で書き、JSZip 3.10.2 で申請書の `<sheetView>` に `A6` の固定の `<pane>` を書き足す（書き戻しは `createFolders: false`）。理由は、要件を全部満たし、決定性を保ち、DEC129 のライブラリの 3 つのまま名前の書き直しが要らないため。(c) ExcelJS は決定性のための書き直しと名前の書き直しが要る。新しい Issue は立てない。
