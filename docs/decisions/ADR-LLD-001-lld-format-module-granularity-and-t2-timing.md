# ADR-LLD-001: LLD の書式とモジュールの粒度を決め、「ファイル」のパスの実在の検査を COD の段から効かせる

| 項目 | 内容 |
|---|---|
| 状態 | 採用・未実装 |
| 決定日 | 2026-10-14 |

---

## Context

詳細設計書（LLD、`docs/40_LLD.md`）は、概要設計書（HLD）の確定とフェーズゲート 3（HLD → LLD）の後に書き始める。書き始める前に、次の 4 つが決まっていなかった。

- LLD の章立てと、モジュールの節の中の書き方。[文書管理ルール「HLD と LLD の書き分け」](../CLAUDE.md#hld-と-lld-の書き分け)は、LLD に「関数ごとの細部（型、内部のデータの持ち方、メッセージの文面、ファイルへの割り付け）」を書くとするが、節の並びは決めていない。
- モジュールの粒度。[ADR-HLD-001](ADR-HLD-001-program-structure-chapter-and-two-tier-it.md) は、プログラムと関数の名前と一覧を [HLD 第 3 章](../30_HLD.md#3-プログラム構造)で決め、LLD のモジュールの粒度は「LLD の書式を決めるときに決める」とした。[追跡の宣言](../CLAUDE.md#追跡の宣言)の検査（`tools/lint_trace.py` の T3）は、LLD の確定後、HLD の第 3 章〜第 5 章のどの節にも、それを「対応 HLD」に持つモジュールを求める。第 5 章（NFR 設計）の 11 節は特定のプログラムに還元しにくい。
- HLD が LLD に送った項目の受け皿。HLD の各節の「目的と範囲」の「対象外」の行に「LLD」と書いた項目が 37 行あり、ログの文面、一時ファイルの名前、書きかけのファイルを残さない書き方のように、いくつもの節で同じ種類の項目が繰り返し出る。[ADR-HLD-008](ADR-HLD-008-remove-hld-open-items-subsections.md) の[付録 B](ADR-HLD-008-remove-hld-open-items-subsections.md#付録-b-旧番号の対応表) は、旧「未決事項と後続」の項目のうち送り先が LLD のものを、この「対象外」の行へ移した。HLD を書く段で挙がった単体テスト（UT）の候補は [#202](https://github.com/jj1xgo/findsummits/issues/202)「LLD と IT を書くときに、UT と IT の候補を割り当てる」に集めてある。
- LLD の「ファイル」の宣言の検査の時期。`tools/lint_trace.py` の T2 は、「ファイル」に書いたパスが git に無ければ、LLD の文書があるだけで止める。今のコードはプロトタイプで、ファイルの名前は HLD の名前（[HLD 2.6.4](../30_HLD.md#264-ディレクトリ構成) と第 3 章）にそろっていない。HLD の名前どおりのパスを書くと、コードの段（COD）でコードを書き直すまで T2 が止め続ける。

持ち主が 2026-10-14 に次のとおり決めた。

## Decision

1. **章立て**: LLD は、§1 に用語と規約、§2 に共通部品と横断、§3 以降に CMP1〜CMP8 の順でコンポーネントごとの章（§3 が CMP1、…、§10 が CMP8）を置き、各章の下にモジュールの節を置く。
   - §2 は、[HLD 3.9](../30_HLD.md#39-共通部品) の共通部品のモジュールと、HLD の「対象外」の行で繰り返し出る項目を受ける横断の節を持つ。横断の節は、ログとメッセージの文面の決まり、ファイルの名前と書き方（一時ファイル・ロックファイル・取得完了の記録の名前と、書きかけのファイルを残さない書き方）、言語ごとに別に実装する式のテストベクトル（HLD の DEC6 の決まりで C++・Python・JavaScript の結果をそろえるもの）の 3 つから始める。
   - 横断の節はファイルに割り付ける単位ではないので、追跡の宣言（`ID`・`対応 HLD`・`ファイル`）を持たない。各モジュールの節は、横断の節の決まりに従うところを、その節へのリンクで指し、写さない。
2. **モジュールの節の書き方**: 各モジュールの節は、見出しの直下に追跡の宣言（`- **ID**: LLD-<モジュール名>`・`- **対応 HLD**:`・`- **ファイル**:`。書式は[文書管理ルール「追跡の宣言」](../CLAUDE.md#追跡の宣言)のまま）を置き、小節を「ファイル割付」「型とデータ」「関数の細部」「メッセージ文面」「UT 候補」の 5 つで、この順に固定する。書くことが無い小節も見出しを残し、「なし」と理由を書く。UT のケース ID は `UT-<モジュール名>-NN` とし、LLD の ID とそろえる。
3. **モジュールの粒度**: プログラム（HLD 第 3 章の各節の「プログラム」の表の 1 行）を 1 モジュールとすることを既定にする。例外は次の 2 つ。
   - CMP4 の `analyze_terrain` は関数の数が多いので、[HLD 3.4.3](../30_HLD.md#343-関数) の表の「群」を 1 モジュールとする（12 モジュール）。
   - CMP7 と CMP8 が共有する `index.html` は、[HLD 3.7.3](../30_HLD.md#373-関数) の「置き場」の「計算」（DOM に触れず Node.js で UT を行う script 要素）と「画面」（DOM・地図・localStorage に触れ、手動で確かめる script 要素）の 2 モジュールに分け、どちらも「対応 HLD」に HLD の 3.7 と 3.8 を並べる。
   - 2 つ以上のプログラムが使う部品のうち、HLD 3.9 の共通部品は §2 の 1 モジュール、CMP5 の[コンポーネント内の共通部品](../30_HLD.md#354-コンポーネント内の共通部品)は §7 の 1 モジュールとする。
4. **モジュール名**: HLD のプログラム名をそのまま使う。CMP4 の群は `analyze_terrain_` の後に群の英語の短い名前を付ける。`index.html` は拡張子を除いた `index` の後に `_calc`（計算）・`_screen`（画面）を付ける。HLD 3.9 の共通部品は `common`、CMP5 のコンポーネント内の共通部品は `cmp5_common` とする。名前は ID の書式（英数字と `_`）に従う。HLD でプログラム名や群を変えたときは、LLD のモジュール名を同じ変更で直す（[文書管理ルール「HLD と LLD の書き分け」](../CLAUDE.md#hld-と-lld-の書き分け)の名前の決まり）。
5. **書き始めのモジュールの一覧**: 次の 26 モジュールで書き始める。「対応 HLD」の第 4 章の節は、HLD の第 3 章の関数の表の「処理の正本」の列と [HLD 2.2.4](../30_HLD.md#224-srs-の-frnfr-との対応) の表から取った書き始めの割り当てで、LLD を書くときに確かめて直す。LLD を書いた後は、LLD の宣言を正とする。

   | 章 | モジュールの ID | HLD での名前 | 対応 HLD（第 3 章・第 4 章） | ファイル（パスの方針） |
   |---|---|---|---|---|
   | §2 | `LLD-common` | 3.9 の共通部品 | 3.9 | `scripts/` の下の Python のファイル（名前は LLD で決める） |
   | §3 | `LLD-preprocess_boundaries` | `preprocess_boundaries` | 3.1・4.17 | `scripts/preprocess_boundaries.py` |
   | §4 | `LLD-fetch_tiles` | `fetch_tiles` | 3.2・4.1 | `scripts/fetch_tiles.py` |
   | §5 | `LLD-run_pipeline` | `run_pipeline` | 3.3・4.23 | `scripts/run_pipeline.sh` |
   | §5 | `LLD-resolve_config` | `resolve_config` | 3.3・4.23 | `scripts/resolve_config.py` |
   | §6 | `LLD-analyze_terrain_launch` | 「起動」の群 | 3.4・4.4・4.14 | `src/` の下の C++ のファイル（以下 CMP4 の群は同じ。群ごとの名前は LLD で決める） |
   | §6 | `LLD-analyze_terrain_target` | 「対象」の群 | 3.4・4.4・4.7・4.14 | 同上 |
   | §6 | `LLD-analyze_terrain_window` | 「窓と省略」の群 | 3.4・4.4・4.14 | 同上 |
   | §6 | `LLD-analyze_terrain_grid` | 「タイルとグリッド」の群 | 3.4・4.2・4.3・4.4・4.14・4.16 | 同上 |
   | §6 | `LLD-analyze_terrain_image` | 「標高地形図」の群 | 3.4・4.15 | 同上 |
   | §6 | `LLD-analyze_terrain_scan` | 「走査」の群 | 3.4・4.5・4.6 | 同上 |
   | §6 | `LLD-analyze_terrain_csv` | 「CSV と早期終了」の群 | 3.4・4.7・4.14・4.16 | 同上 |
   | §6 | `LLD-analyze_terrain_zone` | 「ゾーン」の群 | 3.4・4.16 | 同上 |
   | §6 | `LLD-analyze_terrain_record` | 「出力の記録」の群 | 3.4・4.4・4.14 | 同上 |
   | §6 | `LLD-analyze_terrain_convert` | 「変換」の群 | 3.4・4.7 | 同上 |
   | §6 | `LLD-analyze_terrain_stage` | 「段の進行」の群 | 3.4・4.4・4.14 | 同上 |
   | §6 | `LLD-analyze_terrain_common` | 「3.9 と同じ決まり」の群 | 3.4・3.9 | 同上 |
   | §7 | `LLD-cmp5_common` | 3.5.4 のコンポーネント内の共通部品 | 3.5・4.8・4.9・4.18 | `scripts/` の下の Python のファイル（名前は LLD で決める） |
   | §7 | `LLD-merge_peaks` | `merge_peaks` | 3.5・4.8 | `scripts/merge_peaks.py` |
   | §7 | `LLD-merge_zones` | `merge_zones` | 3.5・4.18 | `scripts/merge_zones.py` |
   | §7 | `LLD-check_cols` | `check_cols` | 3.5・4.22 | `scripts/check_cols.py` |
   | §7 | `LLD-match_summits` | `match_summits` | 3.5・4.9 | `scripts/match_summits.py` |
   | §8 | `LLD-generate_viewer` | `generate_viewer` | 3.6・4.13 | `scripts/generate_viewer.py` |
   | §9 | `LLD-index_calc` | `index.html` の「計算」 | 3.7・3.8・4.11・4.12・4.19・4.20・4.21 | `public/index.html` |
   | §9 | `LLD-index_screen` | `index.html` の「画面」 | 3.7・3.8・4.13・4.19・4.20 | `public/index.html` |
   | §10 | `LLD-build_public_site` | `build_public_site` | 3.8・4.20 | `scripts/build_public_site.sh` |

   パスは、HLD の第 3 章の各節の「プログラム」の表の起動のしかたと [HLD 2.6.4](../30_HLD.md#264-ディレクトリ構成) の置き場から取る。名前を HLD で決めていないファイル（共通部品と CMP4 の C++ のファイル）は、置き場だけを決め、名前は LLD で決める。1 つのファイルを 2 つのモジュールが受け持つとき（`public/index.html`）は、両方の「ファイル」に同じパスを書く。
6. **HLD 第 5 章の受け手**: NFR 設計の 11 節は、次のモジュールの「対応 HLD」に並べて受ける（T3 の被覆に数えるのはモジュールの宣言だけなので、横断の節には並べない）。決まりの中身が 2 つ以上のモジュールにまたがるものは、§2 の横断の節に書き、受け手のモジュールの節から指す。

   | HLD の節 | 受けるモジュール | 横断の節で書くこと |
   |---|---|---|
   | [5.1](../30_HLD.md#51-nfr-001-精度検出網羅性) 精度・検出網羅性 | `LLD-analyze_terrain_grid`・`LLD-analyze_terrain_scan`・`LLD-merge_peaks` | なし |
   | [5.2](../30_HLD.md#52-nfr-002-メモリ使用量) メモリ使用量 | `LLD-analyze_terrain_grid`・`LLD-analyze_terrain_scan`・`LLD-cmp5_common`・`LLD-index_screen` | なし |
   | [5.3](../30_HLD.md#53-nfr-003-再現性決定論的出力) 再現性（決定論的出力） | `LLD-preprocess_boundaries`・`LLD-analyze_terrain_csv`・`LLD-merge_peaks`・`LLD-index_calc` | 言語ごとに別に実装する式のテストベクトル |
   | [5.4](../30_HLD.md#54-nfr-004-アクセスマナー) アクセスマナー | `LLD-fetch_tiles` | なし |
   | [5.5](../30_HLD.md#55-nfr-005-処理時間目標) 処理時間目標 | `LLD-fetch_tiles`・`LLD-analyze_terrain_stage`・`LLD-merge_peaks`・`LLD-generate_viewer` | なし |
   | [5.6](../30_HLD.md#56-nfr-006-可搬性環境) 可搬性・環境 | `LLD-common`・`LLD-run_pipeline` | なし |
   | [5.7](../30_HLD.md#57-nfr-007-ログ出力) ログ出力 | `LLD-common`・`LLD-run_pipeline`・`LLD-analyze_terrain_common` | ログとメッセージの文面の決まり |
   | [5.8](../30_HLD.md#58-nfr-008-ui-レスポンス) UI レスポンス | `LLD-index_screen` | なし |
   | [5.9](../30_HLD.md#59-nfr-009-観測可能性中間成果物の可視化) 観測可能性（中間成果物の可視化） | `LLD-analyze_terrain_image`・`LLD-analyze_terrain_zone`・`LLD-merge_zones` | なし |
   | [5.10](../30_HLD.md#510-nfr-010-描画応答性連続操作の滑らかさ) 描画応答性・連続操作の滑らかさ | `LLD-index_screen` | なし |
   | [5.11](../30_HLD.md#511-nfr-011-手順文書による環境構築成果物生成の完遂性) 手順文書による環境構築・成果物生成の完遂性 | `LLD-common`・`LLD-run_pipeline` | ログとメッセージの文面の決まり（利用者に案内を示すメッセージ） |

   受け手を変えるときは、本 ADR に追記する。
7. **送った項目の受け皿**: HLD の「対象外」の行で送り先が LLD の項目（[付録 B](ADR-HLD-008-remove-hld-open-items-subsections.md#付録-b-旧番号の対応表) の送り先が LLD の行は、HLD のこの行に移っている。今の文面は HLD を正とする）は、1 つのプログラムだけにかかるものはそのモジュールの節の該当の小節に、2 つ以上の節で同じ種類のものは §2 の横断の節に置く。[#202](https://github.com/jj1xgo/findsummits/issues/202) の UT の候補は、該当するモジュールの節の「UT 候補」の小節に割り当てる。IT の候補は、結合テスト仕様書（`60_IT.md`）のつなぎ目のケースに割り当てる。
8. **UT の仕様書**: 単体テスト仕様書（`docs/50_UT.md`）は LLD の段で作る（[テスト方針書 §2](../02_test_policy.md#2-テストレベル定義と役割分担)）。章立ては LLD の §2 以降のモジュールの並びにそろえ、各モジュールの「UT 候補」の小節からケースを起こす。[ADR-IT-001](ADR-IT-001-two-part-it-and-moved-st-cases.md) の Decision 3 が `60_IT.md` の §5 の対応表に「UT（`50_UT.md` で作る）」と書いた行は、`50_UT.md` を作るときに UT のケース ID に置き換える。
9. **「ファイル」のパスの実在の検査の時期**: `tools/lint_trace.py` の T2 のうち、LLD の「ファイル」に書いたパスが git にあるかの検査は、LLD がフェーズゲートを通った後（ゲート 4〈LLD → COD〉で LLD を `CONFIRMED_STAGES` に入れた後。COD の段に入った後）だけ効かせる。段の判定は、ほかの段で効く検査（T3・T5、[ADR-HLD-001](ADR-HLD-001-program-structure-chapter-and-two-tier-it.md) の Decision 5 の LLD の T3、IT の確定後の T3）と同じく `CONFIRMED_STAGES` で行う。それまでも、「ファイル」の宣言が無い・コード表記のパスが無いことは T1 が止める。

## Alternatives

- 関数を 1 モジュールとする: HLD 第 3 章の関数の数だけ節ができ（`index.html` だけで 70 を超える）、型やデータの持ち方のように関数にまたがる細部の置き場が無い。却下。
- ファイルを 1 モジュールとする: ファイルの名前は LLD で決めるもので、書き始めに単位が決まらない。`public/index.html` は 1 ファイルなので、性質の違う計算と画面が 1 節にまとまる。却下。
- CMP4 もプログラム単位（1 モジュール）にする: 関数が 40 を超える 1 節になり、UT のケース ID が 1 つのモジュール名に集まる。群は HLD 3.4.3 で既に決まっている。却下。
- `index.html` を 1 モジュールにする: 計算は Node.js で自動の UT を行い、画面は手動で確かめる（HLD 3.7.3）。UT の書き方が違うものが 1 節にまとまる。却下。
- LLD の章を FR/NFR の順にする: プログラムの中の関数が複数の章に散り、「ファイル」の割り付けと UT の単位がずれる。HLD は処理の正本を第 4 章・第 5 章に置き、第 3 章でプログラムに割り付けたので、LLD はプログラムの側から書く。却下。
- 第 5 章の受け手を §2 の横断の節にし、横断の節にも追跡の宣言を置く: 横断の節はファイルに割り付ける単位ではなく、「ファイル」に何を書くかが決まらない（すべてのファイルを並べることになる）。却下。
- 「ファイル」のパスの実在の検査を `EXEMPTIONS` で外す: `EXEMPTIONS` は構造上の例外を指摘の 1 件ごとに外すもので、モジュールが増えるたびに項目を足し、COD の段で 1 件ずつ消すことになる。外す理由は個々の指摘ではなく段にあるので、段で効かせる。却下。
- 「ファイル」に今のプロトタイプのパスを書き、COD の段で HLD の名前に書き換える: LLD の確定の後に宣言を書き換えることになり、HLD の名前と LLD の宣言がそろわない期間ができる。却下。
- 段の判定に `COD` を `CONFIRMED_STAGES` に足す: `CONFIRMED_STAGES` はフェーズゲートを通った文書の段で、COD には対応する文書が無い（`STAGE_DOCS` に無い段は T1 が止める）。ゲート 4 で LLD を入れることが COD の段に入ることに当たるので、LLD で判定する。却下。

## Consequences

- `docs/40_LLD.md` は、ゲート 3 の判定の後に、本 ADR の章立てと書き始めのモジュールの一覧で書き始める。本 ADR の状態は、LLD の全モジュールの節がそろったときに「採用・実装済み」にする。
- `tools/lint_trace.py` は、LLD の「ファイル」のパスの実在の検査を `'LLD' in confirmed` のときだけ行うように改めた（2026-10-14。[開発ガイド 6.2](../03_development.md#62-検査) の T2 の行）。ゲート 4 で LLD を `CONFIRMED_STAGES` に入れると、この検査と T3・T5 が一緒に効き始める。それまでに、コードを HLD の名前にそろえる作業（COD の段の最初の作業）の段取りを決めておく。
- `public/index.html` は `tools/lint_trace.py` の製品のコードの対象（`src/`・`scripts/` の `.c`・`.h`・`.cpp`・`.hpp`・`.py`・`.sh`）に入っていない。`LLD-index_calc`・`LLD-index_screen` の「ファイル」に書くと、LLD の確定後に T5 が止める。ゲート 4 までに、T5 の対象に `public/index.html` を足すか、本 ADR に扱いを追記する。
- [開発ガイド 6.1](../03_development.md#61-宣言と追跡マトリクス) が「LLD を作るときに検査に足す」とした LLD 末尾の表は、LLD を作るときに置くかどうかと形を決める。
- 横断の節は「対象外」の行で繰り返し出る種類の数だけ増やしてよい。増やすときは本 ADR に追記しない（受け手の表を変えるときだけ追記する）。
- [文書管理ルール「追跡の宣言」](../CLAUDE.md#追跡の宣言)の LLD の書式は変えない。
