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
