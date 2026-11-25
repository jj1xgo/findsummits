# ADR-OPS-011: LLD の確定と製品のコードの照合を分け、`public/` を照合の対象に足す

| 項目 | 内容 |
|---|---|
| 状態 | 採用・実装済み |
| 決定日 | 2026-11-25 |

---

## Context

`tools/lint_trace.py` は、詳細設計書（LLD）を `CONFIRMED_STAGES` に入れると、LLD と上位の概要設計書（HLD）の対応の被覆（T3）、LLD の「ファイル」のパスの実在（T2）、製品のコードと LLD の双方向の照合（T5）を一緒に効かせていた（[ADR-LLD-001](ADR-LLD-001-lld-format-module-granularity-and-t2-timing.md) の Decision 10、[ADR-OPS-005](ADR-OPS-005-test-document-status-and-t5-timing.md) の Decision 6）。ゲート 4（LLD → COD）の判定を `tools/lint_trace.py` に反映する段取りは [#246](https://github.com/jj1xgo/findsummits/issues/246) で決めることにしていた。

2026-11-25（devel `bb7d628`）に、LLD を `CONFIRMED_STAGES` に入れて試すと 97 件の指摘が出た。内訳は、LLD の「ファイル」のパスが git に無い T2 が 40 件、同じファイルが製品のコードの対象でなく、名乗ってもいないという T5 が 40 件、今の試作のコード（`src/*.c`、`scripts/` の今のスクリプト）がどの LLD のモジュールも名乗っていないという T5 が 17 件。T3 は 0 件で、単体テスト仕様書（UT）を `CONFIRMED_STAGES` に足しても増えない。

- 40 件は、名前をそろえても消えず、LLD のファイルがすべてそろうまで残る。
- 試作のコードは、C++ 移行（[ADR-SRS-010](ADR-SRS-010-cpp-opencv-migration.md)）の Phase 1・2 の「現行と完全一致」の比較に使うので、COD の始めには消せない。
- 製品の `public/index.html` とそのテストの `tests/public/`、拡張子の `.html`・`.js` は、T5 の対象に入っていない（ADR-LLD-001 の Consequences）。LLD 1.2 が定める `trace:` の置き方（JavaScript は `// trace:`、`public/index.html` は 1 本が 2 つのモジュールを名乗る）を読む検査は、[#198](https://github.com/jj1xgo/findsummits/issues/198) の (2) に回してあった。
- `tests/public/browser.js`（ブラウザを動かす試験の道具。LLD 2.6）と、空の `tests/scripts/__init__.py`（テスト方針書 3.4）は、どのテストケースにも属さない。

このままでは、ゲート 4 の判定が Go でも、LLD を `CONFIRMED_STAGES` に足すと CI が止まる。持ち主が 2026-11-25 に、次のとおり決めた。

## Decision

1. **LLD の確定**: LLD は、ゲート 4 の判定が Go か条件付きGo なら、今までどおり `CONFIRMED_STAGES` に足す（[開発ガイド §4](../03_development.md#4-フェーズゲート)）。LLD を入れたときから効くのは、T3（HLD の第 3〜5 章の節を対応 HLD に持つモジュールが要る）と、製品のコードの名乗りの誤り（LLD に無いモジュールを名乗る T2、名乗ったモジュールの「ファイル」の欄に無い T5）。
2. **コードの照合**: `IMPLEMENTED_STAGES` に LLD を認める。LLD を入れたときから、LLD の「ファイル」のパスの実在（T2）、どのモジュールも名乗らない製品のファイル（T5）、「ファイル」のパスが製品のコードの対象でないか、そのモジュールを名乗らないこと（T5）が効く。足すのは、製品のコードがそろい、試作のコードを `src/`・`scripts/` から除いた変更で、足した版で `make lint` が通ることで確かめる。LLD を `IMPLEMENTED_STAGES` だけに入れる（`CONFIRMED_STAGES` に入れない）と、T1 で止まる。COD の途中は、新しいファイルの名乗り忘れと、モジュールのファイルの一部が無いことを止めない。「ファイル」のパスが無いファイルは T2 だけで止め、T5 の「対象ではありません」は重ねない。
3. **開始基準**: 各レベルの正式な実行の開始基準（[テスト方針書 5.6](../02_test_policy.md#56-開始基準)）の全レベルに共通の条件に、LLD が `IMPLEMENTED_STAGES` にあり、製品のコードと LLD の照合が通ることを足す。ADR-OPS-005 の Decision 5 と同じく、条件はレベル全体に掛かる。
4. **`public/` と JavaScript**: 製品のコードの対象に `public/`、テストのコードの対象に `tests/public/`、拡張子に `.html`・`.js` を足す。`.js` は、行頭（空白を除く）の `//` のコメントだけを `trace:` として読む（文字列・テンプレートリテラル・`/* */` の中と、行末の `//` は読まない）。`.html` は、script 要素の中の同じ形のコメントだけを読む（HTML のコメントや `<textarea>` の中の疑似の script 要素は読まない。読み方は標準の `html.parser`）。#198 の (2) はこれで済む。
5. **名乗らなくてよいファイル**: 中身が空白だけのテストのファイルは、テストケースを名乗らなくてよい。`tests/public/browser.js` は、どのテストケースにも属さない試験の道具なので、`EXEMPTIONS` の `T5:tests/public/browser.js` で除く（根拠は本 ADR）。
6. **UT の確定**: UT の確定は、ゲート 4 の判定と同じ場で承認者が認める。Go か条件付きGo で UT の確定も認めたら、LLD を足す変更と同じ取り込みで、`50_UT.md` のヘッダーを「確定」にして `CONFIRMED_STAGES` に足す。先に、LLD 全体と UT の最終周回（[#245](https://github.com/jj1xgo/findsummits/issues/245)）で Critical・Important の指摘が残っていないことと、LLD と UT を足した検査で指摘が 0 件であることを確かめる。判定は、ゲートの記録と、UT の進捗を追う Issue（[#244](https://github.com/jj1xgo/findsummits/issues/244)）の両方に記録する。UT を `IMPLEMENTED_STAGES` に入れる時機は ADR-OPS-005 のままで、UT の自動のケースのテストのコードがそろったときに足す。

検査が効き始める時期は、次のとおりになる（LLD に関する行。テスト文書の行は ADR-OPS-005 のまま）。

| 検査 | 対象 | 効き始める時期 |
|---|---|---|
| T3 | LLD の対応 HLD の被覆 | LLD を `CONFIRMED_STAGES` に入れたとき |
| T2 | 製品のコードが名乗る LLD のモジュールの実在 | LLD を `CONFIRMED_STAGES` に入れたとき |
| T5 | 名乗ったモジュールの「ファイル」の欄に、そのファイルがあること | LLD を `CONFIRMED_STAGES` に入れたとき |
| T2 | LLD の「ファイル」のパスの実在 | LLD を `IMPLEMENTED_STAGES` に入れたとき |
| T5 | どのモジュールも名乗らない製品のファイル、「ファイル」のパスの対象外・名乗りの欠け | LLD を `IMPLEMENTED_STAGES` に入れたとき |

## Alternatives

- **COD の最初に、名乗りだけの空のファイルを 40 本置く**: 検査は初めから全部効くが、空のファイルで通るので、コードがそろった印にならない。試作のコードを別の場所へ移す作業も先に要る。不採用。
- **COD の終わりまで LLD を `CONFIRMED_STAGES` に入れない**: ツールはほぼ変わらないが、その間 T3 が効かず、UT も確定にできない（`STAGE_PARENT` が UT の上位に LLD を求める）。開発ガイド §4 の「判定が Go か条件付きGo なら足す」に例外も要る。不採用。
- **UT の確定を、UT の正式な実行の前まで待つ**: COD の間は UT がドラフトのままで、期待値の根拠が固まった状態を表せない。T3 も効かず、確定の前に COD で変わった分をもう一度レビューする手間が増える。不採用。
- **ADR-LLD-001 の Alternatives が却下済みの案**（`EXEMPTIONS` で外す、`COD` の段を `CONFIRMED_STAGES` に足す、「ファイル」に試作のパスを書く）は、そのまま却下のままにする。
- **試験の道具を名前（`test_` で始まるか）で除く**: `tests/src/flow_stage.cpp`・`tests/src/stub_stage.cpp` などの補助のファイルも、ケースを名乗る決まり（LLD 6.1.1・6.11.1）で、名前で除くとその名乗りの検査が外れる。個別の例外は `EXEMPTIONS` に根拠付きで置く。不採用。

## Consequences

- `tools/lint_trace.py` に、`IMPLEMENTED_STAGES` に LLD を認める段の検査（T1）、LLD の「ファイル」のパスの実在と名乗りの検査を `IMPLEMENTED_STAGES` で効かせる変更、`public/`・`tests/public/`・`.html`・`.js` の読み取り（`js_line_comments`、`html_scripts`）、空白だけのテストのファイルの除外、`EXEMPTIONS` の 1 項目を足した。`CONFIRMED_STAGES` と `IMPLEMENTED_STAGES` は変えていない（ゲート 4 の後に足す）。
- 今のリポジトリで、LLD を `CONFIRMED_STAGES` に入れた検査は 0 件（UT を足しても 0 件）、LLD を `IMPLEMENTED_STAGES` にも入れた検査は 57 件（T2 の 40 件と、試作のコードが名乗らない T5 の 17 件）になる。後者は、製品のコードがそろい、試作のコードを除くまで残る。
- [開発ガイド §4・§6.2](../03_development.md#62-検査)、[文書管理ルール「追跡の宣言」](../CLAUDE.md#追跡の宣言)、[テスト方針書 5.6](../02_test_policy.md#56-開始基準)、LLD の 1.2 と 2.6 を合わせて直した。ADR-LLD-001・ADR-OPS-005・[ADR-URD-020](ADR-URD-020-requirement-traceability-and-consistency.md) に追記した。
- 正規表現リテラルの中の引用符・バッククォート・`/*` があると、`.js`・`.html` の名乗りを読み落とす（T5 で止まる側に倒れる）。入れ子のテンプレートリテラルで読み取りの状態がずれうる。どちらも既知の制限として、コードの docstring に書いた。
- COD の最初の作業（骨組み、試作の移動）の作り方は、本 ADR では決めない（[#193](https://github.com/jj1xgo/findsummits/issues/193)・[#3](https://github.com/jj1xgo/findsummits/issues/3)・[#4](https://github.com/jj1xgo/findsummits/issues/4)）。
- ゲート 4 の審査の手順（観点 1 に UT の収束と検査の 0 件を書く、判定を 1 つずつ聞く）は、メンテナ個人の補足資料に書いた。
