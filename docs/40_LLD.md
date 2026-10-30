# findsummits - 詳細設計書 (LLD)

| 項目 | 内容 |
|---|---|
| 作成日 | 2026-10-18 |
| 最終更新日 | 2026-10-30 |
| ステータス | ドラフト |
| 参照 HLD | [`30_HLD.md`](30_HLD.md) |

---

**読み方**: この文書は詳細設計書（LLD）である。概要設計書（HLD）が決めたプログラムと関数の名前、受け取るもの、返すものの上に、関数ごとの細部（型、内部のデータの持ち方、メッセージの文面、ファイルへの割り付け）を足す（書き分けは[文書管理ルール](CLAUDE.md#hld-と-lld-の書き分け)）。LLD の次は実装フェーズ（COD）と単体テスト（UT）で、LLD の字句と上位の文書だけで、コードと単体テストのコードを書ける細かさにすることを目標にする（2026-10-18 に持ち主が決めた）。コードを書く側は、LLD に加えて、ユーザー要件定義書（URD）、ソフトウェア要件仕様書（SRS）、HLD と、関連する文書を読める前提にする。上位の文書に決まっていることは写さずにリンクで指し、どの文書にも決まっていないことをこの文書で決め切る。章立てとモジュールの単位は、アーキテクチャ決定記録（ADR）の [ADR-LLD-001](decisions/ADR-LLD-001-lld-format-module-granularity-and-t2-timing.md) による。今は 2.1 共通部品と 3.1 `preprocess_boundaries`（行政区域前処理）と 4.1 `fetch_tiles`（タイル取得）と 5.1 `run_pipeline`（パイプライン制御）と 5.2 `resolve_config`（設定解決）と 6.1 `analyze_terrain_launch`（地形解析エンジンの起動）と 6.2 `analyze_terrain_target`（地形解析エンジンの対象）と 6.3 `analyze_terrain_window`（地形解析エンジンの窓と省略）と 6.4 `analyze_terrain_grid`（地形解析エンジンのタイルとグリッド）と 6.5 `analyze_terrain_image`（地形解析エンジンの標高地形図）と 6.6 `analyze_terrain_scan`（地形解析エンジンの走査）と 6.7 `analyze_terrain_csv`（地形解析エンジンの CSV と早期終了）と 6.8 `analyze_terrain_zone`（地形解析エンジンのゾーン）と 6.9 `analyze_terrain_record`（地形解析エンジンの出力の記録）と 6.10 `analyze_terrain_convert`（地形解析エンジンの変換）と 6.12 `analyze_terrain_common`（地形解析エンジンの共通部品）と、それらが使う分の 1 章と 2.2〜2.5 だけを書いてある。ほかのモジュールの節は、書くときに足す。

## 目次

- [1. 用語定義と規約](#1-用語定義と規約)
  - [1.1 用語定義](#11-用語定義)
  - [1.2 LLD の規約](#12-lld-の規約)
- [2. 共通部品と横断](#2-共通部品と横断)
  - [2.1 共通部品](#21-共通部品)
    - [2.1.1 ファイル割付](#211-ファイル割付)
    - [2.1.2 型とデータ](#212-型とデータ)
    - [2.1.3 関数の細部](#213-関数の細部)
    - [2.1.4 メッセージ文面](#214-メッセージ文面)
    - [2.1.5 UT 候補](#215-ut-候補)
  - [2.2 ログとメッセージの文面](#22-ログとメッセージの文面)
  - [2.3 ファイルの名前と書き方](#23-ファイルの名前と書き方)
  - [2.4 言語ごとに別に実装する式のテストベクトル](#24-言語ごとに別に実装する式のテストベクトル)
  - [2.5 ビルドとテストの名前](#25-ビルドとテストの名前)
- [3. CMP1 行政区域前処理](#3-cmp1-行政区域前処理)
  - [3.1 `preprocess_boundaries`](#31-preprocess_boundaries)
    - [3.1.1 ファイル割付](#311-ファイル割付)
    - [3.1.2 型とデータ](#312-型とデータ)
    - [3.1.3 関数の細部](#313-関数の細部)
    - [3.1.4 メッセージ文面](#314-メッセージ文面)
    - [3.1.5 UT 候補](#315-ut-候補)
- [4. CMP2 タイル取得](#4-cmp2-タイル取得)
  - [4.1 `fetch_tiles`](#41-fetch_tiles)
    - [4.1.1 ファイル割付](#411-ファイル割付)
    - [4.1.2 型とデータ](#412-型とデータ)
    - [4.1.3 関数の細部](#413-関数の細部)
    - [4.1.4 メッセージ文面](#414-メッセージ文面)
    - [4.1.5 UT 候補](#415-ut-候補)
- [5. CMP3 パイプライン制御](#5-cmp3-パイプライン制御)
  - [5.1 `run_pipeline`](#51-run_pipeline)
    - [5.1.1 ファイル割付](#511-ファイル割付)
    - [5.1.2 型とデータ](#512-型とデータ)
    - [5.1.3 関数の細部](#513-関数の細部)
    - [5.1.4 メッセージ文面](#514-メッセージ文面)
    - [5.1.5 UT 候補](#515-ut-候補)
  - [5.2 `resolve_config`](#52-resolve_config)
    - [5.2.1 ファイル割付](#521-ファイル割付)
    - [5.2.2 型とデータ](#522-型とデータ)
    - [5.2.3 関数の細部](#523-関数の細部)
    - [5.2.4 メッセージ文面](#524-メッセージ文面)
    - [5.2.5 UT 候補](#525-ut-候補)
- [6. CMP4 地形解析エンジン](#6-cmp4-地形解析エンジン)
  - [6.1 `analyze_terrain_launch`](#61-analyze_terrain_launch)
    - [6.1.1 ファイル割付](#611-ファイル割付)
    - [6.1.2 型とデータ](#612-型とデータ)
    - [6.1.3 関数の細部](#613-関数の細部)
    - [6.1.4 メッセージ文面](#614-メッセージ文面)
    - [6.1.5 UT 候補](#615-ut-候補)
  - [6.2 `analyze_terrain_target`](#62-analyze_terrain_target)
    - [6.2.1 ファイル割付](#621-ファイル割付)
    - [6.2.2 型とデータ](#622-型とデータ)
    - [6.2.3 関数の細部](#623-関数の細部)
    - [6.2.4 メッセージ文面](#624-メッセージ文面)
    - [6.2.5 UT 候補](#625-ut-候補)
  - [6.3 `analyze_terrain_window`](#63-analyze_terrain_window)
    - [6.3.1 ファイル割付](#631-ファイル割付)
    - [6.3.2 型とデータ](#632-型とデータ)
    - [6.3.3 関数の細部](#633-関数の細部)
    - [6.3.4 メッセージ文面](#634-メッセージ文面)
    - [6.3.5 UT 候補](#635-ut-候補)
  - [6.4 `analyze_terrain_grid`](#64-analyze_terrain_grid)
    - [6.4.1 ファイル割付](#641-ファイル割付)
    - [6.4.2 型とデータ](#642-型とデータ)
    - [6.4.3 関数の細部](#643-関数の細部)
    - [6.4.4 メッセージ文面](#644-メッセージ文面)
    - [6.4.5 UT 候補](#645-ut-候補)
  - [6.5 `analyze_terrain_image`](#65-analyze_terrain_image)
    - [6.5.1 ファイル割付](#651-ファイル割付)
    - [6.5.2 型とデータ](#652-型とデータ)
    - [6.5.3 関数の細部](#653-関数の細部)
    - [6.5.4 メッセージ文面](#654-メッセージ文面)
    - [6.5.5 UT 候補](#655-ut-候補)
  - [6.6 `analyze_terrain_scan`](#66-analyze_terrain_scan)
    - [6.6.1 ファイル割付](#661-ファイル割付)
    - [6.6.2 型とデータ](#662-型とデータ)
    - [6.6.3 関数の細部](#663-関数の細部)
    - [6.6.4 メッセージ文面](#664-メッセージ文面)
    - [6.6.5 UT 候補](#665-ut-候補)
  - [6.7 `analyze_terrain_csv`](#67-analyze_terrain_csv)
    - [6.7.1 ファイル割付](#671-ファイル割付)
    - [6.7.2 型とデータ](#672-型とデータ)
    - [6.7.3 関数の細部](#673-関数の細部)
    - [6.7.4 メッセージ文面](#674-メッセージ文面)
    - [6.7.5 UT 候補](#675-ut-候補)
  - [6.8 `analyze_terrain_zone`](#68-analyze_terrain_zone)
    - [6.8.1 ファイル割付](#681-ファイル割付)
    - [6.8.2 型とデータ](#682-型とデータ)
    - [6.8.3 関数の細部](#683-関数の細部)
    - [6.8.4 メッセージ文面](#684-メッセージ文面)
    - [6.8.5 UT 候補](#685-ut-候補)
  - [6.9 `analyze_terrain_record`](#69-analyze_terrain_record)
    - [6.9.1 ファイル割付](#691-ファイル割付)
    - [6.9.2 型とデータ](#692-型とデータ)
    - [6.9.3 関数の細部](#693-関数の細部)
    - [6.9.4 メッセージ文面](#694-メッセージ文面)
    - [6.9.5 UT 候補](#695-ut-候補)
  - [6.10 `analyze_terrain_convert`](#610-analyze_terrain_convert)
    - [6.10.1 ファイル割付](#6101-ファイル割付)
    - [6.10.2 型とデータ](#6102-型とデータ)
    - [6.10.3 関数の細部](#6103-関数の細部)
    - [6.10.4 メッセージ文面](#6104-メッセージ文面)
    - [6.10.5 UT 候補](#6105-ut-候補)
  - [6.12 `analyze_terrain_common`](#612-analyze_terrain_common)
    - [6.12.1 ファイル割付](#6121-ファイル割付)
    - [6.12.2 型とデータ](#6122-型とデータ)
    - [6.12.3 関数の細部](#6123-関数の細部)
    - [6.12.4 メッセージ文面](#6124-メッセージ文面)
    - [6.12.5 UT 候補](#6125-ut-候補)

## 1. 用語定義と規約

### 1.1 用語定義

| 用語 | 意味 |
|---|---|
| モジュール | [ADR-LLD-001](decisions/ADR-LLD-001-lld-format-module-granularity-and-t2-timing.md) の Decision 3 の単位。この文書の節 1 つに当たる。 |
| 横断の節 | 2 つ以上のモジュールにかかる決まりを置く節（2.2〜2.4）。追跡の宣言を持たず、モジュールの節から指される。 |
| 部品 | [HLD 3.9](30_HLD.md#39-共通部品) の共通部品の表の 1 行（`load_config` など）。 |
| 起動の部分 | Python のプログラムの `if __name__ == '__main__':` の中。HLD 第 3 章の「引数の解析はプログラムの起動の部分が行い」の部分。 |
| 内部の関数 | モジュールの中だけで呼ぶ関数。名前を `_` で始める。 |
| 本体 | bash のプログラムの、関数の定義の外にある文（ファイルの末尾に置く）。[HLD 3.3.3](30_HLD.md#333-関数)の「プログラムの本体（関数の外）」の部分。 |

### 1.2 LLD の規約

- 追跡の宣言は、文書管理ルールの[追跡の宣言](CLAUDE.md#追跡の宣言)のとおり、モジュールの見出しの直下に置く。小節は「ファイル割付」「型とデータ」「関数の細部」「メッセージ文面」「UT 候補」の 5 つをこの順に置き、書くことが無い小節も「なし」と理由を書いて残す（ADR-LLD-001 の Decision 2）。
- 横断の節の決まりに従うところは、その節へのリンクで指し、写さない。
- 関数の名前は HLD 第 3 章の名前を使う。LLD が足してよい名前は、内部の関数（`_` で始め、ほかのモジュールから呼ばない）と、型・定数・例外の名前だけ。ほかのモジュールから呼ぶ関数を足すときは、HLD 第 3 章を先に直す（文書管理ルールの[HLD と LLD の書き分け](CLAUDE.md#hld-と-lld-の書き分け)）。
- 型は、そのモジュールの言語の書き方で書く（Python は型ヒント。例 `set[str]`。C++ は宣言の形。例 `std::set<std::string>`）。
- Python のプログラム（2.1 の内部の関数を除く）は、`sys.exit(<終了コード>)` を `sys` の属性として呼ぶか、最後まで進んで終わる。`raise SystemExit`・`os._exit`・組み込みの `exit()`・`quit()`・`from sys import exit` を書かない。`except BaseException`、裸の `except:`、`SystemExit`・`LogWriteError`・`SignalStop` を捕まえる `except` を書かない（2.1 の `start_log` が `sys.exit` の差し替えで終了コードを記録し、ログの書き込みの失敗とシグナルを `BaseException` の子の例外で伝えるため）。後始末と結果の要約は `finally` で書く（書き方の型は [2.1.3](#213-関数の細部) の前置き）。`os._exit` を呼ぶのは 2.1 の内部の関数 `_finish_log` だけ。
- CMP4（地形解析エンジン）の C++ の規約（[6](#6-cmp4-地形解析エンジン) のモジュールが従う）:
  - ファイル: 群ごとのモジュールは `src/<群の名前>.hpp` と `src/<群の名前>.cpp` の 2 本（`<群の名前>` はモジュールの ID の `LLD-analyze_terrain_` の後の部分。6.12 は `src/common.hpp`・`src/common.cpp`。6.5 だけは、この 2 本に gist_earth の表のファイル `src/image_gist_earth.hpp` を足した 3 本〈[6.5.1](#651-ファイル割付)〉）。`main` は [6.1](#61-analyze_terrain_launch) の `src/analyze_terrain.cpp` に置く（6.1 だけは、この 2 本に `main` のファイルを足した 3 本）。UT のコードは `tests/src/test_<群の名前>.cpp`（[HLD 2.6.4](30_HLD.md#264-ディレクトリ構成)の DEC18「テストは対象と同じ名前で分ける」）。どのファイルも先頭のコメントに `// trace: LLD-analyze_terrain_<群の名前>` を書き、テストの各ケースには `// trace: UT-analyze_terrain_<群の名前>-NN` を書く。ヘッダーは、先頭の trace のコメントの次の行を `#pragma once` にする。
  - 名前: ほかのモジュールから使う名前（HLD 3.4.3 の関数、LLD が足す型・定数・例外）はヘッダーに宣言し、名前空間に入れない。内部の関数と状態は `.cpp` の無名の名前空間に置き、名前を `_` と英小文字で始める（`_` で始まる名前はグローバルの名前空間では予約されているので、無名の名前空間の外に置かない。`_` と英大文字で始まる名前と、`__` を含む名前は、どこにも使わない）。型は `PascalCase`、関数と変数は `snake_case`、定数は HLD の名前（`EXIT_OK` など）。
  - 使う機能: [ADR-SRS-010](decisions/ADR-SRS-010-cpp-opencv-migration.md) の「C++ 利用の方針」のとおり。標準ライブラリの型（`std::string`・`std::vector`・`std::set`・`std::map`・`std::chrono`）は使ってよい。`std::variant`・`std::any` は使わない。`std::optional` も使わない（値の有無は `bool` の印で持つ）。
  - 止まり方（[HLD 3.4.3](30_HLD.md#343-関数) の「止まり方は LLD で決める」）: 止まるときは、メッセージを `log_error` で出してから `throw ExitRequest(<終了コード>)` する（`ExitRequest` は 6.12 の型）。プログラム（`src/`）で `std::exit`・`exit`・`_Exit`・`_exit`・`quick_exit`・`abort` を呼ぶのは 6.12 の内部の関数だけ。`ExitRequest` を捕まえるのは `main` の最上位だけで、`catch (...)` は後始末をしてから `throw;` で投げ直す（握りつぶさない）。`main` は、最後まで進んだら `EXIT_OK` を返し、`ExitRequest` を捕まえたらその `code` を返す（それ以外の値を返さない。終わりの行の終了コードを `ExitRequest` が記録するため。6.12 の `ExitRequest`）。ただし、`start_log` の前に誤りのメッセージを画面に書けずに `std::system_error` が出たときは `EXIT_USAGE` を返す（[6.1](#61-analyze_terrain_launch) の `main`。`start_log` の前は終わりの行が無い）。`ExitRequest` は `std::exception` の子にしない（呼ぶ側の `catch (const std::exception&)` に捕まらないようにする。Python の `SignalStop`・`LogWriteError` を `BaseException` の子にしたのと同じ理由）。ADR-SRS-010 が採らないとした独自の例外の「階層」（継承で分けた複数の型）には当たらない。
  - 結果の要約（[HLD 5.7.2](30_HLD.md#572-処理の流れ)の 7「結果の要約」）: 要約を出す関数は、次の形で書く（中身は各モジュールの節で決める）。

    ```cpp
    try {
        // 処理（途中で止まるときは throw ExitRequest(...)）
    } catch (...) {
        log_info("<途中で止まったことが分かる要約>");
        throw;
    }
    log_info("<要約>");
    ```

  - シグナル: シグナルのハンドラを付けるのは 6.12 の `start_log` だけで、ほかのモジュールは `signal`・`sigaction` を呼ばない。時間のかかる処理は、区切りで `check_signal()` を呼ぶ（区切りの置き場と遅れの上限は各モジュールの節で決める）。
  - 出力: 標準出力・標準エラー出力・ログファイルへの出力は、6.12 の `log_info`・`log_warning`・`log_error` だけで行う（`std::cout`・`std::cerr`・`printf`・`puts` を使わない。6.12 は出力を `write` で直接書くので、標準入出力のバッファと混ぜると順が崩れる）。
  - `{reason}`: ファイルの読み書きの失敗の理由は、失敗した POSIX の呼び出しの `errno` を `std::strerror` に渡した文（Python の `OSError` の `strerror` と同じ文）。
  - ビルドと警告: ビルドとテストの名前は [2.5](#25-ビルドとテストの名前)。警告はゼロにする（[HLD 2.6.5](30_HLD.md#265-ビルド構成)の DEC23「警告はゼロにするがビルドは止めない」）。
- 利用者向けの Python のコマンド（[3.1](#31-preprocess_boundaries) の `preprocess_boundaries`・[4.1](#41-fetch_tiles) の `fetch_tiles`）は、起動の部分の内部の関数 `_parse_args` で引数を読み、bash の `run_pipeline`（[5.1.3](#513-関数の細部)の `parse_args`）と同じ受け方にする: 引数を左から 1 つずつ読む。値をとる名前は、次の引数（`--config a.ini`）か、名前の後の `=` の後（`--config=a.ini`。最初の `=` で分ける）で値を受け取り、次の引数で受け取る値は `-` で始まっていてもそのまま値にする。受け付けない引数（`--` で始まらない引数、知らない名前、値をとらない名前に `=` を付けたもの〈`--help=x`〉、`--` だけ）、値をとる名前が最後にあって値が無いこと、同じ名前を 2 回渡すこと（`--help` を除く。名前を読んだ時点で、値を受け取るより先に見る）は、その場で終了コード 2 で止める。名前の省略（`--conf`）は受けない。`--help` を読んだら、それより後の引数を読まずに、使い方の文を標準出力に出して終了コード 0 で終わる（設定を読まず、ロックを掛けない。[HLD 2.9.3](30_HLD.md#293-同時起動の排他)）。`--help` より前の引数の誤りは、先に止まる。`argparse` は使わない（名前の省略を受け、誤りのメッセージが [2.2](#22-ログとメッセージの文面) の書き方にならないため）。メッセージの文面と使い方の文は、モジュールの節に置く。3.1 と 4.1 が共有する規約なので、横断の決まりとしてここに置く。
- 2.1 の `start_log`・`log_info`・`log_warning`・`log_error` は、メインのスレッドからだけ呼ぶ（`start_log` はシグナルのハンドラを付けるのに `signal.signal` を使い、これはメインのスレッドでしか呼べない）。ほかのスレッドで動く処理は、知らせたいことをメインのスレッドに返し、メインのスレッドが出す（行が混ざらないようにし、ログの書き込みの失敗とシグナルをメインのスレッドで受けるため）。スレッドを使うかと、シグナルで止まるときにスレッドをどう終えるかは、使うモジュールの節で決める（CMP2（タイル取得）の並列取得の形は [4.1.3](#413-関数の細部) の前置きで決めた。[HLD 2.9.1](30_HLD.md#291-目的と範囲) の対象外の行で LLD に送られていた）。
- LLD の記号（メッセージの記号など）は、`tools/lint_docs.py` の検査 H（1 文字の記号の残り。`C1`〜`C8`・`D` と数字・`K1`〜`K6`。コード表記の中は検査しない）に当たらない名前にする。2.1 と 2.2 の記号は、設定の誤り CF1〜CF7、`--mesh` の誤り A1〜A5、メッシュのリストの誤り R1〜R3、共通の場面 G1〜G7、ログファイルの行 L1〜L3、設定の相互制約 CX1、取得完了の記録の誤り FC2（4.1 と 5.1 が出す）である。5.2 の記号は、引数の誤り RA1・RA2、パスの改行 RP1、標準出力に書けないとき RW1 である。5.1 の記号は、引数の誤り PA1〜PA5、設定解決の出力の誤り RS1、起動前提条件の不足 PC1・PC2、取得完了の記録の不足 FC1（FC2 は 2.2）、前回の出力を消せないとき CO1、単独起動の案内 PG1〜PG3、ログの行 PL1〜PL9 である。2.1.3 のメッシュの読み方のテストベクトルの ID は MV-01〜MV-21、設定ファイルの書式のテストベクトルの ID は CV-01〜CV-27 である。3.1 の記号は、引数の誤り BA1〜BA4、N03 行政区域 ZIP が無いか探せない BZ1・BZ2、入力の検証 BV1〜BV8、生成と書き込みと置き換えの失敗 BF1〜BF4、新しい版の警告 BW1、ログの行 BL1〜BL5 である。4.1 の記号は、引数の誤り TA1〜TA4、起動前提条件の不足 TP1〜TP3、`--mesh` のコードを飛ばすときと版を取れないときの警告 TW1〜TW3、取得を止める応答 TG1・TG2、DEM10b がすべて未整備のメッシュ TD1、ファイルの書き込みと削除の失敗 TF1〜TF3、ログの行 TL1〜TL6、2.4 の取得範囲のテストベクトルの表 4 である。6.1 の記号は、引数の誤り LA1〜LA8 である。6.2 の記号は、`--mesh` のコードを飛ばすときの警告 TM1・TM2、対象にしなかった北方領土除外メッシュのログの行 TM3、コル未確定ピーク座標リストを読めないときと書式が違うとき UP1・UP2、対象ピークの所属メッシュが解析の対象でないとき UP3 である。6.3 の記号は、省略の判定に使う `.meshset` を読めないとき・書式が違うとき・置き場を読めないとき MS1〜MS3、タイルが 1 枚も無いメッシュがあるとき TT1、DEM10b のタイルの欠けが 1% を超える解析対象メッシュがあるとき TT2、パターンを省略したログの行 WN1 である。6.4 の記号は、読めない標高タイルがあるとき TR1 と、2.4 の bounding box の取得範囲のテストベクトルの表 8 である。6.5 の記号は、グリッドに陸地の画素が無いとき IM1、標高地形図を書けないとき IW1 である。6.6 はメッセージの記号を持たない（メッセージを出さない）。6.7 の記号は、per-mesh CSV を書けないとき CW1、早期終了の判定に読み戻す per-mesh CSV を読めないとき・書式が違うとき RB1・RB2 である。6.8 の記号は、per-mesh ピーク候補 GeoJSON を書けないとき ZW1 である。6.9 の記号は、`.meshset` を書けないとき MW1 である。6.10 はメッセージの記号を持たない（2.4 の変換のテストベクトルの表 5〜7 を使う）。6.12 は新しいメッセージの記号を持たない（2.1・2.2 の記号を使う）。
- メッセージの文面は、[2.2](#22-ログとメッセージの文面) の書き方で、置き換える部分を `{名前}` で書く。
- UT 候補は、`ID`・確かめること・準備・入力・期待 の 5 列の表で、`UT-<モジュール名>-NN`（2 桁の連番。[テスト方針書 §6](02_test_policy.md#6-テストケースid命名の大枠)）ごとに 1 行で書く。準備には、入力を与える前に整えること（置くファイル、起こすプロセス、差し替えるもの、捕まえる出力）を書く。小節の前置きに名前を付けて書いた共通の準備で足りるときは、その名前を書き、ケースに固有の準備だけを足す。手動のケースは ID の直後に `（手動）` を付ける。単体テスト仕様書（`50_UT.md`）を作るときは、準備はケースの手順へ移る。
- 規則は、実装者が読むその関数の見出し（関数の細部の `#####` の見出し。群の見出しで分けたモジュールでは `######` の見出し）の下に置く。2 章の横断の節には、2 つ以上のモジュールで共有するものと、どのプログラムにも属さない項目（[ADR-LLD-001](decisions/ADR-LLD-001-lld-format-module-granularity-and-t2-timing.md) の Decision 7。Makefile のターゲット名など）だけを置き、関数の見出しの下からリンクで指す。横断の節にある規則に関数ごとの扱いがあれば、その関数の見出しの下にも書く（実装者は関数の見出しの下を読み、横断の節の段落の奥までは読まないことがあるため）。

## 2. 共通部品と横断

この章は、HLD 3.9 の共通部品のモジュール（2.1）と、HLD の「目的と範囲」の「対象外」の行で繰り返し出る項目を受ける横断の節（2.2〜2.4）を置く。横断の節は追跡の宣言を持たず、モジュールの節から指す（ADR-LLD-001 の Decision 1）。2.2〜2.5 は今は 2.1・3.1・4.1・5.1・5.2・6.1・6.2・6.3・6.4・6.5・6.6・6.7・6.8・6.9・6.10・6.12 が使う項目だけを書き、ほかのモジュールの節を書くときに足す。

### 2.1 共通部品

- **ID**: LLD-common
- **対応 HLD**: [3.9](30_HLD.md#39-共通部品)・[4.1](30_HLD.md#41-fr-001-標高タイル事前取得)・[4.4](30_HLD.md#44-fr-004-33メッシュ結合解析オーケストレーション)・[4.8](30_HLD.md#48-fr-008-per-mesh-csv-統合)・[4.17](30_HLD.md#417-fr-017-n03-行政区域前処理データ準備)・[5.6](30_HLD.md#56-nfr-006-可搬性環境)・[5.7](30_HLD.md#57-nfr-007-ログ出力)・[5.11](30_HLD.md#511-nfr-011-手順文書による環境構築成果物生成の完遂性)
- **ファイル**: `scripts/common.py`

各部品の処理の正本は、[HLD 3.9](30_HLD.md#39-共通部品) の表の「定義のある節」で、この節はそれを Python で書くための細部だけを足す。[5.6](30_HLD.md#56-nfr-006-可搬性環境)（可搬性）は、`fcntl` を使うので POSIX の OS だけで動くことと、ロックは `data_dir` がローカルのファイルシステムにある前提（[HLD 2.9.3](30_HLD.md#293-同時起動の排他)）で受ける。[5.11](30_HLD.md#511-nfr-011-手順文書による環境構築成果物生成の完遂性)（手順文書）は、どのメッセージにも `対処:` の行で次の操作を書くこと（[2.2](#22-ログとメッセージの文面)）で受ける。

#### 2.1.1 ファイル割付

- 部品はすべて `scripts/common.py` 1 本に置く。プログラムは `venv/bin/python3 scripts/<名前>.py` で起動され（HLD 第 3 章）、`scripts/` が import の探索先の先頭になるので、`import common` で読む。
- UT のコードは `tests/scripts/test_common.py` に置く（[HLD 2.6.4](30_HLD.md#264-ディレクトリ構成) の `tests/scripts/`、[DEC18](30_HLD.md#266-設計判断)「テストは対象と同じ名前で分ける」）。テストの枠組みは[テスト方針書 3.4](02_test_policy.md#34-テストを先に書く進め方)で選んだ（Python は標準の `unittest`）。UT のコードの各テストには、`# trace: <UT の ID>`（例 `# trace: UT-common-01`）のコメントを付ける（文書管理ルールの[追跡の宣言](CLAUDE.md#追跡の宣言)）。
- `scripts/common.py` の親の親をソースツリーの根とする。既定の設定ファイル `params/config.ini` とその見本 `params/config.ini.example` は、その下にある（[2.1.2](#212-型とデータ)の `DEFAULT_CONFIG_PATH`・`_EXAMPLE_CONFIG_PATH`）。

#### 2.1.2 型とデータ

- 終了コードの定数（モジュールの最上位の `int`）: `EXIT_OK = 0`・`EXIT_ERROR = 1`・`EXIT_USAGE = 2`・`EXIT_UNRESOLVED = 3`・`EXIT_DEFECT = 4`（[HLD 2.5.1](30_HLD.md#251-終了コード)）。
- ファイルの名前（モジュールの最上位の `str`。内部）: `_LOCK_NAME = 'findsummits.lock'`・`_FETCH_RECORD_NAME = 'fetch_complete.txt'`（[2.3](#23-ファイルの名前と書き方)。bash の `run_pipeline` の `LOCK_NAME`・`FETCH_RECORD_NAME`〈[5.1.2](#512-型とデータ)〉と同じ値）。
- ソースツリーのパス（モジュールの最上位の `str`）: `_SOURCE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))`（内部）、`DEFAULT_CONFIG_PATH = os.path.join(_SOURCE_ROOT, 'params', 'config.ini')`（公開。利用者向けの 2 本〈`preprocess_boundaries`・`fetch_tiles`〉は、`--config` を省いたときに `common.DEFAULT_CONFIG_PATH` を `load_config` に渡す。[HLD 3.1.1](30_HLD.md#311-プログラム)・[3.2.1](30_HLD.md#321-プログラム) の既定のパスの求め方を 1 か所にし、`load_config` の 2 の CF1 の既定の対処の判定と同じ値にするため。`scripts/common.py` は 2 本と同じ `scripts/` にあるので、HLD の「自分の置き場から求める」と同じ値になる）、`_EXAMPLE_CONFIG_PATH = os.path.join(_SOURCE_ROOT, 'params', 'config.ini.example')`（内部）。
- メッシュコード: `str` で、ASCII の数字 4 字（`re.fullmatch(r'[0-9]{4}', s)` に合うもの）。`int` にしない（`0123` のような 4 桁を書いたとおりに保ち、メッセージにそのまま出すため）。集合は `set[str]`。
- `@dataclass(frozen=True) class ConfigValue`: `value: int | str | None`（`None` は未設定。デフォルトの無いキー〈`user_agent_email`・`sota_geojson_version`〉が、必須でなく、書かれていないとき）、`from_file: bool`（ファイルに書いてあった値なら `True`、デフォルト値か未設定なら `False`）。
- `@dataclass(frozen=True) class Config`: `path: str`（設定ファイルの絶対パス。`os.path.abspath` したもの）、`values: dict[str, ConfigValue]`（キーの名前から値への対応。`load_config` に渡したキーだけ）。キーの名前は節をまたいで重ならない（[HLD 2.3.2](30_HLD.md#232-設定ファイル)の表）ので、キーの名前だけで引く。
- `@dataclass(frozen=True) class StartTime`: `wall: datetime`（`datetime.now().astimezone()`。時差付きのローカル時刻）、`mono: float`（`time.monotonic()`）。`@classmethod def now(cls) -> 'StartTime'` で両方を同時に取る。`start_log` を呼ぶ各プログラムは起動の部分の最初（設定と引数の検査の前。[HLD 5.7.2](30_HLD.md#572-処理の流れ) の 2「ファイルの名前」）に `StartTime.now()` を呼び、`start_log` に渡す。`start_log` を呼ばない `resolve_config`（[5.2](#52-resolve_config)）は呼ばない。所要時間は `mono` の差で測る（時刻の補正に左右されない時計。[HLD 5.7.1](30_HLD.md#571-目的と範囲) の対象外の行）。
- 例外: `class LogWriteError(BaseException)`（ログファイルに書けなくなった。[2.1.3](#213-関数の細部)の `log_info`・`log_warning`・`log_error`。属性 `path: str`）、`class SignalStop(BaseException)`（属性 `signum: int`。`SIGINT`・`SIGTERM` を受けた。`_on_signal`）。どちらも `Exception`・`OSError` ではなく `BaseException` の子にして、呼ぶ側の `except Exception`・`except OSError` に捕まらず、プログラムの最上位まで伝わるようにする（ログに書けなくなっても処理が続いて終了コード 0 で終わること、シグナルを受けても止まらないことを防ぐ）。
- 設定のキーの表 `_CONFIG_KEYS`（内部。表の順が設定値をログに書く順）。各行は節・キー・種類・デフォルト・許容範囲の文（メッセージの `{range}` に入れる文）。デフォルトの正本は[HLD 2.3.2](30_HLD.md#232-設定ファイル)の表、範囲の正本は[SRS 2.2.1](20_SRS.md#221-設定可能項目)で、ここはその Python での判定の仕方を決める。

  | 節 | キー | 種類と判定 | デフォルト | 許容範囲の文 |
  |---|---|---|---|---|
  | `paths` | `data_dir` | パス: 空でない文字列で、`os.path.isabs` が真 | なし（必須） | `絶対パス` |
  | `paths` | `log_dir` | パス: 同上 | `os.path.join(<data_dir の値>, 'logs')` | `絶対パス` |
  | `fetch` | `max_parallel` | 整数: 1 以上 16 以下 | `8` | `1 以上 16 以下の整数` |
  | `fetch` | `interval_ms` | 整数: 0 以上 5000 以下 | `0` | `0 以上 5000 以下の整数` |
  | `fetch` | `user_agent_email` | メール: 空でなく、`@` を含み、`str.isspace()` が真になる字と `(`・`)` を含まない | なし（`fetch_tiles` が必須に渡す） | `空でなく、@ を含み、空白と ( ) を含まない連絡先のメールアドレス` |
  | `analysis` | `prominence_primary_m` | 整数: 100 以上（最終フィルタ閾値未満かの相互制約は呼ぶ側。[HLD 3.9](30_HLD.md#39-共通部品) の表の後の段落） | `130` | `100 以上の整数（18 桁まで）` |
  | `analysis` | `activation_zone_drop_m` | 整数: 25 だけ | `25` | `25` |
  | `analysis` | `delete_zone_max_drop_m` | 整数: 200 以上 300 以下 | `250` | `200 以上 300 以下の整数` |
  | `merge` | `prominence_final_m` | 整数: 150 だけ | `150` | `150` |
  | `match` | `sota_geojson_version` | 整数: 1 以上 | なし（未設定のまま `None`） | `1 以上の整数（18 桁まで）` |
  | `match` | `provisional_code_max_prefix` | 英字: `re.fullmatch(r'[A-Z]', v)` | `'A'` | `A〜Z の英大文字 1 字` |
  | `match` | `unmatched_summit_threshold` | 整数: 0 以上 | `10` | `0 以上の整数（18 桁まで）` |

  整数の種類は、値が `re.fullmatch(r'[0-9]+', v)` に合い、先頭の `0` を除いた文字列 `d = v.lstrip('0') or '0'` の桁数（`len(d)`）が 18 以下のときだけ `int(d)` にする（`int(v)` にしない。先頭の `0` が 4300 個を超える値で `ValueError` になるため）。符号・小数点・全角の数字・空の値は型に合わず、19 桁以上は範囲の外とする。18 桁までにするのは、Python の `int` への変換の桁数の上限（既定 4300 桁）に掛からないようにし、CMP4（地形解析エンジン）の C++ の実装が 64 ビットの符号付き整数で持てるようにするため。上の表で上限の無い整数のキーの許容範囲の文に `（18 桁まで）` を付けるのはこのため。この上限は [SRS 2.2.1](20_SRS.md#221-設定可能項目) の「許容範囲に上限を書いていない整数の項目は、18 桁までとする」と [HLD 2.3.3](30_HLD.md#233-検証と記録) の検査に書いてある。値は 2.1.3 の設定ファイルの書式の 6 で前後の空白とタブを除いた文字列。空の値（`key =`）はどのキーでも型に合わない誤りで、「書いていない」とは扱わない（未設定にしたいときはキーの行を書かない）。

- 全キーの名前 `CONFIG_KEY_NAMES: tuple[str, ...]`（モジュールの最上位。公開）: `_CONFIG_KEYS` のキーの名前を表の順に並べたタプル。`_CONFIG_KEYS` から作り、名前を別に書かない。設定解決（[5.2](#52-resolve_config)）が全キーを `load_config` に渡すのに使う（[HLD 2.3.3](30_HLD.md#233-検証と記録)の「設定解決は、ファイルに書かれた全キーを検査する」。キーの一覧を 1 か所にし、HLD の表にキーが足されたときに設定解決の検査から漏れないようにするため）。

- モジュールの状態（内部。`_state` という 1 つの `@dataclass` のインスタンス）: `file`（ログファイルの `TextIO` か `None`）、`path`（ログファイルの絶対パスか `None`）、`program: str`、`start: StartTime | None`、`broken: bool`（ログファイルに書けなくなった）、`exit_code: int | None`（記録した終了コード）、`signum: int | None`（受けたシグナル。`_on_signal` の 1 回目で入れる）、`lock_fd: int | None`（ロックファイルの記述子。閉じないために持つ）。

#### 2.1.3 関数の細部

部品ごとに `#####` の見出し（`##### load_config` のように部品の名前だけ）を立てて書く。止まるときは、メッセージを出してから `sys.exit(<定数>)` を呼ぶ（`start_log` の終了コードの記録のため、`raise SystemExit` を書かない）。結果の要約（[HLD 5.7.2](30_HLD.md#572-処理の流れ) の 7「結果の要約」）は部品が止まるときも呼ぶ側が出す。呼ぶ側の書き方の型を、次のコードで示す（中身の要約の文面は各モジュールの節で決める）。`log_info` は、ログファイルに書けなくなった後は何も出さないので（下の `log_info`・`log_warning`・`log_error`）、その場面では要約が出ない（HLD 5.7.2 の 7「結果の要約」の「ログファイルに書けなくなって止まるときは出さない」）。`try` は `start_log` の後から始める（`load_config`・`read_mesh_arg`・`acquire_lock` のように `start_log` より前に呼ぶ部品で止まるときは、要約を出さない。`start_log` の前の `log_info` は画面に出るので、`try` の中に置くと要約が出てしまう。HLD 5.7.2 の 7「結果の要約」の「ログファイルを開く前に止まるとき」）。

```python
def main() -> None:
    start = common.StartTime.now()
    ...                         # 設定と引数を読み、ロックを取る（ここで止まるときは要約を出さない）
    common.start_log(...)
    completed = False
    code = common.EXIT_OK
    try:
        ...                     # 処理（途中で止まるときは、部品かここで sys.exit を呼ぶ）
        code = ...              # 処理を終えたときの終了コード（0 のほか、check_cols の 3 など）
        completed = True
    finally:
        if completed:
            common.log_info('<要約>')
        else:
            common.log_info('<途中で止まったことが分かる要約>')
    sys.exit(code)
```

`try` の中の `sys.exit` は、途中で止まるときだけに使う。処理を終えて 0 以外の終了コードで終わるとき（[HLD 3.5.3](30_HLD.md#353-関数) の `check_cols` の呼ぶ順の「`write_unresolved_list` と結果の要約の後に終了コード 3」など）は、`try` の中で `code` に入れて `completed = True` にし、`try`/`finally` の後の `sys.exit(code)` で終える（`try` の中で `sys.exit` を呼ぶと `completed` が偽のままになり、終えた実行に途中で止まった要約が出るため）。

##### load_config

`load_config(config_path: str, keys: Collection[str], required: Collection[str]) -> Config`

1. 次のどれかに当たれば `ValueError`（(i) `keys` に `data_dir` が無い、(ii) `keys` に `log_dir` が無い、(iii) `required` に `data_dir` が無い。呼ぶ側の誤り。利用者の誤りではない。[HLD 3.9](30_HLD.md#39-共通部品)の「`data_dir`・`log_dir` はどのバッチも使うので、どのバッチでも当たる」）。このほか、`keys` に `_CONFIG_KEYS` に無い名前があるとき、`required` に `keys` に無い名前があるときも `ValueError`。
2. `path = os.path.abspath(config_path)`（相対パスは起動した作業ディレクトリが基準。[HLD 2.3.2](30_HLD.md#232-設定ファイル)）。`os.path.exists(path)` が偽なら CF1 を出して `EXIT_USAGE`。`path` が `DEFAULT_CONFIG_PATH` と等しいときだけ CF1 の既定の対処にする（呼び出しのたびにモジュールの属性を引く。テストが差し替えて確かめるため）。ディレクトリは CF1 にせず、3 の `open` の `OSError` で CF2 にする（`read_mesh_arg` の 2 と同じ分け方）。
3. `open(path, 'rb')` で全部をバイト列で読む。`OSError`（ディレクトリのときの `IsADirectoryError` を含む）なら CF2 で `EXIT_USAGE`。
4. 下の `_parse_ini(data)` で読む。返された誤りが `None` でなければ、その記号（CF2 か CF3）を `{reason}` つきで出して `EXIT_USAGE`。`[DEFAULT]` もふつうの節として読まれ、下の 5 で知らない節になる。行の途中の `#`・`;` は注釈にならず、値の一部になる（`data_dir = /x # 注` の値は `/x # 注` になる）。
5. ファイル全体の検査: ファイルの順に、`_CONFIG_KEYS` に無い節は CF4、ある節の中で `_CONFIG_KEYS` のその節に無いキーは CF5 を、誤りの一覧に足す（知らない節の中のキーには CF5 を出さず、その節の CF4 だけにする。別の節にあるキー、大文字の違うキーも CF5）。
6. キーごとの検査: `_CONFIG_KEYS` の順に、`keys` にあって、ファイルのその節に書いてあるキー（別の節に書いてあるものは書いていないものとして扱う）の値を [2.1.2](#212-型とデータ)の判定に掛け、合わなければ CF6 を足す。
7. 必須の検査: `_CONFIG_KEYS` の順に、`required` にあってファイルのその節に書いていないキーは CF7 を足す（`[fetch]` の節に `data_dir` のキーを書き、`[paths]` の節に書かなかったときは、5 の CF5 と、この CF7 の両方が出る）。
8. 誤りの一覧が空でなければ、一覧の順に各誤りのメッセージ（2 行ずつ）を `log_error` で出し、`EXIT_USAGE`。1 つでも誤りがあれば、全部を出してから 1 回だけ止まる。
9. `keys` の各キーについて `ConfigValue` を作る。書いてあれば `from_file=True` と判定後の値（整数は `int`）、書いていなければデフォルト（`log_dir` は `data_dir` の値から作る）と `from_file=False`、デフォルトの無いキーは `None` と `from_file=False`。`Config(path, values)` を返す。

確かめないこと: 相互制約、パスに改行を含む設定の拒否（どちらも起動口が自分で確かめる。HLD 3.9 の表の後の段落）。`keys` に無いキーの値。ログには書かない（`start_log` の前なので画面だけ）。

##### _parse_ini

`_parse_ini(data: bytes) -> tuple[list[tuple[str, list[tuple[str, str]]]], tuple[str, str] | None]`（内部。`load_config` の 4 が使う）

返すのは、節の名前と、その節の（キー, 値）の並びを、ファイルの順に並べたリストと、誤り。誤りが無ければ 2 つ目は `None`、あれば（記号 `'CF2'` か `'CF3'`, `{reason}`）で、1 つ目は空のリスト。`_parse_ini` は止まらず、メッセージも出さない（メッセージは `load_config` が出す）。

**設定ファイルの書式**: 受け入れる形を小さく決める。Python の `_parse_ini` と、C++ の CMP4（地形解析エンジン）の `load_config`（[6.12](#612-analyze_terrain_common)）が、この書式を同じ決まりで別に実装する（[HLD 2.3.2](30_HLD.md#232-設定ファイル)の「CMP4 は小さな INI 読み取りを持つ」、[DEC7](30_HLD.md#234-設計判断)「設定は INI 1 本」）。

1. 先頭の UTF-8 の BOM（バイト列 `EF BB BF`）を 1 つだけ除き、残りを UTF-8 として読む。UTF-8 として読めない列（サロゲートの符号化、U+10FFFF を超える符号位置、長すぎる符号化、途中で切れた列）があれば CF2（`{reason}` は `UTF-8 として読めない`）。
2. NUL（U+0000）があれば CF3（`{reason}` は `NUL の文字がある`）。
3. `\n` で行に分け、1 から番号を振る。各行の末尾の `\r` を 1 つだけ除く（CRLF の行）。行の途中の `\r` は行を分けない。
4. 各行の前後から空白（U+0020）とタブ（U+0009）だけを除く（ほかの空白の字は除かない）。空になった行と、`#` か `;` で始まる行は読まない（字下げした注釈も読まない）。行の途中の `#`・`;` は注釈にならず、値の一部になる。
5. `[` で始まる行は節の見出し。`]` で終わり、間の名前が 1 字以上で `[`・`]` を含まないときだけ正しい（名前の前後の空白は除かず、そのまま名前にする）。そうでなければ CF3（`{reason}` は `{line_no} 行目が節の見出しの形でない: {line}`）。同じ名前の節が 2 回目なら CF3（`{line_no} 行目で節 [{section}] が 2 回目`）。
6. ほかの行はキーの行。節の見出しより前なら CF3（`{line_no} 行目のキーが節の見出しより前にある: {line}`）。`=` が無ければ CF3（`{line_no} 行目に = が無い: {line}`）。最初の `=` で分け、前を 4 と同じく空白とタブを除いてキー、後ろを同じく除いて値にする。キーが空なら CF3（`{line_no} 行目のキーの名前が空: {line}`）。同じ節に同じキーが 2 回目なら CF3（`{line_no} 行目でキー {key} が [{section}] に 2 回目`）。値は空でもよい（型の検査で CF6）。キーと節の名前の大文字と小文字は区別する。
7. 最初に見つけた誤りで止まる（CF3 は 1 つだけ出す）。`{line}` は 4 で前後を除いた後の行。

`configparser` の寛大な形（`key: value` の区切り、字下げした行を前の値の続きとして読むこと、節の見出しの後ろの字を捨てること、Unicode の空白を値から除くこと）は、C++ で同じに書くと食い違いやすく、綴りの誤りも見逃すので、受け入れない（誤りとして知らせる）。`params/config.ini.example` の書き方（`[節]`、`キー = 値`、`#` の注釈の行）は通る。

**設定ファイルの書式のテストベクトル**: どの実装も、ファイルの中身（バイト列）ごとに、次の表のとおりになることを UT で確かめる（Python は `UT-common-44`、C++ は `UT-analyze_terrain_common-11`。どちらも `load_config` の結果の列を確かめる。書式の結果の列は `_parse_ini` を書く人のための説明で、UT は内部の関数を直接呼ばない）。`MV-01`〜`MV-21` と同じ書き方で、中身の `\n` などは C の書き方、`EF BB BF` などは 16 進のバイト（バイトの間の空白は区切りでバイトではない）。書式の結果は、読めたときは `[節] キー = 値` を書いた順に `、` で並べたもの（値の中の字は C の書き方）、誤りは記号と `{reason}`。`load_config` の結果の列は、`keys` を `data_dir` と `log_dir`、`required` を `data_dir` にして読んだときの結果で、読めたら `data_dir` の値、止まったら出る記号をこの順に並べたもの（どれも終了コード 2。CF4 は知らない節、CF6 は値が型に合わない、CF7 は必須のキーが無い）。

| ID | 中身 | 書式の結果 | `load_config` の結果 |
|---|---|---|---|
| `CV-01` | `[paths]\ndata_dir = /d\n` | `[paths] data_dir = /d` | `/d` |
| `CV-02` | `[paths]\r\ndata_dir=/d\r\n` | `[paths] data_dir = /d` | `/d` |
| `CV-03` | `EF BB BF` の後に `[paths]\ndata_dir = /d\n` | `[paths] data_dir = /d` | `/d` |
| `CV-04` | 空白・タブ・`[paths]`・空白・`\n`・タブ・`data_dir`・タブ・`=`・タブ・`/d`・空白・`\n` | `[paths] data_dir = /d` | `/d` |
| `CV-05` | `# a\n; b\n  # c\n\n[paths]\ndata_dir = /d # x ; y\n` | `[paths] data_dir = /d # x ; y` | `/d # x ; y` |
| `CV-06` | `[paths]\ndata_dir = /d=e\n` | `[paths] data_dir = /d=e` | `/d=e` |
| `CV-07` | `[paths]\ndata_dir =\n` | `[paths] data_dir =` と空の値 | CF6（`data_dir`） |
| `CV-08` | `[paths]\ndata_dir=/d`（最後の改行なし） | `[paths] data_dir = /d` | `/d` |
| `CV-09` | 空のファイル | 節もキーも無い | CF7（`data_dir`） |
| `CV-10` | `[ paths ]\ndata dir = /d\n` | `[ paths ] data dir = /d`（節の名前は ` paths `、キーは `data dir`） | CF4（`[ paths ]`）、CF7（`data_dir`） |
| `CV-11` | `[DEFAULT]\nx = 1\n` | `[DEFAULT] x = 1` | CF4（`[DEFAULT]`）、CF7（`data_dir`） |
| `CV-12` | `[paths]\ndata_dir = /d` と `C2 A0`（U+00A0）と `\n` | `[paths] data_dir = /d` と U+00A0（U+00A0 を除かない） | `/d` と U+00A0 |
| `CV-13` | `[paths]\ndata_dir = /d` と `0C`（フォームフィード）と `\n` | `[paths] data_dir = /d` と `\f` | `/d` と `\f` |
| `CV-14` | `[paths]\ndata_dir: /d\n` | CF3 `2 行目に = が無い: data_dir: /d` | CF3 |
| `CV-15` | `[paths]\ndata_dir = /d\n  more\n` | CF3 `3 行目に = が無い: more` | CF3 |
| `CV-16` | `[paths]\ndata_dir\n` | CF3 `2 行目に = が無い: data_dir` | CF3 |
| `CV-17` | `data_dir = /d\n` | CF3 `1 行目のキーが節の見出しより前にある: data_dir = /d` | CF3 |
| `CV-18` | `[paths]\n[paths]\n` | CF3 `2 行目で節 [paths] が 2 回目` | CF3 |
| `CV-19` | `[paths]\ndata_dir = /d\ndata_dir = /e\n` | CF3 `3 行目でキー data_dir が [paths] に 2 回目` | CF3 |
| `CV-20` | `[paths] x\n` | CF3 `1 行目が節の見出しの形でない: [paths] x` | CF3 |
| `CV-21` | `[]\n` | CF3 `1 行目が節の見出しの形でない: []` | CF3 |
| `CV-22` | `[pa]ths]\n` | CF3 `1 行目が節の見出しの形でない: [pa]ths]` | CF3 |
| `CV-23` | `[paths]\n= /d\n` | CF3 `2 行目のキーの名前が空: = /d` | CF3 |
| `CV-24` | `[paths]\rdata_dir = /d\n` | CF3 `1 行目が節の見出しの形でない:` と空白 1 つの後に `[paths]`・CR・`data_dir = /d`（CR は行を分けない） | CF3 |
| `CV-25` | `[paths]\nda` と NUL と `ta = /d\n` | CF3 `NUL の文字がある` | CF3 |
| `CV-26` | `FF FE` | CF2 `UTF-8 として読めない` | CF2 |
| `CV-27` | `EF BB BF EF BB BF` の後に `[paths]\ndata_dir = /d\n` | CF3 `1 行目のキーが節の見出しより前にある:` と空白 1 つの後に U+FEFF と `[paths]`（BOM は 1 つだけ除くので、2 つ目の U+FEFF が行の頭に残り、`[` で始まらない） | CF3 |

`CV-24`・`CV-25`・`CV-27` の `{line}` の中の CR・NUL・U+FEFF は、メッセージにそのまま出る（比べるのは終了コードと `{reason}` の文字列）。CF3 の行の `load_config` の結果の列は、書式の結果の列の CF3 が 1 つだけ出る。

##### start_log

`start_log(log_dir: str, config: Config, program: str, argv: Sequence[str], start: StartTime) -> None`

1. 2 回目の呼び出しは `RuntimeError`。
2. `os.makedirs(log_dir, exist_ok=True)`。`OSError`（`log_dir` がファイルのときの `FileExistsError` を含む）なら [2.2](#22-ログとメッセージの文面)の G3（`{path}` は `log_dir`）を出して `EXIT_ERROR`。
3. `path = os.path.join(log_dir, f'{program}_{start.wall:%Y%m%dT%H%M%S}_{os.getpid()}.log')`（[HLD 5.7.2](30_HLD.md#572-処理の流れ) の 2「ファイルの名前」）。`open(path, 'x', encoding='utf-8', newline='\n')`。`FileExistsError` なら G4、ほかの `OSError` なら G3（`{path}` は開けなかったログファイルのパス）を出して `EXIT_ERROR`（既にあるファイルには触れない）。
4. ここで初めて `_state` に `file`・`path`・`program`・`start` を入れ、次をこの順に取り付ける: `atexit.register(_finish_log)`、`sys.exit` を内部の関数 `_exit`（下の `_exit`）に差し替える、`sys.excepthook` を `_excepthook` に差し替える、最後に `SIGINT` と `SIGTERM` のハンドラを `_on_signal` にする（シグナルのハンドラを最後にするのは、ハンドラが上げる `SignalStop` を、`_finish_log` と `_excepthook` が必ず受けるようにするため。先に付けると、取り付けの途中で届いたシグナルで `_finish_log` が動かず、終了コードが 128＋シグナルの番号にならない）。
5. 2.2 の L1・L2 の行（始まりと引数、設定ファイル、設定値）を、`_emit` で標準出力とログファイルに出す。書けなければ下の `log_info`・`log_warning`・`log_error` と同じく `LogWriteError`。`argv` は起動の部分が渡す `sys.argv[1:]`（プログラムの名前を含まない）。引数に改行があれば、L1 はその改行で複数の行になる（`_emit` の行の分け方。[2.2](#22-ログとメッセージの文面)の引用の決まり）。

`sys.exit` を差し替える理由: Python の `atexit` の処理からは終了コードが読めない（2026-10-18 に CPython で確かめた）。HLD 3.9 は「プログラムが終わるときに終わりの行を書く」を `start_log` に持たせ、終わりの行には終了コードが要る（[HLD 5.7.2](30_HLD.md#572-処理の流れ) の 4「始まりと終わりの行」）。選ばなかった案: HLD 3.9 に終わりの行を書く部品を足す（確定した HLD の部品を増やすことになる）。各プログラムが終わりの行を書く（HLD 3.9 の「`start_log` が書く」と食い違う）。

##### _exit

`_exit(code=None) -> NoReturn`（内部。`start_log` の 4 で `sys.exit` と差し替える）

`code` が `None` なら 0、`int` ならその値、それ以外（`sys.exit('msg')` の文字列など）なら 1 を `_state.exit_code` に記録してから、差し替える前の `sys.exit(code)` を呼ぶ（Python の終了コードと同じ値にする）。

##### _finish_log

`_finish_log() -> None`（内部。`atexit` から呼ばれる）

1. まず `SIGINT`・`SIGTERM` を無視にする。`_state.broken` が真なら、終わりの行を書かず（HLD 5.7.2 の 4「始まりと終わりの行」の「ログファイルに書けなくなって止まるときは、終わりの行を書こうとせず」）、標準出力と標準エラー出力を flush して `os._exit(EXIT_ERROR)`（呼ぶ側が規約に反して `LogWriteError` を捕まえて続けても、終了コードを 1 にする。[HLD 5.7.3](30_HLD.md#573-異常系)）。
2. `_state.signum` があれば `code = 128 + _state.signum`（シグナルの後の `finally` の後始末で別の例外が上がって `SignalStop` が置き換わり、`_excepthook` が `exit_code` を 1 にしたときも、シグナルで止まったことを優先する。[HLD 2.5.1](30_HLD.md#251-終了コード) の「シグナルで止まったときは 128＋シグナル番号」。ログに書けなくなったとき（上の 1）と、終わりの行を書けなかったとき（下の 3）の終了コード 1 は、これより先に決まる）。無ければ `code = _state.exit_code`、`None` なら 0（`sys.exit` を呼ばずに最後まで進んだとき）。[2.2](#22-ログとメッセージの文面)の L3 の終わりの行を、`_state.file` へ時刻付きで直接書き、flush して閉じる（書く・flush・閉じるのどれかの `OSError` を、次の 3 の「書けなければ」とする。`_emit` は使わない。書き込みの失敗を `LogWriteError` と G5 でなく、次の 3 の G6 にするため）。書けたら、同じ文面を標準出力へ時刻なしで出す（失敗は下の「画面への出力の失敗」のとおり無視する）。
3. 書けなければ（`OSError`）G6 を標準エラー出力にだけ出し、標準出力と標準エラー出力を flush して `os._exit(EXIT_ERROR)`（終了コード 0 などで終わるはずだったときも 1。HLD 5.7.3）。
4. `_state.signum` があれば flush して `os._exit(code)`（`code` は 2 の 128＋シグナルの番号。Python は捕まらなかった例外で 1 を返すので、この値にするため）。それ以外は、標準出力と標準エラー出力をこの順にそれぞれ flush し、失敗した（`OSError`・`ValueError`）ものは `sys.stdout`・`sys.stderr` の属性を `open(os.devnull, 'w')` に差し替えてから戻る（終了コードは Python のとおり）。差し替えるのは、Python が `atexit` の処理の後に `sys.stdout`・`sys.stderr` をもう一度 flush し、それが失敗すると終了コードを 120 にするため（標準出力が切れたパイプのとき、L3 の画面出力の失敗を無視しても、出せなかった字がバッファに残って起きる。2026-10-19 に CPython 3.14.7 で、差し替えなければ 120、差し替えれば `sys.exit(3)` の 3 になることを確かめた）。差し替えた後の出力は捨てる（どのみち出せない）。

画面への出力の失敗: 1〜4 の画面への出力と flush（1・3・4 の標準出力と標準エラー出力の flush、2 の L3 の画面出力、3 の G6）は、それぞれ `OSError` と `ValueError`（閉じたストリームへの書き込み）を捕まえて無視し、必ず次へ進む（`os._exit` か、戻るところまで届かせる）。`atexit` の処理の中で例外が上がると Python はそれを無視して進むので、`os._exit` に届かず、終了コードが 1 や 128＋シグナルの番号にならないため（HLD 5.7.3、[HLD 2.5.1](30_HLD.md#251-終了コード)）。終わる途中で、止める先も知らせる先も無い。ログファイルへの書き込みの失敗は 2・3 のとおりで、これに当たらない。

`os._exit` を呼ぶと、`start_log` より前に `atexit` に登録された処理（読み込んだライブラリが登録したもの）は動かない。`os._exit` を呼ぶのは、ログに書けなくなったとき、終わりの行を書けなかったとき、シグナルで止まるときだけで、どれもプログラムの成果物の後始末は `finally` で済んでいる。

##### _excepthook

`_excepthook(exc_type, exc, tb) -> None`（内部）

- `SignalStop`: `_state.exit_code = 128 + exc.signum`。メッセージは出さない（終わりの行にシグナルの名前を書く）。
- `LogWriteError`: `_state.exit_code = EXIT_ERROR`。メッセージは書けなくなったときに出してある。
- そのほか: `_state.exit_code = EXIT_ERROR`。2.2 の G7 の 2 行（`log_error` と同じ形の `ERROR:` と `対処:` の行）を下の `_emit` で標準エラー出力とログファイルに出し、続けて `''.join(traceback.format_exception(exc_type, exc, tb))` の末尾の改行を 1 つ除いてから改行で分けた各行（最後に空の行を出さない）を、下の `_emit` で標準エラー出力とログファイルに出す。G7 の `_emit` と Traceback の `_emit` は、別々の `try` で囲み、どちらかで `LogWriteError` が上がったら、その `try` の中で捕まえて次へ進む（G7 の書き込みが失敗しても、Traceback は画面に出る。`broken` は真になっているので、`_finish_log` が 1 で終える）。G7 と Traceback の画面への出力と flush の `OSError`・`ValueError`（標準エラー出力が切れたパイプのときなど）は、`_excepthook` の中に限って捕まえて無視し、ログファイルへの書き込みを続ける（どちらの `_emit` も `ignore_screen_errors=True` で呼ぶ）。画面に出せないときも、止まった理由をログファイルに残すため（G7 の対処は「ログファイルから写して」）。

##### _emit

`_emit(lines: list[str], stream: TextIO, ignore_screen_errors: bool = False) -> None`（内部）

渡された全行（下の改行での分け方の後の行）を、先に画面（`stream`）へ時刻なしで出して flush し、その後で全行をログファイルに時刻付きで書く（1 行ずつ画面とファイルに交互に書かない。ログファイルに書けなくなっても、渡された行は画面にすべて出るようにするため）。`log_info`・`log_warning`・`log_error`、`start_log` の 5 の L1・L2 の行、`_excepthook` の G7 と Traceback の行は、どれもこれで出す。

- 渡された各行の中に改行（`\n`）があれば、`str.split('\n')` でさらに行を分けてから出す（`\r` などのほかの字では分けない。画面には分けた行をそのまま、ログファイルには分けた各行に時刻を付けて書く）。`start_log` の L1 の引数の改行も、この規則で複数の行になる。
- 画面とログファイルへの書き方の細部（flush、出力先の引き方、書けないときの G5 と `LogWriteError`、`broken` の後の扱い）は、下の `log_info`・`log_warning`・`log_error` の「画面」と「ログファイル」の箇条のとおり。
- `ignore_screen_errors` が真なら、画面への出力と flush の `OSError`・`ValueError` を捕まえて無視し、ログファイルへの書き込みに進む（`_excepthook` だけが真で呼ぶ）。偽なら、画面の失敗はそのまま呼ぶ側へ伝わる（「画面」の箇条）。

##### _on_signal

`_on_signal(signum: int, frame) -> None`（内部）

`_state.signum` が `None` でなければ何もしない（2 回目から。止まるための `finally` の後始末を途中で切らないため）。1 回目は `_state.signum = signum` を入れてから `raise SignalStop(signum)`。`_excepthook` は `SignalStop` のとき `_state.signum` を入れ直さない。呼ぶ側は `SignalStop` を捕まえず（`except BaseException` を書かない）、`finally` で後始末をする。`start_log` の前に受けたシグナルは Python の既定の扱い（`SIGINT` は 130、`SIGTERM` は 143 で終わる）。

##### log_info・log_warning・log_error

`log_info(message: str) -> None`・`log_warning(what: str, action: str) -> None`・`log_error(what: str, action: str) -> None`

- 出す行: `log_info` は `message` を（改行があれば、改行で分けたそれぞれが 1 行）、`log_warning` は `WARNING: {what}` と `対処: {action}` の 2 行を、`log_error` は `ERROR: {what}` と `対処: {action}` の 2 行を出す（[HLD 2.5.3](30_HLD.md#253-利用者向けのメッセージ)）。[HLD 3.9](30_HLD.md#39-共通部品) の表も、`log_warning`・`log_error` が `what` と `action` の 2 つを受けるとしている（HLD 2.5.3 の 2 行の書式）。`what`・`action` の中に改行があれば、改行で分けたそれぞれが 1 行で、接頭辞（`WARNING:`・`ERROR:`・`対処:`）は `what` と `action` の最初の行にだけ付け、続きの行には付けない。
- 画面: `log_info` は標準出力、ほかの 2 つは標準エラー出力に、時刻を付けずに出し、そのつど flush。出力先は、呼び出しのたびに `sys.stdout`・`sys.stderr` を引く（import のときに束縛しない。テストが差し替えて確かめるため）。画面への書き込みの失敗（標準出力のパイプ切れなど）は特別扱いしない: `OSError` はそのまま呼ぶ側へ伝わり、捕まらなければ `_excepthook` の G7 で止まる。
- ログファイル: `_state.file` があり `broken` でないときだけ、各行の先頭に `datetime.now().astimezone().isoformat(timespec='seconds')` と空白 1 つを付けて書き、flush（[HLD 5.7.2](30_HLD.md#572-処理の流れ) の 3「行の書式」）。書けなければ（`OSError`）`broken = True` にし、G5 を標準エラー出力にだけ出し、`raise LogWriteError(path) from e`。G5 の画面出力と flush の `OSError` と `ValueError`（閉じたストリームへの書き込み）は捕まえて無視し、必ず `LogWriteError` を上げる（G5 の出力の失敗が呼ぶ側の `except Exception`・`except OSError` に捕まり、ログが壊れたまま処理が続くのを防ぐため。[2.1.2](#212-型とデータ)の `LogWriteError`、[HLD 5.7.3](30_HLD.md#573-異常系) の「止まり」）。`broken` の後は、`log_info` は何も出さず（結果の要約を出さないため。HLD 5.7.2 の 7「結果の要約」）、`log_warning`・`log_error` は標準エラー出力にだけ出す。

##### read_mesh_arg

`read_mesh_arg(value: str) -> set[str]`

1. `value == ''` なら A1 で `EXIT_USAGE`。`re.fullmatch(r'[0-9]{4}', value)` なら `{value}` を返す（[HLD 2.4.3](30_HLD.md#243-メッシュ範囲)）。
2. それ以外はファイルのパス。`path = os.path.abspath(value)`。`os.path.exists(path)` が偽なら A2、`open(path, encoding='utf-8-sig', newline='')` で読めなければ（`OSError`・`UnicodeDecodeError`。ディレクトリも含む）A3 で `EXIT_USAGE`。`newline=''` で改行の変換をしないので、CR は行の区切りにならず、下の 3 で前後の空白として除かれる（[HLD 2.4.3](30_HLD.md#243-メッシュ範囲)の「行末の CR を含む」）。
3. 中身を下の `_parse_mesh_lines` で読む。誤りの行があれば、その最初の行で A4 を出して `EXIT_USAGE`。
4. 集合が空なら A5 で `EXIT_USAGE`。空でなければ返す。日本全土リストに無いコードと北方領土除外メッシュは、ここでは誤りにしない（HLD 2.4.3）。

##### read_mesh_list_file

`read_mesh_list_file(path: str, guidance: str | None) -> set[str]`

- 行の読み方は `read_mesh_arg` の 3 と同じ（下の `_parse_mesh_lines`）。違うのは止まり方で、`os.path.exists` が偽なら R1、ほかの理由で読めなければ（ディレクトリを含む。`read_mesh_arg` の 2 と同じ判定で、`newline=''` で読む）R2、誤りの行があれば R3 を出して `EXIT_ERROR`（HLD 3.9）。有効な行が 0 のときは誤りにせず空の集合を返す。`path` は呼ぶ側が渡したまま使う（`os.path.abspath` してからメッセージに出す）。
- `guidance` は R1〜R3 の `対処:` の行に入れる案内。`None` のときは既定の対処にする（HLD 3.9 の「案内の無いリストは『なし』」）。

##### _parse_mesh_lines

`_parse_mesh_lines(text: str) -> tuple[set[str], int | None, str | None]`（内部。`read_mesh_arg` の 3 と `read_mesh_list_file` が使う）

返すのは、有効な行の値の集合と、最初の誤りの行の番号とその行の中身（誤りが無ければどちらも `None`）。

1. `text.split('\n')` で行に分け、1 から番号を振る。
2. 各行の前後から `' '`・`'\t'`・`'\r'` を除き（`line.strip(' \t\r')`。全角の空白は除かない）、空なら飛ばし、`#` で始まれば飛ばす。
3. 残りが `[0-9]{4}` に合わなければ、最初に見つけた行の番号と中身を誤りとして返す。合う行の値を集合に入れる（重なりは 1 つ）。

この行の読み方（除く空白の字、空行と `#` の行、4 桁の数字の判定、行番号の数え方）と、ファイルの読み方（UTF-8 で読み、先頭の BOM〈U+FEFF〉を 1 つだけ除く。UTF-8 として読めないファイルは読めない誤りにする〈`read_mesh_arg` は A3、`read_mesh_list_file` は R2〉。Python は `encoding='utf-8-sig'` で開いてこれを満たす）は、bash の `run_pipeline` と C++ の CMP4 が同じ決まりで別に実装するときの正本で、それらのモジュールの節はここを指す（[DEC149](30_HLD.md#4234-設計判断)「`--mesh` は bash と Python で別に読む」・[DEC150](30_HLD.md#444-設計判断)「CMP4 は共通部品の決まりを C++ で別に実装する」）。

**メッシュの読み方のテストベクトル**: どの実装も、ファイルの中身（バイト列）ごとに、読んだ結果が次の表のとおりになることを UT で確かめる（Python は `UT-common-43`、bash は `UT-run_pipeline-05`。CMP4 は書くときに足す）。`--mesh` として読むときは、空の集合が A5 になる（リストとして読むときは空の集合を返す）。誤りの行の中身は `{line}` の値（前後の空白を除いた後）。表の中身の列は、`\n` などを C の書き方、`EF BB BF` などを 16 進のバイトで書き、バイトの間の空白は区切りでバイトではない。

| ID | 中身 | 結果 |
|---|---|---|
| `MV-01` | `5339\n` | `{5339}` |
| `MV-02` | 空白 1 つ・`5339`・空白 1 つ・`\r\n`・`\t5340\n` | `{5339, 5340}` |
| `MV-03` | `EF BB BF` の後に `5339\n` | `{5339}` |
| `MV-04` | `# c\n\n5339\n5339\n` | `{5339}` |
| `MV-05` | `5339`（最後の改行なし） | `{5339}` |
| `MV-06` | `#only\n  \n` | 空の集合 |
| `MV-07` | 空のファイル | 空の集合 |
| `MV-08` | `#a` と NUL と `b\n5339\n` | `{5339}` |
| `MV-09` | `5339\n53a9\n5340\n12\n` | 2 行目が誤り（`53a9`） |
| `MV-10` | `5339\n` の後に `EF BB BF` と `5340\n` | 2 行目が誤り（`{line}` は U+FEFF と `5340`） |
| `MV-11` | `EF BB BF EF BB BF` の後に `5339\n` | 1 行目が誤り（`{line}` は U+FEFF と `5339`） |
| `MV-12` | `53` と NUL と `39\n` | 1 行目が誤り |
| `MV-13` | 全角の数字の `5339`（コードポイント U+FF15・U+FF13・U+FF13・U+FF19）と `\n` | 1 行目が誤り |
| `MV-14` | `5339\r5340\n` | 1 行目が誤り（CR は行を分けない） |
| `MV-15` | `\v5339\n`（垂直タブ） | 1 行目が誤り（除く空白は空白・タブ・CR だけ） |
| `MV-16` | `FF FE` | UTF-8 として読めない |
| `MV-17` | `ED A0 80` の後に `\n`（サロゲートの符号化） | UTF-8 として読めない |
| `MV-18` | `#` の後に `F4 90 80 80`（U+10FFFF を超える符号位置）と `\n5339\n` | UTF-8 として読めない |
| `MV-19` | `#` の後に `F8 88 80 80 80`（5 バイトの列）と `\n5339\n` | UTF-8 として読めない |
| `MV-20` | `#` の後に `C0 80`（長すぎる符号化）と `\n5339\n` | UTF-8 として読めない |
| `MV-21` | 空白 1 つの後に `# c\n5339\n`（`#` の前に空白） | `{5339}` |

`MV-08`・`MV-12` の NUL は、bash の実装ではメッセージの `{line}` に出せない（bash の変数は NUL を持てない。[5.1.3](#513-関数の細部)の `_read_mesh_file`）。一致を確かめるのは、集合と、誤りの行の番号と、NUL を含まない行の `{line}` の値だけである。

##### acquire_lock

`acquire_lock(data_dir: str) -> None`

1. `path = os.path.join(data_dir, _LOCK_NAME)`。`fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o644)`。`OSError` なら G2 で `EXIT_ERROR`。
2. `fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)`。`BlockingIOError` なら G1、ほかの `OSError` なら G2 で `EXIT_ERROR`。成功したら `_state.lock_fd = fd` にし、閉じない（プロセスが終わるまで持つ。[HLD 2.9.3](30_HLD.md#293-同時起動の排他)）。ロックファイルは消さない。

呼ぶのは利用者向けの 2 本（`preprocess_boundaries`・`fetch_tiles`）が `start_log` の前（HLD 2.9.3 の起動時の順序）なので、メッセージは画面にだけ出る。bash の `run_pipeline` も同じファイルに `flock` を掛ける（同じ名前を [2.3](#23-ファイルの名前と書き方)から取る）。

##### fetch_record_path

`fetch_record_path(data_dir: str) -> str`

`os.path.join(data_dir, 'tiles', _FETCH_RECORD_NAME)` を返す。ファイルの有無は見ない。

##### mesh_to_latlon

`mesh_to_latlon(mesh: str) -> tuple[tuple[float, float], tuple[float, float]]`

`mesh` が `[0-9]{4}` に合わなければ `ValueError`。`aa = int(mesh[:2])`、`bb = int(mesh[2:])`。返すのは `((南端の緯度, 西端の経度), (北端の緯度, 東端の経度))` で、4 つとも `float`（経度は `float(100 + bb)`・`float(101 + bb)` にする。Python では `100 + bb` が `int` になるため）。式と計算の順は[2.4](#24-言語ごとに別に実装する式のテストベクトル)の決まりのとおり。範囲（3036〜6848）は見ない。

##### latlon_to_tile

`latlon_to_tile(lat: float, lon: float, z: int) -> tuple[int, int]`

`(x, y)` を返す。式と計算の順は [2.4](#24-言語ごとに別に実装する式のテストベクトル) の決まりのとおり。引数を検査しない（呼ぶのは CMP1（行政区域前処理）・CMP2 の関数で、渡すのは日本のメッシュの四隅。HLD 3.9 の表の「使うところ」）。

#### 2.1.4 メッセージ文面

表（記号・場面・1 行目・`対処:` の行・終了コード）で書く。`{path}` は `os.path.abspath` したパス、`{reason}` は `OSError` の `strerror`（無ければ `str(e)`）か、`UnicodeDecodeError` なら `UTF-8 として読めない`。CF2・CF3 の `{reason}` で書式の誤りに当たるものは、2.1.3 の設定ファイルの書式の文。`{example_path}` は `_EXAMPLE_CONFIG_PATH`。全体に共通する場面（ロックとログ）は [2.2](#22-ログとメッセージの文面)の G1〜G7 を指し、ここに写さない。

| 記号 | 場面 | 1 行目（`ERROR:` と空白 1 つの後） | 2 行目（`対処:` と空白 1 つの後） | 終了コード |
|---|---|---|---|---|
| CF1 | 設定ファイルが無い | `設定ファイルが無い: {path}` | 既定のパスなら `{example_path} を複製して {path} を作り、data_dir と user_agent_email を書く`、それ以外は `--config に渡したパスを確かめる` | 2 |
| CF2 | 設定ファイルを読めない | `設定ファイルを読めない: {path}: {reason}` | `ファイルの読み取りの権限と、UTF-8 で保存されていることを確かめる` | 2 |
| CF3 | INI として読めない | `設定ファイルを INI として読めない: {path}: {reason}` | `{example_path} と見比べて、節の見出しとキーの書き方を直す` | 2 |
| CF4 | 表に無い節 | `設定ファイルに知らない節がある: [{section}]（{path}）` | `節の名前を確かめる。使える節は paths・fetch・analysis・merge・match` | 2 |
| CF5 | 表に無いキー | `設定ファイルに知らないキーがある: [{section}] {key}（{path}）` | `キーの名前と節を確かめる。[{section}] に置けるキーは {keys}`（`{keys}` は `_CONFIG_KEYS` のその節のキーを `・` でつないだもの） | 2 |
| CF6 | 値が型か許容範囲に合わない | `設定値が許容範囲の外にある: [{section}] {key} = {value}（{path}）` | `次の範囲にする: {range}`（`{range}` は[2.1.2](#212-型とデータ)の表の許容範囲の文。`{value}` はファイルに書いたまま） | 2 |
| CF7 | 必須のキーが無い | `必須の設定が無い: [{section}] {key}（{path}）` | `[{section}] に {key} を書く（{range}）` | 2 |
| A1 | `--mesh` の値が空 | `--mesh の値が空` | `--mesh に、4 桁のメッシュコードか、メッシュコードを 1 行 1 件で書いたファイルのパスを渡す` | 2 |
| A2 | `--mesh` のファイルが無い | `--mesh のファイルが無い: {path}` | A1 と同じ | 2 |
| A3 | `--mesh` のファイルを読めない | `--mesh のファイルを読めない: {path}: {reason}` | `ファイルの読み取りの権限と、UTF-8 で保存されていることを確かめる` | 2 |
| A4 | 4 桁の数字でない行 | `--mesh のファイルの {line_no} 行目が 4 桁の数字でない: {path}: {line}` | `1 行に 4 桁のメッシュコードを 1 つずつ書く。空行と # で始まる行は読まない` | 2 |
| A5 | 有効な行が無い | `--mesh のファイルにメッシュコードが 1 つも無い: {path}` | A4 と同じ | 2 |
| R1 | リストが無い | `メッシュコードのリストが無い: {path}` | `{guidance}`、`None` なら `ファイル {path} があり、読み取れることを確かめる` | 1 |
| R2 | リストを読めない | `メッシュコードのリストを読めない: {path}: {reason}` | R1 と同じ | 1 |
| R3 | リストに 4 桁の数字でない行 | `メッシュコードのリストの {line_no} 行目が 4 桁の数字でない: {path}: {line}` | R1 と同じ | 1 |

`{line}` は前後の空白を除いた後の行の中身。

#### 2.1.5 UT 候補

すべて自動（合否をテストのコードが判定できる）。`start_log` を呼ぶケースと `acquire_lock` を呼ぶケースは、すべて子のプロセス（`subprocess` で、テストを動かしている Python〈`sys.executable`〉に `-c <試験用の短いプログラム>` を付けて起動し、`scripts/` を import の探索先に入れる。`start_log` に渡す `Config` は、子のプロセスの中で `load_config` で読むので、各ケースの前に、`data_dir` と `log_dir` を絶対パスで書いた設定ファイルを置く）で動かし、終了コード・標準出力・標準エラー出力・ログファイルを親のテストが読んで確かめる（`start_log` は `sys.exit`・`sys.excepthook`・シグナルのハンドラ・`atexit` を差し替えたままにし、2 回目の呼び出しは `RuntimeError` になるので、テストのランナーと同じプロセスで呼ばない）。ログファイルに書けない場面は、子のプロセスの試験用のプログラムの中で、`start_log` の後に `common._state.file` を、`write` が `OSError(errno.ENOSPC)` を上げる物に差し替えて起こす（終わりの行だけを失敗させるときは、`_finish_log` が書く直前に差し替わるよう、`atexit.register` で差し替えの処理を `start_log` の後に登録する。`atexit` は登録の逆順に動くので、差し替えが先に動く）。結合テスト（IT）の仕様書 `60_IT.md` の §5 の対応表で「UT（`50_UT.md` で作る）」とした行に、共通部品に当たるものは無い。HLD を書く段で[#202](https://github.com/jj1xgo/findsummits/issues/202)「LLD と IT を書くときに、UT と IT の候補を割り当てる」に挙がった UT 候補のうち共通部品に当たるのは、同じ名前のログファイル（`UT-common-20`）、ログファイルに書けなくなったとき（`UT-common-22`）、終わりの行だけ書けなかったとき（`UT-common-23`）の 3 つ。`start_log` を呼ばずに `sys.exit` で止まるケース（`load_config`・`read_mesh_arg`・`read_mesh_list_file` の誤り）は、`sys.exit` がまだ差し替えられていないので、同じプロセスで `SystemExit` を捕まえて、終了コードと標準エラー出力を確かめてよい。ログファイルの行の期待は、先頭の時刻と空白を除いた文面で書く。`start_log` を呼ぶと標準出力に L1・L2 の行が時刻なしで出るので、標準出力の期待にはこれらも含める。

表の準備の列の共通の準備は次の 2 つ。ケースに固有の準備は、その後に書く。

- **同じプロセス**: テストを動かしているプロセスの中で、対象の関数を直接呼ぶ。設定ファイルを使うケースは、ケースごとに一時のディレクトリを作り、その下に設定ファイルを書いて絶対パスを渡す（`data_dir`・`log_dir` を書くときは、一時のディレクトリの下の絶対パスにする）。止まるケースは `SystemExit` を捕まえて終了コードを読み、標準出力と標準エラー出力は差し替えて捕まえる（`contextlib.redirect_stdout`・`redirect_stderr`）。
- **子のプロセス**: 上に書いた子のプロセスの形で動かす。子に渡す設定ファイルは、親が一時のディレクトリに置く（`data_dir` と `log_dir` を、一時のディレクトリの下の絶対パスで書く）。子の試験用のプログラムは、`StartTime.now()` と `load_config` を呼んでから（ケースが書かなければ、`keys` は `data_dir` と `log_dir`、`required` は `data_dir`）、入力の列のケースの処理をする。`start_log` は、入力の列が書く位置で 1 回だけ、`start_log(<config の log_dir>, config, '<試験用の名前>', sys.argv[1:], start)` の形で呼ぶ（入力の列が `start_log` の位置を書いていないケースは、ケースの処理の最初に呼ぶ。`UT-common-24` は準備の列のとおり）。

| ID | 確かめること | 準備 | 入力 | 期待 |
|---|---|---|---|---|
| `UT-common-01` | 正しい設定を読む | 同じプロセス。全キーを書いた設定ファイル | 全キーを書いた設定と、全キーの `keys`（`required` は `data_dir` だけ） | 全キーの値が整数か文字列に変わり `from_file` が真 |
| `UT-common-02` | デフォルト | 同じプロセス。`data_dir` だけを書いた設定ファイル | `data_dir` だけの設定と、全キーの `keys`（`required` は `data_dir` だけ） | 任意のキーは HLD 2.3.2 のデフォルトで `from_file` が偽、`log_dir` は `<data_dir>/logs`、`user_agent_email` と `sota_geojson_version` は `None` |
| `UT-common-03` | 設定ファイルが無い | 同じプロセス。存在しない一時のパスを 2 つ作り、一方で `common.DEFAULT_CONFIG_PATH` を差し替える（`params/config.ini` がある環境でも起こせるようにするため） | ほかのパスと、既定のパス（差し替えた `DEFAULT_CONFIG_PATH` と同じパス） | どちらも 2、CF1 の対処が既定のパスのときだけ `config.ini.example` の案内、ログファイルを作らない |
| `UT-common-04` | 読めない・INI でない | 同じプロセス。4 つの中身をそれぞれ別の設定ファイルに書く（UTF-8 でない中身はバイト列で書く）。ほかに一時のディレクトリを 1 つ作る | UTF-8 でない中身、節の見出しの無いキー、同じキーの重複、同じ節の重複、設定ファイルの代わりにディレクトリのパス | どれも 2（CF2・CF3）。ディレクトリは CF2（CF1 でない） |
| `UT-common-05` | 知らない節とキー | 同じプロセス。5 つの中身をそれぞれ別の設定ファイルに書き、どれにも `[paths]` の節に `data_dir` を書く。`required` は `data_dir` だけにする（CF7 を混ぜないため） | `[DEFAULT]` の節、`[foo]` の節、`[fetch]` の節に書いた `data_dir` のキー、`[paths]` の節に書いた `Data_Dir` のキー、`keys` に無い節の知らないキー（どのケースも、`keys` には `data_dir` と `log_dir` を入れる） | どれも 2（CF4・CF5）。`keys` に無くても見つける |
| `UT-common-06` | 整数のキーの境目 | 同じプロセス。値ごとに別の設定ファイル（どれも `data_dir` を書く） | 各キーの許容範囲の端とその外（`prominence_primary_m` に `99`/`100`、`prominence_final_m` に `149`/`150`/`151`、`activation_zone_drop_m` に `24`/`25`/`26`、`delete_zone_max_drop_m` に `199`/`200`/`300`/`301`、`max_parallel` に `0`/`1`/`16`/`17`、`interval_ms` に `0`/`5000`/`5001`、`sota_geojson_version` に `0`/`1`、`unmatched_summit_threshold` に `0`）と、`max_parallel` に書き方の違い（`+5`・`1.5`・全角の数字の `10`〈コードポイント U+FF11 と U+FF10〉・`-1`・空の値） | 端の内は読める、外と書き方の違いは 2（CF6）、`{value}` は書いたまま |
| `UT-common-07` | 英字とメールのキー | 同じプロセス。値ごとに別の設定ファイル（どれも `data_dir` を書く） | `provisional_code_max_prefix` に `A`・`Z`・`a`・`AA`・空、`user_agent_email` に `a@b.example`・`nomail`・`a b@c`・`a(b)@c`・空 | `provisional_code_max_prefix` は `A`・`Z` だけ、`user_agent_email` は `a@b.example` だけ読める |
| `UT-common-08` | 必須とキーの絞り込み | 同じプロセス。2 つの設定ファイル | `user_agent_email` を `required` に入れて書かない設定、`keys` に無い `max_parallel = 99` | 前者は 2（CF7）、後者は誤りにしない |
| `UT-common-09` | 誤りをまとめて出す | 同じプロセス。1 つの設定ファイル | CF5・CF6・CF7 が 1 つずつある設定（`keys` は全キー。CF7 は、`required` を `data_dir` と `user_agent_email` にし、`user_agent_email` を書かないことで起こす） | 標準エラー出力に 3 つのメッセージが CF5・CF6・CF7 の順に出て、終了コード 2 が 1 回 |
| `UT-common-10` | 絶対パスでない | 同じプロセス。1 つの設定ファイルに 2 つのキーを書く | `data_dir = data`、`log_dir = logs` | 2（CF6、範囲の文は `絶対パス`） |
| `UT-common-11` | 呼ぶ側の誤り | 同じプロセス。`data_dir` と `log_dir` を書いた正しい設定ファイル | `keys` に `data_dir` が無い、`keys` に `log_dir` が無い、`required` に `data_dir` が無い、`keys` に表に無い名前、`required` に `keys` に無い名前 | どれも `ValueError` |
| `UT-common-12` | `--mesh` の値を読む | 同じプロセス。ファイルは一時のディレクトリに作る。相対パスのケースは、作業ディレクトリをその一時のディレクトリに移してから呼ぶ | `5339`、`0123`、空白と CR と空行と `#` の行と重複を含むファイル、相対パス | `{'5339'}`、`{'0123'}`、重なりを除いた集合、作業ディレクトリ基準で読む |
| `UT-common-13` | `--mesh` の誤り | 同じプロセス。ファイルとディレクトリは一時のディレクトリに作る | 空の値、無いファイル、ディレクトリ、2 行目と 4 行目が誤りのファイル、全角の数字の `5339`（コードポイント U+FF15、U+FF13、U+FF13、U+FF19）の行、有効な行が無いファイル、`533` | どれも 2。誤りの行は最初の 2 行目を示す（A1〜A5）。`533` はパスとして読む |
| `UT-common-14` | リストを読む | 同じプロセス。ファイルとディレクトリは一時のディレクトリに作る。案内ありは `guidance` に文字列、案内なしは `None` | 正しいリスト、空のファイル、無いファイル（案内あり・なし）、誤りの行、ディレクトリ | 集合、空の集合、1 と R1 の対処（案内か既定）、1 と R3、1 と R2 |
| `UT-common-15` | `start_log` の前の出し先 | 同じプロセス（`start_log` を呼ばない） | `log_info`・`log_warning`・`log_error` | 標準出力か標準エラー出力にだけ出て、`WARNING:`・`ERROR:` と `対処:` の 2 行、時刻なし |
| `UT-common-16` | ログファイルの始まり | 子のプロセス。`load_config` の `keys` は `data_dir`・`log_dir`・`max_parallel`・`user_agent_email`（設定ファイルには `data_dir` と `log_dir` だけを書く） | 子のプロセスで `start_log` を呼び、その後に `log_info('<文面>')` と `log_warning('<対象>', '<操作>')` を呼ぶ | `log_dir` を作る、名前が `<program>_<YYYYMMDDTHHMMSS>_<pid>.log`、L1・L2 の行（L2 は `設定ファイル: <設定ファイルの絶対パス>`、`設定: [paths] data_dir = <値>（ファイル）`、`設定: [paths] log_dir = <値>（ファイル）`、`設定: [fetch] max_parallel = 8（デフォルト）`、`設定: [fetch] user_agent_email = 未設定（デフォルト）` の 5 行がこの順）、後の行の先頭に時刻と空白 1 つ（正規表現 `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}` と空白）、標準出力に L1・L2 の行が時刻なしで先に出る、画面の行には時刻なし、2 行のメッセージは各行に時刻 |
| `UT-common-17` | 終わりの行 | 子のプロセス（4 つの子を別々に） | 子のプロセスで `start_log` の後に `sys.exit(0)`・`sys.exit(3)`・`sys.exit('msg')`・`sys.exit` を呼ばずに終わる | 終了コード 0・3・1・0、ログファイルの最後の行が L3 で同じ終了コード、標準出力の最後の行も同じ文面の L3（行頭の時刻なし）、所要時間が 0 以上で小数 3 桁 |
| `UT-common-18` | 捕まらなかった例外 | 子のプロセス | 子のプロセスで `start_log` の後に `raise RuntimeError('x')` | 終了コード 1、G7 と Traceback が標準エラー出力とログに出る、終わりの行は 1 |
| `UT-common-19` | シグナル | 子のプロセス（`SIGTERM` の子と `SIGINT` の子を別々に。シグナルは `os.kill(os.getpid(), <シグナル>)` で送る） | 子のプロセスで `start_log` の後に自分へ `SIGTERM` を送る子と、`SIGINT` を送る子を別々に動かす（1 つの子に 2 つ送るケースは書かない。最初の 1 つで止まるため。2 回目のシグナルは `UT-common-31` で確かめる）。どちらも `try`/`finally` の中で送り、`finally` で標準出力に `CLEANUP` と書く | 終了コード 143・130、標準出力に `CLEANUP` が出る、終わりの行に `SIGTERM`・`SIGINT` |
| `UT-common-20` | 同じ名前のログファイル | 子のプロセス。子の試験用のプログラムの中で、`start_log` を呼ぶ前に、同じ `StartTime` と自分の PID（`os.getpid()`）から 2.1.3 の `start_log` の 3 の名前を作り、`os.makedirs(<log_dir>, exist_ok=True)` で `log_dir` を作ってから、その下にそのファイルを置く（親は子の PID を起動の前に知れないため） | 子の中で同じ名前のファイルを置いた後に `start_log` | 1、G4、置いたファイルは変わらない |
| `UT-common-21` | ログの出力先を用意できない | 子のプロセス。`log_dir` のパスに通常のファイルを置く | `log_dir` がファイル | 1、G3 が標準エラー出力だけに出る |
| `UT-common-22` | ログファイルに書けなくなった | 子のプロセス。書き込みの失敗は前置きの差し替え（`start_log` の後に `common._state.file` を差し替える） | 子のプロセスで、開いた後の書き込みを失敗させて `log_info('x')` を呼ぶ。(a) そのまま、(b) `try`/`except Exception` で囲んで、`except` の中で標準出力に `CAUGHT` と書いてから `sys.exit(0)`、(c) `try` の中の `log_info('x')` で書き込みが失敗し、`finally` の中の 2 つ目の `log_info('要約')` で要約を出す形。(d) `log_info('x')` を呼ばず、`raise RuntimeError('x')`（G7 の書き込みで失敗させる） | どれも終了コード 1、G5 が標準エラー出力に 1 回出る、ログファイルに終わりの行が無い。(b) の `except Exception` は `LogWriteError` を捕まえない（標準出力に `CAUGHT` が出ない）。(c) の標準出力は L1・L2 の行と 1 つ目の `x` だけで、2 つ目の `log_info` の要約は出ない（`x` は、書き込みの失敗の前に画面へ出る）。(d) の標準エラー出力には、G7 の 2 行、G5 の 2 行、Traceback（最後の行が `RuntimeError: x`）がこの順に出る |
| `UT-common-23` | 終わりの行だけ書けなかった | 子のプロセス。前置きの `atexit.register` による差し替えで、`_state.file` を、`write`・`flush`・`close` のどれか 1 つだけが `OSError(errno.ENOSPC)` を上げる物にする（3 つを別々の子で） | 終わりの行の書き込み・flush・close のどれか 1 つだけを失敗させ、`sys.exit(0)` | 終了コード 1、G6 が標準エラー出力に出る |
| `UT-common-24` | ロック | 子のプロセス 3 つ。1 つ目は `start_log` を呼ばず、`acquire_lock` の後、標準出力に 1 行（例 `LOCKED`）を書いて flush し、親が標準入力を閉じるまで待つ。親はその 1 行を読んでから 2 つ目を起こす。2 つ目と、無い `data_dir` の子は、プログラムの起動の順（[HLD 2.9.3](30_HLD.md#293-同時起動の排他)）で `acquire_lock` の後に `start_log` を呼ぶ形にする。無い `data_dir` の子は、存在しないパスを `data_dir` に、一時のディレクトリの下のパスを `log_dir` に書いた設定ファイル | 1 つ目の子のプロセスがロックを持つ間に 2 つ目、無い `data_dir` | 2 つ目は 1 で G1（ロックファイルのパスを含む）、無い `data_dir` は 1 で G2。どちらも設定した `log_dir` にログファイルを作らない（`start_log` に届かない）。終わってもロックファイルが残る |
| `UT-common-25` | 取得完了の記録のパス | 同じプロセス。なし | `/d` | `/d/tiles/<2.3 の取得完了の記録の名前>` |
| `UT-common-26` | 終了コードの定数 | 同じプロセス。なし | — | 0・1・2・3・4 |
| `UT-common-27` | メッシュ → 緯度経度 | 同じプロセス。なし | 2.4 の表 1 の行 | 期待の値と 2.4 の比べ方で等しく、4 つとも `float` |
| `UT-common-28` | 緯度経度 → タイル | 同じプロセス。なし | 2.4 の表 2 の行 | 期待の値と等しい |
| `UT-common-29` | メッシュコードの誤り | 同じプロセス。なし | `533`、`53a9` | `ValueError` |
| `UT-common-30` | 書けない字と長い数 | 同じプロセス。値ごとに別の設定ファイル（NUL を含む中身はバイト列で書く） | 値ごとに別の設定ファイルを使う（同じキーを 2 回書くと CF3 になるため）。(i) `[\x00]` という節を足した設定、(ii) `[paths]` の `data_dir` の値の末尾に NUL を入れた設定、(iii) `max_parallel` に 19 桁の数、`unmatched_summit_threshold` に次の (iv)〜(vii) をそれぞれ別の設定ファイルで、(iv) 先頭の 0 を除いて 18 桁の数、(v) 19 桁の数、(vi) 4301 桁の数、(vii) `0` を 4300 個並べた後に `1` の値 | (i)(ii) は 2（CF3）、(iii)(v)(vi) は 2（CF6）、(iv) は読める、(vii) は `1` として読める |
| `UT-common-31` | 2 回目のシグナル | 子のプロセス | 子のプロセスで `start_log` の後に `SIGTERM` を受け、`finally` の中で自分へもう 1 回 `SIGTERM` を送ってから、標準出力に `MARK` と書く | 標準出力に `MARK` が出る、終了コード 143、終わりの行は 1 つ |
| `UT-common-32` | 始まりの行の引数 | 子のプロセス。引数は `sys.executable`・`-c`・試験用のプログラムの後に並べて子を起こす（子の `sys.argv[1:]` になる） | 子のプロセスで `argv` に `--config`・`/a b`・`it's`・空の引数を渡して `start_log` | ログファイルの最初の行の、時刻と空白の後の文面が `開始: <program> --config '/a b' 'it'"'"'s' ''`（標準出力の最初の行は、時刻なしの同じ文面） |
| `UT-common-33` | 始まりの行の引数の改行 | 子のプロセス。引数は `UT-common-32` と同じく子を起こすときに並べる | 改行を 1 つ含む 1 つの引数（`x` の後に改行、その後に `y`）で `start_log` | ログファイルの最初の 2 行が、時刻と空白の後に `開始: <program> 'x` と `y'`（2 行目にも時刻が付く）、標準出力の最初の 2 行が時刻なしの同じ 2 つの文面 |
| `UT-common-34` | 終わる途中で画面に出せない | 子のプロセス（3 つの子を別々に）。前置きの `atexit.register` による差し替えの形で、`_finish_log` が動く直前に `sys.stdout` と `sys.stderr` を、`write` と `flush` が (a)(c) は `OSError(errno.EPIPE)`、(b) は `ValueError` を上げる物に差し替える。(c) は `UT-common-23` の形で `_state.file` の `write` も失敗させる | (a) `start_log` の後に `sys.exit(3)`、(b) `start_log` の後に自分へ `SIGTERM`、(c) `start_log` の後に `sys.exit(0)` | 終了コード 3・143・1。(a)(b) はログファイルの最後の行が L3 で同じ終了コード（(b) は `SIGTERM` を受けて止まった形） |
| `UT-common-35` | G5 を画面に出せない | 子のプロセス。`start_log` の後に、`common._state.file` を `write` が `OSError(errno.ENOSPC)` を上げる物に、`sys.stderr` を `write` が `OSError(errno.EPIPE)` を上げる物に差し替える | `try`/`except Exception` で囲んで `log_info('x')` を呼び、`except` の中で標準出力に `CAUGHT` と書いてから `sys.exit(0)` | 終了コード 1、標準出力に `CAUGHT` が出ない（G5 の出力の失敗でも `LogWriteError` になる） |
| `UT-common-36` | 呼ぶ側が `LogWriteError` を捕まえて続ける | 子のプロセス。書き込みの失敗は前置きの差し替え（`start_log` の後に `common._state.file` を差し替える） | `try`/`except common.LogWriteError` で囲んで `log_info('x')` を呼び、`except` の中で標準出力に `CAUGHT` と書いてから `sys.exit(0)`（1.2 の規約に反する書き方を、わざと試す） | 終了コード 1、標準出力に `CAUGHT` が出る、ログファイルに終わりの行が無い |
| `UT-common-37` | シグナルの後の後始末で例外 | 子のプロセス | `start_log` の後の `try` の中で自分へ `SIGTERM` を送り、`finally` の中で `raise RuntimeError('cleanup')` | 終了コード 143、G7 と Traceback（最後の行が `RuntimeError: cleanup`）が標準エラー出力とログに出る、ログファイルの最後の行が `SIGTERM` を受けて止まった形の L3 で終了コード 143 |
| `UT-common-38` | 先頭の BOM | 同じプロセス。3 つのファイルを、それぞれ先頭に BOM（バイト列 `EF BB BF`）を付けて書く | `data_dir` を書いた設定ファイルを `load_config` に、1 行目が `5339` の `--mesh` のファイルを `read_mesh_arg` に、1 行目が `5339` のリストを `read_mesh_list_file` に渡す | 設定は読める（`data_dir` の値に BOM が付かない）、`--mesh` とリストはどちらも `{'5339'}` |
| `UT-common-39` | UTF-8 でないメッシュのファイル | 同じプロセス。UTF-8 として読めないバイト列（例 `FF FE`）だけのファイルを 1 つ置く | そのファイルを `read_mesh_arg` と、`guidance` を `None` にした `read_mesh_list_file` に渡す | `read_mesh_arg` は 2 で A3（`{reason}` は `UTF-8 として読めない`）、`read_mesh_list_file` は 1 で R2（同じ `{reason}`） |
| `UT-common-40` | 標準出力が切れたパイプ | 子のプロセス（2 つの子を別々に）。子の試験用のプログラムの中で、`start_log` の後に `os.pipe()` を作り、書く側を `os.dup2` で記述子 1 に付けてから、読む側と書く側の元の記述子を閉じる（標準出力が読む相手の無いパイプになる） | (a) `sys.exit(3)`、(b) `log_info('x')`（`BrokenPipeError` が捕まらずに止まる） | 終了コード 3・1（120 にならない）。ログファイルの最後の行が L3 で、同じ終了コード。(b) はログファイルに G7（`BrokenPipeError`）がある |
| `UT-common-41` | 標準エラー出力が切れたパイプ | 子のプロセス。`UT-common-40` と同じ形で、記述子 2 を読む相手の無いパイプにする | `start_log` の後に `raise RuntimeError('x')` | 終了コード 1。ログファイルに G7 の 2 行と Traceback（最後の行が `RuntimeError: x`）がこの順にあり、その後が L3 で終了コード 1 |
| `UT-common-42` | 全キーの名前の一覧 | 同じプロセス | `common.CONFIG_KEY_NAMES` | `('data_dir', 'log_dir', 'max_parallel', 'interval_ms', 'user_agent_email', 'prominence_primary_m', 'activation_zone_drop_m', 'delete_zone_max_drop_m', 'prominence_final_m', 'sota_geojson_version', 'provisional_code_max_prefix', 'unmatched_summit_threshold')` と等しい |
| `UT-common-43` | bash と共通のテストベクトル | 同じプロセス。[2.1.3](#213-関数の細部)のメッシュの読み方のテストベクトルの中身ごとに一時のファイルをバイト列で書く | 各ファイルを `read_mesh_arg` と、`guidance` を `None` にした `read_mesh_list_file` に渡す | テストベクトルの表の結果のとおり。誤りの行は `read_mesh_arg` が A4、`read_mesh_list_file` が R3 で、`{line_no}` と `{line}` が表のとおり。空の集合は `read_mesh_arg` が A5、`read_mesh_list_file` が空の集合。UTF-8 として読めないものは A3・R2（`{reason}` は `UTF-8 として読めない`） |
| `UT-common-44` | 設定ファイルの書式のテストベクトル | 同じプロセス。[2.1.3](#213-関数の細部)の設定ファイルの書式のテストベクトル（CV-01〜CV-27）の中身ごとに一時のファイルをバイト列で書く | 各ファイルを `load_config` に渡す（`keys` は `data_dir` と `log_dir`、`required` は `data_dir`） | 表の `load_config` の結果の列のとおり（読めたら `data_dir` の値、止まったら終了コード 2 と、出た記号の並び。CF2・CF3 は `{reason}` も表の書式の結果の列のとおり） |

### 2.2 ログとメッセージの文面

書式と出し先の正本は[HLD 2.5.3](30_HLD.md#253-利用者向けのメッセージ)と[HLD 5.7.2](30_HLD.md#572-処理の流れ)で、ここは文面と行の形を決める。CMP4（地形解析エンジン）の C++ の `start_log` など、同じ決まりを別の言語で実装するモジュール（[6.12](#612-analyze_terrain_common)）も、ここの文面と行の形にする。今は 2.1・3.1・4.1・5.1・5.2・6.1・6.2・6.3・6.4・6.5・6.7・6.8・6.9・6.12 が使う分だけを書いてある。

書き方の決まり:

- 文面は日本語。1 行目は `ERROR:` か `WARNING:` と空白 1 つの後に、起きたことを先に書き、`:` と空白 1 つの後に対象（パス、キー、オプション）を書く。対象を文の頭に置いた短い文（`{option} の値が無い`、`--mesh の値が空`）は、`:` 以下を付けない。
- 2 行目は `対処:` と空白 1 つの後に、利用者が次にすべき操作を書く。
- 文末に句点を付けない。OS の理由（`{reason}`）は OS が返す文のまま（英語でよい）。
- パス: メッセージの対象として出すパス（プログラムが組み立てたか解決したファイルとディレクトリ）は絶対パスで出す。受け取った入力の値（起動の引数、設定ファイルに書いた値。CF6 の `{value}` など）は、受け取ったまま出す（絶対パスにすると、誤りの中身が変わるため）。対処の行に書くコマンド（`venv/bin/python3 scripts/fetch_tiles.py` など）は、ソースツリーの根で打つ形で書く。

ログファイルの行（各行の先頭の時刻は HLD 5.7.2 の 3「行の書式」。下は時刻の後の文面）。L1〜L3 は、ログファイルにこの文面を時刻付きで書き、標準出力にも時刻なしで同じ文面を出す（[SRS NFR-007](20_SRS.md#nfr-007-ログ出力)の「通常のログは標準出力とログディレクトリに同時に出す」と、HLD 5.7.2 の 3「行の書式」の「画面に出すのと同じ文面」による）:

| 記号 | 行 | 文面 |
|---|---|---|
| L1 | 始まりと引数（ログファイルの最初の行） | `開始: {program} {args}`。`{args}` は起動の引数（プログラムの名前を含まない）を、受け取った順に、下の引用の決まりで 1 つずつ書いて空白 1 つでつないだもの。引数が無ければ `開始: {program}` |
| L2 | 設定 | `設定ファイル: {config_path}` の 1 行の後、`load_config` に渡したキーごとに `_CONFIG_KEYS` の順で `設定: [{section}] {key} = {value}（{source}）`。`{source}` は、`from_file` が真なら `ファイル`、偽なら `デフォルト`（値が `None` のときも `デフォルト`）。値が `None` なら `{value}` を `未設定` |
| L3 | 終わり | `終了: 終了コード {code}、終了時刻 {end}、所要時間 {sec} 秒`。`{end}` は先頭の時刻と同じ書式、`{sec}` は `f'{秒:.3f}'`。シグナルで止まったときは `終了: 終了コード {code}（{signame} を受けて止まった）、終了時刻 {end}、所要時間 {sec} 秒`（`{signame}` は `signal.Signals(signum).name`。C++ は `SIGINT` か `SIGTERM` の名前） |

引用の決まり（L1 の `{args}`。[HLD 5.7.2](30_HLD.md#572-処理の流れ) の 4「始まりと終わりの行」の「最初の行にプログラムの名前と、起動の引数を受け取ったとおりに書く」を、引数の切れ目と中身が読み取れる形で 1 行に書くため）: 引数が空でなく、どの字も ASCII の英数字か `_@%+=:,./-` のどれかなら、そのまま書く。それ以外は、`'` で囲み、中の `'` を `'"'"'` に置き換える（空の引数は `''`）。Python の `shlex.join` と同じ結果になる（Python は `shlex.join(argv)` を使ってよい）。引数に改行があれば、その改行でファイルの行が分かれ、分かれた各行に時刻を付ける（[2.1.3](#213-関数の細部)の `_emit`）。bash の `run_pipeline` は L2 を書かない（[HLD 3.3.3](30_HLD.md#333-関数)の `open_log`）。

引用の決まりを当てる範囲: 受け取った起動の引数とその値（`{arg}`・`{value}`、L1 などの `{args}` は各引数を 1 つずつ引用して空白 1 つでつなぎ、全体は囲まない）、受け取った文字列を丸ごと出すもの（5.1 の `{output}`）、対処の行のコマンドに入れる値（`{config_opt}` の設定ファイルのパス）。メッセージの対象として出すパス（`{path}` など）は引用しない。

全体に共通する場面のメッセージ（HLD 2.5.3 の表と[HLD 5.7.3](30_HLD.md#573-異常系)の表の場面のうち、今回の分。`{config_path}` は `start_log` に渡された `Config` の `path`〈設定ファイルの絶対パス〉）:

| 記号 | 場面 | 1 行目（`ERROR:` と空白 1 つの後） | 2 行目（`対処:` と空白 1 つの後） | 終了コード |
|---|---|---|---|---|
| G1 | 同時起動 | `同じデータ置き場で別のコマンドが動いている: {lock_path}` | `動いているコマンドが終わってから起動し直す` | 1 |
| G2 | ロックファイルを開けない・ロックを掛けられない | `ロックファイルを開けないか、ロックを掛けられない: {lock_path}: {reason}` | `設定ファイルの data_dir と、そのディレクトリの書き込みの権限を確かめる` | 1 |
| G3 | ログの出力先を用意できない | `ログの出力先を用意できない: {path}: {reason}`（`{path}` は `log_dir` か、開けなかったログファイル） | `設定ファイル {config_path} の log_dir と、ディレクトリの権限を確かめてから起動し直す` | 1 |
| G4 | 同じ名前のログファイルが既にある | `同じ名前のログファイルが既にある: {path}` | `1 秒以上おいて起動し直す` | 1 |
| G5 | ログファイルに書けなくなった | `ログファイルに書けなくなった: {path}: {reason}` | `ディスクの空きとログファイルの権限を確かめてから起動し直す` | 1 |
| G6 | 終わりの行だけを書けなかった | `ログファイルに終わりの行を書けなかった: {path}: {reason}` | `ディスクの空きとログファイルの権限を確かめる。終了コード 1 はログが欠けたことを示し、書き終えた成果物は消していない` | 1 |
| G7 | 捕まらなかった例外 | `予期しない例外で止まった: {type}: {message}`（`{type}` は例外のクラス名 `exc_type.__name__`、`{message}` は `str(exc)`。`{message}` に改行があれば、`log_error` の決まりで行が分かれる。C++ は `{type}` を例外の型の名前〈`abi::__cxa_demangle` で読める形にしたもの〉、`{message}` を `what()` にする） | `このメッセージと続く Traceback をログファイルから（ログに書けなかったときは画面から）写して開発者に知らせる`（C++ は Traceback を出さないので、`このメッセージをログファイルから（ログに書けなかったときは画面から）写して開発者に知らせる`） | 1（シグナルを受けた後の後始末で上がった例外なら 128＋シグナルの番号。[2.1.3](#213-関数の細部)の `_finish_log` の 2） |

誤りの文面は、その誤りを確かめる部品か関数の節に置く（2.1 では CF1〜CF7・A1〜A5・R1〜R3、5.2 では RA1・RA2・RP1）。同じ入力（同じ設定のキー、同じファイル）を 2 つ以上のモジュールが同じ確かめで見る誤りは、終了コードによらず、下の表に置き、各モジュールの節から指す。各プログラムの起動の引数の誤り（3.1 の BA1〜BA4、4.1 の TA1〜TA4、5.1 の PA1〜PA5 など）は、文面が同じになっても、それぞれのモジュールの節に置く（[1.2](#12-lld-の規約)。確かめるのはそれぞれの引数で、使える引数の案内も違う）。

設定の相互制約（[HLD 2.3.3](30_HLD.md#233-検証と記録)）。確かめるのは、5.2 の `resolve_config`、CMP4（地形解析エンジン）の `analyze_terrain`（[6.1](#61-analyze_terrain_launch) の `_check_cross`）、CMP5（統合・突合）の `merge_peaks` で、同じ文面を出す。

| 記号 | 場面 | 1 行目（`ERROR:` と空白 1 つの後） | 2 行目（`対処:` と空白 1 つの後） | 終了コード |
|---|---|---|---|---|
| CX1 | 一次フィルタ閾値が最終フィルタ閾値以上 | `プロミネンス一次フィルタ閾値が最終フィルタ閾値以上: [analysis] prominence_primary_m = {primary}（{primary_source}）、[merge] prominence_final_m = {final}（{final_source}）（{config_path}）` | `[analysis] prominence_primary_m を [merge] prominence_final_m より小さくする（100 以上 {final} 未満の整数）` | 2 |

`{primary}`・`{final}` は使う値（デフォルトのときはデフォルト値）、`{primary_source}`・`{final_source}` は L2 の `{source}` と同じく `ファイル` か `デフォルト`、`{config_path}` は設定ファイルの絶対パス（`Config` の `path`）。

取得完了の記録（[2.3](#23-ファイルの名前と書き方)）。確かめるのは、CMP2（タイル取得）の `fetch_tiles` の `read_fetch_record`（[4.1.3](#413-関数の細部)）と、bash の `run_pipeline` の `check_fetch_record`（[5.1.3](#513-関数の細部)）で、同じ記録の同じ誤りをどちらで見つけても同じに案内する。

| 記号 | 場面 | 1 行目（`ERROR:` と空白 1 つの後） | 2 行目（`対処:` と空白 1 つの後） | 終了コード |
|---|---|---|---|---|
| FC2 | 取得完了の記録が読めないか、書式が違う | `取得完了の記録が読めないか、書式が違う: {path}: {detail}` | `{path} を消してから、venv/bin/python3 scripts/fetch_tiles.py{config_opt} を --mesh なしで起動し直す（--mesh を付けると、記録はそのメッシュだけになる）` | 1 |

`{path}` は記録の絶対パス。`{detail}` は、読めなければ `{reason}`（作り方は各モジュールの節の前置き）、書式が違えば最初の違う行の `{line_no} 行目が 4 桁の数字でない: {line}`。`{config_opt}` は各モジュールの節のとおり（`--config` を渡されたときは空白 1 つと `--config` と空白 1 つと設定ファイルのパスを引用したもの、渡されなかったときは空）。記号は 5.1 の FC1（記録に無いメッシュがある）と並べて読めるように FC2 とする。

通常のログの共通の形（[HLD 5.7.2](30_HLD.md#572-処理の流れ) の 5「途中経過」・7「結果の要約」。中身はモジュールの節で決め、行の頭と形はここに合わせる）:

- 途中経過（CMP2 と CMP4 が出す）: `途中経過: {what} {done}/{total}（{pct}%）`。`{what}` は何の取得か解析か（モジュールの節で決める）、`{done}` は終えた数、`{total}` は全件数、`{pct}` は `done * 100 // total`（整数部）。`{pct}` が前に出した値（初めは 0）より大きくなったときだけ出し、`{total}` が 0 なら出さない。
- 結果の要約: 1 行目を `結果の要約:` と空白 1 つで始める。2 行目以降が要るときは、1 回の出力で改行でつないで出す。途中で止まったとき（終了コード 1、シグナル）は、1 行目に止まったことを `止まった` の語で書く（`結果の要約: 途中で止まった。…` など）。

### 2.3 ファイルの名前と書き方

置き場の正本は HLD（[2.6.4](30_HLD.md#264-ディレクトリ構成)、[2.9.3](30_HLD.md#293-同時起動の排他)、[4.1.2](30_HLD.md#412-処理の流れ)）で、ここは HLD が LLD に送った名前を決める。今は 2.1・3.1・4.1・5.1・6.3・6.4・6.5・6.7・6.8・6.9 が使う分だけを書いてある。

- ロックファイル: `data_dir` の直下の `findsummits.lock`。中身は空のまま使い、消さない（HLD 2.9.3）。Python は `acquire_lock`、bash は `run_pipeline` の `acquire_lock` が同じ名前を使う。
- 取得完了の記録: `data_dir` の `tiles/` の直下の `fetch_complete.txt`（HLD 4.1.2 の「取得完了の記録」）。中身は、取得を終えた 1 次メッシュのコードを 1 行 1 件で、ASCII の数字 4 字に改行（LF）を付けて書く（BOM・空白・CR・空行・`#` の行を書かない。昇順に並べる）。0 件なら空のファイル。読む側（CMP2 の `fetch_tiles` の `read_fetch_record`〈[HLD 3.2.3](30_HLD.md#323-関数)〉と、bash の `run_pipeline` の `check_fetch_record`〈[5.1](#51-run_pipeline)〉。どちらもこの読み方にする）は、空のファイルを行の無い記録（0 件）とし、そのほかは最後の LF を 1 つ除いてから LF で行に分け、どの行も ASCII の数字 4 字ちょうどでなければ書式が違うとする（最後の行の後の LF は無くてもよい。同じコードの重なりは 1 件とする）。読む側が `--mesh` のファイルの読み方（空白・`#` の行を許す）にしないのは、記録がツールだけが書くファイルで、[HLD 4.1.2](30_HLD.md#412-処理の流れ)が「4 桁の数字でない行があれば」止まると決めているため（壊れた記録を読み飛ばさない）。書き方は、下の一時ファイルの決まりに従う（[4.1.3](#413-関数の細部) の `write_fetch_record`）。Python は `fetch_record_path`、bash は `run_pipeline` の `fetch_record_path` が同じ名前を使う。
- 標高タイルのキャッシュ: `data_dir` の `tiles/` の下の `<サービス名>/<z>/<x>/<y>.png`（[HLD 4.1.2](30_HLD.md#412-処理の流れ) の 7「タイルを次の順に取得する」、[SRS §8.1](20_SRS.md#81-内部データ一覧) の No.5）。サービス名とズームは、DEM5a が `dem5a_png`・DEM5b が `dem5b_png`・DEM5c が `dem5c_png` でズーム 15、DEM10b が `dem_png` でズーム 14（[4.1](#41-fetch_tiles) の `_KINDS` と同じ）。`<z>`・`<x>`・`<y>` は 10 進。書くのは 4.1 の `fetch_tiles` だけで、あるかを見るのは [6.3](#63-analyze_terrain_window) の `check_mesh_tiles`、読むのは [6.4](#64-analyze_terrain_grid) の `read_tile`（パスを組み立てるのは `build_tile_elevation`）。
- per-mesh CSV: `data_dir` の `results/csv/` の下の `<解析識別子>.csv`（[HLD 4.7.2](30_HLD.md#472-処理の流れ)、[SRS §8.1](20_SRS.md#81-内部データ一覧)）。書くのは [6.7](#67-analyze_terrain_csv) の `write_peak_csv` だけで、下の一時ファイルの決まりで `<解析識別子>.csv.tmp` に書いてから置き換える。読むのは、CMP5（統合・突合）の `merge_peaks`（[HLD 4.8.2](30_HLD.md#482-処理の流れ) の 2「読むファイルを選ぶ」は、名前が `.csv` で終わるものだけを選ぶので、`.tmp` で終わる名前は読まない）と、広域モードの 6.7 の `read_back_peak_csv`。
- per-mesh ピーク候補 GeoJSON: `data_dir` の `results/csv/` の下の `<解析識別子>.geojson`（通常解析だけ。[HLD 4.16.2](30_HLD.md#4162-処理の流れ)の「書き出し」、[SRS §8.1](20_SRS.md#81-内部データ一覧) の No.9、ADR-SRS-029）。書くのは [6.8](#68-analyze_terrain_zone) の `write_zone_geojson` だけで、下の一時ファイルの決まりで `<解析識別子>.geojson.tmp` に書いてから置き換える。読むのは CMP5（統合・突合）の `merge_zones`（[HLD 4.18.2](30_HLD.md#4182-処理の流れ)の 1「読むファイルを選ぶ」は `3-<meshcode>.geojson` の名前だけを選ぶので、`.tmp` で終わる名前は読まない）。
- 解析済みウィンドウメッシュ集合（`.meshset`）: `data_dir` の `results/csv/` の下の `<解析識別子>.meshset`（[HLD 4.4.2](30_HLD.md#442-処理の流れ) の「`.meshset` の形式」、[SRS §8.1](20_SRS.md#81-内部データ一覧) の No.13）。書くのは [6.9](#69-analyze_terrain_record) の `write_meshset` だけで、下の一時ファイルの決まりで `<解析識別子>.meshset.tmp` に書いてから置き換える。読むのは [6.3](#63-analyze_terrain_window) の `is_pattern_covered`（名前の一致で選ぶので、`.tmp` で終わる名前は読まない）と `read_meshset`。
- 標高地形図: `data_dir` の `images/` の下の `<解析識別子>_terrain.png`（[SRS §6.2.3](20_SRS.md#623-標高地形図)）。書くのは [6.5](#65-analyze_terrain_image) の `write_terrain_png` だけで、下の一時ファイルの決まりで `<解析識別子>_terrain.png.tmp` に書いてから置き換える。読むプログラムは無い（利用者が開く）。
- 一時ファイル: 出力を一時ファイルに書いてから置き換えるモジュール（今は 3.1・4.1・6.5・6.7・6.8・6.9。CMP4〜CMP6 の節も、書くときにこれに従う）は、出力と同じディレクトリに、出力のファイル名の後に `.tmp` を付けた名前（`regions.geojson` なら `regions.geojson.tmp`）で一時ファイルを書く。名前は固定にする（同じ `data_dir` で動く利用者向けのコマンドは 1 つだけで〈[HLD 2.9.3](30_HLD.md#293-同時起動の排他)〉、内部の起動口は CMP3 のロックの下で動くので、名前が重ならない。プロセスの番号を入れると、強制終了のたびに一時ファイルが増え、消す決まりが別に要る）。前の起動が強制終了で残した一時ファイルは、次の起動が同じ出力を書くときに、開いて中身を捨てて上書きする。同じ出力をもう書かなければ（CMP2 で、止まった後に取らなくなったタイルなど）一時ファイルは残るが、読む側は正規の名前しか読まないので害は無く（CMP2 のタイルの一時ファイルは `.png` で終わらない。[HLD 4.1.2](30_HLD.md#412-処理の流れ) の表の後の段落）、消す決まりは置かない。手順は「書く」と「置き換える」の 2 段に分け、2 段の間に何をするか（いくつの一時ファイルを書き終えてから、どの順で置き換えるか）と、置き換えに失敗したときに一時ファイルを消すか残すか（3.1 は残し、4.1・6.5・6.7・6.8・6.9 は消す）は、そのモジュールの節で決める。書く（Python）: `open(<一時ファイル>, 'wb')`（テキストは `open(<一時ファイル>, 'w', encoding='utf-8', newline='\n')`）で開き、書き、`flush()`、`os.fsync(f.fileno())`、閉じる（`fsync` は、置き換えた後に電源が落ちて中身の無いファイルが残るのを防ぐため）。開く・書く・flush・fsync・閉じるのどれかで `OSError` になったら、その一時ファイルを `os.remove` で消してから（消せないときの `OSError` は無視する）、そのモジュールのメッセージで止まる（同じ処理で先に書き終えたほかの一時ファイルも消すかは、モジュールの節で決める）。置き換える（Python）: `os.replace(<一時ファイル>, <出力>)`。書く（C++）: `open(<一時ファイル>, O_WRONLY | O_CREAT | O_TRUNC | O_CLOEXEC, 0666)` で開き、`write` を全部書くか `EINTR` のほかの失敗まで繰り返し（[6.12.3](#6123-関数の細部) の `_write_all` と同じ形）、`fsync`、`close`（`fsync` の理由と、前の起動の残りを開いて中身を捨てて上書きすることは Python と同じ）。どれかが失敗したら、`errno` を控え、開くことに成功していて、まだ `close` を呼んでいなければ `close` し（結果は見ない。`close` が失敗したときはもう一度呼ばない。`open` が失敗したときは `close` するものが無いので呼ばない）、一時ファイルを `unlink` で消してから（消せないときは無視する。`unlink` は `open` が失敗したときも含め、どの失敗でも呼ぶ。一時ファイルの名前に、先の無いシンボリックリンクなどが残っていることがあるため）、そのモジュールのメッセージで止まる（`{reason}` は控えた `errno` の文。1.2 の C++ の規約）。置き換える（C++）: `rename(<一時ファイル>, <出力>)`。

### 2.4 言語ごとに別に実装する式のテストベクトル

HLD の [DEC6](30_HLD.md#225-設計判断決めたこと理由却下した案)「メッシュ・タイル変換の二重実装を許容」のとおり、`mesh_to_latlon`・`latlon_to_tile` を Python（2.1）・C++（CMP4 の「変換」の群。[6.10](#610-analyze_terrain_convert)）・JavaScript（`index.html` の「3.9 と同じ決まり」の群）で別に実装し、`tile_to_latlon` を Python（3.1）と C++（6.10）で別に実装し（[HLD 3.1.3](30_HLD.md#313-関数)）、`latlon_to_mesh`・`latlon_to_z15_pixel`・`z15_pixel_center_latlon` を Python（CMP5。[HLD 3.5.3](30_HLD.md#353-関数)・[3.5.4](30_HLD.md#354-コンポーネント内の共通部品)）と C++（6.10）で別に実装し、この節の表で一致を確かめる。後の 3 つの関数のテストベクトルは、[HLD 4.7.1](30_HLD.md#471-目的と範囲)の対象外の行が LLD に送っているものである。テストのコードとこの表の置き場とテストのレベルは、[テスト方針書 3.3](02_test_policy.md#33-期待値の根拠)で決めた（各言語の UT にこの表の行を写して期待値にする。[HLD 2.2.1](30_HLD.md#221-目的と範囲)の対象外の行）。今は `mesh_to_latlon`・`latlon_to_tile`・`tile_to_latlon`・`latlon_to_mesh`・`latlon_to_z15_pixel`・`z15_pixel_center_latlon` と、メッシュの取得範囲の決まりの分だけを書いてある。

計算の決まり（どの言語も IEEE 754 の倍精度で、書いた順に左から計算する。式の正本は用語集の[メッシュコード → 緯度経度](00_GLOSSARY.md#mesh-to-latlon)と[緯度経度 → XYZ タイル番号](00_GLOSSARY.md#latlon-to-tile)）。`n = 2^z` は倍精度の値にする。整数の値（`2 × aa`・`x`・`y`、下の取得範囲の決まりの 3 の `x_e`）は、割る前に倍精度にし、整数どうしの割り算をしない（C++ で整数の型のまま `x / n` と書くと整数の割り算になり、表 3 の (1, 1, 1) の経度が −180 になる）:

- `mesh_to_latlon`: 南端の緯度 = `(2 × aa) / 3`（`2 × aa` を整数で求め、3 で 1 回だけ割る）。北端の緯度 = `(2 × (aa + 1)) / 3`。西端の経度 = `100 + bb`、東端の経度 = `101 + bb`。
- `latlon_to_tile`: `n = 2^z`。`x = floor(((lon + 180) / 360) × n)`。`r = (lat × π) / 180`（`math.radians` のような 1 つの関数にまとめない。掛ける順で値が変わるため）。`y = floor(((1 − ln(tan(r) + 1 / cos(r)) / π) / 2) × n)`。`π` は言語の標準の定数（Python の `math.pi`、C++ の `std::numbers::pi`、JavaScript の `Math.PI`。どれも同じ倍精度の値）。`tan`・`cos`・`ln` は言語の標準のもの。
- `tile_to_latlon`: `n = 2^z`。北西端の経度 = `((x / n) × 360) − 180`。北西端の緯度 = `(atan(sinh(π × (1 − (2 × y) / n))) × 180) / π`（`2 × y` を先に求めて `n` で割り、`1` から引き、`π` を掛け、`sinh`、`atan`、`180` を掛け、`π` で割る。この順に計算する）。`x`・`y` は小数でもよい（[HLD 3.1.3](30_HLD.md#313-関数) の表の「タイル番号（小数を含む）」）。南東端は `x + 1`・`y + 1` を同じ式に入れる。`sinh`・`atan` は言語の標準のもの（Python の `math.sinh`・`math.atan`）。式の正本は用語集の[XYZ タイル番号 → 緯度経度](00_GLOSSARY.md#tile-to-latlon)。
- `latlon_to_mesh`: 上 2 桁 `aa = floor((lat × 3) / 2)`、下 2 桁 `bb = floor(lon) − 100`（`lat × 3` を先に求めて 2 で割る。2 で割るのは丸めが無いので、`lat × 1.5` と同じ値になる）。`aa` と `bb` がどちらも 0〜99 のときのコードは、それぞれを 2 桁の 10 進（1 桁なら前に `0`）でつないだ 4 桁。0〜99 に入らないとき（NaN を含む）の扱いは、各言語の節で決める（C++ は 6.10）。四則演算と `floor` だけで決まるので、どの言語も同じコードになる。式の正本は用語集の[緯度経度 → メッシュコード](00_GLOSSARY.md#latlon-to-mesh)。
- `latlon_to_z15_pixel`: `latlon_to_tile(lat, lon, 23)` の `(x, y)` を全球の Z15 の画素の座標 `(gx, gy)` とする（Z15 の 1 画素は z=23 の 1 タイル。[HLD 4.7.2](30_HLD.md#472-処理の流れ) の 5「対象ピークの照合」）。
- `z15_pixel_center_latlon`: `tile_to_latlon(gx + 0.5, gy + 0.5, 23)`（`gx + 0.5`・`gy + 0.5` は倍精度で求める。2²³ より小さい整数に 0.5 を足すので丸めが無い）。経度は `((gx + 0.5) / 2²³) × 360 − 180` で、割るのは 2 の冪、`× 360` の積は 53 ビットに収まるので丸めが無く、どの言語も `==` で等しい。緯度は `sinh`・`atan` を通るので、表 3 と同じく差の絶対値が `1e-12`（度）以下なら一致とする（[HLD 4.7.2](30_HLD.md#472-処理の流れ) の 3「ピークの緯度経度を求める」）。

期待値の導き方: 用語集の式を上の順に倍精度で計算した値で、2026-10-18 に CPython で求めた。`tan`・`cos`・`ln` は言語で最後の桁が違いうるので、表 2 の行は、`floor` の前の値と最も近い整数の差が 0.016 以上ある点か、`floor` の前の値がちょうど整数になる点（経度 −180・0・135 と緯度 0。緯度 0 は `tan(0) = 0`・`cos(0) = 1`・`ln(1) = 0` で、どの言語も正確な値になる）だけにした（日本全土1次メッシュコードリストの 175 メッシュの四隅を、ズーム 14・15 で調べ、経度 135 度のほかは差がどれも 0.016 以上だった）。

表 1 の 4 つの値は、どの言語も期待の値と `==` で等しい（整数と、整数を 3 で 1 回だけ割った値で、四則演算だけで決まるため）。

表 1（`mesh_to_latlon`。値は倍精度の値の最短の 10 進表記）:

| メッシュ | 南端の緯度 | 西端の経度 | 北端の緯度 | 東端の経度 |
|---|---|---|---|---|
| `3036` | 20.0 | 136.0 | 20.666666666666668 | 137.0 |
| `3622` | 24.0 | 122.0 | 24.666666666666668 | 123.0 |
| `4934` | 32.666666666666664 | 134.0 | 33.333333333333336 | 135.0 |
| `5235` | 34.666666666666664 | 135.0 | 35.333333333333336 | 136.0 |
| `5339` | 35.333333333333336 | 139.0 | 36.0 | 140.0 |
| `6848` | 45.333333333333336 | 148.0 | 46.0 | 149.0 |

表 2（`latlon_to_tile`。緯度と経度は表 1 の値をそのまま渡す）:

| 緯度 | 経度 | z | x | y |
|---|---|---|---|---|
| 20.0 | 136.0 | 14 | 14381 | 7262 |
| 20.666666666666668 | 137.0 | 14 | 14427 | 7230 |
| 20.0 | 136.0 | 15 | 28763 | 14525 |
| 20.666666666666668 | 137.0 | 15 | 28854 | 14460 |
| 24.0 | 122.0 | 15 | 27488 | 14132 |
| 24.666666666666668 | 123.0 | 14 | 13789 | 7033 |
| 32.666666666666664 | 134.0 | 15 | 28580 | 13235 |
| 33.333333333333336 | 135.0 | 14 | 14336 | 6581 |
| 33.333333333333336 | 135.0 | 15 | 28672 | 13162 |
| 34.666666666666664 | 135.0 | 15 | 28672 | 13016 |
| 35.333333333333336 | 139.0 | 15 | 29036 | 12942 |
| 36.0 | 140.0 | 15 | 29127 | 12867 |
| 45.333333333333336 | 148.0 | 14 | 14927 | 5872 |
| 46.0 | 149.0 | 15 | 29946 | 11657 |
| 0.0 | -180.0 | 0 | 0 | 0 |
| 0.0 | 0.0 | 1 | 1 | 1 |

`24.666666666666668`・`123.0`・ズーム 14 の y = 7033 は、差が 0.016 の最も近い点で、言語の違いで結果が割れないかを見る行。経度 135 の行は x がちょうど整数になる点。

表 3 は、`tile_to_latlon` の式を上の順に倍精度で計算した値で、2026-10-22 に CPython 3.14.8 で求めた。経度は四則演算だけで決まるので、どの言語も `==` で等しくなる。緯度は `sinh`・`atan` を通り、言語の標準の関数で最後の桁が違いうるので、期待の値との差の絶対値が `1e-12`（度）以下なら一致とする（`floor` で丸める `latlon_to_tile` の表 2 と違い、値をそのまま比べるため。この許容差は変換の関数の値を比べるためのもので、タイルの矩形と北方領土のポリゴンが辺で接するだけか重なるかの判定〈[3.1.3](#313-関数の細部)〉が言語で同じになることまでは言わない。北方領土除外タイルリストを作るのは Python の 3.1 だけである）。

表 3（`tile_to_latlon`。戻り値は（北西端の緯度, 北西端の経度）。値は倍精度の値の最短の 10 進表記）:

| x | y | z | 緯度 | 経度 |
|---|---|---|---|---|
| 0 | 0 | 0 | 85.05112877980659 | -180.0 |
| 1 | 1 | 0 | -85.05112877980659 | 180.0 |
| 1 | 1 | 1 | 0.0 | 0.0 |
| 14381 | 7262 | 14 | 20.014645445341362 | 135.98876953125 |
| 29127 | 12867 | 15 | 36.00467348670187 | 139.998779296875 |
| 29128 | 12868 | 15 | 35.99578538642033 | 140.009765625 |
| 28672 | 13162 | 15 | 33.33970700424027 | 135.0 |
| 29946 | 11657 | 15 | 46.004593255744815 | 148.99658203125 |
| 29127.5 | 12867.5 | 15 | 36.000229561780024 | 140.0042724609375 |

**メッシュの取得範囲の決まり**: 1 次メッシュの取得範囲（タイル番号の範囲 x_min〜x_max・y_min〜y_max。両端を含む）は、CMP2 の `mesh_tile_range`（[4.1](#41-fetch_tiles)）と、CMP4 の `tile_range`（[6.4](#64-analyze_terrain_grid)。解析対象メッシュの bounding box の四隅に同じ決まりを当てる）と、CMP4 の `check_mesh_tiles`（[6.3](#63-analyze_terrain_window)。メッシュ 1 つずつに、ズーム 15 と 14 で同じ決まりを当てる）で同じに求める（[HLD 4.1.1](30_HLD.md#411-目的と範囲) の対象外の行、[HLD 4.4.2](30_HLD.md#442-処理の流れ) の「解析範囲標高グリッドの生成」の 1「範囲を求める」、HLD の [DEC6](30_HLD.md#225-設計判断決めたこと理由却下した案)「メッシュ・タイル変換の二重実装を許容」）。

1. `(x_min, y_min)` は `latlon_to_tile(北端の緯度, 西端の経度, z)`。
2. `(x_e, y_max)` は `latlon_to_tile(南端の緯度, 東端の経度, z)`。
3. `x_e` のタイルの西の境目の経度 `((x_e / 2^z) × 360) − 180`（上の `tile_to_latlon` の経度の式と同じ順。`x_e / 2^z` は 2 の冪で割るので丸めが無く、続く `× 360` と `− 180` もこの範囲の値では丸めが無いので、どの言語でも同じ値になる）が東端の経度と `==` で等しければ `x_max = x_e − 1`、違えば `x_max = x_e`。東端がタイルの境目に重なるとき、境目の東の列はメッシュの外なので含めない（[SRS FR-001](20_SRS.md#fr-001-標高タイル事前取得) の「そのメッシュをカバーする最小範囲」）。含めると、経度 135 度で終わる 5 つのメッシュ（`4934`・`5034`・`5134`・`5234`・`5334`）で、メッシュの外の列のタイルがそのメッシュの取得範囲に入り、CMP2 の DEM10b がすべて未整備かの検査と海の位置の数にメッシュの外のタイルが混ざる。
4. 南端は 3 のように確かめない（`y_max` をそのまま使う）。日本全土 1 次メッシュコードリストの 175 メッシュの南端の緯度は、ズーム 14・15 で、`floor` の前の値と最も近い整数の差がどれも 0.016 以上あり、タイルの境目に重ならない（上の「期待値の導き方」の段落が調べた値）。緯度は `tan`・`cos`・`ln` を通るので、`==` で比べると言語で結果が割れうる。西端と北端は、境目に重なっても `latlon_to_tile` の `floor` がメッシュの中の側のタイルを返すので、確かめない。

表 4（`mesh_tile_range`。メッシュと z を渡し、x_min・x_max・y_min・y_max を返す。値は上の式と決まりで 2026-10-23 に CPython 3.14.8 で求めた。CMP4 の `tile_range` は、メッシュ 1 つの集合を渡したときに、ズーム 15 の行と同じ値を返す。複数のメッシュの bounding box の行は表 8）:

| メッシュ | z | x_min | x_max | y_min | y_max |
|---|---|---|---|---|---|
| `4934` | 15 | 28580 | 28671 | 13162 | 13235 |
| `4934` | 14 | 14290 | 14335 | 6581 | 6617 |
| `5235` | 15 | 28672 | 28763 | 12942 | 13016 |
| `3622` | 14 | 13744 | 13789 | 7033 | 7066 |
| `5339` | 15 | 29036 | 29127 | 12867 | 12942 |
| `6848` | 15 | 29855 | 29946 | 11657 | 11744 |

`4934` の 2 行は東端が経度 135 度でタイルの境目に重なり、3 の決まりで `latlon_to_tile` の値（ズーム 15 は 28672、ズーム 14 は 14336）より 1 小さい。`5235` は西端が経度 135 度で、境目の東のタイル（28672）から始まる。`5235` の `y_min` と `5339` の `y_max` が同じ 12942 であるように、緯度 35.333… の境目のタイルの行は、南北に隣り合うメッシュ（`5235` と `5335`、`5239` と `5339` など）の両方の範囲に入る。

表 8（`tile_range`。メッシュの集合を渡し、ズーム 15 の x_min・x_max・y_min・y_max を返す。bounding box の四隅に上の決まりを当てる。値は上の式と決まりで 2026-10-27 に CPython で求めた）:

| メッシュの集合 | x_min | x_max | y_min | y_max |
|---|---|---|---|---|
| `4934`・`5034` | 28580 | 28671 | 13089 | 13235 |
| `5235`・`5336` | 28672 | 28854 | 12867 | 13016 |
| `4934`・`5235` | 28580 | 28763 | 12942 | 13235 |

`4934`・`5034` の行は、bounding box の東端が経度 135 度で、3 の補正が当たる。

**緯度経度と Z15 の画素の変換のテストベクトル**: `latlon_to_mesh`・`latlon_to_z15_pixel`・`z15_pixel_center_latlon` の表 5〜7 は、上の式と順で 2026-10-24 に CPython 3.14.8 で求めた。選んだ点は、[HLD 4.7.1](30_HLD.md#471-目的と範囲)の対象外の行が挙げる 4 つ（画素の中心の往復、経度 135° の境目、メッシュの南と西の境目に近い点、境目に最も近い中心の画素）で、どの行がどれに当たるかは各表の後に書く。境目に最も近い中心の画素は、日本の範囲（緯度 20〜46 度の 2/3 度ごと、経度 122〜154 度の 1 度ごと）の 1次メッシュの境目を全部調べて選んだ（緯度は約 1.33×10⁻⁷ 度、経度は約 4.77×10⁻⁷ 度。HLD の [DEC55](30_HLD.md#474-設計判断)「地理的範囲フィルタは CSV に書く値で判定する」の数と同じ）。表 6 の行の `floor` の前の値は、ちょうど整数（経度 −180・135 と緯度 0）か、最も近い整数から 0.43 以上離れている（画素の中心から戻す行は約 0.5、境目に乗る行の緯度の側が最も近く約 0.436。表 2 の 0.016 より大きく離れた点だけになった）ので、言語の `tan`・`cos`・`ln` の最後の桁の違いで結果が割れない。表 5 と表 6 の画素の中心の行の緯度経度は、表 7 の値を小数点 8 桁にしたもので、±5×10⁻⁹ 度ずらしても同じ画素とコードになる。8 桁にする関数は CMP4 では「CSV と早期終了」の群の `format_coord` なので、表は 8 桁にした後の数を入力に書く（UT が `format_coord` に頼らないため）。`format_coord` の UT は、表 7 の値を 8 桁にして表 5・6 の入力と同じ文字列になることを確かめる（[6.7.5](#675-ut-候補)）。

表 5（`latlon_to_mesh`。どの言語も期待のコードと等しい）:

| 緯度 | 経度 | コード |
|---|---|---|
| 35.5 | 139.5 | `5339` |
| 35.333333333333336 | 139.0 | `5339` |
| 34.666666666666664 | 135.0 | `5235` |
| 36.0 | 140.0 | `5440` |
| 35.33333334 | 139.5 | `5339` |
| 35.33333333 | 139.5 | `5239` |
| 35.5 | 138.99999999 | `5338` |
| 20.0 | 122.0 | `3022` |
| 21.33333320 | 136.49999857 | `3136` |
| 21.33337317 | 136.49999857 | `3236` |
| 26.50001531 | 127.00000048 | `3927` |
| 26.50001531 | 126.99995756 | `3926` |

1 行目はメッシュの内部の点。8 行目は `3022` の南西の隅で、2・3 行目と同じく南と西の境目がそのメッシュに入る点。2・3 行目は表 1 の南端と西端の値で、メッシュの南と西の境目はそのメッシュに入る。4 行目は `5339` の北東の隅で、北と東の境目は隣のメッシュに入る（[HLD 4.7.2](30_HLD.md#472-処理の流れ) の 4「地理的範囲フィルタ」）。5〜7 行目は境目のすぐ内と外。9〜12 行目は、境目に最も近い中心の画素とその隣の画素の中心（表 7）を 8 桁にしたもの。

表 6（`latlon_to_z15_pixel`。どの言語も期待の値と等しい）:

| 緯度 | 経度 | gx | gy |
|---|---|---|---|
| 85.05112693 | -179.99997854 | 0 | 0 |
| 36.00465613 | 139.99880075 | 7456512 | 3293952 |
| 34.99999777 | 134.99997854 | 7340031 | 3322709 |
| 34.99999777 | 135.00002146 | 7340032 | 3322709 |
| 35.0 | 135.0 | 7340032 | 3322709 |
| 26.50001531 | 127.00000048 | 7153618 | 3553537 |
| 26.50001531 | 126.99995756 | 7153617 | 3553537 |
| 21.33333320 | 136.49999857 | 7374984 | 3685300 |
| 21.33337317 | 136.49999857 | 7374984 | 3685299 |
| 46.00457835 | 148.99660349 | 7666176 | 2984192 |
| 0.0 | -180.0 | 0 | 4194304 |

5 行目は経度 135° の境目にちょうど乗る点で、境目の東の画素（`7340032` = 7 × 2²⁰）になる（HLD の [DEC54](30_HLD.md#474-設計判断)「ピークの座標は Z15 の画素の中心にする」の却下の項）。3・4 行目はその境目をはさむ 2 つの画素の中心。2 行目はタイル (29127, 12867) の北西の隅の画素（表 3 の行と同じタイル）。画素の中心の行（1〜4 行目と 6〜10 行目）は、表 7 の往復（中心を 8 桁にして戻すと同じ画素になる）。

表 7（`z15_pixel_center_latlon`。戻り値は（緯度, 経度）。値は倍精度の値の最短の 10 進表記）:

| gx | gy | 緯度 | 経度 |
|---|---|---|---|
| 0 | 0 | 85.05112692872285 | -179.99997854232788 |
| 7456512 | 3293952 | 36.004656128107385 | 139.99880075454712 |
| 7340031 | 3322709 | 34.99999776698518 | 134.99997854232788 |
| 7340032 | 3322709 | 34.99999776698518 | 135.00002145767212 |
| 7153617 | 3553537 | 26.50001530614219 | 126.99995756149292 |
| 7153618 | 3553537 | 26.50001530614219 | 127.00000047683716 |
| 7374984 | 3685299 | 21.333373174657144 | 136.49999856948853 |
| 7374984 | 3685300 | 21.333333199888905 | 136.49999856948853 |
| 7666176 | 2984192 | 46.004578351228716 | 148.99660348892212 |

`7153618`（経度）と `3685300`（緯度）が、日本の範囲の 1次メッシュの境目に最も近い中心の画素で、`7153617`・`3685299` はその隣（境目の反対の側）。`7666176`・`2984192` は表 1 の `6848` の北端（北緯 46 度）のすぐ北にある画素で、経度は東端 149 度の内側（タイル (29946, 11657) の北西の隅。表 3 の行と同じタイル）。

### 2.5 ビルドとテストの名前

[HLD 2.6.1](30_HLD.md#261-目的と範囲)の対象外の行は、Makefile の個々のターゲット名と変数名、テスト用の実行ファイルの名前を LLD に送っている。どのプログラムにも属さない項目なので、ここに置く（ADR-LLD-001 の Decision 7）。今は CMP4（地形解析エンジン）の C++ の分だけを書いてある。コンパイルとリンクの指定の正本は [HLD 2.6.5](30_HLD.md#265-ビルド構成)の表で、ここには写さない。

- CMP4 の実行ファイルは `build/analyze_terrain`（[HLD 3.4.1](30_HLD.md#341-プログラム)）。`src/` の `.cpp` をすべてコンパイルしてリンクする。`main` を持つのは `src/analyze_terrain.cpp` だけ（[6.1](#61-analyze_terrain_launch)）。
- テスト用の実行ファイルは、`tests/src/test_<群の名前>.cpp` ごとに 1 本の `build/test_<群の名前>`（6.12 は `build/test_common`、6.1 は `build/test_launch`、6.2 は `build/test_target`、6.3 は `build/test_window`、6.4 は `build/test_grid`、6.5 は `build/test_image`、6.6 は `build/test_scan`、6.7 は `build/test_csv`、6.8 は `build/test_zone`、6.9 は `build/test_record`、6.10 は `build/test_convert`。`<群の名前>` は 1.2 の C++ の規約のとおり）。そのテストのファイルと、`src/` の `.cpp` のうち `main` を持たないものすべてをコンパイルし、GoogleTest の `gtest_main` とリンクする（`main` は `gtest_main` のもの）。
- `main` の振る舞いを確かめるための試験用の実行ファイル `build/test_launch_main`: `src/analyze_terrain.cpp`・`src/launch.cpp`・`src/common.cpp` と `tests/src/stub_stage.cpp`（[6.1.5](#615-ut-候補) の段の進行のスタブ）をコンパイルしてリンクする（`gtest_main` はリンクしない。指定は CMP4 の実行ファイルと同じ）。`build/test_launch` が子のプロセスで起動する（6.1.5）。
- コンパイルとリンクの指定は HLD 2.6.5 の表のとおりで、テスト用の実行ファイルは `pkg-config --cflags --libs gtest_main` を足す。インクルードの探索先に `src` を足す（`-I src`）。中間のファイルは `build/obj/` に置く。
- `make test` は、`build/test_launch_main` とテスト用の実行ファイルをすべてビルドし（`build/test_launch_main` は実行しない。`build/test_launch` が起動する）、テスト用の実行ファイルを順に実行し、続けて `tests/scripts/` のテストを `venv/bin/python3 -m unittest discover -s tests/scripts -t .` で実行し、どれかが 0 以外で終われば 0 以外で終わる（HLD 2.6.5 の表の `make test`。Python の枠組みは[テスト方針書 3.4](02_test_policy.md#34-テストを先に書く進め方)）。

## 3. CMP1 行政区域前処理

この章は、CMP1（行政区域前処理）の 1 本のプログラム（[HLD 3.1.1](30_HLD.md#311-プログラム)）のモジュールを置く。CMP1 にコンポーネント内の共通部品は無い（[HLD 3.1.4](30_HLD.md#314-コンポーネント内の共通部品)）。

### 3.1 `preprocess_boundaries`

- **ID**: LLD-preprocess_boundaries
- **対応 HLD**: [3.1](30_HLD.md#31-cmp1-行政区域前処理)・[4.17](30_HLD.md#417-fr-017-n03-行政区域前処理データ準備)・[5.2](30_HLD.md#52-nfr-002-メモリ使用量)・[5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)
- **ファイル**: `scripts/preprocess_boundaries.py`

処理の正本は [HLD 4.17.2](30_HLD.md#4172-処理の流れ)（作り直しの条件と置き換えの順序の正本は [HLD 2.10.3](30_HLD.md#2103-フェーズのやり直し) の「フェーズ1」）で、関数の名前と役割と呼ぶ順は [HLD 3.1.3](30_HLD.md#313-関数) の表のとおり。この節は Python で書くための細部（型、データの持ち方、メッセージの文面、ログの行）だけを足す。[5.2](30_HLD.md#52-nfr-002-メモリ使用量)（メモリ）は、N03 の GeoJSON を読み込むときにフィーチャごとの元の辞書を捨てながら shapely のポリゴンに変えること（3.1.3 の `load_n03_features`）で受け、メモリのピークは実装の後に HLD 5.2.2 の「実測の計画」の 5 で測る。[5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)（再現性）は、出力のフィーチャとポリゴンの並びと JSON の書き方を入力の並びによらず決めること（3.1.3 の `build_regions`・`build_municipalities`・`write_temp_outputs`）と、`tile_to_latlon` を [2.4](#24-言語ごとに別に実装する式のテストベクトル) の表 3 で CMP4 とそろえることで受ける。結合のつなぎ目は `CMP1-INT1`・`CMP1-EXT1`・`CMP1-EXT2`（[HLD 3.1.5](30_HLD.md#315-結合のつなぎ目)）で、IT のケースは `60_IT.md` の `IT-CMP1-INT1-01`〜`06`・`IT-CMP1-EXT1-01`〜`05`・`IT-CMP1-EXT2-01`。

#### 3.1.1 ファイル割付

- 関数はすべて `scripts/preprocess_boundaries.py` 1 本に置く。`venv/bin/python3 scripts/preprocess_boundaries.py` で起動され（[HLD 3.1.1](30_HLD.md#311-プログラム)）、共通部品は `import common` で読む（2.1.1 と同じ）。shapely は `import shapely` と `from shapely.geometry import box, mapping, shape, MultiPolygon, Polygon`・`from shapely.geometry.polygon import orient`・`from shapely.errors import GEOSException` で読む（[環境定義](01_environment.md) の既存の依存。[HLD 4.17.2](30_HLD.md#4172-処理の流れ) の 5「市区町村の GeoJSON を展開する」）。ファイルの先頭のコメントに `# trace: LLD-preprocess_boundaries` を書く。起動の部分は `if __name__ == '__main__': main()`。
- UT のコードは `tests/scripts/test_preprocess_boundaries.py` に置く。各テストに `# trace: UT-preprocess_boundaries-NN` のコメントを付ける。テストの枠組みは 2.1.1 と同じく[テスト方針書 3.4](02_test_policy.md#34-テストを先に書く進め方)で選んだ。

#### 3.1.2 型とデータ

- 定数（モジュールの最上位。どれも内部）:
  - `_SOURCE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))`、`_JAPAN_MESH_LIST_PATH = os.path.join(_SOURCE_ROOT, 'params', 'mesh_list_japan.txt')`（[HLD 3.1.1](30_HLD.md#311-プログラム) の「自分の置き場から求め、起動した作業ディレクトリによらない」）。既定の設定ファイルは `common.DEFAULT_CONFIG_PATH`（[2.1.2](#212-型とデータ)）。
  - `_ZIP_NAME = re.compile(r'N03-([0-9]{8})_GML\.zip')`（`fullmatch` で使う。`\d` は全角の数字にも合うので使わない）。
  - `_NT_CODES = frozenset({'01695', '01696', '01697', '01698', '01699', '01700'})`（[HLD 4.17.2](30_HLD.md#4172-処理の流れ) の「北方領土除外タイルリストと北方領土除外メッシュリスト」）。
  - `_REGIONS: tuple[tuple[str, str, str], ...]`: HLD 4.17.2 の「地域と SOTA のコード」の表の 60 行を、表の順に（N03 の名前, `assoc`, `area_code`）で持つ（モジュールの定数として書き、実行時に HLD を読まない。値は HLD の表のとおりで、正本は HLD の表なので、変えるときは HLD を先に直す。表の順は `UT-preprocess_boundaries-15` の期待に使う）。`assoc` が `JA8` の 14 行が北海道の振興局で、`N03_002` で引く。ほかの 46 行は `N03_001` で引く。
  - 出力の名前: `_OUTPUT_NAMES = ('regions.geojson', 'municipalities.geojson', 'nt_excluded_tiles.txt', 'nt_excluded_meshes.txt')`（この順を、一時ファイルの並び、置き換えの順、要約の順に使う）、`_VERSION_NAME = 'n03_version.txt'`（[HLD 4.17.2](30_HLD.md#4172-処理の流れ) の「出力の置き場」の表）。置き場はどれも `os.path.join(<data_dir>, 'boundaries')`。
  - `_TILE_ZOOM = 15`、`_LIST_LIMIT = 10`（BV5・BV6 のメッセージに並べる件数の上限。[3.1.4](#314-メッセージ文面)）。
- `@dataclass(frozen=True) class N03Feature`: `index: int`（`features` の配列の中の位置。1 から数える。メッセージに出す）、`n03_001: object`・`n03_002: object`・`n03_004: object`・`n03_005: object`・`n03_007: object`（`properties` の同じ名前の値。JSON の値のまま〈`str`・`None`・数など〉。キーが無いか `properties` がオブジェクトでなければ `None`）、`geom_type: object`（`geometry` がオブジェクトならその `type` の値〈`type` のキーが無ければ `None`〉、`geometry` が無いか `null` かオブジェクトでなければ `None`）、`polygons: tuple[Polygon, ...]`（`geom_type` が `'Polygon'` ならその 1 つ、`'MultiPolygon'` なら含まれるポリゴンを配列の順に。どちらも `is_empty` が真のポリゴン〈`{"type":"Polygon","coordinates":[]}` など〉は含めない。ほかの種類と `None` のときは空のタプル。空のポリゴンを除くのは、`validate_n03` の BV7・BV8 がポリゴンの数で判定し、空のポリゴンは外接矩形が NaN になって後の計算を壊すため）。`N03_003`・`N03_006` は持たない（使わない）。
- 出力のフィーチャ: `dict`（GeoJSON の Feature のオブジェクト）。キーの順は `type`（`'Feature'`）、`properties`、`geometry`。`geometry` は `shapely.geometry.mapping(<幾何>)` の値（キーの順は `type`、`coordinates`）。地域の `properties` のキーの順は `assoc`・`area_code`・`region_name`、市区町村は `prefecture`・`municipality`・`code`（[SRS §8.2.1](20_SRS.md#821-n03-前処理済みファイル詳細仕様) の並び）。
- 除外タイル: `tuple[int, int]`（`(x, y)`、ズーム 15）。除外メッシュ: `str`（[2.1.2](#212-型とデータ) のメッシュコード）。
- モジュールの状態（内部。モジュールの最上位の変数で、初めは空の文字列）: `_n03_source: str`（`load_n03_features` の 1 が入れる、メッセージの対象のファイルを示す文 `<ZIP のパス> の N03-<YYYYMMDD>.geojson`。BV3〜BV8・BF2 の `{source}`）、`_config_opt: str`（`main` が `start_log` の後に入れる、[3.1.4](#314-メッセージ文面) の `{config_opt}` の値。BW1 と `{rerun}` を使うメッセージが使う）。
- モジュールの状態の理由: [HLD 3.1.3](30_HLD.md#313-関数) の表の `needs_rebuild`・`validate_n03`・`build_regions` などが受け取るものに、メッセージに要る対象のファイルと設定ファイルのパス（[HLD 4.17.3](30_HLD.md#4173-異常系) の「CMP1 の失敗」の行と「新しい版の N03 ZIP がある」の行）が無い。引数で渡すと HLD の表と食い違い、フィーチャごとに持たせるのは同じ値の重複になる。モジュールの状態は 2.1 の `_state` と同じ扱い。

#### 3.1.3 関数の細部

- 止まるときは、メッセージを出してから `sys.exit(<定数>)` を呼ぶ（[1.2](#12-lld-の規約) の終わり方の規約と [2.1.3](#213-関数の細部) の呼ぶ側の書き方の型をそのまま当てる）。`start_log` の後に止まるときは、`main` の `finally` が結果の要約を出す。
- 交差の判定: 「交差する」（[HLD 4.17.2](30_HLD.md#4172-処理の流れ) の「共通部分が面積を持つ」）は、`shapely.relate_pattern(<ポリゴン>, <矩形>, 'T********')`（内部どうしが交わる）が真であることとする。面積の値と比べない（浮動小数の閾値を置かない）。2 つの面の内部どうしが交われば共通部分は面積を持ち、境界で接するだけなら交わらない。
- 例外の受け方: 各関数が名前を挙げた例外だけを捕まえる（[1.2](#12-lld-の規約) の規約）。`SignalStop`・`LogWriteError` は捕まえない。
- 画面への出力の失敗（標準出力や標準エラー出力が読む相手の無いパイプなど）は、このモジュールでは特別に扱わず、[2.1.3](#213-関数の細部) の `log_info`・`log_warning`・`log_error` と `_finish_log` の決まりのままにする（`start_log` の前に止まる BA1〜BA4 などで標準エラー出力に書けないときの終了コードは、Python の既定のまま）。利用者が端末から起動するコマンドで、[5.2](#52-resolve_config) の `resolve_config` のように標準出力を別のプログラムが読む約束が無いため。
- `{reason}` は [2.1.4](#214-メッセージ文面) と同じ（`OSError` の `strerror`〈無ければ `str(e)`〉、`UnicodeDecodeError` なら `UTF-8 として読めない`）に加えて、`zipfile.BadZipFile`・`zlib.error`・`EOFError`・`NotImplementedError`・`json.JSONDecodeError`・`ValueError`・`TypeError`・`shapely.errors.GEOSException` は `str(e)` の 1 行目（空なら例外のクラス名）。

##### main（preprocess_boundaries）

`main() -> None`。[2.1.3](#213-関数の細部) の呼ぶ側の書き方の型に従い、次の順に行う。

1. `start = common.StartTime.now()`。
2. `args = _parse_args(sys.argv[1:])`（`--help` と引数の誤りは、ここで止まる）。`config_path` は `args.config` が `None` なら `common.DEFAULT_CONFIG_PATH`、それ以外は `args.config`（`load_config` が `os.path.abspath` する）。
3. `config = common.load_config(config_path, ('data_dir', 'log_dir'), ('data_dir',))`（[HLD 2.3.2](30_HLD.md#232-設定ファイル) の表で CMP1 が使うキー）。`data_dir`・`log_dir` はその値。`boundaries_dir = os.path.join(data_dir, 'boundaries')`。
4. `common.acquire_lock(data_dir)`。
5. `common.start_log(log_dir, config, 'preprocess_boundaries', sys.argv[1:], start)`。`_config_opt` に [3.1.4](#314-メッセージ文面) の `{config_opt}` の値を入れる（`args.config is not None` なら `' --config ' + shlex.quote(config.path)`、それ以外は空の文字列）。
6. `try` の前に、`completed = False`、`code = common.EXIT_OK`、要約のための状態（`counts: dict[str, int]`〈空。`地域`・`市区町村`・`除外タイル`・`除外メッシュ` の名前で件数を入れる〉、`replacing = False`、`outcome: str | None = None`、`zip_date: str | None = None`、`recorded: str | None = None`）を置く（[2.1.3](#213-関数の細部) の呼ぶ側の書き方の型）。`try` の中で次を呼ぶ（[HLD 3.1.3](30_HLD.md#313-関数) の呼ぶ順）:
   1. `zip_path, zip_date = find_n03_zip(os.path.join(data_dir, 'ref'))`。
   2. `needs_rebuild(boundaries_dir, args.rebuild, zip_date)` が偽なら、`recorded = _read_version(os.path.join(boundaries_dir, _VERSION_NAME))`、`outcome = 'skipped'`、`completed = True` にし、3〜8 を行わない（`if` で分ける。`return` で抜けると `finally` の後の `sys.exit(code)` に届かないので使わない）。
   3. `japan = common.read_mesh_list_file(_JAPAN_MESH_LIST_PATH, None)`（無い・読めない・誤りの行は R1〜R3 で 1。[HLD 4.17.2](30_HLD.md#4172-処理の流れ) の 4「日本全土リストを読む」）。
   4. `features = load_n03_features(zip_path, zip_date)`。`validate_n03(features)`。
   5. `regions = build_regions(features)`、`counts['地域'] = len(regions)`。`municipalities = build_municipalities(features)`、`counts['市区町村'] = len(municipalities)`。
   6. `nt, other = split_nt_polygons(features)`。`tiles = list_excluded_tiles(nt)`、`counts['除外タイル'] = len(tiles)`。`meshes = list_excluded_meshes(japan, nt, other)`、`counts['除外メッシュ'] = len(meshes)`。
   7. `temp_paths = write_temp_outputs(regions, municipalities, tiles, meshes, boundaries_dir)`。
   8. `replacing = True`。`replace_outputs(temp_paths, data_dir, zip_date)`。`outcome = 'rebuilt'`、`completed = True`。
7. `finally` で結果の要約を `common.log_info` で出す（[3.1.4](#314-メッセージ文面) の BL3〜BL5。`completed` が真なら `outcome` で BL3 か BL4、偽なら BL5）。
8. `sys.exit(code)`。

##### _parse_args（preprocess_boundaries）

`_parse_args(argv: Sequence[str]) -> _Args`（内部）。`@dataclass(frozen=True) class _Args`: `config: str | None`（`--config` の値。渡されなければ `None`）、`rebuild: bool`。

1. [1.2](#12-lld-の規約) の利用者向けの Python のコマンドの引数の受け方で読む。受け付ける名前は、`--config`（値を 1 つとる）、`--rebuild`・`--help`（値をとらない）だけ（[HLD 2.4.2](30_HLD.md#242-共通の書式)）。
2. 誤りは BA1（受け付けない引数）、BA2（値が無い）、BA4（同じ名前を 2 回）で、`common.log_error` で出して `sys.exit(common.EXIT_USAGE)`。1 つの引数が値をとらない名前に `=` を付けたもの（`--rebuild=x`・`--help=x`）なら、同じ名前を読んだことがあっても BA1 とする（BA1 の判定を BA4 の判定より先にする）。
3. `--help` は、[3.1.4](#314-メッセージ文面) の使い方の文を `sys.stdout.write` で出し、`sys.stdout.flush()` の後に `sys.exit(common.EXIT_OK)`。引数は左から 1 つずつ処理して、その場で 2 か 3 を行うので、`--help` より前の引数の誤り（BA1・BA2・BA4）は先に止まり、`--help` より後の引数は誤りも見ずに終わる（`--rebuild --help --foo` は 0、`--foo --help` は BA1）。BA3 は読み終えた後に判定するので、`--config '' --help` は 0 になる。
4. 読み終えたら、`--config` の値が空の文字列なら BA3 で `sys.exit(common.EXIT_USAGE)`。
5. `_Args(config=<値か None>, rebuild=<--rebuild を読んだか>)` を返す。

##### find_n03_zip

`find_n03_zip(ref_dir: str) -> tuple[str, str]`（返すのは（採用した ZIP のパス, YYYYMMDD））。`ref_dir` は呼ぶ側が `data_dir` から `os.path.join` で組み立てたパス（`data_dir` は絶対パス）で、この関数は `os.path.abspath` で正規化しない（`..` やシンボリックリンクがあっても字の上で除かない）。探した場所と読む場所を同じにするため（[2.1.3](#213-関数の細部) の `read_mesh_list_file` の「`path` は呼ぶ側が渡したまま使う」と同じ理由）。

1. `names = os.listdir(ref_dir)`。`FileNotFoundError`・`NotADirectoryError` なら候補が 0 件として 3 へ（`ref/` が無いときも ZIP を置く場所を案内するため）。ほかの `OSError` なら BZ2（`{path}` は `ref_dir`）で `sys.exit(common.EXIT_ERROR)`。
2. 候補は、`_ZIP_NAME.fullmatch(name)` に合い、`os.path.isfile(os.path.join(ref_dir, name))` が真の名前（同じ名前のディレクトリは候補にしない）。
3. 候補が 0 件なら BZ1 で `sys.exit(common.EXIT_ERROR)`（[HLD 4.17.3](30_HLD.md#4173-異常系) の「起動前提条件の不足」の行）。
4. YYYYMMDD（8 桁の文字列。字の順と数の順が同じ）が最大の候補を採る。`path = os.path.join(ref_dir, name)`、`size = os.path.getsize(path)`（`OSError` なら BZ2。`{path}` は ZIP のパス）。BL1 を `common.log_info` で出し、`(path, YYYYMMDD)` を返す。

##### needs_rebuild

`needs_rebuild(boundaries_dir: str, rebuild: bool, zip_date: str) -> bool`

1. `rebuild` が真なら BL2（`--rebuild`）を出して真を返す。
2. `_OUTPUT_NAMES` の順に、`os.path.isfile(os.path.join(boundaries_dir, <名前>))` が偽の最初の名前があれば、BL2（無いファイル）を出して真を返す（ディレクトリが同じ名前で置いてあるときも無いものとする）。
3. `recorded = _read_version(os.path.join(boundaries_dir, _VERSION_NAME))`。`None` なら BL2（版の記録が欠けている）を出して真を返す（[HLD 2.10.3](30_HLD.md#2103-フェーズのやり直し) の「版の記録が読めないか、8 桁の数字の 1 行でなければ、版の記録が欠けているものとして扱う」）。
4. BL2（作り直さない）を出す。`zip_date > recorded` なら BW1 を `common.log_warning` で出す。偽を返す（`zip_date` が `recorded` 以下なら警告しない）。

##### _read_version

`_read_version(path: str) -> str | None`（内部。`needs_rebuild` と `main` が使う）

`open(path, 'rb')` で全部を読み、`re.fullmatch(rb'([0-9]{8})\n?', data)` に合えば、その 8 字を `str`（ASCII）で返す。合わないか、`OSError`（無い、ディレクトリ、読めない）なら `None`。BOM・CR・空白・2 行目は許さない（版の記録は CMP1 だけが書くファイルで、書く側〈`replace_outputs` の 4〉は `YYYYMMDD` と LF 1 つを書く）。

##### load_n03_features

`load_n03_features(zip_path: str, zip_date: str) -> list[N03Feature]`

1. `member = f'N03-{zip_date}.geojson'`。`_n03_source = f'{zip_path} の {member}'`（モジュールの状態に入れる）。
2. `with zipfile.ZipFile(zip_path) as zf:` で開き（3 の展開もこの `with` の中で行う）、`namelist()` に `member` があるかを見る（ZIP の最上位だけ。`/` を含む名前の項目は見ない。[HLD 4.17.2](30_HLD.md#4172-処理の流れ) の 5「市区町村の GeoJSON を展開する」）。開く・名前の一覧を読むときに開けないか読めない（`OSError`・`zipfile.BadZipFile`・`zlib.error`・`EOFError`・`NotImplementedError`）なら BV1、`member` が無ければ BV2 で `sys.exit(common.EXIT_ERROR)`。
3. `with tempfile.TemporaryDirectory(prefix='findsummits-n03-') as work:` の中で、`zf.extract(member, work)` で `member` だけを展開する（`extractall` を使わない）。作業用のディレクトリを作れないか、展開の書き込みが失敗した（`OSError`）なら BF1、ZIP の中身が壊れている（`zipfile.BadZipFile`・`zlib.error`・`EOFError`・`NotImplementedError`）なら BV1 で止まる。
4. 同じ `with` の中で、展開したファイルを `open(<パス>, encoding='utf-8')` で開き、`json.load(f, parse_constant=_reject_constant)` で読む（`_reject_constant` は内部の関数で、`NaN`・`Infinity`・`-Infinity` を受けたら `ValueError(f'{name} は JSON の数でない')` を上げる）。`OSError`・`UnicodeDecodeError`・`ValueError`（`json.JSONDecodeError` を含む）・`RecursionError` なら BV3 で止まる（先頭に BOM があると `json.load` が読めず BV3 になる）。読み終えたら `with` を抜け、作業用のディレクトリを消す（`TemporaryDirectory` が消す。止まるときも、`SignalStop` で抜けるときも消える。[HLD 4.17.3](30_HLD.md#4173-異常系) の「シグナル」の行。消せないときの例外は `TemporaryDirectory` の既定のまま）。
5. 形を確かめる: 読んだ値がオブジェクトで、`type` が `'FeatureCollection'` で、`features` が配列であること。違えば BV3（`{reason}` は `FeatureCollection でない` か `features が配列でない`）。
6. `features` の各要素を、先頭から 1 つずつ `N03Feature` に変える。変えた要素は配列の中で `None` に置き換え（`features[i] = None`）、読んだ値の全体を持つ変数も先に捨てる（元の辞書を持ち続けないため。[HLD 5.2](30_HLD.md#52-nfr-002-メモリ使用量)）。要素がオブジェクトでなければ BV3（`{reason}` は `{index} 番目のフィーチャがオブジェクトでない`）。`geom_type` が `'Polygon'` か `'MultiPolygon'` のときは `shapely.geometry.shape(<geometry>)` でポリゴンを作り、`ValueError`・`TypeError`・`IndexError`・`KeyError`・`AttributeError`・`shapely.errors.GEOSException` なら BV3（`{reason}` は `{index} 番目のフィーチャの幾何の座標を読めない: <例外の 1 行目>`）。
7. `N03Feature` の並び（`features` の順）を返す。属性の値は検査しない（`validate_n03` が見る）。

##### validate_n03

`validate_n03(features: Sequence[N03Feature]) -> None`。次の順に確かめ、最初に当たった検証のメッセージを `common.log_error` で出して `sys.exit(common.EXIT_ERROR)`（[HLD 4.17.2](30_HLD.md#4172-処理の流れ) の「入力の検証」の 2 つ目〜6 つ目の項目。1 つ目の ZIP は `load_n03_features`）。止まるときは何も書かない。

1. 属性と幾何の欠け（BV4）: フィーチャの順に、次をこの順に見て、最初に当たったフィーチャと項目で止まる。`n03_001`・`n03_004`・`n03_007` が空でない `str` でない。`n03_002`・`n03_005` が `str` でも `None` でもない。`geom_type` が `None`（幾何が無い）。`geom_type` が `'Polygon'`・`'MultiPolygon'` でない。
2. 表に無い名前（BV5）: `n03_001 == '北海道'` のフィーチャは `n03_002` が `_REGIONS` の `JA8` の行の名前にあるか、ほかのフィーチャは `n03_001` が `JA8` でない行の名前にあるかを見る（北海道の振興局を都府県の名前で引かず、都府県を振興局の名前で引かない）。無い名前を、北海道なら `北海道/<n03_002>`（`None` なら `北海道/null`）、ほかなら `<n03_001>` の形の文字列にし、重なりを除いて昇順に並べる。
3. 同じコードでの食い違い（BV6）: `n03_007` が同じフィーチャで、`(n03_001, n03_004, n03_005)` の組が 1 つでないコードを昇順に並べる（`None` と空の文字列は違う値とする）。
4. ポリゴンの無い地域（BV7）: 2 の引き方でフィーチャを `_REGIONS` の行に割り当て、ポリゴンの数（`len(polygons)` の和）が 0 の行の名前を表の順に並べる。
5. 北方領土 6 村の欠け（BV8）: `_NT_CODES` のコードのうち、そのコードのフィーチャのポリゴンの数の和が 0 のコードを昇順に並べる（[DEC38](30_HLD.md#4174-設計判断)「北方領土 6 村が N03 に無ければ止める」）。

##### build_regions

`build_regions(features: Sequence[N03Feature]) -> list[dict]`

1. フィーチャを `validate_n03` の 2 の引き方で `_REGIONS` の行に割り当て、行ごとにポリゴンを集める（北方領土 6 村も根室振興局に入る）。
2. 行ごとに（`_REGIONS` の表の順に）、集めたポリゴンを `shapely.to_wkb(p, byte_order=1)` のバイト列の昇順に並べ替えてから `shapely.union_all` で合わせる（並べ替えるのは、合わせた結果が入力のフィーチャの並びによらないようにするため。[HLD 4.17.2](30_HLD.md#4172-処理の流れ) の「出力の置き場」の後の箇条の「出力の並びは入力のフィーチャの並びによらない」、[HLD 5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)）。`shapely.errors.GEOSException` なら BF2（`{step}` は `地域 <表の名前> を合わせる（dissolve）`）で止まる。結果が空か、`Polygon`・`MultiPolygon` でなければ、同じ BF2（`{reason}` は `合わせた結果が面でない: <geom_type>`）で止まる。
3. 結果の各ポリゴンを `orient(p, sign=1.0)`（外側の環を反時計回り、内側の環を時計回り。RFC 7946 の右手則）でそろえる。結果が `Polygon` なら 1 つの `Polygon`、`MultiPolygon` ならそろえたポリゴンを結果の順に並べた `MultiPolygon` にする。
4. フィーチャ（`properties` は `assoc`・`area_code`・`region_name`〈表の名前〉）を作り、`(assoc, area_code)` の昇順（字の順）に並べて返す。

##### build_municipalities

`build_municipalities(features: Sequence[N03Feature]) -> list[dict]`

1. フィーチャを `n03_007` ごとに集める。
2. コードごとに、ポリゴンを `shapely.to_wkb(p, byte_order=1)` のバイト列の昇順に並べ、`MultiPolygon(<並べたポリゴン>)` にする（座標と環の向きは N03 のまま変えない。union しない。ポリゴンが 1 つでも `MultiPolygon`。ポリゴンが 0 個のコード〈そのコードのフィーチャの幾何がすべて空のポリゴン〉はフィーチャにしない。[HLD 4.17.2](30_HLD.md#4172-処理の流れ) の「市区町村 GeoJSON」）。
3. `properties` は、`prefecture` が `n03_001`、`municipality` が `n03_004` に `n03_005` をつなげたもの（`n03_005` が `None` か空の文字列ならつなげない）、`code` が `n03_007`（同じコードのフィーチャは `validate_n03` の 3 で同じ値とわかっている）。
4. `code` の昇順（字の順。5 桁の数字の文字列なので数の順と同じ）に並べて返す。

##### split_nt_polygons

`split_nt_polygons(features: Sequence[N03Feature]) -> tuple[list[Polygon], list[Polygon]]`

フィーチャの順に、`n03_007` が `_NT_CODES` にあるフィーチャのポリゴンを 1 つ目に、ほかのフィーチャのポリゴンを 2 つ目に、フィーチャの中のポリゴンの順で足して返す。

##### list_excluded_tiles

`list_excluded_tiles(nt_polygons: Sequence[Polygon]) -> list[tuple[int, int]]`

1. ポリゴンごとに、`shapely.prepare(p)` してから、外接矩形 `(w, s, e, n) = p.bounds` の北西の隅 `(x0, y0) = common.latlon_to_tile(n, w, 15)` と南東の隅 `(x1, y1) = common.latlon_to_tile(s, e, 15)` を求め、`x` は `x0 − 1` から `x1 + 1`、`y` は `y0 − 1` から `y1 + 1` まで（両端を含む）を調べる範囲にする。両側に 1 つずつ広げるのは、`latlon_to_tile` と `tile_to_latlon` の丸めの違いで端の列や行を取り逃がさないため。余分なタイルは、下の 2 の判定で外れる。
2. 範囲の各タイル `(x, y)` について、`(n_t, w_t) = tile_to_latlon(x, y, 15)`、`(s_t, e_t) = tile_to_latlon(x + 1, y + 1, 15)` の矩形 `box(w_t, s_t, e_t, n_t)` が、ポリゴンと前置きの「交差する」の決まりで交わるなら、集合に足す（重なりは 1 つ）。
3. `(x, y)` の昇順（`x`、次に `y`）に並べて返す。

- 1・2 で `shapely.errors.GEOSException` になったら、BF2（`{step}` は `除外タイルを求める`）で `sys.exit(common.EXIT_ERROR)`。
- 空間索引は使わない（ポリゴンごとに外接矩形の中のタイルだけを調べるので、調べる数は北方領土の広さで決まる。実物の N03 で 726 ポリゴン、5 秒ほど）。

##### list_excluded_meshes

`list_excluded_meshes(japan_codes: Collection[str], nt_polygons: Sequence[Polygon], other_polygons: Sequence[Polygon]) -> list[str]`

1. `tree = shapely.STRtree(other_polygons)`。
2. `japan_codes` を昇順に、`((s, w), (n, e)) = common.mesh_to_latlon(code)`、`rect = box(w, s, e, n)` とし、次の両方を満たすコードを集める: `nt_polygons` のどれかと「交差する」。`tree.query(rect, predicate='intersects')` が返す番号の `other_polygons` のどれとも「交差する」でない（`STRtree` は外接矩形と境界での接触でも候補を返すので、候補ごとに「交差する」の決まりで確かめる）。
3. 昇順のまま返す。

- 1・2 で `shapely.errors.GEOSException` になったら、BF2（`{step}` は `除外メッシュを求める`）で `sys.exit(common.EXIT_ERROR)`。

##### tile_to_latlon

`tile_to_latlon(x: float, y: float, z: int) -> tuple[float, float]`（返すのは（緯度, 経度））。式と計算の順は [2.4](#24-言語ごとに別に実装する式のテストベクトル) の決まりのとおり（`math.sinh`・`math.atan`・`math.pi`）。引数を検査しない。

##### write_temp_outputs

`write_temp_outputs(regions: Sequence[dict], municipalities: Sequence[dict], tiles: Sequence[tuple[int, int]], meshes: Sequence[str], boundaries_dir: str) -> list[str]`（返すのは `_OUTPUT_NAMES` の順の一時ファイルの絶対パス）

1. `os.makedirs(boundaries_dir, exist_ok=True)`。`OSError` なら BF3（`{path}` は `boundaries_dir`）で止まる。
2. 4 つを `_OUTPUT_NAMES` の順に、[2.3](#23-ファイルの名前と書き方) の一時ファイルの決まりの「書く」の段で書く。置き換えはしない（`replace_outputs` が、版の記録と取得完了の記録を消した後に行う。[HLD 4.17.2](30_HLD.md#4172-処理の流れ) の 8「置き換える」）。どれかを書けなかったら、この呼び出しで先に書き終えた一時ファイルもすべて `os.remove` で消してから（消せないときの `OSError` は無視する）止まる（`boundaries/` に一時ファイルを残さない。前の出力と版の記録と取得完了の記録には触れない）。GeoJSON は `json.dump({'type': 'FeatureCollection', 'features': <フィーチャの並び>}, f, ensure_ascii=False, separators=(',', ':'), allow_nan=False)` の後に `'\n'` を 1 つ書く（テキストのモードで開く）。座標は `mapping` が返す `float` のまま（Python の `float` の最短の 10 進表記で書くので、N03 の字面と違っても値は同じ。[HLD 4.17.2](30_HLD.md#4172-処理の流れ) の「座標は N03 の値を丸めない」）。除外タイルは各行 `f'{x} {y}\n'`、除外メッシュは各行 `f'{code}\n'`（0 件なら空のファイル。UTF-8・LF・1 行 1 件。[HLD 4.17.2](30_HLD.md#4172-処理の流れ) の「出力の置き場」の後の箇条）。`OSError` なら、上のとおり一時ファイルを消してから、BF3（`{path}` は書けなかった一時ファイル）で止まる。
3. 一時ファイルのパスを返す。

- JSON の書き方の理由: 区切りの空白を入れない（市区町村の GeoJSON は座標が多く、空白の分だけ大きくなる）。`ensure_ascii=False` は、地域と市区町村の名前を UTF-8 のまま読めるようにするため。キーの順は上の「出力のフィーチャ」のとおりで、`sort_keys` を使わない。

##### replace_outputs

`replace_outputs(temp_paths: Sequence[str], data_dir: str, zip_date: str) -> None`（[HLD 4.17.2](30_HLD.md#4172-処理の流れ) の 8「置き換える」の順のとおり）

1. `os.remove(<boundaries/ の版の記録>)`。`FileNotFoundError` は無視する。
2. `os.remove(common.fetch_record_path(data_dir))`。`FileNotFoundError` は無視する（記録が無ければ何もしない。[HLD 2.10.3](30_HLD.md#2103-フェーズのやり直し)）。
3. `temp_paths` の順に、`os.replace(<一時ファイル>, os.path.join(<boundaries/>, <_OUTPUT_NAMES の同じ位置の名前>))`。
4. 版の記録を、[2.3](#23-ファイルの名前と書き方) の一時ファイルの決まりで `n03_version.txt.tmp` に `f'{zip_date}\n'` の 1 行（ASCII）を書いてから、`os.replace` で置き換える（書けないときも置き換えられないときも、下の BF4）。

- 1〜4 のどれかで `OSError`（1・2 の `FileNotFoundError` を除く）なら、BF4（`{path}` は、`os.remove` が失敗したときは消すパス、`os.replace` が失敗したときは置き換え先のパス〈一時ファイルでなく、`boundaries/` の出力か版の記録〉、版の記録の一時ファイルの書き込みが失敗したときはその一時ファイルのパス）で `sys.exit(common.EXIT_ERROR)`。版の記録の一時ファイルの書き込みが失敗したときは、[2.3](#23-ファイルの名前と書き方) のとおりその一時ファイルを `os.remove` で消してから止まる（消せないときの `OSError` は無視する）。ほかの失敗（1〜3 の失敗と、4 の版の記録の一時ファイルの `os.replace` の失敗）では、残った一時ファイル（3 で置き換えていない出力の一時ファイルと、版の記録の一時ファイル）を消さない（次の起動が上書きする。版の記録が無ければ次の起動で作り直す。[HLD 2.10.3](30_HLD.md#2103-フェーズのやり直し)）。

#### 3.1.4 メッセージ文面

前置き: 書き方は [2.2](#22-ログとメッセージの文面)。ロックとログの場面（G1〜G7。`{config_path}` は `Config` の `path`）は [2.2](#22-ログとメッセージの文面)、設定の誤り（CF1〜CF7）と日本全土リストの誤り（R1〜R3。案内は `None` で既定の対処）は [2.1.4](#214-メッセージ文面) の文面のまま。L1〜L3 は [2.2](#22-ログとメッセージの文面)（`{program}` は `preprocess_boundaries`）。`{path}`・`{zip_path}`・`{ref_dir}` は、`data_dir` から組み立てたパスのまま（`os.path.abspath` で正規化しない。`data_dir` は絶対パスなので、どれも絶対パス）、`{option}` は `--config` などの名前、`{member}` は `N03-{zip_date}.geojson`、`{zip_date}` は採用した ZIP の YYYYMMDD、`{recorded}` は版の記録の YYYYMMDD、`{reason}` は [3.1.3](#313-関数の細部) の前置きのとおり、`{source}` は `_n03_source`。`{arg}`・`{value}` は [2.2](#22-ログとメッセージの文面) の引用の決まりで書いたもの（`shlex.quote`）。`{config_opt}` は `_config_opt`（`--config` を渡されたときは空白 1 つと `--config` と空白 1 つと `Config` の `path` を `shlex.quote` したもの、渡されなかったときは空）。`{rerun}` は `タイル取得とパイプライン制御を起動する前に venv/bin/python3 scripts/preprocess_boundaries.py{config_opt} --rebuild を起動し、正常に終える`（[HLD 4.17.3](30_HLD.md#4173-異常系) の「CMP1 の失敗」の行の「CMP2・CMP3 を起動する前に CMP1 を再実行する案内」。`--rebuild` を付けるのは、前の出力がそろっていても作り直させるため）。

`ERROR:`・`WARNING:` のメッセージ（2 行目は `対処:` と空白 1 つの後）:

| 記号 | 場面 | 1 行目 | 2 行目 | 終了コード |
|---|---|---|---|---|
| BA1 | 受け付けない引数 | `preprocess_boundaries の知らない引数: {arg}` | `使える引数は --config・--rebuild・--help（venv/bin/python3 scripts/preprocess_boundaries.py --help で使い方を出す）` | 2 |
| BA2 | 値が無い | `{option} の値が無い` | `{option} の後に値を書く（venv/bin/python3 scripts/preprocess_boundaries.py --help で使い方を出す）` | 2 |
| BA3 | 値が違う | `--config の値が違う: {value}` | `--config には空でないパスを渡す` | 2 |
| BA4 | 同じ名前を 2 回 | `{option} を 2 回渡した` | `{option} は 1 回だけ渡す` | 2 |
| BZ1 | N03 行政区域 ZIP が無い | `N03 行政区域 ZIP が無い: {ref_dir}/N03-YYYYMMDD_GML.zip（YYYYMMDD は半角の数字 8 桁）` | `国土数値情報の行政区域データ（全国）の ZIP を入手し、名前を変えずに {ref_dir} の直下に置いてから、もう一度起動する` | 1 |
| BZ2 | ZIP か ZIP を探す場所を読めない | `N03 行政区域 ZIP か、ZIP を探す場所を読めない: {path}: {reason}` | `{path} の読み取りの権限を確かめてから、もう一度起動する` | 1 |
| BV1 | ZIP を読めない | `N03 行政区域 ZIP を読めない: {zip_path}: {reason}` | `ZIP を国土数値情報から入手し直して置き換える。{rerun}` | 1 |
| BV2 | ZIP に市区町村の GeoJSON が無い | `N03 行政区域 ZIP の最上位に {member} が無い: {zip_path}` | BV1 と同じ | 1 |
| BV3 | GeoJSON を読めない | `N03 の GeoJSON を読めない: {source}: {reason}` | BV1 と同じ | 1 |
| BV4 | 属性か幾何の欠け | `N03 の GeoJSON に属性か幾何の欠けたフィーチャがある: {source} の {index} 番目のフィーチャ（{detail}）`（`{detail}` は `{key} が空でない文字列でない`、`{key} が文字列でも null でもない`、`幾何が無い`、`幾何の種類が {type}` のどれか。`{key}` は N03 のプロパティの名前〈`N03_001` など。大文字〉。`{type}` は値を `json.dumps(<値>, ensure_ascii=False)` したもの） | `N03 行政区域 ZIP が正しいかを確かめる（入手し直して置き換える）。{rerun}` | 1 |
| BV5 | 地域の対応表に無い名前 | `N03 の都道府県名か振興局名が地域の対応表に無い: {names}（{source}）` | `N03 行政区域 ZIP が正しいかを確かめる。正しければ、都道府県か振興局の再編か改称なので、preprocess_boundaries の地域の対応表を直す（開発者に知らせる）。{rerun}` | 1 |
| BV6 | 同じコードで食い違う | `同じ行政区域コードで都道府県名か市区町村名が食い違う: {codes}（{source}）` | BV4 と同じ | 1 |
| BV7 | ポリゴンの無い地域 | `ポリゴンが 1 つも無い地域がある: {names}（{source}）` | BV5 と同じ | 1 |
| BV8 | 北方領土 6 村の欠け | `北方領土 6 村のポリゴンが N03 に無い: {codes}（{source}）` | `N03 行政区域 ZIP が正しいかを確かめる。正しければ、行政区域コードの変更なので、preprocess_boundaries の北方領土 6 村のコードを直す（開発者に知らせる）。{rerun}` | 1 |
| BF1 | 展開できない | `N03 の GeoJSON を作業用のディレクトリに展開できない: {path}: {reason}`（`{path}` は作業用のディレクトリ。作れなかったときは `tempfile.gettempdir()`） | `ディスクの空きと一時ディレクトリ（環境変数 TMPDIR）の権限を確かめる。{rerun}` | 1 |
| BF2 | ポリゴンの計算ができない | `ポリゴンの計算ができない: {step}: {reason}（{source}）`（`{step}` は `build_regions`・`list_excluded_tiles`・`list_excluded_meshes` が渡す処理の名前） | `このメッセージを写して開発者に知らせる（N03 のポリゴンが不正な形かもしれない）。{rerun}` | 1 |
| BF3 | 一時ファイルに書けない | `出力を一時ファイルに書けない: {path}: {reason}` | `ディスクの空きと {dir} の権限を確かめる（前の出力は残っている）。{rerun}`（`{dir}` は `boundaries/` の絶対パス） | 1 |
| BF4 | 置き換えられない | `出力を置き換えられない: {path}: {reason}` | `{path} とそのディレクトリの権限を確かめる（版の記録を消した後なら、次の起動で作り直す）。{rerun}` | 1 |
| BW1 | 新しい版の ZIP がある（`WARNING:`） | `記録した版より新しい N03 行政区域 ZIP がある: 記録した版 {recorded}、置いてある最新の版 {zip_date}`（ZIP のパスは直前の BL1 に出ている。`needs_rebuild` は ZIP のパスを受け取らない） | `新しい版を使うなら venv/bin/python3 scripts/preprocess_boundaries.py{config_opt} --rebuild を起動する（作り直すと取得完了の記録が消えるので、タイル取得からやり直す）` | 0 |

`{names}`・`{codes}` は、[3.1.3](#313-関数の細部) の `validate_n03` の並びで `・` でつないだもの。BV5・BV6 は先頭から `_LIST_LIMIT`（10）件までで、超えるときは続けて空白 1 つと `ほか {k} 件` を付ける（`{k}` は残りの数）。BV7・BV8 は全部（最大 60 件と 6 件）。

通常のログに出す行（`common.log_info` で標準出力とログファイルに出す）:

| 記号 | 行 | 文面 |
|---|---|---|
| BL1 | 採用した ZIP | `N03 行政区域 ZIP: {zip_path}（版 {zip_date}、{size} バイト）` |
| BL2 | 作り直すかの判定 | `作り直す: --rebuild を付けた`、`作り直す: {path} が無い`、`作り直す: 版の記録が読めないか、8 桁の数字の 1 行でない: {path}`、`作り直さない: 出力と版の記録がそろっている（版 {recorded}）` のどれか |
| BL3 | 結果の要約（作り直した） | `結果の要約: 作り直した（版 {zip_date}）。地域 {n}、市区町村 {n}、除外タイル {n}、除外メッシュ {n}` |
| BL4 | 結果の要約（作り直さなかった） | `結果の要約: 作り直さなかった。採用した ZIP の版 {zip_date}、版の記録 {recorded}`（[HLD 5.7.2](30_HLD.md#572-処理の流れ) の「結果の要約の中身」の `preprocess_boundaries` の行） |
| BL5 | 結果の要約（途中で止まった） | `結果の要約: 途中で止まった。終えた分: {done}`（`{done}` は `counts` にある名前を `地域`・`市区町村`・`除外タイル`・`除外メッシュ` の順に `{名前} {件数}` にして `、` でつないだもの。無ければ `なし`）。`replacing` が真なら続けて `。出力の置き換えに入った後に止まった（版の記録が消えていれば、次の起動で作り直す）` |

使い方の文（`--help`。標準出力に、次の行をこのまま出す。最後の行の後にも LF を付ける）:

```text
使い方: venv/bin/python3 scripts/preprocess_boundaries.py [--config <パス>] [--rebuild]
       venv/bin/python3 scripts/preprocess_boundaries.py --help

N03 行政区域 ZIP から、地域と市区町村の GeoJSON、北方領土除外タイルリスト、北方領土除外メッシュリストを作る。出力と版の記録がそろっていれば作り直さない。

  --config <パス>  設定ファイル（省くとソースツリーの params/config.ini）
  --rebuild        出力と版の記録がそろっていても作り直す
  --help           この使い方を出して終わる
```

- 並べる件数の理由: BV5・BV6 は、N03 の書式が変わると全部の名前やコードに当たりうるので 10 件までにする（利用者がすることは ZIP を確かめるか表を直すかで、全部の名前は要らない）。BV7・BV8 は上限が小さいので全部並べる。

#### 3.1.5 UT 候補

前置き: すべて自動。共通の準備は次の 4 つ。止まるケースの期待の「メッセージ」は、標準エラー出力の行の文面（[2.2](#22-ログとメッセージの文面)・[2.1.4](#214-メッセージ文面)・[3.1.4](#314-メッセージ文面) の文面に値を入れたもの）。ログファイルの行の期待は、先頭の時刻と空白を除いた文面。

- **同じプロセス**: テストのプロセスの中で `scripts/` を import の探索先に入れて `import preprocess_boundaries` し、関数を直接呼ぶ（`start_log` を呼ばない。`log_info` などは画面にだけ出る）。止まるケースは `SystemExit` を捕まえて終了コードを読み、標準出力と標準エラー出力は `contextlib.redirect_stdout`・`redirect_stderr` で捕まえる。一時のディレクトリ `<tmp>` をケースごとに作り、`tempfile.tempdir` を `<tmp>/t`（作っておく）に差し替える（作業用のディレクトリの残りを見るため。ケースの後に元に戻す）。1 つのケースの中で入力を何通りか試すとき（(a)(b)… に分けたケースなど）は、入力ごとに `<tmp>` の下の置き場（`<tmp>/b`・`<tmp>/data` など）を消して作り直し、前の入力の残りを持ち越さない（同じ名前のディレクトリを `os.makedirs` で 2 度作って失敗しないため）。
- **小さな N03**: 次の 67 フィーチャの FeatureCollection（UTF-8 の JSON。`properties` には `N03_001`〜`N03_005`・`N03_007` の 6 つのキーを置き、書かないものは `null`）。各フィーチャの幾何は、ポリゴンを 1 つ持つ `MultiPolygon` で、ポリゴンは外側の環だけの矩形 `[[w, s], [e, s], [e, n], [w, n], [w, s]]`（反時計回り）。
  - 地域のフィーチャ 60: HLD 4.17.2 の対応表の `i` 行目（0 から）ごとに 1 つ。`JA8` の行は `N03_001` が `北海道`・`N03_002` が表の名前、ほかは `N03_001` が表の名前。`N03_004` は `市` と `i` の 2 桁（`市00`）、`N03_007` は `9` と `i` の 4 桁（`90000`）。矩形は `w = 120 + 0.2 × (i mod 10)`、`s = 25 + 0.2 × floor(i / 10)`、`e = w + 0.1`、`n = s + 0.1`。ただし根室振興局の行は `w = 147.5`、`s = 44.8`、`e = 147.6`、`n = 44.9`（メッシュ `6747` の中）。
  - 北方領土のフィーチャ 7: `k` = 0〜5 について、`N03_001` が `北海道`・`N03_002` が `根室振興局`・`N03_004` が `村` と `k`（`村0`）・`N03_007` が `1695 + k` を 0 で埋めた 5 桁（`f'{1695 + k:05d}'`。`01695`〜`01700`）で、矩形は `w = 148.1 + 0.1 × k`、`s = 45.5`、`e = w + 0.05`、`n = 45.55`（メッシュ `6848` の中）。7 つ目は `01695` の 2 つ目のフィーチャ（`N03_004` は `村0`）で、矩形は `w = 147.1`、`s = 44.8`、`e = 147.15`、`n = 44.85`（メッシュ `6747` の中。`6747` は根室振興局の矩形も持つので、除外メッシュにならない）。
  - この N03 からの出力: 地域 60、市区町村 66（`01695` は 2 つのポリゴンの `MultiPolygon`）、日本全土のリストを `3720`・`6747`・`6848` にしたときの除外メッシュは `6848` だけ。根室振興局の地域は、根室振興局の矩形と北方領土の 7 つの矩形の 8 つのポリゴンの `MultiPolygon`。
- **一時の ZIP**: 小さな N03（ケースが書き換えたものを含む）を `json.dumps(…, ensure_ascii=False)` の UTF-8 にして、`<data_dir>/ref/N03-20250101_GML.zip` の最上位の `N03-20250101.geojson` に書く（`zipfile.ZIP_DEFLATED`）。同じ ZIP の最上位に `N03-20250101_prefecture.geojson`（中身は `{}`）も置く。
- **子のプロセス**: 一時のソースツリー `<tmp>/src` を作り、`<tmp>/src/scripts/` にテストする `scripts/preprocess_boundaries.py` と `scripts/common.py` を写し、`<tmp>/src/params/mesh_list_japan.txt` に `3720\n6747\n6848\n` を書く。一時の設定 `<tmp>/c.ini` に `[paths]` の `data_dir = <tmp>/data`・`log_dir = <tmp>/logs` を書き、`<tmp>/data/ref/` に一時の ZIP を置く。`<tmp>/work` と `<tmp>/t` を作る。起動は `subprocess.run([sys.executable, '<tmp>/src/scripts/preprocess_boundaries.py', *<引数>], cwd='<tmp>/work', env={**os.environ, 'TMPDIR': '<tmp>/t'}, capture_output=True)`（ケースが書かなければ引数は `--config ../c.ini`）。終了コード、標準出力と標準エラー出力（UTF-8 で読む）、`<tmp>/logs` の下のログファイル、`<tmp>/data/boundaries/` を確かめる。

| ID | 確かめること | 準備 | 入力 | 期待 |
|---|---|---|---|---|
| `UT-preprocess_boundaries-01` | 引数の正しい形 | 同じプロセス | `_parse_args` に (a) `[]`、(b) `['--config', 'a.ini']`、(c) `['--config=a=b.ini', '--rebuild']`、(d) `['--rebuild', '--config', '--help']` | (a) `_Args(None, False)`、(b) `_Args('a.ini', False)`、(c) `_Args('a=b.ini', True)`、(d) `_Args('--help', True)` |
| `UT-preprocess_boundaries-02` | 引数の誤り | 同じプロセス | `_parse_args` に (a) `['foo']`、(b) `['--foo']`、(c) `['--rebuild=x']`、(d) `['--help=x']`、(e) `['--']`、(f) `['--conf', 'a.ini']`、(g) `['--config']`、(h) `['--config', '']`、(i) `['--config=']`、(j) `['--rebuild', '--rebuild']`、(k) `['--config', 'a', '--config', 'b']`、(l) `['--config', 'a', '--config']`、(m) `['--rebuild', '--rebuild=x']` | どれも 2、標準出力は空。(a)〜(f)(m) は BA1（(a) の 1 行目は `ERROR: preprocess_boundaries の知らない引数: foo`、(f) の引数は `--conf`、(m) の引数は `--rebuild=x` で BA4 でない）、(g) は BA2（`--config の値が無い`）、(h)(i) は BA3（`ERROR: --config の値が違う: ''`）、(j) は BA4（`--rebuild を 2 回渡した`）、(k)(l) は BA4（`--config を 2 回渡した`。(l) は BA2 でない） |
| `UT-preprocess_boundaries-03` | `--help` | 子のプロセス | 引数を (a) `--rebuild --help --foo`、(b) `--foo --help`、(c) `--config '' --help`（`--config` の値は空の文字列） | (a)(c) は 0、標準出力は [3.1.4](#314-メッセージ文面) の使い方の文と等しい、標準エラー出力は空、`<tmp>/data/findsummits.lock` と `<tmp>/logs` が無い（(c) は BA3 を読み終えた後に判定するので、`--help` が先に終わる）。(b) 2、BA1（`--foo`）、標準出力は空 |
| `UT-preprocess_boundaries-04` | ZIP の選び方 | 同じプロセス。`<tmp>/ref/` に、中身が `abc`（3 バイト）の `N03-20250101_GML.zip`、中身が `abcde`（5 バイト）の `N03-20260101_GML.zip`、中身が空で名前が `N03-2026010_GML.zip`・`N03-20270101_GML.ZIP`・`N03-20270101_GML.zip.bak`・数字を全角にした `N03-`・8 桁・`_GML.zip`（数字はコードポイント U+FF10〜U+FF19）のファイルを置き、ディレクトリ `N03-20280101_GML.zip` を作る | `find_n03_zip('<tmp>/ref')` | `('<tmp>/ref/N03-20260101_GML.zip', '20260101')`、標準出力は BL1 の 1 行 `N03 行政区域 ZIP: <tmp>/ref/N03-20260101_GML.zip（版 20260101、5 バイト）` |
| `UT-preprocess_boundaries-05` | ZIP が無い・探せない | 同じプロセス | `find_n03_zip` に (a) 空のディレクトリ、(b) 無いパス、(c) 通常のファイルのパス、(d) 権限 `000` のディレクトリ（実効ユーザーが root なら飛ばす） | (a)(b)(c) は 1、BZ1（1 行目は `ERROR: N03 行政区域 ZIP が無い: <渡したパス>/N03-YYYYMMDD_GML.zip（YYYYMMDD は半角の数字 8 桁）`）。(d) は 1、BZ2（`{reason}` は `Permission denied`） |
| `UT-preprocess_boundaries-06` | 作り直さないときと警告 | 同じプロセス。`<tmp>/b/` に 4 つの出力の名前の空のファイルと、`n03_version.txt`（中身 `20250101\n`）を置く | `needs_rebuild('<tmp>/b', False, …)` に (a) `'20250101'`、(b) `'20260101'`、(c) `'20240101'`、(d) `rebuild` を `True` にして `'20250101'` | (a)(b)(c) は偽、(d) は真。標準出力は (a)(b)(c) が BL2 の `作り直さない: 出力と版の記録がそろっている（版 20250101）`、(d) が `作り直す: --rebuild を付けた`。(b) だけ標準エラー出力に BW1 の 2 行（`WARNING: 記録した版より新しい N03 行政区域 ZIP がある: 記録した版 20250101、置いてある最新の版 20260101` と、`対処: 新しい版を使うなら venv/bin/python3 scripts/preprocess_boundaries.py --rebuild を起動する（作り直すと取得完了の記録が消えるので、タイル取得からやり直す）`）。ほかは標準エラー出力が空 |
| `UT-preprocess_boundaries-07` | 出力が欠けたとき | 同じプロセス。ケースごとに `<tmp>/b` を消して作り直し（前のケースの出力や版の記録を残さない）、06 と同じ置き方から 1 つを変える | (a)〜(d) 4 つの出力のどれか 1 つを消す（別々に）、(e) `nt_excluded_tiles.txt` をディレクトリにする、(f) `<tmp>/b` を消す | どれも真で、BL2 が `作り直す: <無いファイルの絶対パス> が無い`（(f) は `regions.geojson` のパス）。呼ぶ前後で、`<tmp>/b` の下にあるすべてのファイルのバイト列は同じ（ファイルを作らず、消さず、書き換えない） |
| `UT-preprocess_boundaries-08` | 版の記録の形 | 同じプロセス。ケースごとに `<tmp>/b` を消して作り直し（前のケースの版の記録を残さない）、06 と同じ置き方で、`n03_version.txt` の中身をケースごとにバイト列で書く | (a) `20250101`（改行なし）、(b) `20250101\n`、(c) `2025010\n`、(d) `20250101\n20250101\n`、(e) `20250101\r\n`、(f) `20250101\n\n`、(g) `EF BB BF` の後に `20250101\n`、(h) 空、(i) 全角の数字 8 桁（コードポイント U+FF12・U+FF10・U+FF12・U+FF15・U+FF10・U+FF11・U+FF10・U+FF11）と `\n`、(j) `n03_version.txt` を消す、(k) `n03_version.txt` をディレクトリにする。どれも `needs_rebuild('<tmp>/b', False, '20250101')` | (a)(b) は偽（BL2 の版は `20250101`）。(c)〜(i)(k) は真で、BL2 は `作り直す: 版の記録が読めないか、8 桁の数字の 1 行でない: <tmp>/b/n03_version.txt`。(j) は真で、BL2 は同じ文（版の記録は 4 つの出力の後に見るので、`が無い` の文でない） |
| `UT-preprocess_boundaries-09` | ZIP を読む | 同じプロセス。`<tmp>/data/ref/` に一時の ZIP。`zipfile.ZipFile.extract`・`zipfile.ZipFile.extractall` を、呼ばれた項目の名前を記録してから元を呼ぶ物に差し替える | `load_n03_features('<tmp>/data/ref/N03-20250101_GML.zip', '20250101')` | 67 個の `N03Feature`（`index` は 1〜67、`n03_007` などが小さな N03 のとおり、`geom_type` は `MultiPolygon`、`polygons` は 1 つ）。`extract` が `N03-20250101.geojson` の 1 回だけ呼ばれ、`extractall` は呼ばれない。`<tmp>/t` は空 |
| `UT-preprocess_boundaries-10` | ZIP と GeoJSON を読めない | 同じプロセス。ケースごとに `<tmp>/data/ref/N03-20250101_GML.zip` を作る | (a) 中身が `not a zip` のテキストのファイル、(b) 最上位に `N03-20250101.geojson` が無い ZIP（`N03-20250101_prefecture.geojson` だけ）、(c) `x/N03-20250101.geojson` だけの ZIP、(d) `N03-20250101.geojson` の中身が `FF FE`、(e) 中身が `{`、(f) 1 つ目のフィーチャの座標の 1 つを `NaN` にした JSON（字の `NaN`）、(g) 中身が `[]`、(h) `{"type":"FeatureCollection","features":{}}`、(i) `features` の 1 つ目が `1`、(j) 1 つ目のフィーチャの `coordinates` を `[[[1]]]` にした JSON | どれも 1、`<tmp>/t` は空。(a) は BV1、(b)(c) は BV2（1 行目は `ERROR: N03 行政区域 ZIP の最上位に N03-20250101.geojson が無い: <ZIP のパス>`）、(d) は BV3（`{reason}` は `UTF-8 として読めない`）、(e)(f) は BV3、(g) は BV3（`{reason}` は `FeatureCollection でない`）、(h) は BV3（`features が配列でない`）、(i) は BV3（`1 番目のフィーチャがオブジェクトでない`）、(j) は BV3（`{reason}` が `1 番目のフィーチャの幾何の座標を読めない:` と空白 1 つで始まる） |
| `UT-preprocess_boundaries-11` | シグナルでも作業用のディレクトリを消す | 子のプロセスの代わりに、`[sys.executable, '-c', <試験用の短いプログラム>]` を `cwd='<tmp>/work'`・`TMPDIR` を `<tmp>/t` にして起動する。試験用のプログラムは、`<tmp>/src/scripts` を `sys.path` の先頭に入れて `import preprocess_boundaries` し、`json.load` を「自分へ `SIGTERM` を送ってから元の `json.load` を呼ぶ物」に差し替えてから、`sys.argv = ['preprocess_boundaries.py', '--config', '<tmp>/c.ini']` にして `preprocess_boundaries.main()` を呼ぶ | 起動する | 143、`<tmp>/t` は空、`<tmp>/data/boundaries/` は作られていない、ログファイルの最後の行が `SIGTERM` を受けて止まった形の L3 で、その前の行が BL5 の `結果の要約: 途中で止まった。終えた分: なし` |
| `UT-preprocess_boundaries-12` | 属性と幾何の欠け | 同じプロセス。小さな N03 を、ケースごとに 1 か所だけ書き換えて一時の ZIP にし、`load_n03_features` で読む | 3 つ目のフィーチャの (a) `N03_001` を `null`、(b) `N03_004` を `""`、(c) `N03_007` のキーを消す、(d) `N03_002` を `1`、(e) `N03_005` を `[]`、(f) `geometry` を `null`、(g) `geometry` を `{"type":"Point","coordinates":[0,0]}`、(h) 2 つ目のフィーチャの `N03_007` を `null` にし、3 つ目の `geometry` を `null` にする、(i) `geometry` から `type` のキーだけを消す（`coordinates` は残す） | `load_n03_features` はどれも止まらない。`validate_n03` がどれも 1、BV4。`{detail}` は (a) `N03_001 が空でない文字列でない`、(b) `N03_004 が空でない文字列でない`、(c) `N03_007 が空でない文字列でない`、(d) `N03_002 が文字列でも null でもない`、(e) `N03_005 が文字列でも null でもない`、(f)(i) `幾何が無い`、(g) `幾何の種類が "Point"`。(a)〜(g)(i) の `{index}` は 3、(h) は 2 で `N03_007` の項目 |
| `UT-preprocess_boundaries-13` | 表に無い名前 | 同じプロセス。12 と同じ作り方 | (a) 愛知県の行のフィーチャの `N03_001` を `テスト県`、(b) 石狩振興局の行の `N03_002` を `石狩支庁`、(c) 石狩振興局の行の `N03_002` を `東京都`、(d) 愛知県の行の `N03_001` を `石狩振興局`、(e) 対応表の最初の 11 行（愛知県〜茨城県。どれも北海道でない行）のフィーチャの `N03_001` を、表の順に `県A`〜`県K` にする（`A`〜`K` は英大文字） | どれも 1、BV5。`{names}` は (a) `テスト県`、(b) `北海道/石狩支庁`、(c) `北海道/東京都`、(d) `石狩振興局`、(e) `県A・県B・県C・県D・県E・県F・県G・県H・県I・県J ほか 1 件`（(a)(d)(e) は、名前を変えた地域のポリゴンが無くなるが、BV5 が先に止まる） |
| `UT-preprocess_boundaries-14` | 同じコードでの食い違い | 同じプロセス | (a) `01696` のフィーチャをもう 1 つ足し（矩形は `01696` の矩形と同じ）、`N03_004` を `村9` にする、(b) 同じく足して `N03_005` を `""` にする（元は `null`） | どちらも 1、BV6、`{codes}` は `01696` |
| `UT-preprocess_boundaries-15` | ポリゴンの無い地域と北方領土の欠け | 同じプロセス | (a) 愛知県の行のフィーチャを除く、(b) 愛知県と十勝総合振興局の行のフィーチャを除く、(c) 愛知県の行の幾何を `{"type":"MultiPolygon","coordinates":[]}` にする、(d) `01698` のフィーチャを除く、(e) `01698` のフィーチャと愛知県の行のフィーチャを除く、(f) 愛知県の行の幾何を `{"type":"Polygon","coordinates":[]}` にする、(g) `01698` の幾何を `{"type":"Polygon","coordinates":[]}` にする | どれも 1。(a)(c)(f) は BV7 で `{names}` は `愛知県`、(b) は BV7 で `愛知県・十勝総合振興局`（表の順）、(d)(g) は BV8 で `{codes}` は `01698`、(e) は BV7（BV8 より先） |
| `UT-preprocess_boundaries-16` | 地域を合わせる | 同じプロセス。小さな N03 に、愛知県の行の矩形と東の辺を共有する矩形（`w = 120.1`、`s = 25.0`、`e = 120.15`、`n = 25.1`）のフィーチャ（`N03_001` は `愛知県`、`N03_004` は `市60`、`N03_007` は `90060`）を足し、宮城県の行のフィーチャの幾何を、穴を持つポリゴン 1 つの `MultiPolygon`（外側の環は宮城県の行の矩形を時計回りに書いたもの、穴は矩形の中央の 1 辺 0.02 度の正方形を反時計回りに書いたもの）に替えて一時の ZIP にし、`load_n03_features` で読む | `build_regions` | 60 フィーチャ。`properties` の（`assoc`, `area_code`, `region_name`）の並びが、HLD 4.17.2 の「地域と SOTA のコード」の表の 60 行を `(assoc, area_code)` の昇順に並べたものとすべて等しい（テストは表の値を実装と別に写し、途中の行のコードの写し誤りを単体の段で止める）。1 つ目は `assoc` `JA`・`area_code` `AC`、最後は `JA8`・`TC`。根室振興局の地域は 8 つのポリゴンの `MultiPolygon`。愛知県は 1 つの `Polygon`（2 つの矩形が合わさる）で、外側の環が反時計回り（`shapely.LinearRing(<環>).is_ccw` が真）。宮城県は穴を 1 つ持つ `Polygon` で、外側が反時計回り、穴が時計回り。`properties` のキーの順は `assoc`・`area_code`・`region_name` |
| `UT-preprocess_boundaries-17` | 市区町村をまとめる | 同じプロセス。小さな N03 の 1 つ目のフィーチャ（愛知県）の `N03_004` を `札幌市`・`N03_005` を `中央区` にし、2 つ目の `N03_005` を `""` にし、3 つ目の矩形の環を時計回りの順（`[[w, s], [w, n], [e, n], [e, s], [w, s]]`）にして読む | `build_municipalities` | 66 フィーチャで `code` の昇順（最初は `01695`、最後は `90059`）。`01695` は 2 つのポリゴンの `MultiPolygon`。どのフィーチャも幾何の種類が `MultiPolygon`。`90000` の `municipality` は `札幌市中央区`、`90001` は `市01`。`90002` の座標は時計回りのまま、入力と同じ値の並び。`properties` のキーの順は `prefecture`・`municipality`・`code` |
| `UT-preprocess_boundaries-18` | 出力が入力の並びによらない | 同じプロセス。小さな N03 から (a) そのまま、(b) フィーチャの並びを逆にしたもの（`01695` の 2 つのフィーチャの順も逆になる）、の 2 つの一時の ZIP を別の `<data_dir>` に作り、それぞれ読んで `build_regions`・`build_municipalities`・`split_nt_polygons`・`list_excluded_tiles`・`list_excluded_meshes`（日本全土は `{'3720', '6747', '6848'}`）・`write_temp_outputs`（`<data_dir>/boundaries`）を呼ぶ | 2 つの一時ファイルの組 | 4 つの一時ファイルのバイト列が、(a) と (b) でそれぞれ等しい |
| `UT-preprocess_boundaries-19` | 北方領土のポリゴンを分ける | 同じプロセス。小さな N03 を読む | `split_nt_polygons` | 1 つ目は 7 つのポリゴン、2 つ目は 60 のポリゴン |
| `UT-preprocess_boundaries-20` | タイル番号 → 緯度経度 | 同じプロセス | [2.4](#24-言語ごとに別に実装する式のテストベクトル) の表 3 の各行 | 経度は `==` で等しく、緯度は差の絶対値が `1e-12` 以下 |
| `UT-preprocess_boundaries-21` | 除外タイル | 同じプロセス。`(n0, w0) = tile_to_latlon(29127, 12867, 15)`、`(s0, e0) = tile_to_latlon(29128, 12868, 15)` | `list_excluded_tiles` に (a) `[box(w0, s0, e0, n0)]`（タイル 1 枚ちょうど）、(b) そのタイルの中の小さな矩形（`w0` と `e0` の間の 1/4〜3/4、`s0` と `n0` の間の 1/4〜3/4）、(c) 西の端が `w0 + (e0 − w0) × 0.5`、東の端が `e0 + (e0 − w0) × 0.5` で、南北は (b) と同じ矩形、(d) (a) と (b) の 2 つ | (a) `[(29127, 12867)]`（接するだけの隣のタイルを含まない）、(b) `[(29127, 12867)]`、(c) `[(29127, 12867), (29128, 12867)]`、(d) `[(29127, 12867)]`（重なりは 1 つ） |
| `UT-preprocess_boundaries-22` | 除外メッシュ | 同じプロセス。北方領土の矩形 `P = box(148.1, 45.5, 148.15, 45.55)`（`6848` の中） | `list_excluded_meshes` に (a) 日本全土 `{'6848', '6747', '3720'}`、`[P]`、`[box(147.5, 44.8, 147.6, 44.9)]`、(b) 日本全土 `{'6848'}`、`[P]`、`[box(148.5, 45.5, 148.6, 45.6)]`（`6848` の中のほかの陸地）、(c) 日本全土 `{'6848', '6849'}`、`[box(148.9, 45.5, 149.0, 45.6)]`（東の辺が `6849` との境目に乗る）、`[]`、(d) 日本全土 `{'6848'}`、`[P]`、`[box(147.9, 45.5, 148.0, 45.6)]`（西で `6848` の境目に接するだけ） | (a) `['6848']`、(b) `[]`、(c) `['6848']`（`6849` は接するだけ）、(d) `['6848']` |
| `UT-preprocess_boundaries-23` | 一時ファイルの書き方 | 同じプロセス。(a) は `<tmp>/b/` を作らない。(b) は `<tmp>/b/` を作り、`<tmp>/b/nt_excluded_meshes.txt.tmp` を前の起動の残りとして置く。(c) は `<tmp>/b/` に 4 つの出力（中身 `old`）と `n03_version.txt`（`20240101\n`）を置き、`<tmp>/data/tiles/fetch_complete.txt` も置く | (a) `write_temp_outputs([], [], [(1, 2), (3, 4)], ['6848'], '<tmp>/b')`、(b) `<tmp>/b/nt_excluded_meshes.txt.tmp` に `old` を書いてから `write_temp_outputs([<地域のフィーチャ 1 つ〈properties は assoc JA・area_code TK・region_name 東京都、幾何は box(0, 0, 1, 1) の mapping〉>], [], [], [], '<tmp>/b')`、(c) `write_temp_outputs([], [], [], [], '<tmp>/b')` | (a) 返り値は `<tmp>/b/regions.geojson.tmp` など 4 つのパス（`_OUTPUT_NAMES` の順）、`<tmp>/b` が作られる、`regions.geojson.tmp` と `municipalities.geojson.tmp` は `{"type":"FeatureCollection","features":[]}\n`、タイルは `1 2\n3 4\n`、メッシュは `6848\n`。(b) `regions.geojson.tmp` は `{"type":"FeatureCollection","features":[{"type":"Feature","properties":{"assoc":"JA","area_code":"TK","region_name":"東京都"},"geometry":{"type":"Polygon","coordinates":[[[1.0,0.0],[1.0,1.0],[0.0,1.0],[0.0,0.0],[1.0,0.0]]]}}]}\n` の UTF-8（`東京都` はエスケープしない）、メッシュの一時ファイルは空（`old` が残らない）。(c) 4 つの一時ファイルができ、4 つの出力（`old`）と版の記録（`20240101\n`）と取得完了の記録のバイト列は呼ぶ前と同じ（置き換えない） |
| `UT-preprocess_boundaries-24` | 一時ファイルに書けない | 同じプロセス | (a) `<tmp>/b` を通常のファイルにして `write_temp_outputs([], [], [], [], '<tmp>/b')`、(b) `<tmp>/b/nt_excluded_tiles.txt.tmp` をディレクトリにしてから同じく呼ぶ | どちらも 1、BF3。(a) の `{path}` は `<tmp>/b`。(b) の `{path}` は `<tmp>/b/nt_excluded_tiles.txt.tmp` で、`regions.geojson.tmp`・`municipalities.geojson.tmp` は残っていない |
| `UT-preprocess_boundaries-25` | 置き換えの順と中身 | 同じプロセス。`<tmp>/data/boundaries/` に 4 つの出力（中身 `old`）と `n03_version.txt`（`20240101\n`）、`<tmp>/data/tiles/fetch_complete.txt` を置き、4 つの一時ファイルを `write_temp_outputs([], [], [], [], '<tmp>/data/boundaries')` で作る。`preprocess_boundaries` の中の `os.remove`・`os.replace` を、引数を記録してから元を呼ぶ物に差し替える | `replace_outputs(<一時ファイルのパス>, '<tmp>/data', '20250101')` | 呼ばれた順が、`os.remove(<版の記録>)`、`os.remove(<tmp>/data/tiles/fetch_complete.txt)`、`os.replace` が 4 つの一時ファイルから `_OUTPUT_NAMES` の順の出力へ、`os.replace(<版の記録の一時ファイル>, <版の記録>)`。終わった後、版の記録は `20250101\n`、取得完了の記録は無い、4 つの出力は一時ファイルの中身、`.tmp` で終わるファイルは無い |
| `UT-preprocess_boundaries-26` | 記録が無いとき・置き換えの途中の失敗 | 同じプロセス。25 と同じ置き方 | (a) 版の記録と取得完了の記録を置かずに `replace_outputs`、(b) 差し替えた `os.replace` が 3 回目の呼び出しで `OSError(errno.EACCES, …)` を上げる、(c) `preprocess_boundaries` の中の `os.fsync` を `OSError(errno.EIO, os.strerror(errno.EIO))` を上げる物に差し替えて `replace_outputs`（4 つの一時ファイルは準備で書き終えているので、`fsync` を呼ぶのは版の記録の一時ファイルの書き込みだけ） | (a) 止まらず、版の記録は `20250101\n`。(b) 1、BF4（`{path}` は 3 つ目の出力 `nt_excluded_tiles.txt` のパス〈置き換え先〉）、版の記録が無い、取得完了の記録が無い。(c) 1、BF4（`{path}` は `<tmp>/data/boundaries/n03_version.txt.tmp`、`{reason}` は `Input/output error`）、`n03_version.txt.tmp` も版の記録も無い、取得完了の記録が無い、4 つの出力は一時ファイルの中身（置き換えは済んでいる） |
| `UT-preprocess_boundaries-27` | 初めて作る | 子のプロセス。`<tmp>/data/tiles/fetch_complete.txt` を置く | 引数は既定（作業ディレクトリ `<tmp>/work` から相対パスの `--config ../c.ini`） | 0。`<tmp>/data/boundaries/` に 4 つの出力と `n03_version.txt`（`20250101\n`）。地域 60・市区町村 66 フィーチャ、除外メッシュは `6848\n`、除外タイルは 1 枚以上で各行が `^[0-9]+ [0-9]+$`、`(x, y)` の昇順で重なりが無い。取得完了の記録が無い。`<tmp>/t` は空。`<tmp>/data/findsummits.lock` がある。ログファイルの行は L1、L2（`設定ファイル: <tmp>/c.ini`、`[paths]` の `data_dir` と `log_dir` の 2 行）、BL1、BL2（`作り直す: <tmp>/data/boundaries/regions.geojson が無い`）、BL3（`結果の要約: 作り直した（版 20250101）。地域 60、市区町村 66、除外タイル <タイルの行の数>、除外メッシュ 1`）、L3（終了コード 0）の順。標準出力は同じ文面が時刻なしで同じ順 |
| `UT-preprocess_boundaries-28` | 作り直さない・新しい版の警告 | 子のプロセス。27 の後の `<tmp>/data` に、取得完了の記録を置き直す | (a) 引数は既定、(b) `<tmp>/data/ref/` に一時の ZIP を写した `N03-20260101_GML.zip`（中の名前も `N03-20260101.geojson` に変えたもの）を足して、引数は既定 | どちらも 0、4 つの出力と版の記録のバイト列と更新時刻は 27 の後と同じ、取得完了の記録が残る。(a) のログに BL2 `作り直さない: 出力と版の記録がそろっている（版 20250101）` と BL4 `結果の要約: 作り直さなかった。採用した ZIP の版 20250101、版の記録 20250101`。(b) は標準エラー出力とログに BW1（1 行目の後半は `記録した版 20250101、置いてある最新の版 20260101`、2 行目の `{config_opt}` は空白 1 つと `--config <tmp>/c.ini`）、BL1 の ZIP は `<tmp>/data/ref/N03-20260101_GML.zip`、BL4 の ZIP の版は `20260101` |
| `UT-preprocess_boundaries-29` | `--rebuild` | 子のプロセス。27 の後の `<tmp>/data` に、取得完了の記録を置き直す | `--config ../c.ini --rebuild` | 0、BL2 `作り直す: --rebuild を付けた`、取得完了の記録が無い、版の記録は `20250101\n` |
| `UT-preprocess_boundaries-30` | 検証で止まったときは何も変えない | 子のプロセス。27 の後の `<tmp>/data` に、取得完了の記録を置き直し、一時の ZIP を、13 の (a) の書き換えをした小さな N03 のものに置き換える | `--config ../c.ini --rebuild` | 1、標準エラー出力とログに BV5（2 行目に `{rerun}` が入り、`--config <tmp>/c.ini --rebuild` を含む）、ログの L3 の前の行が BL5 `結果の要約: 途中で止まった。終えた分: なし`。4 つの出力と版の記録と取得完了の記録のバイト列は起動の前と同じ。`<tmp>/t` は空 |
| `UT-preprocess_boundaries-31` | 起動の前の止まり方 | 子のプロセス | (a) `--config ../none.ini`、(b) 別のプロセスが `<tmp>/data/findsummits.lock` に `fcntl.flock` で排他ロックを掛けている間に引数は既定、(c) `<tmp>/src/params/mesh_list_japan.txt` を消して引数は既定、(d) `<tmp>/data/ref/` の ZIP を消して引数は既定 | (a) 2、CF1（`対処:` は `--config に渡したパスを確かめる`）、`<tmp>/data/findsummits.lock` と `<tmp>/logs` が無い。(b) 1、G1、`<tmp>/logs` が無い。(c) 1、R1（`{path}` は `<tmp>/src/params/mesh_list_japan.txt`）、ログに BL5（`終えた分: なし`）、`<tmp>/data/boundaries/` は作られていない。(d) 1、BZ1（`{ref_dir}` は `<tmp>/data/ref`）、ログに BL5 |
| `UT-preprocess_boundaries-32` | 置き換えに入った後の要約 | 27 の後の `<tmp>/data` で、11 と同じ形の試験用のプログラムを、`json.load` の代わりに `os.replace` を「3 回目の呼び出しでは元の `os.replace` を呼ばずに自分へ `SIGTERM` を送り、ほかの呼び出しでは元を呼ぶ物」に差し替え、`sys.argv` に `--rebuild` を足して起動する | 起動する | 143。ログの BL5 が `結果の要約: 途中で止まった。終えた分: 地域 60、市区町村 66、除外タイル <n>、除外メッシュ 1。出力の置き換えに入った後に止まった（版の記録が消えていれば、次の起動で作り直す）`。版の記録が無い。もう一度、子のプロセスで引数は既定で起動すると 0 で、BL2 が `作り直す: 版の記録が読めないか、8 桁の数字の 1 行でない: <tmp>/data/boundaries/n03_version.txt`（4 つの出力はある） |
| `UT-preprocess_boundaries-33` | ポリゴンが 0 個のコード | 同じプロセス。小さな N03 の `90005` のフィーチャの幾何を `{"type":"Polygon","coordinates":[]}` にして一時の ZIP にし、`load_n03_features` で読む | `build_municipalities` | 65 フィーチャで、`code` に `90005` を含まない（ほかは `UT-preprocess_boundaries-17` と同じ順） |
| `UT-preprocess_boundaries-34` | ZIP の探す場所と読む場所が同じ | 同じプロセス。`<tmp>/real/child/` と `<tmp>/real/ref/` を作り、`<tmp>/link` から `<tmp>/real/child` へのシンボリックリンクを作る。`<tmp>/real/ref/` に中身が `abc` の `N03-20250101_GML.zip` を置く（`<tmp>/ref/` は作らない） | `find_n03_zip(os.path.join('<tmp>', 'link', '..', 'ref'))` | 戻り値は `('<tmp>/link/../ref/N03-20250101_GML.zip', '20250101')`（`..` を字の上で除かない）。標準出力は BL1 の 1 行で、`{zip_path}` も同じパス（版 20250101、3 バイト） |
| `UT-preprocess_boundaries-35` | 展開できない | 同じプロセス。`<tmp>/data/ref/` に一時の ZIP | `load_n03_features('<tmp>/data/ref/N03-20250101_GML.zip', '20250101')` を (a) `tempfile.TemporaryDirectory` を `OSError(errno.ENOSPC, os.strerror(errno.ENOSPC))` を上げる物に差し替えて、(b) `zipfile.ZipFile.extract` を同じ `OSError` を上げる物に差し替えて呼ぶ | どちらも 1、BF1、`{reason}` は `No space left on device`、標準出力は空。(a) の `{path}` は `tempfile.gettempdir()`（`<tmp>/t`）、(b) の `{path}` は作業用のディレクトリ（`<tmp>/t/findsummits-n03-` で始まる）。`<tmp>/t` は空 |
| `UT-preprocess_boundaries-36` | ポリゴンの計算ができない | 同じプロセス。小さな N03 を一時の ZIP にして `load_n03_features` で読み、`split_nt_polygons` で北方領土の 7 つのポリゴンとそれ以外の 60 のポリゴンに分ける | (a) `shapely.union_all` を `GEOSException('x')` を上げる物に差し替えて `build_regions`、(b) `shapely.union_all` を `shapely.GeometryCollection()` を返す物に差し替えて `build_regions`、(c) `shapely.relate_pattern` を `GEOSException('x')` を上げる物に差し替えて `list_excluded_tiles`（北方領土の 7 つのポリゴン）、(d) (c) と同じ差し替えで `list_excluded_meshes({'6848'}, <北方領土の 7 つのポリゴン>, <それ以外の 60 のポリゴン>)` | どれも 1、BF2、標準出力は空。1 行目の前半は (a) `ERROR: ポリゴンの計算ができない: 地域 愛知県 を合わせる（dissolve）: x（`、(b) `ERROR: ポリゴンの計算ができない: 地域 愛知県 を合わせる（dissolve）: 合わせた結果が面でない: GeometryCollection（`、(c) `ERROR: ポリゴンの計算ができない: 除外タイルを求める: x（`、(d) `ERROR: ポリゴンの計算ができない: 除外メッシュを求める: x（` |

- UT の形の理由: 純粋な関数と、`start_log` を呼ばない関数は同じプロセスで呼ぶ。`main` を通すもの（引数・ロック・ログ・要約・シグナル）は子のプロセスで起動する（[2.1.5](#215-ut-候補)・5.2.5 と同じ分け方）。小さな N03 は、[DEC37](30_HLD.md#4174-設計判断)「地域の SOTA のコードは CMP1 の固定の表で付ける」の「地域が 60 にならなければ止まる」に当たらずに通る最小の入力として、地域ごとに 1 つの矩形と北方領土 6 村の矩形で作る（全国の N03 は大きく、UT の入力にしない。実物は IT の `IT-CMP1-EXT2-01` で読む）。

## 4. CMP2 タイル取得

この章は、CMP2（タイル取得）の 1 本のプログラム（[HLD 3.2.1](30_HLD.md#321-プログラム)）のモジュールを置く。CMP2 にコンポーネント内の共通部品は無い（[HLD 3.2.4](30_HLD.md#324-コンポーネント内の共通部品)）。

### 4.1 `fetch_tiles`

- **ID**: LLD-fetch_tiles
- **対応 HLD**: [3.2](30_HLD.md#32-cmp2-タイル取得)・[4.1](30_HLD.md#41-fr-001-標高タイル事前取得)・[5.4](30_HLD.md#54-nfr-004-アクセスマナー)・[5.5](30_HLD.md#55-nfr-005-処理時間目標)
- **ファイル**: `scripts/fetch_tiles.py`

処理の正本は [HLD 4.1.2](30_HLD.md#412-処理の流れ)（再試行の正本は [HLD 4.1.3](30_HLD.md#413-異常系) の「再試行」）で、関数の名前と役割と呼ぶ順は [HLD 3.2.3](30_HLD.md#323-関数) の表のとおり。この節は Python で書くための細部（型、データの持ち方、スレッド、メッセージの文面、ログの行）だけを足す。[5.4](30_HLD.md#54-nfr-004-アクセスマナー)（アクセスマナー）は、4.1.3 の `build_user_agent`・`_Gate`・`fetch_one_tile` で受ける。[5.5](30_HLD.md#55-nfr-005-処理時間目標)（処理時間）は、実装の後に HLD 5.5.2 の「実測の計画」の 1 で測る（この節では測らない）。結合のつなぎ目は `CMP2-INT1`・`CMP2-EXT1`〜`CMP2-EXT4`（[HLD 3.2.5](30_HLD.md#325-結合のつなぎ目)）で、結合テスト（IT）のケースは `60_IT.md` の `IT-CMP2-INT1-01`〜`06`・`IT-CMP2-EXT1-01`〜`04`・`IT-CMP2-EXT2-01`〜`11`・`IT-CMP2-EXT3-01`〜`03`・`IT-CMP2-EXT4-01`・`02`。

#### 4.1.1 ファイル割付

- 関数はすべて `scripts/fetch_tiles.py` 1 本に置く。`venv/bin/python3 scripts/fetch_tiles.py` で起動され（[HLD 3.2.1](30_HLD.md#321-プログラム)）、共通部品は `import common` で読む（2.1.1 と同じ）。HTTP は標準の `http.client`（と `ssl`・`urllib.parse`）で行う（[環境定義](01_environment.md) の依存を足さない。`requests` は使わない。理由は 4.1.3 の `_Gate`）。並列は標準の `threading`・`queue` で行う。ファイルの先頭のコメントに `# trace: LLD-fetch_tiles` を書く。起動の部分は `if __name__ == '__main__': main()`。
- UT のコードは `tests/scripts/test_fetch_tiles.py` に置く。各テストに `# trace: UT-fetch_tiles-NN` のコメントを付ける。テストの枠組みは 2.1.1 と同じく[テスト方針書 3.4](02_test_policy.md#34-テストを先に書く進め方)で選んだ。

#### 4.1.2 型とデータ

- 定数（モジュールの最上位。どれも内部。テストが差し替えるものは、使うたびにモジュールの属性として引く〈import のときに別の名前へ束縛しない〉）:
  - `_SOURCE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))`、`_JAPAN_MESH_LIST_PATH = os.path.join(_SOURCE_ROOT, 'params', 'mesh_list_japan.txt')`（[HLD 3.2.1](30_HLD.md#321-プログラム) の「自分の置き場から求め、起動した作業ディレクトリによらない」。3.1 と同じ形）。既定の設定ファイルは `common.DEFAULT_CONFIG_PATH`（[2.1.2](#212-型とデータ)）。
  - `_BASE_URL = 'https://cyberjapandata.gsi.go.jp/xyz'`。タイルの URL は `f'{_BASE_URL}/{サービス名}/{z}/{x}/{y}.png'`（[SRS §6](20_SRS.md#6-外部インターフェース仕様) の「タイル URL」の行）。UT と IT は、起動の部分を通さずに `main` を呼ぶ試験用の短いプログラムで、この定数を模擬サーバーの URL に差し替える（4.1.5 の「子のプロセス」。3.1.5 の `UT-preprocess_boundaries-11` と同じ形）。
  - `_KINDS = {'DEM10b': ('dem_png', 14), 'DEM5a': ('dem5a_png', 15), 'DEM5b': ('dem5b_png', 15), 'DEM5c': ('dem5c_png', 15)}`（DEM 種別の名前 → (サービス名, ズーム)。[SRS §8.1](20_SRS.md#81-内部データ一覧) の No.5）。`_KIND_ORDER = ('DEM10b', 'DEM5a', 'DEM5b', 'DEM5c')`（要約と件数の辞書の順）、`_DEM5_KINDS = ('DEM5a', 'DEM5b', 'DEM5c')`（要求の順）。
  - 再試行の固定値（[HLD 4.1.3](30_HLD.md#413-異常系) の「再試行」の表。HLD の固定値で、設定にしない）: `_FIRST_WAIT_S = 60.0`、`_WAIT_FACTOR = 2.0`、`_WAIT_CAP_S = 900.0`（1 回の待ちの上限 15 分）、`_MAX_RETRIES = 5`、`_TIMEOUT_S = 30.0`（接続・送信・読み取りのソケットの操作ごと。`http.client` の接続の `timeout=_TIMEOUT_S`）。
  - `_TOOL_NAME = 'findsummits'`（User-Agent のツール名）。
  - CMP1 の出力の名前（[HLD 4.17.2](30_HLD.md#4172-処理の流れ) の「出力の置き場」の表）: `_NT_TILES_NAME = 'nt_excluded_tiles.txt'`、`_NT_MESHES_NAME = 'nt_excluded_meshes.txt'`、`_C1_VERSION_NAME = 'n03_version.txt'`。置き場は `os.path.join(<data_dir>, 'boundaries')`。
  - `_PROGRESS_POLL_S = 0.2`（メインのスレッドが結果の待ち行列を待つ時間の区切り。4.1.3 の `_run_pool`）。
- タイル: `tuple[int, int]`（`(x, y)`）。DEM 種別は別に持つ。ズーム 15 のタイルの位置も `tuple[int, int]`。キャッシュのパスは内部の関数 `_cache_path(tiles_dir: str, kind: str, tile: tuple[int, int]) -> str` で、`os.path.join(tiles_dir, <サービス名>, str(z), str(x), f'{y}.png')`（`tiles_dir` は `os.path.join(<data_dir>, 'tiles')`）。
- `@dataclass(frozen=True) class _Args`: `config: str | None`（`--config` の値。渡されなければ `None`）、`mesh: str | None`（`--mesh` の値のまま。渡されなければ `None`）。
- 1 枚のタイルの結果: `str` で、`'fetched'`（HTTP 200 を受けて置いた）・`'unchanged'`（HTTP 304）・`'missing'`（HTTP 404）のどれか。
- `@dataclass(frozen=True) class _Stop`（取得を止める要因。ワーカーのスレッドが作ってメインのスレッドへ返す）: `why: str`（`'retry_exceeded'`・`'retry_after'`・`'immediate'`・`'unexpected'`・`'no_last_modified'`・`'file'` のどれか）、`kind: str`、`tile: tuple[int, int]`、`url: str`、`last: str`（最後の応答か失敗の種類の文。4.1.3 の `fetch_one_tile` の「`last` の文」）、`retries: int`（それまでに再試行した回数）、`path: str | None`・`reason: str | None`（`why` が `'file'` のときだけ。扱えなかったファイルのパスと `{reason}`）。
- `class _Gate`（ワーカーの間で共有する待ちと間隔の状態。[HLD 3.2.3](30_HLD.md#323-関数) の `fetch_one_tile` の「持ち方は LLD」）: `__init__(self, interval_ms: int)`。属性は `cond: threading.Condition`、`interval_s: float`（`interval_ms / 1000`）、`next_start: float`（次の要求を始めてよい `time.monotonic()` の時刻。初めは `0.0`）、`pause_until: float`（429・503 で全ワーカーが新しい要求を出さない間の終わりの時刻。初めは `0.0`）、`stopping: bool`（初めは `False`）。属性は `cond` を持っているときだけ読み書きする。メソッドの細部は 4.1.3 の `_Gate`。1 回の起動で 1 つだけ作り、DEM10b と DEM5 の段で共有する（モジュールの状態の `_gate`。段をまたいでもリクエスト間隔と 429・503 の待ちを途切れさせないため）。
- モジュールの状態（内部。モジュールの最上位の変数）: `_config_opt: str`（`main` が `start_log` の後に入れる。3.1 と同じく、`args.config is not None` なら `' --config ' + shlex.quote(config.path)`、それ以外は空の文字列）、`_rerun: str`（`main` が `start_log` の後に入れる、同じ引数で起動し直すコマンド。`'venv/bin/python3 scripts/fetch_tiles.py'` に、`sys.argv[1:]` が空でなければ空白 1 つと `shlex.join(sys.argv[1:])` を足したもの）、`_tally: dict[str, dict[str, int]]`（要約の件数。`main` が `start_log` の後に、`_KIND_ORDER` の各種別に `{'取得': 0, '変更なし': 0, '未整備': 0, '削除': 0}` を入れる。`delete_cached_tiles` と、`download_tiles`・`download_dem5` の結果の受け取り〈メインのスレッド〉が足す）、`_stage: str`（今の段の名前。初めは `'入力の読み込み'`。`main` が段に入るときに入れる）、`_gate: _Gate | None`（初めは `None`。`_run_pool` が初めて呼ばれたときに `_Gate(interval_ms)` を作って入れ、2 回目からはそれを使う）、`_local: threading.local`（スレッドごとの接続の入れ物。属性は `conn`〈その時点の接続。無ければ `None`〉と `key`〈接続を作ったときの `(scheme, host, port)`〉の 2 つ。`fetch_one_tile` の「接続」が入れる）。内部の関数 `_close_connection() -> None` は、呼んだスレッドの `_local.conn` が `None` でなければ `close()` し、`_local.conn` と `_local.key` を `None` にする。
- モジュールの状態の理由: 途中で止まったときの要約（[HLD 5.7.2](30_HLD.md#572-処理の流れ) の 7「結果の要約」の「そこまでに終えた分の件数」）には、止まった段の途中までの件数が要る。HLD 3.2.3 の表で件数は各関数の返すものなので、関数の中で `sys.exit` で止まると返らない。メッセージに要る `{config_opt}`・`{rerun}` も、HLD 3.2.3 の受け取るものに無い。3.1 の `_n03_source`・`_config_opt` と同じ扱い。

#### 4.1.3 関数の細部

- 止まるときは、メッセージを出してから `sys.exit(<定数>)` を呼ぶ（[1.2](#12-lld-の規約) の終わり方の規約と [2.1.3](#213-関数の細部) の呼ぶ側の書き方の型）。`start_log` の後に止まるときは、`main` の `finally` が結果の要約を出す。
- 例外の受け方: 各関数が名前を挙げた例外だけを捕まえる（1.2）。`SignalStop`・`LogWriteError` は捕まえない。ワーカーのスレッドの最上位だけは `except Exception` で捕まえて、メインのスレッドへ渡す（下の `_run_pool`）。
- `{reason}` は [2.1.4](#214-メッセージ文面) と同じ（`OSError` の `strerror`、無ければ `str(e)`）。
- **スレッド**（[HLD 4.1.1](30_HLD.md#411-目的と範囲) の対象外の行「並列取得の実装の形」）: 並列の取得はスレッドで行う（`_run_pool`）。メインのスレッドは、ワーカーを起こし、ワーカーが返す結果を受け取り、件数を数え、途中経過とメッセージを出し、キャッシュを消し、止めると決める。ワーカーのスレッドは、要求を出し、タイルを書き、結果か止まる要因を返すだけで、`common.log_*`・`sys.exit`・`delete_cached_tiles` を呼ばない（1.2 の「`start_log`・`log_*` はメインのスレッドからだけ呼ぶ」。`sys.exit` はワーカーのスレッドでは、そのスレッドを終えるだけでプログラムを止めないため）。シグナル（`SignalStop`）はメインのスレッドだけが受ける。非同期 I/O でなくスレッドにする理由: 標準の `http.client` は同期で、依存を足さずに済む（非同期 I/O の HTTP には新しい依存が要る）。仕事は通信を待つ時間が長く、GIL で遅くならない。最大並列数は 16 まで（2.1.2 の `max_parallel`）。
- 止め方（HLD 4.1.3 の「再試行」の「止めるときは新しい要求を出さず、実行中の要求の終了を待ってから終了コード 1」）: どの止まる要因（再試行の上限超過、すぐ止める応答、想定外の応答、`Last-Modified` が無い応答、ファイルの失敗、ワーカーの例外）でも、シグナルでも、メインのスレッドの `_run_pool` の `finally` が `_Gate` を止め（新しい要求を出させず、待っているワーカーを起こす）、全ワーカーの終わりを待ってから先へ進む。

##### main（fetch_tiles）

`main() -> None`。[2.1.3](#213-関数の細部) の呼ぶ側の書き方の型に従い、次の順に行う。

1. `start = common.StartTime.now()`。
2. `args = _parse_args(sys.argv[1:])`（`--help` と引数の誤りは、ここで止まる）。
3. `mesh_arg = common.read_mesh_arg(args.mesh)`（`args.mesh` が `None` なら `mesh_arg = None`。誤りは A1〜A5 で終了コード 2）。
4. `config_path` は `args.config` が `None` なら `common.DEFAULT_CONFIG_PATH`、それ以外は `args.config`。`config = common.load_config(config_path, ('data_dir', 'log_dir', 'max_parallel', 'interval_ms', 'user_agent_email'), ('data_dir', 'user_agent_email'))`（[HLD 2.3.2](30_HLD.md#232-設定ファイル) の表で CMP2 が使うキーと、[HLD 2.3.3](30_HLD.md#233-検証と記録) の必須のキー）。`data_dir`・`log_dir`・`max_parallel`・`interval_ms` は `config.values` のその値。`boundaries_dir = os.path.join(data_dir, 'boundaries')`、`tiles_dir = os.path.join(data_dir, 'tiles')`。
5. `common.acquire_lock(data_dir)`。
6. `common.start_log(log_dir, config, 'fetch_tiles', sys.argv[1:], start)`。モジュールの状態の `_config_opt`・`_rerun`・`_tally`・`_stage`（`'入力の読み込み'`）を入れる。
7. `try` の前に、`completed = False`、`code = common.EXIT_OK`、要約のための状態（`outcome: str | None = None`〈`'fetched'` か `'empty'`〉、`targets: set[str] = set()`、`removed = False`〈取得完了の記録から対象を外したか〉、`sea_lines: list[tuple[str, int, int]] = []`、`sea_skipped = 0`）と、記録の書き込みに使う `record_path`・`kept: set[str]` を置く（[2.1.3](#213-関数の細部) の呼ぶ側の書き方の型）。`try` の中で次を呼ぶ（HLD 3.2.3 の呼ぶ順）:
   1. `japan = common.read_mesh_list_file(_JAPAN_MESH_LIST_PATH, None)`。`nt_meshes = common.read_mesh_list_file(os.path.join(boundaries_dir, _NT_MESHES_NAME), _cmp1_action())`（`_cmp1_action()` は 4.1.4 の `{cmp1}` の文を返す内部の関数）。`nt_tiles = read_excluded_tiles(os.path.join(boundaries_dir, _NT_TILES_NAME))`。`check_c1_version_record(boundaries_dir)`。
   2. `record_path = common.fetch_record_path(data_dir)`。`record = read_fetch_record(record_path)`。
   3. `targets = select_fetch_meshes(mesh_arg, japan, nt_meshes)`。TL1 を `common.log_info` で出す。
   4. `targets` が空なら: `_stage = '古いキャッシュの削除'`、`delete_cached_tiles(list_stale_tiles(japan, nt_meshes, nt_tiles), tiles_dir)`、`outcome = 'empty'`、`completed = True`（5 から 9 を行わない。`if`/`else` で分け、`return` を使わない。`return` で抜けると `finally` の後の `sys.exit(code)` に届かない）。
   5. そうでなければ: `dem10b, positions = list_fetch_tiles(targets, nt_tiles)`。`kept = remove_from_record(record_path, record, targets, mesh_arg is not None)`、`removed = True`。
   6. `_stage = '古いキャッシュの削除'`、`delete_cached_tiles(list_stale_tiles(japan, nt_meshes, nt_tiles), tiles_dir)`。
   7. `user_agent = build_user_agent(config.values['user_agent_email'].value)`。TL2 を出す。`_stage = 'DEM10b の取得'`、`_, notfound = download_tiles(dem10b, tiles_dir, max_parallel, interval_ms, user_agent)`。
   8. `_stage = 'DEM10b の検査'`、`check_dem10b_meshes(targets, dem10b, notfound, tiles_dir)`。`sea, sea_lines = find_sea_positions(positions, dem10b, notfound, targets, nt_tiles)`。
   9. `_stage = 'DEM5 の取得'`、`_, sea_skipped = download_dem5(positions, sea, tiles_dir, max_parallel, interval_ms, user_agent)`。`outcome = 'fetched'`、`completed = True`。
8. `finally` で結果の要約を `common.log_info` で 1 回出す（[4.1.4](#414-メッセージ文面) の TL4〜TL6。`completed` が真なら `outcome` で TL4 か TL5、偽なら TL6。件数は `_tally` から）。
9. `finally` の後、`outcome == 'fetched'` なら `write_fetch_record(record_path, kept | targets)`（`--mesh` が無ければ `kept` は空なので、記録は今回の対象の集合ちょうど。`completed` が偽なら、例外が `finally` を抜けて伝わるので、ここに届かない）。
10. `sys.exit(code)`。

- 要約と記録の順: HLD 3.2.3 の呼ぶ順のとおり、要約を出してから記録を書く。[2.1.3](#213-関数の細部) の書き方の型で要約は `finally` に置くので、記録の書き込みは `finally` の後、`sys.exit(code)` の前に置く。記録を書けなかったときは、要約の後に TF1 が出て終了コード 1 になる。要約の 1 行目は「タイルの取得を終えた（取得完了の記録はこの後に書く）」として記録の書き込みに触れず、続く TF1 と終了コード 1 が途中で止まったことを示す（[HLD 5.7.2](30_HLD.md#572-処理の流れ) の 7「結果の要約」の「途中で止まったことが分かる形」を、要約と TF1 の組で満たす）。選ばなかった案: 記録を書いてから要約を出す（HLD 3.2.3 の順と食い違う）。

##### _parse_args（fetch_tiles）

`_parse_args(argv: Sequence[str]) -> _Args`（内部）。3.1 の `_parse_args` と同じ手順で、名前と記号だけが違う。

1. [1.2](#12-lld-の規約) の利用者向けの Python のコマンドの引数の受け方で読む。受け付ける名前は、`--config`・`--mesh`（値を 1 つとる）、`--help`（値をとらない）だけ（[HLD 2.4.2](30_HLD.md#242-共通の書式)・[2.4.3](30_HLD.md#243-メッシュ範囲)）。
2. 誤りは TA1（受け付けない引数）、TA2（値が無い）、TA4（同じ名前を 2 回）で、`common.log_error` で出して `sys.exit(common.EXIT_USAGE)`。1 つの引数が値をとらない名前に `=` を付けたもの（`--help=x`）なら、同じ名前を読んだことがあっても TA1 とする（TA1 の判定を TA4 の判定より先にする）。
3. `--help` は、[4.1.4](#414-メッセージ文面) の使い方の文を `sys.stdout.write` で出し、`sys.stdout.flush()` の後に `sys.exit(common.EXIT_OK)`。引数は左から 1 つずつ処理して、その場で 2 か 3 を行うので、`--help` より前の引数の誤り（TA1・TA2・TA4）は先に止まり、`--help` より後の引数は誤りも見ずに終わる（`--mesh 5339 --help --foo` は 0、`--foo --help` は TA1）。TA3 は読み終えた後に判定するので、`--config '' --help` は 0 になる。`--mesh` の値の中身（4 桁かファイルか）は見ない（`main` の 3 の `read_mesh_arg` が見る。`--mesh '' --help` も 0）。
4. 読み終えたら、`--config` の値が空の文字列なら TA3 で `sys.exit(common.EXIT_USAGE)`。`--mesh` の値が空の文字列のときは、ここでは止めない（`read_mesh_arg` の A1）。
5. `_Args(config=<値か None>, mesh=<値か None>)` を返す。

##### read_excluded_tiles

`read_excluded_tiles(path: str) -> set[tuple[int, int]]`

1. `open(path, 'rb')` で全部を読む。`FileNotFoundError` なら TP1、ほかの `OSError`（ディレクトリを含む）なら TP2（`{detail}` は `{reason}`）で `sys.exit(common.EXIT_ERROR)`。
2. 空のバイト列なら空の集合を返す。そうでなければ、最後の `b'\n'` を 1 つ除いてから `b'\n'` で行に分け、1 から番号を振る。各行が `re.fullmatch(rb'([0-9]{1,5}) ([0-9]{1,5})', line)` に合い、2 つの数がどちらも `2 ** 15` 未満なら `(int(x), int(y))` を集合に入れる（重なりは 1 つ）。合わない最初の行で TP2（`{detail}` は `{line_no} 行目が「x y」の形でない: {line}`。`{line}` は `line.decode('utf-8', 'backslashreplace')`）で止まる。
3. 集合を返す。

- 読み方の理由: リストは CMP1 だけが書くファイルで、書く側（[3.1.3](#313-関数の細部) の `write_temp_outputs`）は各行 `f'{x} {y}\n'`（ズーム 15）を書く。読み方を 2.3 の取得完了の記録と同じ厳しさにし、壊れたリストを読み飛ばさない（北方領土の除外はこのリストだけで担保される。[DEC39](30_HLD.md#414-設計判断)「CMP2 は CMP1 の版の記録が無ければ止まる」の理由と同じ）。空行・空白 2 つ・CR・`#` の行は書式違い。

##### check_c1_version_record

`check_c1_version_record(boundaries_dir: str) -> None`

`path = os.path.join(boundaries_dir, _C1_VERSION_NAME)`。`os.path.isfile(path)` が偽なら TP3 で `sys.exit(common.EXIT_ERROR)`。中身は読まない（空のファイルや 8 桁の日付でない中身でも止まらない。[DEC39](30_HLD.md#414-設計判断)「CMP2 は CMP1 の版の記録が無ければ止まる」。`IT-CMP2-EXT1-04`）。同じ名前のディレクトリは無いものとする（[3.1.3](#313-関数の細部) の `needs_rebuild` の 2 と同じ）。

##### read_fetch_record

`read_fetch_record(path: str) -> set[str]`

読み方は [2.3](#23-ファイルの名前と書き方) の取得完了の記録の決まりのとおり（[5.1.3](#513-関数の細部) の `check_fetch_record` と同じ判定）。

1. `open(path, 'rb')` で全部を読む。`FileNotFoundError` なら空の集合を返す（記録が無ければ、取得を終えたメッシュは無い。[HLD 4.1.2](30_HLD.md#412-処理の流れ) の 2「入力を読む」）。ほかの `OSError`（ディレクトリを含む）なら FC2（`{detail}` は `{reason}`）で `sys.exit(common.EXIT_ERROR)`。
2. 空のバイト列なら空の集合を返す。そうでなければ、最後の `b'\n'` を 1 つ除いてから `b'\n'` で行に分け、各行が `re.fullmatch(rb'[0-9]{4}', line)` に合えば `line.decode('ascii')` を集合に入れる。合わない最初の行で FC2（`{detail}` は `{line_no} 行目が 4 桁の数字でない: {line}`。`{line}` は `line.decode('utf-8', 'backslashreplace')`）で止まる。
3. 集合を返す。

##### select_fetch_meshes

`select_fetch_meshes(mesh_arg: set[str] | None, japan: set[str], nt_meshes: set[str]) -> set[str]`

`mesh_arg` が `None` なら `japan - nt_meshes` を返す（警告しない）。そうでなければ、`sorted(mesh_arg)` の順に、`japan` に無いコードは TW1、`nt_meshes` にあるコードは TW2 を `common.log_warning` で出して飛ばし（日本全土のリストに無いかを先に見る）、残りの集合を返す（空でもよい。[HLD 4.1.2](30_HLD.md#412-処理の流れ) の 3「対象のメッシュを決める」）。

##### mesh_tile_range

`mesh_tile_range(mesh: str, z: int) -> tuple[int, int, int, int]`（返すのは `(x_min, x_max, y_min, y_max)`。両端を含む）

`((s, w), (n, e)) = common.mesh_to_latlon(mesh)` の四隅に、[2.4](#24-言語ごとに別に実装する式のテストベクトル) の「メッシュの取得範囲の決まり」を当てる。タイル番号は `common.latlon_to_tile` で求め、`2^z` は `2 ** z` と書く（Python の `/` は整数どうしでも倍精度の値を返す）。引数を検査しない。

##### list_fetch_tiles

`list_fetch_tiles(meshes: set[str], nt_tiles: set[tuple[int, int]]) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]`（返すのは（DEM10b のタイルの集合, ズーム 15 のタイルの位置の集合））

- DEM10b: 各メッシュの `mesh_tile_range(mesh, 14)` の範囲のタイルを合わせ、`{(x // 2, y // 2) for (x, y) in nt_tiles}` を除く（[ADR-SRS-018](decisions/ADR-SRS-018-northern-territories-skip-at-tile-fetch.md)）。
- ズーム 15 の位置: 各メッシュの `mesh_tile_range(mesh, 15)` の範囲の位置を合わせ、`nt_tiles` を除く。
- `mesh_tile_range` はモジュールの属性として呼ぶ（テストが差し替える。[4.1.5](#415-ut-候補) の「小さな範囲」）。

##### remove_from_record

`remove_from_record(path: str, record: set[str], meshes: set[str], mesh_given: bool) -> set[str]`

`kept = record - meshes`（`mesh_given` が偽なら `kept = set()`）。`write_fetch_record(path, kept)` を呼び（記録が無かったときも書く。中身が変わらないときも書き直す）、`kept` を返す（[HLD 4.1.2](30_HLD.md#412-処理の流れ) の 5「取得完了の記録から、今回の対象のメッシュを外す」）。

##### write_fetch_record

`write_fetch_record(path: str, codes: set[str]) -> None`

1. `os.makedirs(os.path.dirname(path), exist_ok=True)`（初めての起動では `tiles/` が無い）。`OSError` なら TF1（`{path}` は `tiles/` のパス）で止まる。
2. [2.3](#23-ファイルの名前と書き方) の一時ファイルの決まりの「書く」の段で、`path + '.tmp'` に `''.join(f'{c}\n' for c in sorted(codes))` を書く（2.3 のテキストのモードの開き方。0 件なら空のファイル）。書けなければ、2.3 のとおり一時ファイルを消してから TF1（`{path}` は一時ファイルのパス）で止まる。
3. `os.replace(path + '.tmp', path)`。`OSError` なら、一時ファイルを `os.remove` で消してから（消せないときの `OSError` は無視する）、TF1（`{path}` は記録のパス）で止まる。

止まるのは、どれも `common.log_error` の後の `sys.exit(common.EXIT_ERROR)`（[HLD 2.5.5](30_HLD.md#255-書き込みの失敗)）。

##### list_stale_tiles

`list_stale_tiles(japan: set[str], nt_meshes: set[str], nt_tiles: set[tuple[int, int]]) -> dict[str, set[tuple[int, int]]]`（返すのは `_KIND_ORDER` の 4 つの種別をキーにした辞書。DEM5a・5b・5c は同じ集合）

[HLD 4.1.2](30_HLD.md#412-処理の流れ) の 6「古いキャッシュを消す」の ① と ② の和を、ズームごとに求める。

1. ズーム 15: ① `nt_tiles`。② `japan & nt_meshes` の各メッシュの `mesh_tile_range(mesh, 15)` の範囲の位置のうち、`japan - nt_meshes` のどのメッシュの `mesh_tile_range(mesh, 15)` の範囲にも入らないもの。
2. ズーム 14: ① `{(x // 2, y // 2) for (x, y) in nt_tiles}`。② 1 の ② と同じく、`mesh_tile_range(mesh, 14)` で求める。
3. `{'DEM10b': <2 の和>, 'DEM5a': <1 の和>, 'DEM5b': <1 の和>, 'DEM5c': <1 の和>}` を返す（DEM5 の 3 つは同じ集合を別々に入れる）。

- ② の求め方: 除外メッシュでないメッシュの範囲は `(x_min, x_max, y_min, y_max)` の並びのまま持ち、タイルが範囲のどれかに入るかを比べる（日本全土のタイルの集合を作らない。北方領土除外メッシュは数が少ないので、比べる数は小さい）。`--mesh` で範囲を絞った実行でも、受け取る `japan` は日本全土 1 次メッシュコードリストのまま（呼ぶ側の `main` が渡す）。

##### delete_cached_tiles

`delete_cached_tiles(tiles_by_kind: Mapping[str, Iterable[tuple[int, int]]], tiles_dir: str) -> dict[str, int]`（返すのは `_KIND_ORDER` の 4 つの種別をキーにした、消した数〈無かったものは数えない〉）

`_KIND_ORDER` の順に、`tiles_by_kind` にある種別のタイルを `sorted` の順に、`os.remove(_cache_path(tiles_dir, kind, tile))` で消す。`FileNotFoundError` は無視して数えない。ほかの `OSError`（ディレクトリのときの `IsADirectoryError`・`PermissionError` を含む）なら TF3 で `sys.exit(common.EXIT_ERROR)`。消した数を `_tally[kind]['削除']` にも足す。メインのスレッドだけが呼ぶ（前置きの「スレッド」）。

##### build_user_agent

`build_user_agent(user_agent_email: str) -> str`

1. `version, problem = _software_version()`。`problem` が `None` でなければ TW3 を `common.log_warning` で出す（`{reason}` は `problem`）。
2. `f'{_TOOL_NAME}/{version} (mailto:{user_agent_email})'` を返す（[HLD 2.3.2](30_HLD.md#232-設定ファイル) の User-Agent の段落、[SRS §2.2.1](20_SRS.md#221-設定可能項目) の形）。`user_agent_email` の検査は `load_config` が済ませている（[2.1.2](#212-型とデータ) の `_CONFIG_KEYS`）。

`_software_version() -> tuple[str, str | None]`（内部。返すのは（版, 取れなかった理由か `None`））: `subprocess.run(['git', '-C', _SOURCE_ROOT, 'describe', '--tags', '--dirty', '--always'], stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=10)`。`FileNotFoundError`（git が無い）なら `('unknown', 'git が無い')`、ほかの `OSError` と `subprocess.TimeoutExpired` なら `('unknown', 'git describe を起動できない: ' + <str(e) の 1 行目>)`、終了コードが 0 でなければ `('unknown', f'git describe の終了コード {rc}')`、標準出力の前後の空白を除いた文字列が `re.fullmatch(r'[0-9A-Za-z._+-]+', s)` に合わなければ `('unknown', 'git describe の出力が版の形でない')`、合えば `(s, None)`。

- 版の取り方の理由: HLD 2.3.2 の「バージョンは解析ソフトウェアの版」を、HLD の [DEC98](30_HLD.md#494-設計判断)「版の文字列は出力を組み立てるときに git から取る」（`software_version`）と同じ取り方にする。「固定値」は設定で変えない値と読む（[開発ガイド](03_development.md#5-バージョンとタグ) は `VERSION` ファイルや文書内の番号表を作らないとしているので、版をコードの定数として持たない）。取れないときに止めないのは、User-Agent の目的（連絡先を示す）が版によらず満たせるため。選ばなかった案: 版をモジュールの定数に書く（版を上げるたびにコードを直すことになり、開発ガイドの「正本は git の annotated tag」と二重になる）。版を付けない（SRS §2.2.1 の形にならない）。

##### _Gate

`_Gate`（内部のクラス。[4.1.2](#412-型とデータ)）。メソッドはどれもワーカーのスレッドからもメインのスレッドからも呼んでよく、属性は `cond` を持って読み書きする。時刻は `time.monotonic()`。

- `send(self, do_send: Callable[[], None]) -> bool`: 次の要求を始めてよくなるまで待ち、`cond` を持ったまま `do_send()`（要求の行とヘッダーを送る。`fetch_one_tile` の 2 の 2）を呼んで真を返す。止まる（`stopping`）なら `do_send` を呼ばずに偽を返す。`cond` を持って繰り返す: `stopping` なら偽を返す。`now = time.monotonic()`、`t = max(next_start, pause_until)`。`now >= t` なら `do_send()` を呼び、`finally` で `next_start = time.monotonic() + interval_s`（送信を終えた時刻から間隔を取る。例外は `next_start` を進めてからそのまま呼ぶ側へ伝わる）にして、真を返す。そうでなければ `cond.wait(t - now)`。リクエスト間隔は、全ワーカーの要求の開始（送信）どうしの間隔として守る（[HLD 4.1.3](30_HLD.md#413-異常系) の「全体で要求の開始どうしの間隔として守る」）。次の送信は前の送信を終えてから `interval_s` 後より前に始まらないので、ロックの中で送信が遅れても、送信の始まりどうしの間隔は `interval_s` 以上になる。`interval_s` が 0 なら、`pause_until` の前のほかは待たない。
- `pause(self, seconds: float) -> None`: `cond` を持って `pause_until = max(pause_until, time.monotonic() + seconds)`、`cond.notify_all()`（429・503 の待ちのあいだ、全ワーカーが新しい要求を出さない。実行中の要求は止めない）。
- `sleep(self, seconds: float) -> bool`: `deadline = time.monotonic() + seconds`。`cond` を持って、`stopping` でなく `time.monotonic() < deadline` のあいだ `cond.wait(deadline - time.monotonic())`。`not stopping` を返す（429・503 以外の失敗で、そのタイルのワーカーだけが待つ）。
- `stop(self) -> None`: `cond` を持って `stopping = True`、`cond.notify_all()`。
- `restart(self) -> None`: `cond` を持って `stopping = False`（`_run_pool` が段の始めに呼ぶ。`next_start` と `pause_until` はそのまま引き継ぐ）。

判定と送信を同じロックの中で行うので、`pause`・`stop` は送信中のワーカーの送信が終わるまで待ち、`pause`・`stop` の後に送信が始まることは無い（HLD 4.1.3 の「全ワーカーが新しい要求を出さない」「止めるときは新しい要求を出さず」）。送信を終えて応答を待っている要求は、実行中の要求としてそのまま完了させる。ロックを持つのは要求の行とヘッダー（数百バイト）を送るあいだだけで、応答はロックの外で読む（並列は応答を待つあいだに効く）。送信が詰まったときにロックを持つ時間の上限は、ソケットのタイムアウト（`_TIMEOUT_S`）。

- 判定と送信を 1 つのロックで行い、標準の `http.client` を使う理由: 判定の後にロックを放してから送ると、その間に別のワーカーが `pause`・`stop` をしても送信が始まり、HLD 4.1.3 の字句に反する。`requests` は 1 回の呼び出しで送信と応答の読み取りをするので、送信だけをロックの中に入れられない。選ばなかった案: `requests` のまま、判定の時点を要求の開始と定義する（HLD の語を LLD で読み替えることになる）。ロックを持ったまま応答まで読む（並列にならず、HLD の [DEC155](30_HLD.md#234-設計判断)「タイル取得は並列 8・間隔なしを既定にする」と合わない）。

##### _run_pool

`_run_pool(items: Sequence[T], work: Callable[[T, _Gate], tuple[object | None, _Stop | None]], max_parallel: int, interval_ms: int, what: str, on_done: Callable[[T, object], None]) -> _Stop | None`（内部。`download_tiles`・`download_dem5` が使う。`T` は各関数の仕事の単位〈タイルか位置〉。`work` は（確定した結果か `None`, 止まる要因か `None`）を返す）

1. `items` が空なら `None` を返す（途中経過も出さない。[HLD 5.7.2](30_HLD.md#572-処理の流れ) の 5「途中経過」の「全件数が 0 のときは出さない」）。
2. `_gate` が `None` なら `_gate = _Gate(interval_ms)` にする。`gate = _gate`、`gate.restart()`。`results = queue.Queue()`、`it = iter(items)` と、`it` を引くための `threading.Lock`、起こしたワーカーの並び `threads = []`。
3. ワーカー: `try` の中で繰り返し、ロックを持って `next(it, None)` で次の単位を取り（`None` なら抜ける）、`res, stop = work(item, gate)` を呼ぶ。`res` が `None` でなければ `results.put(('done', item, res))`（止まる要因と一緒に返った、そこまでに確定した結果も送る）。`stop` が `None` でなければ `results.put(('stop', stop))`、`gate.stop()` して抜ける。`res` も `stop` も `None`（止まるので待ちを切り上げた。止まった後は `work` の中の `gate.send()` が偽を返す）なら抜ける。`except Exception as e` なら `results.put(('crash', e))`、`gate.stop()`。`finally` で、`_close_connection()` を呼び（ワーカーが使っていた接続を開いたまま残さない。残すと、メインのスレッドが止まる要因を受けて終わるときに、閉じていない接続が `ResourceWarning` として標準エラー出力に出うる）、続けて `results.put(('exit', None))`。
4. メインのスレッド: `done = 0`、`last_pct = 0`、`alive = 0`、`first_stop = None`、`crash = None`。`try` の中で、まず `threading.Thread(target=<ワーカー>, daemon=True)` を `min(max_parallel, len(items))` 個、1 つずつ作り、`threads` に足してから `start()` し、`alive += 1` する（起こしている途中でシグナルを受けても、下の `finally` を通るように、起こすのも `try` の中で行う。`start()` の前に足すので、`start()` の直後にシグナルを受けても、起こしたワーカーは `threads` に入っている）。続けて、`alive > 0` のあいだ `ev = results.get(timeout=_PROGRESS_POLL_S)`（`queue.Empty` なら続ける。シグナルを受けられるように、区切って待つ）を受けて、下の「受け取り」をする。`finally` で `gate.stop()`、`threads` のワーカーのうち始まったもの（`t.ident is not None`。`start()` の前にシグナルを受けたワーカーは始まっていないので、`join()` すると `RuntimeError` になる）を `join()` し、その後に待ち行列に残っているものを `results.get_nowait()` で `queue.Empty` まで取り出して、同じ「受け取り」をする。この取り出しの `on_done` を `try`/`except SystemExit as e` で囲み、最初の `e` を控えて取り出しを続け（2 つ目からの `SystemExit` は捨てる）、取り出し終えてから控えた `e` を上げ直す（取り出しの途中で `on_done` の削除が失敗しても〈TF3〉、残りの結果の件数は数え終える）（シグナル・`LogWriteError`・`on_done` の中の `sys.exit` で抜けるときも、実行中の要求の終わりを待ち、その間に確定した結果も数える。HLD 4.1.3 の「再試行」、HLD 5.7.2 の 7「結果の要約」の「そこまでに終えた分の件数」）。
   - 受け取り: `'done'` なら `on_done(item, res)`、`done += 1`、`pct = done * 100 // len(items)` が `last_pct` より大きければ TL3 を `common.log_info` で出して `last_pct = pct`。`'stop'` なら、最初のものだけを `first_stop` に入れる。`'crash'` なら最初のものだけを `crash` に入れる。`'exit'` なら `alive -= 1`。
5. `crash` があれば `raise crash`（ワーカーの例外をメインのスレッドで上げ直し、[2.1.3](#213-関数の細部) の `_excepthook` の G7 と Traceback で止まる）。なければ `first_stop`（`None` のこともある）を返す。

- `on_done` はメインのスレッドで呼ばれ、`_tally` に足し、キャッシュを消す（`delete_cached_tiles`）。止まる要因を受けた後に届いた `'done'` も数える（止める前に実行中だった要求の結果）。
- `finally` の `join()` の途中で 2 回目のシグナルを受けても、2.1 の `_on_signal` は 2 回目から何もしない（例外を上げない）ので、`join()` は続く。`finally` の後の取り出しで `on_done` が `sys.exit` を呼ぶと（TF3）、シグナルで抜ける途中なら 2.1 の `_finish_log` の 2 のとおり、終了コードは 128＋シグナルの番号のままになる。
- ワーカーごとに 1 つの接続（`http.client.HTTPConnection` か `HTTPSConnection`）を使う（`_local` に持ち、初めて要求を出すときに作る。スレッドの間で共有しない。作り方と使い直し方は `fetch_one_tile` の「接続」）。
- 仕事の配り方の理由: 単位ごとに `Future` を作る `concurrent.futures` でなく、ワーカーが共有の反復子から 1 つずつ取る形にする。止めると決めたときに、まだ取っていない単位はどのワーカーも取らないので、取り消しの手順が要らない（`Future` を先に全部作ると、止めるときに未着手の `Future` を取り消す手順が要る）。結果は 1 つの待ち行列で、終わった順にメインのスレッドへ届く。全国の DEM5 の位置は 100 万を超え、単位ごとに `Future` と結果を持つと、そのぶんのメモリも先に使う。

##### download_tiles

`download_tiles(tiles: set[tuple[int, int]], tiles_dir: str, max_parallel: int, interval_ms: int, user_agent: str) -> tuple[dict[str, int], set[tuple[int, int]]]`（返すのは（`{'取得': …, '変更なし': …, '未整備': …}`, HTTP 404 だったタイルの集合））

1. `sorted(tiles)` を単位にして `_run_pool` を呼ぶ（`what` は `DEM10b のタイル`）。`work` は `r = fetch_one_tile('DEM10b', tile, _cache_path(tiles_dir, 'DEM10b', tile), user_agent, gate)` を呼び、`r` が結果の文字列なら `(r, None)`、`_Stop` なら `(None, r)`、`None` なら `(None, None)` を返す。`on_done` は、結果の名前（`'fetched'` → `取得`、`'unchanged'` → `変更なし`、`'missing'` → `未整備`）の数と `_tally['DEM10b']` に 1 を足し、`'missing'` ならタイルを 404 の集合に入れる。HTTP 404 のタイルのキャッシュはここでは消さない（[HLD 3.2.3](30_HLD.md#323-関数) の表）。
2. `_run_pool` が `_Stop` を返したら、`_report_stop(stop)`（下）で止まる。
3. 数と 404 の集合を返す。

`_report_stop(stop: _Stop) -> NoReturn`（内部）: `stop.why` が `'no_last_modified'` なら TG2、`'file'` なら TF2、それ以外なら TG1 を `common.log_error` で出して `sys.exit(common.EXIT_ERROR)`。

##### check_dem10b_meshes

`check_dem10b_meshes(meshes: set[str], dem10b_tiles: set[tuple[int, int]], notfound: set[tuple[int, int]], tiles_dir: str) -> int`

1. `sorted(meshes)` の順に、`mesh_tile_range(mesh, 14)` の範囲のタイルのうち `dem10b_tiles` にあるものを求める。それが空のメッシュは見ない（範囲がすべて北方領土除外で除かれたメッシュ）。それがすべて `notfound` にあるメッシュを、タイルの数とともに控える。
2. 控えたメッシュがあれば TD1 で `sys.exit(common.EXIT_ERROR)`（DEM5 を要求せず、404 のキャッシュも消さない。HLD の [DEC154](30_HLD.md#414-設計判断)「DEM10b がすべて 404 のメッシュでは止める」）。
3. 無ければ、`delete_cached_tiles({'DEM10b': notfound}, tiles_dir)` で 404 だったタイルのキャッシュを消し、消した数を返す。

##### find_sea_positions

`find_sea_positions(positions: set[tuple[int, int]], dem10b_tiles: set[tuple[int, int]], notfound: set[tuple[int, int]], meshes: set[str], nt_tiles: set[tuple[int, int]]) -> tuple[set[tuple[int, int]], list[tuple[str, int, int]]]`（返すのは（海の位置の集合, メッシュごとの（メッシュ, 判定対象の位置数, 海の位置数）の並び。メッシュの昇順））

1. `positions` の各位置 `(x, y)` について、DEM10b のタイル `(x // 2 + dx, y // 2 + dy)`（`dx`・`dy` は `-1`・`0`・`1` の 9 枚）がすべて `notfound` にあれば海の位置とする（`notfound` は `dem10b_tiles` の部分集合なので、`dem10b_tiles` に無いタイル〈今回の対象の範囲の外と、北方領土除外で要求しないタイル〉は 404 でなかったものとして扱われる。[HLD 4.1.2](30_HLD.md#412-処理の流れ) の 7「タイルを次の順に取得する」の 3、HLD の [DEC153](30_HLD.md#414-設計判断)「海の位置では DEM5 を取らない」）。
2. `sorted(meshes)` の順に、`mesh_tile_range(mesh, 15)` の範囲の位置のうち `nt_tiles` に無いものの数（判定対象の位置数）と、そのうち海の位置の数を求める（隣のメッシュと共有する位置は、それぞれのメッシュで数える。HLD 4.1.2 の 8「件数と海の位置を要約して出す」）。

##### download_dem5

`download_dem5(positions: set[tuple[int, int]], sea: set[tuple[int, int]], tiles_dir: str, max_parallel: int, interval_ms: int, user_agent: str) -> tuple[dict[str, dict[str, int]], int]`（返すのは（`_DEM5_KINDS` の各種別に `{'取得': …, '変更なし': …, '未整備': …, '404 で削除': …, '下位で削除': …}` を入れた辞書, 海として要求しなかった位置の数 `len(sea)`））

1. `sorted(positions - sea)` を単位にして `_run_pool` を呼ぶ（`what` は `DEM5 の位置`）。海の位置は要求せず、キャッシュにも手を入れない（HLD の [DEC153](30_HLD.md#414-設計判断)「海の位置では DEM5 を取らない」）。
2. `work(pos, gate)`: `results = []`。`_DEM5_KINDS` の順に `r = fetch_one_tile(kind, pos, _cache_path(tiles_dir, kind, pos), user_agent, gate)`。`r` が `_Stop` なら `(results or None, r)` を、`None` なら `(results or None, None)` を返す（そこまでに確定した種別の結果も返す）。`results.append((kind, r))`。`r` が `'missing'` なら次の種別へ。`'fetched'` か `'unchanged'` なら `(results, None)` を返す。DEM5c まで `'missing'` なら `(results, None)` を返す。`results` は要求した種別ごとの結果の並び（例 `[('DEM5a', 'missing'), ('DEM5b', 'fetched')]`）。
3. `on_done(pos, results)`: 要求した各種別の結果の数と `_tally` に 1 を足す。続けて `delete_cached_tiles` を 2 回に分けて呼ぶ。1 回目は `'missing'` だった種別の、その位置のキャッシュを消し（`{<種別>: [pos], …}`）、返った数を、消した種別の `404 で削除` に足す（種別ごとの数で、消えた種別の欄に足す）。2 回目は、最後の結果が `'fetched'` か `'unchanged'` のときだけ、その種別より下位の種別（DEM5a なら DEM5b・5c、DEM5b なら DEM5c）の、その位置のキャッシュを消し、返った数を、消した下位の種別の `下位で削除` に足す（DEM5a で終えて DEM5b・5c のキャッシュを消したなら、DEM5b の欄と DEM5c の欄に 1 つずつ）（HLD 4.1.2 の 7 の 4・5、HLD の [DEC152](30_HLD.md#414-設計判断)「DEM5 は上の種別が無い位置でだけ取る」）。止まる要因と一緒に返った途中までの結果（最後が `'missing'`）では、2 回目を呼ばない。
4. `_run_pool` が `_Stop` を返したら、`_report_stop(stop)` で止まる。

- 消す時機の理由: HLD 4.1.2 の応答の表の「DEM5 は 7 の 4・5 の位置ごとの処理のとき」。位置の要求を終えたワーカーが結果を返し、メインのスレッドが受け取った時点で消す（ワーカーは消さない。前置きの「スレッド」）。同じ位置は 1 つのワーカーだけが扱い、結果を返した後はその位置に触れないので、消す間に同じパスへ書くワーカーは無い。

##### fetch_one_tile

`fetch_one_tile(kind: str, tile: tuple[int, int], path: str, user_agent: str, gate: _Gate) -> str | _Stop | None`（返すのは 1 枚の結果〈[4.1.2](#412-型とデータ)〉か、止まる要因か、止まるので待ちを切り上げたときの `None`。ワーカーのスレッドで動く。キャッシュは消さない）

1. `url = f'{_BASE_URL}/{サービス名}/{z}/{x}/{y}.png'`（メッセージに出す URL）。`headers = {'User-Agent': user_agent}`。`os.stat(path)` が成功し、通常のファイル（`stat.S_ISREG`）なら `headers['If-Modified-Since'] = email.utils.formatdate(st.st_mtime, usegmt=True)`（[ADR-SRS-032](decisions/ADR-SRS-032-gsi-tile-latest-date-provenance.md)）。`FileNotFoundError` なら付けない。ほかの `OSError` と、通常のファイルでないとき（同じ名前のディレクトリなど）は `_Stop(why='file', path=path, reason=<{reason}、通常のファイルでないときは 'ファイルでない'>)` を返す。
2. `retries = 0` で繰り返す:
   1. スレッドの接続 `conn` を用意する（下の「接続」）。使い直す接続（`conn.sock` が `None` でない）なら、`select.select([conn.sock], [], [], 0)` で読める状態かを見て、読めるなら（使っていない keep-alive の接続にサーバーが切断か想定外のデータを送った）`conn.close()` で閉じる。接続が無ければ、ロックの外で `conn.connect()` する（`TimeoutError` か `OSError` なら、この 2 の 2 の失敗と同じに扱い、4 へ）。切られた接続を要求を出す前に見つけて張り直すので、要求の数は増えない。
   2. `gate.send(lambda: conn.request('GET', path_q, headers=headers))` を呼ぶ（`path_q` は URL のパスの部分 `{_BASE_URL のパス}/{サービス名}/{z}/{x}/{y}.png`）。偽なら `None` を返す。続けてロックの外で `resp = conn.getresponse()`。送信か状態行までの読み取りで、`TimeoutError` なら失敗 `タイムアウト（{_TIMEOUT_S の整数} 秒）`、ほかの `OSError`・`http.client.HTTPException`（`RemoteDisconnected`・`IncompleteRead`・`ssl.SSLError` を含む）なら失敗 `通信の失敗: <例外のクラス名>`。どちらも、接続を `conn.close()` で閉じて捨て（次は新しく張る）、429・503 でない失敗として 4 へ（使い直した接続での失敗も同じく再試行に数える。応答を受けていなくても、要求がサーバーに届いていないとは言えないため。HLD 4.1.3 の「再試行の上限回数」）。状態行を受けた後は、`resp.status` が 200 のときだけ `body = resp.read()`（本体を全部読む。ここでの `TimeoutError`・`OSError`・`http.client.HTTPException` は、上と同じ失敗として 4 へ）。304・404 は本文を結果に使わないが、使い直す接続を空にするために `resp.read()` で読み捨てる（失敗は無視し、接続を閉じて捨てて、結果はそのまま返す）。403・429・503 など、ほかの状態は本文を使わないので読まずに接続を閉じて捨て、3 の状態ごとの扱いに進む（本文を保留する応答や途切れる応答で、すぐ止める・全ワーカーを待たせる判断が `_TIMEOUT_S` 遅れたり失われたりしない。HLD 4.1.3）。本文を読み終えたら、`resp.will_close` が真なら接続を閉じて捨てる。
   3. 応答 `s = resp.status` ごとに（HLD 4.1.2 の応答の表、HLD 4.1.3 の「再試行」）:
      - 200: `lm = _parse_http_date(resp.getheader('Last-Modified'))`。`None` なら `_Stop(why='no_last_modified', …)`。そうでなければ `save_tile(body, lm, path)`（`OSError` なら `_Stop(why='file', path=<e.filename か path>, reason=<{reason}>)`）を呼び、`'fetched'` を返す。
      - 304: `If-Modified-Since` を付けていれば `'unchanged'`、付けていなければ `_Stop(why='unexpected', …)`。
      - 404: `'missing'`。
      - 429・503: 4 へ（全ワーカーを待たせる）。
      - 500〜599 のそのほか: 4 へ（このタイルだけが待つ）。
      - 400〜499 のそのほか: `_Stop(why='immediate', …)`。
      - それ以外（リダイレクトの 3xx、200 以外の 2xx など）: `_Stop(why='unexpected', …)`（リダイレクトは追わない）。
   4. 再試行: `retries += 1`。`retries > _MAX_RETRIES` なら `_Stop(why='retry_exceeded', retries=_MAX_RETRIES, …)`。`ra = _parse_retry_after(resp.getheader('Retry-After'))`（応答が無い失敗では `None`）、`wait = _retry_wait(retries, ra)`。`wait` が `None` なら待たずに `_Stop(why='retry_after', retries=retries - 1, …)`。429・503 なら `gate.pause(wait)` して 1 に戻る（自分も `gate.send` で待つ）。そのほかの失敗なら `gate.sleep(wait)` が偽なら `None` を返し、真なら 1 に戻る。

- 接続: `_BASE_URL` を呼び出しのたびに `urllib.parse.urlsplit` で分け、`scheme` が `https` なら `http.client.HTTPSConnection(host, port, timeout=_TIMEOUT_S, context=ssl.create_default_context())`（証明書を確かめる）、`http` なら `http.client.HTTPConnection(host, port, timeout=_TIMEOUT_S)` を作る。`_TIMEOUT_S` はソケットの 1 回の操作（接続・送信・読み取り）ごとのタイムアウト（HLD 4.1.3 の「タイムアウト（接続・読み取り）30 秒」）。接続はスレッドごとに `_local`（[4.1.2](#412-型とデータ)）に持ち、応答を読み終えた後の次の要求で使い直す（keep-alive）。使い直すのは、今の `_BASE_URL` を分けた `(scheme, host, port)` が `_local.key` と同じときだけで、違えば `_close_connection()` で閉じて作り直す（UT が `_BASE_URL` を差し替えるので、前のケースの接続が残っていても、今のサーバーへ張り直す。通常の起動では `_BASE_URL` は変わらない）。`http.client` はリダイレクトを追わない（HLD 4.1.2 の応答の表の「リダイレクトは追わない」）。要求に付けるヘッダーは `User-Agent` と、キャッシュがあるときの `If-Modified-Since` だけ（`Host` などは `http.client` が付ける）。
- `last` の文（`_Stop.last`）: 応答があれば `HTTP {s}` に、`Retry-After` があれば `（Retry-After: {値}）`、3xx で `Location` があれば `（Location: {値}）`、304 で `If-Modified-Since` を付けていなければ `（If-Modified-Since を付けていない要求）`、200 で `Last-Modified` が無いか読めなければ `（Last-Modified: {値か なし}）` を続ける。応答が無ければ 2 の 2 の失敗の文（`タイムアウト（{_TIMEOUT_S の整数} 秒）`・`通信の失敗: {クラス名}`）。
- `retries` は、`_Stop` を作った時点で済ませた再試行の回数（`'retry_exceeded'` は `_MAX_RETRIES`、`'retry_after'` は打ち切った要求の前の回数、すぐ止める応答と想定外の応答と `Last-Modified` の無い応答は、それまでの回数）。

`_retry_wait(n: int, retry_after: float | None) -> float | None`（内部。`n` は 1 から数えた再試行の回数）: `exp = min(_FIRST_WAIT_S * _WAIT_FACTOR ** (n - 1), _WAIT_CAP_S)`。`retry_after` が `None` なら `exp`。`retry_after > _WAIT_CAP_S` なら `None`（待たずに打ち切る）。それ以外は `max(exp, retry_after)`（1 回の待ちの上限は指数の待ち時間にだけ掛け、`Retry-After` は短くしない。HLD 4.1.3 の「再試行」）。

`_parse_retry_after(value: str | None) -> float | None`（内部）: `None` なら `None`。前後の空白を除き、`re.fullmatch(r'[0-9]+', v)` に合えば、先頭の `0` を除いた `d = v.lstrip('0') or '0'` が 19 桁以上なら `math.inf`、それ以外は `float(int(d))`（2.1.2 の整数の種類と同じく、先頭の `0` を除いてから桁数を見る。`0000000000000000000` は 0 になる）。合わなければ `_parse_http_date(v)` が `None` でないとき `max(0.0, <その時刻> - time.time())`、`None` なら `None`（読めない値は無いものとする）。

`_parse_http_date(value: str | None) -> float | None`（内部。返すのは UNIX 時刻の秒）: `None` か空なら `None`。`email.utils.parsedate_to_datetime(value)` が `TypeError`・`ValueError`・`IndexError`・`OverflowError` なら `None`。時差の無い時刻（`-0000`）は UTC とする。`.timestamp()` を返す。

##### save_tile

`save_tile(body: bytes, last_modified: float, path: str) -> None`（ワーカーのスレッドで動く。失敗は `OSError` のまま呼ぶ側へ伝える）

1. `os.makedirs(os.path.dirname(path), exist_ok=True)`。
2. 一時ファイル `tmp = path + '.tmp'`（`{y}.png.tmp`。`.png` で終わらない。[HLD 4.1.2](30_HLD.md#412-処理の流れ) の表の後の段落、[2.3](#23-ファイルの名前と書き方)）に、2.3 の一時ファイルの決まりの「書く」の段（`open(tmp, 'wb')`・`write(body)`・`flush()`・`os.fsync`・閉じる）で `body` を書く（失敗したら一時ファイルを消してから上げる）。
3. `os.utime(tmp, (last_modified, last_modified))`。失敗したら一時ファイルを消してから（消せないときの `OSError` は無視する）上げる。
4. `os.replace(tmp, path)`。失敗したら一時ファイルを消してから上げる（前のキャッシュはそのまま残る）。

- mtime を置き換えの前に一時ファイルに付けるのは、置き換えた時点で正規のパスのファイルが `Last-Modified` の mtime を持つようにするため（`os.replace` は mtime を変えない）。一時ファイルの名前を固定にしてよいのは、2.3 の理由に加えて、同じタイルは 1 つのワーカーだけが扱うため。

#### 4.1.4 メッセージ文面

前置き: 書き方は [2.2](#22-ログとメッセージの文面)。ロックとログの場面（G1〜G7）と取得完了の記録の誤り（FC2。`{detail}` は 4.1.3 の `read_fetch_record` のとおり）は 2.2、設定の誤り（CF1〜CF7）・`--mesh` の誤り（A1〜A5）・メッシュのリストの誤り（R1〜R3）は [2.1.4](#214-メッセージ文面) の文面のまま。日本全土 1 次メッシュコードリストの R1〜R3 の案内は `None`（既定の対処）、北方領土除外メッシュリストの R1〜R3 の案内は `{cmp1}`。L1〜L3 は 2.2（`{program}` は `fetch_tiles`）。プレースホルダーの意味:

- `{path}` は `data_dir` から組み立てたパスのまま（`data_dir` は絶対パスなので、どれも絶対パス）。`{dir}` は `{path}` のディレクトリ（`os.path.dirname`）。`{reason}` は [4.1.3](#413-関数の細部) の前置きのとおり。`{option}`・`{arg}`・`{value}` は [3.1.4](#314-メッセージ文面) と同じ（`{arg}`・`{value}` は 2.2 の引用の決まりで書いたもの）。
- `{config_opt}`・`{rerun}` はモジュールの状態の `_config_opt`・`_rerun`（[4.1.2](#412-型とデータ)）。`{cmp1}` は `venv/bin/python3 scripts/preprocess_boundaries.py{config_opt} を起動して正常に終えてから、もう一度起動する`（[HLD 4.1.3](30_HLD.md#413-異常系) の「それを作る操作〈除外リストと版の記録は CMP1 の実行〉」）。
- `{kind}` は DEM 種別の名前（`DEM10b` など）、`{url}` は要求した URL、`{last}`・`{retries}` は `_Stop` の `last`・`retries`。`{tile}` は `{kind} {z}/{x}/{y}`（例 `DEM10b 14/14290/6581`）。

`ERROR:`・`WARNING:` のメッセージ（2 行目は `対処:` と空白 1 つの後）:

| 記号 | 場面 | 1 行目 | 2 行目 | 終了コード |
|---|---|---|---|---|
| TA1 | 受け付けない引数 | `fetch_tiles の知らない引数: {arg}` | `使える引数は --config・--mesh・--help（venv/bin/python3 scripts/fetch_tiles.py --help で使い方を出す）` | 2 |
| TA2 | 値が無い | `{option} の値が無い` | `{option} の後に値を書く（venv/bin/python3 scripts/fetch_tiles.py --help で使い方を出す）` | 2 |
| TA3 | 値が違う | `--config の値が違う: {value}` | `--config には空でないパスを渡す` | 2 |
| TA4 | 同じ名前を 2 回 | `{option} を 2 回渡した` | `{option} は 1 回だけ渡す` | 2 |
| TP1 | 北方領土除外タイルリストが無い | `北方領土除外タイルリストが無い: {path}` | `{cmp1}` | 1 |
| TP2 | 北方領土除外タイルリストを読めない・書式が違う | `北方領土除外タイルリストを読めないか、書式が違う: {path}: {detail}`（`{detail}` は 4.1.3 の `read_excluded_tiles` のとおり） | `{cmp1}` | 1 |
| TP3 | CMP1 の版の記録が無い | `行政区域前処理の版の記録が無い（行政区域前処理が正常に終わっていない）: {path}` | `{cmp1}` | 1 |
| TW1 | `--mesh` のコードが日本全土のリストに無い（`WARNING:`） | `--mesh のメッシュコードを飛ばした（日本全土1次メッシュコードリストに無い）: {code}` | `日本全土1次メッシュコードリスト {list_path} にあるコードを渡す（残りのメッシュは続けて取得する）`（`{list_path}` は `_JAPAN_MESH_LIST_PATH`） | 0 |
| TW2 | `--mesh` のコードが北方領土除外メッシュ（`WARNING:`） | `--mesh のメッシュコードを飛ばした（北方領土除外メッシュ）: {code}` | `北方領土除外メッシュは取得しない（隣のメッシュと共有する境目のタイルは、隣のメッシュの取得で取る）` | 0 |
| TW3 | User-Agent の版を取れない（`WARNING:`） | `User-Agent に入れる版を git から取れない: {reason}`（`{reason}` は `_software_version` の理由） | `版を unknown にして取得を続ける。ソースツリーが git の作業ツリーで、git のコマンドを使えるかを確かめる` | 0 |
| TG1 | 再試行の上限超過・すぐ止める応答・想定外の応答・`Retry-After` が上限を超えた | `標高タイルの取得を止めた（{why}）: {tile}（{url}）: 最後の応答 {last}、再試行 {retries} 回`（`{why}` は `_Stop.why` が `'retry_exceeded'` なら `再試行の上限を超えた`、`'retry_after'` なら `Retry-After が 1 回の待ちの上限の 900 秒を超えた`〈900 は `_WAIT_CAP_S` の整数〉、`'immediate'` なら `再試行しない応答`、`'unexpected'` なら `想定外の応答`） | `時間をおいて {rerun} を起動し直す（取得済みのタイルは残っていて、起動し直すと If-Modified-Since で更新のあったタイルだけを取り直す）` | 1 |
| TG2 | HTTP 200 に `Last-Modified` が無いか読めない | `HTTP 200 の応答に Last-Modified が無いか読めない: {tile}（{url}）: {last}` | `提供元の更新日を得られないので取得を止めた。時間をおいて {rerun} を起動し直し、続くなら提供元の応答の変化を確かめる（開発者に知らせる）` | 1 |
| TD1 | 取得範囲の DEM10b がすべて未整備のメッシュがある | `取得範囲の DEM10b のタイルがすべて未整備（HTTP 404）のメッシュがある: {meshes}`（`{meshes}` は控えたメッシュを昇順に `{mesh}（{n} 枚）` にして `、` でつないだもの。`{n}` はそのメッシュの範囲で要求した DEM10b のタイルの数） | `取得の誤りが疑われる。時間をおいて {rerun} を起動し直し、続けて 404 になるなら提供元の状態を確かめる` | 1 |
| TF1 | 取得完了の記録を書けない | `取得完了の記録を書けない: {path}: {reason}` | `ディスクの空きと {dir} の権限を確かめてから {rerun} を起動し直す（記録はこの書き換えの前の内容のまま）` | 1 |
| TF2 | タイルのキャッシュを読み書きできない | `標高タイルのキャッシュを読み書きできない: {path}: {reason}` | `ディスクの空きと {dir} の権限を確かめてから {rerun} を起動し直す` | 1 |
| TF3 | タイルのキャッシュを消せない | `標高タイルのキャッシュを消せない: {path}: {reason}` | TF2 と同じ | 1 |

TF1 の「この書き換え」は、2 つの場面のどちらかを指す。対象のメッシュを記録から外す書き換え（`remove_from_record`）で止まったときは、記録もキャッシュも起動の前のまま。最後の書き換え（`main` の 9）で止まったときは、記録は対象を外した後のままで、取得したタイルは残る。どちらも、起動し直して正常に終えれば記録に戻る。

通常のログに出す行（`common.log_info` で標準出力とログファイルに出す）:

| 記号 | 行 | 文面 |
|---|---|---|
| TL1 | 対象のメッシュ | `対象のメッシュ {n} 件: {codes}`（`{codes}` は昇順に空白 1 つでつないだもの。0 件なら `対象のメッシュ 0 件`） |
| TL2 | User-Agent | `User-Agent: {user_agent}` |
| TL3 | 途中経過 | 2.2 の「通常のログの共通の形」の途中経過の形（`{what}` は `_run_pool` の `what`〈`DEM10b のタイル` か `DEM5 の位置`〉。[HLD 5.7.2](30_HLD.md#572-処理の流れ) の 5「途中経過」） |
| TL4 | 結果の要約（取得を終えた） | 1 行目 `結果の要約: タイルの取得を終えた（取得完了の記録はこの後に書く）。対象のメッシュ {n} 件`、続けて `_KIND_ORDER` の順に `{kind}: 取得 {a}、変更なし {b}、未整備 {c}、削除 {d}`（`_tally` の値）の 4 行、`海として DEM5 を要求しなかった位置: {sea}`、対象のメッシュごとに昇順に `海の位置: {mesh} 判定対象 {judged}、海 {sea_n}、割合 {ratio}`（`{ratio}` は `f'{sea_n * 100 / judged:.1f}%'`、`judged` が 0 なら `-`）。1 回の `log_info` に改行でつないで渡す |
| TL5 | 結果の要約（対象が 0 件） | 1 行目 `結果の要約: 対象のメッシュが 0 件なので取得しなかった（取得完了の記録は変えていない）`、続けて TL4 と同じ種別ごとの 4 行（削除のほかは 0） |
| TL6 | 結果の要約（途中で止まった） | 1 行目 `結果の要約: 途中で止まった（{stage}）。終えた分:`（`{stage}` は `_stage`）、続けて TL4 と同じ種別ごとの 4 行。`removed` が真なら最後に `今回の対象のメッシュは取得完了の記録から外したまま（起動し直して正常に終えると記録に戻る）` |

使い方の文（`--help`。標準出力に、次の行をこのまま出す。最後の行の後にも LF を付ける）:

```text
使い方: venv/bin/python3 scripts/fetch_tiles.py [--config <パス>] [--mesh <メッシュコードかファイル>]
       venv/bin/python3 scripts/fetch_tiles.py --help

国土地理院のタイルサーバーから標高タイル（DEM10b と DEM5a〜5c）を取得してキャッシュに置き、取得を終えたメッシュを取得完了の記録に残す。

  --config <パス>  設定ファイル（省くとソースツリーの params/config.ini）
  --mesh <値>      取得するメッシュ。4 桁のメッシュコードか、1 行 1 件で書いたファイルのパス（省くと日本全土）
  --help           この使い方を出して終わる
```

- TL4 の中身の正本は [HLD 4.1.2](30_HLD.md#412-処理の流れ) の 8「件数と海の位置を要約して出す」（HLD 5.7.2 の「結果の要約の中身」の `fetch_tiles` の行）。削除は 6 と HTTP 404 と 7 の 5 で消した数の和（`_tally` の `削除`）。

#### 4.1.5 UT 候補

前置き: すべて自動。共通の準備は次の 4 つ。止まるケースの期待の「メッセージ」は、標準エラー出力の行の文面（[2.2](#22-ログとメッセージの文面)・[2.1.4](#214-メッセージ文面)・[4.1.4](#414-メッセージ文面) の文面に値を入れたもの）。ログファイルの行の期待は、先頭の時刻と空白を除いた文面。時刻を照らすケースの許容差は、各ケースの期待に書いた値を正とする（試験の計算機の遅れを見込んで、待ち時間より少し短い値と比べる）。

- **同じプロセス**: テストのプロセスの中で `scripts/` を import の探索先に入れて `import fetch_tiles` し、関数を直接呼ぶ（`start_log` を呼ばない。`log_info` などは画面にだけ出る）。止まるケースは `SystemExit` を捕まえて終了コードを読み、標準出力と標準エラー出力は `contextlib.redirect_stdout`・`redirect_stderr` で捕まえる。一時のディレクトリ `<tmp>` をケースごとに作る。各ケースの前に `fetch_tiles._tally` を `_KIND_ORDER` の各種別の `{'取得': 0, '変更なし': 0, '未整備': 0, '削除': 0}` に、`_config_opt` を空の文字列に、`_rerun` を `venv/bin/python3 scripts/fetch_tiles.py` に、`_gate` を `None` にする。1 つのケースの中で (a)(b) と分けた入力を続けて呼ぶときは、(a)(b) のそれぞれの前にも、`_tally` と `_gate` をこの値に戻す（`_gate` は最初の `_run_pool` の `interval_ms` で作られ、戻さないと 2 つ目以降の入力の `interval_ms` が使われない）。1 つのケースの中で (a)(b)… と分けた独立な入力を続けて呼ぶときは、入力が作ったファイルとディレクトリ（`.tmp` に置いたディレクトリなど）と、入力のために差し替えた定数と関数も、次の入力の前に戻す（前の入力の状態を引き継ぐのは、そう書いたケースだけ）。差し替えた定数と関数は、ケースの後に元に戻す。ケースの後に、テストを動かすスレッドの接続を `fetch_tiles._close_connection()` で閉じる（ワーカーのスレッドの接続は、ワーカーが終わるときに閉じる）。待ちを照らすケースは `_FIRST_WAIT_S = 0.05`、`_WAIT_CAP_S = 0.4`、`_TIMEOUT_S = 0.5` に差し替える（ケースが別に書けばその値）。`fetch_one_tile` を直接呼ぶケースは `_Gate(0)` を渡す。
- **模擬サーバー**: `http.server.ThreadingHTTPServer(('127.0.0.1', 0), <ハンドラ>)` をテストのプロセスのスレッドで動かし、`fetch_tiles._BASE_URL` を `http://127.0.0.1:<ポート>/xyz` にする。ハンドラは、パス（`/xyz/dem_png/14/100/200.png` の形）ごとに応答の台本（応答の並び。並びの最後の応答を、それより後の要求にも使う）を引き、台本の無いパスには `Last-Modified: Wed, 21 Oct 2015 07:28:00 GMT`（UNIX 時刻 1445412480）と本体 `PNG` の 200 を返す。応答には `status`（既定 200）、`headers`、`body`（既定 `PNG`）、`delay`（返す前に待つ秒）、`wait_for`（返す前に、そのパスの要求を受けるまで待つ。5 秒まで）、`hold`（返す前に、テストが `set` する `threading.Event` を待つ）、`close`（応答を返さずに接続を切る）、`body_hold`（ヘッダーを送った後、本文を送らずに待つ秒。待った後に接続を切る）を書ける。台本の応答も、`status` が 200 で `headers` に `Last-Modified` を書かなければ、台本の無いパスと同じ `Last-Modified` を付ける。`Last-Modified` を付けない 200 は、`headers` に `Last-Modified` を `None` と書いて表す。受けた要求ごとに、パス・`User-Agent`・`If-Modified-Since`（無ければ `None`）・クライアントのポート（`self.client_address[1]`）・受けた時刻・返し終えた時刻（どちらも `time.monotonic()`。切ったときは切った時刻）を記録する。`Content-Length` を付ける。ハンドラの `protocol_version` は `'HTTP/1.1'` にする（既定の HTTP/1.0 では応答のたびに接続が切られ、`fetch_one_tile` の接続の使い直しを通らないため）。
- **小さな範囲**: `fetch_tiles.mesh_tile_range` を、次の表を引く関数に差し替える（実物の範囲はタイルが多いので）。日本全土 1 次メッシュコードリストは `5339`・`5340`・`6848`、北方領土除外メッシュは `6848`、北方領土除外タイルは `(207, 403)`・`(209, 403)`（DEM10b にすると `(103, 201)`・`(104, 201)`）。

  | メッシュ | ズーム 14 の範囲（x_min, x_max, y_min, y_max） | ズーム 15 の範囲 | 役 |
  |---|---|---|---|
  | `5339` | (100, 101, 200, 201) | (200, 203, 400, 403) | A |
  | `5340` | (102, 103, 200, 201) | (204, 207, 400, 403) | B（`(207, 403)` が北方領土除外） |
  | `6848` | (103, 104, 200, 201) | (206, 209, 400, 403) | 北方領土除外メッシュ（B と x = 103・206・207 の列を共有する） |
  | `5439` | (110, 114, 210, 214) | (220, 229, 420, 429) | 海の位置を見るメッシュ |
  | `5341` | (103, 103, 201, 201) | (206, 207, 402, 403) | DEM10b の範囲がすべて北方領土除外のメッシュ |

- **子のプロセス**: 一時のソースツリー `<tmp>/src` を作り、`<tmp>/src/scripts/` にテストする `scripts/fetch_tiles.py` と `scripts/common.py` を写し、`<tmp>/src/params/mesh_list_japan.txt` に `5339\n5340\n6848\n` を書く。一時の設定 `<tmp>/c.ini` に `[paths]` の `data_dir = <tmp>/data`・`log_dir = <tmp>/logs` と、`[fetch]` の `user_agent_email = test@example.com`・`max_parallel = 2`・`interval_ms = 0` を書く。`<tmp>/data/boundaries/` に `nt_excluded_tiles.txt`（`207 403\n209 403\n`）・`nt_excluded_meshes.txt`（`6848\n`）・`n03_version.txt`（`20250101\n`）を置く。`<tmp>/work` を作る。起動は `subprocess.run([sys.executable, '-c', <試験用の短いプログラム>], cwd='<tmp>/work', capture_output=True, timeout=60)`（シグナルのケースは `subprocess.Popen`）。試験用のプログラムは、`<tmp>/src/scripts` を `sys.path` の先頭に入れて `import fetch_tiles` し、`_BASE_URL` を模擬サーバーの URL に、`_FIRST_WAIT_S`・`_WAIT_CAP_S`・`_TIMEOUT_S` を `0.05`・`0.4`・`1.0` に、`mesh_tile_range` を小さな範囲の関数に、`_software_version` を `('v0-test', None)` を返す関数に差し替えてから、`sys.argv = ['fetch_tiles.py', *<引数>]` にして `fetch_tiles.main()` を呼ぶ（引数は、ケースの「入力」の欄に書いた引数の前に、いつも `--config ../c.ini` を付ける。ケースが `--config` を書いたときだけ、それに従う）。User-Agent は `findsummits/v0-test (mailto:test@example.com)` になる。

| ID | 確かめること | 準備 | 入力 | 期待 |
|---|---|---|---|---|
| `UT-fetch_tiles-01` | 引数の正しい形 | 同じプロセス | `_parse_args` に (a) `[]`、(b) `['--config', 'a.ini']`、(c) `['--config=a=b.ini', '--mesh', '5339']`、(d) `['--mesh', '--help']`、(e) `['--mesh=-x', '--config', 'c']` | (a) `_Args(None, None)`、(b) `_Args('a.ini', None)`、(c) `_Args('a=b.ini', '5339')`、(d) `_Args(None, '--help')`、(e) `_Args('c', '-x')` |
| `UT-fetch_tiles-02` | 引数の誤り | 同じプロセス | `_parse_args` に (a) `['foo']`、(b) `['--foo']`、(c) `['--help=x']`、(d) `['--']`、(e) `['--me', '5339']`、(f) `['--mesh']`、(g) `['--config', '']`、(h) `['--config=']`、(i) `['--mesh', '5339', '--mesh', '5340']`、(j) `['--config', 'a', '--config']` | どれも 2、標準出力は空。(a)〜(e) は TA1（(a) の 1 行目は `ERROR: fetch_tiles の知らない引数: foo`、(c) の引数は `--help=x`、(e) の引数は `--me`）、(f) は TA2（`--mesh の値が無い`）、(g)(h) は TA3（`ERROR: --config の値が違う: ''`）、(i) は TA4（`--mesh を 2 回渡した`）、(j) は TA4（`--config を 2 回渡した`。TA2 でない） |
| `UT-fetch_tiles-03` | `--help` | 子のプロセス | 引数を (a) `--mesh 5339 --help --foo`、(b) `--foo --help`、(c) `--config '' --help`（`--config` の値は空の文字列） | (a)(c) は 0、標準出力は [4.1.4](#414-メッセージ文面) の使い方の文と等しい、標準エラー出力は空、`<tmp>/data/findsummits.lock` と `<tmp>/logs` が無い、模擬サーバーは要求を受けない。(b) は 2、TA1（`--foo`）、標準出力は空 |
| `UT-fetch_tiles-04` | 待ち時間の計算 | 同じプロセス（定数は差し替えない） | `_retry_wait(n, ra)` に (n, ra) を (1, None)、(2, None)、(3, None)、(4, None)、(5, None)、(6, None)、(1, 1.0)、(1, 120.0)、(5, 0.0)、(2, 900.0)、(1, 900.5) | 順に `60.0`、`120.0`、`240.0`、`480.0`、`900.0`、`900.0`、`60.0`、`120.0`、`900.0`、`900.0`、`None` |
| `UT-fetch_tiles-05` | `Retry-After` の読み方 | 同じプロセス | `_parse_retry_after` に (a) `None`、(b) `'120'`、(c) `' 7 '`、(d) `'1.5'`、(e) `'abc'`、(f) `'9'` を 19 字、(g) `email.utils.formatdate(time.time() + 100, usegmt=True)`、(h) `'Wed, 21 Oct 2015 07:28:00 GMT'`、(i) `'0'` を 19 字、(j) `'0'` を 19 字の後に `'900'` | (a) `None`、(b) `120.0`、(c) `7.0`、(d)(e) `None`、(f) `math.inf`、(g) 98 以上 101 以下、(h) `0.0`、(i) `0.0`、(j) `900.0`（先頭の `0` を除いてから桁数を見る） |
| `UT-fetch_tiles-06` | HTTP の日付の読み方 | 同じプロセス | `_parse_http_date` に (a) `'Wed, 21 Oct 2015 07:28:00 GMT'`、(b) `'Wed, 21 Oct 2015 07:28:00 -0000'`、(c) `'garbage'`、(d) `''`、(e) `None`、(f) `'Wed, 32 Oct 2015 07:28:00 GMT'` | (a)(b) `1445412480.0`、(c)〜(f) `None` |
| `UT-fetch_tiles-07` | 取得範囲（2.4 の表 4） | 同じプロセス | `mesh_tile_range` に [2.4](#24-言語ごとに別に実装する式のテストベクトル) の表 4 の 6 行のメッシュと z | 各行の `(x_min, x_max, y_min, y_max)` と等しい |
| `UT-fetch_tiles-08` | 北方領土除外タイルリストを読む | 同じプロセス | `read_excluded_tiles` に、中身が (a) `207 403\n209 403\n`、(b) 空、(c) `1 2`（最後の改行なし）、(d) `1  2\n`、(e) `1 2\n\n`、(f) `1 2\r\n`、(g) `32768 1\n`、(h) `x y\n` のファイル、(i) 無いパス、(j) ディレクトリ | (a) `{(207, 403), (209, 403)}`、(b) 空の集合、(c) `{(1, 2)}`。(d)〜(j) は 1。(d)(f)(g)(h) は TP2（`{detail}` は `1 行目が「x y」の形でない: <行>`）、(e) は TP2（`{detail}` は `2 行目が「x y」の形でない:` の後に空白 1 つだけ。行は空）、(i) は TP1、(j) は TP2（`{detail}` は `Is a directory`）。TP1〜TP2 の 2 行目は `venv/bin/python3 scripts/preprocess_boundaries.py を起動して正常に終えてから、もう一度起動する` |
| `UT-fetch_tiles-09` | CMP1 の版の記録の有無 | 同じプロセス。`<tmp>/b/` を作る | `check_c1_version_record('<tmp>/b')` に、`<tmp>/b/n03_version.txt` を (a) `20250101\n`、(b) 空のファイル、(c) 置かない、(d) ディレクトリにする | (a)(b) は止まらない（標準エラー出力は空）。(c)(d) は 1、TP3（`{path}` は `<tmp>/b/n03_version.txt`） |
| `UT-fetch_tiles-10` | 取得完了の記録を読む | 同じプロセス | `read_fetch_record` に、(a) 無いパス、中身が (b) 空、(c) `5339\n5340`、(d) `5339\n5339\n`、(e) `5339\n\n`、(f) `52a9\n`、(g) `EF BB BF` と `5339\n` のファイル、(h) ディレクトリ | (a)(b) 空の集合、(c) `{'5339', '5340'}`、(d) `{'5339'}`。(e)〜(h) は 1、FC2。`{detail}` は (e) `2 行目が 4 桁の数字でない:` の後に空白 1 つだけ、(f) `1 行目が 4 桁の数字でない: 52a9`、(g) `1 行目が 4 桁の数字でない:` で始まる、(h) `Is a directory`。2 行目は `<パス> を消してから、venv/bin/python3 scripts/fetch_tiles.py を --mesh なしで起動し直す（--mesh を付けると、記録はそのメッシュだけになる）` |
| `UT-fetch_tiles-11` | 対象のメッシュを決める | 同じプロセス | `select_fetch_meshes(m, {'5339', '5340', '6848'}, {'6848'})` の `m` を (a) `None`、(b) `{'5339', '9999', '6848'}`、(c) `{'6848'}` | (a) `{'5339', '5340'}`、標準エラー出力は空。(b) `{'5339'}`、標準エラー出力は TW2（`WARNING: --mesh のメッシュコードを飛ばした（北方領土除外メッシュ）: 6848`）の 2 行の後に TW1（`…（日本全土1次メッシュコードリストに無い）: 9999`）の 2 行。(c) 空の集合、TW2 の 2 行 |
| `UT-fetch_tiles-12` | 取得するタイルの集合 | 同じプロセス。小さな範囲 | `list_fetch_tiles({'5339', '5340'}, {(207, 403), (209, 403)})` | DEM10b は `(100, 200)`・`(100, 201)`・`(101, 200)`・`(101, 201)`・`(102, 200)`・`(102, 201)`・`(103, 200)` の 7 枚（`(103, 201)` が除かれる）。ズーム 15 の位置の集合は、x = 200〜207・y = 400〜403 のすべての組（32）から `(207, 403)` を除いた 31 の集合と等しい |
| `UT-fetch_tiles-13` | 古いキャッシュのタイル | 同じプロセス。小さな範囲 | `list_stale_tiles({'5339', '5340', '6848'}, {'6848'}, {(207, 403), (209, 403)})` | `DEM10b` は `{(103, 201), (104, 200), (104, 201)}`。`DEM5a`・`DEM5b`・`DEM5c` はどれも、x = 208・209 と y = 400〜403 の 8 つに `(207, 403)` を足した 9 つ（x = 206・207 の列は B の範囲に入るので、除外メッシュの取得範囲から除かれる。`(207, 403)` は北方領土除外タイルとして入る） |
| `UT-fetch_tiles-14` | 記録から対象を外す | 同じプロセス。`<tmp>/data/tiles/` を作る | `remove_from_record('<tmp>/data/tiles/fetch_complete.txt', record, {'5339'}, given)` を (a) `record = {'5339', '5340'}`・`given = True`、(b) 同じ `record`・`given = False`、(c) 記録のファイルを置かず `record = set()`・`given = True`、(d) 記録 `5339\n5340\n` を置き、`fetch_tiles` の中の `os.replace` を `OSError(errno.EACCES, os.strerror(errno.EACCES))` を上げる物に差し替えてから (a) と同じく | (a) 返り値 `{'5340'}`、ファイルは `5340\n`。(b) 返り値は空の集合、ファイルは空。(c) 返り値は空の集合、空のファイルができる。(d) 1、TF1（2 行目は `ディスクの空きと <tmp>/data/tiles の権限を確かめてから venv/bin/python3 scripts/fetch_tiles.py を起動し直す（記録はこの書き換えの前の内容のまま）`）、記録は `5339\n5340\n` のまま。どれも `fetch_complete.txt.tmp` が残らない |
| `UT-fetch_tiles-15` | 記録を書く | 同じプロセス | `write_fetch_record('<tmp>/data/tiles/fetch_complete.txt', codes)` を (a) `<tmp>/data/tiles/` を作らずに `{'5340', '5339'}`、(b) `set()`、(c) `fetch_complete.txt.tmp` をディレクトリにしてから `{'5339'}`、(d) 記録 `5339\n` を置き、`fetch_tiles` の中の `os.replace` を `OSError(errno.EACCES, os.strerror(errno.EACCES))` を上げる物に差し替えてから `{'5340'}`、(e) 記録 `5339\n` を置き、`fetch_tiles` の中の `os.fsync` を `OSError(errno.EIO, os.strerror(errno.EIO))` を上げる物に差し替えてから `{'5340'}` | (a) `tiles/` ができ、ファイルは `5339\n5340\n`。(b) 空のファイル。(c) 1、TF1（`{path}` は `<tmp>/data/tiles/fetch_complete.txt.tmp`）。(d) 1、TF1（`{path}` は記録のパス、`{reason}` は `Permission denied`）、記録は `5339\n` のまま、`.tmp` は残らない。(e) 1、TF1（`{path}` は `<tmp>/data/tiles/fetch_complete.txt.tmp`、`{reason}` は `Input/output error`）、記録は `5339\n` のまま、`.tmp` は残らない。(a)(b) も `.tmp` は残らない |
| `UT-fetch_tiles-16` | キャッシュを消す | 同じプロセス。`<tiles>` = `<tmp>/tiles` に DEM10b の `(100, 200)` と DEM5a の `(200, 400)` のキャッシュを置く | (a) `delete_cached_tiles({'DEM10b': {(100, 200), (101, 200)}, 'DEM5a': {(200, 400)}}, '<tiles>')`、(b) DEM5b の `(200, 400)` のパスをディレクトリにしてから `delete_cached_tiles({'DEM5b': {(200, 400)}}, '<tiles>')` | (a) 返り値は `{'DEM10b': 1, 'DEM5a': 1, 'DEM5b': 0, 'DEM5c': 0}`、2 つのファイルが無い、`_tally` の `削除` が DEM10b と DEM5a で 1。(b) 1、TF3（`{path}` は `<tiles>/dem5b_png/15/200/400.png`） |
| `UT-fetch_tiles-17` | タイルを置く | 同じプロセス | (a) `save_tile(b'abc', 1445412480.0, '<tmp>/t/dem_png/14/1/2.png')`（ディレクトリは無い）、(b) 中身 `old` のファイルがあるパスに同じく、(c) 中身 `old` のファイルがあるパスで、`fetch_tiles` の中の `os.fsync` を `OSError(errno.EIO, os.strerror(errno.EIO))` を上げる物に差し替えて呼ぶ、(d) 同じく `os.replace` を `OSError(errno.EACCES, …)` を上げる物に差し替えて呼ぶ | (a)(b) ファイルの中身は `abc`、mtime は 1445412480、`2.png.tmp` が無い。(c)(d) `OSError` が上がる、ファイルは `old` のまま、`.tmp` が無い |
| `UT-fetch_tiles-18` | User-Agent と版 | 同じプロセス | (a) `_software_version` を `('v1.2.3', None)` を返す物に差し替えて `build_user_agent('a@b')`、(b) `('unknown', 'git が無い')` を返す物に差し替えて同じく、(c) `fetch_tiles` の中の `subprocess.run` を、(i) `FileNotFoundError` を上げる、(ii) 終了コード 128 を返す、(iii) 標準出力 `v1 2\n` を返す、(iv) 標準出力 `v1.2.3-4-gabcdef0-dirty\n` を返す物に差し替えて `_software_version()` | (a) `'findsummits/v1.2.3 (mailto:a@b)'`、標準エラー出力は空。(b) `'findsummits/unknown (mailto:a@b)'`、標準エラー出力に TW3（`WARNING: User-Agent に入れる版を git から取れない: git が無い`）。(c) (i) `('unknown', 'git が無い')`、(ii) `('unknown', 'git describe の終了コード 128')`、(iii) `('unknown', 'git describe の出力が版の形でない')`、(iv) `('v1.2.3-4-gabcdef0-dirty', None)`。(c) は `git` に `-C <ソースツリーの根> describe --tags --dirty --always` を渡す |
| `UT-fetch_tiles-19` | HTTP 200 で置く | 同じプロセス。模擬サーバー | `fetch_one_tile('DEM10b', (100, 200), _cache_path('<tmp>/tiles', 'DEM10b', (100, 200)), 'UA/1', _Gate(0))` | `'fetched'`。`<tmp>/tiles/dem_png/14/100/200.png` の中身は `PNG`、mtime は 1445412480。模擬サーバーは `/xyz/dem_png/14/100/200.png` の要求を 1 回受け、`User-Agent` は `UA/1`、`If-Modified-Since` は無い |
| `UT-fetch_tiles-20` | HTTP 304 | 同じプロセス。模擬サーバーは `(100, 200)` に 304。キャッシュに中身 `old`・mtime 1445412480 のファイルを置く | 19 と同じ | `'unchanged'`。要求の `If-Modified-Since` は `Wed, 21 Oct 2015 07:28:00 GMT`。ファイルの中身と mtime は変わらない |
| `UT-fetch_tiles-21` | HTTP 404 | 同じプロセス。模擬サーバーは `(100, 200)` に 404。キャッシュに中身 `old` のファイルを置く | 19 と同じ | `'missing'`。キャッシュのファイルは残る（`fetch_one_tile` は消さない） |
| `UT-fetch_tiles-22` | すぐ止める応答 | 同じプロセス。模擬サーバー | 19 と同じ呼び方で、模擬サーバーが `(100, 200)` に (a) 403、(b) `Location: /xyz/x.png` の 301、(c) 206、(d) 304（キャッシュなし）、(e) `Last-Modified` の無い 200（キャッシュに中身 `old`・mtime 1000000000 のファイルを置く）、(f) `Last-Modified: garbage` の 200、(g) キャッシュのパスをディレクトリにする | どれも `_Stop`。`why`・`last`・`retries` は (a) `immediate`・`HTTP 403`・0、(b) `unexpected`・`HTTP 301（Location: /xyz/x.png）`・0（`/xyz/x.png` の要求は無い）、(c) `unexpected`・`HTTP 206`・0、(d) `unexpected`・`HTTP 304（If-Modified-Since を付けていない要求）`・0、(e) `no_last_modified`・`HTTP 200（Last-Modified: なし）`・0（キャッシュの中身は `old`、mtime は 1000000000 のまま）、(f) `no_last_modified`・`HTTP 200（Last-Modified: garbage）`・0。(a)〜(f) の要求は 1 回。(g) `why` は `file`、`reason` は `ファイルでない`、要求は 0 回 |
| `UT-fetch_tiles-23` | 再試行 | 同じプロセス。模擬サーバー。待ちの定数を差し替える | 19 と同じ呼び方で、`(100, 200)` の台本を (a) 503 を 6 回、(b) 502・200、(c) `delay` 1.0 の 200・200、(d) `close`・200、(e) 500 を 6 回、(f) 403 を送り、ヘッダーの後に本文を `body_hold` 2.0 秒止める（`_TIMEOUT_S` の 0.5 秒より長い）、(g) 429（`Retry-After: 1`）を同じく本文を止める、(h) 200 を同じく本文の途中で切る・200 | (a) `_Stop`（`retry_exceeded`・`HTTP 503`・5）、要求は 6 回で、k 回目を返し終えてから k + 1 回目を受けるまでが、順に 0.05・0.1・0.2・0.4・0.4 秒から 0.02 を引いた値以上。(b)(c)(d) `'fetched'`、要求は 2 回（(c) の 1 回目は 0.5 秒でタイムアウト）。(e) `_Stop`（`retry_exceeded`・`HTTP 500`・5）。(f) `_Stop`（`immediate`・`HTTP 403`・0）、要求は 1 回、呼んでから 0.3 秒より前に返る（本文を待たない）。(g) `_Stop`（`retry_after`・`HTTP 429（Retry-After: 1）`・0）、要求は 1 回、呼んでから 0.3 秒より前に返る。(h) `'fetched'`、要求は 2 回（本文の途中で切れた 200 は、失敗として再試行する） |
| `UT-fetch_tiles-24` | `Retry-After` | 同じプロセス。模擬サーバー。待ちの定数を差し替える | 19 と同じ呼び方で、`(100, 200)` の台本を (a) `Retry-After: 1` の 429（1 は差し替えた `_WAIT_CAP_S` の 0.4 より大きい）、(b) `Retry-After: 0` の 503・200 | (a) `_Stop`（`retry_after`・`HTTP 429（Retry-After: 1）`・0）、要求は 1 回、呼んでから 0.3 秒より前に返る（待たない）。(b) `'fetched'`、2 回目の要求を受けたのは 1 回目を返し終えてから 0.03 秒以上後（指数の待ち時間 0.05 と 0 の長い方） |
| `UT-fetch_tiles-25` | 間隔と全体の待ちと止め方 | 同じプロセス。`do_send` は、呼ばれた時刻（`time.monotonic()`）を並びに足す関数 | (a) `_Gate(100)` で、2 つのスレッドがそれぞれ `send(do_send)` を 2 回呼ぶ、(b) `_Gate(0)` で `pause(0.3)` の直後に別のスレッドが `send(do_send)`、(c) `_Gate(0)` で `pause(10)` の後に別のスレッドが `send(do_send)` を呼び、0.1 秒後に `stop()`、続けて `sleep(10)`、(d) `_Gate(0)` で、スレッド A が、`threading.Event` を待ってから時刻を足す `do_send` で `send` を呼び、A が `do_send` に入ったら（もう 1 つの `Event` で知らせる）、メインのスレッドが、0.2 秒後に A の `Event` を `set` するタイマー（`threading.Timer`）を起動してから `pause(0.5)` を呼び、それが返った時刻を控える（`pause` は A の `do_send` が終わるまで返らないので、`set` を `pause` が返った後にしない。`pause` が 5 秒たっても返らなければ失敗とする）、(e) (d) と同じく A が `do_send` の中で止まっているあいだに、メインのスレッドが同じタイマーを起動してから `stop()` を呼び、返った後に別のスレッド B が `send(do_send)` | (a) 4 回とも真を返し、`do_send` が呼ばれた時刻を並べた差がどれも 0.09 秒以上。(b) 真を返し、`do_send` は `pause` から 0.28 秒以上後に呼ばれる。(c) `send` は `stop()` から 0.3 秒より前に偽を返し、`do_send` は呼ばれない。`sleep(10)` はすぐ偽を返す。(d) `pause(0.5)` が返ったのは A の `do_send` が終わった後（`set` から後。判定と送信が同じロックの中なので、送信の途中に全体の待ちが割り込まない）。(e) `stop()` が返ったのは A の `do_send` が終わった後で、B の `send` は `do_send` を呼ばずに偽を返す |
| `UT-fetch_tiles-26` | 429 の待ちのあいだ全ワーカーが要求を出さない | 同じプロセス。模擬サーバー。小さな範囲の A の DEM10b の 4 枚。`_FIRST_WAIT_S` を 0.5 に、`_WAIT_CAP_S` を 1.0 に差し替える（待ちは `min(0.5, 1.0)` の 0.5 秒）。台本は `(100, 200)` が `wait_for` `(100, 201)` の 429・200、`(100, 201)` が `delay` 0.3 の 200 | `download_tiles(<A の 4 枚>, '<tmp>/tiles', 2, 0, 'UA/1')` | 返り値の数は `取得` 4・`変更なし` 0・`未整備` 0、404 の集合は空。429 を返し終えた時刻 t から t + 0.45 秒までに受けた要求は無い。`(100, 200)` の 2 回目を受けたのは t + 0.45 秒以後 |
| `UT-fetch_tiles-27` | 数と 404 の集合と途中経過 | 同じプロセス。模擬サーバー。A の DEM10b の 4 枚。台本は `(100, 201)` が 304、`(101, 200)`・`(101, 201)` が 404。`(100, 201)` と `(101, 201)` のキャッシュを置く | `download_tiles(<A の 4 枚>, '<tmp>/tiles', 2, 0, 'UA/1')` | 返り値は（`{'取得': 1, '変更なし': 1, '未整備': 2}`, `{(101, 200), (101, 201)}`）。`(101, 201)` のキャッシュは残る。標準出力は `途中経過: DEM10b のタイル 1/4（25%）`・`2/4（50%）`・`3/4（75%）`・`4/4（100%）` の 4 行（2 行目からは `途中経過: DEM10b のタイル` と空白 1 つの後の部分を書いた）。`_tally['DEM10b']` は `取得` 1・`変更なし` 1・`未整備` 2 |
| `UT-fetch_tiles-28` | 止めるときは実行中の要求を待つ | 同じプロセス。模擬サーバー。A の DEM10b の 4 枚。`_TIMEOUT_S` を 2.0 に差し替える（応答の遅れ 0.5 秒でタイムアウトにならないように）。台本は `(100, 200)` が `delay` 0.5 の 200、`(100, 201)` が `wait_for` `(100, 200)` の 403 | `download_tiles(<A の 4 枚>, '<tmp>/tiles', 2, 0, 'UA/1')` | 1、TG1（`ERROR: 標高タイルの取得を止めた（再試行しない応答）: DEM10b 14/100/201（<URL>）: 最後の応答 HTTP 403、再試行 0 回`）。`SystemExit` を捕まえた時刻は `(100, 200)` を返し終えた時刻より後。`(100, 200)` のキャッシュの中身は `PNG`、mtime は 1445412480。`(101, 200)`・`(101, 201)` の要求は無い。`<tmp>/tiles` の下に `.tmp` で終わるファイルは無い |
| `UT-fetch_tiles-29` | 最大並列数とリクエスト間隔 | 同じプロセス。模擬サーバー。A と B の DEM10b の 8 枚（北方領土除外を除かない） | (a) 各タイルの台本を `delay` 0.2 の 200 にして `download_tiles(<8 枚>, '<tmp>/tiles', 2, 0, 'UA/1')`、(b) 遅れなしで、(a) の後に `_gate` を `None` に戻してから `download_tiles(<8 枚>, '<tmp>/tiles', 4, 100, 'UA/1')` | (a) 模擬サーバーの記録で、同時に応答中の要求の数の最大がちょうど 2。(b) 受けた時刻を並べた差がどれも 0.09 秒以上 |
| `UT-fetch_tiles-30` | ワーカーのファイルの失敗はメインで止まる | 同じプロセス。模擬サーバー。`<tmp>/tiles/dem_png/14/100` を通常のファイルにする | `download_tiles({(100, 200)}, '<tmp>/tiles', 2, 0, 'UA/1')` | 1、TF2（`{path}` は `<tmp>/tiles/dem_png/14/100/200.png`、`{reason}` は `Not a directory`）。模擬サーバーは要求を受けない |
| `UT-fetch_tiles-31` | DEM10b がすべて 404 のメッシュ | 同じプロセス。小さな範囲 | (a) `check_dem10b_meshes({'5339', '5340'}, <UT-12 の DEM10b の 7 枚>, <A の 4 枚>, '<tmp>/tiles')`（A の 4 枚のキャッシュを置く）、(b) 404 の集合を `{(100, 200), (103, 200)}` にして同じく（その 2 枚と `(101, 200)` のキャッシュを置く）、(c) `check_dem10b_meshes({'5340', '5341'}, <list_fetch_tiles({'5340', '5341'}, 北方領土除外タイル) の DEM10b>, set(), '<tmp>/tiles')`、(d) (c) の 404 の集合を B の DEM10b の 3 枚にする | (a) 1、TD1（`ERROR: 取得範囲の DEM10b のタイルがすべて未整備（HTTP 404）のメッシュがある: 5339（4 枚）`）、4 枚のキャッシュは残る。(b) 返り値 2、2 枚のキャッシュが無く、`(101, 200)` は残る。(c) 返り値 0（`5341` は範囲の DEM10b がすべて北方領土除外なので見ない）。(d) 1、TD1 の `{meshes}` は `5340（3 枚）` だけ |
| `UT-fetch_tiles-32` | 海の位置 | 同じプロセス。小さな範囲 | `find_sea_positions(<positions>, <dem10b>, <notfound>, {'5439'}, <nt>)` を (a) `list_fetch_tiles({'5439'}, set())` の 2 つの集合、`notfound` は DEM10b の 25 枚すべて、`nt = set()`、(b) (a) の `notfound` から `(114, 214)` を除く、(c) `nt = {(220, 420)}` で `list_fetch_tiles({'5439'}, nt)` の 2 つの集合、`notfound` はその DEM10b の 24 枚すべて | (a) 海の位置は x = 222〜227・y = 422〜427 の 36、並びは `[('5439', 100, 36)]`。(b) (a) の 36 から x = 226・227・y = 426・427 の 4 を除いた 32、`[('5439', 100, 32)]`。(c) (a) の 36 から x = 222・223・y = 422・423 の 4 を除いた 32（北方領土除外で要求しない `(110, 210)` を 404 でなかったものとして扱う）、`[('5439', 99, 32)]` |
| `UT-fetch_tiles-33` | DEM5 の位置ごとの取り方と消し方 | 同じプロセス。模擬サーバー。位置 P1 = `(200, 400)`、P2 = `(200, 401)`、P3 = `(201, 400)`、P4 = `(201, 401)`、P5 = `(202, 400)`、海の位置 S = `(202, 401)`。台本は P2 の DEM5a が 404、P3 の DEM5a・5b が 404、P4 の DEM5a が 304、P5 の DEM5a が 404・DEM5b が 304（ほかは既定の 200）。キャッシュは P1 の DEM5b・5c、P2 の DEM5a・5c、P4 の DEM5a・5b、P5 の DEM5b・5c、S の DEM5a に置く | `download_dem5({P1, P2, P3, P4, P5, S}, {S}, '<tmp>/tiles', 2, 0, 'UA/1')` | 要求は、P1 は DEM5a、P2 は DEM5a・5b、P3 は DEM5a・5b・5c、P4 は DEM5a、P5 は DEM5a・5b だけで、S には無い。後のキャッシュは、P1 は DEM5a だけ、P2 は DEM5b だけ、P3 は DEM5c だけ、P4 は DEM5a だけ（中身と mtime は前のまま）、P5 は DEM5b だけ（前のまま）、S は DEM5a（前のまま）。返り値は（`DEM5a` が `取得` 1・`変更なし` 1・`未整備` 3・`404 で削除` 1・`下位で削除` 0、`DEM5b` が 1・1・1・0・2、`DEM5c` が 1・0・0・0・3, 1）。標準出力は `途中経過: DEM5 の位置 1/5（20%）` から `5/5（100%）` までの 5 行 |
| `UT-fetch_tiles-34` | 初めての取得 | 子のプロセス。模擬サーバー | `--mesh 5339` | 0。取得完了の記録は `5339\n`。要求は DEM10b が x = 100・101・y = 200・201 の 4 枚、DEM5a が x = 200〜203・y = 400〜403 の 16 で、DEM5b・5c は無い。どの要求も `User-Agent` は `findsummits/v0-test (mailto:test@example.com)` で、`If-Modified-Since` は無い。DEM10b の 4 枚を返し終えてから DEM5a の最初の要求を受ける。キャッシュの 20 のファイルの mtime は 1445412480。ログファイルの行は、L1（`開始: fetch_tiles --config ../c.ini --mesh 5339`）、L2（`設定ファイル: <tmp>/c.ini` と、`data_dir`・`log_dir`・`max_parallel`・`interval_ms`・`user_agent_email` の 5 行。どれも `ファイル`）、TL1（`対象のメッシュ 1 件: 5339`）、TL2、TL3 の DEM10b の 4 行、TL3 の DEM5 の 16 行、TL4（`結果の要約: タイルの取得を終えた（取得完了の記録はこの後に書く）。対象のメッシュ 1 件`、`DEM10b: 取得 4、変更なし 0、未整備 0、削除 0`、`DEM5a: 取得 16、変更なし 0、未整備 0、削除 0`、`DEM5b: 取得 0、変更なし 0、未整備 0、削除 0`、`DEM5c: 取得 0、変更なし 0、未整備 0、削除 0`、`海として DEM5 を要求しなかった位置: 0`、`海の位置: 5339 判定対象 16、海 0、割合 0.0%`）、L3（終了コード 0）の順。標準出力は同じ文面が時刻なしで同じ順 |
| `UT-fetch_tiles-35` | 記録の書き直し | 子のプロセス。模擬サーバー | (a) 記録を `5339\n` にして `--mesh 5340`、(b) 記録を `5339\n9999\n` にして `--mesh` なし | (a) 0、記録は `5339\n5340\n`。要求は DEM10b が `(102, 200)`・`(102, 201)`・`(103, 200)` の 3 枚、DEM5a が B の 16 から `(207, 403)` を除いた 15。(b) 0、記録は `5339\n5340\n`（`9999` の行は残らない） |
| `UT-fetch_tiles-36` | 対象が 0 件 | 子のプロセス。模擬サーバー。記録を `5339\n` にして、バイト列と mtime を控える。キャッシュに DEM10b の `(104, 200)`、DEM5a の `(208, 400)`、DEM5b の `(207, 403)`、DEM5a の `(205, 400)` を置く。`<tmp>/work/m.txt` に `9999\n6848\n` を書く | `--mesh m.txt` | 0。標準エラー出力は TW2（`6848`）の 2 行の後に TW1（`9999`）の 2 行。模擬サーバーは要求を受けない。記録のバイト列と mtime は控えたとおり。DEM10b の `(104, 200)`、DEM5a の `(208, 400)`、DEM5b の `(207, 403)` のキャッシュが無く、DEM5a の `(205, 400)` は残る。ログの要約は TL5（`結果の要約: 対象のメッシュが 0 件なので取得しなかった（取得完了の記録は変えていない）`、`DEM10b: 取得 0、変更なし 0、未整備 0、削除 1`、`DEM5a: 取得 0、変更なし 0、未整備 0、削除 1`、`DEM5b: 取得 0、変更なし 0、未整備 0、削除 1`、`DEM5c: 取得 0、変更なし 0、未整備 0、削除 0`）。TL1 は `対象のメッシュ 0 件` |
| `UT-fetch_tiles-37` | 起動前提条件の不足と記録の誤り | 子のプロセス。模擬サーバー。記録を `5339\n` にし、DEM10b の `(100, 200)` のキャッシュを置き、記録とキャッシュのバイト列と mtime を控える | `--mesh 5339` で、(a) `nt_excluded_tiles.txt` を消す、(b) `nt_excluded_meshes.txt` をディレクトリにする、(c) `n03_version.txt` を消す、(d) 記録を `52a9\n` にする（控えもこの中身で採る）、(e) `<tmp>/src/params/mesh_list_japan.txt` を消す（それぞれ） | どれも 1。メッセージは (a) TP1、(b) R2（2 行目は `venv/bin/python3 scripts/preprocess_boundaries.py --config <tmp>/c.ini を起動して正常に終えてから、もう一度起動する`）、(c) TP3、(d) FC2（`{detail}` は `1 行目が 4 桁の数字でない: 52a9`、2 行目の `{config_opt}` は空白 1 つと `--config <tmp>/c.ini`）、(e) R1（既定の対処）。模擬サーバーは要求を受けない。記録とキャッシュは控えたとおり。ログの要約は TL6（`結果の要約: 途中で止まった（入力の読み込み）。終えた分:` と 4 行の 0）で、記録から外した旨の行は無い |
| `UT-fetch_tiles-38` | DEM10b がすべて 404 で止まる | 子のプロセス。模擬サーバーは A の DEM10b の 4 枚に 404。記録を `5339\n5340\n` にし、DEM10b の `(100, 200)` のキャッシュを置く | `--mesh 5339` | 1、TD1（`5339（4 枚）`）。DEM5 の要求は無い。記録は `5340\n`。`(100, 200)` のキャッシュは残る。ログの要約は TL6（`結果の要約: 途中で止まった（DEM10b の検査）。終えた分:`、`DEM10b: 取得 0、変更なし 0、未整備 4、削除 0`、DEM5 の 3 行は 0、最後に `今回の対象のメッシュは取得完了の記録から外したまま（起動し直して正常に終えると記録に戻る）`） |
| `UT-fetch_tiles-39` | シグナルでも実行中の要求を待つ | 子のプロセス（`subprocess.Popen`）。模擬サーバーは `(100, 200)` の DEM10b を `hold` で止める。記録を `5339\n` にする | `--mesh 5339` で起動し、模擬サーバーが A の DEM10b の 4 枚すべての要求を受けたら（10 秒まで待つ）子に `SIGTERM` を送り、0.3 秒後に `hold` の `Event` を `set` する | 143。子が終わったのは `set` より後。`SIGTERM` を送ってから 0.1 秒より後に受けた要求は無い。ログファイルの最後の行は `SIGTERM` を受けて止まった形の L3 で、その前が TL6（`結果の要約: 途中で止まった（DEM10b の取得）。終えた分:`、`DEM10b: 取得 4、変更なし 0、未整備 0、削除 0`〈止めた後に終わった `(100, 200)` も数える〉、DEM5 の 3 行は 0、最後に記録から外した旨の行）。記録は空のファイル。`(100, 200)` のキャッシュは中身 `PNG`・mtime 1445412480。`<tmp>/data/tiles` の下に `.tmp` で終わるファイルは無い |
| `UT-fetch_tiles-40` | 同時起動 | 子のプロセス。模擬サーバー。テストのプロセスが `<tmp>/data/findsummits.lock` を開いて `fcntl.flock(LOCK_EX)` で持つ | `--mesh 5339` | 1、G1（`{lock_path}` は `<tmp>/data/findsummits.lock`）。`<tmp>/logs` が無い。模擬サーバーは要求を受けない |
| `UT-fetch_tiles-41` | ワーカーの例外はメインで止まる | 子のプロセス。模擬サーバー。試験用のプログラムで、さらに `fetch_tiles.save_tile` を `RuntimeError('boom')` を上げる関数に差し替える。記録を `5339\n` にする | `--mesh 5339` | 1。標準エラー出力に `ERROR: 予期しない例外で止まった: RuntimeError: boom` と `Traceback (most recent call last):` の行。ログの要約は TL6（`DEM10b の取得`）。記録は空のファイル |
| `UT-fetch_tiles-42` | DEM5 の途中で止まっても確定した結果は数えて消す | 同じプロセス。模擬サーバー。位置 P1 = `(200, 400)` の DEM5a が 404、DEM5b が 403。P1 の DEM5a のキャッシュを置く | `download_dem5({(200, 400)}, set(), '<tmp>/tiles', 1, 0, 'UA/1')` | 1、TG1（`DEM5b 15/200/400`、`再試行しない応答`、`HTTP 403`）。P1 の DEM5a のキャッシュが無い（止まる前に確定した 404 で消す）。`_tally['DEM5a']` は `未整備` 1・`削除` 1、`_tally['DEM5b']` はどれも 0 |
| `UT-fetch_tiles-43` | 最後の記録の書き込みに失敗する | 子のプロセス。模擬サーバー。試験用のプログラムで、さらに `os.replace` を、置き換え先の名前が `fetch_complete.txt` の呼び出しの 2 回目だけ `OSError(errno.EACCES, os.strerror(errno.EACCES))` を上げる物（ほかは元の `os.replace` を呼ぶ）に差し替える。記録を `5339\n` にする | `--mesh 5339` | 1。ログの行は、TL4（1 行目 `結果の要約: タイルの取得を終えた（取得完了の記録はこの後に書く）。対象のメッシュ 1 件`）の後に TF1 の 2 行（`{path}` は記録のパス、`{reason}` は `Permission denied`）、L3（終了コード 1）の順。記録は空のファイル（対象を外した後のまま）。キャッシュの 20 のファイルは残る。`fetch_complete.txt.tmp` は残らない |
| `UT-fetch_tiles-44` | ワーカーを起こす途中のシグナル | 子のプロセス。模擬サーバーは `(100, 200)` の DEM10b を `delay` 0.5 にする。試験用のプログラムで、さらに `threading.Thread.start` を、元の `start` を呼んだ後、1 回目の呼び出しのときだけ自分へ `SIGTERM` を送る物に差し替える。記録を `5339\n` にする | `--mesh 5339` | 143。ログファイルの最後の行は `SIGTERM` を受けて止まった形の L3 で、その前が TL6（`DEM10b の取得`。最後に記録から外した旨の行）。模擬サーバーが受けた要求は 1 回以下で、受けた要求は返し終えている（子は実行中の要求を待ってから終わる）。`<tmp>/data/tiles` の下に `.tmp` で終わるファイルは無い |
| `UT-fetch_tiles-45` | 段をまたいでも間隔を守る | 同じプロセス。模擬サーバー | `download_tiles({(100, 200)}, '<tmp>/tiles', 1, 300, 'UA/1')` の直後に、`download_dem5({(200, 400)}, set(), '<tmp>/tiles', 1, 300, 'UA/1')` | 2 回の要求を受けた時刻の差が 0.27 秒以上（2 つの段で同じ `_gate` を使う） |
| `UT-fetch_tiles-46` | 使い直す前に切られた接続を見つけて張り直す | 同じプロセス。模擬サーバーは、どの応答の後にも、`Connection: close` を付けずにハンドラの側で接続を切る（`self.close_connection = True`）。`_FIRST_WAIT_S` と `_WAIT_CAP_S` を 1.0 に差し替える（再試行の待ちがちょうど 1.0 秒になる） | 同じスレッドで、同じ `_Gate(0)` を渡して `fetch_one_tile` を `(100, 200)` の DEM10b に呼び、0.1 秒おいて `(100, 201)` に呼ぶ | どちらも `'fetched'`。模擬サーバーが受けた要求は 2 回で、どちらも応答を返し終えている（切られた接続には要求を出さない）。2 回の要求のクライアントのポートが違う（2 回目は張り直した接続で来る）。2 回目の呼び出しは 0.5 秒より前に終わる（再試行の待ち 1.0 秒を待たない） |
| `UT-fetch_tiles-47` | 取り出しの途中で削除が失敗しても確定した結果は数える | 同じプロセス。`work` は、3 つのワーカーが全員そろう `threading.Barrier(3)` を待ってから `(item, None)` を返す関数。`on_done` は、呼ばれた単位を並びに足してから `sys.exit(1)` を呼ぶ関数 | `_run_pool(['a', 'b', 'c'], work, 3, 0, 'x', on_done)` | `SystemExit` が上がり、終了コードは 1。`on_done` は 3 つの単位すべてに呼ばれる（1 つ目で抜けた後の取り出しでも、残りの 2 つを数える） |

- UT 候補の数の理由: [HLD 4.1.2](30_HLD.md#412-処理の流れ) の 1〜8、応答の表の各行、[HLD 4.1.3](30_HLD.md#413-異常系) の異常系の表と「再試行」の各段落、IT が UT に送った待ち時間の計算（`IT-CMP2-EXT2-06` の「待ち時間の計算は UT で照らす」）を、それぞれ 1 つ以上のケースで照らす。実サーバーへの要求（`IT-CMP2-EXT2-01`）と、実時間の 60 秒以上の待ち（IT の `CMP2-EXT2`）は UT で行わない。
- 子のプロセスのケースも、起動の部分ではなく試験用の短いプログラムから `main` を呼ぶ（`_BASE_URL` と範囲と待ちの定数を差し替えるため。3.1.5 の `UT-preprocess_boundaries-11` と同じ形）。待ちの定数を小さくして、待ちの計算（`UT-fetch_tiles-04`）と待ちの振る舞い（`23`〜`26`）を分けて照らす。

## 5. CMP3 パイプライン制御

この章は、CMP3（パイプライン制御）の 2 本のプログラム（[HLD 3.3.1](30_HLD.md#331-プログラム)）のモジュールを置く。5.1 `run_pipeline` は bash、5.2 `resolve_config` は Python で書く。`resolve_config` と `run_pipeline` は、起動（`--config <絶対パス>`）、標準出力の 2 行、終了状態だけでつながる（結合のつなぎ目 `CMP3-INT1`。[HLD 3.3.5](30_HLD.md#335-結合のつなぎ目)）。

### 5.1 `run_pipeline`

- **ID**: LLD-run_pipeline
- **対応 HLD**: [3.3](30_HLD.md#33-cmp3-パイプライン制御)・[4.1](30_HLD.md#41-fr-001-標高タイル事前取得)・[4.23](30_HLD.md#423-fr-023-解析パイプライン制御)・[5.6](30_HLD.md#56-nfr-006-可搬性環境)・[5.7](30_HLD.md#57-nfr-007-ログ出力)・[5.11](30_HLD.md#511-nfr-011-手順文書による環境構築成果物生成の完遂性)
- **ファイル**: `scripts/run_pipeline.sh`

処理の正本は[HLD 4.23.2](30_HLD.md#4232-処理の流れ)（順序の正本は[HLD 2.9.3](30_HLD.md#293-同時起動の排他)）で、関数の名前と役割は[HLD 3.3.3](30_HLD.md#333-関数)の表のとおり。この節は、それを bash で書くための細部（変数、コマンド、メッセージの文面、ログの行）だけを足す。[5.6](30_HLD.md#56-nfr-006-可搬性環境)（可搬性）は、Linux のコマンド（util-linux の `flock`、GNU coreutils の `readlink`・`realpath`・`date`、GNU grep、glibc の `iconv`）と `/proc/uptime` を使うので、Linux だけで動くこと（動作の前提の環境は環境定義の Ubuntu）で受ける。[5.11](30_HLD.md#511-nfr-011-手順文書による環境構築成果物生成の完遂性)（手順文書）は、どのメッセージにも `対処:` の行で次の操作を書くことで受ける。[4.1](30_HLD.md#41-fr-001-標高タイル事前取得)は、日本全土1次メッシュコードリストと北方領土除外メッシュリストの読み方（[HLD 4.1.2](30_HLD.md#412-処理の流れ)の 2「入力を読む」）と、取得完了の記録の読み方（[2.3](#23-ファイルの名前と書き方)）で受ける。結合のつなぎ目は `CMP3-INT1`・`CMP3-EXT1`〜`CMP3-EXT6`（[HLD 3.3.5](30_HLD.md#335-結合のつなぎ目)）で、その結合テスト（IT）のケースは `60_IT.md` の `IT-CMP3-INT1-01`〜`04` と `IT-CMP3-EXT1-01`〜`IT-CMP3-EXT6-04` である。

#### 5.1.1 ファイル割付

- 関数と本体はすべて `scripts/run_pipeline.sh` 1 本に置く。1 行目は `#!/usr/bin/env bash`、2 行目は `# trace: LLD-run_pipeline`、3 行目は `set -euo pipefail`。ファイルは実行できる権限で git に入れる（利用者は `scripts/run_pipeline.sh` で起動する。[HLD 2.6.4](30_HLD.md#264-ディレクトリ構成)）。並びは、定数、関数の定義、本体の順。
- UT のコードは `tests/scripts/test_run_pipeline.py` に置き、`scripts/run_pipeline.sh` を子のプロセスで起動して確かめる（[5.1.5](#515-ut-候補)の共通の準備）。各テストに `# trace: UT-run_pipeline-NN` のコメントを付ける。テストの枠組みは[2.1.1](#211-ファイル割付)と同じく[テスト方針書 3.4](02_test_policy.md#34-テストを先に書く進め方)で選んだ。Python から子のプロセスで起動する形は、テスト方針書 3.4 が CMP3 の bash のテストのしかたとして選んだもの。

UT のコードを Python で書く理由: UT 候補はどれも、起動の引数・終了コード・画面の出力・ログファイル・内部の起動口に渡した引数・消したファイルを、プログラムの外から見るものなので、子のプロセスで起動して確かめる。テストを動かす環境は 2.1・5.2 と同じ venv にする。bash のテストの枠組み（bats など）は新しい依存になり、[HLD 2.6.3](30_HLD.md#263-ライブラリと使う範囲)の判断が要るので使わない。

#### 5.1.2 型とデータ

bash の変数で持つ。関数が「返すもの」（[HLD 3.3.3](30_HLD.md#333-関数)の表）は、下の表のグローバル変数に入れて返す（関数の終了状態は、止まらないかぎり 0。HLD 3.3.3 の「関数は直接呼ぶ」「充足判定の結果は変数で本体へ渡す」）。関数の中だけで使う変数は `local` で宣言する。

- 定数（`readonly`）: `EXIT_OK=0`・`EXIT_ERROR=1`・`EXIT_USAGE=2`・`EXIT_UNRESOLVED=3`・`EXIT_DEFECT=4`（[HLD 2.5.1](30_HLD.md#251-終了コード)。HLD 3.3.3 の「3.9 の同じ名前の部品と同じ決まりを bash で別に実装したもの」）、`LOCK_NAME=findsummits.lock`・`FETCH_RECORD_NAME=fetch_complete.txt`（[2.3](#23-ファイルの名前と書き方)）。ロックファイルの記述子は 9、ログファイルの記述子は 8 にする（bash のリダイレクトは記述子の番号を変数で書けないので、定数にせず、どこでも数字で直接書く）。
- ソースツリー（`readonly`。定数の並びの中で求める）: `SOURCE_ROOT` は `readlink -f -- "${BASH_SOURCE[0]}"` の親の親（シンボリックリンクから起動されても、リンクの先のファイルの置き場から求める。[HLD 3.3.1](30_HLD.md#331-プログラム)の「自分の置き場から求め、起動した作業ディレクトリによらない」）。`DEFAULT_CONFIG_PATH="$SOURCE_ROOT/params/config.ini"`、`PYTHON="$SOURCE_ROOT/venv/bin/python3"`、`SCRIPTS_DIR="$SOURCE_ROOT/scripts"`（内部の起動口の Python のファイルは `$SCRIPTS_DIR/<名前>.py`）、`ANALYZE_TERRAIN="$SOURCE_ROOT/build/analyze_terrain"`、`JAPAN_MESH_LIST="$SOURCE_ROOT/params/mesh_list_japan.txt"`（[HLD 2.3.1](30_HLD.md#231-受け渡す値の種類)の `params/` のファイルの段落、[DEC151](30_HLD.md#234-設計判断)「CMP4 には日本全土リストのパスを引数で渡す」）。
- 起動の時刻: `START_STAMP`（`date +%Y%m%dT%H%M%S` の値。ログファイルの名前に使う）と `START_UP`（`/proc/uptime` の 1 つ目の値。所要時間に使う）。どちらもファイルの先頭の定数の並びで、引数を読む前に取る（[HLD 5.7.2](30_HLD.md#572-処理の流れ)の 2「ファイルの名前」）。所要時間を `/proc/uptime` で測るのは、時刻の補正に左右されない時計にするため（HLD 5.7.1 の対象外の行。[2.1.2](#212-型とデータ)の `StartTime` の `mono` と同じ考え方）。
- メッシュコードの集合: 添字をコードの数（`$((10#$code))`）、値をコードの文字列にした添字付きの配列（`declare -a`）。`0123` は添字 123、値 `0123`。添字の昇順に並ぶので、`"${!集合[@]}"` で昇順にたどれ、並べ替えのコマンドが要らない。含むかは `[[ -n ${集合[$i]+x} ]]` で見る。
- グローバル変数（どれも本体が使う前に、下の関数が値を入れる。宣言はファイルの先頭の定数の後に、空の値で置く。`CONFIG_GIVEN`・`MESH_GIVEN`・`LOG_OPEN`・`LOG_BROKEN` だけは `0` で置く）:

  | 変数 | 入れる関数 | 中身 |
  |---|---|---|
  | `CONFIG_PATH` | `parse_args` | 設定ファイルの絶対パス |
  | `CONFIG_GIVEN` | `parse_args` | `--config` を渡されたら `1`、渡されなければ `0` |
  | `PHASE` | `parse_args` | `--phase` の値（`2`・`3`・`4`）か、通しなら空 |
  | `STAGE_N` | `parse_args` | `--n` の値（`4`・`5`・`6`）か空 |
  | `MESH_GIVEN` | `parse_args` | `--mesh` を渡されたら `1`、渡されなければ `0`（`--mesh ''` も `1`） |
  | `MESH_VALUE` | `parse_args` | `--mesh` の値（受け取ったまま）。渡されなければ空。`parse_args` が終わった後は、空の値は A1 で止まっているので、空は「渡されなかった」だけを表す |
  | `MESH_ARG_CODES` | `read_mesh_arg` | `--mesh` のコードの集合 |
  | `DATA_DIR`・`LOG_DIR` | `resolve_paths` | 設定解決が返した 2 つのパス（受け取ったまま） |
  | `JAPAN_CODES`・`EXCLUDED_CODES` | `read_mesh_list_file`（本体が配列の名前を渡す） | 日本全土1次メッシュコードリストと北方領土除外メッシュリストのコードの集合 |
  | `REQUIRED_CODES` | `list_required_meshes` | 解析に要るメッシュの集合 |
  | `FETCH_RECORD_PATH` | `fetch_record_path` | 取得完了の記録のパス |
  | `LOG_PATH` | `open_log` | ログファイルの絶対パス（開く前は空） |
  | `LOG_OPEN`・`LOG_BROKEN` | `open_log`・`_emit` | ログファイルを開いたら `LOG_OPEN=1`、書けなくなったら `LOG_BROKEN=1`（初めはどちらも `0`） |
  | `SIGNUM` | `_on_signal` | 受けたシグナルの番号（受けていなければ空） |
  | `CHILD_RC` | `_run_child` | 最後に起動した内部の起動口の終了状態 |
  | `SATISFY_RC` | `run_merge` | 充足判定の結果（`0` か `3`） |
  | `CURRENT_STAGE`・`LAST_STAGE`・`LAST_RESULT` | 本体・`run_merge`・`run_phase4` | 今の段の名前（段の外では空）、最後に終えた段の名前と結果の文（[5.1.4](#514-メッセージ文面)の PL8 の `{stage}` と `{result}`。まだ無ければ空） |
  | `PRECOND_WHAT`・`PRECOND_ACTION` | `check_preconditions`・`check_fetch_record` | 起動前提条件の誤りの `what` と `action`（同じ添字で対になる配列。初めは空） |

#### 5.1.3 関数の細部

bash の規約（この節の関数すべてに当てる。bash のモジュールは今は 5.1 だけなので、ここに置く。CMP8（公開用ビューア）の `build_public_site`〈10.1〉を書くときに、共通にするものを[1.2](#12-lld-の規約)に移す）:

1. `set -euo pipefail` の下で書く（[HLD 2.5.2](30_HLD.md#252-パイプライン制御での扱い)）。この節の関数は、[HLD 3.3.3](30_HLD.md#333-関数)のとおり直接呼び、`||`・`&&`・`if`・`while` の条件、`$( )`、パイプの中で呼ばない。外部のコマンドと bash の組み込みのコマンドは、条件や `|| rc=$?` の中に置いてよい。`set -e` で止まらないように受けたい外部のコマンドは、`rc=0; <コマンド> || rc=$?` の形で受ける。
2. 3 行目の `set -euo pipefail` の次の行に、`set +o posix +o noglob` と `shopt -u failglob nullglob` を置き、続けて `trap '' PIPE` を置く。前の 2 つは、環境変数の `SHELLOPTS`・`BASHOPTS` から入るシェルのオプションで、グロブと `exec` の振る舞いが変わるのを打ち消すため。`trap '' PIPE` は、標準出力が読む相手のいないパイプのとき（`scripts/run_pipeline.sh | head` など）に、`run_pipeline` が SIGPIPE で黙って止まって（141）、終わりの行も要約も残らないのを防ぐため。無視にしておけば、書き込みが失敗して終了状態が 0 以外になるだけになり、下の `_emit` の決まりで止まる。内部の起動口は SIGPIPE を既定に戻して起動する（下の `_run_child` と `resolve_paths`。無視の扱いが起動口に引き継がれないようにするため）。
3. 数の足し算は `i=$((i + 1))` と書く（`((i++))` は値が 0 のとき終了状態が 1 になり、`set -e` で止まるため）。
4. 作業ディレクトリを変えない（`cd` を書かない。[HLD 3.3.1](30_HLD.md#331-プログラム)）。環境変数を足さず、変えずに内部の起動口へ渡す（シェルの変数 `LC_ALL` も変えない）。パスの変数は、どこでも `"…"` で囲んで展開する（`DATA_DIR` などの値に空白や `[`・`*` があっても、語に分かれたりグロブとして広がったりしないため）。グロブと組み合わせるときは、変数の部分だけを囲み、グロブの部分を囲まない（例 `"$DATA_DIR"/ref/sota_updatelist_[0123456789][0123456789][0123456789][0123456789].xhtml`、`"$DATA_DIR"/results/csv/"$n"-[0123456789]…`）。
5. ロケール: 文字の種類を判定するところでは、範囲（`[0-9]`・`[A-Z]`）を使わず、字を並べて書く（`[0123456789]` など）。ロケールによらず ASCII の字だけに合わせるため（HLD 4.23.2 の登録変更リストの「数字は ASCII の 0〜9 だけ」）。`grep`・`iconv` は、コマンドの前に `LC_ALL=C` を付けて動かす（そのコマンドにだけ効く）。
6. メッセージの `{reason}`（[2.2](#22-ログとメッセージの文面)の G2・G3・G5・G6 などの OS の理由）は、失敗したコマンドを `LC_ALL=C` で動かして標準エラー出力を変数に受け、その最後の行の、最後の「`:` と空白 1 つ」より後の部分にする（例: `mkdir: cannot create directory '/x': Permission denied` から `Permission denied`）。bash のリダイレクトの失敗は、`err=$( { LC_ALL=C; : <"$path"; } 2>&1 )` のように、サブシェルの中で同じリダイレクトを試して受ける（サブシェルの中で `LC_ALL` を変えても、親のシェルは変わらない）。
7. メッセージとログの行は、下の `log_info`・`log_warning`・`log_error` で出す。文面の書き方は[2.2](#22-ログとメッセージの文面)。引数の値などを文面に引用するときは、2.2 の引用の決まりで書く（下の `_quote`。当てる範囲は 2.2 の「引用の決まりを当てる範囲」。メッセージの対象のパスは引用しない）。
8. 内部の起動口は、下の `_run_child` で起動する。起動口の標準出力と標準エラー出力は、`resolve_config` の標準出力を除き、受け取らずに画面へそのまま出す（[HLD 5.7.2](30_HLD.md#572-処理の流れ)の 6「`run_pipeline` のログ」）。起動口は前に置いて（フォアグラウンドで）動かし、終わるまで待つ。
9. シグナル: `open_log` の前は bash の既定の扱いで、`SIGINT`・`SIGTERM` を受けるとその場で止まる（呼んだ側から見た終了コードは 128＋シグナル番号）。`open_log` の後は `_on_signal` で受け、終わりの行にシグナルの名前を書いて 128＋シグナル番号で止まる。bash は、前で動かしている起動口が終わるまでシグナルの処理を待つ。端末の Ctrl-C は起動口にも届くので起動口が止まり、その後に `run_pipeline` が 130 で止まる。`run_pipeline` のプロセスだけに `SIGTERM` を送ったときは、動いている起動口が終わってから 143 で止まる（起動口には送り直さない）。すぐに止めたいときはプロセスのグループに送る（利用手順書に書く）。起動口がシグナルで止まって 0・3・4 以外を返したときは、その値で止まる（[HLD 2.5.1](30_HLD.md#251-終了コード)の「子がシグナルで止まったら同じ値」）。

シグナルを起動口へ送り直さない理由: 起動口を後ろ（`&` と `wait`）で動かせば、受けたシグナルをすぐに処理して起動口へ送り直せるが、bash は後ろで動かすコマンドの `SIGINT` を無視にして起動するので、Ctrl-C で起動口が止まらなくなり、起動口の終了状態の受け方も複雑になる。HLD 2.5.1 は送り直しを求めていない。

確かめた事実（bash 5.3.9、GNU grep・iconv・flock、2026-10-21 に Linux のコンテナで確かめた）: bash の `read` は入力の NUL を捨てる。`exec` のリダイレクトの失敗は、POSIX モードでない bash では `if` の条件の中に置けば止まらずに終了状態 1 になる。`exec 9<>file` で開いた記述子は起動口に引き継がれ、`flock` のロックは、その記述子を持つプロセスがすべて終わるまで外れない。`set -C` の下の `>` は、既にあるファイルに書かずに失敗する。フォアグラウンドの起動口を待つ間に受けたシグナルの trap は、起動口が終わってから動く。SIGPIPE を無視にすると、切れたパイプへの書き込みは失敗になるだけで殺されない。`iconv` の UTF-8 から UTF-8 への変換は、U+10FFFF を超える符号位置と 5 バイトの列を通してしまうので、検査の変換先は UTF-32LE にする。

##### 起動と準備

###### parse_args

`parse_args "$@"`（受け取るのは起動の引数のすべて）。入れるもの: `CONFIG_PATH`・`CONFIG_GIVEN`・`PHASE`・`STAGE_N`・`MESH_GIVEN`・`MESH_VALUE`・`MESH_ARG_CODES`。

1. 引数を左から 1 つずつ読む。受け付けるのは `--config`・`--phase`・`--n`・`--mesh`（値を 1 つとる）と `--help`（値をとらない）だけ。値は、次の引数（`--phase 2`）か、名前の後の `=` の後（`--phase=2`）で受け取る。`=` の形では、最初の `=` で分ける（`--mesh=a=b` の値は `a=b`）。次の引数で受け取る値は、`-` で始まっていてもそのまま値にする（`--config --help` の `--config` の値は `--help`）。
2. 次のどれかなら、その場で止まる（終了コード 2。メッセージは[5.1.4](#514-メッセージ文面)）: 受け付けない引数（`--` で始まらない引数、`--foo`、`--help=x`、`--` だけ。PA1）、値をとる名前が最後にあって値が無い（PA2）、同じ名前を 2 回（`--help` を除く。PA4）。PA4 は名前を読んだ時点で、値を受け取るより先に見る（`--phase 2 --phase` は PA2 でなく PA4）。
3. `--help` を読んだら、それより後の引数を読まずに、5.1.4 の使い方の文を標準出力に出して `exit "$EXIT_OK"`（ロックを掛けず、設定解決も起動しない。[HLD 2.9.3](30_HLD.md#293-同時起動の排他)）。`--help` より前の引数の誤りは、2 で先に止まる。
4. 読み終えたら、値を確かめる（PA3。この順）: `--config` の値が空、`--phase` の値が `2`・`3`・`4` のどれでもない、`--n` の値が `4`・`5`・`6` のどれでもない。続けて組み合わせ（PA5。この順）: `--phase 3` で `--n` が無い、`--n` があって `--phase` が `3` でない、`MESH_GIVEN` が 1 で `--phase` が `3` か `4`（[HLD 2.4.4](30_HLD.md#244-フェーズ指定)）。どれも最初に当たったもので止まる。
5. `CONFIG_PATH`: `--config` が無ければ `DEFAULT_CONFIG_PATH`（`CONFIG_GIVEN=0`）。あれば、`/` で始まればその値、それ以外は `"$PWD/<値>"`（`CONFIG_GIVEN=1`。正規化しない。[HLD 2.3.2](30_HLD.md#232-設定ファイル)の「相対パスは起動した作業ディレクトリが基準」）。
6. `MESH_GIVEN` が 1 なら（`MESH_VALUE` には 1 の読み取りのときに値を入れてある）、`read_mesh_arg "$MESH_VALUE"` を呼ぶ（空の値は A1、そのほかの誤りも 2 で止まる）。

引数の書き方の理由: 長いオプション名の後の値は、次の引数と `=` の後の両方で受ける（GNU 形式の長いオプション。[HLD 2.4.2](30_HLD.md#242-共通の書式)）。名前の省略（`--ph`）は受けない。

###### read_mesh_arg（bash）

`read_mesh_arg <値>`。入れるもの: `MESH_ARG_CODES`。[2.1.3](#213-関数の細部)の `read_mesh_arg` と同じ決まりを bash で書く（[HLD の DEC149](30_HLD.md#4234-設計判断)「`--mesh` は bash と Python で別に読む」）。

1. 値が空なら A1（[2.1.4](#214-メッセージ文面)）で `exit "$EXIT_USAGE"`。値が `[0123456789]` の 4 字ちょうどなら、その 1 つのコードを集合に入れて戻る。
2. それ以外はファイルのパス。`_read_mesh_file <値> arg MESH_ARG_CODES` を呼ぶ（誤りなら A2〜A4 で 2 で止まる）。
3. 集合が空なら A5 で `exit "$EXIT_USAGE"`。

###### _read_mesh_file

`_read_mesh_file <パス> <arg|list> <配列の名前> [<案内>]`（内部。`read_mesh_arg` と `read_mesh_list_file` が使う）。2.1.3 の `_parse_mesh_lines` とファイルの読み方の決まりを bash で書く。2 つ目の引数が `arg` なら誤りを A2〜A4 で `EXIT_USAGE`、`list` なら R1〜R3 で `EXIT_ERROR` にする（`list` の R1〜R3 の `対処:` は 4 つ目の引数の案内。無ければ 2.1.4 の既定の対処）。読んだコードは、3 つ目の引数の名前の配列（`local -n` で受ける）に入れる。

1. メッセージの `{path}` は、どちらでも `realpath -s -m -- <パス>` の値にする（シンボリックリンクをたどらずに `.`・`..`・重なった `/` を字の上で除いた絶対パス。Python の `os.path.abspath` と同じ結果で、違うのは先頭の `//` を `/` にすることだけ）。以下の確かめと読み込みに当てる `path` は、2 つ目の引数で分ける。`arg` なら、その正規化した値（2.1.3 の `read_mesh_arg` の 2 と同じく、正規化した後のパスで有無を見る。`nodir/..` は `nodir` が無くても `path` が作業ディレクトリになる）。`list` なら、渡されたパスのまま（2.1.3 の `read_mesh_list_file` の「`path` は呼ぶ側が渡したまま使う」と同じ。`data_dir` がシンボリックリンクの後に `..` を含むとき、字の上で除くとリンクの先の親と別の場所を読むため）。`[[ -e $path ]]` が偽なら A2・R1。
2. 読めるかを見る: `[[ -d $path ]]` なら A3・R2（`{reason}` は `Is a directory`）。前置きの 6 の形で `: <"$path"` を試し、失敗すれば A3・R2（`{reason}` はその理由）。`LC_ALL=C iconv -f UTF-8 -t UTF-32LE <"$path" >/dev/null 2>&1` が 0 以外なら A3・R2（`{reason}` は `UTF-8 として読めない`。変換先を UTF-32LE にするのは、glibc の `iconv` が UTF-8 から UTF-8 への変換では U+10FFFF を超える符号位置と 5 バイトの列を通してしまい、Python の UTF-8 の読み方と食い違うため。テストベクトルの MV-18・MV-19）。
3. 誤りの行を探す: `rc=0; bad=$(LC_ALL=C grep -n -a -x -v -E -m 1 "$re" -- "$path" | tr -d '\000') || rc=$?`（`$re` は `$'(\xef\xbb\xbf)?[ \t\r]*(#.*|[0123456789]{4}[ \t\r]*)?'`。行の頭の BOM〈`EF BB BF`〉、空白・タブ・CR、`#` で始まる行、4 桁の数字と後ろの空白に合わない行を探す）。`rc` が 0 なら `bad` の `:` の前が行の番号。1 なら誤りの行は無い。2 以上なら A3・R2（`{reason}` は `grep` の標準エラー出力の理由）。続けて、2 行目以降の頭の BOM を探す: `LC_ALL=C grep -n -a -m 2 $'^\xef\xbb\xbf' -- "$path" | tr -d '\000'` の出力のうち、番号が 2 以上の最初の行（`grep` の終了状態は前と同じく受ける: 0・1 はそのまま、2 以上は A3・R2）。2 つの番号の小さい方を誤りの行にする（BOM を除くのはファイルの先頭の 1 つだけ。2 行目以降の BOM と、2 つ目の BOM は除かない）。誤りの行があれば A4・R3（`{line_no}` はその番号、`{line}` はその行の中身から、1 行目なら先頭の BOM を 1 つ除き、前後の空白・タブ・CR を除いたもの。NUL は `tr` が除いたもの）。
4. コードを読む: `while IFS= read -r line || [[ -n $line ]]; do …; done <"$path"` で行を読み、1 行目は先頭の BOM を 1 つ除き、前後の空白・タブ・CR を除き、空か `#` で始まれば飛ばし、残り（3 で 4 桁の数字と分かっている）を集合に入れる（重なりは 1 つ）。NUL は 3 で `#` の行の中にしか無いと分かっているので、`read` が捨てても結果は変わらない。

###### resolve_paths

`resolve_paths`。入れるもの: `DATA_DIR`・`LOG_DIR`。

1. `rc=0; out=$( trap - PIPE; "$PYTHON" "$SCRIPTS_DIR/resolve_config.py" --config "$CONFIG_PATH" | LC_ALL=C tr '\000' '\r' && printf '.' ) || rc=$?`。最後に `.` を足すのは、`$( )` が末尾の改行を除くのを防いで、出力の行の形のままを受けるため。`tr` で NUL を CR に替えるのは、`$( )` が NUL を黙って捨てて、壊れた出力が正しい 2 行に見えるのを防ぐため。2 の判定は CR を含む値、CR を含む名前、LF で終わらない出力をどれも外すので、NUL がどこにあっても（値の中、行の区切りの代わり、最後の LF の後）必ず外れる（LF に替えると、`data_dir=/data<NUL>log_dir=/logs\n` が正しい 2 行に化けるので使わない）。`pipefail` の下なので、`rc` は `resolve_config` の終了コードになる（`tr` は 0 で終わる）。`trap - PIPE` は前置きの 2 のとおり、起動口に SIGPIPE の無視を引き継がないため（`$( )` の中のサブシェルだけに効く）。`rc` が 0 以外なら、メッセージを足さずに `exit "$rc"`（設定解決が標準エラー出力に出している。ロックを掛けず、何も消さない。[HLD 2.3.2](30_HLD.md#232-設定ファイル)）。`resolve_config` は `_run_child` で起動しない（ログファイルがまだ無く、標準出力を受け取るため）。
2. `out` の最後の `.` を除き、次のすべてを満たすかを見る（HLD 2.3.2 の「2 行の形」）: 最後の字が LF。最後の LF を除いて LF で分けると、ちょうど 2 行。各行を最初の `=` で分けた名前の組が `data_dir` と `log_dir` の 1 つずつ（順は問わない）。どちらの値も空でなく `/` で始まり、CR（`\r`）を含まない（値の途中の CR も、行の LF の前の CR も外れる。[5.2](#52-resolve_config)は CR を含むパスを RP1 で拒否するので、正しい出力に CR は入らない）。`eval` しない。
3. 満たさなければ RS1 を `log_error` で出して `exit "$EXIT_ERROR"`（ロックを掛けず、何も消さない。ログファイルを開く前なので標準エラー出力だけ）。満たせば、値をそのまま `DATA_DIR`・`LOG_DIR` に入れる（正規化しない。5.2 の `write_resolved_paths` の 1 と同じく、ほかのバッチが設定ファイルから読む値と同じにするため）。

###### acquire_lock（bash）

`acquire_lock`。2.1.3 の `acquire_lock` と同じ決まりを bash で書く。

1. `lock_path="$DATA_DIR/$LOCK_NAME"`。前置きの 6 の形で `: <>"$lock_path"` を試し、失敗すれば G2（`{lock_path}`・`{reason}`）を `log_error` で出して `exit "$EXIT_ERROR"`。続けて `if ! { exec 9<>"$lock_path"; } 2>/dev/null; then` G2（`{reason}` は 1 つ目の試しと同じ形で取り直したもの）で止まる（`<>` は無ければ作る）。
2. `rc=0; err=$(LC_ALL=C flock -n -E 73 9 2>&1) || rc=$?`。`rc` が 73 なら G1、0 以外のほかの値なら G2（`{reason}` は `err` の理由）で `exit "$EXIT_ERROR"`。記述子 9 は閉じない（起動口に引き継がれ、すべてが終わるまでロックが外れない。[HLD 2.9.3](30_HLD.md#293-同時起動の排他)）。ロックファイルは消さない。

###### open_log

`open_log "$@"`（受け取るのは起動の引数のすべて。L1 に書く）。[HLD 3.3.3](30_HLD.md#333-関数)の `open_log`。

1. `mkdir -p -- "$LOG_DIR"` を `err` に受けて動かし、失敗すれば G3（`{path}` は `LOG_DIR`、`{config_path}` は `CONFIG_PATH`）で `exit "$EXIT_ERROR"`（`log_dir` がファイルのときも、`mkdir` が失敗する）。
2. `path="$LOG_DIR/run_pipeline_${START_STAMP}_$$.log"`（[HLD 5.7.2](30_HLD.md#572-処理の流れ)の 2「ファイルの名前」）。`err=$( { LC_ALL=C; set -C; : >"$path"; } 2>&1 )` が失敗したら、`[[ -e $path ]]` なら G4、そうでなければ G3（`{path}` は `path`）で `exit "$EXIT_ERROR"`（既にあるファイルには触れない）。
3. `if ! { exec 8>>"$path"; } 2>/dev/null; then` G3 で止まる。開けたら `LOG_PATH="$path"`、`LOG_OPEN=1`。
4. trap を次の順に付ける: `trap _on_exit EXIT`、`trap '_on_signal 2' INT`、`trap '_on_signal 15' TERM`（シグナルを最後にするのは、シグナルで止まるときに必ず `_on_exit` が動くようにするため。2.1.3 の `start_log` の 4 と同じ）。
5. L1（2.2。引数は `_quote` で引用）、PL1（起動のしかた）、PL2（データ置き場）、PL3（ログの置き場）をこの順に `log_info` で出す。L2（設定値）は書かない（HLD 3.3.3 の `open_log`）。

###### log_info・log_warning・log_error（bash）

`log_info <文>`・`log_warning <what> <action>`・`log_error <what> <action>`。出す行と出し先は 2.1.3 の同じ名前の部品と同じ（`log_info` は標準出力、ほかの 2 つは標準エラー出力。`WARNING:`・`ERROR:`・`対処:` の接頭辞は `what`・`action` の最初の行にだけ付ける）。どれも下の `_emit` で出す。

###### _emit（bash）

`_emit <out|err> <0|1> <文>`（内部）。2 つ目が `1` なら画面への出力の失敗を無視する（`_on_exit` だけが使う）。

1. 文を LF で行に分ける。
2. 画面: 1 つ目が `out` なら標準出力、`err` なら標準エラー出力に、各行を時刻なしで出す。標準エラー出力への書き込みの失敗は、いつも `|| true` で無視する（`log_warning`・`log_error` の後は必ず止まるので、出せなくても決まりの終了コードで止まるようにするため。5.2 の `_stop` の 1・2 と同じ考え方）。標準出力への書き込みの失敗は、2 つ目が `0` ならそのまま（`printf` が 0 以外を返し、`set -e` で終了コード 1 で止まる。`_on_exit` が要約と終わりの行をログファイルに書く。画面への出力の失敗を特別扱いしない。2.1.3 の `log_info` の「画面」の箇条と同じ）、`1` なら `|| true` で無視する。SIGPIPE は前置きの 2 で無視にしてあるので、切れたパイプでも書き込みの失敗になるだけで、`run_pipeline` は殺されない。
3. ログファイル: `LOG_OPEN` が 1 で `LOG_BROKEN` が 0 のときだけ、`date +%Y-%m-%dT%H:%M:%S%:z` の時刻（[HLD 5.7.2](30_HLD.md#572-処理の流れ)の 3「行の書式」。1 回の `_emit` の全行に同じ時刻）と空白 1 つを各行の頭に付けて、全行を 1 回の `printf` で記述子 8 に書く。前置きの 6 の形で、`if ! err=$( { LC_ALL=C; printf '%s' "$buf" >&8; } 2>&1 ); then` で失敗を受ける。失敗したら、`LOG_BROKEN=1` にし、G5（`{path}` は `LOG_PATH`）を標準エラー出力にだけ（`_emit err 1` で）出して `exit "$EXIT_ERROR"`。

###### _quote

`_quote <文字列>`（内部）。2.2 の引用の決まりの文字列を `QUOTED` に入れる（`$( )` の中で呼ばないため、変数で返す）。空でなく、どの字も `ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_@%+=:,./-` のどれかなら、そのまま。それ以外は、中の `'` を `'"'"'` に置き換えて `'` で囲む（空なら `''`）。引数の並びは、各引数を `_quote` した値を空白 1 つでつなぐ。

###### _on_signal（bash）

`_on_signal <番号>`（内部）。`SIGNUM` に番号を入れて `exit $((128 + 番号))`（`_on_exit` が動く）。

###### _on_exit

`_on_exit`（内部。`EXIT` の trap）。2.1.3 の `_finish_log` と同じ決まりを bash で書く。

1. `code=$?` を最初に取る。続けて `trap '' INT TERM`（後始末を途中で切らない）。
2. `LOG_BROKEN` が 1 なら、何も書かずに `exit "$EXIT_ERROR"`（[HLD 5.7.2](30_HLD.md#572-処理の流れ)の 4「始まりと終わりの行」の「ログファイルに書けなくなって止まるとき」）。
3. 結果の要約 PL9 を `_emit out 1` で出す（書けなければ `_emit` の 3 のとおり G5 で 1）。
4. L3（2.2）を作る。`SIGNUM` があれば、シグナルの形（`{signame}` は `2` なら `SIGINT`、`15` なら `SIGTERM`）で、終了コードは `code`（128＋番号）。`{end}` は今の時刻（`_emit` と同じ書式）。`{sec}` は今の `/proc/uptime` の 1 つ目の値から `START_UP` を引いた値（どちらも小数 2 桁なので、100 倍の整数で引き、`%d.%02d0` の形で小数 3 桁にする）。
5. L3 を、時刻と空白を付けて記述子 8 にだけ直接書く（`_emit` を使わない。書き込みの失敗を G5 でなく G6 にするため）。失敗したら G6 を標準エラー出力にだけ（失敗は無視して）出して `exit "$EXIT_ERROR"`（[HLD 5.7.3](30_HLD.md#573-異常系)の「終わりの行だけを書けなかった」）。書けたら、同じ文面を標準出力に時刻なしで出し（失敗は無視する）、`exit "$code"`。

##### 起動前提条件

###### read_mesh_list_file（bash）

`read_mesh_list_file <パス> <案内> <配列の名前>`。2.1.3 の `read_mesh_list_file` と同じ決まり（無い・読めない・誤りの行は R1〜R3 で `EXIT_ERROR`、空のファイルは空の集合）を、`_read_mesh_file <パス> list <配列の名前> <案内>` で行う。案内が空なら 2.1.4 の既定の対処。本体は、日本全土1次メッシュコードリストを `read_mesh_list_file "$JAPAN_MESH_LIST" '' JAPAN_CODES`、北方領土除外メッシュリストを `read_mesh_list_file "$DATA_DIR/boundaries/nt_excluded_meshes.txt" "<5.1.4 の除外リストの案内>" EXCLUDED_CODES` で読む（この順。[HLD 4.23.2](30_HLD.md#4232-処理の流れ)の「取得完了の記録の検査」の「除外メッシュリストが無いときは CMP1 の実行を案内する」）。

###### list_required_meshes

`list_required_meshes`。入れるもの: `REQUIRED_CODES`（HLD 4.23.2 の「取得完了の記録の検査」の表）。

- `PHASE` が空か `2` で `MESH_GIVEN` が 0 なら、`JAPAN_CODES` のうち `EXCLUDED_CODES` に無いもの。
- `PHASE` が空か `2` で `MESH_GIVEN` が 1 なら、`MESH_ARG_CODES` のうち `JAPAN_CODES` にあり、`EXCLUDED_CODES` に無いもの（警告は出さない。HLD 4.23.2 の「CMP3 は警告を出さない」）。
- `PHASE` が `3` か `4` なら、上の 1 つ目と同じ。

###### fetch_record_path（bash）

`fetch_record_path`。`FETCH_RECORD_PATH="$DATA_DIR/tiles/$FETCH_RECORD_NAME"` を入れる。ファイルの有無は見ない。

###### check_fetch_record

`check_fetch_record`（受け取るものは `FETCH_RECORD_PATH` と `REQUIRED_CODES`）。誤りがあれば、メッセージを `PRECOND_WHAT`・`PRECOND_ACTION` に足す（下の `check_preconditions` がまとめて出す）。記録の書式は[2.3](#23-ファイルの名前と書き方)。

1. 記録が無い（`[[ -e ]]` が偽）なら、`REQUIRED_CODES` のすべてを記録に無いコードとして FC1（記録が無い形）を足して戻る。要るメッシュが 0 件でも足す（[HLD 4.23.2](30_HLD.md#4232-処理の流れ)の「取得完了の記録の検査」の「2 つのリストと記録が無い・読めない・書式が違うときは、0 件でも止まる」、`CMP3-EXT1`）。0 件のときは FC1 の 0 件の形にする。
2. 読めないなら FC2 を足して戻る。ディレクトリ（`[[ -d ]]`）なら `{detail}` は `Is a directory`（bash では `: <dir` が失敗しないので、先に見る）、前置きの 6 の形の `: <` が失敗すれば `{detail}` はその理由。要るメッシュが 0 件でも同じ。
3. `rc=0; bad=$(LC_ALL=C grep -n -a -x -v -E -m 1 '[0123456789]{4}' -- "$FETCH_RECORD_PATH" | tr -d '\000') || rc=$?` で書式の違う行を探す。ただし最後の行の後の LF は数えないので、ファイルが空でなく最後の字が LF でないときも、最後の行は行として見る（`grep` はそう扱う）。空の行（ファイルの途中か、最後の LF の後にさらに LF がある）は書式違いになる。`rc` が 0 なら FC2（`{detail}` は `<番号> 行目が 4 桁の数字でない: <行>`）、2 以上なら FC2（`{detail}` は理由）を足して戻る。要るメッシュが 0 件でも同じ。
4. 記録の行を集合に読み（`while IFS= read -r` で、`_read_mesh_file` の 4 と同じく最後の行を落とさない）、`REQUIRED_CODES` のうち記録に無いコードがあれば、昇順に並べて FC1 を足す。要るメッシュが 0 件なら、ここでは何も足さない（記録と照らす検査を満たしたものとする。HLD 4.23.2 の「`--mesh` ありで要るメッシュが 0 件になったとき」。1〜3 の記録が無い・読めない・書式が違うときは、0 件でも止まっている）。

###### check_preconditions

`check_preconditions`（受け取るものは `PHASE`・`STAGE_N`・`DATA_DIR`・`REQUIRED_CODES`）。HLD 4.23.2 の「フェーズごとの起動前提条件」を確かめる。誤りは、配列 `PRECOND_WHAT`（`what`）と `PRECOND_ACTION`（`action`）に同じ添字で足していき、最後にまとめて出す（`check_fetch_record` も同じ 2 つの配列に足す）。

1. 次をこの順に見て、無ければ PC1 を足す（どれも `[[ -e "…" ]]` で有無だけを見る）: `PHASE` が `3` なら `"$DATA_DIR"/results/key_col_unresolved_peaks-$((STAGE_N - 1)).csv`、`PHASE` が `3` か `4` なら `"$DATA_DIR"/results/merged_peak.csv`、`PHASE` が `4` なら `"$DATA_DIR"/results/merged_peak.geojson`、`PHASE` が空か `4` なら `"$DATA_DIR"/ref/summitslist.csv`。
2. `PHASE` が空か `4` なら、`"$DATA_DIR"/ref/sota_updatelist_[0123456789][0123456789][0123456789][0123456789].xhtml` のグロブに合って `[[ -e "$f" ]]` が真のものが 1 つも無ければ PC2 を足す（`found=0; for f in <そのグロブ>; do if [[ -e "$f" ]]; then found=1; fi; done` で見る。合うものが無いとき、グロブはそのままの文字列になり `-e` が偽になる。`&&` で書くと、偽のときに `for` の終了状態が 1 になるので `if` で書く）。
3. `fetch_record_path` を呼び、`check_fetch_record` を呼ぶ。
4. 足したものがあれば、足した順に `log_error` で出して `exit "$EXIT_ERROR"`（何も消さない。全部を出してから 1 回だけ止まる）。
5. `PHASE` が空か `2` か `3` なら、`_run_child merge_peaks --check-land-peaks` を呼び（HLD 4.23.2 の 2「起動前提条件を検査する」、[DEC85](30_HLD.md#4234-設計判断)「CMP3 は陸地最高峰リストの書式を CMP5 で確かめる」）、`CHILD_RC` が 0 以外なら `exit "$CHILD_RC"`（何も消さない）。1〜4 で止まったときは起動しない（陸地最高峰リストの検査は、ほかの前提がそろってから行う）。

本体が `check_preconditions` を呼ぶ前に、`JAPAN_CODES`・`EXCLUDED_CODES` を読み（`read_mesh_list_file`。無い・読めない・誤りなら R1〜R3 でその場で 1 で止まる）、`list_required_meshes` を呼ぶ（HLD 3.3.3 の呼ぶ順）。

##### 段の進行

###### _run_child

`_run_child <名前> <引数…>`（内部）。名前が `analyze_terrain` なら `"$ANALYZE_TERRAIN"`、それ以外なら `"$PYTHON" "$SCRIPTS_DIR/<名前>.py"` を、`--config "$CONFIG_PATH"` を先頭にして、残りの引数をそのままの順で付けて起動する（すべての内部の起動口に `--config <絶対パス>` を渡す。[HLD 2.4.5](30_HLD.md#245-内部引数)）。

1. PL6（`起動: <名前> <引数>`。引数は `--config` からの全部を `_quote` でつないだもの）を `log_info` で出す。
2. `CHILD_RC=0; ( trap - PIPE; exec <コマンド> ) 8>&- || CHILD_RC=$?`（サブシェルで SIGPIPE を既定に戻してから `exec` で起動する。前置きの 2。ログファイルの記述子 8 を閉じて起動する。起動口は自分のログファイルを持ち、`run_pipeline` のログには書かない。[HLD 5.7.2](30_HLD.md#572-処理の流れ)の 6。ロックの記述子 9 は閉じない）。
3. PL7（`起動口の終了: <名前> 終了コード <CHILD_RC>`）を `log_info` で出す。

起動口の実行ファイルが無いときは、bash が 127 を返し、`CHILD_RC` が 127 になる（呼ぶ側は 0・3・4 以外として、その値で止まる）。

###### clear_outputs

`clear_outputs <2|3|4> [<N>]`。[HLD 2.10.3](30_HLD.md#2103-フェーズのやり直し)の表のとおりに消す。消すのは `$DATA_DIR/results/` と `$DATA_DIR/images/` の下だけ。

- 広域の N（`n` は、段が 2 なら 4〜6、段が 3 なら `N`〜6）ごとのグロブ（前置きの 4 のとおり、変数の部分だけを囲む）: `"$DATA_DIR"/results/csv/"$n"-[0123456789][0123456789][0123456789][0123456789]-[NS][EW].csv`、同じ名前の `.meshset`、`"$DATA_DIR"/images/"$n"-[0123456789][0123456789][0123456789][0123456789]-[NS][EW]_terrain.png`（解析識別子 `<N>-<対象メッシュコード>-<コーナー>` とコーナー NW・NE・SW・SE。[FR-014](20_SRS.md#fr-014-広域結合解析オーケストレーション)・[FR-015](20_SRS.md#fr-015-標高地形図出力)と、[SRS 8.1](20_SRS.md#81-内部データ一覧)の No.8・13。通常の `3-<コード>` のファイルは合わない）。
- 未確定リスト: 段が 2 なら `key_col_unresolved_peaks-3.csv`〜`-6.csv`、段が 3 なら `-<N>.csv`〜`-6.csv`（`$DATA_DIR/results/` の直下）。
- 段が 2 なら `merged_peak.csv`・`merged_peak.geojson`。どの段も `merged_summit.geojson`・`merged_summit.xlsx`・`merged_viewer.html`・`merged_viewer_data.js`（どれも `$DATA_DIR/results/` の直下）。

グロブに合ったものと名前を書いたものを 1 つずつ、`if [[ -e "$f" || -L "$f" ]]; then` で `rm -f -- "$f"` を `err` に受けて動かし、失敗すれば CO1（`{path}` は `f`、`{reason}`）を `log_error` で出して `exit "$EXIT_ERROR"`（[HLD 2.5.5](30_HLD.md#255-書き込みの失敗)）。消し終えたら PL5（消した数）を `log_info` で出す。

###### run_merge

`run_merge <N> [<--mesh の値>]`。入れるもの: `SATISFY_RC`、`LAST_STAGE`・`LAST_RESULT`。

1. `N` が 4 以上なら、`$DATA_DIR/results/merged_peak.geojson` があれば消す（HLD 2.10.3 の[DEC79](30_HLD.md#2104-設計判断)「フェーズ3 ではピーク候補 GeoJSON を統合直前に消す」。消し方と失敗は `clear_outputs` と同じ。消したら PL5 の 1 件の形を出す）。
2. `_run_child merge_peaks`（2 つ目の引数があれば `--mesh <値>` を付ける）。`CHILD_RC` が 0 以外なら `exit "$CHILD_RC"`。
3. `_run_child merge_zones`（同じく `--mesh`）。0 以外なら `exit "$CHILD_RC"`。
4. `_run_child check_cols --n <N>`。`CHILD_RC` が 0 か 3 なら `SATISFY_RC="$CHILD_RC"`、それ以外なら `exit "$CHILD_RC"`（HLD 2.5.2 の「[FR-022](20_SRS.md#fr-022-コル充足判定) の呼び出しだけは終了コードを明示的に受け取る」。`_run_child` の `|| CHILD_RC=$?` がこの受け取りに当たる）。
5. `LAST_STAGE="$CURRENT_STAGE"`、`LAST_RESULT="充足判定の終了コード $SATISFY_RC"`、PL8 を `log_info` で出す。

###### run_normal_stage

`run_normal_stage`。`_run_child analyze_terrain --mode normal --japan-mesh-list "$JAPAN_MESH_LIST"`（`MESH_GIVEN` が 1 なら最後に `--mesh "$MESH_VALUE"`）。0 以外なら `exit "$CHILD_RC"`。`run_merge 3 "$MESH_VALUE"`（`MESH_GIVEN` が 0 なら 2 つ目を渡さない）。

###### run_wide_stage

`run_wide_stage <N>`。`_run_child analyze_terrain --mode wide --japan-mesh-list "$JAPAN_MESH_LIST" --n <N> --unresolved "$DATA_DIR/results/key_col_unresolved_peaks-$((N - 1)).csv"`（`--mesh` は渡さない。[HLD 2.4.3](30_HLD.md#243-メッシュ範囲)）。0 以外なら `exit "$CHILD_RC"`。`run_merge <N>`。

###### run_phase4

`run_phase4`。

1. `_run_child match_summits`。`CHILD_RC` が 4 なら、`LAST_STAGE`・`LAST_RESULT`（`突合の終了コード 4、ビューア生成は起動しない`）を入れて PL8 を出し、`$DATA_DIR/results/key_col_unresolved_peaks-6.csv` があれば PG3 を `log_warning` で出してから、`exit "$EXIT_DEFECT"`（HLD 2.5.2 の表、[HLD 4.23.3](30_HLD.md#4233-異常系)の「N=6 でも未確定が残った場合の不備ゲート」）。0 と 4 以外なら `exit "$CHILD_RC"`。
2. `_run_child generate_viewer`。`LAST_STAGE`・`LAST_RESULT`（`突合の終了コード 0、ビューア生成の終了コード <CHILD_RC>`）を入れて PL8 を出す。`CHILD_RC` が 0 以外なら `exit "$CHILD_RC"`。

PG3 の出し方の理由: HLD 4.23.3 の「N=6 でも未確定が残った場合の不備ゲート」の行は、不備ゲートの件数と列（[HLD 2.5.3](30_HLD.md#253-利用者向けのメッセージ)の「不備ゲート」の行。`match_summits` が出す）に加えて、手動解決の手順の案内を求める。CMP3 は CSV を読まない（PRE3）ので、不備の種類は見分けられない。`key_col_unresolved_peaks-6.csv` は、N=6 の段の始まりに消され、その段の充足判定で未確定が残ったときだけ作られる（[HLD 2.10.3](30_HLD.md#2103-フェーズのやり直し)、`clear_outputs`）ので、`match_summits` が 4 を返したときにこのファイルがあれば、N=6 でも未確定が残った状態の不備ゲートとみなして、`run_pipeline` が手動解決の手順を案内する（無ければ出さない）。件数と列は `match_summits` の不備ゲートのメッセージに任せる。

###### 本体

ファイルの末尾に、次の順に書く（[HLD 3.3.3](30_HLD.md#333-関数)の呼ぶ順、[HLD 2.2.3](30_HLD.md#223-コンポーネント間のデータの流れとインターフェース)の再解析の制御、HLD 2.5.2 の表）。「段を始める」は、`CURRENT_STAGE` に段の名前（`フェーズ2`・`フェーズ3 の N=<N>`・`フェーズ4`）を入れ、PL4 を `log_info` で出し、その段の `clear_outputs` を呼ぶことを指す（段の名前と PL4 は本体だけが出し、段の関数は出さない）。

1. `parse_args "$@"`、`resolve_paths`、`acquire_lock`、`open_log "$@"`。
2. `read_mesh_list_file`（日本全土、北方領土除外の順）、`list_required_meshes`、`check_preconditions`。
3. `PHASE` が空（通し）: フェーズ2 の段を始め（`clear_outputs 2`）、`run_normal_stage`。`n=3`。`SATISFY_RC` が 3 で `n` が 6 より小さいあいだ、`n=$((n + 1))`、フェーズ3 の N=`n` の段を始め（`clear_outputs 3 "$n"`）、`run_wide_stage "$n"` を繰り返す。続けてフェーズ4 の段を始め（`clear_outputs 4`）、`run_phase4`、`exit "$EXIT_OK"`（通しの終了コードはフェーズ4 の結果。`run_phase4` は 0 以外なら中で止まる）。
4. `PHASE` が `2`: フェーズ2 の段を始め、`run_normal_stage`。`SATISFY_RC` が 3 なら PG1 を `log_warning` で出して `exit "$EXIT_UNRESOLVED"`、0 なら PG2 を `log_info` で出して `exit "$EXIT_OK"`（[HLD 4.23.3](30_HLD.md#4233-異常系)の「単独起動で未確定あり」「単独起動で未確定なし」）。
5. `PHASE` が `3`: フェーズ3 の N=`STAGE_N` の段を始め、`run_wide_stage "$STAGE_N"`。後は 4 と同じ。
6. `PHASE` が `4`: フェーズ4 の段を始め、`run_phase4`、`exit "$EXIT_OK"`。

#### 5.1.4 メッセージ文面

書き方は[2.2](#22-ログとメッセージの文面)。ロックとログの場面（G1〜G6。`{config_path}` は `CONFIG_PATH`）と取得完了の記録の誤り（FC2。`{detail}` は `{reason}` か `{line_no} 行目が 4 桁の数字でない: {line}`）は 2.2、`--mesh` とリストの誤り（A1〜A5・R1〜R3）は[2.1.4](#214-メッセージ文面)の文面を、bash でも同じに出す。L1・L3 は 2.2（`{program}` は `run_pipeline`）。`{reason}` は[5.1.3](#513-関数の細部)の規約の 6、`{path}` は絶対パス、`{value}`・`{arg}`・`{output}` は `_quote` で引用した値、`{args}` は各引数を `_quote` して空白 1 つでつないだもの。G7（捕まらなかった例外）は bash には無い。

`ERROR:`・`WARNING:` のメッセージ（2 行目は `対処:` と空白 1 つの後）:

| 記号 | 場面 | 1 行目 | 2 行目 | 終了コード |
|---|---|---|---|---|
| PA1 | 受け付けない引数 | `run_pipeline の知らない引数: {arg}` | `使える引数は --config・--phase・--n・--mesh・--help（scripts/run_pipeline.sh --help で使い方を出す）` | 2 |
| PA2 | 値が無い | `{option} の値が無い` | `{option} の後に値を書く（scripts/run_pipeline.sh --help で使い方を出す）` | 2 |
| PA3 | 値が違う | `{option} の値が違う: {value}` | `--config は空でないパス、--phase は 2・3・4 のどれか、--n は 4・5・6 のどれかを渡す` | 2 |
| PA4 | 同じ名前を 2 回 | `{option} を 2 回渡した` | `{option} は 1 回だけ渡す` | 2 |
| PA5 | 組み合わせの誤り | `--phase 3 に --n が無い`、`--n は --phase 3 のときだけ使える`、`--mesh は --phase {phase} と一緒に使えない` のどれか | 1 つ目は `--phase 3 には --n 4・5・6 のどれかを付ける`、2 つ目は `--n を外すか、--phase 3 にする`、3 つ目は `--mesh は通しの実行か --phase 2 で使う（--phase 3・4 は日本全土を対象にする）` | 2 |
| RS1 | 設定解決の出力が 2 行の形でない | `設定解決の出力が 2 行の形でない: {output}`（`{output}` は受け取った標準出力の全体〈最後に足した `.` を除いたもの〉を 1 つの文字列として `_quote` したもの。改行があれば、`log_error` の決まりで行が分かれる） | `プログラムの欠陥として起票して調べる（resolve_config が終了コード 0 で、data_dir= と log_dir= の 2 行のほかの形を出した）` | 1 |
| PC1 | 起動前提条件のファイルが無い | `起動前提条件のファイルが無い: {path}` | ファイルごとに次の文（下の PC1 の 2 行目の表） | 1 |
| PC2 | 山岳データ登録変更リストが無い | `山岳データ登録変更リストが無い: {ref_dir}/sota_updatelist_YYYY.xhtml（YYYY は半角の数字 4 桁）` | `入手の入口のページ（https://little-ctc.com/sota_hp/）から年のページをブラウザで保存し、{ref_dir} の直下に sota_updatelist_YYYY.xhtml の名前で置いてから、もう一度起動する（保存のときに「ウェブページ、完全」などで別の名前にならないようにする）` | 1 |
| FC1 | 取得完了の記録に無いメッシュがある | 記録が無いときは `取得完了の記録が無い: {path}（要るメッシュ {count} 件: {codes}）`（要るメッシュが 0 件なら `取得完了の記録が無い: {path}`）、あるときは `取得完了の記録に無いメッシュがある: {path}（{count} 件: {codes}）`（`{codes}` は昇順に空白 1 つでつないだもの。全部を並べる） | `venv/bin/python3 scripts/fetch_tiles.py{config_opt} を --mesh なしで起動して取得を終えてから、もう一度起動する（足りないメッシュだけを取るなら、それらを --mesh で指定する）` | 1 |
| CO1 | 前回の出力を消せない | `前回の出力を消せない: {path}: {reason}` | `{path} とそのディレクトリの権限を確かめてから、もう一度起動する` | 1 |
| PG1 | 単独起動で未確定あり（`WARNING:`） | `未確定のピークが残った: {path}`（`{path}` は `$DATA_DIR/results/key_col_unresolved_peaks-<N>.csv`） | N<6 なら `次に scripts/run_pipeline.sh --phase 3 --n {N+1}{config_opt} を起動する`、N=6 なら `次に scripts/run_pipeline.sh --phase 4{config_opt} を起動する`。`--phase 2` に `--mesh` を付けたときは、続けて `。--phase 3 には日本全土の取得完了が要る（範囲を絞った確認は通しの実行で行う）` | 3 |
| PG3 | N=6 でも未確定が残った不備ゲート（`WARNING:`） | `N=6 でも未確定のピークが残っている: {path}`（`{path}` は `$DATA_DIR/results/key_col_unresolved_peaks-6.csv`。PG1 と同じ形） | `merged_summit.xlsx の is_key_col_unresolved の行でピークを確かめる。島の最高峰で Key コルが海面にあたるなら、緯度経度を merged_summit.xlsx から桁を落とさずに写して、陸地最高峰リストの保守として足し、足した版を params/land_highest_peaks.csv に取り込んでから、scripts/run_pipeline.sh --phase 3 --n 6{config_opt}、scripts/run_pipeline.sh --phase 4{config_opt} の順に起動する。島の最高峰でなければ解析の欠陥として起票し、リストに足さない`（[HLD 4.23.2](30_HLD.md#4232-処理の流れ)の「N=6 でも未確定が残ったとき」の 1〜4 の要約） | 4 |

`{config_opt}` は、`--config` を渡されたとき（`CONFIG_GIVEN=1`）は空白 1 つと `--config` と空白 1 つと `CONFIG_PATH` を `_quote` したもの、渡されなかったときは空。`{option}` は `--config` などの名前。`{phase}` は `PHASE`。`{ref_dir}` は `$DATA_DIR/ref`。

PC1 の 2 行目（足りないファイルごと。`対処:` と空白 1 つの後）:

| 足りないファイル | 2 行目 |
|---|---|
| `key_col_unresolved_peaks-<N−1>.csv`（`--phase 3 --n <N>`） | N−1 が 3 なら `先に scripts/run_pipeline.sh --phase 2{config_opt} を起動する。前の段で未確定のピークが無ければ、このファイルは作られない。そのときは --phase 3 は要らず、--phase 4 を起動する`。4 以上なら `先に scripts/run_pipeline.sh --phase 3 --n {N−1}{config_opt} を起動する。前の段で未確定のピークが無ければ、このファイルは作られない。そのときは --phase 3 は要らず、--phase 4 を起動する`（先頭の起動の指示だけが違い、続く 2 文は同じ） |
| `merged_peak.csv`・`merged_peak.geojson` | `先に scripts/run_pipeline.sh --phase 2{config_opt} を起動する（通しの実行でもよい）` |
| `summitslist.csv` | `SOTA サミットリスト CSV を https://www.sotadata.org.uk/summitslist.csv から入手して {path} に置いてから、もう一度起動する` |

北方領土除外メッシュリストの案内（`read_mesh_list_file` に渡す R1〜R3 の `対処:`）: `venv/bin/python3 scripts/preprocess_boundaries.py{config_opt} を起動して北方領土除外メッシュリストを作ってから、もう一度起動する`（`{config_opt}` は上の `ERROR:`・`WARNING:` の表の後の段落のとおり）。

通常のログに出す行（`log_info` で標準出力とログファイルに出す）:

| 記号 | 行 | 文面 |
|---|---|---|
| PG2 | 単独起動で未確定なし | `未確定のピークは無い。次に scripts/run_pipeline.sh --phase 4{config_opt} を起動する`。`--phase 2` に `--mesh` を付けたときは、続けて `。--phase 4 には日本全土の取得完了が要る（範囲を絞った確認は通しの実行で行う）` |
| PL1 | 起動のしかた | `起動のしかた: 通し`、`起動のしかた: --phase 2`、`起動のしかた: --phase 3 --n {N}`、`起動のしかた: --phase 4` のどれか |
| PL2 | データ置き場 | `データ置き場: {data_dir}`（`DATA_DIR` のまま） |
| PL3 | ログの置き場 | `ログの置き場: {log_dir}`（`LOG_DIR` のまま） |
| PL4 | 段の始まり | `段の始まり: {stage}`（`{stage}` は `フェーズ2`・`フェーズ3 の N={N}`・`フェーズ4`） |
| PL5 | 前回の出力を消した | 段の始まりは `前回の出力を {count} 件消した`、`run_merge` の 1 は `統合の前に {path} を消した` |
| PL6 | 内部の起動口の起動 | `起動: {name} {args}` |
| PL7 | 内部の起動口の終わり | `起動口の終了: {name} 終了コード {rc}`（終わりの行 L3 の `終了:` と見分けるため） |
| PL8 | 段の終わり | `段の終わり: {stage}（{result}）`（`{result}` は `run_merge` の 5 と `run_phase4` の文） |
| PL9 | 結果の要約 | 段を始める前に止まった（`CURRENT_STAGE` も `LAST_STAGE` も空）: `結果の要約: 段を始める前に止まった`。段の途中で止まった（`CURRENT_STAGE` が空でなく `LAST_STAGE` と違う）: `結果の要約: {current} の途中で止まった。最後に終えた段: {last}（{result}）`（`LAST_STAGE` が空なら `。最後に終えた段: なし`）。それ以外: `結果の要約: 最後に終えた段: {last}（{result}）`（[HLD 5.7.2](30_HLD.md#572-処理の流れ)の 7「結果の要約」の `run_pipeline` の行） |

使い方の文（`--help`。標準出力に、次の行をこのまま出す。最後の行の後にも LF を付ける）:

```text
使い方: scripts/run_pipeline.sh [--config <パス>] [--phase 2|3|4] [--n 4|5|6] [--mesh <値>]
       scripts/run_pipeline.sh --help

解析パイプライン（フェーズ2〜4）を動かす。--phase を省くと、フェーズ2 から 4 までを通しで行う。

  --config <パス>  設定ファイル（省くとソースツリーの params/config.ini）
  --phase 2|3|4    1 つの段だけを行う（2: 通常の解析・統合・充足判定、3: --n の広域解析・統合・充足判定、4: 突合とビューアの生成）
  --n 4|5|6        --phase 3 の広域解析の N（--phase 3 のときだけ、必ず付ける）
  --mesh <値>      4 桁のメッシュコードか、メッシュコードを 1 行 1 件で書いたファイルのパス（通しと --phase 2 だけ）
  --help           この使い方を出して終わる
```

記録に無いメッシュを全部並べる理由: [HLD 4.23.1](30_HLD.md#4231-目的と範囲)の対象外の行が LLD に送った「記録に無いメッシュをメッセージに何件まで並べるか」は、全部（最大で日本全土の 175 件）とする。利用者が足りないメッシュを `--mesh` のファイルに写せるようにするため。

#### 5.1.5 UT 候補

すべて自動。どのケースも、下の共通の準備の「一時のソースツリー」の `scripts/run_pipeline.sh` を子のプロセスで起動し、終了コード、標準出力、標準エラー出力、ログファイル、スタブの記録、`data_dir` の下のファイルを確かめる。内部の起動口はスタブにする（`run_pipeline` が起動口に渡す引数と、起動口の終了状態の受け方を確かめるため。起動口の中身は各モジュールの UT と IT で確かめる）。ログファイルの行の期待は、先頭の時刻と空白を除いた文面で書く。止まるケースの「何も消さない」は、共通の準備の「前回の出力」がすべて残っていること。表の準備・入力の列に (a)(b)… や (i)(ii)… と並べたものは、それぞれ別の起動で、別の `<tmp>` を新しく作って行う（前の起動の `<tmp>` を引き継がない）。準備の列に書いた準備は、どの起動にも行う。「(d) (a) に `--mesh 5339` を足す」のように別の入力を参照するものは、その入力の準備を引き継ぐ。

共通の準備:

- **起動口の記録**: スタブの記録は `resolve_config` の記録も含めて通し番号が付く。「起動口の記録」は、そのうち `resolve_config` の記録を除いたもので、番号の順に数える。表の「起動口の記録が無い」は、`resolve_config` のほかに記録が無いこと。「スタブの記録が無い」は、`resolve_config` を含めて記録が無いこと（設定解決より前に止まるケース）。
- **一時のソースツリー**: ケースごとに一時のディレクトリ `<tmp>` を作り、`<tmp>/src/scripts/run_pipeline.sh` にテストする `scripts/run_pipeline.sh` を写す（シンボリックリンクにしない。リンクだと `readlink -f` でリポジトリのソースツリーに戻るため）。`<tmp>/src/venv/bin/python3` と `<tmp>/src/build/analyze_terrain` に、下の「スタブ」を同じ中身で置く。`<tmp>/src/params/mesh_list_japan.txt` は `5339\n5340\n6841\n`。どれも実行の権限を付ける。作業ディレクトリは `<tmp>/work`（作る）。
- **スタブ**: bash のスクリプト。`basename "$0"` が `python3` なら、1 つ目の引数のファイル名から `.py` を除いたものを名前に、2 つ目からを引数にする。それ以外なら名前は `analyze_terrain`、引数はすべて。環境変数 `STUB_DIR`（`<tmp>/stub`）の下で次を行う。
  1. 通し番号（`$STUB_DIR/seq` の数に 1 を足したもの）を `k` とし、`$STUB_DIR/calls/<k>.args` に名前と引数を NUL で区切って書き、`$STUB_DIR/calls/<k>.info` に 3 行を書く: 作業ディレクトリ（`pwd -P`）、ロック（`"$STUB_DATA_DIR/findsummits.lock"` が無ければ `nofile`〈`flock` を動かさない。`flock` は無いファイルを作るので、ロックの前に動く `resolve_config` のスタブがロックファイルを作らないようにする〉、あれば `flock -n -E 73 "$STUB_DATA_DIR/findsummits.lock" true` が 73 なら `locked`、0 なら `unlocked`。`STUB_DATA_DIR` は環境変数で、ケースが `data_dir` を変えたときはその値にする）、記述子 8 が開いているか（`[[ -e /proc/self/fd/8 ]]` なら `fd8-open`、偽なら `fd8-closed`）。続けて `$STUB_DIR/calls/<k>.files` に、`$STUB_DATA_DIR/results` と `$STUB_DATA_DIR/images` の下のファイルの、`$STUB_DATA_DIR` からの相対パスを 1 行ずつ書く（呼ばれた時点で残っているもの）。
  2. `$STUB_DIR/<名前>.rcs` があれば、その名前の何回目の呼び出しか（`$STUB_DIR/<名前>.count`）の行の数を終了コードにする（無いか行が足りなければ 0）。
  3. 名前が `resolve_config` なら、`$STUB_DIR/resolve_config.out` の中身をそのまま標準出力に出す。それ以外の名前で `$STUB_DIR/<名前>.say` があれば、その中身をそのまま標準出力と標準エラー出力に 1 回ずつ出す（無ければ何も出さない）。
  4. `$STUB_DIR/<名前>.wait` があれば、`$STUB_DIR/<名前>.started` を作り、`$STUB_DIR/release` ができるまで 0.1 秒ずつ待つ。
  5. 2 の終了コードで終わる。
- **一時の設定**: `<tmp>/data`（`STUB_DATA_DIR`）と `<tmp>/logs` を `resolve_config.out` に `data_dir=<tmp>/data\nlog_dir=<tmp>/logs\n` で書く（ケースが書かなければ）。`<tmp>/data` に `boundaries/nt_excluded_meshes.txt`（`6841\n`）、`tiles/fetch_complete.txt`（`5339\n5340\n`）、`ref/summitslist.csv`（空）、`ref/sota_updatelist_2026.xhtml`（空）を置く。`--phase 3`・`--phase 4` で起動するケースは、準備の列がそのファイルを消す・置かないと書いたものを除いて、`results/merged_peak.csv`・`results/merged_peak.geojson`・`results/key_col_unresolved_peaks-3.csv`〜`-5.csv`（空）も置く。
- **前回の出力**: 段の始まりの削除と「何も消さない」を確かめるケースは、`<tmp>/data` に次を空のファイルで置く: `results/csv/3-5339.csv`・`3-5339.geojson`・`3-5339.meshset`、`images/3-5339_terrain.png`、N=4・5・6 のそれぞれの `results/csv/<N>-5339-NW.csv`・`<N>-5339-SE.meshset`、`images/<N>-5339-NE_terrain.png`、`results/key_col_unresolved_peaks-3.csv`〜`-6.csv`、`results/merged_peak.csv`・`merged_peak.geojson`・`merged_summit.geojson`・`merged_summit.xlsx`・`merged_viewer.html`・`merged_viewer_data.js`。
- **時刻の固定**: ログファイルの名前の時刻を決めるケース（`UT-run_pipeline-13`）は、`<tmp>/fakebin/date` に、引数が `+%Y%m%dT%H%M%S` のときだけ `20260101T000000` を出し、それ以外は `/usr/bin/date` にそのまま渡す bash のスクリプトを置き、環境の `PATH` の先頭に `<tmp>/fakebin` を足して起動する。
- **起動**: `subprocess.run([<tmp>/src/scripts/run_pipeline.sh, *<引数>], cwd=<tmp>/work, env=<親の環境に STUB_DIR と STUB_DATA_DIR を足したもの>, capture_output=True)`。シグナルを送るケースは `subprocess.Popen` で、`start_new_session=True` にする。

##### 起動と準備（UT 候補）

| ID | 確かめること | 準備 | 入力 | 期待 |
|---|---|---|---|---|
| `UT-run_pipeline-01` | 使い方 | 一時のソースツリー | (i) `--help`、(ii) `--phase 2 --help --foo`、(iii) `--foo --help` | (i)(ii) は 0、標準出力が[5.1.4](#514-メッセージ文面)の使い方の文と等しい、スタブの記録が無い（設定解決を起動しない）、`<tmp>/data/findsummits.lock` が無い。(iii) は 2 で PA1（`--foo`） |
| `UT-run_pipeline-02` | 引数の誤り | 一時のソースツリーと一時の設定と前回の出力 | それぞれ: `x`、`--foo`、`--`、`--phase`、`--phase 1`、`--n 4`、`--phase 3`、`--phase 3 --n 7`、`--phase 4 --mesh 5339`、`--phase 2 --phase 2`、`--phase 2 --phase`、`--config ''`、`--help=1` | どれも 2、標準出力は空、スタブの記録が無い、ロックファイルが無い、何も消さない。メッセージはこの順に PA1（`x`）・PA1（`--foo`）・PA1（`--`）・PA2（`--phase`）・PA3（`--phase`、`1`）・PA5 の 2 つ目・PA5 の 1 つ目・PA3（`--n`、`7`）・PA5 の 3 つ目（`{phase}` は `4`）・PA4（`--phase`）・PA4（`--phase`。最後に値が無くても PA2 でない）・PA3（`--config`、`''`）・PA1（`--help=1`） |
| `UT-run_pipeline-03` | 設定ファイルのパスと引数の書き方 | 一時のソースツリーと一時の設定。`resolve_config.rcs` を `2` にする（設定解決で止める） | (i) 引数なし、(ii) `--config cfg.ini`、(iii) `--config=/x/y.ini`、(iv) `--config --help` | どれも 2。`resolve_config` の記録の引数が、(i) `--config <tmp>/src/params/config.ini`、(ii) `--config <tmp>/work/cfg.ini`、(iii) `--config /x/y.ini`、(iv) `--config <tmp>/work/--help` |
| `UT-run_pipeline-04` | `--mesh` を読み、そのまま渡す | 一時のソースツリーと一時の設定。`<tmp>/work/m.txt` に `MV-02` の中身 | `--phase 2 --mesh m.txt` | 0。`analyze_terrain`・`merge_peaks`・`merge_zones` の引数の最後が `--mesh m.txt`（受け取ったまま。絶対パスにしない）。どの記録の作業ディレクトリも `<tmp>/work` |
| `UT-run_pipeline-05` | Python と共通のテストベクトル | 一時のソースツリーと一時の設定。[2.1.3](#213-関数の細部)のメッシュの読み方のテストベクトルの中身ごとに `<tmp>/work/v.txt` を書く（別々の起動）。日本全土のリストを同じ中身にしたケースも別に起動する（`<tmp>/src/params/mesh_list_japan.txt` を差し替える） | (a) `--phase 2 --mesh v.txt`、(b) 引数なし（日本全土のリストを差し替えた方） | (a)(b) とも、テストベクトルの結果が空でない集合なら、取得完了の記録を空のファイルにして起動し、1 で FC1（あるときの形）の `{count}`・`{codes}` が表の集合と等しい（読んだ集合を外から見るため。表の集合のコードはどれも日本全土のリストにあり、除外リストに無い）。(a) 集合が空のケースは 2 で A5。誤りの行は 2 で A4（`{line_no}`・`{line}` が表のとおり。NUL を含む行は `{line}` を見ない）。UTF-8 として読めないものは 2 で A3（`{reason}` は `UTF-8 として読めない`）。(b) 誤りは 1 で R3・R2、空の集合は止まらない（共通の準備の記録のまま。要るメッシュが 0 件） |
| `UT-run_pipeline-06` | `--mesh` のファイルの誤りのほか | 一時のソースツリーと一時の設定と前回の出力。`<tmp>/work/d` にディレクトリ | それぞれ: `--mesh ''`、`--mesh none.txt`、`--mesh d`、`--mesh 533` | どれも 2、スタブの記録が無い、何も消さない。A1、A2（`{path}` は `<tmp>/work/none.txt`）、A3（`{reason}` は `Is a directory`）、A2（`533` はパスとして読む） |
| `UT-run_pipeline-07` | 設定解決が 0 以外を返す | 一時のソースツリーと一時の設定と前回の出力 | `resolve_config.rcs` を `1`・`2`・`5` にして、それぞれ引数なし | 終了コード 1・2・5、ロックファイルが無い、`<tmp>/logs` が無い、何も消さない、スタブの記録は `resolve_config` の 1 回だけ |
| `UT-run_pipeline-08` | 設定解決の出力の形 | 一時のソースツリーと一時の設定と前回の出力 | `resolve_config.out` をそれぞれ: (a) 正しい 2 行の後に `x\n`、(b) `data_dir=<tmp>/data\n` だけ、(c) `data_dir=data\nlog_dir=<tmp>/logs\n`、(d) `data_dir=\nlog_dir=<tmp>/logs\n`、(e) 正しい 2 行の最後の LF なし、(f) `data_dir=` の行を 2 回、(g) 各行の LF の前に CR、(h) 正しい 2 行の後に空の行、(i) `data_dir=<tmp>/da` と NUL と `ta\nlog_dir=<tmp>/logs\n`、(j) `data_dir=<tmp>/data` と NUL と `log_dir=<tmp>/logs\n`（行の区切りの LF の代わりに NUL） | どれも 1、標準エラー出力に RS1（`{output}` は受け取った全体）、ロックファイルが無い、`<tmp>/logs` が無い、何も消さない |
| `UT-run_pipeline-09` | 設定解決の値を文字列のまま使う | 一時のソースツリーと一時の設定。`data_dir` を `<tmp>/a b/$(touch <tmp>/evil)/x=y` にして、そのディレクトリに一時の設定の `data_dir` のファイルを置く。`resolve_config.out` は `log_dir=<tmp>/l g\ndata_dir=<その値>\n`（順を入れ替える） | `--phase 4` で `results/merged_peak.csv` を置かない | 1（PC1 の `merged_peak.csv` だけ。PC2 は出ない）、`<tmp>/evil` が無い、ロックファイルがそのディレクトリの下にある、`<tmp>/l g` の下にログファイルがある |
| `UT-run_pipeline-10` | 同時起動 | 一時のソースツリーと一時の設定と前回の出力。テストのプロセスが `<tmp>/data/findsummits.lock` を開いて `fcntl.flock(LOCK_EX)` を持つ | 引数なし | 1、標準エラー出力に G1（`{lock_path}` は `<tmp>/data/findsummits.lock`）、`<tmp>/logs` にログファイルが無い、何も消さない |
| `UT-run_pipeline-11` | ロックファイルを開けない | 一時のソースツリー。`resolve_config.out` の `data_dir` を無いディレクトリ `<tmp>/nodata` にする | 引数なし | 1、G2、ログファイルが無い |
| `UT-run_pipeline-12` | ログの出力先を用意できない | 一時のソースツリーと一時の設定と前回の出力。`<tmp>/logs` に通常のファイルを置く | 引数なし | 1、標準エラー出力に G3（`{path}` は `<tmp>/logs`、`{config_path}` は `<tmp>/src/params/config.ini`）、標準出力は空、何も消さない |
| `UT-run_pipeline-13` | 同じ名前のログファイル | 一時のソースツリーと一時の設定。共通の準備の「時刻の固定」。子を `bash -c 'mkdir -p <tmp>/logs; printf old > "<tmp>/logs/run_pipeline_20260101T000000_$$.log"; exec <tmp>/src/scripts/run_pipeline.sh'` で起動する（`exec` で PID が変わらない） | なし | 1、G4、置いたファイルの中身は `old` のまま |
| `UT-run_pipeline-14` | ログファイルの始まりと終わり | 一時のソースツリーと一時の設定 | `--phase 2 --mesh 5339 --config <tmp>/c.ini` に、別の起動で `--phase=2 --mesh "a b'c"` のファイル（中身 `5339`）を渡す | 0。ログファイルの名前が `run_pipeline_<YYYYMMDDTHHMMSS>_<PID>.log`、最初の行が L1（引数は `_quote` のとおり。2 つ目の起動は `開始: run_pipeline --phase=2 --mesh 'a b'"'"'c'`）、続けて PL1（`起動のしかた: --phase 2`）・PL2・PL3、各行の頭に時刻（`^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}` と空白 1 つ）、標準出力に同じ文面が時刻なしで出る、最後の 2 行が PL9 と L3（終了コード 0、所要時間が小数 3 桁）、L2 の行（`設定ファイル:`・`設定:`）が無い |
| `UT-run_pipeline-15` | 始まりの行の引数の改行 | 一時のソースツリーと一時の設定。`<tmp>/work` に、名前が `x`・改行・`y` のファイル（中身 `5339`） | `--phase 2 --mesh <そのファイルの名前>` | ログファイルの最初の 2 行が `開始: run_pipeline --phase 2 --mesh 'x` と `y'`（2 行目にも時刻） |
| `UT-run_pipeline-16` | ログファイルに書けなくなった | 一時のソースツリーと一時の設定。子を `bash -c 'trap "" XFSZ; ulimit -f 1; exec <tmp>/src/scripts/run_pipeline.sh'` で起動する（ログファイルが 1024 バイトを超えたところで書き込みが `EFBIG` になる） | なし（通し。`check_cols.rcs` を `3\n3\n3\n3` にして行を増やす） | 1、標準エラー出力に G5 が 1 回、ログファイルの最後の行が L3 でない |

終わりの行だけを書けなかったとき（G6）は UT にしない: Python の 2.1 はファイルの物を差し替えて起こせたが、bash の記述子 8 への書き込みは外から 1 つだけ失敗させられない。`ulimit -f` の境目は 1024 バイトずつで、L3 だけに当てられない。`_on_exit` の 5 を読んで確かめる。

##### 起動前提条件（UT 候補）

| ID | 確かめること | 準備 | 入力 | 期待 |
|---|---|---|---|---|
| `UT-run_pipeline-17` | 要るメッシュと記録 | 一時のソースツリーと一時の設定と前回の出力 | (i) `--phase 2`、(ii) 記録を `5339\n` にして `--phase 2`、(iii) 記録を `5339\n` にして `--phase 2 --mesh` に `5339`・`1234`・`6841` を書いたファイル、(iv) 記録を `5339\n` にして `--phase 2 --mesh 1234`、(v) 記録を `5339\n` にして `--phase 4`、(vi) 記録を `5339\n` にして `--phase 2 --config <tmp>/c.ini`（`resolve_config.out` は既定のまま） | (i)(iii)(iv) は前提を通る（`merge_peaks --check-land-peaks` が起動される）。(ii)(v)(vi) は 1、FC1（あるときの形、`1 件: 5340`）、何も消さない、起動口の記録が無い。(ii) の FC1 の 2 行目は `venv/bin/python3 scripts/fetch_tiles.py を` で始まり、(vi) は `venv/bin/python3 scripts/fetch_tiles.py --config <tmp>/c.ini を` で始まる |
| `UT-run_pipeline-18` | 記録が無い・読めない・書式が違う | 一時のソースツリーと一時の設定と前回の出力 | `--phase 2` で、記録を (a) 置かない、(b) ディレクトリにする、(c) `5339\n53a9\n`、(d) `5339\n\n`、(e) `5339\r\n`、(f) `5339\n5340`（最後の LF なし）、(g) 空のファイルにして `--phase 2 --mesh 1234`、(h) 置かずに `--phase 2 --mesh 1234`、(i) ディレクトリにして `--phase 2 --mesh 1234`、(j) ディレクトリにして `--phase 2 --config <tmp>/c.ini`（`resolve_config.out` は既定のまま） | (a) 1 で FC1（無いときの形、`2 件: 5339 5340`）。(b) 1 で FC2（`Is a directory`）。(c) 1 で FC2（`2 行目が 4 桁の数字でない: 53a9`）。(d)(e) 1 で FC2。(f)(g) は前提を通る。(h) 1 で FC1（要るメッシュが 0 件の形）、(i) 1 で FC2（要るメッシュが 0 件でも止まる）。(j) 1 で FC2、2 行目が `{path} を消してから、venv/bin/python3 scripts/fetch_tiles.py --config <tmp>/c.ini を` で始まる（`{path}` は記録のパス）。止まるものはどれも何も消さない |
| `UT-run_pipeline-19` | リストが無い・誤り | 一時のソースツリーと一時の設定と前回の出力 | `--phase 2` で (a) 除外リストを消す、(b) 日本全土のリストを消す、(c) 除外リストを `68x1\n` にする、(d) 一時の設定のファイルを `<tmp>/real` の下に置き（`<tmp>/data` には置かない）、`<tmp>/real/x` を作り、`<tmp>/link` に `<tmp>/real/x` へのシンボリックリンクを置き、`data_dir`（`resolve_config.out` と `STUB_DATA_DIR`）を `<tmp>/link/..` にする、(e) (d) と同じ準備で `<tmp>/real/boundaries/nt_excluded_meshes.txt` を消す、(f) 除外リストを消して `--phase 2 --config <tmp>/c.ini`（`resolve_config.out` は既定のまま） | (a)(b)(c)(e)(f) は 1、何も消さない。(a) R1 で `対処:` が[5.1.4](#514-メッセージ文面)の除外リストの案内（`--config` を渡していないので `{config_opt}` は空）。(f) R1 で `対処:` が `venv/bin/python3 scripts/preprocess_boundaries.py --config <tmp>/c.ini を` で始まる。(b) R1 で[2.1.4](#214-メッセージ文面)の既定の対処（`{path}` は `<tmp>/src/params/mesh_list_japan.txt`）。(c) R3。(d) 前提を通る（除外リストは渡されたパスのまま読むので、リンクの先の親 `<tmp>/real` の下を読む）。(e) R1 で `{path}` は `<tmp>/boundaries/nt_excluded_meshes.txt`（字の上で `..` を除いた値） |
| `UT-run_pipeline-20` | `--phase 3` の前提 | 一時のソースツリーと一時の設定と前回の出力 | (a) `key_col_unresolved_peaks-3.csv` を消して `--phase 3 --n 4`、(b) `-4.csv` を消して `--phase 3 --n 5`、(c) `merged_peak.csv` を消して `--phase 3 --n 4`、(d) `merged_peak.geojson` だけを消して `--phase 3 --n 4`、(e) `summitslist.csv` と登録変更リストを消して `--phase 3 --n 4` | (a)(b)(c) は 1 で PC1（(a) は PC1 の 2 行目の表の N−1=3 の文、(b) は `--phase 3 --n 4` の文）、何も消さない。(d)(e) は前提を通る |
| `UT-run_pipeline-21` | `--phase 4` と通しの前提 | 一時のソースツリーと一時の設定と前回の出力 | (a) `merged_peak.geojson` を消して `--phase 4`、(b) `summitslist.csv` を消して `--phase 4`、(c) `summitslist.csv` を消して通し、(d) 登録変更リストを消し、`ref/` に 年の数字が全角の `sota_updatelist_2026.xhtml`（数字のコードポイントは U+FF12・U+FF10・U+FF12・U+FF16）・`sota_updatelist_2026.xhtml.html`・`sota_updatelist_2026Xxhtml`・`sota_updatelist_202.xhtml` を置いて `--phase 4`、(e) (d) と同じ準備で通し、(f) 登録変更リストを `sota_updatelist_2025.xhtml` と `sota_updatelist_2026.xhtml` の 2 つにして `--phase 4` | (a)〜(e) は 1、何も消さない。(a)(b)(c) は PC1、(d)(e) は PC2（`{ref_dir}` は `<tmp>/data/ref`）。(f) は前提を通る |
| `UT-run_pipeline-22` | 誤りをまとめて出す | 一時のソースツリーと一時の設定と前回の出力。`merged_peak.csv`・`summitslist.csv`・登録変更リストを消し、記録を `5339\n` にする | `--phase 4` | 1、標準エラー出力に PC1（`merged_peak.csv`）・PC1（`summitslist.csv`）・PC2・FC1 がこの順に出て 1 回だけ止まる、`merge_peaks` を起動しない |
| `UT-run_pipeline-23` | 陸地最高峰リストの書式の検査 | 一時のソースツリーと一時の設定と前回の出力 | (a) 通し・`--phase 2`・`--phase 3 --n 4`・`--phase 4` で `merge_peaks.rcs` を `0`、(b) `--phase 2` で `merge_peaks.rcs` を `1`、(c) 同じく `2` | (a) 通し・2・3 は最初の起動口の記録が `merge_peaks --config <パス> --check-land-peaks`、`--phase 4` は `merge_peaks` を起動しない。(b)(c) は終了コード 1・2、何も消さない、その後の起動口の記録が無い |

##### 段の進行（UT 候補）

| ID | 確かめること | 準備 | 入力 | 期待 |
|---|---|---|---|---|
| `UT-run_pipeline-24` | フェーズ2 の段と単独起動の案内 | 一時のソースツリーと一時の設定と前回の出力 | (a) `--phase 2`、(b) `check_cols.rcs` を `3` にして `--phase 2`、(c) `check_cols.rcs` を `3` にして `--phase 2 --mesh 5339`、(d) `--phase 2 --mesh 5339`、(e) `check_cols.rcs` を `3` にして `--phase 2 --config <tmp>/c.ini`（`resolve_config.out` は既定のまま） | 起動口の記録の順は `merge_peaks`（`--check-land-peaks`）・`analyze_terrain`（`--config <パス> --mode normal --japan-mesh-list <tmp>/src/params/mesh_list_japan.txt`、(c)(d) は最後に `--mesh 5339`）・`merge_peaks`・`merge_zones`（(c)(d) は `--mesh 5339`）・`check_cols --config <パス> --n 3`。`analyze_terrain` の時点の `.files` に、[HLD 2.10.3](30_HLD.md#2103-フェーズのやり直し)のフェーズ2 の行のファイルが無く、通常の `3-5339.*` と `images/3-5339_terrain.png` が残る。(a) 0 で PG2、(b) 3 で PG1（N<6 の文、`{path}` は `key_col_unresolved_peaks-3.csv`）、(c) 3 で PG1 に `--mesh` の文が続く、(d) 0 で PG2 に `--mesh` の文が続く、(e) 3 で PG1 の次の起動の文に空白 1 つと `--config <tmp>/c.ini` |
| `UT-run_pipeline-25` | フェーズ3 の段 | 一時のソースツリーと一時の設定と前回の出力 | (a) `--phase 3 --n 5`、(b) `check_cols.rcs` を `3` にして `--phase 3 --n 6`、(c) `check_cols.rcs` を `3` にして `--phase 3 --n 4` | `analyze_terrain` の引数が `--config <パス> --mode wide --japan-mesh-list <パス> --n <N> --unresolved <tmp>/data/results/key_col_unresolved_peaks-<N−1>.csv`（`--mesh` なし）。`analyze_terrain` の時点の `.files` に、N〜6 の広域のファイルと `-<N>.csv`〜`-6.csv` と `merged_summit.*`・`merged_viewer*` が無く、`merged_peak.csv`・`merged_peak.geojson` と N より小さい広域のファイル（(a) は N=4 の 3 つ）と `-<N−1>.csv` が残る。`merge_peaks`（2 回目）の時点の `.files` に `merged_peak.geojson` が無い。`check_cols` は `--n <N>`。(a) 0 で PG2、(b) 3 で PG1（N=6 の文）、(c) 3 で PG1（`--phase 3 --n 5`） |
| `UT-run_pipeline-26` | 通しの段の進め方 | 一時のソースツリーと一時の設定と前回の出力 | (a) `check_cols.rcs` を `3\n3\n3\n3`、(b) `check_cols.rcs` を `0`、(c) `check_cols.rcs` を `3\n0`、(d) (a) に `--mesh 5339` を足す | (a) `analyze_terrain` が normal・wide N=4・5・6 の 4 回、`check_cols` が `--n 3`・`4`・`5`・`6`、その後に `match_summits`・`generate_viewer`、0。(b) wide を起動せずに `match_summits` へ。(c) wide は N=4 だけ。(d) `--mesh 5339` は normal の `analyze_terrain` とフェーズ2 の `merge_peaks`・`merge_zones` にだけ付く。どれも段の始まりごとに、その段の HLD 2.10.3 の行のファイルが次の起動の `.files` に無い |
| `UT-run_pipeline-27` | フェーズ4 の結果 | 一時のソースツリーと一時の設定と前回の出力 | `--phase 4` で、(a) `match_summits.rcs` を `0`、(b) `4`（前回の出力から `key_col_unresolved_peaks-6.csv` を除く）、(c) `4`（`key_col_unresolved_peaks-6.csv` を置いたまま）、(d) `1`、(e) `match_summits` は 0 で `generate_viewer.rcs` を `2` | (a) 0、`generate_viewer` を起動する。(b) 4、`generate_viewer` を起動しない、PG3 が出ない。(c) 4、PG3 が出る。(d) 1、`generate_viewer` を起動しない。(e) 2。`match_summits` の時点の `.files` に `merged_summit.*`・`merged_viewer*` が無く、`merged_peak.*` が残る |
| `UT-run_pipeline-28` | 起動口の失敗 | 一時のソースツリーと一時の設定と前回の出力 | 通しで、(a) `analyze_terrain.rcs` を `1`、(b) `merge_peaks.rcs` を `0\n2`（1 回目の `--check-land-peaks` は 0、続く通常の統合の `merge_peaks` が 2）、(c) `check_cols.rcs` を `1`、(d) `check_cols.rcs` を `4`、(e) `analyze_terrain.rcs` を `137` | 終了コード 1・2・1・4・137。どれもその起動の後に起動口の記録が無い。ログファイルの最後の 2 行が PL9（途中で止まった形。(a) は `最後に終えた段: なし`）と L3 |
| `UT-run_pipeline-29` | ロックとログの記述子 | 一時のソースツリーと一時の設定 | `--phase 2` | `resolve_config` の記録は `nofile`、ほかの起動口の記録はどれも `locked` と `fd8-closed`。終わった後、テストのプロセスが `<tmp>/data/findsummits.lock` に排他のロックを `fcntl.flock` で待たずに（`LOCK_EX` と `LOCK_NB` を合わせて）掛けられ、ロックファイルが残る |
| `UT-run_pipeline-30` | ログの段と起動口の行 | 一時のソースツリーと一時の設定。`check_cols.rcs` を `3\n0`。`analyze_terrain.say` に `stub-say\n` | 通し | ログファイルに、PL4（`段の始まり: フェーズ2`）、PL5、PL6（`起動: analyze_terrain --config …`）、PL7（`起動口の終了: analyze_terrain 終了コード 0`）、…、PL8（`段の終わり: フェーズ2（充足判定の終了コード 3）`）、PL4（`フェーズ3 の N=4`）、…、PL8（`段の終わり: フェーズ4（突合の終了コード 0、ビューア生成の終了コード 0）`）、PL9（`結果の要約: 最後に終えた段: フェーズ4（突合の終了コード 0、ビューア生成の終了コード 0）`）、L3 がこの順にある。スタブが画面に出したもの（`stub-say`）は、標準出力と標準エラー出力にそれぞれ `analyze_terrain` の起動の回数（2 回）だけ出て、ログファイルには無い |
| `UT-run_pipeline-31` | シグナル | 一時のソースツリーと一時の設定。`analyze_terrain.wait` を置く | (a) `--phase 2` を起こし、`analyze_terrain.started` ができたら、`run_pipeline` のプロセスにだけ `SIGTERM` を送り、1 秒待って `run_pipeline` がまだ動いていること（`Popen.poll()` が `None`）を確かめてから `release` を作る。(b) 同じく起こし、プロセスのグループに `SIGINT` を送る（`os.killpg`） | (a) 143、`release` を作るまで止まらない（送った後もスタブが動いている）、ログファイルの最後の 2 行が PL9（`フェーズ2 の途中で止まった`）と L3（`SIGTERM` を受けて止まった形、終了コード 143）。(b) 130、L3 は `SIGINT` の形 |
| `UT-run_pipeline-32` | ソースツリーの求め方 | 一時のソースツリーと一時の設定。`<tmp>/bin/rp` に `<tmp>/src/scripts/run_pipeline.sh` へのシンボリックリンクを置く | `<tmp>/bin/rp --phase 2` を `<tmp>/work` から起動する | 0、スタブが起動される（`<tmp>/src` の `venv/bin/python3` と `build/analyze_terrain` が使われる）、`--japan-mesh-list` が `<tmp>/src/params/mesh_list_japan.txt` |
| `UT-run_pipeline-33` | 空白とグロブの字を含む `data_dir` での削除と前提 | 一時のソースツリーと一時の設定と前回の出力を、`data_dir` を `<tmp>/d a[t]a*`（空白・`[`・`]`・`*` を含む）にして置く（`resolve_config.out` と `STUB_DATA_DIR` もその値）。別に `<tmp>/d` と `<tmp>/a[t]a` に空のファイル `x` を置く | (a) `--phase 2`、(b) 通し（`check_cols.rcs` を `0`） | (a) 0、`analyze_terrain` の時点の `.files` が `UT-run_pipeline-24` の (a) と同じ（フェーズ2 の行のファイルだけが消え、通常の出力が残る）。(b) PC2 が出ずに前提を通る。どちらも `<tmp>/d/x` と `<tmp>/a[t]a/x` が残る |
| `UT-run_pipeline-34` | 標準出力が読む相手のいないパイプ | 一時のソースツリーと一時の設定。`subprocess.Popen` で `stdout=subprocess.PIPE` にして起動し、親がすぐに読む側を閉じる | `--phase 2` | 終了コード 1（141 でない）。ログファイルの最後の 2 行が PL9 と L3（終了コード 1） |
| `UT-run_pipeline-35` | 標準エラー出力が使えないときの終了コード | 一時のソースツリーと一時の設定。標準エラー出力を、(i) `UT-run_pipeline-34` と同じく読む相手のいないパイプ、(ii) `preexec_fn` で記述子 2 を閉じたものにして起動する（別々の起動） | (i)(ii) のそれぞれで `--foo`（PA1）と、記録を `5339\n` にした `--phase 2`（FC1） | `--foo` はどれも 2（1 や 141 にならない）、`--phase 2` はどれも 1（141 にならない） |

### 5.2 `resolve_config`

- **ID**: LLD-resolve_config
- **対応 HLD**: [3.3](30_HLD.md#33-cmp3-パイプライン制御)
- **ファイル**: `scripts/resolve_config.py`

処理の正本は[HLD 2.3.2](30_HLD.md#232-設定ファイル)の設定解決の段落と[HLD 2.3.3](30_HLD.md#233-検証と記録)で、この節はそれを Python で書くための細部だけを足す。`run_pipeline` とのつなぎ目は `CMP3-INT1`（[HLD 3.3.5](30_HLD.md#335-結合のつなぎ目)）で、その結合テスト（IT）のケースは `60_IT.md` の `IT-CMP3-INT1-01`〜`04` である。

#### 5.2.1 ファイル割付

- 関数はすべて `scripts/resolve_config.py` 1 本に置く。`venv/bin/python3 scripts/resolve_config.py` で起動され（[HLD 3.3.1](30_HLD.md#331-プログラム)）、共通部品は `import common` で読む（[2.1.1](#211-ファイル割付)と同じ）。ファイルの先頭のコメントに `# trace: LLD-resolve_config` を書く。
- UT のコードは `tests/scripts/test_resolve_config.py` に置く。各テストに `# trace: UT-resolve_config-NN`（確かめる UT 候補の ID）のコメントを付ける。

#### 5.2.2 型とデータ

なし。新しい型・定数は無い。設定値は `common.load_config` の返す `common.Config`（[2.1.2](#212-型とデータ)）で受け、全キーの名前は `common.CONFIG_KEY_NAMES`（2.1.2）を使う。必須のキーは `('data_dir',)` で、関数の中に直接書く（[HLD 2.3.3](30_HLD.md#233-検証と記録)の「設定解決が要求する必須キーは `data_dir` だけ」）。

#### 5.2.3 関数の細部

`resolve_config` は `start_log` を呼ばない（ログファイルを作らない。[HLD 3.9](30_HLD.md#39-共通部品)の前置き）ので、[2.1.3](#213-関数の細部)の前置きの呼ぶ側の書き方の型（`start_log` の後の `try`/`finally` と結果の要約）は当てない。`StartTime.now()` も呼ばない（`start_log` に渡す先が無い）。`log_info` は標準出力に出すので呼ばない（標準出力は 2 行だけに使う。HLD 2.3.2）。`log_warning` を呼ぶ場面は無い（警告して続ける場面が HLD に無い）。メッセージは `common.log_error` で標準エラー出力に出す（`start_log` の前なので、ログファイルには出ない。出すのは下の `_stop` の中）。[1.2](#12-lld-の規約)の終わり方の規約（`sys.exit` を `sys` の属性として呼ぶ。`except BaseException` などを書かない）はそのまま当てる。捕まらなかった例外は Python の既定のまま（Traceback を標準エラー出力に出して終了コード 1）、`SIGINT`・`SIGTERM` も Python の既定のまま（130・143）で、どちらも `_excepthook`・`_on_signal` は付かない（`start_log` が付けるため）。

画面への出力の失敗: 標準エラー出力が読む相手のいないパイプのときなど、`common.log_error` の書き込みの失敗（`OSError`、閉じたストリームなら `ValueError`）は呼び出し側へ伝わり、Python が終わるときの flush も失敗して、終了コードが決まりの 1・2 でなく 120 になる（失敗を捕まえてから `sys.exit` を呼んでも同じ。2026-10-21 に CPython 3.14.7 で、標準エラー出力を読む相手のいないパイプにして確かめた。壊れたストリームを `open(os.devnull, 'w')` に差し替えてから `sys.exit` を呼ぶと、決まりの終了コードのままになる）。`resolve_config` には `start_log` が取り付ける後始末（[2.1.3](#213-関数の細部)の `_finish_log`）が無いので、自分で止まるときは、下の内部の関数 `_stop` で止まる。`load_config` の中で止まるとき（CF1〜CF7）のメッセージの出力の失敗は、`main` の 2 が受ける。起動の時点で標準出力の記述子が閉じていると、Python は `sys.stdout` を `None` にし、`os.write(1, …)` は `OSError`（`EBADF`）になる（`write_resolved_paths` の 3 の RW1）。このとき `_stop` の 2 は `sys.stdout` を飛ばす（`None` の `flush` は `AttributeError` で、`sys.exit` に届かずに終了コードが 2 でなく 1 になる。2026-10-21 に CPython 3.14.7 で、記述子 1 を閉じて起動して確かめた）。起動の時点で標準エラー出力の記述子が閉じていて `sys.stderr` が `None` のときは、2.1 と同じく扱わない。

##### main

`main() -> None`（起動の部分。`if __name__ == '__main__': main()`）。`main` は[1.1](#11-用語定義)の「起動の部分」の関数で、名前は 2.1.3 の前置きの呼ぶ側の書き方の型（`def main()`）に従う（ほかのモジュールから呼ばない。1.2 の名前の規約の「内部の関数」と同じ扱い）。次の順に行う。

1. `config_path = _parse_args(sys.argv[1:])`。
2. `try` の中で `config = common.load_config(config_path, common.CONFIG_KEY_NAMES, ('data_dir',))` を呼ぶ（誤りがあれば `load_config` が CF1〜CF7 を出して終了コード 2 で止まり、戻らない）。`except (OSError, ValueError):` で `_stop(common.EXIT_USAGE, [])`。`load_config` が `OSError` か `ValueError` を上げるのは、誤りのメッセージを出せなかったとき（標準エラー出力が使えないとき）だけである（渡すキーは固定なので、呼ぶ側の誤りの `ValueError` は上がらない。設定ファイルの読み取りの失敗と UTF-8 の誤りは `load_config` が CF2 で受ける）。メッセージを出せなかった誤りは、どれも終了コード 2 の誤り（CF1〜CF7）なので、終了コードは 2 にする。
3. `errors = _check_resolved(config)`。空でなければ `_stop(common.EXIT_USAGE, errors)`（一覧の順に全部を出して、1 回だけ止まる。`load_config` の 8 と同じ）。
4. `write_resolved_paths(config.values['data_dir'].value, config.values['log_dir'].value)`。
5. `sys.exit(common.EXIT_OK)`。

`load_config` の誤りがあると 3 の検査は行われない（`load_config` が先に止まるため。設定を直して起動し直すと 3 の誤りが出る）。

##### _parse_args

`_parse_args(argv: Sequence[str]) -> str`（内部）

1. `len(argv) == 2` かつ `argv[0] == '--config'` でなければ、RA1 の `(what, action)` を `_stop(common.EXIT_USAGE, [(what, action)])` に渡して止まる。`--config=<パス>` の形、`--help`、知らないオプション、位置引数、`--config` を 2 回書いた形（`--config <パス> --config <パス>`。引数が 3 つ以上）も RA1 になる。引数が 2 つで 1 つ目が `--config` のときは、2 つ目が `--config` でも RA1 でなく、2 の判定に進む（`--config --config` は、絶対パスでない値として RA2）（受け取るのは `run_pipeline` が渡す `--config <絶対パス>` の形だけ。[HLD 2.4.5](30_HLD.md#245-内部引数)。`--help` は利用者向けの 3 コマンドだけのもの。[HLD 2.4.2](30_HLD.md#242-共通の書式)）。
2. `os.path.isabs(argv[1])` が偽なら（空の文字列を含む）、RA2 の `(what, action)` を `_stop(common.EXIT_USAGE, [(what, action)])` に渡して止まる（内部の起動口は絶対パスを必須にする。[HLD 2.3.2](30_HLD.md#232-設定ファイル)）。
3. `argv[1]` を返す。ファイルがあるか、読めるかは `load_config` が確かめる（無ければ CF1。対処の文の分岐は[2.1.3](#213-関数の細部)の `load_config` の 2 のとおりで、既定の設定ファイルの絶対パスなら見本の複製の案内、それ以外は `--config に渡したパスを確かめる`）。

##### _check_resolved

`_check_resolved(config: common.Config) -> list[tuple[str, str]]`（内部）

`load_config` が確かめない 2 つ（[HLD 3.9](30_HLD.md#39-共通部品)の表の後の段落）を確かめ、誤りごとに `(what, action)` を返す（無ければ空のリスト）。順は次のとおり。

1. パスの改行: `data_dir` の値に `'\n'` か `'\r'` があれば RP1（`{key}` は `data_dir`）。`log_dir` は `from_file` が真で、値に `'\n'` か `'\r'` があるときだけ RP1（`{key}` は `log_dir`。デフォルトの `log_dir` は `data_dir` から作るので、`data_dir` の RP1 で足りる）。2.1.3 の設定ファイルの書式では、行は `'\n'` で分かれるので値に `'\n'` は入らないが、行の途中の `'\r'` は値に残りうる。読み方に頼らず両方を見る（[HLD 2.3.2](30_HLD.md#232-設定ファイル)の「パスに改行を含む設定は、設定解決が終了コード 2 で拒否する」）。
2. 相互制約: `prominence_primary_m` の値が `prominence_final_m` の値以上なら CX1（[2.2](#22-ログとメッセージの文面)）。どちらもデフォルトのときも比べる（今の許容範囲では最終フィルタ閾値は 150 だけなので、一次フィルタ閾値に 150 以上を書いたときに当たる）。

##### write_resolved_paths

`write_resolved_paths(data_dir: str, log_dir: str) -> None`（[HLD 3.3.3](30_HLD.md#333-関数)の表の関数）

1. `data = f'data_dir={data_dir}\nlog_dir={log_dir}\n'.encode('utf-8')`。値は `load_config` が返したまま書き、正規化しない（末尾の `/`、空白、`$`・`=` などもそのまま。ほかのバッチが同じ設定ファイルから読む値と同じにするため）。UTF-8 にするのは、設定ファイルが UTF-8 で、ロケールが UTF-8 でないときも `run_pipeline` がほかのバッチと同じバイト列のパスを得るため（`sys.stdout` の文字コードに頼らない）。
2. ファイル記述子 1 に `os.write(1, …)` で書く。`os.write` が書いた数が残りより少なければ、残りを書き続ける。`sys.stdout` は使わない（`sys.stdout` のバッファに書けなかった字が残ると、Python が終わるときにもう一度 flush して終了コードを 120 にするため。2.1.3 の `_finish_log` の 4 と同じ理由）。
3. `OSError`（切れたパイプ、閉じた記述子など）なら、RW1 の `(what, action)` を `_stop(common.EXIT_ERROR, [(what, action)])` に渡して止まる（[HLD 2.5.1](30_HLD.md#251-終了コード)の読み書きの失敗）。途中まで書けていても止まる（`run_pipeline` は 0 以外を受けてその値で止まる。[HLD 2.5.2](30_HLD.md#252-パイプライン制御での扱い)）。

##### _stop

`_stop(code: int, messages: Sequence[tuple[str, str]]) -> NoReturn`（内部。`resolve_config` が自分で止まる場所はすべてこれで止まる）

1. `messages` の各 `(what, action)` を、順に `common.log_error(what, action)` で出す。`OSError` か `ValueError` が上がったら、捕まえて、残りのメッセージは出さない。
2. `sys.stdout`・`sys.stderr` をこの順に flush する。`None` のもの（起動の時点で記述子が閉じていた。上の前置きの段落）は、flush も差し替えもせずに飛ばす。`OSError` か `ValueError` が上がったものは、その属性を `open(os.devnull, 'w')` に差し替える（出力は捨てる。Python が終わるときにもう一度行う flush が失敗して、終了コードが 120 になるのを防ぐ。2.1.3 の `_finish_log` の 4 と同じ理由）。
3. `sys.exit(code)`。

#### 5.2.4 メッセージ文面

書き方は[2.2](#22-ログとメッセージの文面)。`{args}` は起動の引数を L1 の引用の決まり（2.2）で 1 つずつ書いて空白 1 つでつないだもの（`shlex.join(argv)`）で、引数が無ければ `（引数なし）`。`{value}` は `--config` の値を同じ引用の決まりで書いたもの（`shlex.quote(value)`。空なら `''`）。`{path}` は `Config` の `path`。`{reason}` は `OSError` の `strerror`（無ければ `str(e)`）。CF1〜CF7 は[2.1.4](#214-メッセージ文面)、CX1 は 2.2 にあり、ここに写さない。

| 記号 | 場面 | 1 行目（`ERROR:` と空白 1 つの後） | 2 行目（`対処:` と空白 1 つの後） | 終了コード |
|---|---|---|---|---|
| RA1 | 引数の形が違う | `resolve_config の引数が違う: {args}` | `--config と設定ファイルの絶対パスの 2 つだけを渡す（resolve_config は run_pipeline が起動する内部の起動口）` | 2 |
| RA2 | `--config` が絶対パスでない | `--config のパスが絶対パスでない: {value}` | `--config に設定ファイルの絶対パスを渡す` | 2 |
| RP1 | パスに改行がある | `設定のパスに改行がある: [paths] {key}（{path}）` | `[paths] の {key} を 1 行の絶対パスにする（行の途中の CR は値の一部として読まれる）` | 2 |
| RW1 | 標準出力に書けない | `設定解決の結果を標準出力に書けない: {reason}` | `run_pipeline から起動し直す。続くときは、このメッセージを写して開発者に知らせる` | 1 |

#### 5.2.5 UT 候補

すべて自動。どのケースも子のプロセスで動かす（引数の読み方と標準出力のバイト列は `CMP3-INT1` が頼る起動の約束なので、起動のしかたのまま確かめる）。表の準備の列の共通の準備は次の 2 つ。ケースに固有の準備は、その後に書く。

- **子のプロセス**: `subprocess.run([sys.executable, <ソースツリー>/scripts/resolve_config.py, *<引数>], capture_output=True)` で起動する（`<ソースツリー>` はテストのファイルの親の親の親。ケースが書かなければ環境は親のまま）。終了コード、標準出力のバイト列、標準エラー出力の文字列（UTF-8 で読む）を確かめる。
- **一時の設定**: ケースごとに一時のディレクトリ `<tmp>` を作り、`<tmp>/config.ini` に設定を UTF-8 で書く。`data_dir` は、ケースが書かなければ `<tmp>/data`（作らない）。引数は、ケースが書かなければ `--config <tmp>/config.ini`。

共通の準備と違う起動をするケース（`UT-resolve_config-09`〜`-13`）は、その行の準備に書く。止まるケースの期待の「標準出力は空」は、標準出力のバイト列が `b''` であること。メッセージの期待は、標準エラー出力の行の文面（2.2・2.1.4・5.2.4 の文面に値を入れたもの）。

| ID | 確かめること | 準備 | 入力 | 期待 |
|---|---|---|---|---|
| `UT-resolve_config-01` | 正しい設定の 2 行 | 子のプロセス。一時の設定に全キーを書く: `[paths]` に `data_dir = <tmp>/data`・`log_dir = <tmp>/logs`、`[fetch]` に `max_parallel = 4`・`interval_ms = 100`・`user_agent_email = jj@example.com`、`[analysis]` に `prominence_primary_m = 130`・`activation_zone_drop_m = 25`・`delete_zone_max_drop_m = 250`、`[merge]` に `prominence_final_m = 150`、`[match]` に `sota_geojson_version = 3`・`provisional_code_max_prefix = B`・`unmatched_summit_threshold = 5` | 引数は既定 | 0。標準出力は `data_dir=<tmp>/data\nlog_dir=<tmp>/logs\n` の UTF-8 と等しい。標準エラー出力は空。`<tmp>/data` と `<tmp>/logs` は作られていない |
| `UT-resolve_config-02` | `log_dir` のデフォルトと、必須でないキー | 子のプロセス。一時の設定は `[paths]` の `data_dir` だけ | 引数は既定 | 0。標準出力は `data_dir=<tmp>/data\nlog_dir=<tmp>/data/logs\n`（`log_dir` は `os.path.join(<tmp>/data, 'logs')`）。`user_agent_email` が無くても止まらない。`<tmp>/data` は作られていない |
| `UT-resolve_config-03` | 値をそのまま UTF-8 で出す | 子のプロセス。環境に `PYTHONIOENCODING=ascii` を足す。一時の設定の `data_dir` を `<tmp>/a b/$(touch <tmp>/evil)/x=y/日本/`（末尾の `/` まで） | 引数は既定 | 0。標準出力は `data_dir=<その値>\nlog_dir=<os.path.join(その値, 'logs')>\n` の UTF-8 と等しい。`<tmp>/evil` は作られていない |
| `UT-resolve_config-04` | 自分が使わないキーも確かめる | 子のプロセス。キーごとに別の一時の設定（どれも `data_dir` を書く。`log_dir` のケースは `data_dir` と同じ `[paths]` の見出しの下に書く。見出しを 2 回書くと INI として読めず、CF3 になる） | 次の 12 の設定をそれぞれ: `data_dir = data`、`log_dir = logs`、`max_parallel = 0`、`interval_ms = 5001`、`user_agent_email = a b@example.com`、`prominence_primary_m = 99`、`activation_zone_drop_m = 26`、`delete_zone_max_drop_m = 301`、`prominence_final_m = 151`、`sota_geojson_version = 0`、`provisional_code_max_prefix = a`、`unmatched_summit_threshold = -1`（`data_dir = data` のケースは、`data_dir` をこの値だけにする） | どれも 2、CF6 のメッセージがそのキーの 1 つ、標準出力は空 |
| `UT-resolve_config-05` | 設定ファイルが無い・必須の `data_dir` が無い | 子のプロセス。(ii) は一時の設定に `[fetch]` の `max_parallel = 4` だけを書く | (i) 一時の設定を書かずに `--config <tmp>/none.ini`、(ii) 引数は既定 | どれも 2、標準出力は空。(i) は CF1 で `対処:` は `--config に渡したパスを確かめる`。(ii) は CF7（`[paths] data_dir`）が 1 つだけ |
| `UT-resolve_config-06` | 相互制約 | 子のプロセス。値ごとに別の一時の設定（`prominence_final_m` は書かない） | `prominence_primary_m = 149`、`prominence_primary_m = 150` | 149 は 0 で 2 行が出る。150 は 2、標準エラー出力は CX1 の 2 行だけで、1 行目は `ERROR: プロミネンス一次フィルタ閾値が最終フィルタ閾値以上: [analysis] prominence_primary_m = 150（ファイル）、[merge] prominence_final_m = 150（デフォルト）（<tmp>/config.ini）`、標準出力は空 |
| `UT-resolve_config-07` | パスの改行 | 子のプロセス。ケースごとに別の一時の設定。改行は行の途中の CR で入れる（`data_dir = <tmp>/x` の後に CR と `y` を同じ行に書く。バイト列で書く。2.1.3 の設定ファイルの書式では値に LF が入らず、行の途中の CR だけが値に残る） | (i) `data_dir` だけを CR 入りにする（`log_dir` は書かない）、(ii) `log_dir` だけを CR 入りにする、(iii) `data_dir` と `log_dir` を CR 入りにし、`prominence_primary_m = 150` も書く | (i) 2、RP1（`data_dir`）が 1 つだけ。(ii) 2、RP1（`log_dir`）。(iii) 2、RP1（`data_dir`）・RP1（`log_dir`）・CX1 がこの順に出る。どれも標準出力は空 |
| `UT-resolve_config-08` | 引数の誤り | 子のプロセス。一時の設定は `data_dir` だけ | 引数をそれぞれ: (i) なし、(ii) `--config`、(iii) `--config <tmp>/config.ini --extra`、(iv) `--config=<tmp>/config.ini`、(v) `--help`、(vi) `<tmp>/config.ini`、(vii) `--config config.ini`、(viii) `--config ''`、(ix) `--config --config` | どれも 2、標準出力は空。(i)〜(vi) は RA1 で、(i) の 1 行目は `ERROR: resolve_config の引数が違う: （引数なし）`、(v) は `ERROR: resolve_config の引数が違う: --help`。(vii)(viii)(ix) は RA2 で、1 行目は `ERROR: --config のパスが絶対パスでない: config.ini`、`ERROR: --config のパスが絶対パスでない: ''`、`ERROR: --config のパスが絶対パスでない: --config` |
| `UT-resolve_config-09` | 標準出力に書けない | 一時の設定は `data_dir` だけ。共通の準備の `capture_output=True` を使わず（`stdout=` と併せると `ValueError` になる）、`<tmp>/config.ini` を読むだけで開いたもの（`open(<tmp>/config.ini, 'rb')`）を `stdout=` に、`subprocess.PIPE` を `stderr=` に渡して起動する（読むだけの記述子への書き込みは `OSError`〈`EBADF`〉になる） | 引数は既定 | 1（120 でない）、標準エラー出力は RW1 の 2 行だけで、1 行目は `ERROR: 設定解決の結果を標準出力に書けない: <os.strerror(errno.EBADF)>` |
| `UT-resolve_config-10` | 少しずつしか書けないとき・途中で書けなくなったとき | 一時の設定は `data_dir` だけ。子のプロセスを `[sys.executable, '-c', <試験用の短いプログラム>, '--config', <tmp>/config.ini]` で起動し、`capture_output=True` で受ける。試験用のプログラムは、`<ソースツリー>/scripts` を `sys.path` の先頭に入れて `import resolve_config` し、`os.write` を差し替えてから `sys.argv = ['resolve_config.py', '--config', <tmp>/config.ini]` にして `resolve_config.main()` を呼ぶ | (i) 差し替えた `os.write` は、毎回もとの `os.write` で先頭の 5 バイトまでだけを書いてその数を返す。(ii) 1 回目はもとの `os.write` で先頭の 5 バイトだけを書いて 5 を返し、2 回目は `OSError(errno.EPIPE, os.strerror(errno.EPIPE))` を上げる | (i) 0、標準出力は `UT-resolve_config-02` と同じ 2 行の全部。(ii) 1、標準出力は 2 行の UTF-8 の先頭の 5 バイト、標準エラー出力は RW1 の 2 行で、1 行目は `ERROR: 設定解決の結果を標準出力に書けない: <os.strerror(errno.EPIPE)>` |
| `UT-resolve_config-11` | 標準エラー出力が使えないときの終了コード | 子のプロセス。共通の準備の `capture_output=True` を使わず、`os.pipe()` で作ったパイプの読む側を親が閉じ（読む相手のいない標準エラー出力にする）、書く側を `stderr=` に、`subprocess.PIPE` を `stdout=` に渡して起動する（起動した後、親は書く側も閉じる）。一時の設定は入力ごとに別 | (i) 引数なし（RA1）、(ii) `[paths]` の `data_dir = data` だけの設定（CF6。`load_config` の中の誤り）、(iii) `data_dir` と `prominence_primary_m = 150` の設定（CX1） | どれも終了コード 2（120 でない）。標準出力は `b''` |
| `UT-resolve_config-12` | 標準出力も標準エラー出力も書けない | 一時の設定は `data_dir` だけ。`UT-resolve_config-09` の標準出力（`<tmp>/config.ini` を読むだけで開いたもの）と、`UT-resolve_config-11` の標準エラー出力（読む相手のいないパイプ）を組み合わせて起動する（`capture_output=True` は使わない） | 引数は既定 | 終了コード 1（120 でない） |
| `UT-resolve_config-13` | 起動の時点で標準出力が閉じているとき | 子のプロセス。共通の準備の `capture_output=True` を使わず、`stderr=subprocess.PIPE` と `preexec_fn=lambda: os.close(1)` を渡して起動する（子の記述子 1 を閉じたまま Python を起動する）。一時の設定は入力ごとに別 | (i) 引数なし（RA1）、(ii) `data_dir` と `prominence_primary_m = 150` の設定（CX1）、(iii) `data_dir` だけの設定（正しい設定） | (i)(ii) は終了コード 2、(iii) は 1。標準エラー出力は、(i) が RA1 の 2 行だけ、(ii) が CX1 の 2 行だけ、(iii) が RW1 の 2 行だけ（1 行目は `ERROR: 設定解決の結果を標準出力に書けない: <os.strerror(errno.EBADF)>`）で、どれも `Traceback` を含まない |

## 6. CMP4 地形解析エンジン

この章は、CMP4（地形解析エンジン）の `analyze_terrain`（[HLD 3.4.1](30_HLD.md#341-プログラム)の実行ファイル 1 本）を、[HLD 3.4.3](30_HLD.md#343-関数)の表の群ごとのモジュールに分けて置く（ADR-LLD-001 の Decision 3）。どのモジュールも 1.2 の C++ の規約に従う。今は 6.1〜6.10・6.12 を書き、ほかの群の節は書くときに 6.11 の番号で足す（6.12 と 6.10 を先に書いたのは、ほかの群がその型と関数を使うため）。6.1 の `main` が呼ぶ `run_normal_mode`・`run_wide_mode` は 6.11 の関数で、その宣言の形は [6.1.2](#612-型とデータ) で決めた（6.11 を書くときは、その形で宣言する。変えるときは 6.1 も同じ変更で直す）。CMP4 にコンポーネント内の共通部品は無い（[HLD 3.4.4](30_HLD.md#344-コンポーネント内の共通部品)）。

### 6.1 `analyze_terrain_launch`

- **ID**: LLD-analyze_terrain_launch
- **対応 HLD**: [3.4](30_HLD.md#34-cmp4-地形解析エンジン)・[4.4](30_HLD.md#44-fr-004-33メッシュ結合解析オーケストレーション)・[4.14](30_HLD.md#414-fr-014-広域結合解析オーケストレーション)
- **ファイル**: `src/launch.hpp`・`src/launch.cpp`・`src/analyze_terrain.cpp`

処理の正本は [HLD 3.4.3](30_HLD.md#343-関数) の前置きの段落と呼ぶ順の「起動」で、引数は [HLD 2.4.5](30_HLD.md#245-内部引数) の CMP4（地形解析エンジン）の行と [HLD 2.4.2](30_HLD.md#242-共通の書式)・[2.4.3](30_HLD.md#243-メッシュ範囲)、誤りは [HLD 4.4.3](30_HLD.md#443-異常系)・[4.14.3](30_HLD.md#4143-異常系) の「引数・設定の誤り」の行である。この節は、それを C++ で書くための細部だけを足す。1.2 の C++ の規約と、6.12 の型と関数を使う。`run_pipeline` とのつなぎ目は `CMP4-EXT1`（[HLD 3.4.5](30_HLD.md#345-結合のつなぎ目)）で、その結合テスト（IT）のケースは `60_IT.md` の `IT-CMP4-EXT1-01`・`-02` である。結果の要約（[HLD 5.7.2](30_HLD.md#572-処理の流れ)の 7「結果の要約」の `analyze_terrain` の行）は 6.11 の `run_normal_mode`・`run_wide_mode` が出し、6.1 は持たない（`start_log` から段までの間に処理が無い）。

#### 6.1.1 ファイル割付

- `src/launch.hpp`: `Args` と `parse_args` の宣言。`#include "common.hpp"` はしない（`Args` は標準ライブラリの型だけ）。`<set>`・`<string>`・`<vector>` を読む。
- `src/launch.cpp`: `parse_args` と、無名の名前空間の内部の関数（[6.1.3](#613-関数の細部)）。`#include "launch.hpp"` と `#include "common.hpp"`。
- `src/analyze_terrain.cpp`: `int main(int argc, char* argv[])` と、無名の名前空間の `_check_cross`。プログラムの名前（[HLD 3.4.1](30_HLD.md#341-プログラム)）にそろえた名前で、ヘッダーを持たない。`#include <opencv2/core.hpp>`（`cv::setNumThreads`。[HLD 2.6.5](30_HLD.md#265-ビルド構成)のモジュールごとのヘッダ）、`"common.hpp"`・`"launch.hpp"`・`"stage.hpp"`（6.11 のヘッダー。宣言の形は [6.1.2](#612-型とデータ)）。6.1 の 3 本のうち OpenCV を読むのはこのファイルだけで、`src/launch.hpp`・`src/launch.cpp` は OpenCV のヘッダーを読まず、OpenCV の関数を直接使わない。`build/test_launch` がどのファイルをリンクするかは [2.5](#25-ビルドとテストの名前)のとおりで、6.1 では決めない。
- `main` を `src/launch.cpp` に置かず別のファイルに分けるのは、2.5 の決まり（テスト用の実行ファイルに `main` を持たない `.cpp` をすべてリンクする）のまま、`parse_args` を `build/test_launch` から直接呼べるようにするため。
- 3 本とも先頭のコメントに `// trace: LLD-analyze_terrain_launch` を書く。ヘッダーは、先頭の trace のコメントの次の行を `#pragma once` にする（1.2）。
- UT のコードは `tests/src/test_launch.cpp`（`build/test_launch`。2.5）と、`main` の振る舞いを確かめる試験用の実行ファイル `build/test_launch_main`（2.5 の `build/test_<群の名前>` のテスト用の実行ファイルとは別のもの）にだけリンクする段の進行のスタブ `tests/src/stub_stage.cpp` に置く。`tests/src/test_launch.cpp` の各テストに `// trace: UT-analyze_terrain_launch-NN`（確かめる UT 候補の ID）を書く。`tests/src/stub_stage.cpp` の先頭のコメントには、スタブを使うケースの ID を並べて書く: `// trace: UT-analyze_terrain_launch-16, UT-analyze_terrain_launch-17, UT-analyze_terrain_launch-20, UT-analyze_terrain_launch-21, UT-analyze_terrain_launch-22, UT-analyze_terrain_launch-23`（`tools/lint_trace.py` は `tests/src/` の下のファイルごとにテストケースの ID を求め、無ければ単体テスト（UT）の段で T5 で止めるため。`LLD-` の trace はここで数えない）。テストの枠組みは GoogleTest（[テスト方針書 3.4](02_test_policy.md#34-テストを先に書く進め方)）。

#### 6.1.2 型とデータ

`src/launch.hpp` の公開の宣言は次のとおり（名前空間に入れない。1.2 の C++ の規約）。

```cpp
#pragma once
#include <set>
#include <string>
#include <vector>

struct Args {
    std::string config_path;              // --config の値（絶対パス。受け取ったまま）
    bool wide = false;                    // --mode wide なら真、normal なら偽
    std::string japan_mesh_list;          // --japan-mesh-list の値（絶対パス。受け取ったまま）
    int n = 0;                            // --n の値（4・5・6）。通常は 0
    std::string unresolved;               // --unresolved の値（絶対パス。受け取ったまま）。通常は空
    bool has_mesh = false;                // --mesh を受け取ったら真（通常だけ）
    std::string mesh_value;               // --mesh の値（受け取ったまま）。無ければ空
    std::set<std::string> mesh_codes;     // read_mesh_arg(mesh_value) の結果。無ければ空
};

Args parse_args(const std::vector<std::string>& args);   // args は argv[1] から後
```

- `wide` を `bool` にするのは、1.2 の「値の有無は `bool` の印で持つ」に合わせ、モードが 2 つだけなので列挙の型を足さないため。
- `run_normal_mode`・`run_wide_mode` の宣言の形（6.11 の `src/stage.hpp` に置く。[HLD 3.4.3](30_HLD.md#343-関数)の表の受け取るものの順。`Config` は 6.12）:

  ```cpp
  void run_normal_mode(const std::string& japan_mesh_list, bool has_mesh,
                       const std::set<std::string>& mesh_codes, const Config& config);
  void run_wide_mode(const std::string& japan_mesh_list, int n,
                     const std::string& unresolved, const Config& config);
  ```

  `has_mesh` が偽なら `mesh_codes` は空で、HLD の「なし」に当たる。止まるときは `ExitRequest` を投げ、最後まで進んだら戻る。
- `main` が `load_config` に渡すキーの定数（`src/analyze_terrain.cpp` の無名の名前空間の `const std::vector<std::string> _load_keys` と `_load_required`。6.12 の内部の `_config_keys` と読み違えないよう別の名前にする）: `_load_keys` は `data_dir`・`log_dir`・`prominence_primary_m`・`activation_zone_drop_m`・`delete_zone_max_drop_m`・`prominence_final_m`（[HLD 2.3.2](30_HLD.md#232-設定ファイル)の表で CMP4 が入っている 6 キー。6.12.2 の `_config_keys` の値を判定する 6 行と同じ）、`_load_required` は `data_dir`（[HLD 2.3.3](30_HLD.md#233-検証と記録)）。

#### 6.1.3 関数の細部

関数ごとに `#####` の見出しを立てる。5.2 など同じ名前の見出しは、重複（MD024）を避けるために `（analyze_terrain_launch）` を付ける。止まるときは、メッセージを `log_error` で出してから `throw ExitRequest(<定数>)` する（1.2 の C++ の規約）。

##### main（analyze_terrain_launch）

`int main(int argc, char* argv[])`（`src/analyze_terrain.cpp`）。1.2 の C++ の規約の止まり方のとおり、次の順に行う。

1. `StartTime start = StartTime::now();`（6.12.2 の「`main` は最初に」）。
2. `cv::setNumThreads(1);`（[HLD 2.9.2](30_HLD.md#292-cmp4-と-opencv-のスレッド)、[DEC28](30_HLD.md#294-設計判断)「OpenCV は 1 スレッドで動かす」。1 の後で、ほかの OpenCV の関数の前。1 回だけ）。
3. `std::vector<std::string> args;` を空で作り、`argc > 1` のときだけ `args.assign(argv + 1, argv + argc);`（`argc` が 0 か 1 のときは空。`argc` が 0 のときに `args(argv + 1, argv + argc)` と書くと範囲が逆になるため、この形にする）。
4. 1 つ目の `try`（`start_log` の前の検査）の前に `Args a; Config config;` を宣言し、`try` の中で順に代入する: `a = parse_args(args);` → `config = load_config(a.config_path, _load_keys, _load_required);` → `_check_cross(config);`（`try` の中で `Args a = …` と宣言し直さない。外の変数が初期値のまま 5 に渡るため）。`catch (const ExitRequest& e)` で `return e.code;`。`catch (const std::system_error&)` で `return EXIT_USAGE;`（標準エラー出力が読む相手の無いパイプなどで書けず、`log_error` の中の 6.12 の `_emit` が投げたもの。`SIGPIPE` は 6.12 の起動のときの準備で無視されている。捕まえないと 6.12 の `_on_terminate` が終了コード 1 で止めて、HLD の「引数・設定の誤りは終了コード 2」と食い違うため、`start_log` の前に限って捕まえる。`start_log` の前は終わりの行が無いので、1.2 の「`main` は `EXIT_OK` か `ExitRequest` の `code` だけを返す」理由（終わりの行の終了コードとそろえる）を壊さない。5.2 の `main` の 2 と同じ考え）。
5. 2 つ目の `try` の中で、順に: `start_log(config.values.at("log_dir").text, config, "analyze_terrain", args, start);` → `a.wide` なら `run_wide_mode(a.japan_mesh_list, a.n, a.unresolved, config)`、偽なら `run_normal_mode(a.japan_mesh_list, a.has_mesh, a.mesh_codes, config)`。`catch (const ExitRequest& e)` で `return e.code;`。ほかの例外は捕まえない（6.12 の `_on_terminate` が G7 で止める。`start_log` の後の `std::system_error` もここに当たる）。`catch (...)` は置かない（後始末が無い）。
6. 2 つ目の `try` を抜けたら `return EXIT_OK;`。

`start_log` より前に止まる誤り（`parse_args`、`load_config`、`_check_cross`）は、標準エラー出力だけに出て、ログファイルと `log_dir` を作らない（[HLD 3.4.3](30_HLD.md#343-関数)の「ここまでの誤りは、ログファイルを作らずに終了コード 2」。`start_log` が `log_dir` を作るため）。`start_log` の前に受けたシグナルは既定の扱い（6.12.3 の `check_signal`）。

##### _check_cross

`void _check_cross(const Config& config)`（内部。`src/analyze_terrain.cpp`）

`config.values.at("prominence_primary_m").integer >= config.values.at("prominence_final_m").integer` なら、[2.2](#22-ログとメッセージの文面)の CX1 を `log_error` で出して `throw ExitRequest(EXIT_USAGE)`。`{primary}`・`{final}` は 10 進（先頭の `0` なし）、`{primary_source}`・`{final_source}` は `from_file` が真なら `ファイル`、偽なら `デフォルト`、`{config_path}` は `config.path`。どちらもデフォルトのときも比べる（5.2 の `_check_resolved` の 2 と同じ）。

##### parse_args（analyze_terrain_launch）

`Args parse_args(const std::vector<std::string>& args)`（`src/launch.cpp`）。止まるときは、[6.1.4](#614-メッセージ文面)のメッセージを `log_error` で出して `throw ExitRequest(EXIT_USAGE)`（`start_log` の前なので、標準エラー出力だけに出る）。最初に見つけた誤り 1 つで止まる（5.1 の `parse_args` と 5.2 の `_parse_args` と同じ）。引数は、名前と値を別の引数で渡す形だけを受け、順は問わず、同じ名前は 2 回渡せない。`run_pipeline` が渡す 2 つの形（[5.1.3](#513-関数の細部)の `_run_child`・`run_normal_stage`・`run_wide_stage`）が必ず通り、CMP4 を単独で試す人が名前の順を間違えても通るため。次の順に行う。

1. **名前と値を読む**。`args` を左から読む。各位置の引数が次の 6 つの名前のどれかと一致すれば（バイト列の完全一致）、次の引数をその値にして 2 つ進む: `--config`・`--mode`・`--japan-mesh-list`・`--n`・`--unresolved`・`--mesh`。値の引数は `-` で始まっていてもそのまま値にする（1.2 の利用者向けの Python のコマンドの受け方と同じ）。次の誤りは、見つけた位置で止まる:
   - 6 つの名前のどれでもない引数（位置引数、知らない名前、`--config=<パス>` のような `=` の付いた形、`--help`、`--` だけ、空の引数）: LA1（`{arg}` はその引数）。`=` の形を受けないのは、`run_pipeline` が名前と値を別の引数で渡すため（5.1.3 の `_run_child`）。`--help` を受けないのは、内部の起動口だから（[HLD 2.4.2](30_HLD.md#242-共通の書式)。5.2 と同じ）。
   - 名前を読んだとき、その名前がすでに出ていた: LA3（値を見る前に判定する）。
   - 名前が最後の引数で、値が無い: LA2。
2. **必須の名前**。`--config`・`--mode`・`--japan-mesh-list` の順に、無いものの最初で LA4。
3. **`--mode` の値**。`normal` か `wide`（バイト列の完全一致）でなければ LA5。
4. **モードの組み合わせ**。通常（`normal`）で `--n` があれば LA8（`{option}` は `--n`）、無くて `--unresolved` があれば LA8（`--unresolved`）。広域（`wide`）で `--mesh` があれば LA8（`--mesh`）。続けて、広域で `--n`・`--unresolved` の順に、無いものの最初で LA4。[HLD 4.14.3](30_HLD.md#4143-異常系)の「`--mesh` が付いている」は、この組み合わせの誤りとして見る。
5. **`--n` の値**（広域だけ）。値が 1 バイトで `4`・`5`・`6` のどれかでなければ LA7（`04`・`+4`・先頭に空白の付いた 4・`4.0`・空も LA7）。
6. **絶対パス**。`--config`・`--japan-mesh-list`・`--unresolved`（広域だけ）の順に、値が `/` で始まらないもの（空を含む）の最初で LA6。ファイルがあるか、読めるかはここで見ない（`--config` は `load_config` が CF1・CF2 で、`--japan-mesh-list` は 6.11 の `run_normal_mode`・`run_wide_mode` が 6.12 の `read_mesh_list_file` で R1・R2 として〈終了コード 1〉、`--unresolved` は 6.2 の `read_unresolved_peaks` が見る。HLD 4.4.3・4.14.3）。値は正規化しない（受け取ったまま `Args` に入れる）。
7. **`--mesh`**（通常で、あるときだけ）。`has_mesh = true`、`mesh_value` に値、`mesh_codes = read_mesh_arg(mesh_value)`（6.12。誤りは `read_mesh_arg` が A1〜A5 を出して `ExitRequest(EXIT_USAGE)` で止まり、`parse_args` は捕まえない）。最後に行うのは、ファイルを読む処理を、引数の形の誤りより後にするため。
8. `Args` を返す（6.1.2 の「通常は」の値は、受け取らなかった項目の初期値）。

`{option}` は名前（`--n` など）、`{value}`・`{arg}` は受け取った値を [2.2](#22-ログとメッセージの文面)の引用の決まりで書いたもの（内部の関数 `_quote_arg`。6.12.3 の同じ名前の関数と同じ決まりで、`src/launch.cpp` の無名の名前空間に別に置く。6.12 のものは `src/common.cpp` の中だけの関数で呼べないため）。`{mode}` は `normal` か `wide`。

#### 6.1.4 メッセージ文面

書き方は [2.2](#22-ログとメッセージの文面)。どれも終了コード 2。CX1 は 2.2、A1〜A5・CF1〜CF7 は [2.1.4](#214-メッセージ文面)（と [6.12.4](#6124-メッセージ文面)の違い）にあり、ここに写さない。`{option}`・`{value}`・`{arg}`・`{mode}` の作り方は 6.1.3 の `parse_args`。

| 記号 | 場面 | 1 行目（`ERROR:` と空白 1 つの後） | 2 行目（`対処:` と空白 1 つの後） |
|---|---|---|---|
| LA1 | 受け付けない引数 | `analyze_terrain の知らない引数: {arg}` | `analyze_terrain は run_pipeline が起動する内部の起動口。使える名前は --config・--mode・--japan-mesh-list・--n・--unresolved・--mesh で、値は次の引数で渡す` |
| LA2 | 値が無い | `{option} の値が無い` | `{option} の後に値を渡す` |
| LA3 | 同じ名前を 2 回 | `{option} を 2 回渡した` | `{option} は 1 回だけ渡す` |
| LA4 | 必須の名前が無い | `{option} が無い` | `--config・--mode・--japan-mesh-list は必ず渡し、--mode wide ではさらに --n・--unresolved を渡す` |
| LA5 | `--mode` の値が違う | `--mode の値が違う: {value}` | `--mode には normal か wide を渡す` |
| LA6 | 絶対パスでない | `{option} のパスが絶対パスでない: {value}` | `{option} に絶対パスを渡す` |
| LA7 | `--n` の値が違う | `--n の値が違う: {value}` | `--n には 4・5・6 のどれかを渡す` |
| LA8 | モードに合わない名前 | `{option} は --mode {mode} と一緒に使えない` | `--n と --unresolved は --mode wide だけ、--mesh は --mode normal だけで使う` |

表は 5.2.4 の列から終了コードの列を除いた 4 列にした（どれも 2 なので、終了コードは表の前の 1 文に書いた）。`{arg}` が空の引数なら `''`（2.2 の引用の決まり）。

#### 6.1.5 UT 候補

すべて自動。GoogleTest のテストのケースごとに `// trace: UT-analyze_terrain_launch-NN` を付ける。表の準備の列の共通の準備は次の 3 つ。ケースに固有の準備は、その後に書く。期待の「誤りの 2 行」は、6.1.4 の文面に値を入れた `ERROR:` と `対処:` の 2 行で、そのとき標準出力は空。G7（2.2）の 2 行も同じ形で、標準エラー出力でも、ログファイルの行（時刻と空白を除いた文面）でも、1 行目は `ERROR:` と空白 1 つで、2 行目は `対処:` と空白 1 つで始まる。表の中の「01」「04 の (a)」のように番号だけで指すものは、この表のその番号のケースの入力を指す。

- **同じプロセス**: 6.12.5 の「同じプロセス」と同じ（記述子 1・2 を一時のファイルに付け替えて捕まえ、`ExitRequest` を捕まえて `code` を確かめる）。`parse_args` を直接呼ぶ。`--mesh` のファイルを使うケースは、一時のディレクトリにファイルを書く。
- **起動**: `build/test_launch_main` を子のプロセスで起動する。パスは、テストの実行ファイルの置き場（`readlink("/proc/self/exe")` の親のディレクトリ）の `test_launch_main`。親は `std::fflush(nullptr)` の後に `fork` し、子は記述子 1・2 を親が読む 2 つのパイプの書く側に付け替えて元の 4 つの記述子を閉じ、`unsetenv("STUB_STAGE")` で親から受け継いだ値を必ず消してから、ケースが `STUB_STAGE`（下のスタブの動き）を書いたときだけ `setenv` で付けて、`execv(<パス>, <argv>)` する（`argv[0]` は `analyze_terrain`）。`execv` が戻ったら子は `_exit(127)`。親は 6.12.5 の「子のプロセス」と同じく、2 つのパイプを `poll` で EOF まで読み、`waitpid` の終了状態（シグナルで死んでいたら、そのシグナルの番号を期待と比べる。期待に無ければケースの失敗）とログファイル（`<log_dir>` の下の `analyze_terrain_*_<子の PID>.log`）を確かめる。設定ファイルは、親が一時のディレクトリ `<tmp>` に置く（ケースが書かなければ `[paths]` に `data_dir = <tmp>/data` と `log_dir = <tmp>/logs` だけ）。1 つの ID の中で入力を (a)(b) などに分けたケースは、入力ごとに `<tmp>` を新しく作る（先の入力が `start_log` で作った `<tmp>/logs` を、後の入力の「`<tmp>/logs` が無い」の確かめに残さないため）。引数はケースが書かなければ、通常の `--config <tmp>/config.ini --mode normal --japan-mesh-list /nonexistent/j.txt`（スタブは日本全土のリストを読まないので、ファイルは無くてよい）。
- **段の進行のスタブ**（`tests/src/stub_stage.cpp`。`"stage.hpp"`・`"common.hpp"`・`<opencv2/core.hpp>` を読み、宣言の形がずれたらコンパイルで分かるようにする）: `run_normal_mode` は `log_info("stub: run_normal_mode japan=" + japan_mesh_list + " has_mesh=" + (has_mesh ? "1" : "0") + " meshes=" + <mesh_codes を昇順に , でつないだもの> + " threads=" + std::to_string(cv::getNumThreads()) + " data_dir=" + config.values.at("data_dir").text)` を出す。`run_wide_mode` は `log_info("stub: run_wide_mode japan=" + japan_mesh_list + " n=" + std::to_string(n) + " unresolved=" + unresolved + " threads=" + std::to_string(cv::getNumThreads()) + " data_dir=" + config.values.at("data_dir").text)` を出す。どちらも出した後、`std::getenv("STUB_STAGE")` が `exit1` なら `log_error("stub", "stub")` の後に `throw ExitRequest(EXIT_ERROR)`、`runtime` なら `throw std::runtime_error("stub runtime")`、`sigterm` なら `raise(SIGTERM)` の後に `check_signal()`、それ以外（無いときを含む）は戻る。スタブの動きを環境変数で選ぶのは、試験用の実行ファイルを 1 本にして、段が止まる 3 つの経路（`ExitRequest`、捕まらない例外、シグナル）を `main` の外から作れるようにするため。スタブはテストの準備で、製品のコードは環境変数を読まない（[HLD 2.3.1](30_HLD.md#231-受け渡す値の種類)の「環境変数では設定を受け取らない」に当たらない）。

| ID | 確かめること | 準備 | 入力 | 期待 |
|---|---|---|---|---|
| `UT-analyze_terrain_launch-01` | 通常の最小の形 | 同じプロセス | `--config /c/a.ini --mode normal --japan-mesh-list /p/j.txt` | `config_path` `/c/a.ini`、`wide` 偽、`japan_mesh_list` `/p/j.txt`、`n` 0、`unresolved` 空、`has_mesh` 偽、`mesh_value` 空、`mesh_codes` 空。出力なし |
| `UT-analyze_terrain_launch-02` | 通常の `--mesh`（コード） | 同じプロセス | 01 の後に `--mesh 5339` | `has_mesh` 真、`mesh_value` `5339`、`mesh_codes` `{5339}`。ほかは 01 と同じ |
| `UT-analyze_terrain_launch-03` | 通常の `--mesh`（相対パスのファイル） | 同じプロセス。一時のディレクトリに `m.txt`（`MV-02` の中身）を書き、作業ディレクトリをそこへ移す（呼んだ後に戻す） | 01 の後に `--mesh m.txt` | `mesh_value` `m.txt`、`mesh_codes` は `MV-02` の期待の集合 |
| `UT-analyze_terrain_launch-04` | 広域の形と、名前の順によらないこと | 同じプロセス | (a) `--config /c/a.ini --mode wide --japan-mesh-list /p/j.txt --n 5 --unresolved /d/u.csv`、(b) 同じ名前と値を `--unresolved /d/u.csv --n 5 --mode wide --japan-mesh-list /p/j.txt --config /c/a.ini` の順で | どちらも `wide` 真、`n` 5、`unresolved` `/d/u.csv`、`has_mesh` 偽、ほかは 01 と同じ |
| `UT-analyze_terrain_launch-05` | 値は `-` で始まっても値 | 同じプロセス | `--config --mode --mode normal --japan-mesh-list /p/j.txt` | `code` 2、LA6（`{option}` `--config`、`{value}` `--mode`）の 2 行（1 つ目の `--mode` は `--config` の値として読まれ、LA3 にならない） |
| `UT-analyze_terrain_launch-06` | 受け付けない引数 | 同じプロセス | 01 の後にそれぞれ: (a) `x`、(b) `--help`、(c) `--config=/c/a.ini` を 01 の `--config /c/a.ini` の代わりに、(d) `--`、(e) 空の引数、(f) `--conf /c/a.ini` を 01 の前に | どれも `code` 2、LA1 の 2 行で、`{arg}` は (a) `x`、(b) `--help`、(c) `--config=/c/a.ini`、(d) `--`、(e) `''`、(f) `--conf` |
| `UT-analyze_terrain_launch-07` | 値が無い | 同じプロセス | (a) `--config`、(b) 01 の後に `--mesh` | (a) LA2（`--config`）、(b) LA2（`--mesh`）。どちらも `code` 2 |
| `UT-analyze_terrain_launch-08` | 同じ名前を 2 回 | 同じプロセス | (a) 01 の後に `--mode wide`、(b) 01 の後に `--config` だけ（値なし） | どちらも `code` 2、LA3（(a) は `--mode`、(b) は `--config`。(b) は値を見る前に LA3 で、LA2 にならない） |
| `UT-analyze_terrain_launch-09` | 必須の名前が無い | 同じプロセス | (a) 引数なし、(b) `--mode normal --japan-mesh-list /p/j.txt`、(c) `--config /c/a.ini --japan-mesh-list /p/j.txt`、(d) `--config /c/a.ini --mode normal`、(e) `--config /c/a.ini --mode wide --japan-mesh-list /p/j.txt --unresolved /d/u.csv`、(f) `--config /c/a.ini --mode wide --japan-mesh-list /p/j.txt --n 4` | どれも `code` 2、LA4 で `{option}` は (a) `--config`、(b) `--config`、(c) `--mode`、(d) `--japan-mesh-list`、(e) `--n`、(f) `--unresolved` |
| `UT-analyze_terrain_launch-10` | `--mode` の値 | 同じプロセス | 01 の `normal` を (a) `Normal`、(b) 空、(c) `wide` の後に空白 1 つを付けたもの に | どれも `code` 2、LA5 で `{value}` は (a) `Normal`、(b) `''`、(c) `wide` と空白を `'` で囲んだもの |
| `UT-analyze_terrain_launch-11` | `--n` の値 | 同じプロセス | 04 の (a) の `5` を、(a) `4`、(b) `6`、(c) `3`、(d) `7`、(e) `04`、(f) `+4`、(g) 空、(h) `4.0` に | (a)(b) は `n` 4・6。(c)〜(h) は `code` 2、LA7 で `{value}` はその値（(g) は `''`） |
| `UT-analyze_terrain_launch-12` | 絶対パス | 同じプロセス | (a) 01 の `/c/a.ini` を `a.ini`、(b) 01 の `/p/j.txt` を `j.txt`、(c) 04 の (a) の `/d/u.csv` を `u.csv`、(d) 01 の `/c/a.ini` を空、(e) (a) と (b) を両方 | どれも `code` 2、LA6 で (a) `--config`・`a.ini`、(b) `--japan-mesh-list`・`j.txt`、(c) `--unresolved`・`u.csv`、(d) `--config`・`''`、(e) `--config`・`a.ini`（最初の 1 つだけ） |
| `UT-analyze_terrain_launch-13` | モードの組み合わせ | 同じプロセス | (a) 01 の後に `--n 4`、(b) 01 の後に `--unresolved /d/u.csv`、(c) 04 の (a) の後に `--mesh 5339`、(d) 01 の後に `--n 9 --unresolved u.csv` | どれも `code` 2、LA8 で (a) `--n`・`normal`、(b) `--unresolved`・`normal`、(c) `--mesh`・`wide`、(d) `--n`・`normal`（`--n` の値と絶対パスの誤りより先） |
| `UT-analyze_terrain_launch-14` | 検査の順 | 同じプロセス | (a) `--mesh 12 --mode normal`（`--config` と `--japan-mesh-list` が無い）、(b) `--config a.ini --mode bad --japan-mesh-list /p/j.txt`、(c) 04 の (a) の `--n 5` を `--n 9` に、`/d/u.csv` を `u.csv` に | (a) LA4（`--config`。`--mesh` の誤りにならない）、(b) LA5（LA6 より先）、(c) LA7（LA6 より先）。どれも `code` 2 |
| `UT-analyze_terrain_launch-15` | `--mesh` の誤りは `read_mesh_arg` のまま | 同じプロセス | 01 の後に (a) `--mesh ''`、(b) `--mesh /nonexistent/m.txt` | どちらも `code` 2。(a) は A1、(b) は A2（`{path}` は `/nonexistent/m.txt`）の 2 行（2.1.4 の文面。6.12 の `read_mesh_arg` のとおり） |
| `UT-analyze_terrain_launch-16` | 通常の起動 | 起動 | 既定の引数の後に `--mesh 5339` | 終了コード 0。標準出力は L1（`開始: analyze_terrain --config <tmp>/config.ini --mode normal --japan-mesh-list /nonexistent/j.txt --mesh 5339`）、L2 の行（設定ファイルの行と 6 キーの行）、`stub: run_normal_mode japan=/nonexistent/j.txt has_mesh=1 meshes=5339 threads=1 data_dir=<tmp>/data`、L3（終了コード 0）の順。標準エラー出力は空。ログファイルが 1 つあり、同じ行がこの順で時刻付きで並ぶ（`threads=1` が `cv::setNumThreads(1)` の呼び忘れを見分けるのは、CPU が 2 つ以上の計算機だけ） |
| `UT-analyze_terrain_launch-17` | 広域の起動 | 起動。日本全土のリストと未確定のリストのファイルは置かない | `--config <tmp>/config.ini --mode wide --japan-mesh-list /nonexistent/j.txt --n 4 --unresolved /nonexistent/u.csv` | 終了コード 0。標準出力に `stub: run_wide_mode japan=/nonexistent/j.txt n=4 unresolved=/nonexistent/u.csv threads=1 data_dir=<tmp>/data` が L2 の後、L3（終了コード 0）の前に 1 行 |
| `UT-analyze_terrain_launch-18` | 引数の誤りではログを作らない | 起動 | 既定の引数から `--mode normal` を除く | 終了コード 2。標準エラー出力は LA4（`--mode`）の 2 行だけ、標準出力は空。`<tmp>/logs` が無い |
| `UT-analyze_terrain_launch-19` | 設定の誤りではログを作らない | 起動。設定ファイルを置かない | 既定の引数 | 終了コード 2。標準エラー出力は CF1（`<tmp>/config.ini`、対処は `--config に渡したパスを確かめる`）の 2 行だけ。標準出力は空。`<tmp>/logs` が無い |
| `UT-analyze_terrain_launch-20` | 相互制約 | 起動。設定ファイルの `[analysis]` に `prominence_primary_m` を書く（値は入力ごと。`prominence_final_m` は書かない） | (a) `prominence_primary_m = 149`、(b) `prominence_primary_m = 150` | (a) 終了コード 0、スタブの行が出る。(b) 終了コード 2、標準エラー出力は CX1 の 2 行だけで、1 行目は `ERROR: プロミネンス一次フィルタ閾値が最終フィルタ閾値以上: [analysis] prominence_primary_m = 150（ファイル）、[merge] prominence_final_m = 150（デフォルト）（<tmp>/config.ini）`、標準出力は空、`<tmp>/logs` が無い |
| `UT-analyze_terrain_launch-21` | 段が止まったときの終了コード | 起動。`STUB_STAGE=exit1` | 既定の引数 | 終了コード 1。標準エラー出力は `ERROR: stub` と `対処: stub`。ログファイルの最後の行は L3（終了コード 1） |
| `UT-analyze_terrain_launch-22` | 捕まらない例外 | 起動。`STUB_STAGE=runtime` | 既定の引数 | 終了コード 1。標準エラー出力に G7（`{type}` は `std::runtime_error`、`{message}` は `stub runtime`）の 2 行。ログファイルにも同じ G7 の 2 行（1 行目は `ERROR: 予期しない例外で止まった: std::runtime_error: stub runtime`）があり、最後の行は L3（終了コード 1） |
| `UT-analyze_terrain_launch-23` | シグナルで止まる | 起動。`STUB_STAGE=sigterm` | 既定の引数 | 終了コード 143（`waitpid` の終了状態は正常終了で 143。シグナルで死んでいない）。ログファイルの最後の行は `SIGTERM` を受けて止まった形の L3（143） |
| `UT-analyze_terrain_launch-24` | 標準エラー出力に書けないときの `start_log` の前の誤り | 起動。ただし標準エラー出力は、読む側を閉じた `pipe` の書く側にする（読む相手のいない標準エラー出力。親が `pipe` を作り、`fork` の前に読む側を閉じ、子は書く側を記述子 2 に付け替える。親は標準出力のパイプだけを読む）。設定ファイルは入力ごと | (a) 既定の引数から `--mode normal` を除く（LA4）、(b) 設定ファイルを置かない（CF1）、(c) 設定ファイルの `[analysis]` に `prominence_primary_m = 150` を書く（20 の (b) と同じ。CX1） | どれも終了コード 2（1 でない）。標準出力は空。`<tmp>/logs` が無い |

### 6.2 `analyze_terrain_target`

- **ID**: LLD-analyze_terrain_target
- **対応 HLD**: [3.4](30_HLD.md#34-cmp4-地形解析エンジン)・[4.4](30_HLD.md#44-fr-004-33メッシュ結合解析オーケストレーション)・[4.7](30_HLD.md#47-fr-007-per-mesh-csv-出力プロミネンス閾値適用)・[4.14](30_HLD.md#414-fr-014-広域結合解析オーケストレーション)
- **ファイル**: `src/target.hpp`・`src/target.cpp`

関数の名前と役割は [HLD 3.4.3](30_HLD.md#343-関数) の表の「対象」の群で、処理の正本は [HLD 4.4.2](30_HLD.md#442-処理の流れ) の 3「対象メッシュを決める」（通常モード）と [4.14.2](30_HLD.md#4142-処理の流れ) の 2「入力を読む」・3「対象メッシュを決める」（広域モード）、止まる場面とメッセージに含める内容は [4.4.3](30_HLD.md#443-異常系)・[4.14.3](30_HLD.md#4143-異常系) である。日本全土1次メッシュコードリストと北方領土除外メッシュリストを読むのは 6.11 の `run_normal_mode`・`run_wide_mode`（6.12 の `read_mesh_list_file`）で、6.2 は読んだ集合を受け取る。所属メッシュは 6.10 の `latlon_to_mesh`、全球の Z15 の画素は 6.10 の `latlon_to_z15_pixel` で求める（画素の使い方は [HLD 4.7.2](30_HLD.md#472-処理の流れ) の 5「対象ピークの照合」）。この節は、それを C++ で書くための細部を足す。1.2 の C++ の規約に従う。

#### 6.2.1 ファイル割付

- 公開の宣言は `src/target.hpp`、定義と内部の関数は `src/target.cpp` に置く。どちらも先頭のコメントに `// trace: LLD-analyze_terrain_target` を書き、ヘッダーは次の行を `#pragma once` にする。
- `src/target.hpp` は `"convert.hpp"`（`Z15Pixel`）・`<map>`・`<set>`・`<string>`・`<vector>` を読む。`src/target.cpp` は `"target.hpp"`・`"common.hpp"`・`"convert.hpp"`・`<cerrno>`・`<charconv>`・`<cstring>`・`<fcntl.h>`・`<stdexcept>`・`<string>`・`<system_error>`・`<unistd.h>`・`<utility>` を読む。OpenCV のヘッダーは読まない。
- UT のコードは `tests/src/test_target.cpp` に置き、`build/test_target` にビルドする（[2.5](#25-ビルドとテストの名前)。`src/` の `main` を持たない `.cpp` をすべてリンクするので、`common.cpp`・`convert.cpp` も入る）。各テストに `// trace: UT-analyze_terrain_target-NN`（確かめる UT 候補の ID）のコメントを付ける。2.4 の表の行を写したテストには、写した表の名前（`2.4 の表 6` など）もコメントに書く（[テスト方針書 3.3](02_test_policy.md#33-期待値の根拠)）。テストの枠組みは GoogleTest（[テスト方針書 3.4](02_test_policy.md#34-テストを先に書く進め方)）。

#### 6.2.2 型とデータ

`src/target.hpp` の公開の宣言は次のとおり（名前空間に入れない。1.2 の C++ の規約）。

```cpp
#pragma once
#include <map>
#include <set>
#include <string>
#include <vector>
#include "convert.hpp"

struct SkippedMesh {
    std::string code;        // --mesh のコード
    bool excluded = false;   // 真なら北方領土除外メッシュ、偽なら日本全土1次メッシュコードリストに無い
};

struct TargetMeshes {
    std::vector<std::string> targets;       // 対象メッシュ（コードの昇順）
    std::vector<SkippedMesh> skipped;       // --mesh のうち飛ばしたもの（コードの昇順）
    std::vector<std::string> not_targeted;  // 日本全土1次メッシュコードリストにある北方領土除外メッシュ（コードの昇順）
};

struct UnresolvedPeak {
    std::string lat_text;   // peak_lat の文字列（読んだまま）
    std::string lon_text;   // peak_lon の文字列（読んだまま）
    double lat = 0.0;       // lat_text を数にした値
    double lon = 0.0;       // lon_text を数にした値
};

struct TargetPeak {
    UnresolvedPeak peak;
    Z15Pixel pixel;         // latlon_to_z15_pixel(peak.lat, peak.lon)
};

using PeakGroups = std::map<std::string, std::vector<TargetPeak>>;   // 鍵は対象メッシュのコード

TargetMeshes select_target_meshes(const std::set<std::string>& japan,
                                  const std::set<std::string>& excluded,
                                  bool has_mesh,
                                  const std::set<std::string>& mesh_codes);
std::vector<UnresolvedPeak> read_unresolved_peaks(const std::string& path, int n);
PeakGroups group_peaks_by_mesh(const std::vector<UnresolvedPeak>& peaks,
                               const std::set<std::string>& japan,
                               const std::set<std::string>& excluded);
```

- `japan` は日本全土1次メッシュコードリスト、`excluded` は北方領土除外メッシュリストを、6.12 の `read_mesh_list_file` で読んだ集合（6.11 が読んで渡す）。`has_mesh`・`mesh_codes` は 6.1 の `Args` の同じ名前の値（[6.1.2](#612-型とデータ) の `run_normal_mode` の宣言）。`n` は `--n` の値（[6.1.2](#612-型とデータ) の `run_wide_mode` の宣言）。
- `PeakGroups` は `std::map` なので、鍵の順（4 バイトの ASCII の数字の辞書順で、コードの数の昇順に当たる）が [HLD 4.14.2](30_HLD.md#4142-処理の流れ) の 3「対象メッシュを決める」の「対象メッシュはコードの昇順」になる。対象メッシュの並びを別に持たない（並びと鍵が食い違わないようにするため）。組の中の対象ピークの順は、`read_unresolved_peaks` が返した順。
- 構造体は、6.10・6.12 と同じく名前で読める形にし、値の有無を持つ型（`std::optional`）を使わない（1.2）。`TargetPeak` が `UnresolvedPeak` を持つのは、[HLD 3.4.3](30_HLD.md#343-関数) が、`group_peaks_by_mesh` は `read_unresolved_peaks` の返すもの（文字列とその数の値）に Z15 の画素の座標を足して返すとしているため。文字列を持つのは、メッセージに読んだままの値を出すため。

#### 6.2.3 関数の細部

処理の正本は上の前置きのとおりで、この節は C++ で書くための細部を足す。どの関数も `check_signal` を呼ばない（[HLD 3.4.3](30_HLD.md#343-関数) の `check_signal` を呼ぶ群に「対象」は入っていない。リストの読み込みと集合の操作だけで、時間がかからない）。止まるときは、メッセージを `log_error` で出してから `throw ExitRequest(EXIT_ERROR)` する（1.2 の C++ の規約）。呼ぶ側の誤りは `std::invalid_argument` を投げる（6.10・6.12 と同じ。`main` は捕まえないので、6.12 の `_on_terminate` が G7 で止める）。3 つの関数は、通常のログも警告も出さない（`select_target_meshes` の警告とログは、返したものを 6.11 の `run_normal_mode` が [6.2.4](#624-メッセージ文面) の文面で出す）。

関数ごとに `#####` の見出しを立てる。

##### select_target_meshes

`TargetMeshes select_target_meshes(const std::set<std::string>& japan, const std::set<std::string>& excluded, bool has_mesh, const std::set<std::string>& mesh_codes)`

1. `has_mesh` が偽で `mesh_codes` が空でなければ、`std::invalid_argument("select_target_meshes: has_mesh が偽なのに mesh_codes が空でない")`。
2. `not_targeted` は、`japan` の要素のうち `excluded` にあるもの（昇順）。`has_mesh` によらず求める（[HLD 4.4.2](30_HLD.md#442-処理の流れ) の 3「対象メッシュを決める」の「どちらのときも」）。
3. `has_mesh` が偽なら、`targets` は `japan` の要素のうち `excluded` に無いもの（昇順）。`skipped` は空。
4. `has_mesh` が真なら、`mesh_codes` を昇順に見て、`japan` に無ければ `skipped` に `{code, false}`、`japan` にあって `excluded` にあれば `{code, true}`、どちらでもなければ `targets` に足す。`japan` に無いことを先に見る（北方領土除外メッシュリストにあって日本全土1次メッシュコードリストに無いコードは「日本全土1次メッシュコードリストに無い」にする。4.1 の TW1・TW2 と同じ順）。
5. 止まらない。`targets` が空でも返す（0 件のときの結果の要約と終了コード 0 は 6.11。[HLD 4.4.2](30_HLD.md#442-処理の流れ) の 3「対象メッシュを決める」）。

##### read_unresolved_peaks

`std::vector<UnresolvedPeak> read_unresolved_peaks(const std::string& path, int n)`（`n` は `--n` の値）

1. `n` が 4・5・6 のどれでもなければ、`std::invalid_argument("read_unresolved_peaks: n が 4・5・6 でない: " + std::to_string(n))`。
2. `_read_file(path, data, err)`（下）で全部を読む。失敗したら UP1（`{reason}` は `std::strerror(err)`。無いファイルは `No such file or directory`、ディレクトリは `Is a directory`）を出して止まる。
3. `data` の先頭が `EF BB BF` なら、その 3 バイトを 1 つだけ除く。UTF-8 として読めるかは見ない（値は ASCII の数字などだけを受け、ほかのバイトは 6 で数として読めない）。
4. `\n` のバイトで行に分け、1 から番号を振る。各行の末尾の `\r` を 1 バイトだけ除く（CMP5 が `\r\n` で書いても読めるように）。1 行目が見出しの行。
5. 見出しの行: `data` が空か 1 行目が空なら UP2（`{detail}` は `見出しの行が無い`）。1 行目を `,` で分けた列の名前のうち、`peak_lat` と `peak_lon` がちょうど 1 つずつでなければ UP2（`{detail}` は `見出しの行に peak_lat と peak_lon の列が 1 つずつ無い: {line}`）。列の名前はバイト列のまま比べ、前後の空白を除かず、引用符（`"`）を特別に扱わない（`"peak_lat"` は別の名前）。ほかの列があってもよく、並びは問わない（[HLD 4.14.2](30_HLD.md#4142-処理の流れ) の 2「入力を読む」の「見出しの行に `peak_lat` と `peak_lon` の列があり」）。
6. 2 行目から: 空の行（`\r` を除いた後に 0 バイト）は飛ばす（末尾の改行の後の空の行も同じ）。ほかの行は `,` で分け、列の数が見出しの行と違えば UP2（`{detail}` は `{line_no} 行目の列の数が見出しの行と違う: {line}`）。`peak_lat`・`peak_lon` の列の値が下の「数として読める」に当たらなければ UP2（`{detail}` は `{line_no} 行目の peak_lat か peak_lon が数として読めない: {line}`）。誤りは、ファイルの順で最初の 1 つだけを出して止まる。
7. 数として読める: 値のバイト列が、ASCII の `+` か `-` が 0 個か 1 個、ASCII の数字が 1 個以上、続けて `.` と ASCII の数字 1 個以上が 0 回か 1 回、の形（ほかのバイトを含まない）で、先頭の `+` を除いた残りを `std::from_chars`（`std::chars_format::fixed`）に渡して `ec` が `std::errc{}` で、全部を読んだ（`ptr` が末尾）とき。`1e5`・`35.`・`.5`・`NaN`・`inf`・前後の空白・全角の数字・空は読めない。`std::from_chars` が `std::errc::result_out_of_range` を返す桁数の値（有限の倍精度に入らない）も読めない。緯度経度として正しい範囲かはここでは見ない（[HLD 4.14.2](30_HLD.md#4142-処理の流れ) の 2「入力を読む」は数として読めることだけを求め、範囲の外は `group_peaks_by_mesh` が止める）。形を先に決めるのは、`std::from_chars` が受ける `inf`・`nan`・指数の書き方を処理系に任せずに止めるため。リストの値は CMP5 が `merged_peak.csv` の文字列（CMP4 の `format_coord` が書いた小数点 8 桁）をそのまま写したもの（[HLD 4.22.2](30_HLD.md#4222-処理の流れ) の 4「未確定のリストを書く」、DEC107）なので、この形で足りる。
8. 重なり: 読んだ値の組 `(lat, lon)` が、返す並びに入れた行の組と `==` で等しければ、その行を足さない（先の行の文字列を残す。`35.5` と `35.50` は同じ座標）。[HLD 4.14.2](30_HLD.md#4142-処理の流れ) の 2「入力を読む」の「同じ座標の行が重なっていれば 1 件にまとめる」の「同じ座標」は文字列でなく座標の意味なので、数の値で比べる。
9. ファイルの順に返す。データの行が無ければ空の並び（0 件のときの結果の要約と終了コード 0 は 6.11。[HLD 4.14.2](30_HLD.md#4142-処理の流れ) の 2「入力を読む」）。

- `{path}` は受け取った `path` のまま（`run_pipeline` が絶対パスで渡す。[HLD 2.4.5](30_HLD.md#245-内部引数)）。`{line}` は 4 で `\r` を除いた後の行のバイト列のまま。`{line_no}` は 10 進（先頭の `0` なし）。
- `_read_file`（内部。`src/target.cpp` の無名の名前空間）: 6.12.3 の内部の小さな関数の `_read_file` と同じ決まり（`open(path, O_RDONLY | O_CLOEXEC)` と `read` を `EINTR` のほかの失敗か 0 まで繰り返し、`close`。失敗は `err` に `errno`）。6.12 の内部の関数はほかの `.cpp` から呼べないので、同じ形を置く。

##### group_peaks_by_mesh

`PeakGroups group_peaks_by_mesh(const std::vector<UnresolvedPeak>& peaks, const std::set<std::string>& japan, const std::set<std::string>& excluded)`

1. `peaks` を順に見て、`code = latlon_to_mesh(peak.lat, peak.lon)`。次の順に当てる: `code` が空なら「範囲の外（コードなし）」、`peak.lon >= 180.0` なら「経度が範囲の外」（`code` は控える）、`japan` に無ければ「日本全土1次メッシュコードリストに無い」、`excluded` にあれば「北方領土除外メッシュ」として控える（控えたものは組に入れない）。どれでもなければ、`pixel = latlon_to_z15_pixel(peak.lat, peak.lon)` を求め（[HLD 4.7.2](30_HLD.md#472-処理の流れ) の 5「対象ピークの照合」の「組ごとに 1 回求め」。ここで 1 回だけ求め、6.4 と 6.7 はこの値を使う）、`groups[code]` の末尾に `{peak, pixel}` を足す。
2. 全部を見た後、控えたものが 1 つ以上あれば UP3 を出して `throw ExitRequest(EXIT_ERROR)`（出力を作らずに止まる。[HLD 4.14.2](30_HLD.md#4142-処理の流れ) の 3「対象メッシュを決める」、DEC51）。
3. 控えたものが無ければ `groups` を返す。`peaks` が空なら空の `PeakGroups`。

- 全部を見てから挙げるのは、リストの書き換えか、日本全土か北方領土除外のリストの変更で起きるので、1 件ずつ止めると直すたびに起動し直すことになるため（HLD の DEC49「読めないタイルでは窓のタイルを読み終えてから挙げて止める」と同じ考え）。全件を挙げる（[HLD 4.14.3](30_HLD.md#4143-異常系) の必ず含める内容は「ピークの緯度経度と所属メッシュのコード」で、件数の上限を書いていない）。
- `latlon_to_z15_pixel` を呼ぶ値は、6.10.3 の渡せる範囲に入る。`latlon_to_mesh` が空でないコードを返すのは緯度が 0 以上 200/3 未満・経度が 100 以上 200 未満のときだけ（6.10.3 の 0〜99 の条件）で、残る経度 180 以上を 1 の「経度が範囲の外」で除くため。経度 180 以上はコードが作れる（`(35.5, 180.5)` は `5380`）が、Web メルカトルのタイルの範囲の外で、日本の 1 次メッシュにならない。日本全土1次メッシュコードリストの中身（4 桁の形だけを確かめる。6.12.3）には頼らない。
- UP3 では、コードが空のピークは「1 次メッシュの範囲の外」と書く（空のコードをそのまま出すと読めない）。経度が 180 以上のピークは、作れたコードを添えて「経度が 180 以上で 1 次メッシュの範囲の外」と書く（[HLD 4.14.3](30_HLD.md#4143-異常系) の必ず含める内容は所属メッシュのコード）。

#### 6.2.4 メッセージ文面

書き方は [2.2](#22-ログとメッセージの文面)。`{path}`・`{line}`・`{line_no}`・`{reason}` は 6.2.3 のとおり。`{n}` は `read_unresolved_peaks` の `n`。`{code}` は、TM1・TM2 では `skipped` の `code`、TM3 では `not_targeted` の 1 件、UP3 の `{peaks}` では 4 桁の所属メッシュのコード。

`ERROR:`・`WARNING:` のメッセージ（2 行目は `対処:` と空白 1 つの後）:

| 記号 | 場面 | 1 行目 | 2 行目 | 終了コード |
|---|---|---|---|---|
| TM1 | `--mesh` のコードが日本全土のリストに無い（`WARNING:`） | `--mesh のメッシュコードを飛ばした（日本全土1次メッシュコードリストに無い）: {code}` | `日本全土1次メッシュコードリスト {list_path} にあるコードを渡す（残りのメッシュは続けて解析する）`（`{list_path}` は `--japan-mesh-list` の値） | 0 |
| TM2 | `--mesh` のコードが北方領土除外メッシュ（`WARNING:`） | `--mesh のメッシュコードを飛ばした（北方領土除外メッシュ）: {code}` | `北方領土除外メッシュは解析しない（残りのメッシュは続けて解析する）` | 0 |
| UP1 | コル未確定ピーク座標リストを読めない | `コル未確定ピーク座標リストを読めない: {path}: {reason}` | `{redo}` | 1 |
| UP2 | コル未確定ピーク座標リストの書式が違う | `コル未確定ピーク座標リストの書式が違う: {path}: {detail}`（`{detail}` は 6.2.3 の `read_unresolved_peaks` の 5・6 のとおり） | `{redo}` | 1 |
| UP3 | 対象ピークの所属メッシュが解析の対象でない | `所属メッシュが解析の対象でない対象ピークがある: {count} 件: {peaks}` | `日本全土1次メッシュコードリストか北方領土除外メッシュリストを、このリストを作った後に変えたか、リストを手で書き換えたときに起きる。設定ファイルの data_dir の下の results/csv/ の中を消してから、scripts/run_pipeline.sh を --phase を付けずに起動し、フェーズ2 から通しでやり直す（設定ファイルを指定して起動したときは、同じ --config を付ける）` | 1 |

- `{redo}`: `n` が 4 なら `scripts/run_pipeline.sh --phase 2 を起動し直して、このリストを作り直す（設定ファイルを指定して起動したときは、同じ --config を付ける）`、5・6 なら `scripts/run_pipeline.sh --phase 3 --n {n−1} を起動し直して、このリストを作り直す（設定ファイルを指定して起動したときは、同じ --config を付ける）`（`{n−1}` は `n − 1` の 10 進）。[HLD 4.14.3](30_HLD.md#4143-異常系) の表の「そのリストを作った段をやり直す案内」である。
- `{count}` は控えた件数の 10 進。`{peaks}` は控えたものを `peaks` の順にすべて、1 件を `{lat_text},{lon_text}（{code}、日本全土1次メッシュコードリストに無い）`・`{lat_text},{lon_text}（{code}、北方領土除外メッシュ）`・`{lat_text},{lon_text}（{code}、経度が 180 以上で 1 次メッシュの範囲の外）`（コードが作れて経度が 180 以上のとき）・`{lat_text},{lon_text}（1 次メッシュの範囲の外）`（コードが空のとき）のどれかにして `、` でつないだもの。
- TM1・TM2 は 4.1 の TW1・TW2 と同じ形で、「取得」を「解析」に替えたもの（[HLD 4.4.3](30_HLD.md#443-異常系) の「スキップしたコードと理由」）。2.2 の「各プログラムの起動の引数の誤りは、文面が同じになっても、それぞれのモジュールの節に置く」と同じ考えで、共通の表にしない。

通常のログに出す行（`log_info` で標準出力とログファイルに出す）:

| 記号 | 行 | 文面 |
|---|---|---|
| TM3 | 対象メッシュにしなかった北方領土除外メッシュ | `北方領土除外メッシュなので対象メッシュにしなかった: {code}`（`not_targeted` の 1 件ごとに 1 行。[HLD 4.4.2](30_HLD.md#442-処理の流れ) の 3「対象メッシュを決める」、ADR-SRS-053） |

出し方: 6.11 の `run_normal_mode` は `select_target_meshes` の後に、`skipped` を順に TM1・TM2 の `log_warning` で 1 件ずつ、続けて `not_targeted` を順に TM3 の `log_info` で 1 件ずつ出す。UP1〜UP3 は 6.2 の関数が出す。

#### 6.2.5 UT 候補

すべて自動。GoogleTest のケースごとに `// trace: UT-analyze_terrain_target-NN` を付ける。共通の準備は 1 つ。

- **同じプロセス**: テストのプロセスの中で対象の関数を直接呼ぶ（`start_log` を呼ばない。6.12.5 の「同じプロセス」と同じく、一時のディレクトリを `mkdtemp` で作り、ファイルはその下にバイト列で書いて絶対パスを渡す。標準エラー出力は `dup`・`dup2` で記述子 2 を一時のファイルに付け替えて捕まえ、呼んだ後に戻す）。止まるケースは `ExitRequest` を捕まえて `code` を確かめる。メッセージの期待は、標準エラー出力の 2 行（`ERROR: …` と `対処: …`）の全文。

| ID | 確かめること | 準備 | 入力 | 期待 |
|---|---|---|---|---|
| `UT-analyze_terrain_target-01` | `--mesh` が無いとき | 同じプロセス | `japan` は `{5339, 5340, 6841, 6842}`、`excluded` は `{6841, 6848}`、`has_mesh` は偽、`mesh_codes` は空 | `targets` が `[5339, 5340, 6842]`、`skipped` が空、`not_targeted` が `[6841]`（`6848` は `japan` に無いので入らない）。標準エラー出力に何も出ない |
| `UT-analyze_terrain_target-02` | `--mesh` があるとき | 同じプロセス | `japan`・`excluded` は 01 と同じ、`has_mesh` は真、`mesh_codes` は `{1234, 5339, 6841, 6848}` | `targets` が `[5339]`、`skipped` が `[{1234, 偽}, {6841, 真}, {6848, 偽}]`（`6848` は `japan` に無いので偽）、`not_targeted` が `[6841]` |
| `UT-analyze_terrain_target-03` | `--mesh` のコードがすべて飛ぶとき | 同じプロセス | `japan`・`excluded` は 01 と同じ、`has_mesh` は真、`mesh_codes` は `{1234, 6841}` | 止まらない。`targets` が空、`skipped` が 2 件、`not_targeted` が `[6841]` |
| `UT-analyze_terrain_target-04` | 呼ぶ側の誤り | 同じプロセス | (a) `has_mesh` が偽で `mesh_codes` が `{5339}` の `select_target_meshes`、(b) 正しいリストのファイルで `n` が 3 の `read_unresolved_peaks`、(c) 同じく `n` が 7 | どれも `std::invalid_argument`（`ExitRequest` でない）。標準エラー出力に何も出ない |
| `UT-analyze_terrain_target-05` | リストを読む | 同じプロセス。リストのファイル `peak_lat,peak_lon\n35.12345678,139.12345678\n-0.50000000,+140.5\n` | `read_unresolved_peaks(<パス>, 4)` | 2 件。1 件目の `lat_text`・`lon_text` が `35.12345678`・`139.12345678`、`lat`・`lon` が `35.12345678`・`139.12345678`（C++ の倍精度の字句と `==`）。2 件目の文字列が `-0.50000000`・`+140.5`、値が `-0.5`・`140.5` |
| `UT-analyze_terrain_target-06` | 読み方の幅 | 同じプロセス。10 のファイル | (a) 改行が `\r\n` のファイル、(b) 先頭に BOM（`EF BB BF`）を付けたファイル、(c) 見出しが `foo,peak_lon,peak_lat` で行が `x,139.5,35.5`、(d) `peak_lat,peak_lon\n\n35.5,139.5\n\n36.0,140.0\n\n`（2 行目・4 行目・6 行目が空）、(e) 見出しの後に `35.5,139.5`・`36.0,140.0`・`35.50,139.500` の 3 行（3 行目は 1 行目と同じ座標）、(f) 見出しの行だけ、(g) 05 の中身から末尾の `\n` を除いたもの、(h) `peak_lat,peak_lon\n-0.0,139.5\n0.0,139.5\n`、(i) `peak_lat,peak_lon,foo\n35.5,139.5,\n`（末尾の列が空）、(j) `peak_lat,peak_lon\r\n\r\n35.5,139.5\r\n`（2 行目は `\r` だけ） | (a)(b)(g) は 05 と同じ結果。(c) は 1 件で `lat` が 35.5、`lon` が 139.5。(d) は 2 件（`35.5,139.5`・`36.0,140.0`）。(e) は 2 件で、1 件目の文字列は `35.5`・`139.5`。(f) は空の並び。(h) は 1 件で文字列が `-0.0`（`-0.0 == 0.0` なので 3 行目は重なり）。(i) は 1 件（空の列も 1 列に数え、列の数は 3 で見出しと同じ）。(j) は 1 件。どれも標準エラー出力に何も出ない |
| `UT-analyze_terrain_target-07` | 見出しの誤り | 同じプロセス。6 つのファイル | (a) 0 バイト、(b) 1 行目が空で 2 行目が `peak_lat,peak_lon`、(c) 見出しが `lat,lon`、(d) 見出しが `peak_lat,peak_lon,peak_lat`、(e) 見出しが `"peak_lat","peak_lon"`、(f) BOM（`EF BB BF`）の 3 バイトだけ。どれも `n` は 4 | どれも `code` が 1 の UP2。`{detail}` は (a)(b)(f) が `見出しの行が無い`、(c)(d)(e) が `見出しの行に peak_lat と peak_lon の列が 1 つずつ無い:` と空白 1 つの後に見出しの行のまま |
| `UT-analyze_terrain_target-08` | 値の誤り | 同じプロセス。値ごとに別のファイル（見出しは `peak_lat,peak_lon`、2 行目が `35.5,139.5`、3 行目が誤り） | 3 行目の `peak_lat` の値が (a) `1e5`、(b) `35.`、(c) `.5`、(d) `NaN`、(e) `inf`、(f) 空白 1 つの後に `35.0`、(g) 全角の数字 2 字（U+FF13、U+FF15。UTF-8 で 6 バイト。16 進で `EF BC 93 EF BC 95`、バイトの間の空白は区切り）、(h) 空、(i) `"35.0"`、(j) `1` の後に `0` を 400 個並べた数、(k) `--5`。ほかに (l) 3 行目が `35.5,139.5,1`（列の数が違う）、(m) 3 行目と 5 行目が誤り（3 行目が `x,139.5`、4 行目が正しい行 `36.0,140.0`、5 行目が `y,139.5`） | (a)〜(k) は `code` が 1 の UP2 で、`{detail}` が `3 行目の peak_lat か peak_lon が数として読めない:` と空白 1 つの後に 3 行目のまま。(l) は `3 行目の列の数が見出しの行と違う: 35.5,139.5,1`。(m) は 3 行目だけを挙げる |
| `UT-analyze_terrain_target-09` | リストを読めない | 同じプロセス | (a) 一時のディレクトリの下の存在しないパス、(b) 一時のディレクトリそのもの。どちらも `n` は 4 | どちらも `code` が 1。標準エラー出力が `ERROR: コル未確定ピーク座標リストを読めない: <パス>: No such file or directory`（(b) は `Is a directory`）と、`対処: scripts/run_pipeline.sh --phase 2 を起動し直して、このリストを作り直す（設定ファイルを指定して起動したときは、同じ --config を付ける）` の 2 行 |
| `UT-analyze_terrain_target-10` | やり直しの案内と N | 同じプロセス。09 の (a) のパス | `n` を 5、6 にしてそれぞれ呼ぶ | 2 行目が `対処: scripts/run_pipeline.sh --phase 3 --n 4 を起動し直して、…`（`n` が 6 なら `--n 5`）。1 行目は 09 の (a) と同じ |
| `UT-analyze_terrain_target-11` | 所属メッシュごとの組 | 同じプロセス | `peaks` は 2.4 の表 6 の 3 行目〜5 行目と 2 行目の 4 点を、この順に `{lat_text, lon_text, lat, lon}` にしたもの（`34.99999777,134.99997854`・`34.99999777,135.00002146`・`35.0,135.0`・`36.00465613,139.99880075`）、`japan` は `{5234, 5235, 5439}`、`excluded` は空 | 鍵が `[5234, 5235, 5439]` の順。`5234` の組は 1 件目の点で、画素は表 6 の (7340031, 3322709)。`5235` の組は 2 件目と 3 件目の点がこの順で、画素はどちらも (7340032, 3322709)（座標が違うので重ならない）。`5439` の組は 4 件目の点で、画素は (7456512, 3293952)。各 `TargetPeak` の `peak` は、渡した対応する点と同じ（`lat_text`・`lon_text`・`lat`・`lon` の 4 項目すべてが、4 つの `TargetPeak` のすべてで等しい）。画素は 4 つの `TargetPeak` のすべてで上のとおり |
| `UT-analyze_terrain_target-12` | 所属メッシュが解析の対象でない | 同じプロセス | `peaks` は順に `35.0,135.0`（`5235`）、`35.5,139.5`（`5339`）、`45.5,141.5`（`6841`）、`-10.0,139.0`（範囲の外）、`japan` は `{5235, 6841}`、`excluded` は `{6841}` | `code` が 1。標準エラー出力の 1 行目が `ERROR: 所属メッシュが解析の対象でない対象ピークがある: 3 件: 35.5,139.5（5339、日本全土1次メッシュコードリストに無い）、45.5,141.5（6841、北方領土除外メッシュ）、-10.0,139.0（1 次メッシュの範囲の外）`、2 行目が 6.2.4 の UP3 の対処の文 |
| `UT-analyze_terrain_target-13` | 経度 180 以上 | 同じプロセス | `peaks` は `35.0,135.0`（`5235`）と `35.5,180.5`（コードは `5380`）、`japan` は `{5235, 5380}`、`excluded` は空 | `code` が 1。1 行目が `ERROR: 所属メッシュが解析の対象でない対象ピークがある: 1 件: 35.5,180.5（5380、経度が 180 以上で 1 次メッシュの範囲の外）`（`japan` にあっても範囲の外。`latlon_to_z15_pixel` を呼ばない） |
| `UT-analyze_terrain_target-14` | 対象ピークが無い | 同じプロセス | `peaks` は空、`japan` は `{5235}`、`excluded` は空 | 空の `PeakGroups`。標準エラー出力に何も出ない |

### 6.3 `analyze_terrain_window`

- **ID**: LLD-analyze_terrain_window
- **対応 HLD**: [3.4](30_HLD.md#34-cmp4-地形解析エンジン)・[4.4](30_HLD.md#44-fr-004-33メッシュ結合解析オーケストレーション)・[4.14](30_HLD.md#414-fr-014-広域結合解析オーケストレーション)
- **ファイル**: `src/window.hpp`・`src/window.cpp`

関数の名前と役割は [HLD 3.4.3](30_HLD.md#343-関数) の表の「窓と省略」の群で、処理の正本は [HLD 4.4.2](30_HLD.md#442-処理の流れ) の 4「対象メッシュごとに、昇順に次を行う」の 2・3（通常モード）と、[4.14.2](30_HLD.md#4142-処理の流れ) の 4「対象メッシュごとに、昇順に次を行う」の 1 と 2 の 2〜4（広域モード）、`.meshset` の形式は [4.4.2](30_HLD.md#442-処理の流れ) の「`.meshset` の形式」、止まる場面とメッセージに含める内容は [4.4.3](30_HLD.md#443-異常系)・[4.14.3](30_HLD.md#4143-異常系) である。メッシュ 1 つのタイルの範囲は [2.4](#24-言語ごとに別に実装する式のテストベクトル) の「メッシュの取得範囲の決まり」、タイルの置き場は [2.3](#23-ファイルの名前と書き方) の「標高タイルのキャッシュ」で決まっている。5 つの関数を呼ぶ順と、日本全土1次メッシュコードリストと北方領土除外メッシュリストから作る集合の受け渡しは 6.11 の `run_normal_mode`・`run_wide_mode`（[HLD 3.4.3](30_HLD.md#343-関数) の呼ぶ順）で、6.3 は渡された集合とパスを受け取る。この節は、それを C++ で書くための細部を足す。1.2 の C++ の規約に従う。

#### 6.3.1 ファイル割付

- 公開の宣言は `src/window.hpp`、定義と内部の関数は `src/window.cpp` に置く。どちらも先頭のコメントに `// trace: LLD-analyze_terrain_window` を書き、ヘッダーは次の行を `#pragma once` にする。
- `src/window.hpp` は `<set>`・`<string>` を読む。`src/window.cpp` は `"window.hpp"`・`"common.hpp"`・`"convert.hpp"`・`<algorithm>`・`<cerrno>`・`<cmath>`・`<cstdio>`・`<cstring>`・`<dirent.h>`・`<fcntl.h>`・`<stdexcept>`・`<string>`・`<sys/stat.h>`・`<unistd.h>`・`<vector>` を読む。OpenCV のヘッダーは読まない。
- UT のコードは `tests/src/test_window.cpp` に置き、`build/test_window` にビルドする（[2.5](#25-ビルドとテストの名前)。`src/` の `main` を持たない `.cpp` をすべてリンクするので、`common.cpp`・`convert.cpp` も入る）。各テストに `// trace: UT-analyze_terrain_window-NN`（確かめる UT 候補の ID）のコメントを付ける。2.4 の表の行を写したテストには、写した表の名前（`2.4 の表 4` など）もコメントに書く（[テスト方針書 3.3](02_test_policy.md#33-期待値の根拠)）。テストの枠組みは GoogleTest（[テスト方針書 3.4](02_test_policy.md#34-テストを先に書く進め方)）。

#### 6.3.2 型とデータ

`src/window.hpp` の公開の宣言は次のとおり（名前空間に入れない。1.2 の C++ の規約）。

```cpp
#pragma once
#include <set>
#include <string>

struct PatternCover {
    bool covered = false;        // 真なら、解析対象メッシュの集合を含む .meshset があった
    std::string meshset_path;    // 含んでいた .meshset のパス（covered が偽なら空）
};

std::set<std::string> normal_window(const std::string& center,
                                    const std::set<std::string>& meshes);
std::set<std::string> pattern_window(const std::string& target, int n,
                                     const std::string& corner,
                                     const std::set<std::string>& existing);
std::set<std::string> read_meshset(const std::string& path, int n);
PatternCover is_pattern_covered(const std::string& csv_dir, const std::string& target,
                                const std::set<std::string>& window, int n);
void check_mesh_tiles(const std::set<std::string>& meshes, const std::string& tiles_dir,
                      bool check_dem10b);
```

- 引数の並びは [HLD 3.4.3](30_HLD.md#343-関数) の表の受け取るものの順で、`read_meshset` と `is_pattern_covered` の `n`（`--n` の値）は最後に置く。`csv_dir` は `data_dir` の下の `results/csv`、`tiles_dir` は `data_dir` の下の `tiles` の絶対パスで、どちらも末尾に `/` を付けない（6.11 が組み立てて渡す）。`corner` は `NW`・`NE`・`SW`・`SE` のどれか（解析識別子に書く字のまま）。`window` は解析対象メッシュの集合。
- メッシュの集合は 6.2 と同じ `std::set<std::string>`（4 バイトの ASCII の数字。昇順はコードの数の昇順）。返す窓も集合で、並びは集合の順。
- `PatternCover` は 6.2 の構造体と同じく名前で読める形にし、値の有無を持つ型（`std::optional`）を使わない（1.2）。パスを返すのは、省略したことのログ（[6.3.4](#634-メッセージ文面) の WN1）を 6.11 が出すため（[HLD 3.4.3](30_HLD.md#343-関数) の「含んでいた `.meshset` のパス（ログに出すため）」）。
- 内部（`src/window.cpp` の無名の名前空間）は、`struct TileRange { int x_min, x_max, y_min, y_max; }`（両端を含む）と `TileRange _mesh_tile_range(const std::string& mesh, int z)`（`check_mesh_tiles` の 1）、`_read_file`（[6.2.3](#623-関数の細部) の `_read_file` と同じ形）、サービス名とズームの定数（DEM5a `dem5a_png`・DEM5b `dem5b_png`・DEM5c `dem5c_png` はズーム 15、DEM10b `dem_png` はズーム 14。[2.3](#23-ファイルの名前と書き方) の「標高タイルのキャッシュ」）。
- メッシュ 1 つの範囲を求める内部の関数を 6.3 が持つのは、[HLD 3.4.3](30_HLD.md#343-関数) の呼ぶ関係で `tile_range`（解析対象メッシュの bounding box の範囲を求める。[6.4](#64-analyze_terrain_grid)）を呼ぶのが `build_grid_z15`・`build_grid_z14` だけで、`check_mesh_tiles` はメッシュ 1 つずつの範囲を要るため。2.4 の決まりの C++ の写しが `tile_range` とこの関数の 2 か所になり、同じ範囲になることは表 4 の行を写した UT で確かめる（UT 18・19）。

#### 6.3.3 関数の細部

処理の正本は上の前置きのとおりで、この節は C++ で書くための細部を足す。どの関数も `check_signal` を呼ばない（[HLD 3.4.3](30_HLD.md#343-関数) の `check_signal` を呼ぶ群に「窓と省略」は入っていない。窓の計算とファイルの有無を見るだけで、時間がかからない）。止まるときは、メッセージを `log_error` で出してから `throw ExitRequest(EXIT_ERROR)` する（1.2 の C++ の規約）。呼ぶ側の誤りは `std::invalid_argument` を投げる（6.2・6.10・6.12 と同じ。`main` は捕まえないので、6.12 の `_on_terminate` が G7 で止める）。通常のログと警告は出さない（WN1 は 6.11 が出す）。

呼ぶ側の誤りのメッセージは次の形にする。メッシュのコードの検査（4 バイトで、どのバイトも ASCII の `0`〜`9`）は 6.10 の `mesh_to_latlon` と同じ判定で、`<関数名>: <引数名> が 4 桁の数字でない: <値>`。ほかは `<関数名>: n が 4・5・6 でない: <10 進の n>`、`pattern_window: corner が NW・NE・SW・SE でない: <値>`、`is_pattern_covered: window が空`、`<関数名>: <引数名> が空か / で終わる: <値>`（`csv_dir`・`tiles_dir`）。UT はメッセージの文を比べず、例外の型だけを確かめる。

関数ごとに `#####` の見出しを立てる。

##### normal_window

`std::set<std::string> normal_window(const std::string& center, const std::set<std::string>& meshes)`

1. `center` がメッシュのコードでなければ `std::invalid_argument`。
2. `p` を `center` の上 2 桁、`u` を下 2 桁の数にする（`std::stoi` を使わず、2 バイトの数字から `10 × 上 + 下` で求める）。`dp`・`du` をそれぞれ −1・0・1 にした 9 通りのうち、`p + dp` と `u + du` がどちらも 0 以上 99 以下のものについて、2 桁ずつ（1 桁なら前に `0`）つないだコードを作り、`meshes` にあれば返す集合に入れる。範囲の外は作らない（コードを 1 つの 4 桁の数として ±1・±100 すると、`0099` の東が `0100` になり、隣でないコードができるため）。
3. `center` が `meshes` に無くても誤りにしない（返す集合に入らないだけ。通常モードの対象メッシュと広域モードの対象メッシュは、呼ぶ前に集合にある）。

##### pattern_window

`std::set<std::string> pattern_window(const std::string& target, int n, const std::string& corner, const std::set<std::string>& existing)`

1. `target` がメッシュのコードでなければ、`n` が 4・5・6 のどれでもなければ、`corner` が `NW`・`NE`・`SW`・`SE` のどれでもなければ（大文字だけ。バイト列で比べる）、`std::invalid_argument`（この順に検査する）。
2. `p`・`u` は `normal_window` と同じ。緯度の番号の範囲は、NW・NE が `p − (n − 1)`〜`p`、SW・SE が `p`〜`p + (n − 1)`。経度の番号の範囲は、NW・SW が `u`〜`u + (n − 1)`、NE・SE が `u − (n − 1)`〜`u`（[HLD 4.14.2](30_HLD.md#4142-処理の流れ) の 4「対象メッシュごとに、昇順に次を行う」の 2 の 2）。どちらも両端を含む。
3. 範囲のうち、緯度の番号と経度の番号がどちらも 0 以上 99 以下の組だけコードを作り、`existing` にあれば返す集合に入れる。

##### read_meshset

`std::set<std::string> read_meshset(const std::string& path, int n)`（`n` は `--n` の値）

1. `n` が 4・5・6 のどれでもなければ `std::invalid_argument`。
2. `_read_file(path, data, err)` で全部を読む。失敗したら MS1（`{reason}` は `std::strerror(err)`。無いファイルは `No such file or directory`、ディレクトリは `Is a directory`）を出して止まる。
3. `data` が空なら MS2（`{detail}` は `行が無い`）。最後のバイトが `\n` でなければ MS2（`{detail}` は `{line_no} 行目（最後の行）が改行（LF）で終わっていない: {line}`。`{line_no}` は最後の `\n` の後の行の番号、`{line}` はその行のバイト列のまま）。
4. 最後の `\n` までを `\n` で行に分け、1 から番号を振る（最後の `\n` の後の空の文字列は行に数えない）。各行を順に見て、最初の誤りの 1 つだけで MS2 を出して止まる。
   - 行の最後のバイトが `\r` なら `{line_no} 行目の行末に CR がある: {line}`（この `{line}` は最後の `\r` を除いたバイト列）。
   - そうでなく、行が 4 バイトの ASCII の数字でなければ（空の行、BOM、空白を含む）`{line_no} 行目が 4 桁のメッシュコードでない: {line}`。
   - そうでなく、1 つ前の行のコード以下（バイト列の比較で `<=`）なら `{line_no} 行目のコードが前の行より大きくない（昇順でないか、重なっている）: {line}`。
5. 誤りが無ければ、行のコードの集合を返す。日本全土1次メッシュコードリストにあるかは見ない（形だけを確かめる）。

- `{path}` は受け取った `path` のまま（6.11 が絶対パスで組み立てる）。`{line}` は行のバイト列のまま、`{line_no}` は 10 進（先頭の `0` なし）。
- 厳しく読むのは、書き手が `write_meshset` だけで（[HLD 4.4.2](30_HLD.md#442-処理の流れ) の「`.meshset` の形式」: 4 桁のコードを 1 行 1 件、昇順、各行を LF で終え、見出しや注釈の行を持たない）、形が崩れたものは壊れたか手で書き換えたものだから。省略の判定に使うので、崩れたものを読み流すと、解析していない範囲を解析済みとみなして省きうる。`read_mesh_list_file`（空白・空行・`#` の行を許す）の読み方にはしない。

##### is_pattern_covered

`PatternCover is_pattern_covered(const std::string& csv_dir, const std::string& target, const std::set<std::string>& window, int n)`（`n` は `--n` の値）

1. `csv_dir` が空か最後のバイトが `/` なら、`target` がメッシュのコードでなければ、`window` が空なら、`n` が 4・5・6 のどれでもなければ、`std::invalid_argument`（この順に検査する）。
2. `opendir(csv_dir)` と `readdir` で項目の名前を全部読み、`closedir` する。`opendir` が `ENOENT` で失敗したら項目が無いものとして扱う（4 へ進み、偽を返す）。ほかの失敗（`ENOTDIR`・`EACCES` など）と `readdir` の失敗（`errno` を 0 にしてから呼び、`nullptr` が返って `errno` が 0 でない）は MS3 を出して止まる（`{reason}` は `std::strerror(errno)`）。
3. 選ぶ名前（バイト列で完全に一致するものだけ）は、次の 2 つ。
   - `3-` と 4 桁の ASCII の数字と `.meshset`（通常解析のもの。どのメッシュのものでも選ぶ）。
   - `4`・`5`・`6` のどれか 1 字と `-` と `target` と `-` と `NW`・`NE`・`SW`・`SE` のどれかと `.meshset`（同じ対象メッシュの広域解析のもの。N とコーナーは問わない）。

   ほかの名前（`.` と `..`、`.meshset.tmp` で終わるもの、別の対象メッシュのもの、桁や字の違うもの）は読まない（[HLD 4.14.2](30_HLD.md#4142-処理の流れ) の 4「対象メッシュごとに、昇順に次を行う」の 2 の 3、ADR-SRS-063）。項目の種類（ファイルかディレクトリか）は見ない（ディレクトリなら 4 の `read_meshset` が MS1 で止まる）。
4. 選んだ名前をバイト列の昇順に並べ、その順にすべてを `read_meshset(csv_dir + "/" + 名前, n)` で読む（途中で含むものが見つかっても、残りも読む。読めないものか書式の違うものがあれば、そこで止まる）。
5. 全部を読んだ後、読んだ順で最初に `window` のすべてのコードを含む（`std::includes`）集合があれば `{true, そのパス}`、無ければ `{false, ""}` を返す。

- 全部を読んでから判定するのは、[HLD 4.14.2](30_HLD.md#4142-処理の流れ) が「選んで読む」「読んだ `.meshset` が読めないか、形式でない行があれば止まる」と書いていて、含むものが見つかった時点で読むのをやめると、壊れたファイルで止まるかどうかがファイルの並びで変わるため。並びをバイト列の昇順に決めるのは、同じ入力で同じログになるようにするため。
- 置き場が無いとき（`ENOENT`）に偽を返すのは、省略できるファイルが無いのと同じで、パターンを行っても結果を誤らないため。ほかの理由で読めないときは、[HLD 4.14.3](30_HLD.md#4143-異常系) の「判定に使う `.meshset` が読めない」と同じく止まる（読めないまま省略の判定をしない）。

##### check_mesh_tiles

`void check_mesh_tiles(const std::set<std::string>& meshes, const std::string& tiles_dir, bool check_dem10b)`

1. 範囲は内部の `_mesh_tile_range(mesh, z)` で求める。[2.4](#24-言語ごとに別に実装する式のテストベクトル) の「メッシュの取得範囲の決まり」の 1〜4 のとおりに、6.10 の `mesh_to_latlon`・`latlon_to_tile` と、3 の西の境目の経度の式（`((x_e / 2^z) × 360) − 180` を倍精度で、2.4 の字句の順に求める。`2^z` は 6.10.3 と同じく `std::ldexp(1.0, z)`）で `x_min`・`x_max`・`y_min`・`y_max` を求める。
2. 4 より前に引数を全部確かめる。`tiles_dir` が空か最後のバイトが `/` なら `std::invalid_argument`。`meshes` を昇順に見て、メッシュのコードでなければ前置きの文の `std::invalid_argument`、下 2 桁（経度の番号）が 79 以上なら `std::invalid_argument("check_mesh_tiles: mesh の東端が経度 180 以上: " + mesh)`（東端が `101 + 経度の番号` 度で、180 度以上になり、6.10.3 の `latlon_to_tile` の渡せる範囲〈経度 180 未満〉の外。日本全土1次メッシュコードリストは 6.12.3 で 4 桁の形しか確かめないので、手で書き換えたリストで起きうる）。
3. タイルのパスは `tiles_dir + "/" + サービス名 + "/" + z + "/" + x + "/" + y + ".png"`（z・x・y は 10 進）。「ある」は `stat` が成功したとき（種類を問わない。ディレクトリも「ある」）。`stat` が `ENOENT` か `ENOTDIR` で失敗したら「無い」。ほかの失敗（`EACCES` など）は「ある」として扱う（読めるかは、[6.4](#64-analyze_terrain_grid) の `read_tile` が見る。[HLD 4.4.2](30_HLD.md#442-処理の流れ) の 4「対象メッシュごとに、昇順に次を行う」の 3 の「ここではファイルがあるかだけを見て、読めるかは 4 で見る」）。
4. 1 枚も無い検査: `meshes` を昇順にすべて見て、ズーム 15 の範囲の位置の DEM5a・DEM5b・DEM5c のファイルと、ズーム 14 の範囲の DEM10b のファイルが、どれも無いメッシュを控える（1 枚見つかったら、そのメッシュの残りは見ない）。控えたものが 1 つ以上あれば TT1 を出して止まる。
5. 欠けの割合の検査（`check_dem10b` が真で、4 で止まらなかったときだけ）: `meshes` を昇順にすべて見て、メッシュごとに、ズーム 15 の範囲の位置 `(x, y)` を `y` の昇順、同じ `y` では `x` の昇順に見る。DEM5a・DEM5b・DEM5c のどれかのファイルがある位置の数を `p`、そのうち DEM10b の `(x / 2, y / 2)`（整数の割り算。位置は 0 以上）のファイルが無い位置の数を `m` とし、無かった DEM10b のタイル `(x / 2, y / 2)` を、重ねずに控えた順（位置を見る順に、初めて出たもの）に並べる。`p` が 0 でなく `m × 100 > p`（整数で比べる。ちょうど 1% は超えない）なら、そのメッシュを控える。控えたものが 1 つ以上あれば TT2 を出して止まる。
6. 止まらなければ戻る。

- 全部のメッシュを見てから挙げるのは、直すには CMP2 でタイルを取り直すことになり、1 件ずつ止めると取り直すたびに解析を起動し直すことになるため（HLD の DEC49「読めないタイルでは窓のタイルを読み終えてから挙げて止める」と同じ考え）。1 枚も無い検査を先にすべて終えてから割合を見るのは、[HLD 4.4.2](30_HLD.md#442-処理の流れ) の 4「対象メッシュごとに、昇順に次を行う」の 3 の順（1 枚も無いかを見て、続けて割合を見る）による。
- 「ある」を `stat` の成功にするのは、HLD がファイルがあるかだけを見て読めるかは後の段で見るとしているため。ディレクトリや権限で読めないものを「無い」にすると、後の段で NODATA として黙って続きうる。
- 欠けたタイルの座標を先頭の 5 件にするのは、[HLD 4.4.3](30_HLD.md#443-異常系) が「先頭のいくつか」とだけ書いているため。1% を超えるメッシュでは数千件になりうる（HLD の DEC64「DEM10b の欠けが 1% を超えるメッシュでは止める」の理由が挙げる 5539 の例）ので、UP3 のように全件は挙げない。
- 存在メッシュの中で、北方領土除外タイルと親の Z14 のタイルを共有する DEM5 の位置は、CMP2 が DEM10b を取らないので、`m` に数わる。止まる側にだけ振れ、北方領土の近くの数か所なので、`check_mesh_tiles` は北方領土除外タイルリストを受け取らない（[HLD 3.4.3](30_HLD.md#343-関数)）。

#### 6.3.4 メッセージ文面

書き方は [2.2](#22-ログとメッセージの文面)。`{path}`・`{line}`・`{line_no}`・`{reason}`・`{detail}` は 6.3.3 のとおり。`{n}` は `read_meshset` と `is_pattern_covered` の `n`、`{dir}` は `is_pattern_covered` の `csv_dir`。`{redo}`・`{refetch}`・`{meshes}`・`{entries}` は表の後に書く。

`ERROR:` のメッセージ（2 行目は `対処:` と空白 1 つの後）:

| 記号 | 場面 | 1 行目 | 2 行目 | 終了コード |
|---|---|---|---|---|
| MS1 | 省略の判定に使う `.meshset` を読めない | `省略の判定に使う .meshset を読めない: {path}: {reason}` | `{redo}` | 1 |
| MS2 | 省略の判定に使う `.meshset` の書式が違う | `省略の判定に使う .meshset の書式が違う: {path}: {detail}`（`{detail}` は 6.3.3 の `read_meshset` の 3・4 のとおり） | `{redo}` | 1 |
| MS3 | `.meshset` の置き場を読めない | `.meshset の置き場を読めない: {dir}: {reason}` | `{dir} の権限を確かめてから、scripts/run_pipeline.sh --phase 3 --n {n} を起動し直す（設定ファイルを指定して起動したときは、同じ --config を付ける）` | 1 |
| TT1 | タイルが 1 枚も無いメッシュがある | `4 つの DEM 種別のどのローカルキャッシュにもタイルが無いメッシュがある: {meshes}` | `{refetch}` | 1 |
| TT2 | DEM10b のタイルの欠けが 1% を超える解析対象メッシュがある | `DEM10b のタイルの欠けが 1% を超える解析対象メッシュがある: {entries}` | `{refetch}` | 1 |

- `{redo}`: `{path} を消してから、scripts/run_pipeline.sh --phase 3 --n {n} を起動し直す（.meshset は省略の判定にだけ使うので、消しても解析の結果は変わらない。設定ファイルを指定して起動したときは、同じ --config を付ける）`。[HLD 4.14.3](30_HLD.md#4143-異常系) の表の「そのファイルを消してから同じ段を起動し直す案内」である。
- `{meshes}`: 控えたメッシュのコードを昇順に `、` でつないだもの。TT1 の 1 行目に「解析対象メッシュ」と書かないのは、広域モードの 3×3 の検査（`check_dem10b` が偽）では存在メッシュも見るため（[HLD 4.14.2](30_HLD.md#4142-処理の流れ) の 4「対象メッシュごとに、昇順に次を行う」の 1）。
- `{entries}`: 控えたメッシュを昇順に、1 件を `{mesh}（DEM5 のタイルがある位置 {p}、うち DEM10b のタイルが無い位置 {m}、{ratio}%、DEM10b のタイルが無い先頭のタイル: {tiles}）` にして `、` でつないだもの。`{ratio}` は `100.0 × m / p` を倍精度で求め、`std::snprintf` の `%.3f` で書いたもの。`{tiles}` は控えた DEM10b のタイルの先頭の 5 件（5 件より少なければ全部）を `14/{x}/{y}` の形で空白 1 つでつないだもの。
- `{refetch}`: `メッシュごとに venv/bin/python3 scripts/fetch_tiles.py --mesh <コード> を起動してタイルを取り直してから、解析を起動し直す（設定ファイルを指定して起動したときは、どちらにも同じ --config を付ける）`。[HLD 4.4.3](30_HLD.md#443-異常系) の表の「CMP2 を起動し直す案内」である。`--mesh` は 1 つのコードかファイルしか受けないので（[HLD 2.4.3](30_HLD.md#243-メッシュ範囲)）、メッシュごとに起動する形にする。`<コード>` は文字どおりそのまま書く（控えたメッシュのコードに替えず、利用者が 1 行目に並べたコードに読み替える）。2 行目は 1 つの文で、メッシュの数によらず繰り返さない。
- `{redo}`・`{refetch}`・MS3 の 2 行目の括弧「設定ファイルを指定して起動したときは、同じ --config を付ける」は、関数が設定ファイルの指定の有無を知らないので、いつでもそのまま書く（6.2 の UP3 の対処の文と同じ）。

通常のログに出す行（`log_info` で標準出力とログファイルに出す）:

| 記号 | 行 | 文面 |
|---|---|---|
| WN1 | パターンを省略した | `パターンを省略した（解析対象メッシュが {meshset} に含まれる）: {analysis_id}`（`{meshset}` は `is_pattern_covered` が返した `meshset_path`、`{analysis_id}` は `<N>-<対象メッシュコード>-<コーナー>`。[HLD 4.14.2](30_HLD.md#4142-処理の流れ) の 4「対象メッシュごとに、昇順に次を行う」の 2 の 3 の「省略したことと、含んでいたファイルをログに出す」） |

出し方: 6.11 の `run_wide_mode` は、`is_pattern_covered` が `covered` の真を返したら WN1 を `log_info` で出して次のパターンへ進む。MS1〜MS3・TT1・TT2 は 6.3 の関数が出す。

#### 6.3.5 UT 候補

すべて自動。GoogleTest のケースごとに `// trace: UT-analyze_terrain_window-NN` を付ける。共通の準備は 6.2.5 の「同じプロセス」と同じ（`mkdtemp` で一時のディレクトリを作り、ファイルはその下にバイト列で書いて絶対パスを渡す。標準エラー出力は記述子 2 の付け替えで捕まえる。止まるケースは `ExitRequest` を捕まえて `code` を確かめ、メッセージの期待は標準エラー出力の 2 行の全文）。タイルのファイルは空のファイルでよい（あるかだけを見るため）。`csv_dir`・`tiles_dir` は一時のディレクトリの下に作った絶対パス。

| ID | 確かめること | 準備 | 入力 | 期待 |
|---|---|---|---|---|
| `UT-analyze_terrain_window-01` | 3×3 の窓 | 同じプロセス | `normal_window("5339", {5238, 5239, 5240, 5338, 5339, 5340, 5438, 5439, 5440, 5341})` | 9 件（`5341` を除く 9 つ） |
| `UT-analyze_terrain_window-02` | 集合にあるものだけ | 同じプロセス | `normal_window("5339", {5339, 5440, 6841})` | `{5339, 5440}` |
| `UT-analyze_terrain_window-03` | 番号の端 | 同じプロセス | (a) `normal_window("0099", {0098, 0099, 0198, 0199, 0100, 0000})`、(b) `normal_window("9900", {9899, 9900, 9800, 9801, 9901, 0000})` | (a) `{0098, 0099, 0198, 0199}`（`0100` と `0000` は隣でない）、(b) `{9800, 9801, 9900, 9901}`（`9899` は隣でない） |
| `UT-analyze_terrain_window-04` | パターンの窓（ADR-SRS-004 の例） | 同じプロセス。`existing` は緯度の番号 46〜56・経度の番号 30〜40 のすべてのコード（121 件） | `pattern_window("5135", 4, c, existing)` を `c` を `NW`・`NE`・`SW`・`SE` にして | NW は緯度の番号 48〜51・経度の番号 35〜38 の 16 件（`4835`〜`5138`）、NE は 48〜51・32〜35（`4832`〜`5135`）、SW は 51〜54・35〜38（`5135`〜`5438`）、SE は 51〜54・32〜35（`5132`〜`5435`） |
| `UT-analyze_terrain_window-05` | N の大きさ | 同じプロセス。04 と同じ `existing` | `pattern_window("5135", n, "NW", existing)` を `n` を 5・6 にして | 5 は緯度の番号 47〜51・経度の番号 35〜39 の 25 件（`4735`〜`5139`）、6 は 46〜51・35〜40 の 36 件（`4635`〜`5140`） |
| `UT-analyze_terrain_window-06` | パターンの番号の端 | 同じプロセス | `pattern_window("0099", 4, "NE", {0096, 0097, 0098, 0099, 0100, 9999})` | `{0096, 0097, 0098, 0099}` |
| `UT-analyze_terrain_window-07` | 窓の呼ぶ側の誤り | 同じプロセス | (a) `normal_window("533", …)`、(b) `normal_window("53a9", …)`、(c) `pattern_window("5135", 3, "NW", …)`、(d) `n` が 7、(e) `corner` が `nw`、(f) `corner` が `N`、(g) `target` が `51a5` | どれも `std::invalid_argument`。標準エラー出力に何も出ない |
| `UT-analyze_terrain_window-08` | `.meshset` を読む | 同じプロセス | 中身が (a) `5238\n5239\n5339\n`、(b) `5339\n` のファイルを `n` 4 で `read_meshset` | (a) `{5238, 5239, 5339}`、(b) `{5339}`。標準エラー出力に何も出ない |
| `UT-analyze_terrain_window-09` | `.meshset` の書式の誤り | 同じプロセス。中身ごとに別のファイル、`n` は 4 | (a) 0 バイト、(b) `5339`（LF 無し）、(c) `5339\r\n`、(d) BOM（`EF BB BF`）の後に `5339\n`、(e) `5339\n\n5340\n`、(f) `5339\n5339\n`、(g) `5340\n5339\n`、(h) `5339 \n`、(i) `53390\n` | どれも `code` が 1 の MS2。`{detail}` は (a) `行が無い`、(b) `1 行目（最後の行）が改行（LF）で終わっていない: 5339`、(c) `1 行目の行末に CR がある: 5339`、(d)(h)(i) `1 行目が 4 桁のメッシュコードでない:` と空白 1 つの後に行のまま、(e) `2 行目が 4 桁のメッシュコードでない:` と空白 1 つ（その後が空）、(f)(g) `2 行目のコードが前の行より大きくない（昇順でないか、重なっている）: 5339` |
| `UT-analyze_terrain_window-10` | `.meshset` を読めない、やり直しの案内と N | 同じプロセス | (a) 存在しないパス、(b) 一時のディレクトリそのもの。どちらも `n` を 4・5・6 にしてそれぞれ | `code` が 1 の MS1（(a) `No such file or directory`、(b) `Is a directory`）。2 行目は `{redo}` で、`--n` の後が渡した `n` |
| `UT-analyze_terrain_window-11` | 省略できる | 同じプロセス。`csv_dir` に `3-5135.meshset`（`5134\n5135\n`）、`3-5236.meshset`（`5135\n5136\n5236\n`）、`4-5135-NW.meshset`（`5135\n5136\n`） | `is_pattern_covered(csv_dir, "5135", {5135, 5136}, 4)` | `{true, <csv_dir>/3-5236.meshset}`（バイト列の昇順で `3-5236` が `4-5135-NW` より先） |
| `UT-analyze_terrain_window-12` | 選ばない名前は読まない | 同じプロセス。11 の 3 つのほかに、中身が `x\n` のファイル `4-5136-NW.meshset`・`3-5135.meshset.tmp`・`7-5135-NW.meshset`・`4-5135-N.meshset`・`3-513.meshset`・`5135.meshset`・`4-5135-nw.meshset` と、ディレクトリ `sub` | 11 と同じ | 11 と同じ結果。標準エラー出力に何も出ない |
| `UT-analyze_terrain_window-13` | 省略できない | 同じプロセス | (a) 11 の `csv_dir` で `window` が `{5135, 5137}`、(b) `csv_dir` が存在しないパス | どちらも `{false, ""}`。標準エラー出力に何も出ない |
| `UT-analyze_terrain_window-14` | 含むものの後の壊れたファイルでも止まる | 同じプロセス。11 の 3 つのほかに `6-5135-SW.meshset`（`5135\n5134\n`） | 11 と同じ（`n` は 5） | `code` が 1 の MS2。`{path}` は `<csv_dir>/6-5135-SW.meshset`、`{detail}` は `2 行目のコードが前の行より大きくない（昇順でないか、重なっている）: 5134`、2 行目の `--n` の後は 5 |
| `UT-analyze_terrain_window-15` | 選んだ名前がディレクトリ | 同じプロセス。`csv_dir` にディレクトリ `3-5300.meshset` だけ | `is_pattern_covered(csv_dir, "5135", {5135}, 4)` | `code` が 1 の MS1（`Is a directory`） |
| `UT-analyze_terrain_window-16` | 置き場がディレクトリでない | 同じプロセス。`csv_dir` に普通のファイルのパスを渡す | `is_pattern_covered(csv_dir, "5135", {5135}, 4)` | `code` が 1 の MS3（`Not a directory`）。2 行目は 6.3.4 の MS3 の文で `--n 4` |
| `UT-analyze_terrain_window-17` | 省略の呼ぶ側の誤り | 同じプロセス | (a) `csv_dir` が空、(b) 末尾が `/`、(c) `target` が `51a5`、(d) `window` が空、(e) `n` が 3 | どれも `std::invalid_argument`。標準エラー出力に何も出ない |
| `UT-analyze_terrain_window-18` | 1 枚も無い（2.4 の表 4） | 同じプロセス。`tiles_dir` の下に、`dem5b_png/15/28672/12942.png`（`5235` の範囲の北西の隅）、`dem5a_png/15/28672/13162.png` と `dem_png/14/14336/6581.png`（どちらも `4934` の東端の外） | `check_mesh_tiles({4934, 5235}, tiles_dir, false)` | `code` が 1。1 行目は `ERROR: 4 つの DEM 種別のどのローカルキャッシュにもタイルが無いメッシュがある: 4934`、2 行目は 6.3.4 の `{refetch}` の文の全文（`<コード>` の字もそのまま） |
| `UT-analyze_terrain_window-19` | 範囲の端の内側（2.4 の表 4） | 同じプロセス。それぞれ別の `tiles_dir` | `4934` に、(a) `dem5c_png/15/28671/13235.png` だけを置いて `check_dem10b` が偽、(b) `dem_png/14/14335/6617.png` だけを置いて偽、(c) (b) と同じで `check_dem10b` が真、(d) `dem5a_png/15/28580/13162.png` という名前のディレクトリだけを作って偽 | どれも止まらない。標準エラー出力に何も出ない |
| `UT-analyze_terrain_window-20` | 欠けの割合 | 同じプロセス。`4934` に、DEM5a を 100 の位置（`y` が 13162 と 13164 の `x` が 28580〜28670 の偶数 46 か所ずつと、`y` が 13166 の `x` が 28580〜28594 の偶数 8 か所。親のタイルはすべて違う）に置き、それぞれの親 `(x / 2, y / 2)` の DEM10b を、`y`・`x` の昇順に見た先頭の `k` 枚（`14/14290/6581` から順）を除いて置く | `check_mesh_tiles({4934}, tiles_dir, check_dem10b)` を、(a) `k` が 1 で `check_dem10b` が真、(b) `k` が 2 で真、(c) `k` が 6 で真、(d) `k` が 2 で偽。ほかに (e) 別の `tiles_dir` で、DEM5a を `y` が 13162 と 13163 の `x` が 28580〜28629 の 100 の位置（親は `(14290, 6581)`〜`(14314, 6581)` の 25 枚で、1 枚に 4 つの位置）に置き、DEM10b を `(14290, 6581)` を除く 24 枚に置いて `check_dem10b` が真 | (a)(d) 止まらない。(b) `code` が 1 で、1 行目が `ERROR: DEM10b のタイルの欠けが 1% を超える解析対象メッシュがある: 4934（DEM5 のタイルがある位置 100、うち DEM10b のタイルが無い位置 2、2.000%、DEM10b のタイルが無い先頭のタイル: 14/14290/6581 14/14291/6581）`、2 行目が 6.3.4 の `{refetch}` の文の全文。(c) は位置 6、`6.000%`、先頭のタイルは `14/14290/6581` から `14/14294/6581` の 5 件。(e) は位置 4、`4.000%`、先頭のタイルは `14/14290/6581` の 1 件（`m` は位置の数で、親のタイルの数ではない） |
| `UT-analyze_terrain_window-21` | 1 枚も無い検査が先 | 同じプロセス。(a) の `tiles_dir`: `5235` に DEM5a を 100 の位置（`y` が 12942 と 12944 の `x` が 28672〜28762 の偶数 46 か所ずつと、`y` が 12946 の `x` が 28672〜28686 の偶数 8 か所）に置き、それぞれの親の DEM10b を、先頭の 2 枚（`14/14336/6471`・`14/14337/6471`）を除いて置く（20 の (b) と同じ欠け方で、`check_dem10b` が真なら `5235` だけで TT2 に当たる置き方）。`4934` には何も置かない。(b) の別の `tiles_dir`: `4934` に 20 の (b) の置き方、`5235` には何も置かない | それぞれの `tiles_dir` で `check_mesh_tiles({4934, 5235}, tiles_dir, true)` | どちらも `code` が 1 の TT1 で、(a) は `4934` だけ、(b) は `5235` だけを挙げる（TT2 は出ない。先に見たメッシュが TT2 に当たる (b) でも、1 枚も無い検査をすべてのメッシュで終えてから割合を見る）。1 行目は `ERROR: 4 つの DEM 種別のどのローカルキャッシュにもタイルが無いメッシュがある:` と空白 1 つの後にそのコード、2 行目は 6.3.4 の `{refetch}` の文の全文 |
| `UT-analyze_terrain_window-22` | 複数のメッシュ | 同じプロセス。`4934` に 20 の (b) の置き方、`5235` に 21 の (a) の置き方 | 21 と同じ | `code` が 1 の TT2。1 行目が `ERROR: DEM10b のタイルの欠けが 1% を超える解析対象メッシュがある: 4934（DEM5 のタイルがある位置 100、うち DEM10b のタイルが無い位置 2、2.000%、DEM10b のタイルが無い先頭のタイル: 14/14290/6581 14/14291/6581）、5235（DEM5 のタイルがある位置 100、うち DEM10b のタイルが無い位置 2、2.000%、DEM10b のタイルが無い先頭のタイル: 14/14336/6471 14/14337/6471）` |
| `UT-analyze_terrain_window-23` | 検査の呼ぶ側の誤り | 同じプロセス | (a) `meshes` に `53a9`、(b) `tiles_dir` が空、(c) 末尾が `/`、(d) `meshes` に `5380`、(e) `meshes` に `5379`（東端がちょうど 180 度） | どれも `std::invalid_argument`。標準エラー出力に何も出ない |
| `UT-analyze_terrain_window-24` | 経度の端の内側 | 同じプロセス。`tiles_dir` の下に `dem5a_png/15/32585/12867.png`（`5378` の範囲の北西の隅）だけ | `check_mesh_tiles({5378}, tiles_dir, false)`（`5378` の東端は 179 度で渡せる範囲の内側） | 止まらない。標準エラー出力に何も出ない |

### 6.4 `analyze_terrain_grid`

- **ID**: LLD-analyze_terrain_grid
- **対応 HLD**: [3.4](30_HLD.md#34-cmp4-地形解析エンジン)・[4.2](30_HLD.md#42-fr-002-dem-階層フォールバック)・[4.3](30_HLD.md#43-fr-003-標高デコードnodata-処理)・[4.4](30_HLD.md#44-fr-004-33メッシュ結合解析オーケストレーション)・[4.14](30_HLD.md#414-fr-014-広域結合解析オーケストレーション)・[4.16](30_HLD.md#416-fr-016-ピーク域ポリゴン生成)・[5.1](30_HLD.md#51-nfr-001-精度検出網羅性)・[5.2](30_HLD.md#52-nfr-002-メモリ使用量)
- **ファイル**: `src/grid.hpp`・`src/grid.cpp`

関数の名前と役割は [HLD 3.4.3](30_HLD.md#343-関数) の表の「タイルとグリッド」の群で、処理の正本は [HLD 4.4.2](30_HLD.md#442-処理の流れ) の「解析範囲標高グリッドの生成」の 1〜5 と「解析対象メッシュ範囲情報」（通常モード）、[4.14.2](30_HLD.md#4142-処理の流れ) の「Z14 のグリッドの生成」の 1〜4（広域モード）、DEM の選び方は [4.2.2](30_HLD.md#422-処理の流れ)、デコードは [4.3.2](30_HLD.md#432-処理の流れ)、止まる場面とメッセージに含める内容は [4.4.3](30_HLD.md#443-異常系)・[4.14.3](30_HLD.md#4143-異常系) である。メッシュの集合のタイルの範囲は [2.4](#24-言語ごとに別に実装する式のテストベクトル) の「メッシュの取得範囲の決まり」、タイルの置き場は [2.3](#23-ファイルの名前と書き方) の「標高タイルのキャッシュ」で決まっている。`pixel_center_mesh` は 6.8 の `fill_zone`・`judge_area_complete` も呼ぶ（[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の 2「塗る」・3「`area_complete` を決める」）。関数を呼ぶ順は 6.11 の `run_normal_mode`・`run_wide_mode`（[HLD 3.4.3](30_HLD.md#343-関数) の呼ぶ順）で決まっている。非機能要件は 2 つで、[5.1](30_HLD.md#51-nfr-001-精度検出網羅性)（精度・検出網羅性）の DEM の項目（DEM5 を優先し DEM10b で補う）は `select_dem_rgb` で受け、[5.2](30_HLD.md#52-nfr-002-メモリ使用量)（メモリ使用量）は、グリッドを `float` の 1 本の配列で持ち、タイルを位置ごとに読んで捨てる（メモリに持つのはグリッドと、読んでいるタイル 4 枚と、256×256 の標高 1 つ）ことで受ける（実測は [HLD 5.2.2](30_HLD.md#522-処理の流れ) の実測の計画の 1・2）。この節は、それを C++ で書くための細部を足す。1.2 の C++ の規約に従う。

#### 6.4.1 ファイル割付

- 公開の宣言は `src/grid.hpp`、定義と内部の関数は `src/grid.cpp` に置く。どちらも先頭のコメントに `// trace: LLD-analyze_terrain_grid` を書き、ヘッダーは次の行を `#pragma once` にする。
- `src/grid.hpp` は `<opencv2/core.hpp>`（`cv::Mat`・`cv::Vec3b`）・`"convert.hpp"`（`MeshBounds`・`TileXY`・`Z15Pixel`）・`"target.hpp"`（`TargetPeak`）・`<compare>`・`<cstdint>`・`<map>`・`<set>`・`<string>`・`<vector>` を読む。`src/grid.cpp` は `"grid.hpp"`・`"common.hpp"`・`"convert.hpp"`・`<opencv2/imgcodecs.hpp>`・`<algorithm>`・`<cerrno>`・`<cmath>`・`<cstring>`・`<fcntl.h>`・`<stdexcept>`・`<string>`・`<unistd.h>`・`<utility>`・`<vector>` を読む。OpenCV のヘッダーは core と imgcodecs のものだけを読む（[HLD 2.6.5](30_HLD.md#265-ビルド構成) のモジュールごとのヘッダー。imgproc は使わない）。
- UT のコードは `tests/src/test_grid.cpp` に置き、`build/test_grid` にビルドする（[2.5](#25-ビルドとテストの名前)）。各テストに `// trace: UT-analyze_terrain_grid-NN`（確かめる UT 候補の ID）のコメントを付ける。2.4 の表の行を写したテストには、写した表の名前（`2.4 の表 4`・`2.4 の表 7` など）もコメントに書く（[テスト方針書 3.3](02_test_policy.md#33-期待値の根拠)）。テストの枠組みは GoogleTest（[テスト方針書 3.4](02_test_policy.md#34-テストを先に書く進め方)）。テストは PNG のファイルを `cv::imwrite` で一時のディレクトリに作り、リポジトリに画像を置かない。

#### 6.4.2 型とデータ

`src/grid.hpp` の公開の宣言は次のとおり（名前空間に入れない。1.2 の C++ の規約）。

```cpp
#pragma once
#include <compare>
#include <cstdint>
#include <map>
#include <set>
#include <string>
#include <vector>
#include <opencv2/core.hpp>
#include "convert.hpp"
#include "target.hpp"

constexpr float NODATA_ELEVATION = -9999.0f;

struct AnalysisBox {
    MeshBounds bbox;     // 解析対象メッシュを囲む最小の矩形の四隅
    int x_min = 0;       // Z15 のタイル番号の範囲（両端を含む）
    int x_max = 0;
    int y_min = 0;
    int y_max = 0;
};

struct TileImage {
    cv::Mat bgr;              // CV_8UC3・256×256。無い・読めないときは全画素が cv::Vec3b(0, 0, 128)
    bool unreadable = false;  // 真なら読めないタイル（無いタイルは偽）
    std::string reason;       // 読めないときの理由（それ以外は空）
};

struct DecodedElevation {
    std::int32_t x = 0;       // R×65536 + G×256 + B（0〜0xFFFFFF）
    float elevation = 0.0f;   // 符号付きの標高（NODATA は NODATA_ELEVATION）
};

struct UnreadableTile {
    std::string path;
    std::string reason;
};

struct TileElevation {
    std::vector<float> values;                // 65,536 個。タイル内の画素 (i, j) は values[j * 256 + i]
    std::vector<UnreadableTile> unreadable;   // 読めなかったタイル（読んだ順）
};

struct GridXY {
    int px = 0;
    int py = 0;
    auto operator<=>(const GridXY&) const = default;
};

struct ElevationGrid {
    int width = 0;
    int height = 0;
    std::vector<float> values;   // 画素 (px, py) は values[static_cast<std::int64_t>(py) * width + px]
};

struct GridRange {
    std::set<std::string> meshes;       // 解析対象メッシュ
    bool z14 = false;                   // 偽なら Z15 のグリッド（タイル 1 枚が 256 画素）、真なら Z14（128 画素）
    AnalysisBox box;                    // tile_range の結果（Z14 のグリッドも Z15 のタイル番号の範囲）
    std::map<GridXY, Z15Pixel> picks;   // Z14 だけ。縮約で採った画素の Z15 の座標の控え（Z15 は空）
};

struct GridResult {
    ElevationGrid grid;
    GridRange range;
};

AnalysisBox tile_range(const std::set<std::string>& meshes);
TileImage read_tile(const std::string& path);
cv::Vec3b select_dem_rgb(const cv::Vec3b& dem5a, const cv::Vec3b& dem5b,
                         const cv::Vec3b& dem5c, const cv::Vec3b& dem10b);
DecodedElevation decode_signed_elevation(const cv::Vec3b& bgr);
float clamp_to_sea_level(std::int32_t x, float elevation);
std::string pixel_center_mesh(const Z15Pixel& pixel);
TileElevation build_tile_elevation(const TileXY& tile, const std::set<std::string>& meshes,
                                   const MeshBounds& bbox, const std::string& tiles_dir);
GridResult build_grid_z15(const std::set<std::string>& meshes, const std::string& tiles_dir);
GridResult build_grid_z14(const std::set<std::string>& meshes,
                          const std::vector<TargetPeak>& peaks, const std::string& tiles_dir);
```

- 引数の並びは [HLD 3.4.3](30_HLD.md#343-関数) の表の受け取るものの順。`tiles_dir` は `data_dir` の下の `tiles` の絶対パスで、末尾に `/` を付けない（6.3 と同じ。6.11 が組み立てて渡す）。`peaks` は 6.2 の `PeakGroups` のその対象メッシュの組。
- 画素の色: `cv::Vec3b` は OpenCV の並び（`[0]` が B、`[1]` が G、`[2]` が R。[HLD 4.3.2](30_HLD.md#432-処理の流れ) の「画素の表現」）。HLD の RGB (128, 0, 0) は `cv::Vec3b(0, 0, 128)`。UT の色も、RGB で書いた値を `cv::Vec3b(b, g, r)` にして書く。
- グリッドを `std::vector<float>` で持つのは、後の群（[6.6](#66-analyze_terrain_scan) の走査）が画素の番号 `py × W + px`（64 ビット。[HLD 4.5.2](30_HLD.md#452-処理の流れ) の前置き）で読み書きし、OpenCV の型に頼らずに済むため。`width`・`height` は `int`（最大の窓でも 2³¹ に届かない）、番号の計算は `std::int64_t` で行う。
- `GridRange` が HLD の「解析対象メッシュ範囲情報」。グリッドの画素と全球の画素の対応は、Z15 では (256 × `x_min` + px − 1, 256 × `y_min` + py − 1)、Z14 では全球の Z14 の画素 (128 × `x_min` + px − 1, 128 × `y_min` + py − 1)（[HLD 4.4.2](30_HLD.md#442-処理の流れ) の「解析対象メッシュ範囲情報」、[4.14.2](30_HLD.md#4142-処理の流れ) の「Z14 のグリッドの生成」の 4「解析対象メッシュ範囲情報」）。対応を計算する関数は足さず（1.2 の「LLD が足してよい名前」。ほかのモジュールから呼ぶ関数は HLD 3.4.3 の名前だけ）、後の群がこの式で求める。地理的範囲フィルタと `area_complete` の「範囲」は bounding box でなく `meshes`（解析対象メッシュの矩形を合わせたもの。[HLD 4.7.2](30_HLD.md#472-処理の流れ) の 4「地理的範囲フィルタ」、[4.16.2](30_HLD.md#4162-処理の流れ) の 3「`area_complete` を決める」）。`box.bbox` は、NODATA で埋める範囲（6.4 の `build_tile_elevation`）と、`area_complete` の外の隣が bounding box の中か外か（NODATA で埋めた範囲か、はみ出しか。HLD 4.16.2 の 3 の 2 つ目と 3 つ目の箇条）の区別に使う。
- `picks` の鍵はグリッドの画素、値は採った画素の全球の Z15 の座標（HLD の「タイル座標とタイル内の画素位置の組」と同じ値で、(256 × tx + i, 256 × ty + j)。[HLD 4.7.2](30_HLD.md#472-処理の流れ) の 2「ピークの Z15 の画素を求める」がこの形で使う）。
- 構造体は 6.2・6.10 と同じく名前で読める形にし、値の有無を持つ型（`std::optional`）を使わない（1.2）。`AnalysisBox` を 6.3 の内部の `TileRange` と別の名前にするのは、bounding box の四隅も持つことと、読み違えないため。
- 内部（`src/grid.cpp` の無名の名前空間）は、サービス名とズームの定数（6.3 と同じ。[2.3](#23-ファイルの名前と書き方) の「標高タイルのキャッシュ」）、PNG の署名の 8 バイト `89 50 4E 47 0D 0A 1A 0A`、`_tile_path(tiles_dir, service, z, x, y)`、`_check_tiles_dir(関数名, tiles_dir)`、`_fill_grid(...)`（Z15 と Z14 の共通の走り方）。

#### 6.4.3 関数の細部

処理の正本は上の前置きのとおりで、この節は C++ で書くための細部を足す。`check_signal` を呼ぶのは `build_grid_z15`・`build_grid_z14` の、タイルの位置ごとの処理の前と、全部の位置を終えた後（読めないタイルを挙げる前）だけ（[HLD 3.4.3](30_HLD.md#343-関数) の `check_signal` を呼ぶ群に「タイルとグリッド」が入っている）。受けてから止まるまでの遅れは、タイルの位置 1 つの処理（タイル 4 枚の読み込みと 65,536 画素）の分までで、グリッドの確保と 0 の書き込みの間（最大の窓で約 18GB。数秒から数十秒）だけは、その後の最初の位置の前まで延びる（確保は 1 回の呼び出しで、途中に区切りを置けない）。ほかの 7 関数は呼ばない（1 回で終わる計算か、タイル 1 枚の処理）。止まるときは、メッセージを `log_error` で出してから `throw ExitRequest(EXIT_ERROR)` する（1.2 の C++ の規約）。呼ぶ側の誤りは `std::invalid_argument` を投げる（6.2・6.3・6.10・6.12 と同じ。メッセージの形は `<関数名>: <引数名> が空か / で終わる: <値>`、`<関数名>: meshes が空`、そのほかは各関数の見出しの下。`<関数名>` は、呼ばれて投げる関数の名前で、`build_grid_z15`・`build_grid_z14` が `tiles_dir` を確かめて投げるときは、その関数自身の名前を書く。UT は例外の型だけを確かめる）。通常のログと警告は出さない。グリッドを確保できないときの `std::bad_alloc` は捕まえない（6.12 の `_on_terminate` が G7 で止める。終了コード 1。[HLD 4.5.3](30_HLD.md#453-異常系) の走査のメモリと同じ扱い）。

関数ごとに `#####` の見出しを立てる。

##### tile_range

`AnalysisBox tile_range(const std::set<std::string>& meshes)`

1. `meshes` が空なら `std::invalid_argument`。各コードを昇順に見て、6.10 の `mesh_to_latlon` と同じ形の判定（4 バイトで、どのバイトも ASCII の `0`〜`9`）に当たらなければ `std::invalid_argument("tile_range: mesh が 4 桁の数字でない: " + mesh)`。上 2 桁が 01〜98 でないか、下 2 桁が 01〜78 でなければ `std::invalid_argument("tile_range: mesh の上 2 桁が 01〜98 でないか、下 2 桁が 01〜78 でない: " + mesh)`。
2. `bbox` は、各メッシュの `mesh_to_latlon` の `south` の最小、`west` の最小、`north` の最大、`east` の最大。
3. 範囲は [2.4](#24-言語ごとに別に実装する式のテストベクトル) の「メッシュの取得範囲の決まり」の 1〜4 を、`bbox` の四隅とズーム 15 で当てる（東端の補正は 6.3 の `_mesh_tile_range` と同じ式・同じ順。`2^z` は `std::ldexp(1.0, 15)`）。

- 1 の上 2 桁・下 2 桁の範囲は、範囲のタイルのどの画素の中心でも `pixel_center_mesh` が空でないコードを返す（はみ出しは 1 タイル〈約 0.011 度〉で、メッシュの 1 行・1 列より小さい）ことと、6.10.3 の `latlon_to_tile` の渡せる範囲（経度 180 未満）を守るため。下 2 桁が 79 以上を止めるのは 6.3 の `check_mesh_tiles` と同じ理由。日本全土1次メッシュコードリスト（上 2 桁 30〜68、下 2 桁 22〜48）はどれも入る。
- 南端の補正をしない（2.4 の 4）理由は bounding box でも同じ: `bbox.south` はどれかのメッシュの南端で、2.4 の 4 が調べた 175 メッシュの南端のどれか。

##### read_tile

`TileImage read_tile(const std::string& path)`

1. `open(path, O_RDONLY | O_CLOEXEC | O_NONBLOCK)`（`O_NONBLOCK` は、キャッシュに名前付きパイプが置かれていても書き手を待って止まらないため。普通のファイルの読み方は変わらない）。`ENOENT` か `ENOTDIR` で失敗したら、無いタイル: 全画素が `cv::Vec3b(0, 0, 128)` の 256×256 の `CV_8UC3`、`unreadable` は偽、`reason` は空を返す（6.3 の `check_mesh_tiles` の「無い」と同じ判定）。ほかの理由で失敗したら、読めないタイル（`reason` は `PNG として読めない（{reason}）`。`{reason}` は `errno` の文。1.2）。
2. 先頭の 8 バイトを `read` で読む（`EINTR` は繰り返す。8 バイトに満たずに終わりが来たら、そこまで）。`read` が失敗したら（ディレクトリは `EISDIR`）`close` して、読めないタイル（`PNG として読めない（{reason}）`）。読めたら `close`（結果は見ない）。
3. 8 バイトに満たないか、署名と違えば、読めないタイル（`PNG の署名でない`）。
4. `cv::imread(path, cv::IMREAD_UNCHANGED)` を `try` で囲んで呼ぶ。`cv::Exception` が上がったか、空の画像なら読めないタイル（`PNG として読めない`）。
5. `type()` が `CV_8UC3` でなければ `8 ビット・3 チャンネルでない`、`rows` か `cols` が 256 でなければ `256×256 画素でない`（この順に見る）。
6. どれにも当たらなければ、読んだ画像、`unreadable` は偽、`reason` は空を返す。

- 読めないタイルの `bgr` は、無いタイルと同じく全画素が `cv::Vec3b(0, 0, 128)`（[HLD 4.4.2](30_HLD.md#442-処理の流れ) の 3「タイルの位置ごとの処理」の「全画素が (128, 0, 0) のタイルとして続ける」）。
- 署名を先に見るのは HLD 4.4.2 の 3 の「`cv::imread` は PNG でない画像の形式も読むため」。OpenCV や libpng が標準エラー出力に出す警告は止めない（UT は `read_tile` の標準エラー出力を比べない）。
- ファイルを開けない・読めないとき（権限、ディレクトリ）の理由を「PNG として読めない」に括弧で OS の理由を添えて入れるのは、`cv::imread` が開けないファイルを空の画像で返し、HLD 4.4.2 の 3 の「`cv::imread` が空の画像を返すもの」に当たるため。6.3 の `check_mesh_tiles` が「ある」とした位置（ディレクトリと権限で読めないものを含む）を、利用者に見えない NODATA にせず、挙げて止める。

##### select_dem_rgb

`cv::Vec3b select_dem_rgb(const cv::Vec3b& dem5a, const cv::Vec3b& dem5b, const cv::Vec3b& dem5c, const cv::Vec3b& dem10b)`

DEM5a、DEM5b、DEM5c、DEM10b の順に見て、`!= cv::Vec3b(0, 0, 128)`（RGB (128, 0, 0) と 3 つの値のどれか 1 つでも違う）ものを最初に返す。4 つとも等しければ `cv::Vec3b(0, 0, 128)` を返す（[HLD 4.2.2](30_HLD.md#422-処理の流れ) の 1〜3）。

##### decode_signed_elevation

`DecodedElevation decode_signed_elevation(const cv::Vec3b& bgr)`

`x = R × 65536 + G × 256 + B`（`R = bgr[2]`、`G = bgr[1]`、`B = bgr[0]`。`std::int32_t` で求める）。`x == 0x800000` なら `elevation = NODATA_ELEVATION`。`x > 0x800000` なら `static_cast<float>(x - 16777216) / 100.0f`。それ以外は `static_cast<float>(x) / 100.0f`（[HLD 4.3.2](30_HLD.md#432-処理の流れ) の 1、DEC44「標高は float32 でプロトタイプと同じ順に計算する」の順。整数を `float` に変えてから `float` の 100 で割る。`0.01f` を掛けない）。

##### clamp_to_sea_level

`float clamp_to_sea_level(std::int32_t x, float elevation)`

`x == 0x800000` なら `NODATA_ELEVATION`。それ以外で `elevation < 0.0f` なら `0.0f`、そうでなければ `elevation`（HLD 4.3.2 の 2。NODATA かは `x` で決め、値で決めない）。

##### pixel_center_mesh

`std::string pixel_center_mesh(const Z15Pixel& pixel)`

`const LatLon c = z15_pixel_center_latlon(pixel); return latlon_to_mesh(c.lat, c.lon);`（6.10）。引数を検査しない（どの値でも未定義の動作にならない。6.10.3）。

- 境目の扱い（[HLD 4.4.1](30_HLD.md#441-目的と範囲) の対象外の行）: 中心は `latlon_to_mesh` の `floor` で決まり、メッシュの南と西の境目はそのメッシュに、北と東の境目は隣のメッシュに入る（2.4 の表 5 の後の段落）。経度は中心が境目にちょうど乗ることが無い（中心の経度は `((gx + 0.5) / 2²³) × 360 − 180` で、整数の経度 `k − 180` に等しいには `gx + 0.5 = k × 2²³ / 360 = k × 2²⁰ / 45` が要り、左は整数と 0.5 の和、右は分母が奇数の分数なので等しくならない）。緯度は `sinh`・`atan` を通るので乗るかを式では言えないが、乗っても `floor` が 1 つに決める。
- 呼ぶ側（6.4 の `build_tile_elevation`、6.8 の `fill_zone`・`judge_area_complete`）は、返ったコードが集合にあるかを引く。空の文字列はどの集合にも無い（6.10.3 の `latlon_to_mesh`）。

##### build_tile_elevation

`TileElevation build_tile_elevation(const TileXY& tile, const std::set<std::string>& meshes, const MeshBounds& bbox, const std::string& tiles_dir)`

1. `tiles_dir` が空か最後のバイトが `/` なら `std::invalid_argument`。それでなくて `meshes` が空でも `std::invalid_argument("build_tile_elevation: meshes が空")`（この順に検査する。どちらか一方で投げる）。
2. 4 枚を `read_tile` で読む。パスは `tiles_dir + "/" + サービス名 + "/" + z + "/" + x + "/" + y + ".png"`（2.3。z・x・y は 10 進）で、DEM5a・DEM5b・DEM5c はズーム 15 の `(tile.x, tile.y)`、DEM10b はズーム 14 の `(tile.x / 2, tile.y / 2)`（整数の割り算。位置は 0 以上）。この順に読み、読めないタイルを `unreadable` にこの順に足す。DEM10b を読み直すか持っておくか（HLD 4.4.1 の対象外の行）は、位置ごとに読み直す（4 つの位置で同じ 1 枚を読む）。
3. 行と列のメッシュの番号: `k` を 0〜255 にして `pixel_center_mesh({256 × tile.x + k, 256 × tile.y + k})` を求め、その上 2 桁を行 `k` の、下 2 桁を列 `k` の番号として控える。空の文字列が返ったら `std::invalid_argument("build_tile_elevation: 画素の中心がメッシュの番号の範囲の外: " + 10 進の tile.x + "/" + 10 進の tile.y)`（タイルの位置を書く。画素の座標ではない）。画素 (i, j) の中心が入るメッシュは、行 `j` の上 2 桁と列 `i` の下 2 桁をつないだコードで、`pixel_center_mesh({256 × tile.x + i, 256 × tile.y + j})` と同じになる（中心の緯度は gy だけ、経度は gx だけで決まり〈2.4 の `z15_pixel_center_latlon`〉、`latlon_to_mesh` の上 2 桁は緯度だけ、下 2 桁は経度だけで決まるため）。
4. NODATA で埋める画素（HLD 4.4.2 の 4、DEC47「bbox 内で解析対象外の画素は中心で NODATA にする」）: 3 のコードの `mesh_to_latlon` が `bbox` の中（`south >= bbox.south`・`west >= bbox.west`・`north <= bbox.north`・`east <= bbox.east`）にあり、`meshes` に無い画素。`bbox` の値はどれかのメッシュの `mesh_to_latlon` の値そのもので、同じ式で求めた値どうしを比べるので、丸めで割れない。コードの組（タイルの中で高々 4 つ）ごとに 1 回だけ判定する。
5. 画素ごとに（`j` を 0〜255、各 `j` で `i` を 0〜255）: 4 の画素なら `NODATA_ELEVATION`。それ以外は、`select_dem_rgb(a(j, i), b(j, i), c(j, i), d(128 × (tile.x % 2) + i / 2 の列, 128 × (tile.y % 2) + j / 2 の行))`（`cv::Mat::at<cv::Vec3b>(行, 列)`。DEM10b の対応付けは HLD 4.4.2 の 3 の 2 つ目の箇条）を `decode_signed_elevation`、`clamp_to_sea_level` の順に当てた値。`values[j * 256 + i]` に書く。
6. 読んだタイルは返す前に捨てる（`cv::Mat` は関数を出るときに解放される。HLD 4.4.2 の 3 の最後の箇条、[NFR-002](20_SRS.md#nfr-002-メモリ使用量)）。

- 4 の画素は 4 つの DEM 種別の RGB をすべて (128, 0, 0) にしたのと同じ結果（`select_dem_rgb` が (128, 0, 0) を返し、デコードと 0m にそろえる処理が -9999 のまま残す）なので、直接 `NODATA_ELEVATION` を書く。
- 3 で 256 回だけ `pixel_center_mesh` を呼ぶのは、65,536 画素ごとに `sinh`・`atan` を通すと、最大の窓（約 46.5 億画素）で時間がかかるため。結果は画素ごとに呼んだときと同じで、UT で確かめる（UT 15）。

##### build_grid_z15

`GridResult build_grid_z15(const std::set<std::string>& meshes, const std::string& tiles_dir)`

1. `tiles_dir` を `build_tile_elevation` の 1 の前半と同じに確かめ（空か最後のバイトが `/` なら、`build_grid_z15` の名前で `std::invalid_argument`）、`box = tile_range(meshes)`（`meshes` の誤りは `tile_range` が投げる）。
2. 返す `GridResult result` を先に作り、`result.grid.width = (x_max − x_min + 1) × 256 + 2`、`result.grid.height = (y_max − y_min + 1) × 256 + 2`、`result.grid.values` を `std::int64_t` の `width × height` 個の `0.0f` にする（外周の 1 画素が海面ボーダーの 0。内側はすべて、この後の 3 でタイルの位置ごとに書く）。グリッドはこの 1 本だけを持ち、別の変数に作ってから写さない（写すと、写す間に同じ大きさの配列が 2 本になる）。
3. `y` を `y_min`〜`y_max`、各 `y` で `x` を `x_min`〜`x_max` の昇順に: `check_signal()`、`build_tile_elevation({x, y}, meshes, box.bbox, tiles_dir)`、読めないタイルのうちパスがまだ控えていないものを控え（読んだ順。同じパスは最初の理由のまま）、タイルの画素 (i, j) を `result.grid` の (256 × (x − x_min) + i + 1, 256 × (y − y_min) + j + 1) に写す。
4. 全部の位置を終えた後、`check_signal()` を呼び、控えが 1 つ以上あれば TR1 を出して止まる（HLD 4.4.2 の 5、DEC49「読めないタイルでは窓のタイルを読み終えてから挙げて止める」）。
5. `result.range` を `{meshes, false, box, {}}` にして `return result;`（グリッドの値をコピーしない。`range.meshes` には引数の `meshes` の複製を入れる）。

##### build_grid_z14

`GridResult build_grid_z14(const std::set<std::string>& meshes, const std::vector<TargetPeak>& peaks, const std::string& tiles_dir)`

1. `build_grid_z15` の 1 と同じ（`tiles_dir` の誤りは `build_grid_z14` の名前で投げる）。`peaks` の各 `pixel` が `256 × x_min ≤ gx < 256 × (x_max + 1)` と `256 × y_min ≤ gy < 256 × (y_max + 1)` に無ければ `std::invalid_argument("build_grid_z14: 対象ピークの画素が範囲の外: " + 10 進の gx + "/" + 10 進の gy)`（[HLD 4.14.2](30_HLD.md#4142-処理の流れ) の「Z14 のグリッドの生成」の 3 の「必ずグリッドの範囲にある」。呼ぶ側の誤り）。
2. `width = (x_max − x_min + 1) × 128 + 2`、`height = (y_max − y_min + 1) × 128 + 2`。ほかは `build_grid_z15` の 2 と同じ（`GridResult result` を先に作り、そのメンバーに書く）。
3. `build_grid_z15` の 3 と同じ順に位置を回し、`check_signal()`・`build_tile_elevation`・読めないタイルの控えも同じ。各位置で、`i`・`j` を 0〜127 にして、タイルの画素 (2i, 2j)・(2i + 1, 2j)・(2i, 2j + 1)・(2i + 1, 2j + 1) をこの順に見て、前に見たものより大きい（`>`）ときだけ採る（同じ値なら先のもの。北の行が先、同じ行は西が先。HLD 4.14.2 の 3、ADR-SRS-055）。採った値をグリッドの (128 × (x − x_min) + i + 1, 128 × (y − y_min) + j + 1) に書く。
4. 控え（DEC50「縮約で採った画素の座標は対象ピークを含む 2×2 だけ控える」）: その位置のタイルに入る対象ピーク（`gx / 256 == x` かつ `gy / 256 == y`）ごとに、`i = (gx % 256) / 2`、`j = (gy % 256) / 2` の 2×2 で 3 が採った画素の全球の Z15 の座標 `{256 × x + 採った列, 256 × y + 採った行}`（採った列・行は、タイルの中の 0〜255 の画素の列・行で、`2i` か `2i + 1`、`2j` か `2j + 1`）を、`picks[{128 × (x − x_min) + i + 1, 128 × (y − y_min) + j + 1}]` に入れる（同じ 2×2 に対象ピークが 2 つあっても 1 つの項目）。
5. `build_grid_z15` の 4 と同じ。`result.range` を `{meshes, true, box, <4 の控え>}` にして `return result;`（控えは `result.range.picks` に直接入れてよい）。

- 4 つとも NODATA の 2×2 は、`>` で先の画素（(2i, 2j)）を採り、値は NODATA になる（HLD 4.14.2 の 2）。

#### 6.4.4 メッセージ文面

書き方は [2.2](#22-ログとメッセージの文面)。`{entries}`・`{meshes}` は表の後に書く。

`ERROR:` のメッセージ（2 行目は `対処:` と空白 1 つの後）:

| 記号 | 場面 | 1 行目 | 2 行目 | 終了コード |
|---|---|---|---|---|
| TR1 | 読めない標高タイルがある | `読めない標高タイルがある: {entries}` | `挙げたファイルを消してから、それを取得範囲に含むメッシュ {meshes} のメッシュごとに venv/bin/python3 scripts/fetch_tiles.py --mesh <コード> を起動してタイルを取り直し、解析を起動し直す（消さずに取り直すと、提供元のタイルが変わっていなければ取り直さない。設定ファイルを指定して起動したときは、どちらにも同じ --config を付ける）` | 1 |

- `{entries}`: 控えた読めないタイルを控えた順に、1 件を `{path}（{reason}）` にして `、` でつないだもの。`{path}` は `build_tile_elevation` が組み立てた絶対パス、`{reason}` は `read_tile` の理由の文（6.4.3）。全件を挙げる（[HLD 4.4.3](30_HLD.md#443-異常系) の「読めなかったタイルのパスすべて」）。
- `{meshes}`: bounding box に入る 1 次メッシュ（上 2 桁が `meshes` の上 2 桁の最小〜最大、下 2 桁が下 2 桁の最小〜最大のコード。解析対象でないものも含む）のうち、控えた読めないタイルのどれかを取得範囲に含むものを、昇順に `、` でつないだもの。控えたタイルの位置は、`path` の末尾の `<サービス名>/<z>/<x>/<y>.png` から読む（`UnreadableTile` に位置の値は持たせない。サービス名が `dem_png` なら DEM10b のタイル、そうでなければ DEM5 のタイル。`<x>`・`<y>` は 10 進）。含むかは `tile_range({コード})` の範囲で見る: DEM5a・DEM5b・DEM5c のタイル (x, y) は `x_min ≤ x ≤ x_max` かつ `y_min ≤ y ≤ y_max`、DEM10b のタイル (X, Y) は `x_min / 2 ≤ X ≤ x_max / 2` かつ `y_min / 2 ≤ Y ≤ y_max / 2`（整数の割り算。ズーム 14 の取得範囲は、2.4 の決まりでズーム 15 の範囲を 2 で割ったものと同じになる）。`<コード>` は文字どおりそのまま書く（6.3 の `{refetch}` と同じ）。
- `{meshes}` に解析対象でないメッシュも入れるのは、bounding box の中の解析対象でないメッシュ（`--mesh` で範囲を絞った実行で起きる）の位置のタイルも、HLD 4.4.1 の「範囲のタイルはすべて読む」で読まれて挙がり、利用者が消したまま取り直さないと、後でそのメッシュを解析するときに取得完了の記録の後で消えたタイルとして黙って NODATA になる（[HLD 4.4.2](30_HLD.md#442-処理の流れ) の「取得完了の記録の後でキャッシュから消えたタイル」）ため。日本全土1次メッシュコードリストに無いコードか北方領土除外メッシュが入っても、CMP2 が警告して飛ばす（4.1 の TW1・TW2）。
- 括弧の「消さずに取り直すと…」は HLD 4.4.3 の表の行の注（`If-Modified-Since` で 304 になる）を利用者向けにしたもの。「設定ファイルを指定して…」は関数が設定ファイルの指定の有無を知らないので、いつでもそのまま書く（6.3 と同じ）。

出し方: `build_grid_z15`・`build_grid_z14` が出す。

#### 6.4.5 UT 候補

すべて自動。GoogleTest のケースごとに `// trace: UT-analyze_terrain_grid-NN`。共通の準備は 3 つ。

- **同じプロセス**: 6.2.5 の同じ名前の準備と同じ（`mkdtemp`、絶対パス、記述子 2 の付け替えで標準エラー出力を捕まえる、止まるケースは `ExitRequest` の `code` とメッセージの 2 行の全文）。
- **タイルを置く**: `tiles_dir` は一時のディレクトリの下の `tiles`（作る）。タイルは `<tiles_dir>/<サービス名>/<z>/<x>/<y>.png` に、ディレクトリを作ってから、`cv::Mat(256, 256, CV_8UC3, cv::Scalar(b, g, r))` を `cv::imwrite` で書く（RGB で書いた色を B・G・R の順に渡す）。ケースが一部の画素の色を書くときは、書く前にその画素を `at<cv::Vec3b>(行, 列)` で替える。標高の色: 50m は RGB (0, 19, 136)、70m は (0, 27, 88)、100m は (0, 39, 16)、200m は (0, 78, 32)、300m は (0, 117, 48)、400m は (0, 156, 64)、500m は (0, 195, 80)（それぞれ x が 5000・7000・10000・20000・30000・40000・50000）。NODATA は (128, 0, 0)。期待の標高は `static_cast<float>(x) / 100.0f` と `EXPECT_EQ`（`50.0f` などに等しい）。
- **子のプロセス**: 6.12.5 の同じ名前の準備と同じ。

| ID | 確かめること | 準備 | 入力 | 期待 |
|---|---|---|---|---|
| `UT-analyze_terrain_grid-01` | 範囲（2.4 の表 4・表 8） | 同じプロセス | `tile_range` に 2.4 の表 4 のズーム 15 の 4 行のメッシュ 1 つの集合（`{4934}`・`{5235}`・`{5339}`・`{6848}`）と、表 8 の 3 行の集合 | `x_min`・`x_max`・`y_min`・`y_max` が表の行と等しい。`bbox` の 4 つは集合の各メッシュの 2.4 の表 1 の値の最小・最大と `==`（`{5235, 5336}` は `34.666666666666664`・`135.0`・`36.0`・`137.0`） |
| `UT-analyze_terrain_grid-02` | 範囲の呼ぶ側の誤り | 同じプロセス | `tile_range` に (a) 空、(b) `{53a9}`、(c) `{0035}`、(d) `{9935}`、(e) `{5200}`、(f) `{5279}`、(g) `{5235, 533}` | どれも `std::invalid_argument`。ほかに `{0101}`・`{9878}` は投げない |
| `UT-analyze_terrain_grid-03` | DEM の順 | 同じプロセス。RGB で `A = (0, 39, 16)`、`B = (0, 78, 32)`、`C = (0, 117, 48)`、`D = (0, 156, 64)`、`N = (128, 0, 0)` | `select_dem_rgb` に (a) `A, B, C, D`、(b) `N, B, C, D`、(c) `N, N, C, D`、(d) `N, N, N, D`、(e) `N, N, N, N`、(f) `(128, 0, 1), B, C, D`、(g) `N, B, N, D` | (a) `A`、(b) `B`、(c) `C`、(d) `D`、(e) `N`（`cv::Vec3b(0, 0, 128)`）、(f) `(128, 0, 1)`、(g) `B` |
| `UT-analyze_terrain_grid-04` | デコード | 同じプロセス | `decode_signed_elevation` に RGB (a) `(0, 39, 16)`、(b) `(0, 0, 0)`、(c) `(127, 255, 255)`、(d) `(128, 0, 0)`、(e) `(128, 0, 1)`、(f) `(240, 190, 36)`、(g) `(255, 255, 255)` | `x` は (a) 10000、(b) 0、(c) 8388607、(d) 8388608、(e) 8388609、(f) 15777316、(g) 16777215。`elevation` は (a) `10000.0f / 100.0f`、(b) `0.0f`、(c) `8388607.0f / 100.0f`、(d) `-9999.0f`、(e) `-8388607.0f / 100.0f`、(f) `-999900.0f / 100.0f`（`-9999.0f` に等しい）、(g) `-1.0f / 100.0f`（どれも `EXPECT_EQ`） |
| `UT-analyze_terrain_grid-05` | 0m にそろえる | 同じプロセス | `clamp_to_sea_level` に (a) `(8388608, -9999.0f)`、(b) `(15777316, -9999.0f)`、(c) `(16777215, -0.01f)`、(d) `(10000, 100.0f)`、(e) `(0, 0.0f)` | (a) `-9999.0f`、(b) `0.0f`（値が -9999 でも NODATA でない）、(c) `0.0f`、(d) `100.0f`、(e) `0.0f` |
| `UT-analyze_terrain_grid-06` | 画素の中心のメッシュ（2.4 の表 7） | 同じプロセス | `pixel_center_mesh` に `(7374984, 3685299)`・`(7374984, 3685300)`・`(7153617, 3553537)`・`(7153618, 3553537)`・`(7340031, 3322709)`・`(7340032, 3322709)` | `3236`・`3136`・`3926`・`3927`・`5234`・`5235` |
| `UT-analyze_terrain_grid-07` | タイルを読む | 同じプロセス。タイルを置く（DEM5a の (28700, 12980) に 100m の色、画素 (列 3, 行 5) だけ 200m の色） | `read_tile(<そのパス>)` | `unreadable` が偽、`reason` が空、`type()` が `CV_8UC3`、256×256、`at<cv::Vec3b>(5, 3)` が `cv::Vec3b(32, 78, 0)`、`at<cv::Vec3b>(0, 0)` が `cv::Vec3b(16, 39, 0)` |
| `UT-analyze_terrain_grid-08` | 無いタイル | 同じプロセス | (a) 存在しないパス、(b) 普通のファイルの下のパス（`<ファイル>/1.png`） | どちらも `unreadable` が偽、`reason` が空、256×256 の `CV_8UC3` で全画素が `cv::Vec3b(0, 0, 128)`（`cv::countNonZero` を各チャンネルで数えるか、全画素を比べる） |
| `UT-analyze_terrain_grid-09` | 読めないタイル | 同じプロセス。ファイルごとに別のパス | (a) 中身が `<?xml version="1.0"?>`、(b) 0 バイト、(c) 署名の先頭 7 バイトだけ、(d) 署名の 8 バイトの後に `xxxx`、(e) `.png` で終わる名前のディレクトリ、(f) `CV_8UC4` の 256×256 を `cv::imwrite`、(g) `CV_16UC3` の 256×256、(h) `CV_8UC1` の 256×256、(i) `cv::Mat(256, 255, CV_8UC3, …)`（行 256・列 255）、(j) `cv::Mat(255, 256, CV_8UC3, …)`（行 255・列 256） | どれも `unreadable` が真で、全画素が `cv::Vec3b(0, 0, 128)` の 256×256。`reason` は (a)(b)(c) `PNG の署名でない`、(d) `PNG として読めない`、(e) `PNG として読めない（Is a directory）`、(f)(g)(h) `8 ビット・3 チャンネルでない`、(i)(j) `256×256 画素でない` |
| `UT-analyze_terrain_grid-10` | 権限で開けない | 同じプロセス。100m の色の PNG を置いて `chmod 000`。`geteuid() == 0` なら `GTEST_SKIP()` | `read_tile(<そのパス>)` | `unreadable` が真、`reason` が `PNG として読めない（Permission denied）` |
| `UT-analyze_terrain_grid-11` | DEM の順とデコード（タイルから） | 同じプロセス。それぞれ別の `tiles_dir`。位置は (28700, 12980)、`meshes` は `{5235}`、`bbox` は `tile_range({5235}).bbox` | (a) DEM5a に、列 0〜127 が 100m・列 128〜255 が NODATA の色のタイル、DEM5b に 200m の色のタイル（DEM5c と DEM10b は置かない）、(b) タイルを 1 枚も置かない、(c) DEM5a に画素 (列 0, 行 0) だけ RGB (255, 255, 255)・ほかは 100m のタイル | (a) 列 0〜127 は `100.0f`、列 128〜255 は `200.0f`、`unreadable` は空。(b) 全画素が `-9999.0f`。(c) (0, 0) が `0.0f`（海面下を 0m に）、ほかは `100.0f` |
| `UT-analyze_terrain_grid-12` | DEM10b の対応付け | 同じプロセス。DEM10b の (14350, 6490) に、列 0〜127・行 0〜127 が 100m、列 128〜255・行 0〜127 が 200m、列 0〜127・行 128〜255 が 300m、列 128〜255・行 128〜255 が 400m、画素 (列 133, 行 7) だけ 500m のタイル。DEM5 は置かない | `build_tile_elevation` を位置 (28700, 12980)・(28701, 12980)・(28700, 12981)・(28701, 12981) で（`meshes` と `bbox` は 11 と同じ） | 全画素が順に `100.0f`・`200.0f`・`300.0f`・`400.0f`。ただし (28701, 12980) の画素 (列 10〜11, 行 14〜15) の 4 つは `500.0f` |
| `UT-analyze_terrain_grid-13` | NODATA で埋める範囲（2.4 の表 4） | 同じプロセス。DEM5a の (28763, 13000) と (28700, 12942) に 100m の色のタイル | (a) 位置 (28763, 13000)、`meshes` が `{5235, 5336}`、`bbox` は `tile_range({5235, 5336}).bbox`、(b) (a) の位置で `meshes` が `{5235}`、`bbox` は `tile_range({5235}).bbox`、(c) 位置 (28700, 12942)、(a) と同じ `meshes`・`bbox` | (a) 列 0〜5 は `100.0f`、列 6〜255 は `-9999.0f`（`5236` は bounding box の中で解析対象でない）。(b) 全画素が `100.0f`（`5236` は bounding box の外のはみ出し）。(c) 行 0〜55 は `-9999.0f`（`5335`）、行 56〜255 は `100.0f` |
| `UT-analyze_terrain_grid-14` | 読めないタイルを返す | 同じプロセス。位置 (28700, 12980)。DEM5a に NODATA の色のタイル、DEM5b に中身が `<?xml version="1.0"?>` のファイル、DEM5c に 300m の色のタイル、DEM10b の (14350, 6490) に `CV_8UC4` の PNG | `build_tile_elevation`（`meshes` と `bbox` は 11 と同じ） | 全画素が `300.0f`。`unreadable` は 2 件で、順に `{<DEM5b のパス>, "PNG の署名でない"}`、`{<DEM10b のパス>, "8 ビット・3 チャンネルでない"}`。標準エラー出力に `ERROR:` の行が無い |
| `UT-analyze_terrain_grid-15` | 行と列で求めたメッシュが画素ごとと同じ | 同じプロセス。DEM5a の (28763, 12942) に 100m の色のタイル | `build_tile_elevation` を位置 (28763, 12942)、`meshes` が `{5235}`、`bbox` は `tile_range({5235, 5336}).bbox` で | 各画素 (i, j) が、`pixel_center_mesh({256 × 28763 + i, 256 × 12942 + j})` が `5235` なら `100.0f`、そうでなければ `-9999.0f`（65,536 画素をすべて比べる）。行 56〜255 かつ列 0〜5 だけが `100.0f` |
| `UT-analyze_terrain_grid-16` | タイルの呼ぶ側の誤り | 同じプロセス | `build_tile_elevation` の (a) `tiles_dir` が空、(b) 末尾が `/`、(c) `meshes` が空 | どれも `std::invalid_argument` |
| `UT-analyze_terrain_grid-17` | Z15 のグリッド | 同じプロセス。DEM5a の (28672, 12942) に 100m、(28763, 13016) に 200m の色のタイル | `build_grid_z15({5235}, tiles_dir)` | `width` が 23554、`height` が 19202。外周（px が 0 か 23553、py が 0 か 19201）はすべて `0.0f`。(1, 1) が `100.0f`、(23552, 19200) が `200.0f`（南東の隅のタイルの画素 (255, 255)。中心は `5136` で、bounding box の外のはみ出しなので値が残る）、(257, 1) が `-9999.0f`（タイルが無い位置）。`range.meshes` が `{5235}`、`range.z14` が偽、`range.box` が `tile_range({5235})` と同じ、`range.picks` が空 |
| `UT-analyze_terrain_grid-18` | 読めないタイルで止まる | 同じプロセス。DEM5a の (28672, 12942) と DEM10b の (14336, 6471) に、中身が `<?xml version="1.0"?>` のファイル | (a) `build_grid_z15({5235}, tiles_dir)`、(b) `build_grid_z14({5235}, {}, tiles_dir)`。ほかに (c) 別の `tiles_dir` で、DEM5a の (28800, 12980)（`5236` の取得範囲だけに入る位置）に同じ中身のファイルを置き、`build_grid_z14({5235, 5336}, {}, tiles_dir)` | (a)(b) `code` が 1 の TR1。1 行目は `ERROR: 読めない標高タイルがある: <tiles_dir>/dem5a_png/15/28672/12942.png（PNG の署名でない）、<tiles_dir>/dem_png/14/14336/6471.png（PNG の署名でない）`（DEM10b のタイルは 4 つの位置で読むが 1 件）。2 行目は 6.4.4 の TR1 の文で `{meshes}` が `5235`。(c) `code` が 1 の TR1 で、`{meshes}` が `5236`（解析対象でない bounding box の中のメッシュ） |
| `UT-analyze_terrain_grid-19` | Z14 のグリッドと縮約 | 同じプロセス。DEM5a の (28700, 12980) に 50m の色で、画素 (列 10, 行 20) が 100m、(11, 20) が 300m、(10, 21) が 300m、(11, 21) が 200m のタイル。DEM5a の (28701, 12980) に 70m の色で、画素 (列 0, 行 0)・(列 1, 行 0)・(列 0, 行 1) が NODATA の色のタイル。DEM5a の (28702, 12980) に NODATA の色で、画素 (列 2, 行 2) だけ 100m のタイル、DEM5b の (28702, 12980) に 300m の色のタイル。`peaks` は `TargetPeak` 2 つで、`pixel` が `{256 × 28700 + 10, 256 × 12980 + 21}` と `{256 × 28702 + 2, 256 × 12980 + 2}`（`peak` は既定の値） | `build_grid_z14({5235}, peaks, tiles_dir)` | `width` が 11778、`height` が 9602。(3590, 4875) が `300.0f`、(3585, 4865) が `50.0f`、(3713, 4865) が `70.0f`（3 つが NODATA の 2×2）、(1, 1) が `-9999.0f`、(3842, 4866) が `300.0f`（画素ごとにフォールバックしてから縮約するので、DEM5a の 100m でなく DEM5b の 300m になる。DEM 種別ごとに先に縮約すると 100m になる）。`range.z14` が真、`range.picks` は 2 件で、鍵 `{3590, 4875}` の値が `{256 × 28700 + 11, 256 × 12980 + 20}`（同じ 300m の 2 つのうち北の行）、鍵 `{3842, 4866}` の値が `{256 × 28702 + 3, 256 × 12980 + 2}`（採った 300m の画素は (列 3, 行 2)。北の行の先頭の (列 2, 行 2) は 100m） |
| `UT-analyze_terrain_grid-20` | 控えの重なりと範囲の外 | 同じプロセス。タイルは置かない | (a) `peaks` の `pixel` が `{256 × 28700 + 10, 256 × 12980 + 21}` と `{256 × 28700 + 11, 256 × 12980 + 20}`（同じ 2×2）、(b) `peaks` の `pixel` が `{256 × 28764, 256 × 12980}`（x が範囲の外） | (a) `range.picks` が 1 件で、鍵 `{3590, 4875}`、値 `{256 × 28700 + 10, 256 × 12980 + 20}`（4 つとも NODATA で、先の画素）。(b) `std::invalid_argument`（`meshes` は `{5235}`） |
| `UT-analyze_terrain_grid-21` | シグナルで止まる | 子のプロセス。タイルは置かない | 子の中で `start_log` の後に、`kill(getpid(), SIGTERM)`、`build_grid_z15({5235}, tiles_dir)` | `ExitRequest` の `code` が 143（最初の位置の `check_signal`）。子の終了コードが 143 |
| `UT-analyze_terrain_grid-22` | グリッドの呼ぶ側の誤り | 同じプロセス | `build_grid_z15`・`build_grid_z14` のそれぞれに (a) `tiles_dir` が空、(b) 末尾が `/`、(c) `meshes` が空 | どれも `std::invalid_argument` |

- UT 17〜21 は、UT 18 の (c) 以外はメッシュ 1 つの窓で、Z15 のグリッドは約 1.8GB（約 4.5 億画素の `float`）、Z14 は約 0.45GB を使う。UT 18 の (c) は `{5235, 5336}` の 2 メッシュの窓で、Z14 でも約 1.8GB を使う（メモリを多く使うので、実行する環境のメモリを確かめてから回す）。

### 6.5 `analyze_terrain_image`

- **ID**: LLD-analyze_terrain_image
- **対応 HLD**: [3.4](30_HLD.md#34-cmp4-地形解析エンジン)・[4.15](30_HLD.md#415-fr-015-標高地形図出力)・[5.9](30_HLD.md#59-nfr-009-観測可能性中間成果物の可視化)
- **ファイル**: `src/image.hpp`・`src/image.cpp`・`src/image_gist_earth.hpp`

関数の名前と役割は [HLD 3.4.3](30_HLD.md#343-関数) の表の「標高地形図」の群（`render_terrain`・`write_terrain_png`）で、処理の正本は [HLD 4.15.2](30_HLD.md#4152-処理の流れ) の 1〜9、止まる場面は [4.15.3](30_HLD.md#4153-異常系)、計算の決まりは [4.15.4](30_HLD.md#4154-設計判断) の DEC65「色と陰影は `LightSource.shade()` と同じ」・DEC66「NODATA と海面は 0 にしてから色と陰影を求める」・DEC67「`vmax` は縮小の前のグリッド全体の最大標高にする」・DEC68「縮小は出力の画素の中心に当たる画素を採る」である。[HLD 4.15.1](30_HLD.md#4151-目的と範囲) の対象外の行が LLD に送った項目（表の引き方、勾配の端、引き伸ばせないときの扱い、精度、8 ビットの丸め、縮小の式を整数で数えるか、白の画素の印、表の版と作り方、参照実装と比べるテスト）は、6.5.1〜6.5.5 で決める。matplotlib をテストの依存に入れるかと版の固め方は、[テスト方針書 3.3](02_test_policy.md#33-期待値の根拠) の最後の箇条で決めた。置き場の名前と一時ファイルの書き方は [2.3](#23-ファイルの名前と書き方) で決まっている。関数を呼ぶ順は 6.11 の `run_normal_mode`・`run_wide_mode`（`render_terrain` → `write_terrain_png` → `make_scan_order`。[HLD 3.4.3](30_HLD.md#343-関数) の呼ぶ順）で、6.5 は渡されたグリッドと解析識別子とパスを受け取る。`check_signal` は呼ばない（[HLD 3.4.3](30_HLD.md#343-関数) の `check_signal` を呼ぶ群に「標高地形図」は入っていない。[6.9](#69-analyze_terrain_record) と同じ）。[HLD 5.9](30_HLD.md#59-nfr-009-観測可能性中間成果物の可視化) の表に標高地形図の行は無く、6.5 が 5.9 から足して受けるものは無い（標高地形図は [FR-015](20_SRS.md#fr-015-標高地形図出力) のとおり解析単位ごとに書き、段の始まりで消さない。[HLD 2.10.3](30_HLD.md#2103-フェーズのやり直し)）。この節は、それを C++ で書くための細部を足す。1.2 の C++ の規約に従う。

#### 6.5.1 ファイル割付

- 公開の宣言は `src/image.hpp`、定義と内部の関数は `src/image.cpp` に置く。どちらも先頭のコメントに `// trace: LLD-analyze_terrain_image` を書き、ヘッダーは次の行を `#pragma once` にする。
- 表のファイル `src/image_gist_earth.hpp`: gist_earth の 256 色の表を置く（1.2 の C++ の規約の「群ごとに 2 本」の例外で、6.5 だけ表のファイルを 1 本足す。拡張子を `.hpp` にするのは、`tools/lint_trace.py` が数えるコードの拡張子に `.inc` が無いため）。中身は、1 行目 `// trace: LLD-analyze_terrain_image`、2 行目 `#pragma once`、3 行目 `// matplotlib 3.11.2 の gist_earth の表（6.5.1 のコマンドで作った。手で直さない）`、4 行目 `inline constexpr double GIST_EARTH_LUT[256][3] = {`、続けて 256 行の `{赤, 緑, 青},`（matplotlib の `_lut` の 0〜255 行目の赤・緑・青。値は Python の `repr` の最短の 10 進表記で、倍精度で読めば元の値と同じになる）、最後の行 `};` である。`GIST_EARTH_LUT` は LLD が足す定数の名前で、`src/image.cpp` だけが読む。表を作るコマンドは次のとおり（matplotlib 3.11.2 と numpy 2.5.4 を入れた一時の仮想環境で動かす。実行にも CI にも、リポジトリの依存にも matplotlib を入れない。[テスト方針書 3.3](02_test_policy.md#33-期待値の根拠)）。出力の 256 行を、上の 4 行と最後の `};` ではさんでファイルにする。

  ```text
  python -I -c "import matplotlib; c = matplotlib.colormaps['gist_earth']; c._init(); print('\n'.join('{%r, %r, %r},' % tuple(float(v) for v in row[:3]) for row in c._lut[:256]))"
  ```

  表の 0 行目は `{0.0, 0.0, 0.0}`、255 行目は `{0.9922, 0.9843, 0.9843}` である。表の中身は UT 候補の 01〜03・05 の色で確かめる。
- `src/image.hpp` は `"grid.hpp"`（`ElevationGrid`・`GridRange`）・`<cstdint>`・`<string>`・`<vector>` を読む。`src/image.cpp` は `"image.hpp"`・`"common.hpp"`・`"convert.hpp"`（`tile_to_latlon`）・`"image_gist_earth.hpp"`・`<opencv2/core.hpp>`・`<opencv2/imgcodecs.hpp>`・`<cerrno>`・`<cmath>`・`<cstdio>`・`<cstring>`・`<fcntl.h>`・`<numbers>`・`<stdexcept>`・`<string>`・`<unistd.h>`・`<vector>` を読む。
- UT のコードは `tests/src/test_image.cpp` に置き、`build/test_image` にビルドする（[2.5](#25-ビルドとテストの名前)）。各テストに `// trace: UT-analyze_terrain_image-NN`（確かめる UT 候補の ID）のコメントを付ける。テストの枠組みは GoogleTest（[テスト方針書 3.4](02_test_policy.md#34-テストを先に書く進め方)）。

#### 6.5.2 型とデータ

`src/image.hpp` の公開の宣言は次のとおり（名前空間に入れない。1.2 の C++ の規約）。

```cpp
#pragma once
#include <cstdint>
#include <string>
#include <vector>
#include "grid.hpp"

struct TerrainImage {
    int width = 0;                  // W'
    int height = 0;                 // H'
    std::vector<std::uint8_t> rgb;  // 画素 (i, j) の赤・緑・青は rgb[(static_cast<std::int64_t>(j) * width + i) * 3 + 0〜2]
};

TerrainImage render_terrain(const ElevationGrid& grid, const GridRange& range,
                            const std::string& analysis_id);
void write_terrain_png(const TerrainImage& image, const std::string& analysis_id,
                       const std::string& images_dir);
```

- 引数の並びは [HLD 3.4.3](30_HLD.md#343-関数) の表の受け取るものの順。`grid`・`range` は [6.4.2](#642-型とデータ) の `ElevationGrid`・`GridRange`（`range.meshes` は解析対象メッシュ、`range.z14` は Z14 のグリッドか、`range.box.y_min` は Z15 のタイル番号の範囲の北端）。`analysis_id` は解析識別子（[6.9.3](#693-関数の細部) の `write_meshset` と同じ形）。`images_dir` は `data_dir` の下の `images` の絶対パスで、末尾に `/` を付けない（6.11 が組み立てて渡す）。
- `TerrainImage` は OpenCV の型を使わない（`render_terrain` を OpenCV なしで確かめられるようにし、青・緑・赤の並べ替えを `write_terrain_png` の中に閉じるため）。
- 持つもの: `render_terrain` の中で持つのは、出力の画素ごとの標高（`std::vector<double>`）と明るさ（`std::vector<double>`）と、返す `rgb` である。6000 × 6000 で 288MB + 288MB + 108MB。色は明るさを求めた後に画素ごとに求めて `rgb` に書き、配列にしない。標高と明るさは戻る前に捨てる（関数の中の変数）。[HLD 4.15.2](30_HLD.md#4152-処理の流れ) の末尾の見積もり（倍精度で約 1.4GiB）に収まる。
- 呼ぶ側の誤りは `std::invalid_argument` を投げる（グリッドと画像に触れる前に確かめる。文は 6.9 と同じ `<関数名>: …` の形）。確かめる順と文は 6.5.3 の各関数の 1 に書く。
- 内部（`src/image.cpp` の無名の名前空間）の関数のうち、LLD が形を決めるのは `bool _write_all(int fd, const unsigned char* data, std::size_t size)` だけ（[6.12.3](#6123-関数の細部) の内部の `_write_all` と同じ形: `write` を、全部書くか `EINTR` のほかの失敗まで繰り返す。失敗したら `false` を返し、`errno` を残す）。6.12 の内部の関数はほかの `.cpp` から呼べないので、同じ形を置く。解析識別子の形の判定（6.9.3 の `write_meshset` の 1 の 2 つ目と同じ）、`{rerun}`・`{meshes}` の組み立て、IW1 を出して止まる手順のように、2 つの関数で同じ判定や文を使う補助の関数は、足してよい（名前と形は書く人が決め、公開の宣言には出さない）。

#### 6.5.3 関数の細部

処理の正本は上の前置きのとおりで、この節は C++ で書くための細部を足す。止まるときは、メッセージを `log_error` で出してから `throw ExitRequest(EXIT_ERROR)` する（1.2 の C++ の規約）。通常のログと警告は出さない。計算は倍精度で、`-ffp-contract=off` の下で、書いた順に行う。

`render_terrain` の計算は、matplotlib 3.11.2 の `LightSource(azdeg=180, altdeg=77.7).shade(E, cm.gist_earth, vmin=vmin, vmax=vmax, vert_exag=8, dx=dx, dy=dy)`（`blend_mode` は overlay、`fraction` は 1。`E` は縮小して 0 以下を 0 にした標高の倍精度の配列、`vmin`・`vmax`・`dx`・`dy` は Python の float）の計算と同じ順にする。対応する matplotlib の関数は、`colors.py` の `Normalize.__call__`・`Colormap._get_rgba_and_mask`・`LightSource.direction`・`hillshade`・`shade_normals`・`shade`・`shade_rgb`・`blend_overlay` と、`colorizer.py` の `_pass_image_data`（`bytes=True`）、numpy 2.5.4 の `gradient`（`edge_order=1`）である。C++ の和は左から足す。参照の側（numpy の `dot`）の和の順や `sin`・`cos` の違いは、UT 候補の許容差（各チャンネル ±1）で吸う。

##### render_terrain

1. 引数を次の順に確かめ、最初に当たったもので `std::invalid_argument` を投げる。
   - `grid.width` か `grid.height` が 1 未満: `render_terrain: grid の幅か高さが 1 未満: <width>x<height>`。
   - `grid.values.size()` が `width × height`（64 ビットで求める）と違う: `render_terrain: grid.values の個数が幅 × 高さと違う: <個数>`。
   - `analysis_id` が解析識別子の形でない（判定は 6.9.3 の `write_meshset` の 1 の 2 つ目と同じ）: `render_terrain: analysis_id が解析識別子の形でない: <値>`。
   - `range.meshes` が空: `render_terrain: range.meshes が空`。
   - 手順 3 で求める出力の幅 `W'` か高さ `H'` が 2 未満（手順 3 の式を、手順 2 の前に、ここで求めて確かめる。`W'`・`H'` の値は手順 3 のとおり）: `render_terrain: 縮小後の幅か高さが 2 未満: <W'>x<H'>`（`np.gradient` は 2 画素ない軸を受けない。実際のグリッドは長辺が 6000 を超え、短辺も 2 未満にならない）。
2. `vmax`: `grid.values` の最大を、`float` のまま比べて取り、`double` にする。`vmax <= 0.0` なら IM1 を出して止まる。
3. 出力の大きさ `W'`・`H'`: `W = grid.width`、`H = grid.height`、`L = max(W, H)`。`L ≤ 6000` なら `W' = W`、`H' = H`。超えれば長辺を 6000 にし、短辺 `s` は `(2 × s × 6000 + L) / (2 × L)`（`std::int64_t` の整数の割り算。四捨五入で 0.5 は切り上げ）にする。`W = H` のときはどちらも 6000。
4. 縮小と標高 `E`: 出力の画素 `(i, j)` には、グリッドの画素 `(((2 × i + 1) × W) / (2 × W'), ((2 × j + 1) × H) / (2 × H'))`（`std::int64_t` の整数の割り算。[DEC68](30_HLD.md#4154-設計判断) の ⌊(i + 0.5) × W / W'⌋ と同じ値）の標高を当てる。その値を `double` にし、0 以下なら 0.0 にしたものを `E` とする。白で塗る画素は `E` が 0.0 の画素とし、印を別に持たない（陸地の画素の標高は正なので 0.0 にならない）。
5. 正規化と色: `vmin = (-0.25 * vmax) / 0.75`、`v = (E - vmin) / (vmax - vmin)`。色の添字 `k = static_cast<int>(v * 256.0)` で、`k` が 256 以上なら 255、0 未満なら 0 にする（`E` は 0 以上 `vmax` 以下なので 0 未満と 256 超は起きないが、matplotlib の範囲外の色〈下は 0 行目、上は 255 行目〉と同じにする）。色 `c` は `GIST_EARTH_LUT[k]` の赤・緑・青の 3 つの `double`。
6. 緯度と画素の間隔: `row = (range.z14 ? 128.0 : 256.0) * range.box.y_min - 1.0 + H / 2.0`（`H` は縮小の前の高さ。`double`）、`z = range.z14 ? 22 : 23`、`phi = tile_to_latlon(0.0, row, z).lat`（[6.10](#610-analyze_terrain_convert)。経度は使わない）。`res = 2.0 * std::numbers::pi * 6378137.0 * std::cos(phi * (std::numbers::pi / 180.0)) / std::ldexp(1.0, z)`（度からラジアンへは numpy の `np.radians` と同じ `x * (π / 180)` の順）、`dx = res * (static_cast<double>(W) / W')`、`dy = res * (static_cast<double>(H) / H')`。
7. 明るさ（`LightSource.hillshade(E, vert_exag=8, dx, dy)`）:
   - `F = 8.0 × E`（`F`・`ex`・`ey`・法線・内積は、画素ごとに `E` から求めて配列にしない。配列に持つのは `E`・`I`・`rgb` だけで、6.5.2 の「持つもの」の見積もりに収める）。
   - 列の勾配 `ex`: 0 < i < W' − 1 は `(F[i+1] − F[i−1]) / (2.0 * dx)`、i = 0 は `(F[1] − F[0]) / dx`、i = W' − 1 は `(F[W'−1] − F[W'−2]) / dx`（行 j ごと）。行の勾配 `ey` は同じ式で、列を行に、`dx` を `h = -dy` に替える（北から数える行を上にするため符号を反転する。matplotlib の `dy = -dy`）。
   - 法線は `nx = -ex`、`ny = -ey`、`m = std::sqrt(nx * nx + ny * ny + 1.0)`（左から足す）として、`(nx / m, ny / m, 1.0 / m)`。
   - 光源の向き `d = (cos(az) × cos(alt), sin(az) × cos(alt), sin(alt))`、`az = (90.0 - 180.0) * (std::numbers::pi / 180.0)`、`alt = 77.7 * (std::numbers::pi / 180.0)`。
   - 明るさ `I = nx/m × d0 + ny/m × d1 + (1.0/m) × d2`（左から足す）。
   - 全画素の最小 `imin` と最大 `imax` を求め、`imax - imin > 1e-6` なら全画素を `(I - imin) / (imax - imin)` にする。それ以外は引き伸ばさない（平らな絵では `I` はどの画素も sin(alt) ≈ 0.977 になる）。最後に 0 未満を 0、1 を超えるものを 1 にする。
8. 合成（`blend_overlay`）: チャンネルごとに、`c ≤ 0.5` なら `2.0 * I * c`、それ以外は `1.0 - 2.0 * (1.0 - I) * (1.0 - c)`。
9. 白: `E` が 0.0 の画素は 3 チャンネルとも 1.0 にする。
10. 8 ビット: 値 `x` を `static_cast<std::uint8_t>(x * 255.0)`（切り捨て。`x` は 0〜1）にする。`rgb` の順は赤・緑・青。

- グリッドは書き換えない（`const`）。並列にしない（[HLD 2.9](30_HLD.md#29-並行性スレッド設計) は並列にしてよいとするが、LLD では逐次にする。最小と最大を確定してから引き伸ばす順だけを守る）。
- 採用のサンプル（[ADR-SRS-047](decisions/ADR-SRS-047-terrain-color-scheme-gist-earth-hillshade.md)）は `imshow` と `savefig` を通っていて、表示のときに補間し直されているので、画素で比べる相手にしない（6.5.5 の前置き）。

##### write_terrain_png

1. 引数を次の順に確かめ、最初に当たったもので `std::invalid_argument` を投げる（ファイルに触れる前に確かめる）。
   - `images_dir` が空か、最後のバイトが `/`: `write_terrain_png: images_dir が空か / で終わる: <値>`。
   - `analysis_id` が解析識別子の形でない: `write_terrain_png: analysis_id が解析識別子の形でない: <値>`。
   - `image.width` か `image.height` が 1 未満: `write_terrain_png: image の幅か高さが 1 未満: <width>x<height>`。
   - `image.rgb.size()` が `width × height × 3`（64 ビットで求める）と違う: `write_terrain_png: image.rgb の個数が幅 × 高さ × 3 と違う: <個数>`。
2. バイト列にする。`cv::Mat bgr(image.height, image.width, CV_8UC3)` に、画素ごとに青・緑・赤の順で写す。`std::vector<unsigned char> buf` に `cv::imencode(".png", bgr, buf)`（引数の指定なし。OpenCV の既定の圧縮）。偽を返すか `cv::Exception` が出たら IW1（`{reason}` は `PNG のバイト列に変換できない`）を出して止まる。
3. パスを決め、書く。`path = images_dir + "/" + analysis_id + "_terrain.png"`、`tmp = path + ".tmp"`（[2.3](#23-ファイルの名前と書き方) の一時ファイルの決まり）。2.3 の「書く（C++）」で `tmp` に `buf` を書く（`_write_all` を使う）。開く・書く・`fsync`・`close` のどれで失敗しても、2.3 のとおり後始末をしてから、IW1（`{reason}` は控えた `errno` の `std::strerror`）を出して止まる。
4. 置き換える。2.3 の「置き換える（C++）」で `rename(tmp, path)` を呼ぶ。失敗したら、`errno` を控え、`unlink(tmp)`（失敗は無視する）してから、IW1 を出して止まる（置き換えに失敗したときに一時ファイルを消す。6.9 と同じ）。
5. 戻る。`path` が書き終えた中身か、前の起動が書いた中身のどちらかになる。書けずに止まったときは、前の起動の標高地形図を消さない。

- IW1 の `{path}` は、どの段で失敗しても `path`（一時ファイルでなく本来の名前）。
- ディレクトリを作らない（`images/` を作るのは 6.11。`images_dir` が無ければ `open` が `ENOENT` で失敗して IW1 になる）。ディレクトリの `fsync` はしない（2.3 と同じ）。
- `cv::imwrite` は使わない（拡張子で形式を決めるので `.png.tmp` に書けず、失敗の理由〈`errno`〉も返さない）。

#### 6.5.4 メッセージ文面

書き方は [2.2](#22-ログとメッセージの文面)。

`ERROR:` のメッセージ（2 行目は `対処:` と空白 1 つの後）:

| 記号 | 場面 | 1 行目 | 2 行目 | 終了コード |
|---|---|---|---|---|
| IM1 | グリッドに陸地の画素が無い（`vmax` が 0 以下） | `解析範囲標高グリッドに陸地の画素が無い: {analysis_id}（解析対象メッシュ: {meshes}）` | `{meshes} の窓のタイルの中身が、すべて海面か NODATA になっていないかを確かめてから、{rerun}` | 1 |
| IW1 | 標高地形図を書けない | `標高地形図を書けない: {path}: {reason}` | `{dir} の空きと権限を確かめてから、{rerun}` | 1 |

- `{meshes}` は `range.meshes` を昇順に `、` でつないだもの（[6.3.4](#634-メッセージ文面) と同じ）。`{dir}` は `images_dir`。`{reason}` は控えた `errno` の `std::strerror`。`write_terrain_png` の手順 2 の変換の失敗では `PNG のバイト列に変換できない`。`{rerun}` は [6.9.4](#694-メッセージ文面) の `{rerun}` と同じ（`analysis_id` の先頭の 1 字で通常と広域を分ける）。
- IM1 は `render_terrain` が、IW1 は `write_terrain_png` が出す（呼ぶ側の 6.11 は出さない）。

#### 6.5.5 UT 候補

すべて自動。GoogleTest のケースごとに `// trace: UT-analyze_terrain_image-NN` を付ける。共通の準備は 2 つで、[6.9.5](#695-ut-候補) の「同じプロセス」と「子のプロセス（書けない）」と同じ（`csv_dir` を `images_dir` に読み替える）。`range` は、`meshes = {5339}`、`z14 = false`、`box.y_min = 12900`（ほかの欄は 0）を基本とし、ケースが替える欄だけを書く。`analysis_id` は書かなければ `3-5339`。グリッドは行ごとに北から、`values[py * W + px]` の並びで書く。

**色の比べ方**: 期待の画素は `RRGGBB` の 16 進で書く。`FFFFFF` の画素は 3 チャンネルとも一致、ほかの画素は各チャンネルの差が 1 以下（`EXPECT_LE(std::abs(actual - expected), 1)`）にする。期待値は 2026-10-28 に、matplotlib 3.11.2・numpy 2.5.4 で、6.5.3 の前置きの呼び出し（`E` は手順 4 の値を倍精度の配列にしたもの、`vmin`・`vmax`・`dx`・`dy` は手順 5・6 の式を Python の float で計算したもの）の結果の赤・緑・青に、`E` が 0 の画素を 1.0 にしてから `(x * 255).astype(np.uint8)` を当てて求めた（[テスト方針書 3.3](02_test_policy.md#33-期待値の根拠)の箇条による。表の値は、同じ版の matplotlib の結果と許容差つきで比べる形で、[DEC65](30_HLD.md#4154-設計判断)「色と陰影は `LightSource.shade()` と同じ」の「参照実装の結果と許容差つきで比べるテスト」を満たす）。採用のサンプルは `imshow` と `savefig` を通っているので、画素の比べ先にしない。出来上がりの絵は、グラデーションに違和感が無く細部が見えるかを持ち主が目で見る（実装フェーズの段で行う）。

| ID | 確かめること | 準備 | 入力 | 期待 |
|---|---|---|---|---|
| `UT-analyze_terrain_image-01` | 色と陰影、白（海面・NODATA・外周） | なし | W=6、H=5。行 0・4 は全部 0。行 1 `0 120 340 560 300 0`、行 2 `0 80 900 1200 450 0`、行 3 `0 0 650 -9999 200 0` | 幅 6・高さ 5。行 0・4 は全部 `FFFFFF`。行 1 `FFFFFF 0E2F1F 023902 1C5800 093D0A FFFFFF`、行 2 `FFFFFF 143831 A0661F FCF9F9 2B6D1F FFFFFF`、行 3 `FFFFFF FFFFFF 8D9C41 FFFFFF 2A6D46 FFFFFF`（`vmax` 1200、`vmin` −400、φ 35.71078556612323、`dx`=`dy`=3.87905337290483） |
| `UT-analyze_terrain_image-02` | Z15 と Z14 の画素の間隔の違い | なし | W=6、H=5、全部陸地。行 0 `100 100 101 101 102 102`、行 1 `100 101 102 103 103 102`、行 2 `101 102 104 105 104 103`、行 3 `101 102 103 104 103 102`、行 4 `100 101 102 102 101 101`。(a) `z14 = false`、(b) `z14 = true`（`box.y_min` は同じ 12900） | (a) 行 0 `FFFFFF EBCECD EFD8D6 EBCECC F2E1E0 FFFFFF`、行 1 `EDD4D2 EED6D4 F0DCDB F4E5E4 F6EAEA F4E4E3`、行 2 `F1DCDB F3E1E0 FAF4F3 FDFBFB FBF7F6 F8F0EF`、行 3 `F4E5E4 F7EBEA F9F1F0 FBF8F8 F8F0EF F6EAEA`、行 4 `F1DEDD F4E4E3 F8EEEE F6E9E8 F3E2E1 F7ECEC`（`dx` 3.87905337290483）。(b) 行 0 `FFFFFF EFD8D6 F2DFDE EBCECC F5E7E6 FFFFFF`、行 1 `F1DEDC F0DBDA F1DDDC F4E5E4 F8EEEE F6EAEA`、行 2 `F4E4E3 F4E5E4 FAF5F5 FDFCFC FCF9F9 FAF4F4`、行 3 `F8EDED F9F1F1 FAF4F4 FCFAF9 F9F2F2 F8F0EF`、行 4 `F5E6E6 F7EBEA FBF5F5 F7ECEB F5E6E5 FBF5F5`（φ 35.710733296912096、`dx` 7.758111833517059。(a) と (b) の差は最大 10）。(a)・(b) の `FFFFFF` は陸地の画素で、白く塗ったのではなく、明るさが 1 で色が 0.5 を超えるため |
| `UT-analyze_terrain_image-03` | 平らな絵（引き伸ばさない） | なし | W=4、H=3、全部 100 | 全画素 `FEFEFE`（明るさは sin(77.7°)、色は 255 行目） |
| `UT-analyze_terrain_image-04` | 縮小の画素の選び方（DEC68） | なし | W=8000、H=4。行 0 と行 3 は、列 c を 4 で割った余りが 3 なら 500、ほかは 0。行 1・2 は全部 0 | 幅 6000・高さ 3。出力の画素 (i, j) は、`p = ((2i+1) × 8000) / 12000` を 4 で割った余りが 3（i を 3 で割った余りが 2 の列）で、かつ j が 0 か 2（採るグリッドの行が 0 と 3）のときだけ白でなく、ほかは `FFFFFF`。白でない画素は 4000 個（全画素で確かめる）。左上を採る式（⌊i × 8000 / 6000⌋ は 4 で割った余りが 0・1・2 だけ、⌊j × 4 / 3⌋ は行 0・1・2）なら白でない画素は 0 個になり、列だけ、行だけを誤っても数と位置が変わる |
| `UT-analyze_terrain_image-05` | 縮小した絵の色（`dx`・`dy` に縮小率を掛ける、`vmax` を縮小の前のグリッドから求める） | なし | (a) W=6600、H=4。行 0・3 は全部 0。行 1・2 は、列 0 と 6599 が 0、ほかは `100 + (c % 50) × 7 + r × 3`（r は行の番号）。(b) W=4、H=6600。列 0・3 は全部 0。列 1・2 は、行 0 と 6599 が 0、ほかは `100 + (r % 50) × 7 + c × 3`（c は列の番号）。(c) (a) と同じで、グリッドの画素 (5, 1)（列 5、行 1。縮小で採られない）だけを 2000 にする | (a) 幅 6000・高さ 4。(i, j) が (0, 1) `FFFFFF`、(1, 1) `073808`、(2, 2) `317C36`、(2999, 1) `F8F1F1`、(3000, 2) `1F5D27`、(5998, 1) `F2E1E0`、(5999, 2) `FFFFFF`、(0, 0) `FFFFFF`（`dx` 4.266957777448575、`dy` 3.8790525249532504）。(b) 幅 4・高さ 6000。(1, 0) `FFFFFF`、(1, 1) `073909`、(2, 2) `165318`、(1, 2999) `FAF5F4`、(2, 3000) `2D7539`、(1, 5998) `F5E9E8`、(2, 5999) `FFFFFF`、(0, 1) `FFFFFF`（φ 35.59579766549123、`dx` 3.8846418265923717、`dy` 4.2731060092516095。行の採り方〈⌊(j + 0.5) × H / H'⌋〉と `dy` の縮小率、φ の H / 2 を確かめる）。(c) 幅 6000・高さ 4。(0, 1) `FFFFFF`、(1, 1) `05100D`、(2, 2) `235F5A`、(2999, 1) `042E05`、(3000, 2) `173F3B`、(5998, 1) `053107`、(5999, 2) `FFFFFF`、(0, 0) `FFFFFF`（`vmax` 2000、`dx`・`dy` は (a) と同じ。列 5 は 6600 → 6000 の縮小で採られない〈採る列は 4 と 6〉ので、`E` は (a) と同じで、色だけが (a) と変わる。`vmax` を縮小した画像の最大 449 から求める実装は (a) と同じ色を返して落ちる） |
| `UT-analyze_terrain_image-06` | 出力の大きさ | なし | 全部 1 のグリッドで、(a) 6000×3、(b) 6001×3、(c) 3×6001、(d) 8000×10、(e) 8000×6、(f) 12000×3 | 幅×高さが (a) 6000×3、(b) 6000×3、(c) 3×6000、(d) 6000×8（7.5 の切り上げ）、(e) 6000×5（4.5 の切り上げ）、(f) 6000×2 |
| `UT-analyze_terrain_image-07` | 陸地が無い | 同じプロセス | (a) W=3、H=3、全部 0。(b) 同じで、中央が -9999。(c) (a) を `analysis_id = "4-5135-NW"`、`meshes = {5135, 5136, 5235, 5236}` で | `code` 1。標準エラー出力が IM1 の 2 行の全文（(a)(b) は `{rerun}` が通常、(c) は広域で `--n 4`、`{meshes}` は `5135、5136、5235、5236`） |
| `UT-analyze_terrain_image-08` | 呼ぶ側の誤り（`render_terrain`） | 同じプロセス | (a) `values` が W × H より 1 少ない、(b) W = 0、(c) `analysis_id` が `3-533`、(d) `meshes` が空、(e) 12001×3（H' が 1） | どれも `std::invalid_argument`。標準エラー出力に何も出ない |
| `UT-analyze_terrain_image-09` | グリッドを書き換えない | なし | UT-analyze_terrain_image-01 の入力 | 戻った後の `values` が呼ぶ前と同じ（-9999 も 0 も残る） |
| `UT-analyze_terrain_image-10` | PNG を書く | 同じプロセス | `image` は 3×2、画素 (0,0) `FF0000`、(1,0) `00FF00`、(2,0) `0000FF`、(0,1) `010203`、(1,1) `FFFFFF`、(2,1) `000000` | `<images_dir>/3-5339_terrain.png` を `cv::imread(path, cv::IMREAD_UNCHANGED)` で読むと 3 チャンネルの 3×2 で、各画素の青・緑・赤が入力の赤・緑・青と逆の順で一致。`.tmp` が無い。標準エラー出力に何も出ない |
| `UT-analyze_terrain_image-11` | 置き換える | 同じプロセス。`3-5339_terrain.png` に `old`、`3-5339_terrain.png.tmp` に 100 バイトの `x` を置く | UT-analyze_terrain_image-10 の画像 | UT-analyze_terrain_image-10 と同じ中身になる。`.tmp` が無い |
| `UT-analyze_terrain_image-12` | 置き場が無い、案内の分け方、開けないときの一時ファイルの後始末 | 同じプロセス。(a)(b) の `images_dir` は存在しないパス。(c) の `images_dir` は存在するディレクトリで、中に `3-5339_terrain.png.tmp` という名前の、存在しない場所（`<images_dir>/no_such/x`）を指すシンボリックリンクを置く（権限に依らず、一時ファイルを開くのが `ENOENT` で失敗する） | (a) `analysis_id` が `3-5339`、(b) `5-5135-SE`、(c) `3-5339` | `code` 1 の IW1（`{reason}` は `No such file or directory`）。(a) は通常、(b) は広域の `--n 5` の `{rerun}`。(c) は `{path}` が `<images_dir>/3-5339_terrain.png` で、シンボリックリンク `3-5339_terrain.png.tmp` が消えている（`std::filesystem::symlink_status` が `not_found`。開くのに失敗したときも 2.3 のとおり一時ファイルを `unlink` する）。`3-5339_terrain.png` は無い |
| `UT-analyze_terrain_image-13` | 置き換えに失敗する | 同じプロセス。`3-5339_terrain.png` という名前の空のディレクトリ | UT-analyze_terrain_image-10 の画像 | `code` 1 の IW1（`Is a directory`）。`.tmp` が無い。ディレクトリは残る |
| `UT-analyze_terrain_image-14` | 書く途中で失敗する | 子のプロセス（書けない）。親が `3-5339_terrain.png` に `old` を置く。上限は (a) 0、(b) 5（UT-analyze_terrain_image-10 の画像を書く。その PNG は 5 バイトより長いので、5 バイトだけ書けて残りで失敗する） | 子で UT-analyze_terrain_image-10 の画像を書く | (a)(b) とも、子の終了コード 1。標準エラー出力が IW1（`File too large`）。`3-5339_terrain.png` は `old` のまま、`.tmp` が無い |
| `UT-analyze_terrain_image-15` | 呼ぶ側の誤り（`write_terrain_png`） | 同じプロセス | (a) `images_dir` が空、(b) 末尾が `/`、(c) `analysis_id` が `3-5339-NW`、(d) `rgb` が 1 バイト少ない、(e) 幅 0 | どれも `std::invalid_argument`。ファイルを作らない |

### 6.6 `analyze_terrain_scan`

- **ID**: LLD-analyze_terrain_scan
- **対応 HLD**: [3.4](30_HLD.md#34-cmp4-地形解析エンジン)・[4.5](30_HLD.md#45-fr-005-ピーク候補検出)・[4.6](30_HLD.md#46-fr-006-コル検出プロミネンス計算)・[5.1](30_HLD.md#51-nfr-001-精度検出網羅性)・[5.2](30_HLD.md#52-nfr-002-メモリ使用量)・[5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)
- **ファイル**: `src/scan.hpp`・`src/scan.cpp`

関数の名前と役割は [HLD 3.4.3](30_HLD.md#343-関数) の表の「走査」の群で、処理の正本は [HLD 4.5.2](30_HLD.md#452-処理の流れ) の「走査の準備」「1 画素の処理」「連結成分のデータ」「ピーク候補リスト」と、[4.6.2](30_HLD.md#462-処理の流れ) の「成分ごとに足すもの」「合流のとき」「走査の後（海面確定規則）」「コルの座標」「`col_margin_px`」「ピーク候補・コル情報リスト」である。止まる場面は [4.5.3](30_HLD.md#453-異常系)・[4.6.3](30_HLD.md#463-異常系) である。コルの座標の式は [2.4](#24-言語ごとに別に実装する式のテストベクトル) の `tile_to_latlon`・`z15_pixel_center_latlon`（[6.10](#610-analyze_terrain_convert) の関数を呼ぶ）。関数を呼ぶ順は 6.11 の `run_normal_mode`・`run_wide_mode`（[HLD 3.4.3](30_HLD.md#343-関数) の呼ぶ順）で決まっていて、通常モードと広域モードで同じ関数を呼ぶ（違うのは `build_col_list` のコルの座標だけ）。非機能要件は 3 つで、[5.1](30_HLD.md#51-nfr-001-精度検出網羅性)（精度・検出網羅性）は、`key_col_resolved` と海面確定規則を HLD 4.6.2 のとおりに決める（一次フィルタと最終フィルタが `key_col_resolved=false` の行を残すか落とすかの元になる）ことで受け、[5.2](30_HLD.md#52-nfr-002-メモリ使用量)（メモリ使用量）は [6.6.2](#662-型とデータ) のメモリの箇条（画素ごとの成分の番号を関数の中で捨てる、成分ごとのデータを 32 バイトにする）で受ける（実測は [HLD 5.2.2](30_HLD.md#522-処理の流れ) の実測の計画の 1）。[5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)（再現性）は、走査の順をキーの降順と番号の昇順にし（DEC58「走査の順は標高を 0.01m 単位の整数にして数え上げで作る」）、成分の番号を作った順にし、行を成分の番号の順に並べる（並べ替えない）ことで受ける。この節は、それを C++ で書くための細部を足す。1.2 の C++ の規約に従う。

#### 6.6.1 ファイル割付

- 公開の宣言は `src/scan.hpp`、定義と内部の関数は `src/scan.cpp` に置く。どちらも先頭のコメントに `// trace: LLD-analyze_terrain_scan` を書き、ヘッダーは次の行を `#pragma once` にする。
- `src/scan.hpp` は `<cstdint>`・`<vector>`・`"grid.hpp"`（`ElevationGrid`・`GridRange`・`GridXY`）を読む。`src/scan.cpp` は `"scan.hpp"`・`"common.hpp"`（`check_signal`）・`"convert.hpp"`（`LatLon`・`Z15Pixel`・`tile_to_latlon`・`z15_pixel_center_latlon`）・`<algorithm>`・`<cmath>`・`<cstdint>`・`<stdexcept>`・`<string>`・`<utility>`・`<vector>` を読む。OpenCV のヘッダーを直接読まない（`grid.hpp` が core を読む）。
- UT のコードは `tests/src/test_scan.cpp` に置き、`build/test_scan` にビルドする（[2.5](#25-ビルドとテストの名前)）。各テストに `// trace: UT-analyze_terrain_scan-NN`（確かめる UT 候補の ID）のコメントを付ける。2.4 の式で期待値を求めたテスト（UT 12・13・16）には、`2.4 の tile_to_latlon` もコメントに書く（[テスト方針書 3.3](02_test_policy.md#33-期待値の根拠)）。テストの枠組みは GoogleTest（[テスト方針書 3.4](02_test_policy.md#34-テストを先に書く進め方)）。

#### 6.6.2 型とデータ

`src/scan.hpp` の公開の宣言は次のとおり（名前空間に入れない。1.2 の C++ の規約）。

```cpp
#pragma once
#include <cstdint>
#include <vector>
#include "grid.hpp"

constexpr std::int64_t NO_COL_PIXEL = -1;

enum class KeyCol : std::uint8_t {
    Undecided,   // Key コルが決まっていない（根の成分）
    Pixel,       // グリッドの画素で決まった（合流で残さなかった成分）
    Sea,         // 海面確定規則で海面にした
};

struct Component {
    std::int64_t peak_pixel = 0;            // ピーク候補の画素の番号（py × W + px）
    std::int64_t col_pixel = NO_COL_PIXEL;  // key_col が Pixel のときの Key コルの画素の番号
    std::uint32_t parent = 0;               // Union-Find の親（根は自分の番号。根が代表の成分を兼ねる）
    float peak_elevation = 0.0f;
    float col_elevation = 0.0f;             // Pixel なら Key コルの画素の標高、Sea なら 0.0f
    KeyCol key_col = KeyCol::Undecided;
    bool border = false;                    // 人工ボーダーへの接触の印（根のものだけが今の成分の印）
    bool key_col_resolved = false;
};
static_assert(sizeof(Component) == 32);

struct PeakColRow {
    GridXY peak;                  // ピークのグリッドの画素
    float peak_elevation = 0.0f;
    double col_lat = 0.0;         // key_col_resolved が偽の行と海面確定の行は 0.0
    double col_lon = 0.0;
    float col_elevation = 0.0f;   // key_col_resolved が偽の行は未確定（0.0f を入れ、読まない）
    float prominence = 0.0f;      // 同上
    bool key_col_resolved = false;
    int col_margin_px = 0;
};

std::vector<std::int64_t> make_scan_order(const ElevationGrid& grid);
std::vector<Component> scan_peaks_and_cols(const ElevationGrid& grid,
                                           const std::vector<std::int64_t>& order);
std::vector<Component> apply_sea_level_rule(std::vector<Component> components);
std::vector<PeakColRow> build_col_list(const std::vector<Component>& components,
                                       int width, int height, const GridRange& range);
```

- 引数の並びは [HLD 3.4.3](30_HLD.md#343-関数) の表の受け取るものの順。`width`・`height` はグリッドの `width`・`height`（6.11 が渡す）。`apply_sea_level_rule` は値で受け取り、直して返す（6.11 が `std::move` で渡すので写さない）。
- 成分ごとのデータが HLD の「連結成分のデータ」と「成分ごとに足すもの」で、`std::vector<Component>` の添字が成分の番号（作った順。[HLD 4.5.2](30_HLD.md#452-処理の流れ) の「ピーク候補リスト」のとおり、ピーク候補リストを兼ねる）。代表の成分の番号は持たない（根の番号が代表。[6.6.3](#663-関数の細部) の `scan_peaks_and_cols`）。HLD の「未決」は `key_col` の `Undecided` で表し、そのときの `col_pixel` は `NO_COL_PIXEL`、`col_elevation` は `0.0f`。`key_col_resolved` は `Pixel` と `Sea` のときと、海面確定規則で偽にした `Undecided` のときに意味を持つ。`Pixel` で `key_col_resolved` が偽の成分も、合流の画素と標高を記録したままにする（[HLD 4.6.2](30_HLD.md#462-処理の流れ) の「合流のとき」の 2 のとおり記録し、3 のとおり使わない）。
- `PeakColRow` が HLD の「ピーク候補・コル情報リスト」の 1 行。`key_col_resolved` が偽の行の `col_elevation`・`prominence` は未確定（[FR-006](20_SRS.md#fr-006-コル検出プロミネンス計算) の sentinel: 空欄。空欄にして書くのは 6.7）。`std::optional` を使わず（1.2）、`key_col_resolved` で見分ける。
- 画素ごとの成分の番号は `scan_peaks_and_cols` の中の `std::vector<std::uint32_t>`（グリッドと同じ数）で持ち、返す前に捨てる（関数を出るときに解放される）。値: 内部の定数 `_not_component = 0xFFFFFFFFu`（人工ボーダー・海面・NODATA）、`_unprocessed = 0xFFFFFFFEu`（まだ処理していない陸地）、それより小さい値は成分の番号。成分の数は (W を 2 で割って切り上げた数) × (H を 2 で割って切り上げた数) 以下（HLD 4.5.2 の「連結成分のデータ」）で、最大の窓でも約 11.6 億なので `_unprocessed` に届かない。
- メモリ（[HLD 5.2](30_HLD.md#52-nfr-002-メモリ使用量)）: 走査の間に持つのは、グリッド（画素ごとに 4 バイト）、走査の順（陸地の画素ごとに 8 バイト）、画素ごとの成分の番号（4 バイト）、成分ごとのデータ（成分ごとに 32 バイト。`std::vector` の `push_back` で伸ばすので、伸ばす間は一時に最大で約 3 倍）、キーごとの画素の数（`make_scan_order` の中だけ。キーの最大値 + 1 個の `std::int64_t`、最大で 64MiB）。画素の番号を詰めるかは [#187](https://github.com/jj1xgo/findsummits/issues/187)「最大の窓で画素の番号を詰めるか」で決める（決まったら、この節の型を直す）。
- 内部（`src/scan.cpp` の無名の名前空間）: `_not_component`・`_unprocessed`、`_scan_key(float)`（キー）、`_check_grid(関数名, grid)`（グリッドを確かめて陸地の画素の数を返す）、`_find(components, x)`（経路の半減で根を返す）。

#### 6.6.3 関数の細部

処理の正本は 6.6 の前置きのとおりで、この節は C++ で書くための細部を足す。どの関数もメッセージを出さず、通常のログと警告も出さない。止まるのは、メモリを確保できないとき（`std::bad_alloc` を捕まえない。6.12 の `_on_terminate` が G7 で止める。終了コード 1。[HLD 4.5.3](30_HLD.md#453-異常系) の 1 行目）、OS に止められるとき（137。同 2 行目）、シグナル（`check_signal`）だけ。`check_signal` は、この群のどのループでも（確かめのループと初期化のループを含む）次の区切りで呼ぶ（[HLD 3.4.3](30_HLD.md#343-関数) の `check_signal` を呼ぶ群に「走査」が入っている）。グリッドを py・px の順に走るループ（`_check_grid`、`make_scan_order` の 2・4 の各走り、`scan_peaks_and_cols` の 2）は各行（py）の始め、走査の順・キー・成分を添字で走るループ（`scan_peaks_and_cols` の 1 の走査の順の確かめと 3 の処理、`make_scan_order` の 3、`apply_sea_level_rule` の 1・2、`build_col_list` の 1・2）は添字（0 から）が 2²⁰ の倍数のときの、その要素の前（`make_scan_order` の 3 はキーを `K` から 0 へ降りるので、降りた回数が 0 から数えて 2²⁰ の倍数のとき、そのキーの前）。受けてから止まるまでの遅れは、グリッドの 1 行（最大の窓で約 7 万画素）か、2²⁰ 個の要素の処理の分まで。区切りを置けないのは `std::vector` の確保（画素ごとの成分の番号は最大の窓で約 17GiB、走査の順は陸地の画素ごとに 8 バイト）と `push_back` が伸ばすときの写しの間だけで、その間は、その後の最初の区切りまで延びる。数と番号の計算は `std::int64_t` で行う（`static_cast<std::int64_t>(width) * height` など。`int` の積は最大の窓であふれる）。呼ぶ側の誤りは `std::invalid_argument` を投げる（6.4 と同じ。メッセージは `<関数名>: <内容>` の形で、内容は各関数の見出しの下。UT は例外の型だけを確かめる）。

関数ごとに `#####` の見出しを立てる。

##### _check_grid（内部）

`std::int64_t _check_grid(const char* func, const ElevationGrid& grid)`。次のどれかなら `std::invalid_argument`: `width` か `height` が 3 未満（`<func>: グリッドの幅か高さが 3 未満`）、`values.size()` が `static_cast<std::int64_t>(width) * height` と違う（`<func>: values の数が幅×高さと違う`）、外周の画素（px が 0 か W − 1、または py が 0 か H − 1）の値が `0.0f` と `==` でない（`<func>: 外周の画素が 0 でない: (<px>, <py>)`）、外周でない画素の値が `NODATA_ELEVATION` と `==` でも、`0.0f` と `==` でも、陸地（`> 0.0f` で `static_cast<double>(v) * 100.0 < 8388607.5`）でもない（NaN、負の値、無限大、キーが 8388607 を超える値。`<func>: 画素の値が NODATA でも 0 でも陸地の標高でもない: (<px>, <py>)`）。陸地の画素の数を返す。

- 陸地のキーの上限 8388607 は、デコードの最大の正の値 `8388607 / 100.0f`（[HLD 4.3.2](30_HLD.md#432-処理の流れ)）のキー。Z14 のグリッドは 2×2 の最大なので同じ範囲。外周の画素がどれも 0 で、外周に陸地が無いので、陸地の画素の 8 近傍がいつもグリッドの中になる（[HLD 4.5.2](30_HLD.md#452-処理の流れ) の「1 画素の処理」の 1）。

##### _scan_key（内部）

`std::int64_t _scan_key(float v)`。`std::llround(static_cast<double>(v) * 100.0)`（HLD 4.5.2 の「走査の準備」の 3、DEC58「走査の順は標高を 0.01m 単位の整数にして数え上げで作る」。掛け算は倍精度で、`float` のまま掛けない）。

##### make_scan_order

`std::vector<std::int64_t> make_scan_order(const ElevationGrid& grid)`

1. `_check_grid("make_scan_order", grid)` で陸地の数 `L` を得る。`L` が 0 なら空の並びを返す。
2. 1 回目の走り（py を 0〜H − 1、各 py で px を 0〜W − 1）で、陸地（`> 0.0f`）の画素のキーの最大値 `K` を求める。2 回目の走り（同じ順）で、`std::vector<std::int64_t> count(K + 1)` にキーごとの数を数える。
3. キーの大きい順に置き場所の始まりを決める（`K` から 0 へ、始まり = それまでの数の和）。
4. 3 回目の走り（同じ順）で、陸地の画素の番号 `static_cast<std::int64_t>(py) * W + px` を、そのキーの置き場所に順に置く。これで、キーの降順、同じキーは番号の昇順に並ぶ。長さは `L`。

- 海面（`0.0f`）・NODATA・人工ボーダーは並べない（HLD 4.5.2 の「走査の準備」の 1・3、DEC57「陸地でない画素は成分に入れず、近傍の成分に数えない」）。

##### scan_peaks_and_cols

`std::vector<Component> scan_peaks_and_cols(const ElevationGrid& grid, const std::vector<std::int64_t>& order)`

1. `_check_grid("scan_peaks_and_cols", grid)` で陸地の数 `L` を得る。走査の順を確かめる: どの番号も 0 以上 W × H 未満（`scan_peaks_and_cols: 走査の順の画素の番号が範囲の外: <番号>`）、その画素が陸地（`scan_peaks_and_cols: 走査の順に陸地でない画素がある: <番号>`）、`k` が 1 以上のどれでも、`k − 1` 番目のキーが `k` 番目のキーより大きいか、キーが等しく `k − 1` 番目の番号が `k` 番目の番号より小さい（どちらでもなければ `scan_peaks_and_cols: 走査の順がキーの降順と番号の昇順でない: <k>`。番号が等しいときも当たる）、長さが `L`（`scan_peaks_and_cols: 走査の順の数が陸地の画素の数と違う`）。この 4 つで、走査の順が `make_scan_order` の返すものと同じであることが決まる（重なりは 3 で、抜けは 4 で見つかる）。
2. 画素ごとの成分の番号を用意する: 陸地の画素は `_unprocessed`、ほかは `_not_component`（HLD 4.5.2 の「走査の準備」の 2）。
3. 走査の順に、画素 `p`（px = p % W、py = p / W、標高 `v`）を次のとおり処理する（HLD 4.5.2 の「1 画素の処理」の 1〜5、[4.6.2](30_HLD.md#462-処理の流れ) の「合流のとき」の 1〜4）。
   1. 8 近傍の画素のうち、成分の番号が `_unprocessed` より小さいものについて `_find` で根を求め、重なりを除いて集める（最大 8 つ。集める順は結果に効かない）。
   2. 根が 0 個: 新しい成分を `push_back` する（`peak_pixel = p`、`peak_elevation = v`、`parent` は自分の番号〈それまでの成分の数〉、ほかは既定の値）。`p` の成分の番号に入れる。
   3. 根が 1 個: その根を `p` の成分の番号に入れる。
   4. 根が 2 個以上（合流）: 根の中で `peak_elevation` がいちばん大きいもの（同じなら番号の小さいもの）を勝った根 `w` とする。`w` 以外の根 `l` のそれぞれに、`key_col = Pixel`、`col_pixel = p`、`col_elevation = v`、`key_col_resolved = !l.border`（合流の前の印。DEC61「`key_col_resolved` は合流の前の印で決める」）を入れ、`l.parent = w` にする。`w.border` を、集めた根のどれかの `border` が真なら真にする。`w` を `p` の成分の番号に入れる。
   5. `p` が外周から 2 番目の行か列（px が 1 か W − 2、または py が 1 か H − 2）なら、`p` の成分の根（2 なら新しい成分、3 ならその根、4 なら `w`）の `border` を真にする（合流の後にだけ数える）。
4. 成分ごとのデータを返す（画素ごとの成分の番号はここで捨てる）。

- `_find` は経路の半減: `while (c[x].parent != x) { c[x].parent = c[c[x].parent].parent; x = c[x].parent; }`。根を残す成分は 4 の勝った根だけなので、根の番号が代表の成分の番号に等しい（[HLD 4.6.2](30_HLD.md#462-処理の流れ) の「成分ごとに足すもの」の代表の成分の番号を、根の番号で表す）。合流で勝った成分の根を残して負けた根をその下に付けると、「根の番号 = 代表の成分の番号」がいつも成り立つ（作ったときは自分が根で代表。合流で残すのは勝った成分の根で、帰納法で勝った成分自身）ので、代表の番号を成分ごとに別に持たずに済む（成分ごとに 4 バイト、最大の窓で約 4.3GiB）。経路の縮め方は経路の半減（path halving）だけにする。再帰の圧縮は、深い木でスタックを使い切るので使わない。大きさや高さで根を選ばないのは、根を勝った成分に決めるため。
- 根を勝った成分に決めるので、DEC60「合流では最も高いピークの成分を残す」の却下の案（根の成分をそのまま残すピークにする）の前提（根の選び方がピークの高さと関係なく決まる）は起きず、根の番号が代表の成分の番号と同じになる。
- 4 で負けた根は、合流の後は根でなくなり、その `border` は使わない。3 つ以上が同時に合流しても、勝つのは 1 つで、ほかのすべてが `p` を Key コルにする（HLD 4.6.2 の「合流のとき」の 2）。

##### apply_sea_level_rule

`std::vector<Component> apply_sea_level_rule(std::vector<Component> components)`

1. 確かめる: どの成分も `parent` が成分の数より小さい（`apply_sea_level_rule: 成分の親が範囲の外: <番号>`）。`key_col` が `Undecided` の成分の集合と、`parent` が自分の番号の成分（根）の集合が等しい（片方にだけ入る成分があれば、どちらの向きでも投げる。`apply_sea_level_rule: 未決の成分と根が一致しない: <番号>`。`scan_peaks_and_cols` が返したものなら成り立つ）。
2. `key_col` が `Undecided` の成分（根）のそれぞれについて、`border` が偽なら `key_col = Sea`、`col_elevation = 0.0f`、`key_col_resolved = true`。真なら `key_col_resolved = false`（`key_col` は `Undecided` のまま）。ほかの成分は変えない（HLD 4.6.2 の「走査の後（海面確定規則）」）。
3. 直した成分ごとのデータを返す。

- 根の `border` は、まとめた成分の全体の印（合流のたびに集めた根の印をまとめるため）。

##### build_col_list

`std::vector<PeakColRow> build_col_list(const std::vector<Component>& components, int width, int height, const GridRange& range)`

1. 確かめる: `range.z14` が偽なら 1 タイルの画素の数 `s = 256`、真なら `s = 128` として、（`std::int64_t` で計算して）`width == s × (box.x_max − box.x_min + 1) + 2` かつ `height == s × (box.y_max − box.y_min + 1) + 2`（[HLD 4.4.2](30_HLD.md#442-処理の流れ) の「解析範囲標高グリッドの生成」の 2、[4.14.2](30_HLD.md#4142-処理の流れ) の「Z14 のグリッドの生成」の 1。違えば `build_col_list: 幅か高さが解析対象メッシュ範囲情報と合わない: <W>×<H>`）。各成分の `peak_pixel` が 0 以上 W × H（`static_cast<std::int64_t>(width) * height`）未満（`build_col_list: ピークの画素の番号が範囲の外: <成分の番号>`）。`key_col` が `Undecided` の成分は、どれも `key_col_resolved` が偽で `border` が真（海面確定規則の後に `Undecided` で残るのは人工ボーダーに接触した根だけなので、`apply_sea_level_rule` を呼び忘れると `border` が偽の根で見つかる。違えば `build_col_list: 海面確定規則を当てていない成分がある: <成分の番号>`）。`key_col_resolved` が真で `key_col` が `Pixel` の成分の `col_pixel` が 0 以上 W × H 未満（`build_col_list: Key コルの画素の番号が範囲の外: <成分の番号>`）。
2. 成分の番号の順に 1 行ずつ作る（並べ替えない。HLD 4.6.2 の「ピーク候補・コル情報リスト」）。`peak` は `{static_cast<int>(peak_pixel % W), static_cast<int>(peak_pixel / W)}`（1 で範囲を確かめた後なので `int` に入る。コルの画素も同じ）、`peak_elevation` は成分の値。
   - `key_col_resolved` が偽: `col_lat`・`col_lon` は `0.0`、`col_elevation`・`prominence` は `0.0f`、`col_margin_px` は 1（HLD 4.6.2 の「合流のとき」の 3、「`col_margin_px`」）。
   - 真で `Sea`: `col_lat`・`col_lon` は `0.0`、`col_elevation` は `0.0f`、`prominence` は `peak_elevation`、`col_margin_px` は −1。
   - 真で `Pixel`: コルの画素 (px, py) = `{col_pixel % W, col_pixel / W}`。`col_elevation` は成分の値、`prominence` は `peak_elevation - col_elevation`（`float` で引く）。`col_margin_px` は `std::min({px, py, W - 1 - px, H - 1 - py})`。座標は、Z15（`range.z14` が偽）なら `z15_pixel_center_latlon({256 × box.x_min + px − 1, 256 × box.y_min + py − 1})`、Z14 なら `tile_to_latlon(static_cast<double>(128 × box.x_min + px − 1) + 0.5, static_cast<double>(128 × box.y_min + py − 1) + 0.5, 22)` の `lat`・`lon`（HLD 4.6.2 の「コルの座標」、DEC62「コルの座標はグリッドの画素の中心にする」。Z14 の 1 画素は z=22 の 1 タイル）。
3. 行の並びを返す。

- 地理的範囲フィルタと一次フィルタは当てない（6.7 の `filter_peak_rows`）。`range.meshes`・`range.picks`・`box.bbox` は使わない。

#### 6.6.4 メッセージ文面

なし（この群はメッセージを出さない。止まるのは、メモリの不足とシグナルだけで、どちらも 6.12 のメッセージで止まる〈[6.6.3](#663-関数の細部) の前置き〉）。

#### 6.6.5 UT 候補

すべて自動。GoogleTest のケースごとに `// trace: UT-analyze_terrain_scan-NN`。共通の準備は 3 つ。

- **同じプロセス**: [6.2.5](#625-ut-候補) の同じ名前の準備と同じ。
- **小さいグリッド**: `ElevationGrid` の `width`・`height` をケースの W・H にし、`values` を W × H 個の `0.0f` で作ってから、ケースが挙げた画素 (px, py) の値を書く（`values[py * W + px]`）。挙げない画素は海面か人工ボーダー（0）。画素の番号は `py × W + px`。成分ごとのデータを確かめるときは、成分ごとに `peak_pixel`・`peak_elevation`・`parent`・`key_col`・`col_pixel`・`col_elevation`・`key_col_resolved` を比べ、`border` は根（`parent` が自分）だけを比べる。値は `EXPECT_EQ`（標高は表の整数の値の `float` か、ケースが書いた `float` の式に等しい）。
- **子のプロセス**: [6.12.5](#6125-ut-候補) の同じ名前の準備と同じ。

成分の書き方: `[番号] peak=<peak_pixel>/<peak_elevation> parent=<parent> <key_col>(<col_pixel>/<col_elevation>) res=<key_col_resolved> border=<border>`。`<key_col>` が `Undecided` か `Sea` なら括弧の中は `-1/0`。書かない項目は既定の値（`res=false`、`border=false`）。「…」は直前に書いた同じ番号の成分と同じ値。

| ID | 確かめること | 準備 | 入力 | 期待 |
|---|---|---|---|---|
| `UT-analyze_terrain_scan-01` | 走査の順と同じ標高 | 同じプロセス。小さいグリッド W=6・H=4: (1,1)=100、(2,1)=200、(3,1)=100、(1,2)=-9999、(2,2)=200、(3,2)=50、(4,2)=100（(4,1) は 0） | `make_scan_order` に (a) このグリッド、(b) 同じ大きさで (1,1)=-9999 だけのグリッド | (a) `{8, 14, 7, 9, 16, 15}`。(b) 空 |
| `UT-analyze_terrain_scan-02` | キーの丸め（DEC58） | 同じプロセス。小さいグリッド W=7・H=3: (1,1)=`6553609 / 100.0f`、(2,1)=`6553610 / 100.0f`、(4,1)=`100.004f`、(5,1)=`100.0f` | `make_scan_order` | `{9, 8, 11, 12}`（`float` のまま 100 倍すると (1,1) のキーが 6553610 になり、`{8, 9, 11, 12}` になる） |
| `UT-analyze_terrain_scan-03` | グリッドの呼ぶ側の誤り | 同じプロセス。UT 01 の (a) のグリッドを元にする | `make_scan_order` に (a) W=2・H=4 の 8 個の 0、(b) W=4・H=2 の 8 個の 0、(c) W=4・H=4 で値が 15 個、(d) 元の (0,1)=5、(e) 元の (1,1)=-1、(f) 元の (1,1)=NaN、(g) 元の (1,1)=`83886.08f`、(h) 元の (1,1)=+∞ | どれも `std::invalid_argument`。ほかに、元の (1,1) を `8388607 / 100.0f`・`-9999.0f`・`0.0f` にしたものは投げない |
| `UT-analyze_terrain_scan-04` | 1 つのピークと海面確定 | 同じプロセス。小さいグリッド W=7・H=7: px と py が 2〜4 の 9 画素が 100、ただし (3,3)=300 | `make_scan_order`、`scan_peaks_and_cols`、`apply_sea_level_rule` の順 | 走査の順は `{24, 16, 17, 18, 23, 25, 30, 31, 32}`。走査の後は 1 つ: `[0] peak=24/300 parent=0 Undecided(-1/0) res=false border=false`。海面確定の後は `[0] … Sea(-1/0) res=true border=false` |
| `UT-analyze_terrain_scan-05` | 2 つのピークの合流 | 同じプロセス。小さいグリッド W=9・H=5: (2,2)=300、(3,2)=200、(4,2)=150、(5,2)=250、(6,2)=100 | UT 04 と同じ順 | 走査の順は `{20, 23, 21, 22, 24}`。走査の後は `[0] peak=20/300 parent=0 Undecided(-1/0) res=false border=false`、`[1] peak=23/250 parent=0 Pixel(22/150) res=true`。海面確定の後は `[0]` が `Sea(-1/0) res=true`、`[1]` は変わらない |
| `UT-analyze_terrain_scan-06` | 平らな頂上（HLD 4.5.2 の例） | 同じプロセス。小さいグリッド W=16・H=16: (10,10)=500、(12,10)=500、(11,11)=500 | UT 04 と同じ順 | 走査の順は `{170, 172, 187}`。走査の後は `[0] peak=170/500 parent=0 Undecided(-1/0) border=false`、`[1] peak=172/500 parent=0 Pixel(187/500) res=true`（同じ標高は番号の小さい `[0]` が勝ち、プロミネンスは 0 になる）。海面確定の後は `[0]` が `Sea(-1/0) res=true` |
| `UT-analyze_terrain_scan-07` | 3 成分の同時の合流 | 同じプロセス。小さいグリッド W=11・H=11: (5,4)=300、(6,6)=300、(4,6)=200、(5,5)=50 | UT 04 と同じ順 | 走査の順は `{49, 72, 70, 60}`。走査の後は `[0] peak=49/300 parent=0 Undecided(-1/0) border=false`、`[1] peak=72/300 parent=0 Pixel(60/50) res=true`、`[2] peak=70/200 parent=0 Pixel(60/50) res=true` |
| `UT-analyze_terrain_scan-08` | 人工ボーダーへの接触（DEC61） | 同じプロセス。小さいグリッド W=9・H=7 を 3 つ: (a) (3,2)=300、(5,2)=200、(4,1)=100、(b) (3,3)=300、(5,1)=200、(4,2)=100、(c) (5,1)=300、(3,3)=200、(4,2)=100 | それぞれ UT 04 と同じ順 | (a) 走査の順 `{21, 23, 13}`。走査の後 `[0] peak=21/300 parent=0 Undecided(-1/0) border=true`、`[1] peak=23/200 parent=0 Pixel(13/100) res=true`（合流の画素自身の接触は合流の後だけ）。海面確定の後 `[0]` は `Undecided(-1/0) res=false`。(b) 走査の順 `{30, 14, 22}`。走査の後 `[0] peak=30/300 parent=0 Undecided(-1/0) border=true`、`[1] peak=14/200 parent=0 Pixel(22/100) res=false`（負けた成分が合流の前に接触）。海面確定の後 `[0]` は `res=false`。(c) 走査の順 `{14, 30, 22}`。走査の後 `[0] peak=14/300 parent=0 Undecided(-1/0) border=true`、`[1] peak=30/200 parent=0 Pixel(22/100) res=true`（勝った成分の接触は負けた成分に響かない）。海面確定の後 `[0]` は `res=false` |
| `UT-analyze_terrain_scan-09` | 海と NODATA で隔てた陸地 | 同じプロセス。小さいグリッド W=11・H=7: (2,3)=100、(3,3)=200、(5,3)=150、(6,3)=-9999、(7,3)=120、(8,3)=80（(4,3) は 0） | UT 04 と同じ順 | 走査の順は `{36, 38, 40, 35, 41}`。走査の後は 3 つで、`[0] peak=36/200 parent=0`、`[1] peak=38/150 parent=1`、`[2] peak=40/120 parent=2`、どれも `Undecided(-1/0) border=false`。海面確定の後はどれも `Sea(-1/0) res=true` |
| `UT-analyze_terrain_scan-10` | 走査の順の確かめ | 同じプロセス。UT 01 の (a) のグリッド | `scan_peaks_and_cols` に走査の順 (a) `{14, 8, 7, 9, 16, 15}`、(b) `{8, 14, 7, 9, 16}`、(c) `{8, 14, 7, 9, 16, 15, 15}`、(d) `{8, 14, 7, 9, 10, 16, 15}`、(e) `{8, 14, 7, 9, 16, 24}`、(f) `{-1, 8, 14, 7, 9, 16, 15}`、(g) `{8, 14, 7, 9, 15, 16}`。ほかに (h) UT 03 の (d) のグリッドと `{8, 14, 7, 9, 16, 15}` | どれも `std::invalid_argument`。UT 01 の (a) のグリッドと `{8, 14, 7, 9, 16, 15}` は投げない |
| `UT-analyze_terrain_scan-11` | 海面確定規則の呼ぶ側の誤り | 同じプロセス | `apply_sea_level_rule` に (a) `[0] parent=1 Undecided` だけ、(b) `[0] parent=0 Undecided` と `[1] parent=0 Undecided`、(c) `[0] parent=0 Pixel(5/10) res=true` だけ | どれも `std::invalid_argument`。空の並びは空を返す |
| `UT-analyze_terrain_scan-12` | 行（Z15） | 同じプロセス。`range` は `meshes` が `{5235}`、`z14` が偽、`box` の `x_min`・`x_max`・`y_min`・`y_max` が 28700・28701・12980・12980（W=514、H=258）。成分は 4 つ: `[0] peak=515/500 parent=0 Sea(-1/0) res=true`、`[1] peak=10290/300 parent=0 Pixel(51907/120.5) res=true`、`[2] peak=2575/250 parent=0 Pixel(131840/90) res=false`、`[3] peak=1030/200 parent=3 Undecided(-1/0) res=false border=true` | `build_col_list(成分, 514, 258, range)` | 4 行がこの順。`[0]` は `peak` (1, 1)、`peak_elevation` 500、`col_lat`・`col_lon` 0.0、`col_elevation` 0、`prominence` 500、真、−1。`[1]` は (10, 20)、300、`col_lat`・`col_lon` が `tile_to_latlon(7347706.5, 3322979.5, 23)` の `lat`・`lon` と `==`、かつ経度が `135.3293538093567` と等しく（`==`）、緯度が `34.99050558441977` との差 `1e-12` 以下、120.5、`179.5f`、真、6。`[2]` は (5, 5)、250、0.0・0.0、0、0、偽、1。`[3]` は (2, 2)、200、0.0・0.0、0、0、偽、1 |
| `UT-analyze_terrain_scan-13` | 行（Z14） | 同じプロセス。`range` は UT 12 の `z14` を真にしたもの（W=258、H=130）。成分は 2 つ: `[0] peak=1035/400 parent=0 Pixel(2644/150.25) res=true`、`[1] peak=259/300 parent=1 Sea(-1/0) res=true` | `build_col_list(成分, 258, 130, range)` | 2 行。`[0]` は (3, 4)、400、`col_lat`・`col_lon` が `tile_to_latlon(3673663.5, 1661449.5, 22)` の `lat`・`lon` と `==`、かつ経度が `135.31306743621826` と等しく（`==`）、緯度が `34.99333577626061` との差 `1e-12` 以下、150.25、`249.75f`、真、10。`[1]` は (1, 1)、300、0.0・0.0、0、300、真、−1 |
| `UT-analyze_terrain_scan-14` | 行の呼ぶ側の誤り | 同じプロセス。UT 12 の `range` と成分 | `build_col_list` に (a) 幅 513、(b) 高さ 257、(c) `range.z14` を真にして幅 514・高さ 258、(d) `[0]` の `peak` を 132612（W × H）に、(e) `[1]` の `col_pixel` を −1 に、(f) `[3]` の `key_col_resolved` を真に、(g) `[3]` の `border` を偽に（海面確定規則を呼び忘れた形） | どれも `std::invalid_argument` |
| `UT-analyze_terrain_scan-15` | シグナルで止まる | 子のプロセス。UT 01 の (a) のグリッドと走査の順、UT 12 の `range` と成分 | 子の中で `start_log` の後に `kill(getpid(), SIGTERM)` してから、(a) `make_scan_order`、(b) `scan_peaks_and_cols`（走査の順は `kill` の前に求めておく）、(c) `apply_sea_level_rule` に `[0] peak=0/100 parent=0 Undecided(-1/0)` だけ、(d) `build_col_list(UT 12 の成分, 514, 258, range)`（ケースごとに別の子） | どれも `ExitRequest` の `code` が 143、子の終了コードが 143 |
| `UT-analyze_terrain_scan-16` | 画素の番号を 64 ビットで計算すること（最大の窓） | 同じプロセス。`range` は UT 12 の `meshes` と `z14`（偽）で、`box` の `x_min`・`x_max`・`y_min`・`y_max` が 28700・28956・12980・13236（257 タイル。W=H=65794、W × H=4328850436 で 32 ビットに収まらない）。グリッドは作らない（`build_col_list` は成分だけを受け取る）。成分は 1 つ: `[0] peak=4311875586/300 parent=0 Pixel(4311941381/120.5) res=true` | `build_col_list` に (a) `(成分, 65794, 65794, range)`、(b) `[0]` の `peak` を 4328850436（W × H）にしたもの | (a) 1 行。`peak` は (2, 65536)、`peak_elevation` 300、`col_lat`・`col_lon` が `tile_to_latlon(7347202.5, 3388416.5, 23)` の `lat`・`lon` と `==`、かつ経度が `135.3077244758606` との差、緯度が `32.657857671573154` との差がどちらも `1e-12` 以下、`col_elevation` 120.5、`prominence` が `179.5f`、真、`col_margin_px` 3（コルの画素は (3, 65537)）。(b) `std::invalid_argument` |

### 6.7 `analyze_terrain_csv`

- **ID**: LLD-analyze_terrain_csv
- **対応 HLD**: [3.4](30_HLD.md#34-cmp4-地形解析エンジン)・[4.7](30_HLD.md#47-fr-007-per-mesh-csv-出力プロミネンス閾値適用)・[4.14](30_HLD.md#414-fr-014-広域結合解析オーケストレーション)・[4.16](30_HLD.md#416-fr-016-ピーク域ポリゴン生成)・[5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)
- **ファイル**: `src/csv.hpp`・`src/csv.cpp`

関数の名前と役割は [HLD 3.4.3](30_HLD.md#343-関数) の表の「CSV と早期終了」の群である。処理の正本は、フィルタが [HLD 4.7.2](30_HLD.md#472-処理の流れ) の 1〜5、per-mesh CSV の書き方が同じ節の「残った行を、入力のリストの順に…」から始まる段落、読み戻しが同じ節の「早期終了への受け渡し」と [4.14.2](30_HLD.md#4142-処理の流れ) の 4「対象メッシュごとに、昇順に次を行う」の 2 の 10 で、列と精度は [FR-007](20_SRS.md#fr-007-per-mesh-csv-出力プロミネンス閾値適用) の出力カラムである。止まる場面は [4.7.3](30_HLD.md#473-異常系) と [4.14.3](30_HLD.md#4143-異常系) の「書き込みに失敗する」「早期終了の判定で、書き終えた per-mesh CSV を読み戻せないか、書式が違う」の行、書き込みの失敗は [HLD 2.5.5](30_HLD.md#255-書き込みの失敗) である。[HLD 4.16](30_HLD.md#416-fr-016-ピーク域ポリゴン生成)（ピーク域ポリゴン）は、`format_coord` を 6.8 の群が頂点の緯度経度に使うことで受ける（[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の頂点の段落）。[HLD 5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)（再現性）は、フィルタの後の行を入力の順のまま書くことと、数の書き方（`std::to_chars` が値を正しく丸める。ロケールに依存しない）で受ける。[HLD 4.7.1](30_HLD.md#471-目的と範囲) の対象外の行が LLD に送った、書き込みの途中で失敗したときに書きかけのファイルを残さない書き方は、[2.3](#23-ファイルの名前と書き方) の一時ファイルの決まりで受ける。4 つの関数は `check_signal` を呼ばない（[HLD 3.4.3](30_HLD.md#343-関数) の表の後の段落が挙げる群に「CSV と早期終了」は入っていない。行を順に処理して文字列を作るか読むだけで、時間がかからない。6.9 と同じ）。関数を呼ぶ順は 6.11 の `run_normal_mode`・`run_wide_mode` で決まる（通常は `filter_peak_rows` → `write_peak_csv`、広域はその後に 6.9 の `write_meshset` → `read_back_peak_csv`。[HLD 3.4.3](30_HLD.md#343-関数) の呼ぶ順）。通常モードの出力は、`filter_peak_rows` が返した行を [HLD 4.4.2](30_HLD.md#442-処理の流れ) の 4「対象メッシュごとに、昇順に次を行う」の 8 が 6.8 の群へ渡す。この節は、それを C++ で書くための細部を足す。1.2 の C++ の規約に従う。

#### 6.7.1 ファイル割付

- 公開の宣言は `src/csv.hpp`、定義と内部の関数は `src/csv.cpp` に置く。どちらも先頭のコメントに `// trace: LLD-analyze_terrain_csv` を書き、ヘッダーは次の行を `#pragma once` にする。
- `src/csv.hpp` は `"convert.hpp"`（`Z15Pixel`）・`"grid.hpp"`（`GridRange`）・`"scan.hpp"`（`PeakColRow`）・`"target.hpp"`（`TargetPeak`）・`<set>`・`<string>`・`<vector>` を読む。`src/csv.cpp` は `"csv.hpp"`・`"common.hpp"`・`"convert.hpp"`・`<cerrno>`・`<charconv>`・`<cmath>`・`<cstdint>`・`<cstdio>`・`<cstring>`・`<fcntl.h>`・`<stdexcept>`・`<string>`・`<system_error>`・`<unistd.h>` を読む。OpenCV のヘッダーは直接読まない（`grid.hpp` が core を読む）。
- UT のコードは `tests/src/test_csv.cpp` に置き、`build/test_csv` にビルドする（[2.5](#25-ビルドとテストの名前)。`src/` の `main` を持たない `.cpp` をすべてリンクするので、`common.cpp`・`convert.cpp` も入る）。各テストに `// trace: UT-analyze_terrain_csv-NN`（確かめる UT 候補の ID）のコメントを付ける。2.4 の表の行を写したテスト（UT-analyze_terrain_csv-01）には、写した表の名前（`2.4 の表 7` など）もコメントに書く（[テスト方針書 3.3](02_test_policy.md#33-期待値の根拠)）。テストの枠組みは GoogleTest（[テスト方針書 3.4](02_test_policy.md#34-テストを先に書く進め方)）。

#### 6.7.2 型とデータ

`src/csv.hpp` の公開の宣言は次のとおり（名前空間に入れない。1.2 の C++ の規約）。

```cpp
#pragma once
#include <set>
#include <string>
#include <vector>
#include "convert.hpp"
#include "grid.hpp"
#include "scan.hpp"
#include "target.hpp"

struct PeakCsvRow {
    PeakColRow row;          // build_col_list の行（peak はグリッドの画素のまま）
    std::string lat_text;    // peak_lat（format_coord の文字列）
    std::string lon_text;    // peak_lon（同じ）
};

std::vector<PeakCsvRow> filter_peak_rows(const std::vector<PeakColRow>& rows,
                                         const GridRange& range,
                                         const std::string& analysis_id,
                                         long long prominence_primary_m,
                                         const std::vector<TargetPeak>& peaks);
std::string format_coord(double value);
void write_peak_csv(const std::vector<PeakCsvRow>& rows, const std::string& analysis_id,
                    const std::string& csv_dir);
std::set<Z15Pixel> read_back_peak_csv(const std::string& path,
                                      const std::vector<TargetPeak>& peaks, int n);
```

- 引数の並びは [HLD 3.4.3](30_HLD.md#343-関数) の表の受け取るものの順。`rows` は 6.6 の `build_col_list` の戻り値、`range` は 6.4 の `GridRange`、`analysis_id` は解析識別子。`prominence_primary_m` は 6.12 の `ConfigValue::integer`（`long long`）をそのまま受ける（通常モードだけが読む。広域モードでは読まないので、6.11 は設定の値をそのまま渡してよい）。`peaks` は 6.2 の `PeakGroups` のその対象メッシュの組で、通常モードでは空の並びを渡す。`csv_dir` は `data_dir` の下の `results/csv` の絶対パスで、末尾に `/` を付けない（6.3・6.9 と同じ。6.11 が組み立てて渡す）。`path` は 6.11 が `csv_dir + "/" + analysis_id + ".csv"` で組み立てて渡す。`n` は `--n` の値。
- `PeakCsvRow` が HLD の「フィルタの後のリスト」の 1 行（各行はグリッドの画素の位置と、ピークの座標の文字列を持つ）。6.8 の群の `fill_zone`・`write_zone_geojson` がこの型を受ける。join キーは `lat_text`・`lon_text`（[HLD 4.7.2](30_HLD.md#472-処理の流れ) の「書いた行と同じ集合を、フィルタの後のリストとして返す」の段落、[4.16.2](30_HLD.md#4162-処理の流れ)）。
- `read_back_peak_csv` の返すものは、`key_col_resolved` が `true` の行に一致した対象ピークの Z15 の画素の集合（HLD の「確定して出た対象ピークの集合」）。照合は画素で行うので、画素の集合で表す（同じ画素の対象ピークは一緒に確定する）。6.11 は、パターンをまたいでこの集合を和で積み上げ、組のすべての対象ピークの `pixel` が入れば、残りのパターンを行わない（[HLD 4.14.2](30_HLD.md#4142-処理の流れ) の 4「対象メッシュごとに、昇順に次を行う」の 2 の 10）。
- 内部（`src/csv.cpp` の無名の名前空間）:
  - `_header`: 見出しの行の文字列 `peak_lat,peak_lon,peak_elev,col_lat,col_lon,col_elev,prominence,key_col_resolved,col_margin_px,analysis_id`（[FR-007](20_SRS.md#fr-007-per-mesh-csv-出力プロミネンス閾値適用) の出力カラムの順）。
  - `_format_fixed(double value, int digits)`: 6.7.3 の「数の書き方」。
  - `_parse_decimal(const std::string& s, double& out)`: [6.2.3](#623-関数の細部) の `read_unresolved_peaks` の 7「数として読める」と同じ判定と値（読めれば `true`）。
  - `_check_analysis_id(関数名, analysis_id)`: [6.9.3](#693-関数の細部) の `write_meshset` の 1 の 2 つ目の判定と同じ。頭の関数名だけを替えた文で `std::invalid_argument` を投げる。
  - `bool _write_all(int fd, const std::string& s)`: [6.9.2](#692-型とデータ) と同じ形。
  - `_read_file(path, data, err)`: [6.2.3](#623-関数の細部) と同じ形。
  - 6.12・6.2・6.9 の内部の関数は、ほかの `.cpp` から呼べないので、同じ形をここに置く。
  - 上の一覧のほかに、2 つ以上の関数で同じ判定や文を使う補助の関数（`{rerun}`・`{redo}` の組み立て、CW1・RB1・RB2 を出して止まる手順、行を `,` で分ける手順など）は、足してよい（名前と形は書く人が決め、公開の宣言には出さない。名前は `_` と英小文字で始める）。

#### 6.7.3 関数の細部

処理の正本は 6.7 の前置きのとおりで、この節は C++ で書くための細部を足す。止まるときは、メッセージを `log_error` で出してから `throw ExitRequest(EXIT_ERROR)` する（1.2 の C++ の規約）。呼ぶ側の誤りは `std::invalid_argument` を投げる（6.2・6.9・6.10 と同じ。`main` は捕まえないので、6.12 の `_on_terminate` が G7 で止める）。文は `<関数名>:` と空白 1 つの後に内容を続ける形で、内容は書く人が決めてよい（UT は例外の型だけを確かめる）。通常のログと警告は出さない（段の始まりと早期終了のログは 6.11 が出す）。

数を文字列にするのは `std::to_chars`、文字列を数にするのは `std::from_chars` だけを使う（`printf`・`std::ostream`・`std::stod` は、ロケールで小数点が変わりうるので使わない）。ただし整数の `col_margin_px` だけは `std::to_string` で書く（小数点が無く、ロケールで変わらない。下の `write_peak_csv` の 2）。

**数の書き方（`_format_fixed`）**: `char buf[64]` に `std::to_chars(buf, buf + 64, value, std::chars_format::fixed, digits)` で書く。呼ぶ値は有限で、`float` の値か ±180 の内なので、64 バイトに収まり、結果の `ec` は `std::errc{}` になる（`ec` を確かめる分岐は置かない）。結果の文字列の先頭が `-` で、残りのバイトが `0` と `.` だけ（`-0.00`・`-0.00000000`）なら、先頭の `-` を除く。`std::to_chars` は値を正しく丸める（ちょうど半分の値は偶数に丸める。C ロケールの `printf` と同じ）ので、同じ値は CPython の `f'{x:.8f}'`・`f'{x:.2f}'` と同じ文字列になる。2 桁の列（`peak_elev`・`col_elev`・`prominence`）は、`float` の値を `double` にしてから渡す。

関数ごとに `#####` の見出しを立てる。

##### filter_peak_rows

`std::vector<PeakCsvRow> filter_peak_rows(const std::vector<PeakColRow>& rows, const GridRange& range, const std::string& analysis_id, long long prominence_primary_m, const std::vector<TargetPeak>& peaks)`

1. 呼ぶ側の誤り（行に触れる前に、この順で確かめ、最初に当たったもので投げる）: `analysis_id` が解析識別子の形でない（`_check_analysis_id`）。通常（先頭が `3`）で `range.z14` が真か `peaks` が空でない。広域（先頭が `4`・`5`・`6`）で `range.z14` が偽か `peaks` が空。`range.meshes` が空。
2. 広域だけ、`targets` を、`peaks` の各 `pixel` の `std::set<Z15Pixel>` にする（対象ピークの画素は 6.2 の `group_peaks_by_mesh` が組ごとに 1 回求めた値で、`latlon_to_z15_pixel` を呼び直さない。[HLD 4.7.2](30_HLD.md#472-処理の流れ) の 5「対象ピークの照合」の「組ごとに 1 回求め」）。
3. `rows` を順に、各行に次を当てる。落とした行は、その後の判定を行わない（[HLD 4.7.2](30_HLD.md#472-処理の流れ) の 1〜5 の順）。
   1. 一次フィルタ（通常だけ）: `key_col_resolved` が真で、`static_cast<double>(prominence) < static_cast<double>(prominence_primary_m)` なら落とす（[HLD 4.7.2](30_HLD.md#472-処理の流れ) の 1 の字句どおり、6.6 が求めた値で比べる。CSV に書く 2 桁の値では比べない。たとえば `prominence` が `129.996f` の行は、CSV では `130.00` と書く値だが、130 未満なので閾値 130 で落ちる）。`prominence` が NaN の行は、比べた結果が偽になって残り、`write_peak_csv` の 1 が止める（6.6 の行は有限なので起きない）。
   2. Z15 の画素: 通常は `Z15Pixel{256 * range.box.x_min + peak.px - 1, 256 * range.box.y_min + peak.py - 1}`（[HLD 4.7.2](30_HLD.md#472-処理の流れ) の 2「ピークの Z15 の画素を求める」。`peak` は行の `GridXY`）。広域は `range.picks` を `peak` で引き、無ければ落とす（控えの無い 2×2 で検出された行は、どの対象ピークとも一致しない。[DEC50](30_HLD.md#4144-設計判断)「縮約で採った画素の座標は対象ピークを含む 2×2 だけ控える」）。
   3. 座標: `c = z15_pixel_center_latlon(pixel)`、`lat_text = format_coord(c.lat)`、`lon_text = format_coord(c.lon)`。`lat`・`lon` は、その文字列を `_parse_decimal` で読み戻した値（[HLD 4.7.2](30_HLD.md#472-処理の流れ) の 3「ピークの緯度経度を求める」の「この文字列を数として読み戻した値」。`format_coord` の文字列はいつも読める）。
   4. 地理的範囲フィルタ: `latlon_to_mesh(lat, lon)` が `range.meshes` に無ければ落とす（空の文字列も、無いコードとして落ちる。6.10.3。[DEC55](30_HLD.md#474-設計判断)「地理的範囲フィルタは CSV に書く値で判定する」）。範囲は `range.box.bbox` でなく `range.meshes`（解析対象メッシュの矩形を合わせたもの）。
   5. 対象ピークの照合（広域だけ）: `pixel` が `targets` に無ければ落とす。
   6. 残った行を `{row, lat_text, lon_text}` にして、末尾に足す（入力の順のまま。並べ替えない。[HLD 5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)）。
4. 返す。0 件でも返す（見出しだけの CSV を書くのは `write_peak_csv`）。

##### format_coord

`std::string format_coord(double value)`。`value` が有限でないか、−180 より小さいか 180 より大きければ `std::invalid_argument`。そうでなければ `_format_fixed(value, 8)` を返す（小数点 8 桁。[HLD 4.7.2](30_HLD.md#472-処理の流れ) の 3）。使う側は、`filter_peak_rows`・`write_peak_csv`（`col_lat`・`col_lon`）と、6.8 の群の頂点（[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の頂点の段落）。

##### write_peak_csv

`void write_peak_csv(const std::vector<PeakCsvRow>& rows, const std::string& analysis_id, const std::string& csv_dir)`

1. 呼ぶ側の誤り（ファイルに触れる前に、次の順で確かめ、最初に当たったもので投げる。行の検査は `rows` の順に 1 行ずつ、行の中は書いた順）: `csv_dir` が空か最後のバイトが `/`、`analysis_id` の形（`_check_analysis_id`）、行の `lat_text`・`lon_text` のどちらかが `_parse_decimal` で読めない（空を含む）、行の `peak_elevation`・`col_lat`・`col_lon` と、`key_col_resolved` が真の行の `col_elevation`・`prominence` のどれかが有限でない（偽の行の `col_elevation`・`prominence` は読まないので見ない）。`col_lat`・`col_lon` が有限でも ±180 の外なら、2 の `format_coord` が `std::invalid_argument` を投げる（ファイルに触れる前に投げることは同じ。行をまたぐと、ほかの行の上の検査より後に投げることになるが、どちらも `std::invalid_argument` で、UT は型だけを確かめる）。
2. 中身を作る。`_header` と `\n`、続けて行ごとに次の 10 列を `,` でつないで `\n` を続ける（BOM・CR・引用符を書かない。最後の行も `\n` で終える）: `lat_text`、`lon_text`、`_format_fixed(peak_elevation, 2)`、`format_coord(col_lat)`、`format_coord(col_lon)`、`key_col_resolved` が真なら `_format_fixed(col_elevation, 2)`（偽なら空）、同じく `prominence`、`true` か `false`、`col_margin_px` の 10 進（`std::to_string`。負の値は `-1` のように `-` を付ける）、`analysis_id`。0 件なら見出しの行だけ（[HLD 4.7.3](30_HLD.md#473-異常系)）。
3. パスを決め、書く。`path = csv_dir + "/" + analysis_id + ".csv"`、`tmp = path + ".tmp"`（[2.3](#23-ファイルの名前と書き方) の一時ファイルの決まり）。書くのと置き換えるのは、[6.9.3](#693-関数の細部) の `write_meshset` の 4・5 と同じ（2.3 の「書く（C++）」「置き換える（C++）」、`_write_all`）。どの段で失敗しても、2.3 のとおり後始末をしてから CW1 を出して止まる（置き換えに失敗したときは `unlink(tmp)` してから CW1。`{reason}` は控えた `errno` の `std::strerror`）。CW1 の `{path}` は、どの段でも `path`（一時ファイルでなく本来の名前）。
4. ディレクトリを作らない。`csv_dir` が無ければ、`open` が `ENOENT` で失敗して CW1 になる（`results/csv` を作るのは 6.11。[6.5.3](#653-関数の細部) の `images/` と同じ）。ディレクトリの `fsync` はしない。
5. 書けずに止まったときは、前の起動の CSV を消さない（[6.9.3](#693-関数の細部) の 6 と同じ）。

##### read_back_peak_csv

`std::set<Z15Pixel> read_back_peak_csv(const std::string& path, const std::vector<TargetPeak>& peaks, int n)`

1. 呼ぶ側の誤り: `n` が 4・5・6 のどれでもない、`peaks` が空。
2. `_read_file(path, data, err)` で全部を読む。失敗したら RB1 を出して止まる（`{reason}` は `std::strerror(err)`）。
3. `data` が空なら RB2（`{detail}` は `見出しの行が無い`）。空でなければ、末尾の `\n` を 1 つだけ除き、`\n` のバイトで行に分け、1 から番号を振る。BOM と `\r` は除かない（読むのは CMP4 が自分で書いたファイルだけで、壊れた形を読み飛ばさない。[2.3](#23-ファイルの名前と書き方) の取得完了の記録と同じ考え）。
4. 1 行目がバイト列で `_header` と違えば RB2（`{detail}` は `見出しの行が per-mesh CSV の列の並びでない: {line}`）。
5. 2 行目からの各行を `,` で分ける（無い列は空の文字列とみなす）。上の行から順に、1 行の中で次の順に確かめ、ファイルの順で最初の誤りだけを出して止まる（[HLD 4.7.2](30_HLD.md#472-処理の流れ) の「早期終了への受け渡し」が確かめるとした 3 つだけ）。
   - 1 列目（`peak_lat`）か 2 列目（`peak_lon`）が `_parse_decimal` で読めない（空の行を含む）: RB2（`{detail}` は `{line_no} 行目の peak_lat か peak_lon が数として読めない: {line}`）。
   - 8 列目（`key_col_resolved`）が `true` でも `false` でもない: RB2（`{detail}` は `{line_no} 行目の key_col_resolved が true でも false でもない: {line}`）。
   - ほかの列（列の数を含む）と、緯度経度の範囲は確かめない（`col_elev`・`prominence` の空欄は、未確定の行の正しい値である）。
6. 全行を確かめた後、`key_col_resolved` が `true` の行ごとに、読んだ値が 6.10.3 の `latlon_to_tile` の渡せる範囲（緯度が −85.0511287798066 以上 85.0511287798066 以下、経度が −180 以上 180 未満）に入れば `latlon_to_z15_pixel(lat, lon)` を求め、`peaks` のどれかの `pixel` と等しければ集合に入れる。範囲の外の行は `latlon_to_z15_pixel` を呼ばず、確定を与えない（未定義の動作を避けるため。対象ピークの `pixel` は 6.2 が存在メッシュの中で求めた画素なので、範囲の外の行と一致することは無く、照合の結果は変わらない）。`false` の行は確定を与えない（[DEC53](30_HLD.md#4144-設計判断)「早期終了は対象ピークが確定して出たかで判定する」）。
7. 集合を返す（見出しの行だけなら空）。

- `{path}` は受け取った `path`。`{line}` は分けた行のバイト列のまま、`{line_no}` は 10 進（先頭の `0` なし）。

#### 6.7.4 メッセージ文面

書き方は [2.2](#22-ログとメッセージの文面)。`{path}`・`{reason}`・`{line}`・`{line_no}`・`{detail}` は 6.7.3 のとおり、`{dir}` は `csv_dir`、`{n}` は `read_back_peak_csv` の `n`。

`ERROR:` のメッセージ（2 行目は `対処:` と空白 1 つの後）:

| 記号 | 場面 | 1 行目 | 2 行目 | 終了コード |
|---|---|---|---|---|
| CW1 | per-mesh CSV を書けない | `per-mesh CSV を書けない: {path}: {reason}` | `{dir} の空きと権限を確かめてから、{rerun}` | 1 |
| RB1 | 早期終了の判定に読み戻す per-mesh CSV を読めない | `早期終了の判定に読み戻す per-mesh CSV を読めない: {path}: {reason}` | `{redo}` | 1 |
| RB2 | 早期終了の判定に読み戻した per-mesh CSV の書式が違う | `早期終了の判定に読み戻した per-mesh CSV の書式が違う: {path}: {detail}` | `{redo}` | 1 |

- CW1 は `write_peak_csv`、RB1・RB2 は `read_back_peak_csv` が出す（呼ぶ側の 6.11 は出さない）。
- `{rerun}`: [6.9.4](#694-メッセージ文面) の `{rerun}` と同じ（`analysis_id` の先頭の 1 字で、通常と広域を分ける）。
- `{redo}`: `ディスクの状態を確かめてから、scripts/run_pipeline.sh --phase 3 --n {n} を起動し直して、その段をやり直す（設定ファイルを指定して起動したときは、同じ --config を付ける）`（[HLD 4.14.3](30_HLD.md#4143-異常系) の必ず含める内容の表の、早期終了の判定のために読み戻した per-mesh CSV が読めないか、書式が違う場面の行）。

#### 6.7.5 UT 候補

すべて自動。GoogleTest のケースごとに `// trace: UT-analyze_terrain_csv-NN` を付ける。期待値は、2026-10-30 に CPython 3 の `f'{x:.8f}'`・`f'{x:.2f}'`（`float` の値は `struct` で 32 ビットに丸めた正確な値を使う）と、2.4 の式で求めた（[テスト方針書 3.3](02_test_policy.md#33-期待値の根拠)）。同じ値は `std::to_chars` でも同じ文字列になることを、C++ のプログラムで確かめた。入力と期待の「N 行目」は、見出しの行を 1 行目とするファイルの行の番号である（6.7.3 の `{line_no}` と同じ）。共通の準備は 3 つ。

- **同じプロセス**: [6.9.5](#695-ut-候補) の同じ名前の準備と同じ（`write_meshset` を `write_peak_csv` に読み替える。`csv_dir` は一時のディレクトリの下に作ったディレクトリの絶対パス）。
- **子のプロセス（書けない）**: 6.9.5 の同じ名前の準備と同じ（`write_meshset` を `write_peak_csv` に読み替える）。
- **範囲と行**: `PeakColRow` は、書いた欄のほかは既定の値（`col_lat`・`col_lon`・`col_elevation`・`prominence`・`col_margin_px` は 0）。`TargetPeak` の `peak` は、`lat_text`・`lon_text`・`lat`・`lon` に画素の中心の 8 桁の値を入れる。**通常の範囲**は `meshes = {5235}`、`z14 = false`、`box.x_min = 28671`、`box.y_min = 12979`（ほかの欄は 0）で、グリッドの画素 (px, 86) は Z15 の画素 (7339775 + px, 3322709)。**広域の範囲**は `meshes = {5439}`、`z14 = true`、`picks = {GridXY{10, 10} → Z15Pixel{7456512, 3293952}, GridXY{11, 10} → Z15Pixel{7456514, 3293952}}`、`peaks` は画素 (7456512, 3293952) の 1 件（`36.00465613`・`139.99880075`）。

| ID | 確かめること | 準備 | 入力 | 期待 |
|---|---|---|---|---|
| `UT-analyze_terrain_csv-01` | 8 桁の文字列（2.4 の表 7 から表 5・6 の入力） | 同じプロセス | `format_coord` に、2.4 の表 7 の 9 行の緯度と経度（18 個。倍精度の値は表の 10 進の表記のまま）を 1 つずつ | 表 5・6 の画素の中心の行の入力と同じ文字列。9 行の (緯度, 経度) の順に (`85.05112693`, `-179.99997854`)、(`36.00465613`, `139.99880075`)、(`34.99999777`, `134.99997854`)、(`34.99999777`, `135.00002146`)、(`26.50001531`, `126.99995756`)、(`26.50001531`, `127.00000048`)、(`21.33337317`, `136.49999857`)、(`21.33333320`, `136.49999857`)、(`46.00457835`, `148.99660349`) |
| `UT-analyze_terrain_csv-02` | 8 桁の丸めと符号 | 同じプロセス | `format_coord` に (a) `0.0`、(b) `-0.0`、(c) `0.001953125`、(d) `-0.001953125`、(e) `180.0`、(f) `-180.0`、(g) `-1e-10` | (a)(b)(g) `0.00000000`、(c) `0.00195312`、(d) `-0.00195312`、(e) `180.00000000`、(f) `-180.00000000` |
| `UT-analyze_terrain_csv-03` | `format_coord` の呼ぶ側の誤り | 同じプロセス | NaN、正の無限大、`180.0000001`、`-180.0000001` | どれも `std::invalid_argument` |
| `UT-analyze_terrain_csv-04` | 通常: 一次フィルタと地理的範囲フィルタと順 | 同じプロセス。通常の範囲 | 閾値 130。行は順に (a) (257, 86) 真・`prominence` 130.0f、(b) (258, 86) 真・129.99f、(c) (259, 86) 真・129.996f、(d) (260, 86) 偽・0.0f、(e) (256, 86) 真・500.0f | 2 行で (a)・(d) の順。`lat_text` はどちらも `34.99999777`、`lon_text` は `135.00002146`・`135.00015020`。`row` は入力の (a)・(d) の行と全欄（`peak`・`peak_elevation`・`col_lat`・`col_lon`・`col_elevation`・`prominence`・`key_col_resolved`・`col_margin_px`）が等しい。(b) と (c) は一次フィルタで落ちる（(c) は CSV では `130.00` と書く値だが、6.6 の値 `129.99600219726562` は 130 未満）。(e) は地理的範囲フィルタ（`5234`）で落ちる |
| `UT-analyze_terrain_csv-05` | 広域: 一次フィルタを当てない、控えと照合 | 同じプロセス。広域の範囲 | 閾値 130。行は順に (a) (10, 10) 真・50.0f、(b) (11, 10) 真・999.0f、(c) (12, 10) 真・999.0f、(d) (10, 10) 偽・0.0f | 2 行で (a)・(d) の順、どちらも `36.00465613`・`139.99880075`。(b) は照合（画素 (7456514, 3293952) は対象でない）、(c) は控えが無くて落ちる |
| `UT-analyze_terrain_csv-06` | 0 件 | 同じプロセス。通常の範囲 | `rows` が空 | 空の並び |
| `UT-analyze_terrain_csv-07` | `filter_peak_rows` の呼ぶ側の誤り | 同じプロセス | 各ケースは、次の基本から、そのケースが替える 1 つだけを替える。通常は `analysis_id` `3-5235`・通常の範囲・空の `peaks`、広域は `4-5439-NW`・広域の範囲・`peaks` 1 件（`rows` は空）。(a) `analysis_id` が `3-533`、(b) 通常で `z14` が真、(c) 通常で `peaks` が 1 件、(d) 広域で `z14` が偽、(e) 広域で `peaks` が空、(f) `meshes` が空 | どれも `std::invalid_argument`。標準エラー出力に何も出ない |
| `UT-analyze_terrain_csv-08` | CSV を書く | 同じプロセス | `analysis_id` `3-5235`。行は 3 つ: (1) `34.99999777`・`135.00002146`、`peak_elevation` 1234.56f、`col_lat` 35.01234567891、`col_lon` 135.1、`col_elevation` 1000.25f、`prominence` 234.31f、真、`col_margin_px` 12。(2) `36.00465613`・`139.99880075`、3776.12f、0.0、0.0、0.0f、0.0f、偽、1。(3) `34.99999777`・`135.00006437`、50.0f、0.0、0.0、0.0f、50.0f、真、−1 | `<csv_dir>/3-5235.csv` の中身が、見出しの行と、`34.99999777,135.00002146,1234.56,35.01234568,135.10000000,1000.25,234.31,true,12,3-5235`、`36.00465613,139.99880075,3776.12,0.00000000,0.00000000,,,false,1,3-5235`、`34.99999777,135.00006437,50.00,0.00000000,0.00000000,0.00,50.00,true,-1,3-5235` の 4 行（それぞれ `\n` で終わる）。`.tmp` が無い。標準エラー出力に何も出ない |
| `UT-analyze_terrain_csv-09` | 0 件でも見出しを書く | 同じプロセス | `rows` が空、`analysis_id` `4-5439-NW` | 中身が見出しの行と `\n` だけ |
| `UT-analyze_terrain_csv-10` | 置き換える | 同じプロセス。`3-5235.csv` に `old`、`3-5235.csv.tmp` に 1000 バイトの `x` を置く | UT-analyze_terrain_csv-08 の入力 | UT-analyze_terrain_csv-08 と同じ中身。`.tmp` が無い |
| `UT-analyze_terrain_csv-11` | 置き場が無い、案内の分け方 | 同じプロセス。`csv_dir` は存在しないパス | (a) `analysis_id` が `3-5235`、(b) `5-5439-SE`（`rows` はどちらも空） | `code` 1 の CW1（`No such file or directory`）。(a) の 2 行目は `対処: <csv_dir> の空きと権限を確かめてから、止まったコマンドを同じ引数で起動し直す（それより前のメッシュの出力は残っていて、起動し直すと書き直す）`。(b) の 1 行目のパスは `<csv_dir>/5-5439-SE.csv`、2 行目は `対処: <csv_dir> の空きと権限を確かめてから、scripts/run_pipeline.sh --phase 3 --n 5 を起動し直す（設定ファイルを指定して起動したときは、同じ --config を付ける）` |
| `UT-analyze_terrain_csv-12` | 置き換えに失敗する | 同じプロセス。`3-5235.csv` という名前の空のディレクトリ | UT-analyze_terrain_csv-08 の入力 | `code` 1 の CW1（`Is a directory`）。`.tmp` が無い。ディレクトリは残る |
| `UT-analyze_terrain_csv-13` | 書く途中で失敗する | 子のプロセス（書けない）。親が `3-5235.csv` に `old` を置く。上限は (a) 0、(b) 5 | UT-analyze_terrain_csv-08 の入力 | (a)(b) とも、子の終了コード 1、標準エラー出力が CW1（`File too large`）。`3-5235.csv` は `old` のまま、`.tmp` が無い |
| `UT-analyze_terrain_csv-14` | `write_peak_csv` の呼ぶ側の誤り | 同じプロセス | UT-analyze_terrain_csv-08 の入力を基に、(a) `csv_dir` が空、(b) 末尾が `/`、(c) `analysis_id` が `3-5235-NW`、(d) (1) の `peak_elevation` が NaN、(e) (1) の `prominence` が正の無限大、(f) (1) の `lat_text` が空、(g) (1) の `lon_text` が `abc`。ほかに (h) (2) の行（偽）の `col_elevation`・`prominence` を NaN にしたもの | (a)〜(g) はどれも `std::invalid_argument` で、(c)〜(g) は `csv_dir` の下にファイルができない（(a)(b) は確かめる場所が決まらないので、ファイルを確かめない）。(h) は投げず、UT-analyze_terrain_csv-08 と同じ中身を書く |
| `UT-analyze_terrain_csv-15` | 読み戻して確定を求める | 同じプロセス。`peaks` は 3 件（画素 (7456512, 3293952)・(7340032, 3322709)・(7340033, 3322709)）。ファイルは見出しの行の後に `36.00465613,139.99880075,1234.56,35.01234568,135.10000000,1000.25,234.31,true,12,4-5439-NW`（対象の 1 件目）、`34.99999777,135.00002146,3776.12,0.00000000,0.00000000,,,false,1,4-5439-NW`（2 件目）、`34.99999777,135.00010729,50.00,0.00000000,0.00000000,0.00,50.00,true,-1,4-5439-NW`（対象でない画素 7340034）の 3 行（どれも `\n` で終わる。1 行目が見出し、データは 2〜4 行目） | `read_back_peak_csv(<パス>, peaks, 4)` | 集合が {(7456512, 3293952)} の 1 件 |
| `UT-analyze_terrain_csv-16` | 書いたものを読み戻す | 同じプロセス。UT-analyze_terrain_csv-05 の (a)(d) の結果を `write_peak_csv` で `4-5439-NW` に書く。`peaks` は広域の 1 件 | そのパスで `read_back_peak_csv` | 集合が {(7456512, 3293952)}。このファイルは同じ画素の行が 2 つあり、CMP5 の [HLD 4.8.2](30_HLD.md#482-処理の流れ) の 3「行を読む」には外れるので、6.11 の UT・結合テスト（IT）に流用しない |
| `UT-analyze_terrain_csv-17` | 確かめないものは止めない | 同じプロセス。UT-analyze_terrain_csv-15 の `peaks` | (a) UT-analyze_terrain_csv-09 のファイル、(b) UT-analyze_terrain_csv-15 のファイルから最後の `\n` を除いたもの、(c) 15 のファイルの 2 行目の `peak_elev` を `x` にし、末尾に `,extra` を足したもの（11 列）、(d) 15 のファイルに `89.00000000,139.99880075,1.00,0.00000000,0.00000000,0.00,1.00,true,-1,4-5439-NW` の行（緯度が範囲の外の `true` の行）を足したもの、(e) 同じく `36.00465613,180.00000000,1.00,0.00000000,0.00000000,0.00,1.00,true,-1,4-5439-NW`（経度が範囲の外）を足したもの | (a) は空の集合。(b)(c)(d)(e) は 15 と同じ集合で、標準エラー出力に何も出ない |
| `UT-analyze_terrain_csv-18` | 読めない | 同じプロセス。`peaks` は UT-analyze_terrain_csv-15 と同じ 3 件 | (a) 存在しないパスで `n` 4、(b) 一時のディレクトリそのもので `n` 6 | `code` 1 の RB1。(a) は `No such file or directory`、(b) は `Is a directory`。2 行目は `{redo}` で、(a) は `対処: ディスクの状態を確かめてから、scripts/run_pipeline.sh --phase 3 --n 4 を起動し直して、その段をやり直す（設定ファイルを指定して起動したときは、同じ --config を付ける）`、(b) は `--n 6` |
| `UT-analyze_terrain_csv-19` | 書式が違う | 同じプロセス。UT-analyze_terrain_csv-15 のファイルと `peaks` | (a) 0 バイト、(b) 全行の `\n` の前に `\r` を足す（CRLF のファイル）、(c) 先頭に BOM、(d) 見出しの `prominence` を `prom` に替える、(e) 2 行目の `peak_lat` を `1e5`、(f) 2 行目の `peak_lon` を空、(g) 2 行目と 3 行目の間に空の行を足す、(j) 2 行目の `key_col_resolved` を `True`、(k) 2 行目を `36.00465613,139.99880075` だけにする、(l) 3 行目の `key_col_resolved` を `x`、4 行目の `peak_lat` を `y` にする | どれも `code` 1 の RB2。`{detail}` は (a) `見出しの行が無い`、(b)(c)(d) `見出しの行が per-mesh CSV の列の並びでない:` と空白 1 つの後に見出しの行のまま、(e)(f)(g) `<行番号> 行目の peak_lat か peak_lon が数として読めない:` と空白 1 つの後に行のまま（(g) は 3 行目で行は空）、(j)(k) `2 行目の key_col_resolved が true でも false でもない:` と空白 1 つの後に行のまま、(l) 3 行目だけを挙げる。(h)(i) は欠番（緯度経度の範囲の外は止めない。UT-analyze_terrain_csv-17 の (d)(e) で確かめる） |
| `UT-analyze_terrain_csv-20` | `read_back_peak_csv` の呼ぶ側の誤り | 同じプロセス。UT-analyze_terrain_csv-15 のファイル | (a) `n` 3、(b) `n` 7、(c) `peaks` が空 | どれも `std::invalid_argument`。標準エラー出力に何も出ない |
| `UT-analyze_terrain_csv-21` | 2 桁の符号 | 同じプロセス | UT-analyze_terrain_csv-08 の (1) の行の `peak_elevation` を (a) `-0.001f`、(b) `-5.5f` にして書く | 2 行目の 3 列目が (a) `0.00`、(b) `-5.50` |

- パターンをまたいだ確定の積み上げと早期終了は 6.11 の UT 候補に置き、書いた per-mesh CSV を CMP5 の `merge_peaks` が読めることは結合テスト（IT）で確かめる（[ADR-LLD-001](decisions/ADR-LLD-001-lld-format-module-granularity-and-t2-timing.md) の Decision 2）。

### 6.8 `analyze_terrain_zone`

- **ID**: LLD-analyze_terrain_zone
- **対応 HLD**: [3.4](30_HLD.md#34-cmp4-地形解析エンジン)・[4.16](30_HLD.md#416-fr-016-ピーク域ポリゴン生成)・[5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)・[5.9](30_HLD.md#59-nfr-009-観測可能性中間成果物の可視化)
- **ファイル**: `src/zone.hpp`・`src/zone.cpp`

関数の名前と役割は [HLD 3.4.3](30_HLD.md#343-関数) の表の「ゾーン」の群である。処理の正本は、塗りの準備が [HLD 4.16.2](30_HLD.md#4162-処理の流れ) の「準備」、閾値の条件と塗りが同じ節の 1「閾値の条件を決める」・2「塗る」、`area_complete` が 3「`area_complete` を決める」、輪郭が 4「輪郭を取る」と頂点の段落、GeoJSON が「Feature」と「書き出し」である。止まる場面は [HLD 4.16.3](30_HLD.md#4163-異常系) の「GeoJSON の書き込みに失敗する」の行、書き込みの失敗は [HLD 2.5.5](30_HLD.md#255-書き込みの失敗) である。ゾーンは通常モードだけで作り、広域モードでは作らない（[HLD 4.16.1](30_HLD.md#4161-目的と範囲)）。[HLD 5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)（再現性）は、Feature の順と、Polygon・環の並べ方と環の始まりの頂点を決め切ること、角を 6.10 の `tile_to_latlon` と 6.7 の `format_coord` で文字列にすること、GeoJSON の字句（空白、キーの順、数の書き方）を決め切ることで受ける。[HLD 5.9](30_HLD.md#59-nfr-009-観測可能性中間成果物の可視化)（観測可能性）は、Feature・`properties`・スタイルの属性を HLD 4.16.2 の「Feature」のとおりに書くことで受ける。メモリは、[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の「メモリ」の段落が挙げる訪問の印（画素ごとに 1 ビット）、塗った画素の番号の並び（待ち行列を兼ねる）、輪郭の辺を、[6.8.2](#682-型とデータ)・[6.8.3](#683-関数の細部) の形で持つことで受ける。段落が挙げていないものとして、解析単位の全行のゾーンの頂点の文字列（`RowZones`）を `write_zone_geojson` まで持つことと、GeoJSON の全文を 1 つの文字列に組むことがある。大きさは [HLD 5.2.2](30_HLD.md#522-処理の流れ) の実測の計画の 1 で測る。[HLD 4.16.1](30_HLD.md#4161-目的と範囲) の対象外の行が LLD に送った項目（辺のつなぎ方と環の最初の頂点、一直線の頂点の除き方、訪問の印の持ち方、設定の値をキーにする丸め、GeoJSON の数と空白の書き方）は、この節で決める。4 つの関数は `check_signal` を呼ぶ（[HLD 3.4.3](30_HLD.md#343-関数) の表の後の段落が挙げる群に「ゾーン」が入っている）。区切りと遅れの上限は [6.8.3](#683-関数の細部) の前置きで決める。関数を呼ぶ順は 6.11 の `run_normal_mode` で決まる（[HLD 3.4.3](30_HLD.md#343-関数) の呼ぶ順: `filter_peak_rows` → `write_peak_csv` の後、フィルタの後のリストの行ごとに、アクティベーションゾーン、delete判定ゾーンの順に `fill_zone` → `judge_area_complete` → `trace_outline`、続けて `write_zone_geojson`、その後に `write_meshset`）。入力のフィルタの後のリストは 6.7 の `filter_peak_rows` が返す `PeakCsvRow` の並びで、書いた CSV の行と同じ順である（[6.7.2](#672-型とデータ)）。この節は、それを C++ で書くための細部を足す。1.2 の C++ の規約に従う。

#### 6.8.1 ファイル割付

- 公開の宣言は `src/zone.hpp`、定義と内部の関数は `src/zone.cpp` に置く。どちらも先頭のコメントに `// trace: LLD-analyze_terrain_zone` を書き、ヘッダーは次の行を `#pragma once` にする。
- `src/zone.hpp` は `"csv.hpp"`（`PeakCsvRow`）・`"grid.hpp"`（`ElevationGrid`・`GridRange`）・`<cstdint>`・`<set>`・`<string>`・`<vector>` を読む。`src/zone.cpp` は `"zone.hpp"`・`"common.hpp"`・`"convert.hpp"`・`"csv.hpp"`（`format_coord`）・`"grid.hpp"`（`pixel_center_mesh`）・`<algorithm>`・`<cerrno>`・`<charconv>`・`<cmath>`・`<cstdint>`・`<cstdio>`・`<cstring>`・`<fcntl.h>`・`<map>`・`<stdexcept>`・`<string>`・`<system_error>`・`<unistd.h>`・`<utility>`・`<vector>` を読む。OpenCV のヘッダーは直接読まない（`grid.hpp` が core を読む）。
- UT のコードは `tests/src/test_zone.cpp` に置き、`build/test_zone` にビルドする（[2.5](#25-ビルドとテストの名前)。`src/` の `main` を持たない `.cpp` をすべてリンクするので、`common.cpp`・`convert.cpp`・`grid.cpp`・`csv.cpp` も入る）。各テストに `// trace: UT-analyze_terrain_zone-NN`（確かめる UT 候補の ID）のコメントを付ける。2.4 の式で期待値を求めたテスト（UT 15）には、`2.4 の tile_to_latlon` もコメントに書く（[テスト方針書 3.3](02_test_policy.md#33-期待値の根拠)）。テストの枠組みは GoogleTest（[テスト方針書 3.4](02_test_policy.md#34-テストを先に書く進め方)）。

#### 6.8.2 型とデータ

`src/zone.hpp` の公開の宣言は次のとおり（名前空間に入れない。1.2 の C++ の規約）。

```cpp
#pragma once
#include <cstdint>
#include <set>
#include <string>
#include <vector>
#include "csv.hpp"
#include "grid.hpp"

enum class ZoneKind : std::uint8_t {
    Activation,   // アクティベーションゾーン
    Delete,       // delete判定ゾーン
};

struct ZoneThreshold {
    std::int64_t key = 0;   // 比べるキー（0.01m 単位）
    bool exclusive = false; // 真なら k(e) > key、偽なら k(e) >= key
};

struct ZoneFill {
    std::vector<std::int64_t> pixels;   // 塗った画素の番号（py × W + px）。先頭はピークの画素
    ZoneThreshold threshold;
};

struct ZoneVertex {
    std::string lat_text;   // format_coord の文字列
    std::string lon_text;
};

struct ZonePolygon {
    std::vector<ZoneVertex> outer;              // 外周の環（反時計回り。始まりの頂点を終わりにもう一度置く）
    std::vector<std::vector<ZoneVertex>> holes; // 穴の環（時計回り。同じく閉じる）
};

struct RowZones {
    std::vector<ZonePolygon> delete_zone;       // 1 つなら Polygon、2 つ以上なら MultiPolygon
    bool delete_complete = false;               // delete判定ゾーンの area_complete
    std::vector<ZonePolygon> activation_zone;
    bool activation_complete = false;
};

ZoneFill fill_zone(const PeakCsvRow& row, ZoneKind kind, const ElevationGrid& grid,
                   const GridRange& range, long long activation_zone_drop_m,
                   long long delete_zone_max_drop_m, std::vector<std::uint64_t>& marks);
bool judge_area_complete(const std::vector<std::int64_t>& pixels, const ZoneThreshold& threshold,
                         const ElevationGrid& grid, const GridRange& range,
                         const std::set<std::string>& japan_meshes,
                         const std::set<std::string>& excluded_meshes);
std::vector<ZonePolygon> trace_outline(const std::vector<std::int64_t>& pixels,
                                       const GridRange& range);
void write_zone_geojson(const std::vector<PeakCsvRow>& rows, const std::vector<RowZones>& zones,
                        const std::string& analysis_id, const std::string& csv_dir);
```

- 引数の並びは [HLD 3.4.3](30_HLD.md#343-関数) の表の受け取るものの順。`row` は 6.7 の `filter_peak_rows` が返した行（`row.row.peak` はグリッドの画素のまま）。`kind` はゾーンの種類。設定の 2 つ（`activation_zone_drop_m`・`delete_zone_max_drop_m`）は 6.12 の `ConfigValue::integer`（`long long`）をそのまま受ける。`japan_meshes`・`excluded_meshes` は 6.11 が `read_mesh_list_file` で読んだ日本全土1次メッシュコードリストと北方領土除外メッシュリスト。`zones` は `rows` と同じ数で同じ順（行ごとのゾーン）。`csv_dir` は `data_dir` の下の `results/csv` の絶対パスで、末尾に `/` を付けない（6.7・6.9 と同じ。6.11 が組み立てて渡す）。
- 座標の書き方（この節で使う）: グリッドの画素 (px, py) は、西から px 列目、北から py 行目（6.4 の `ElevationGrid`）。グリッドの角 (cx, cy) は画素の角の格子点で、画素 (px, py) の北西の角が (px, py)、南東の角が (px + 1, py + 1)（[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の頂点の段落）。cy は南へ増える。
- 訪問の印（[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の「準備」）は `std::vector<std::uint64_t>`（画素 p のビットは `marks[p / 64]` の `p % 64` ビット目）。6.11 が解析単位の初めに `(W × H + 63) / 64` 個の 0 で 1 回だけ作り（最大の窓の約 46 億画素で約 0.54GiB）、行と種類ごとの `fill_zone` に同じものを渡す。`fill_zone` は塗った画素のビットを立て、返す前にそのビットだけを消す（正常に返るときは、いつもすべて 0 の状態で返る）。印を作る関数は足さない（1.2 の「LLD が足してよい名前」）。
- 閾値の条件は `ZoneThreshold`。`fill_zone` が返し、6.11 が同じ行・同じ種類の `judge_area_complete` に渡す。
- `trace_outline` の頂点は `ZoneVertex` の文字列（[HLD 3.4.3](30_HLD.md#343-関数) の「頂点は緯度経度の文字列」）。`ZonePolygon` の並びが 1 つのゾーンの形で、1 つなら GeoJSON の Polygon、2 つ以上なら MultiPolygon になる。
- 画素の番号は `std::int64_t`（6.6.2 と同じ。番号を詰めるかは [#187](https://github.com/jj1xgo/findsummits/issues/187)「最大の窓で画素の番号を詰めるか」で決め、決まったらこの節の型も直す）。
- 内部（`src/zone.cpp` の無名の名前空間）:
  - `_zone_key(float)`: 6.6 の `_scan_key` と同じ（`std::llround(static_cast<double>(v) * 100.0)`。[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の k(e)）。
  - `_center_code`: 画素の中心が入るメッシュコードを、行（py）ごとの上 2 桁と列（px）ごとの下 2 桁の控えから求める内部の手順（[6.8.3](#683-関数の細部) の「範囲の判定」）。控えを持つ型は書く人が決めてよい。
  - `_check_analysis_id_normal(関数名, analysis_id)`: `3` と `-` と 4 バイトの ASCII の数字（合わせて 6 バイト）でなければ `std::invalid_argument`（[6.9.3](#693-関数の細部) の `write_meshset` の 1 の 2 つ目の判定の、通常の形だけ）。
  - `_parse_decimal(const std::string& s, double& out)`: [6.7.2](#672-型とデータ) と同じ（[6.2.3](#623-関数の細部) の `read_unresolved_peaks` の 7「数として読める」と同じ判定と値）。
  - `bool _write_all(int fd, const std::string& s)`: [6.9.2](#692-型とデータ) と同じ形。
  - 上の一覧のほかに、2 つ以上の関数で同じ判定や文を使う補助の関数（範囲の判定、角の文字列への変換、ZW1 を出して止まる手順など）は、足してよい（名前は `_` と英小文字で始め、公開の宣言に出さない。[6.7.2](#672-型とデータ) と同じ）。

#### 6.8.3 関数の細部

処理の正本は 6.8 の前置きのとおりで、この節は C++ で書くための細部を足す。止まるときは、メッセージを `log_error` で出してから `throw ExitRequest(EXIT_ERROR)` する（1.2 の C++ の規約）。呼ぶ側の誤りは `std::invalid_argument` を投げる（6.2・6.7・6.9・6.10 と同じ。`main` は捕まえないので、6.12 の `_on_terminate` が G7 で止める）。文は `<関数名>:` と空白 1 つの後に内容を続ける形で、内容は書く人が決めてよい（UT は例外の型だけを確かめる）。通常のログと警告は出さない（段の始まりのログは 6.11）。メモリを確保できないときの `std::bad_alloc` は捕まえない（6.12 の `_on_terminate` が G7 で止める。終了コード 1。[HLD 4.16.3](30_HLD.md#4163-異常系) の後の段落）。

シグナル: 4 つの関数とも、呼び出しごとに 1 つの数え（0 から）を持ち、下に挙げるループの 1 回ごとに、その回の処理の前に、数えが 2²⁰ の倍数なら `check_signal()` を呼んでから、数えに 1 を足す（ループをまたいで数え続ける。最初のループの 1 回目の前にも呼ぶ。6.6.3 の「2²⁰ の倍数のとき、その要素の前」と同じ考えを、関数全体の数えで行う）。数えるループは次のとおり。

- `fill_zone`: 3 の塗った画素を 1 つ読むごとと、4 の印を 1 つ消すごと。
- `judge_area_complete`: 2 の塗った画素 1 つごと。
- `trace_outline`: 1 の範囲の確かめの画素 1 つごと、2 の成分の番号付けで画素を 1 つ取り出すごと（外側の走りと内側のたどりの両方）、3 の画素 1 つごと、4 の辺を 1 本使うごと、5 の角を 1 つ読むごと、6・7 の環の角 1 つごと、8 の角 1 つごと。
- `write_zone_geojson`: 2 で座標の組（[経度, 緯度] 1 つ）を 1 つ書くごと。

受けてから止まるまでの遅れは、2²⁰ 回の処理の分まで。区切りを置けないのは、`std::vector` の確保・写し・並べ替えと、`write_zone_geojson` の 3 の書き出しの間だけで、その後の最初の区切りまで延びる（書き出しの後に区切りは無いので、書き出しの間に受けたシグナルは、6.11 の次の区切りで止まる）。

範囲の判定（内部の `_center_code`）: 画素 (px, py) の中心が入るメッシュコードは、6.4 の `pixel_center_mesh({256 × x_min + px − 1, 256 × y_min + py − 1})`（`x_min`・`y_min` は `range.box`）である。画素ごとに呼ぶと `sinh`・`atan` を画素の数だけ通すので、呼ぶ関数の中で、行 py の上 2 桁と、列 px の下 2 桁を、それぞれ初めて要るときに 1 回だけ `pixel_center_mesh` で求めて控える。上 2 桁は、基準の列 `px0` と行 py の画素の `pixel_center_mesh` の先頭 2 字、下 2 桁は、列 px と基準の行 `py0` の画素の後ろ 2 字である（基準の画素 (px0, py0) は、その関数がはじめに受け取った画素で、`fill_zone` ではピーク、`judge_area_complete` では `pixels[0]`。中心が範囲の中にあるので、コードは空でない）。`pixel_center_mesh` が空の文字列を返したら、その行か列は「番号の範囲の外」と控え、その行か列の画素のコードは空の文字列とする。こうして求めたコードは、画素ごとに `pixel_center_mesh` を呼んだ値と同じである（中心の緯度は py だけ、経度は px だけで決まり〈2.4 の `z15_pixel_center_latlon`〉、`latlon_to_mesh` の上 2 桁は緯度だけ、下 2 桁は経度だけで決まる。[6.4.3](#643-関数の細部) の `build_tile_elevation` の 3 と同じ理由）。控えは行の数 H と列の数 W の配列で、関数を出るときに捨てる。画素の中心が範囲の中にあるとは、このコードが `range.meshes` にあることをいう。

##### fill_zone

`ZoneFill fill_zone(const PeakCsvRow& row, ZoneKind kind, const ElevationGrid& grid, const GridRange& range, long long activation_zone_drop_m, long long delete_zone_max_drop_m, std::vector<std::uint64_t>& marks)`

1. 呼ぶ側の誤り（この順に確かめ、最初に当たったもので投げる）: `range.z14` が真（ゾーンは通常モードだけ）。`grid.width`・`grid.height` が `256 × (x_max − x_min + 1) + 2`・`256 × (y_max − y_min + 1) + 2` と違う（`range.box` から。`std::int64_t` で計算する。[6.6.3](#663-関数の細部) の `build_col_list` の 1 と同じ）。`grid.values.size()` が W × H と違う。`marks.size()` が `(W × H + 63) / 64` と違う。`row.row.peak` が外周でないグリッドの中（px が 1〜W − 2、py が 1〜H − 2）に無い。ピークの画素の値が陸地（`> 0.0f`）でない。ピークの画素の値が `row.row.peak_elevation` と `==` でない。ピークの画素の中心が範囲の中でない。
2. 閾値の条件を決める（[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の 1「閾値の条件を決める」。`kp = _zone_key(row.row.peak_elevation)`）。
   - アクティベーションゾーン: `{kp − 100 × activation_zone_drop_m, false}`。
   - delete判定ゾーン: `key_col_resolved` が真なら `kc = _zone_key(row.row.col_elevation)` を求め（偽の行の `col_elevation` は読まない。[6.6.2](#662-型とデータ)）、`kc >= kp − 100 × delete_zone_max_drop_m` なら `{kc, true}` にする（コルの標高を含めない。[DEC70](30_HLD.md#4164-設計判断)「Key コルで決まる閾値はコルの標高を含めない」。2 つが等しいときもこちら）。それ以外（`key_col_resolved` が偽か、コルがそれより低い）は `{kp − 100 × delete_zone_max_drop_m, false}`。海面確定の行（`col_elevation` が 0）で前者に当たると `{0, true}` になり、陸地の画素（値は 0.01 以上でキーは 1 以上）がすべて条件を満たす。特別扱いしない。
   - 設定の値は整数なので、`100 × d` が HLD の round(100 × d) と同じ値になる。範囲は確かめない（6.12 の `load_config` が確かめた値）。
3. 塗る（[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の 2「塗る」。[DEC69](30_HLD.md#4164-設計判断)「塗りは範囲の中の陸地の画素だけを 8 近傍でたどる」）。ピークの画素 p0 の印を立て、`pixels = {p0}` にする。`i` を 0 から、`i < pixels.size()` の間、`pixels[i]` の画素 (px, py) の 8 近傍を、(dy, dx) が (−1, −1)・(−1, 0)・(−1, 1)・(0, −1)・(0, 1)・(1, −1)・(1, 0)・(1, 1) の順に見て、次のすべてを満たす画素 q の印を立てて、`pixels` の末尾に足す。
   - q の印が立っていない。
   - q が外周でない（px が 1〜W − 2、py が 1〜H − 2）で、値が陸地（`> 0.0f`）である。外周の人工ボーダーは位置で除く（[HLD 4.5.2](30_HLD.md#452-処理の流れ) の「走査の準備」の 1「画素を 4 つに分ける」。値は 0 なので陸地の判定でも落ちるが、位置で見る）。
   - `_zone_key(値)` が閾値の条件を満たす（`exclusive` なら `>`、でなければ `>=`）。
   - q の中心が範囲の中である（上の「範囲の判定」）。

   ピークの画素は条件を見ずに塗る（[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の 2 の「ピークの画素は必ず塗る」。プロミネンスが 0 の行で `{kp, true}` になっても塗る）。`pixels` は待ち行列を兼ねる（先頭から読み、末尾に足す。別の待ち行列を持たない）。8 近傍の確かめの順は、条件の結果に効かない。
4. `pixels` の画素の印を全部消す（`marks` を、呼ぶ前と同じすべて 0 にする。[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の「準備」の「塗りを終えたらその画素の印だけを消す」）。呼ぶ前に印がすべて 0 であることは確かめない（W × H に比例する手間になるため）。途中で例外（`ExitRequest`・`std::bad_alloc`）が出たときは印が立ったまま残るが、そのときはプロセスが止まるので使い回されない。
5. `{pixels, 閾値の条件}` を返す。

- 返す並びの順は、3 の塗った順（先頭がピーク）。`judge_area_complete`・`trace_outline` の結果は、この順に依らない。

##### judge_area_complete

`bool judge_area_complete(const std::vector<std::int64_t>& pixels, const ZoneThreshold& threshold, const ElevationGrid& grid, const GridRange& range, const std::set<std::string>& japan_meshes, const std::set<std::string>& excluded_meshes)`

1. 呼ぶ側の誤り: `range.z14` が真、グリッドの大きさと値の数（`fill_zone` の 1 と同じ）、`pixels` が空、`pixels` に 0 以上 W × H 未満でない番号がある、`pixels` に外周の画素（px が 0 か W − 1、または py が 0 か H − 1）がある（`fill_zone` は外周を塗らない。外周を除けば、8 近傍はいつもグリッドの中）、`pixels[0]` の中心が範囲の中でない。8 近傍は、番号の足し引きでなく (px, py) から求める。
2. 塗った画素ごとに（並びの順）、8 近傍の画素 q（`fill_zone` の 3 の順と同じ）を次の順で見て、どれかが「途切れた」なら `false` を返す（[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の 3「`area_complete` を決める」。[DEC73](30_HLD.md#4164-設計判断)「`area_complete` は範囲の外の隣の画素で決める」）。
   1. q が外周（px が 0 か W − 1、または py が 0 か H − 1）: 人工ボーダーなので、途切れた。
   2. q のコード `m`（上の「範囲の判定」）が `range.meshes` にある（範囲の中）: 見ない。
   3. `m` が空の文字列か、`japan_meshes` に無いか、`excluded_meshes` にある: 途切れたとみなさない。
   4. `m` の `mesh_to_latlon` が `range.box.bbox` の中（`south >= bbox.south`・`west >= bbox.west`・`north <= bbox.north`・`east <= bbox.east`。[6.4.3](#643-関数の細部) の `build_tile_elevation` の 4 と同じ比べ方。メッシュは bounding box の中か外のどちらかに丸ごと入る）: NODATA で埋めた範囲なので、値によらず途切れた。
   5. それ以外（はみ出し）: q の値が陸地（`> 0.0f`）で、`_zone_key(値)` が閾値の条件を満たせば、途切れた。そうでなければ、途切れたとみなさない。
3. どれにも当たらなければ `true` を返す。

- 外周を先に見るのは、外周の画素の中心のコードが範囲のメッシュになることがあるため（位置で人工ボーダーを見分ける。[HLD 4.5.2](30_HLD.md#452-処理の流れ) の 1）。グリッドを 6.4 の `build_grid_z15` で作れば、外周は bounding box の外のタイルのさらに外なので範囲に入らないが、UT は小さい範囲で組むので、順を決めておく。
- `mesh_to_latlon` の判定は、コードごとに 1 回だけ求めて控えてよい（結果は同じ）。

##### trace_outline

`std::vector<ZonePolygon> trace_outline(const std::vector<std::int64_t>& pixels, const GridRange& range)`

[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の 4「輪郭を取る」と頂点の段落を、次の 1〜8 で行う（[DEC71](30_HLD.md#4164-設計判断)「輪郭は塗った画素の境界をたどる」・[DEC72](30_HLD.md#4164-設計判断)「穴は内側の環として出す」）。

1. 呼ぶ側の誤り: `range.z14` が真、`pixels` が空。W・H は、`fill_zone` の 1 の式で `range.box` から求める。`pixels` を写して昇順に並べ（`S`）、0 以上 W × H 未満でない番号か、重なる番号があれば `std::invalid_argument`。塗った画素かは、(px, py) がグリッドの中（px が 0〜W − 1、py が 0〜H − 1）のときだけ `std::binary_search(S, py × W + px)` で引き、グリッドの外は塗っていないとする（隣は番号の足し引きでなく (px, py) から求める。px が 0 の画素の西の隣を番号 − 1 で引くと、前の行の東の端の画素と取り違えるため）。外周の画素を受けてもよい。
2. 4 連結の成分の番号: `S` の順に、まだ番号の無い画素から 4 近傍（北・西・南・東）でたどって、同じ番号を付ける（番号は 0 から、見つけた順。`S` と同じ数の `std::uint32_t` の並びで持つ）。
3. 辺: `S` の各画素 (px, py) について、北・西・南・東の順に、隣が塗っていなければ、塗った画素を左に見る向きの単位の辺を 1 本作る。角の座標で、北は (px + 1, py) から西へ、西は (px, py) から南へ、南は (px, py + 1) から東へ、東は (px + 1, py + 1) から北へ。辺は、始まりの角・向き・その画素の成分の番号を持つ。辺を（始まりの cy、始まりの cx、向き〈東・北・西・南の順〉）の昇順に並べる。どの角でも、そこから出る辺は 1 本か 2 本で、2 本なのは塗った画素が斜めにだけ接する角だけである。
4. たどる: 並べた辺を先頭から見て、使っていない辺 e から閉じた歩みを作る。角の並び `walk = {e の始まり}`、`cur = e` にする。`cur` を使った印にし、`cur` の終わりの角 v から出る辺を、3 の並びから引く（二分探索）。1 本ならそれを、2 本なら `cur` の向きを左に 90 度回した向き（東→北→西→南→東）の辺を、次の辺にする（いまたどっている塗った画素の側に曲がり、斜めの塗った画素へは渡らない。[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の 4）。次が e なら歩みを閉じる。そうでなければ v を `walk` に足し、`cur` を次の辺にして続ける。歩みの辺は、どれも e と同じ成分の番号を持つ（左へ曲がる規則は、4 近傍でつながる画素の辺だけをたどる）。
5. 環を分ける: `walk` を先頭から読み、角をスタックに積む。積んである角がまた来たら、スタックのその角から上を、その角で閉じた 1 つの環として取り出し、その角を残してそれより上を下ろす。読み終えたら、スタックの残りを 1 つの環にする（[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の 4 の「同じ頂点を 2 度通る環は…その頂点で環を分ける」）。分けた環は、歩みの成分の番号を受け継ぐ。
6. 一直線の頂点を除く: 環ごとに、前の角から来る向きと次の角へ行く向きが同じ角を除く（環の前後をつないで見る。単位の辺の向きで判定するので、除く角は 1 回の見直しで決まる）。続けて、環を、cy が最小で、その中で cx が最小の角から始まるように回す（その角は曲がり角で、除かれない）。
7. 向きと Polygon: 環ごとに、角 (cx, cy) の並び（閉じる前）で `A = Σ (x_{i+1} × y_i − x_i × y_{i+1})`（添字は環の前後をつなぐ。`std::int64_t`）を求める。正なら外周（地図の上で反時計回り）、負なら穴（時計回り）である。0 にはならない。各成分の外周はちょうど 1 つで、成分ごとに 1 つの Polygon を作り、同じ成分の番号の穴を、その Polygon の穴にする（[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の 4 の「各穴は、それを囲む外周…のうち最も内側のもの」と同じ結果になる。理由は下の箇条）。Polygon は外周の始まりの角の (cy, cx) の昇順（北が先、同じなら西が先）、同じ Polygon の穴も始まりの角の (cy, cx) の昇順に並べる（[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の「Feature」の並べ方。環の始まりは最も北で最も西の角なので、その角を比べる）。並べ替えは安定な並べ替えにする（同じ角を始まりに持つ環は無いが、あっても結果が決まる）。
8. 角を文字列にする: 角 (cx, cy) は、全球の Z15 の画素の角 (gx, gy) = (256 × x_min + cx − 1, 256 × y_min + cy − 1) である。`c = tile_to_latlon(static_cast<double>(gx), static_cast<double>(gy), 23)` の `lat`・`lon` を `format_coord` で文字列にする（[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の頂点の段落。画素の中心でなく角なので、0.5 を足さない）。環の終わりに、始まりの角をもう一度置く。

- 穴の帰属: 穴の環の辺の左はどれも、その成分 C の塗った画素なので、穴は C の外周の内側にある。C の外周より内側にあって、この穴を囲む外周 O があるとすると、O は C の画素の一部を内側に含み、C は 4 近傍でつながっていて O の辺（O の成分の画素と、その外の画素の間の辺）を越えないので、C 全体が O の内側にあり、C の外周が O の内側に来て矛盾する。よって、穴を囲む外周のうち最も内側のものは、C の外周である。UT 18 が、乱数の塗りで、すべての画素の中心の内外を確かめる。
- 環は同じ角を 2 度通らず、外周と穴は 1 つの角で接することがある（OGC が許す。DEC71・DEC72）。

##### write_zone_geojson

`void write_zone_geojson(const std::vector<PeakCsvRow>& rows, const std::vector<RowZones>& zones, const std::string& analysis_id, const std::string& csv_dir)`

1. 呼ぶ側の誤り（ファイルに触れる前に、この順に確かめ、最初に当たったもので投げる）: `csv_dir` が空か最後のバイトが `/`。`analysis_id` が通常の解析識別子の形でない（`_check_analysis_id_normal`。広域モードは GeoJSON を書かない。[HLD 4.16.1](30_HLD.md#4161-目的と範囲)）。`zones.size()` が `rows.size()` と違う。行ごとに（`rows` の順に）: `lat_text`・`lon_text` のどちらかが `_parse_decimal` で読めない、`key_col_resolved` が真で `col_lat` か `col_lon` が有限でないか ±180 の外（`format_coord` が投げる）、`delete_zone`・`activation_zone` のどちらかが空、どれかの環の頂点が 4 つ未満か、最初と最後の頂点の `lat_text`・`lon_text` のどちらかが違う（両方が同じ文字列でなければ誤り）。`lat_text`・`lon_text` と頂点の文字列は、`format_coord` の文字列を受ける前提で、JSON の数の字句として正しいか（先頭の `+`、整数部の先頭の `0` など）は確かめない（`lat_text` の検査は、空と数でない文字列を止めるため。頂点の文字列は確かめない）。
2. 中身（下の「GeoJSON の書き方」）を組み立てる。Feature は [HLD 4.16.2](30_HLD.md#4162-処理の流れ) の「Feature」の順: delete判定ゾーン（すべての行）、アクティベーションゾーン（すべての行）、接続線（`key_col_resolved` が真で、`col_lat`・`col_lon` がどちらも 0.0 でない行）、コル（接続線と同じ行）、ピーク（すべての行）。同じ種類の中は `rows` の順。
3. パスは `csv_dir + "/" + analysis_id + ".geojson"`、一時ファイルは `<パス>.tmp`（[2.3](#23-ファイルの名前と書き方) の一時ファイルの決まり）。書くのと置き換えるのは、[6.7.3](#673-関数の細部) の `write_peak_csv` の 3〜5 と同じ（2.3 の「書く（C++）」「置き換える（C++）」、`_write_all`。失敗は後始末をしてから ZW1 を出して止まり、置き換えに失敗したら `unlink(tmp)` してから ZW1。ZW1 の `{path}` は、どの段でも本来の名前。ディレクトリを作らない〈`results/csv` を作るのは 6.11〉。書けずに止まったときは、前の起動の GeoJSON を消さない）。[HLD 4.16.3](30_HLD.md#4163-異常系) のとおり、同じメッシュの per-mesh CSV は書き終えていて、`.meshset` は書かない（6.11 が `write_meshset` を呼ぶ前に止まる）。

GeoJSON の書き方（[HLD 4.16.1](30_HLD.md#4161-目的と範囲) の対象外の行の「GeoJSON の数と空白の書き方」。UTF-8 で、ASCII だけになる。BOM・CR を書かない）:

- 全体: 1 行目 `{"type":"FeatureCollection","features":[`、続けて Feature を 1 行に 1 つ（最後のほかは行末に `,`）、最後の行 `]}`。どの行も `\n` で終える。Feature が 0 なら、1 行目と最後の行の 2 行だけ。
- 空白を書かない。オブジェクトのキーは、書いた順（Feature は `"type":"Feature"`、`"properties"`、`"geometry"` の順）。`crs` を書かない（RFC 7946）。
- `properties`: ゾーンは `"peak_lat":<lat_text>,"peak_lon":<lon_text>,"feature_type":"<種類>","area_complete":<true|false>` の後に、点と線は `"peak_lat":<lat_text>,"peak_lon":<lon_text>,"feature_type":"<種類>"` の後に、[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の表のスタイルの属性を、表の順に書く。数は文字列をそのまま書く（`peak_lat`・`peak_lon` は per-mesh CSV と同じ 8 桁の文字列。スタイルの数は表の字句どおり `2`・`1`・`0.3`・`5`・`6`）。色と `CircleMarker` は `"` で囲む（エスケープの要る字は無い）。
- `geometry`: Polygon は `{"type":"Polygon","coordinates":[<外周>,<穴>...]}`、MultiPolygon は `{"type":"MultiPolygon","coordinates":[[<外周>,<穴>...],...]}`、環は `[[<lon>,<lat>],...]`。LineString は `{"type":"LineString","coordinates":[[<ピークの lon>,<lat>],[<コルの lon>,<lat>]]}`、Point は `{"type":"Point","coordinates":[<lon>,<lat>]}`。座標は [経度, 緯度] の順で、文字列をそのまま書く。ピークは `lat_text`・`lon_text`、コルは `format_coord(col_lat)`・`format_coord(col_lon)`（6.7 の `write_peak_csv` が CSV に書いた文字列と同じ）。

#### 6.8.4 メッセージ文面

書き方は [2.2](#22-ログとメッセージの文面)。`{path}`・`{reason}` は 6.8.3 のとおり、`{dir}` は `csv_dir`。

`ERROR:` のメッセージ（2 行目は `対処:` と空白 1 つの後）:

| 記号 | 場面 | 1 行目 | 2 行目 | 終了コード |
|---|---|---|---|---|
| ZW1 | per-mesh ピーク候補 GeoJSON を書けない | `per-mesh ピーク候補 GeoJSON を書けない: {path}: {reason}` | `{dir} の空きと権限を確かめてから、止まったコマンドを同じ引数で起動し直す（それより前のメッシュの出力は残っていて、起動し直すと書き直す）` | 1 |

- ZW1 は `write_zone_geojson` が出す（呼ぶ側の 6.11 は出さない）。
- 2 行目の後半は、[6.9.4](#694-メッセージ文面) の `{rerun}` の通常解析の文と同じ（GeoJSON は通常モードだけなので、広域の案内は要らない）。

#### 6.8.5 UT 候補

すべて自動。GoogleTest のケースごとに `// trace: UT-analyze_terrain_zone-NN` を付ける。期待値は、2026-10-30 に CPython 3 の `f'{x:.8f}'` と 2.4 の式で求めた（[テスト方針書 3.3](02_test_policy.md#33-期待値の根拠)）。同じ角の文字列は `std::to_chars` でも同じになることを、C++ のプログラムで確かめた。ID の列の `01` などは、`UT-analyze_terrain_zone-01` のことである。共通の準備は 5 つ。

- **同じプロセス**: [6.9.5](#695-ut-候補) の同じ名前の準備と同じ（`write_meshset` を `write_zone_geojson` に読み替える。`csv_dir` は一時のディレクトリの下に作ったディレクトリの絶対パス）。
- **子のプロセス（書けない）**: 6.9.5 の同じ名前の準備と同じ（`write_meshset` を `write_zone_geojson` に読み替える）。
- **子のプロセス**: [6.12.5](#6125-ut-候補) の同じ名前の準備と同じ（[6.4.5](#645-ut-候補) の UT 21 と同じ形）。
- **基本の範囲**: `meshes = {5235}`、`z14 = false`、`box.x_min = 28671`、`box.x_max = 28672`、`box.y_min = 12979`、`box.y_max = 12979`、`box.bbox = mesh_to_latlon("5235")`、`picks` は空。W = 514、H = 258。グリッドの画素 (px, py) の中心のメッシュは、px 0〜256 が `5234`、px 257〜513 が `5235`。グリッドの角 (cx, cy) は Z15 の角 (7339775 + cx, 3322623 + cy)。**広い bbox** は、基本の範囲の `box.bbox` を `{south: 34.666666666666664, west: 134.0, north: 35.333333333333336, east: 136.0}`（`5234` と `5235` を囲む矩形）にしたもの。
- **小さいグリッド**: `ElevationGrid` の W = 514・H = 258、`values` を W × H 個の `0.0f` で作ってから、ケースが挙げた画素の値を書く。印は `(514 × 258 + 63) / 64` 個の 0。画素の番号は `py × 514 + px`。ケースの行（`PeakCsvRow`）は、書いた欄のほかは既定の値（`lat_text`・`lon_text` は `34.99952318`・`135.00184536` など空でない文字列。`fill_zone` は読まない）。行の `row.peak` はケースのピークの画素、`peak_elevation` はその画素の値と同じ（UT 03 の (e) は 200）。設定は `activation_zone_drop_m` 25、`delete_zone_max_drop_m` 250。

期待の形の書き方: 塗った画素は、番号を昇順に並べた集合で比べる（並びの順は比べない。先頭がピークの画素であることは比べる）。環は角 (cx, cy) の並びで書き、テストは各角を `format_coord(tile_to_latlon(7339775 + cx, 3322623 + cy, 23).lat)`・同じく `.lon` の文字列にして比べる（6.10・6.7 の関数は、それぞれの節の UT で確かめてある）。

| ID | 確かめること | 準備 | 入力 | 期待 |
|---|---|---|---|---|
| `UT-analyze_terrain_zone-01` | アクティベーションゾーンの閾値、8 近傍、陸地 | 同じプロセス。基本の範囲。小さいグリッド: (300,100)=1000、(301,100)=975、(302,100)=974.99f、(299,101)=980、(298,102)=990、(297,103)=990、(299,99)=-9999、(295,105)=990（(296,104) は 0） | `fill_zone`（行のピーク (300,100)、`peak_elevation` 1000、`kind` Activation） | 塗った画素は (300,100)・(301,100)・(299,101)・(298,102)・(297,103)、先頭は (300,100)。閾値の条件は `{97500, false}`。印はすべて 0 |
| `UT-analyze_terrain_zone-02` | 範囲で止まる | 同じプロセス。基本の範囲。小さいグリッド: (257,50)・(258,50)・(256,50)・(255,50) が 500 | `fill_zone`（ピーク (258,50)、500、Activation） | 塗った画素は (258,50)・(257,50) だけ（(256,50) は `5234` で範囲の外） |
| `UT-analyze_terrain_zone-03` | delete判定ゾーンの閾値 | 同じプロセス。基本の範囲。ピーク (300,100)=1000。ケースごとの小さいグリッドと行 | (a) 真・コル 800、(301,100)=800・(299,100)=800.01f。(b) 真・コル 700、(301,100)=750・(299,100)=749.99f。(c) 偽（コル 0）、(b) と同じ画素。(d) 真・コル 750、(301,100)=750・(299,100)=750.01f。(e) 真・コル 0（海面確定）、ピーク (300,100)=200、(301,100)=0.01f。どれも `kind` Delete | (a) `{80000, true}`、塗るのは (300,100)・(299,100)。(b) `{75000, false}`、(300,100)・(301,100)。(c) (b) と同じ。(d) `{75000, true}`、(300,100)・(299,100)。(e) `{0, true}`、(300,100)・(301,100) |
| `UT-analyze_terrain_zone-04` | ピークの画素は必ず塗る | 同じプロセス。基本の範囲。小さいグリッド: (300,100)=500、(301,100)=500 | `fill_zone`（ピーク (300,100)、500、真・コル 500〈プロミネンス 0〉、Delete） | 閾値の条件 `{50000, true}`、塗った画素は (300,100) だけ |
| `UT-analyze_terrain_zone-05` | 印を使い回す | 同じプロセス。UT 01 のグリッド | 同じ印で UT 01 の呼び出しを 2 回 | 2 回とも UT 01 と同じ結果。2 回目の後も印はすべて 0 |
| `UT-analyze_terrain_zone-06` | `fill_zone` の呼ぶ側の誤り | 同じプロセス。UT 01 の準備を基本にし、1 つだけ替える | (a) `z14` が真、(b) `grid.width` が 513、(c) `values` が 1 つ少ない、(d) 印が 1 つ少ない、(e) ピークが (0,100)、(f) ピークの値が 0、(g) `peak_elevation` が 999、(h) ピークが (100,100)（`5234`。値は 1000 にする） | どれも `std::invalid_argument`。標準エラー出力に何も出ない |
| `UT-analyze_terrain_zone-07` | 範囲の中で完結 | 同じプロセス。基本の範囲。小さいグリッド: (300,100)=1000 | `judge_area_complete`（塗った画素 {(300,100)}、`{97500, false}`、日本 {5234, 5235}、除外 {}） | `true` |
| `UT-analyze_terrain_zone-08` | 人工ボーダー | 同じプロセス。基本の範囲。小さいグリッド: (512,100)=1000 | 塗った画素 {(512,100)}、ほかは UT 07 と同じ | `false`（(513, *) は外周） |
| `UT-analyze_terrain_zone-09` | はみ出し | 同じプロセス。基本の範囲。小さいグリッド: (257,100)=1000 と、(256,99)・(256,100)・(256,101) にケースの値 | 塗った画素 {(257,100)}。(a) 値 600、閾値 `{50000, false}`、日本 {5234, 5235}、除外 {}。(b) 値 400。(c) 値 0。(d) 値 -9999。(e) 値 600、日本 {5235}。(f) 値 600、除外 {5234}。(g) 値 600、閾値 `{60000, true}`。(h) 値 600.01f、閾値 `{60000, true}` | (a) `false`、(b)〜(g) `true`、(h) `false` |
| `UT-analyze_terrain_zone-10` | NODATA で埋めた範囲 | 同じプロセス。広い bbox。小さいグリッド: (257,100)=1000、(256,99)〜(256,101)=-9999 | 塗った画素 {(257,100)}、閾値 `{50000, false}`。(a) 日本 {5234, 5235}、除外 {}。(b) 日本 {5235}。(c) 除外 {5234}。(d) (a) で (256,100) の値を 400 にする | (a) `false`、(b)(c) `true`、(d) `false`（bounding box の中は値を見ない） |
| `UT-analyze_terrain_zone-11` | `judge_area_complete` の呼ぶ側の誤り | 同じプロセス。UT 07 を基本にし、1 つだけ替える | (a) `z14` が真、(b) `grid.height` が 257、(c) 塗った画素が空、(d) 番号が W × H、(e) 塗った画素の先頭が (100,100)、(f) 塗った画素が {(300,100), (513,100)}（外周） | どれも `std::invalid_argument` |
| `UT-analyze_terrain_zone-12` | 1 画素と L の形（一直線の頂点を除く） | 同じプロセス。基本の範囲 | `trace_outline` に (a) {(300,100)}、(b) {(300,100), (301,100), (302,100), (300,101)} | (a) Polygon 1 つ、外周 (300,100)・(300,101)・(301,101)・(301,100)・(300,100)、穴なし。(b) 外周 (300,100)・(300,102)・(301,102)・(301,101)・(303,101)・(303,100)・(300,100) |
| `UT-analyze_terrain_zone-13` | 穴 | 同じプロセス。基本の範囲 | (300〜302, 100〜102) の 9 画素から (301,101) を除いた 8 画素 | Polygon 1 つ。外周 (300,100)・(300,103)・(303,103)・(303,100)・(300,100)。穴 1 つ (301,101)・(302,101)・(302,102)・(301,102)・(301,101) |
| `UT-analyze_terrain_zone-14` | 斜めにだけ接する（MultiPolygon） | 同じプロセス。基本の範囲 | {(300,100), (301,101)} | Polygon 2 つがこの順: (300,100)・(300,101)・(301,101)・(301,100)・(300,100) と、(301,101)・(301,102)・(302,102)・(302,101)・(301,101) |
| `UT-analyze_terrain_zone-15` | 環を分ける（穴が外周に 1 つの角で接する）と角の文字列 | 同じプロセス。基本の範囲 | (a) {(300,100), (301,100), (302,100), (300,101), (302,101), (300,102), (301,102)}。(b) {(257,86)} | (a) Polygon 1 つ。外周 (300,100)・(300,103)・(302,103)・(302,102)・(303,102)・(303,100)・(300,100)。穴 (301,101)・(302,101)・(302,102)・(301,102)・(301,101)。(b) 外周の最初の頂点が `35.00001534`・`135.00000000`、3 つ目（南東の角 (258,87)）が `34.99998019`・`135.00004292`（2.4 の `tile_to_latlon` から求めた字句。テストに文字列で書く） |
| `UT-analyze_terrain_zone-16` | 入れ子と最も内側の外周 | 同じプロセス。基本の範囲 | 枠: px か py が端の (300〜306, 100〜106) の 24 画素。島: px か py が端の (302〜304, 102〜104) の 8 画素 | Polygon 2 つがこの順。1 つ目: 外周 (300,100)・(300,107)・(307,107)・(307,100)・(300,100)、穴 (301,101)・(306,101)・(306,106)・(301,106)・(301,101)。2 つ目: 外周 (302,102)・(302,105)・(305,105)・(305,102)・(302,102)、穴 (303,103)・(304,103)・(304,104)・(303,104)・(303,103) |
| `UT-analyze_terrain_zone-17` | Polygon と穴の並び | 同じプロセス。基本の範囲 | (a) {(310,100), (305,100), (300,101)}。(b) (300〜304, 100〜103) の 20 画素から (303,101) と (301,102) を除いた 18 画素 | (a) Polygon 3 つが (305,100)、(310,100)、(300,101) を始まりにする順。(b) Polygon 1 つ、外周 (300,100)・(300,104)・(305,104)・(305,100)・(300,100)、穴 2 つがこの順: (303,101)・(304,101)・(304,102)・(303,102)・(303,101) と、(301,102)・(302,102)・(302,103)・(301,103)・(301,102) |
| `UT-analyze_terrain_zone-18` | 乱数の塗り（[DEC71](30_HLD.md#4164-設計判断)「輪郭は塗った画素の境界をたどる」の確かめ） | 同じプロセス。基本の範囲。`std::mt19937`（種 20261030）で 500 件: 1 辺 n を 4〜14、確率 p を 0.35〜0.75 で選び、(300, 100) を北西の隅とする n × n の窓の外周を除く画素を確率 p で陸地にし、陸地からランダムに 1 画素を選んで 8 近傍でつながる陸地を集める（テストのコードで集める）。陸地が 1 つも無ければ、その件は数えずに n・p から引き直す（500 件は `trace_outline` に渡した件の数）。乱数の引き方の細部（分布の型と呼ぶ順）はテストが決めてよい（期待は性質だけで、件の中身に依らない） | 集めた画素の番号の並びを `trace_outline` に | 各件で: (1) どの環も最初と最後が同じで、それ以外に同じ頂点が無い。(2) 頂点の文字列を角に戻し（`gx = round((lon + 180) / 360 × 2²³)`、`gy = round((1 − ln(tan(r) + 1 / cos(r)) / π) / 2 × 2²³)`、`r = lat × π / 180`）、外周の 7 の `A` が正、穴が負。(3) 外周の `A` と穴の `A`（負）の和が画素の数の 2 倍。角は `cx = gx − 7339775`、`cy = gy − 3322623`。(4) 窓のすべての画素の中心について、Polygon のどれかの内側（外周の内側で、その穴のどれの内側でもない。内外は中心から東への半直線と縦の辺の交わりの数の偶奇）であることと、集めた画素であることが一致 |
| `UT-analyze_terrain_zone-19` | `trace_outline` の呼ぶ側の誤り | 同じプロセス。基本の範囲 | (a) `z14` が真、(b) 空、(c) 番号が W × H、(d) 番号が -1、(e) 同じ番号が 2 つ | どれも `std::invalid_argument` |
| `UT-analyze_terrain_zone-20` | GeoJSON を書く | 同じプロセス | `analysis_id` `3-5235`。行と環は下の「UT 20 の入力」 | `<csv_dir>/3-5235.geojson` の中身が下の「UT 20 の期待」とバイト列で等しい。`.tmp` が無い。標準エラー出力に何も出ない |
| `UT-analyze_terrain_zone-21` | 0 行 | 同じプロセス | 行もゾーンも空、`analysis_id` `3-5235` | 中身が `{"type":"FeatureCollection","features":[\n]}\n` |
| `UT-analyze_terrain_zone-22` | 置き換える | 同じプロセス。`3-5235.geojson` に `old`、`3-5235.geojson.tmp` に 1000 バイトの `x` を置く | UT 20 の入力 | UT 20 と同じ中身。`.tmp` が無い |
| `UT-analyze_terrain_zone-23` | 置き場が無い | 同じプロセス。`csv_dir` は存在しないパス | UT 21 の入力 | `code` 1。`ERROR: per-mesh ピーク候補 GeoJSON を書けない: <csv_dir>/3-5235.geojson: No such file or directory` と `対処: <csv_dir> の空きと権限を確かめてから、止まったコマンドを同じ引数で起動し直す（それより前のメッシュの出力は残っていて、起動し直すと書き直す）` |
| `UT-analyze_terrain_zone-24` | 置き換えに失敗する | 同じプロセス。`3-5235.geojson` という名前の空のディレクトリ | UT 20 の入力 | `code` 1 の ZW1（`Is a directory`）。`.tmp` が無い。ディレクトリは残る |
| `UT-analyze_terrain_zone-25` | 書く途中で失敗する | 子のプロセス（書けない）。親が `3-5235.geojson` に `old` を置く。上限は (a) 0、(b) 5 | 子で UT 20 の入力 | (a)(b) とも子の終了コード 1、標準エラー出力が ZW1（`File too large`）の 2 行。`3-5235.geojson` の中身は `old` のまま。`.tmp` が無い |
| `UT-analyze_terrain_zone-26` | `write_zone_geojson` の呼ぶ側の誤り | 同じプロセス。UT 20 の入力を基本にし、1 つだけ替える | (a) `csv_dir` が空、(b) 末尾が `/`、(c) `analysis_id` が `4-5439-NW`、(d) `3-523`、(e) ゾーンが 1 つ少ない、(f) 1 行目の `lat_text` が空、(g) 1 行目の `col_lon` が NaN、(h) 2 行目の `activation_zone` が空、(i) 1 行目の delete判定ゾーンの外周の頂点が 3 つ、(j) 同じ外周の最後の頂点が最初と違う | どれも `std::invalid_argument`。標準エラー出力に何も出ない。`csv_dir` の下にファイルができない（(a)(b) を除く） |
| `UT-analyze_terrain_zone-27` | シグナルで止まる | 子のプロセス。小さいグリッドは UT 01 と同じ。子は 4 つ（関数ごと） | 子の中で `start_log` の後に、`kill(getpid(), SIGTERM)` の後で、(a) UT 01 の `fill_zone`、(b) UT 07 の `judge_area_complete`、(c) UT 12 の (a) の `trace_outline`、(d) UT 20 の入力の `write_zone_geojson` | どれも `ExitRequest` の `code` が 143（数えが 0 の区切りの `check_signal`）。子の終了コードが 143。(d) は `csv_dir` に `3-5235.geojson` も `.tmp` もできない（区切りが書き出しより前にある） |

- UT 27 のあとに: 途中の区切り（数えが 2²⁰ の倍数のとき）は、前もって送ったシグナルを入り口の区切りが必ず先に受けるので、UT から決まった点で受けさせられない。時間に頼る試験は不安定なので置かず、区切りの置き場はコードの読み合わせで確かめる（6.6.5 の UT 15 も入り口で止まることを確かめる形）。

UT 20 の入力（行は 3 つ。`PeakColRow` の書かない欄は既定の値）:

- 行 1: `lat_text` `34.99999777`、`lon_text` `135.00002146`、`key_col_resolved` 真、`col_lat` 35.01234567891、`col_lon` 135.1。
- 行 2: `36.00465613`・`139.99880075`、偽、`col_lat`・`col_lon` 0.0。
- 行 3: `34.99999777`・`135.00006437`、真、`col_lat`・`col_lon` 0.0（海面確定）。
- 環（頂点は（緯度, 経度）の文字列）: A = (`35.1`,`135.1`)・(`35.0`,`135.1`)・(`35.0`,`135.2`)・(`35.1`,`135.2`)・(`35.1`,`135.1`)。B = (`35.3`,`135.3`)・(`35.2`,`135.3`)・(`35.2`,`135.4`)・(`35.3`,`135.4`)・(`35.3`,`135.3`)。H = (`35.08`,`135.12`)・(`35.08`,`135.18`)・(`35.02`,`135.18`)・(`35.02`,`135.12`)・(`35.08`,`135.12`)。
- ゾーン: 行 1 は delete が [{A, [H]}]・真、activation が [{A}]・真。行 2 は delete が [{A}, {B}]・偽、activation が [{B}]・真。行 3 は delete が [{B}]・真、activation が [{A}]・偽。

UT 20 の期待（13 行。各行は `\n` で終わる）:

```text
{"type":"FeatureCollection","features":[
{"type":"Feature","properties":{"peak_lat":34.99999777,"peak_lon":135.00002146,"feature_type":"delete_zone","area_complete":true,"_color":"#ef6c00","_weight":2,"_opacity":1,"_fill":false},"geometry":{"type":"Polygon","coordinates":[[[135.1,35.1],[135.1,35.0],[135.2,35.0],[135.2,35.1],[135.1,35.1]],[[135.12,35.08],[135.18,35.08],[135.18,35.02],[135.12,35.02],[135.12,35.08]]]}},
{"type":"Feature","properties":{"peak_lat":36.00465613,"peak_lon":139.99880075,"feature_type":"delete_zone","area_complete":false,"_color":"#ef6c00","_weight":2,"_opacity":1,"_fill":false},"geometry":{"type":"MultiPolygon","coordinates":[[[[135.1,35.1],[135.1,35.0],[135.2,35.0],[135.2,35.1],[135.1,35.1]]],[[[135.3,35.3],[135.3,35.2],[135.4,35.2],[135.4,35.3],[135.3,35.3]]]]}},
{"type":"Feature","properties":{"peak_lat":34.99999777,"peak_lon":135.00006437,"feature_type":"delete_zone","area_complete":true,"_color":"#ef6c00","_weight":2,"_opacity":1,"_fill":false},"geometry":{"type":"Polygon","coordinates":[[[135.3,35.3],[135.3,35.2],[135.4,35.2],[135.4,35.3],[135.3,35.3]]]}},
{"type":"Feature","properties":{"peak_lat":34.99999777,"peak_lon":135.00002146,"feature_type":"activation_zone","area_complete":true,"_color":"#2e7d32","_weight":1,"_opacity":1,"_fillColor":"#2e7d32","_fillOpacity":0.3},"geometry":{"type":"Polygon","coordinates":[[[135.1,35.1],[135.1,35.0],[135.2,35.0],[135.2,35.1],[135.1,35.1]]]}},
{"type":"Feature","properties":{"peak_lat":36.00465613,"peak_lon":139.99880075,"feature_type":"activation_zone","area_complete":true,"_color":"#2e7d32","_weight":1,"_opacity":1,"_fillColor":"#2e7d32","_fillOpacity":0.3},"geometry":{"type":"Polygon","coordinates":[[[135.3,35.3],[135.3,35.2],[135.4,35.2],[135.4,35.3],[135.3,35.3]]]}},
{"type":"Feature","properties":{"peak_lat":34.99999777,"peak_lon":135.00006437,"feature_type":"activation_zone","area_complete":false,"_color":"#2e7d32","_weight":1,"_opacity":1,"_fillColor":"#2e7d32","_fillOpacity":0.3},"geometry":{"type":"Polygon","coordinates":[[[135.1,35.1],[135.1,35.0],[135.2,35.0],[135.2,35.1],[135.1,35.1]]]}},
{"type":"Feature","properties":{"peak_lat":34.99999777,"peak_lon":135.00002146,"feature_type":"peak_col_link","_color":"#616161","_weight":2,"_opacity":1},"geometry":{"type":"LineString","coordinates":[[135.00002146,34.99999777],[135.10000000,35.01234568]]}},
{"type":"Feature","properties":{"peak_lat":34.99999777,"peak_lon":135.00002146,"feature_type":"key_col","_markerType":"CircleMarker","_radius":5,"_color":"#ffffff","_weight":1,"_opacity":1,"_fillColor":"#1565c0","_fillOpacity":1},"geometry":{"type":"Point","coordinates":[135.10000000,35.01234568]}},
{"type":"Feature","properties":{"peak_lat":34.99999777,"peak_lon":135.00002146,"feature_type":"peak","_markerType":"CircleMarker","_radius":6,"_color":"#ffffff","_weight":1,"_opacity":1,"_fillColor":"#d32f2f","_fillOpacity":1},"geometry":{"type":"Point","coordinates":[135.00002146,34.99999777]}},
{"type":"Feature","properties":{"peak_lat":36.00465613,"peak_lon":139.99880075,"feature_type":"peak","_markerType":"CircleMarker","_radius":6,"_color":"#ffffff","_weight":1,"_opacity":1,"_fillColor":"#d32f2f","_fillOpacity":1},"geometry":{"type":"Point","coordinates":[139.99880075,36.00465613]}},
{"type":"Feature","properties":{"peak_lat":34.99999777,"peak_lon":135.00006437,"feature_type":"peak","_markerType":"CircleMarker","_radius":6,"_color":"#ffffff","_weight":1,"_opacity":1,"_fillColor":"#d32f2f","_fillOpacity":1},"geometry":{"type":"Point","coordinates":[135.00006437,34.99999777]}}
]}
```

- 書いた GeoJSON を CMP5 の `merge_zones` が読むケースと、6.7 の `filter_peak_rows` から 6.8 の 4 関数をつなぐケース（通常モードの 1 メッシュで、CSV と GeoJSON のピークの文字列が同じこと）は、複数のモジュールの関数のつながりを確かめるので、6.11 の UT 候補と結合テスト（IT）に置く（[ADR-LLD-001](decisions/ADR-LLD-001-lld-format-module-granularity-and-t2-timing.md) の Decision 2。6.11 を書くときに足し、6.8 からそのケースを指す）。ここでは、出力のバイト列（UT 20）で、`merge_zones` が受ける形を確かめる。

### 6.9 `analyze_terrain_record`

- **ID**: LLD-analyze_terrain_record
- **対応 HLD**: [3.4](30_HLD.md#34-cmp4-地形解析エンジン)・[4.4](30_HLD.md#44-fr-004-33メッシュ結合解析オーケストレーション)・[4.14](30_HLD.md#414-fr-014-広域結合解析オーケストレーション)
- **ファイル**: `src/record.hpp`・`src/record.cpp`

関数の名前と役割は [HLD 3.4.3](30_HLD.md#343-関数) の表の「出力の記録」の群で、処理の正本は [HLD 4.4.2](30_HLD.md#442-処理の流れ) の 4「対象メッシュごとに、昇順に次を行う」の 9（通常モード）と、[4.14.2](30_HLD.md#4142-処理の流れ) の 4「対象メッシュごとに、昇順に次を行う」の 2 の 9（広域モード）、`.meshset` の形式は [4.4.2](30_HLD.md#442-処理の流れ) の「`.meshset` の形式」、書き込みの失敗は [2.5.5](30_HLD.md#255-書き込みの失敗) と、[4.4.3](30_HLD.md#443-異常系)・[4.14.3](30_HLD.md#4143-異常系) の「出力の書き込みに失敗する」の行である。置き場の名前と一時ファイルの書き方は [2.3](#23-ファイルの名前と書き方) で決まっている。書いた `.meshset` を読むのは [6.3](#63-analyze_terrain_window) の `read_meshset` と `is_pattern_covered` である。関数を呼ぶ順は 6.11 の `run_normal_mode`（メッシュごとの最後）・`run_wide_mode`（パターンごとに `write_peak_csv` の後。[HLD 3.4.3](30_HLD.md#343-関数) の呼ぶ順）で、6.9 は渡された集合と解析識別子とパスを受け取る。この節は、それを C++ で書くための細部を足す。1.2 の C++ の規約に従う。

#### 6.9.1 ファイル割付

- 公開の宣言は `src/record.hpp`、定義と内部の関数は `src/record.cpp` に置く。どちらも先頭のコメントに `// trace: LLD-analyze_terrain_record` を書き、ヘッダーは次の行を `#pragma once` にする。
- `src/record.hpp` は `<set>`・`<string>` を読む。`src/record.cpp` は `"record.hpp"`・`"common.hpp"`・`<cerrno>`・`<cstdio>`・`<cstring>`・`<fcntl.h>`・`<stdexcept>`・`<string>`・`<unistd.h>` を読む。OpenCV のヘッダーは読まない。
- UT のコードは `tests/src/test_record.cpp` に置き、`build/test_record` にビルドする（[2.5](#25-ビルドとテストの名前)。`src/` の `main` を持たない `.cpp` をすべてリンクするので、`common.cpp` も入る）。各テストに `// trace: UT-analyze_terrain_record-NN`（確かめる UT 候補の ID）のコメントを付ける。テストの枠組みは GoogleTest（[テスト方針書 3.4](02_test_policy.md#34-テストを先に書く進め方)）。

#### 6.9.2 型とデータ

`src/record.hpp` の公開の宣言は次のとおり（名前空間に入れない。1.2 の C++ の規約）。

```cpp
#pragma once
#include <set>
#include <string>

void write_meshset(const std::set<std::string>& meshes, const std::string& analysis_id,
                   const std::string& csv_dir);
```

- 引数の並びは [HLD 3.4.3](30_HLD.md#343-関数) の表の受け取るものの順。`meshes` は解析対象メッシュの集合（6.2・6.3 と同じ `std::set<std::string>`。4 バイトの ASCII の数字で、昇順はコードの数の昇順）。`analysis_id` は解析識別子（通常解析は `3-<4 桁の数字>`、広域解析は `<4・5・6 のどれか>-<4 桁の数字>-<NW・NE・SW・SE のどれか>`。[FR-007](20_SRS.md#fr-007-per-mesh-csv-出力プロミネンス閾値適用) の命名）。`csv_dir` は `data_dir` の下の `results/csv` の絶対パスで、末尾に `/` を付けない（6.3 と同じ。6.11 が組み立てて渡す）。
- 内部（`src/record.cpp` の無名の名前空間）は、`bool _write_all(int fd, const std::string& s)` だけ（[6.12.3](#6123-関数の細部) の内部の `_write_all` と同じ形: `write` を、全部書くか `EINTR` のほかの失敗まで繰り返す。失敗したら `false` を返し、`errno` を残す）。6.12 の内部の関数はほかの `.cpp` から呼べないので、同じ形を置く。

#### 6.9.3 関数の細部

処理の正本は上の前置きのとおりで、この節は C++ で書くための細部を足す。`check_signal` を呼ばない（[HLD 3.4.3](30_HLD.md#343-関数) の `check_signal` を呼ぶ群に「出力の記録」は入っていない。数十行を書くだけで、時間がかからない）。止まるときは、メッセージを `log_error` で出してから `throw ExitRequest(EXIT_ERROR)` する（1.2 の C++ の規約）。呼ぶ側の誤りは `std::invalid_argument` を投げる（6.2・6.3・6.10・6.12 と同じ）。通常のログと警告は出さない。

#### `write_meshset`

1. 引数を次の順に確かめ、最初に当たったもので `std::invalid_argument` を投げる（ファイルに触れる前に確かめる）。
   - `csv_dir` が空か、最後のバイトが `/`: `write_meshset: csv_dir が空か / で終わる: <値>`。
   - `analysis_id` が、`3` と `-` と 4 バイトの ASCII の数字（合わせて 6 バイト）でも、`4`・`5`・`6` のどれか 1 字と `-` と 4 バイトの ASCII の数字と `-` と `NW`・`NE`・`SW`・`SE` のどれか（合わせて 9 バイト）でもない（バイト列で比べる。大文字だけ）: `write_meshset: analysis_id が解析識別子の形でない: <値>`。解析識別子はファイル名になり、6.3 の `is_pattern_covered` が選ぶ名前（`3-<4 桁>.meshset` と `<4・5・6>-<対象メッシュ>-<コーナー>.meshset`）と、MW1 の 2 行目の案内を先頭の 1 字で決めるため、形の崩れた値で書かない。
   - `meshes` が空: `write_meshset: meshes が空`（通常の対象メッシュも広域の対象メッシュも解析対象メッシュに入るので、空は呼ぶ側の誤り）。
   - `meshes` を昇順に見て、4 バイトの ASCII の数字でないコードがある: `write_meshset: meshes のコードが 4 桁の数字でない: <値>`（6.10 の `mesh_to_latlon` と同じ判定。日本全土1次メッシュコードリストにあるかは見ない）。
2. 中身を作る。`meshes` を集合の順（昇順）に、コードと `\n` を続けて 1 つの `std::string` にする（見出し・注釈・BOM・CR・空行を書かない。[HLD 4.4.2](30_HLD.md#442-処理の流れ) の「`.meshset` の形式」。6.3 の `read_meshset` がそのまま受ける形）。
3. パスを決める。`path = csv_dir + "/" + analysis_id + ".meshset"`、一時ファイル `tmp = path + ".tmp"`（[2.3](#23-ファイルの名前と書き方) の一時ファイルの決まり）。一時ファイルに書いてから置き換えるのは、途中で止まっても、書きかけの `.meshset` が本来の名前で残らないようにするため。
4. 書く。2.3 の一時ファイルの決まりの「書く（C++）」で、`tmp` に 2 の中身を書く（`_write_all` を使う）。開く・書く・`fsync`・`close` のどれで失敗しても、2.3 のとおり後始末をしてから、MW1（`{reason}` は控えた `errno` の `std::strerror`）を出して止まる。
5. 置き換える。2.3 の「置き換える（C++）」で `rename(tmp, path)` を呼ぶ。失敗したら、`errno` を控え、`unlink(tmp)`（失敗は無視する）してから、MW1 を出して止まる（置き換えに失敗したときに一時ファイルを消すかは節で決めるとある。6.9 は消す）。
6. 戻る。`path` が書き終えた中身か、前の起動が書いた中身のどちらかになる。書けずに止まったときは、前の起動の `.meshset` を消さない（同じ解析識別子の `.meshset` は、起動し直せば同じメッシュかパターンで書き直す。[HLD 4.4.2](30_HLD.md#442-処理の流れ) の 5「終了コード 0 で終わる」・[4.14.2](30_HLD.md#4142-処理の流れ) の 5「終了コード 0 で終わる」の、それより前の出力は残すとする決まりも、古いものを消すとはしていない）。

- MW1 の `{path}` は、どの段で失敗しても `path`（一時ファイルでなく本来の名前）。
- ディレクトリを作らない。`csv_dir` が無ければ、`open` が `ENOENT` で失敗して MW1 になる。`results/csv` を作る関数は [HLD 3.4.3](30_HLD.md#343-関数) の表に無いので、6.9 は作らない（作るのは 6.11。[6.7.3](#673-関数の細部) の `write_peak_csv` も作らない）。ディレクトリの `fsync` はしない（2.3 の Python の書き方と同じ）。

#### 6.9.4 メッセージ文面

書き方は [2.2](#22-ログとメッセージの文面)。`{path}`・`{reason}` は 6.9.3 のとおり、`{dir}` は `csv_dir`、`{rerun}` は表の後に書く。

`ERROR:` のメッセージ（2 行目は `対処:` と空白 1 つの後）:

| 記号 | 場面 | 1 行目 | 2 行目 | 終了コード |
|---|---|---|---|---|
| MW1 | `.meshset` を書けない | `.meshset を書けない: {path}: {reason}` | `{dir} の空きと権限を確かめてから、{rerun}` | 1 |

- MW1 は `write_meshset` が出す（呼ぶ側の 6.11 は出さない）。
- `{rerun}`: `analysis_id` の先頭の 1 字が `3` なら（通常解析）`止まったコマンドを同じ引数で起動し直す（それより前のメッシュの出力は残っていて、起動し直すと書き直す）`。`4`・`5`・`6` なら（広域解析）`scripts/run_pipeline.sh --phase 3 --n {n} を起動し直す（設定ファイルを指定して起動したときは、同じ --config を付ける）`（`{n}` は先頭の 1 字）。[HLD 2.5.5](30_HLD.md#255-書き込みの失敗) は書き込みの失敗の終了コードだけを決め、案内の文面は決めていない。通常解析は、通しの起動でも `--phase 2` でも `--mesh` を付けた起動でも止まりうるが、関数には起動の仕方が分からないので、止まった起動と同じ引数で起動し直す形にする。広域解析は、6.3 の MS1〜MS3 と同じく、フェーズ 3 の `--n` を指す。括弧の「設定ファイルを…」は、関数が設定ファイルの指定の有無を知らないので、いつでもそのまま書く（6.3 の MS3 と同じ）。

#### 6.9.5 UT 候補

すべて自動。GoogleTest のケースごとに `// trace: UT-analyze_terrain_record-NN` を付ける。共通の準備は 2 つ。

- **同じプロセス**: 6.3.5 の「同じプロセス」と同じ（`mkdtemp` で一時のディレクトリを作り、`csv_dir` はその下に作ったディレクトリの絶対パス。ファイルの中身はバイト列で読んで比べる。標準エラー出力は記述子 2 の付け替えで捕まえる。止まるケースは `ExitRequest` を捕まえて `code` を確かめ、メッセージの期待は標準エラー出力の 2 行の全文）。
- **子のプロセス（書けない）**: 親が `csv_dir` と、ケースが前もって置くファイルを作ってから、`std::fflush(nullptr)` の後に `fork` する。子は記述子 2 を、親が読むパイプの書く側に付け替えて元の 2 つの記述子を閉じ、`SIGXFSZ` を無視にし、`setrlimit(RLIMIT_FSIZE, ...)` の `rlim_cur` をケースの値（0 か 5）にしてから（[6.12.5](#6125-ut-候補) の「ログファイルに書けない場面」と同じ。0 なら以後のファイルへの `write` が `EFBIG`〔`File too large`〕で失敗する。5 なら最初の `write` は 5 バイトだけ書けて、書いた数を返し、続く `write` が `EFBIG` で失敗する。パイプには効かない。`rlim_max` は変えない）、`try { write_meshset(...); } catch (const ExitRequest& e) { std::_Exit(e.code); } catch (...) { std::_Exit(99); } std::_Exit(EXIT_OK);` を行う（`start_log` を呼ばないので、終わりの行も `atexit` も無い。`std::_Exit` は GoogleTest の後始末を子の中で動かさないため）。親は `fork` の後、読み始める前に、パイプの書く側を閉じる（閉じないと、子が終わっても EOF にならない）。パイプを EOF まで読み切ってから `waitpid` し、終了コードと標準エラー出力を確かめる。

| ID | 確かめること | 準備 | 入力 | 期待 |
|---|---|---|---|---|
| `UT-analyze_terrain_record-01` | 通常の `.meshset` を書く | 同じプロセス | `write_meshset({5238, 5239, 5339}, "3-5339", csv_dir)` | `<csv_dir>/3-5339.meshset` の中身が `5238\n5239\n5339\n`。`<csv_dir>/3-5339.meshset.tmp` が無い。標準エラー出力に何も出ない |
| `UT-analyze_terrain_record-02` | 広域の `.meshset` を書く | 同じプロセス | `write_meshset({5135, 5136, 5235, 5236}, "4-5135-NW", csv_dir)` | `<csv_dir>/4-5135-NW.meshset` の中身が `5135\n5136\n5235\n5236\n`。`.tmp` が無い。標準エラー出力に何も出ない |
| `UT-analyze_terrain_record-03` | 昇順で書く | 同じプロセス | `write_meshset({5340, 0099, 5339}, "3-5339", csv_dir)`（初期化子の並びをわざと崩す） | 中身が `0099\n5339\n5340\n`。標準エラー出力に何も出ない |
| `UT-analyze_terrain_record-04` | 置き換える | 同じプロセス。`<csv_dir>/3-5339.meshset` に `9999\n`、`<csv_dir>/3-5339.meshset.tmp` に `5238\n5239\n5240\n5338\n`（前の起動の残り。新しい中身より長い） | `write_meshset({5339}, "3-5339", csv_dir)` | `3-5339.meshset` の中身が `5339\n`。`.tmp` が無い。標準エラー出力に何も出ない |
| `UT-analyze_terrain_record-05` | 置き場が無い、案内の分け方 | 同じプロセス。`csv_dir` は一時のディレクトリの下の、存在しないパス | (a) `write_meshset({5339}, "3-5339", csv_dir)`、(b) `write_meshset({5135}, "5-5135-SE", csv_dir)` | どちらも `code` 1。(a) は `ERROR: .meshset を書けない: <csv_dir>/3-5339.meshset: No such file or directory` と `対処: <csv_dir> の空きと権限を確かめてから、止まったコマンドを同じ引数で起動し直す（それより前のメッシュの出力は残っていて、起動し直すと書き直す）`。(b) は 1 行目のパスが `<csv_dir>/5-5135-SE.meshset`、2 行目が `対処: <csv_dir> の空きと権限を確かめてから、scripts/run_pipeline.sh --phase 3 --n 5 を起動し直す（設定ファイルを指定して起動したときは、同じ --config を付ける）` |
| `UT-analyze_terrain_record-06` | 置き換えに失敗する | 同じプロセス。`<csv_dir>/3-5339.meshset` という名前の空のディレクトリ | `write_meshset({5339}, "3-5339", csv_dir)` | `code` 1 の MW1（`{reason}` は `Is a directory`、`{path}` は `<csv_dir>/3-5339.meshset`）。`.tmp` が無い。ディレクトリは残る |
| `UT-analyze_terrain_record-07` | 書く途中で失敗する | 子のプロセス（書けない）。親が `<csv_dir>/3-5339.meshset` に `5339\n` を置く。上限は (a) 0、(b) 5（中身 `5238\n5339\n` の 10 バイトのうち 5 バイトだけ書けて、残りで失敗する） | 子で `write_meshset({5238, 5339}, "3-5339", csv_dir)` | (a)(b) とも、子の終了コード 1。標準エラー出力が MW1（`{reason}` は `File too large`）の 2 行。`3-5339.meshset` の中身は `5339\n` のまま。`.tmp` が無い（(b) は、`write` を 1 回だけ呼んで書いた数を見ない実装を落とす） |
| `UT-analyze_terrain_record-08` | 呼ぶ側の誤り | 同じプロセス | (a) `meshes` が空、(b) `meshes` が `{5238, 5239, 5339, 53a9}`、(c) `meshes` が `{5238, 5239, 5339, 53390}`、(d) `analysis_id` が `3-533`、(e) `7-5135-NW`、(f) `4-5135`、(g) `3-5339-NW`、(h) `4-5135-nw`、(i) `csv_dir` が空、(j) `csv_dir` の末尾が `/`。ほかの引数は UT-analyze_terrain_record-01 と同じ | どれも `std::invalid_argument`。標準エラー出力に何も出ない。`csv_dir` の下にファイルができない（(i)(j) を除く） |

- 書いた `.meshset` を 6.3 の `read_meshset` で読み戻して、同じ集合になることを確かめるケースは、2 つのモジュールの関数のつながりを確かめるので、6.11 の UT 候補に置く（[ADR-LLD-001](decisions/ADR-LLD-001-lld-format-module-granularity-and-t2-timing.md) の Decision 2。6.11 を書くときに足し、6.9 からそのケースを指す）。ここでは、出力のバイト列（UT-analyze_terrain_record-01〜03）で、6.3 の `read_meshset` が受ける形を確かめる。

### 6.10 `analyze_terrain_convert`

- **ID**: LLD-analyze_terrain_convert
- **対応 HLD**: [3.4](30_HLD.md#34-cmp4-地形解析エンジン)・[4.7](30_HLD.md#47-fr-007-per-mesh-csv-出力プロミネンス閾値適用)・[5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)
- **ファイル**: `src/convert.hpp`・`src/convert.cpp`

関数の名前と役割は [HLD 3.4.3](30_HLD.md#343-関数) の表の「変換」の群で、式の正本は用語集の座標変換計算式（[メッシュコード → 緯度経度](00_GLOSSARY.md#mesh-to-latlon)・[緯度経度 → メッシュコード](00_GLOSSARY.md#latlon-to-mesh)・[緯度経度 → XYZ タイル番号](00_GLOSSARY.md#latlon-to-tile)・[XYZ タイル番号 → 緯度経度](00_GLOSSARY.md#tile-to-latlon)）である。言語をまたいで同じ値にするための計算の順とテストベクトルは [2.4](#24-言語ごとに別に実装する式のテストベクトル) に置いた（HLD の [DEC6](30_HLD.md#225-設計判断決めたこと理由却下した案)「メッシュ・タイル変換の二重実装を許容」）。`mesh_to_latlon`・`latlon_to_tile`・`tile_to_latlon` は Python の [2.1](#21-共通部品)・[3.1](#31-preprocess_boundaries) の同じ名前の関数と、`latlon_to_mesh`・`latlon_to_z15_pixel`・`z15_pixel_center_latlon` は CMP5（統合・突合）の同じ名前の関数（[HLD 3.5.3](30_HLD.md#353-関数)・[3.5.4](30_HLD.md#354-コンポーネント内の共通部品)）と、同じ表で一致を確かめる。Z15 の画素とその中心の使い方は [HLD 4.7.2](30_HLD.md#472-処理の流れ) の 2「ピークの Z15 の画素を求める」〜5「対象ピークの照合」と [DEC54](30_HLD.md#474-設計判断)「ピークの座標は Z15 の画素の中心にする」である。[HLD 5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)（再現性）は、2.4 の計算の順と [HLD 2.6.5](30_HLD.md#265-ビルド構成)のコンパイルの指定で受ける（同じ入力から、経度と整数の結果〈メッシュコード・タイル番号・画素〉はどの計算機でも同じ値になり、`sinh`・`atan` を通る緯度は 2.4 の許容差〈`1e-12` 度〉の中で一致する）。成果物の座標は、この値を [DEC54](30_HLD.md#474-設計判断)「ピークの座標は Z15 の画素の中心にする」のとおり小数点 8 桁にした文字列で、その再現性は 8 桁の丸めと出力の決まり（`format_coord`）と合わせて受ける。この節は、C++ で書くための細部だけを足す。1.2 の C++ の規約に従う。

#### 6.10.1 ファイル割付

- 公開の宣言は `src/convert.hpp`、定義は `src/convert.cpp` に置く。どちらも先頭のコメントに `// trace: LLD-analyze_terrain_convert` を書き、ヘッダーは次の行を `#pragma once` にする。
- `src/convert.hpp` は `<compare>`・`<string>` を読む。`src/convert.cpp` は `"convert.hpp"`・`<cmath>`・`<numbers>`・`<stdexcept>`・`<string>` を読む。`"common.hpp"` と OpenCV のヘッダーは読まない（ログを出さず、止まらず、画像を扱わない）。
- UT のコードは `tests/src/test_convert.cpp` に置き、`build/test_convert` にビルドする（[2.5](#25-ビルドとテストの名前)）。各テストに `// trace: UT-analyze_terrain_convert-NN`（確かめる UT 候補の ID）のコメントを付ける。2.4 の表の行を写したテストには、写した表の名前（`2.4 の表 5` など）もコメントに書く（[テスト方針書 3.3](02_test_policy.md#33-期待値の根拠)）。テストの枠組みは GoogleTest（[テスト方針書 3.4](02_test_policy.md#34-テストを先に書く進め方)）。

#### 6.10.2 型とデータ

`src/convert.hpp` の公開の宣言は次のとおり（名前空間に入れない。1.2 の C++ の規約）。

```cpp
#pragma once
#include <compare>
#include <string>

struct LatLon {
    double lat = 0.0;   // 緯度（度）
    double lon = 0.0;   // 経度（度）
};

struct MeshBounds {
    double south = 0.0; // 南端の緯度
    double west = 0.0;  // 西端の経度
    double north = 0.0; // 北端の緯度
    double east = 0.0;  // 東端の経度
};

struct TileXY {
    int x = 0;
    int y = 0;
    auto operator<=>(const TileXY&) const = default;
};

struct Z15Pixel {
    int gx = 0;   // 全球の Z15 の画素の列（西から東）
    int gy = 0;   // 全球の Z15 の画素の行（北から南）
    auto operator<=>(const Z15Pixel&) const = default;
};

MeshBounds mesh_to_latlon(const std::string& mesh);
std::string latlon_to_mesh(double lat, double lon);
TileXY latlon_to_tile(double lat, double lon, int z);
LatLon tile_to_latlon(double x, double y, int z);
Z15Pixel latlon_to_z15_pixel(double lat, double lon);
LatLon z15_pixel_center_latlon(const Z15Pixel& pixel);
```

- `MeshBounds` は 4 つの名前の付いた値にする（Python の [2.1](#21-共通部品) の `((南, 西), (北, 東))` の組の並びを、名前で取り違えないようにする。[HLD 3.4.3](30_HLD.md#343-関数) の「緯度経度 2 組」と同じ中身）。
- `TileXY`・`Z15Pixel` の比べ方（既定の `<=>`。`==` も既定で決まる）は、`std::set`・`std::map` の鍵と、一致の判定のためのもの。順は宣言の順（`x` か `gx` が先）で、出力の並び（HLD の DEC83 の gy・gx の順など）を決めるものではない。出力の並びは、並べる群の節で決める。
- メッシュコードは 6.12 と同じく `std::string`（4 バイトの ASCII の数字）。
- `Z15Pixel` を `TileXY` と分けるのは、z=23 のタイル番号と同じ値でも意味（Z15 の画素）が違い、後の群（[6.4](#64-analyze_terrain_grid) の Z14 の控え〈`GridRange::picks` の値〉、CSV と早期終了）が使うため。

#### 6.10.3 関数の細部

式と計算の順の正本は 2.4 の「計算の決まり」で、この節は C++ の書き方と、引数の範囲と、範囲の外の扱いを足す。どの関数もログを出さず、`ExitRequest` を投げず、`check_signal` を呼ばない（すぐ終わる計算だけで、[HLD 3.4.3](30_HLD.md#343-関数) の `check_signal` を呼ぶ群に「変換」は入っていない）。2.4 の「書いた順に左から計算する」は、HLD 2.6.5 のコンパイルの指定（`-ffp-contract=off`。HLD の [DEC22](30_HLD.md#266-設計判断)「再現性を崩すオプションを使わない」）の下で成り立つ（掛け算と足し算を 1 つの命令にまとめると丸めが変わるため）。`π` は `std::numbers::pi`、`2^z` は `std::ldexp(1.0, z)`（倍精度の値。2 の冪なので丸めが無い）、`floor`・`tan`・`cos`・`log`・`sinh`・`atan` は `<cmath>` の `std::` の関数を使う。

関数ごとに `#####` の見出しを立てる。2.1・3.1 と同じ名前の見出しは、重複（MD024）を避けるために `（analyze_terrain_convert）` を付ける（6.12 と同じ）。

##### mesh_to_latlon（analyze_terrain_convert）

`MeshBounds mesh_to_latlon(const std::string& mesh)`。`mesh` が 4 バイトで、どのバイトも ASCII の `0`〜`9` でなければ、`std::invalid_argument("mesh_to_latlon の引数が 4 桁の数字でない: " + mesh)` を投げる（呼ぶ側の誤り。2.1 の Python の `ValueError` に当たる。6.12 が呼ぶ側の誤りを `std::invalid_argument` にしたのと同じ。`main` は捕まえないので、6.12 の `_on_terminate` が G7 で止める）。`aa` は上 2 バイト、`bb` は下 2 バイトを 10 進の `int` にした値。`south = static_cast<double>(2 * aa) / 3.0`、`north = static_cast<double>(2 * (aa + 1)) / 3.0`、`west = static_cast<double>(100 + bb)`、`east = static_cast<double>(101 + bb)`（2.4 の決まりのとおり、`2 × aa` を整数で求めてから倍精度にし、3 で 1 回だけ割る。`(2 * aa) / 3` を整数のまま割ると整数の割り算になる）。範囲（3036〜6848）は見ない（2.1 と同じ）。

##### latlon_to_mesh

`std::string latlon_to_mesh(double lat, double lon)`。`a = std::floor((lat * 3.0) / 2.0)`、`b = std::floor(lon) - 100.0` を倍精度のまま求める（2.4 の決まり）。`a` と `b` がどちらも 0 以上 99 以下（`a >= 0.0 && a <= 99.0 && b >= 0.0 && b <= 99.0` で比べる）なら、`a` と `b` を `int` にして、それぞれ 2 桁の 10 進（1 桁なら前に `0`）でつないだ 4 バイトの文字列を返す（`(35.5, 139.5)` は `5339`）。そうでなければ空の文字列を返す（`lat` か `lon` が NaN のときは比べた結果が偽になるので空、無限大のときも空）。比べてから `int` に変えるので、どの `double` を渡しても未定義の動作にならない。

空の文字列は、どのメッシュの集合にも無いコードとして扱える。後の群の呼ぶ側（対象、[6.4](#64-analyze_terrain_grid) のタイルとグリッド、CSV と早期終了）は、返ったコードが集合にあるかを見る。空のときのメッセージは呼ぶ側の節で決める（6.2 の `group_peaks_by_mesh` は、範囲の外として UP3 に挙げる）。空の文字列は「値が無い」の印ではなく「どのメッシュの集合にも無いコード」で、呼ぶ側は有無を調べずに集合を引くだけなので、1.2 の C++ の規約の「値の有無は `bool` の印で持つ」には当たらない。範囲の外を空の文字列にするのは、コル未確定ピーク座標リストが数として読めることしか確かめない（[HLD 4.14.2](30_HLD.md#4142-処理の流れ) の 2「入力を読む」）ので、日本の外の値や NaN が来うるためで、止めるかどうかは呼ぶ側が決める（HLD の [DEC51](30_HLD.md#4144-設計判断)「対象ピークの所属メッシュが解析の対象でなければ止める」）。例外で止めると、利用者には G7（捕まらない例外）の形の誤りになる。

##### latlon_to_tile（analyze_terrain_convert）

`TileXY latlon_to_tile(double lat, double lon, int z)`。式と計算の順は 2.4 の `latlon_to_tile` のとおり。`floor` の後の倍精度の値を `static_cast<int>` で `x`・`y` にする。引数を検査しない（2.1 の Python と同じ）。

渡せるのは、`lat` が −85.0511287798066 以上 85.0511287798066 以下（Web メルカトルの緯度の限界。[HLD 4.8.2](30_HLD.md#482-処理の流れ) の 1「リストを読む」の座標として読める条件の (3) の注）、`lon` が −180 以上 180 未満（同じく (2)）、`z` が 0 以上 23 以下のときだけである。このとき `x` は 0 以上 `2^z` 以下（`lon` が 180 未満の最大の倍精度の値のときは、`lon + 180` が丸めで 360 になり `x = 2^z`）、`y` は −1 以上 `2^z − 1` 以下（緯度 +85.0511287798066 で −1、緯度 −85.0511287798066 で `2^z − 1`）に入り、`int` に変えられる。範囲の外を渡すと、`int` に変えるところで未定義の動作になりうる（−90 に最も近い倍精度の緯度では `tan(r) + 1 / cos(r)` が 0 になり、`log` が負の無限大を返す。NaN も同じ）ので、呼ぶ側が範囲を守る。今の呼ぶ側は、bounding box の四隅で呼ぶ [6.4](#64-analyze_terrain_grid) の `tile_range`（上 2 桁と下 2 桁の範囲を確かめてから呼ぶ）と、6.3 の `check_mesh_tiles`（メッシュの四隅で呼ぶ）、所属メッシュが存在メッシュだと確かめた後の対象ピークで `latlon_to_z15_pixel` を通して呼ぶ「対象」の群、読み戻した値で呼ぶ「CSV と早期終了」の群である。範囲を確かめてから渡すかは、それぞれの群の節で決める。

##### tile_to_latlon（analyze_terrain_convert）

`LatLon tile_to_latlon(double x, double y, int z)`。返すのは北西端の `{lat, lon}`。式と計算の順は 2.4 の `tile_to_latlon` のとおり。整数の引数を渡すときも、呼ぶ前に `double` になる（引数の型が `double`）ので、`x / n` が整数の割り算にならない。引数を検査しない（`int` への変換が無いので、どの値でも未定義の動作にならない）。

##### latlon_to_z15_pixel

`Z15Pixel latlon_to_z15_pixel(double lat, double lon)`。`latlon_to_tile(lat, lon, 23)` の `x`・`y` を `gx`・`gy` にして返す（2.4 の決まり。Z15 の 1 画素は z=23 の 1 タイルに当たる）。渡せる範囲は `latlon_to_tile` と同じ。

##### z15_pixel_center_latlon

`LatLon z15_pixel_center_latlon(const Z15Pixel& pixel)`。`tile_to_latlon(static_cast<double>(pixel.gx) + 0.5, static_cast<double>(pixel.gy) + 0.5, 23)` を返す（2.4 の決まり。HLD 4.7.2 の 3「ピークの緯度経度を求める」、DEC54）。小数点 8 桁の文字列にするのは「CSV と早期終了」の群の `format_coord` で、この関数は丸めない。

#### 6.10.4 メッセージ文面

なし。6.10 の関数はメッセージを出さない（`mesh_to_latlon` の `std::invalid_argument` は呼ぶ側の誤りで、文は 6.10.3 に書いた。利用者に見えるのは 6.12 の G7 の形）。

#### 6.10.5 UT 候補

すべて自動。GoogleTest のケースごとに `// trace: UT-analyze_terrain_convert-NN` を付け、2.4 の表の行を写したケースは表の名前もコメントに書く（[テスト方針書 3.3](02_test_policy.md#33-期待値の根拠)）。共通の準備は 1 つ。

- **同じプロセス**: テストのプロセスの中で対象の関数を直接呼ぶ。ファイルも出力も使わない。倍精度の値の期待は、2.4 の表の 10 進の表記を C++ の倍精度の字句としてそのまま書く（最短の 10 進表記なので、同じ倍精度の値になる）。`==` で比べるものは `EXPECT_EQ`、緯度の許容差のものは `EXPECT_NEAR(<値>, <期待>, 1e-12)`（`EXPECT_DOUBLE_EQ` は 4 ULP の比べ方で 2.4 の決まりと違うので使わない）。

| ID | 確かめること | 準備 | 入力 | 期待 |
|---|---|---|---|---|
| `UT-analyze_terrain_convert-01` | メッシュ → 緯度経度 | 同じプロセス | 2.4 の表 1 の 6 行 | `south`・`west`・`north`・`east` の 4 つとも期待の値と `==` |
| `UT-analyze_terrain_convert-02` | メッシュコードの形の誤り | 同じプロセス | (a) `533`、(b) `53390`、(c) `53a9`、(d) 空、(e) 全角の数字 4 字（UTF-8 で 12 バイト。16 進で `EF BC 95 EF BC 93 EF BC 93 EF BC 99`、バイトの間の空白は区切り）、(f) `-339` | どれも `std::invalid_argument`。`what()` は `mesh_to_latlon の引数が 4 桁の数字でない:` と空白 1 つの後に入力をそのまま続けたもの |
| `UT-analyze_terrain_convert-03` | 緯度経度 → メッシュ | 同じプロセス | 2.4 の表 5 の 12 行 | 期待のコードと等しい（4 バイト） |
| `UT-analyze_terrain_convert-04` | メッシュの範囲の外 | 同じプロセス | (a) `(-10.0, 139.0)`、(b) `(35.0, 99.5)`、(c) `(35.0, 200.0)`、(d) `(66.7, 139.0)`、(e) `(0.5, 100.0)`、(f) 緯度が NaN（`std::numeric_limits<double>::quiet_NaN()`）で経度 139.0、(g) 緯度 35.0 で経度が正の無限大 | (a)〜(d)・(f)・(g) は空の文字列。(e) は `0000`（`aa`・`bb` が 0 のときも 2 桁ずつ） |
| `UT-analyze_terrain_convert-05` | 緯度経度 → タイル | 同じプロセス | 2.4 の表 2 の 16 行 | `x`・`y` が期待の値と等しい |
| `UT-analyze_terrain_convert-06` | タイル → 緯度経度 | 同じプロセス | 2.4 の表 3 の 9 行（`x`・`y` は表の 10 進の値を `double` で渡す） | 経度は期待の値と `==`、緯度は差の絶対値が `1e-12` 以下 |
| `UT-analyze_terrain_convert-07` | 緯度経度 → Z15 の画素 | 同じプロセス | 2.4 の表 6 の 11 行 | `gx`・`gy` が期待の値と等しい |
| `UT-analyze_terrain_convert-08` | Z15 の画素の中心 | 同じプロセス | 2.4 の表 7 の 9 行 | 経度は期待の値と `==`、緯度は差の絶対値が `1e-12` 以下 |
| `UT-analyze_terrain_convert-09` | 画素の座標の比べ方 | 同じプロセス | `Z15Pixel{1, 2}` と `Z15Pixel{1, 2}`、`Z15Pixel{1, 3}` と `Z15Pixel{2, 0}`、`TileXY{5, 1}` と `TileXY{5, 2}` | 1 組目は `==` が真。2 組目は前が小さい（`<` が真。`gx` が先に比べられる）。3 組目は前が小さい。`std::set<Z15Pixel>` に `{1, 2}` を 2 回入れると大きさが 1 |

### 6.12 `analyze_terrain_common`

- **ID**: LLD-analyze_terrain_common
- **対応 HLD**: [3.4](30_HLD.md#34-cmp4-地形解析エンジン)・[3.9](30_HLD.md#39-共通部品)・[5.7](30_HLD.md#57-nfr-007-ログ出力)
- **ファイル**: `src/common.hpp`・`src/common.cpp`

各関数の決まりの正本は [2.1](#21-共通部品)（Python の同じ名前の部品）と [HLD 3.9](30_HLD.md#39-共通部品)で、この節は C++ で書くための細部と、Python と違うところだけを足す（[HLD 3.4.3](30_HLD.md#343-関数)の DEC150「CMP4 は共通部品の決まりを C++ で別に実装する」）。HLD 3.9 の部品のうち CMP4 が使うのは `load_config`・`read_mesh_arg`・`read_mesh_list_file`・`start_log`・`log_info`・`log_warning`・`log_error` と `EXIT_OK`〜`EXIT_USAGE` で、`acquire_lock`（CMP4 はロックを掛けない。CMP3 のロックの下で動く。[HLD 2.9.3](30_HLD.md#293-同時起動の排他)）・`fetch_record_path`・`mesh_to_latlon`・`latlon_to_tile`（6.10 の「変換」の群）は持たない。C++ だけの関数に `check_signal` がある（[HLD 3.4.3](30_HLD.md#343-関数)）。[5.7](30_HLD.md#57-nfr-007-ログ出力)（ログ出力）は、6.12.3 の `start_log`・`log_*`・`_finish_log`・`check_signal` で受ける。

#### 6.12.1 ファイル割付

- 公開の宣言は `src/common.hpp`、定義と内部の関数は `src/common.cpp` に置く。ファイルの先頭のコメントに `// trace: LLD-analyze_terrain_common` を書く。
- UT のコードは `tests/src/test_common.cpp` に置き、`build/test_common` にビルドする（[2.5](#25-ビルドとテストの名前)）。各テストに `// trace: UT-analyze_terrain_common-NN`（確かめる UT 候補の ID）のコメントを付ける。テストの枠組みは GoogleTest（[テスト方針書 3.4](02_test_policy.md#34-テストを先に書く進め方)）。

#### 6.12.2 型とデータ

`src/common.hpp` の公開の宣言は次のとおり（名前空間に入れない。1.2 の C++ の規約）。

```cpp
#pragma once
#include <chrono>
#include <map>
#include <set>
#include <string>
#include <vector>

constexpr int EXIT_OK = 0;
constexpr int EXIT_ERROR = 1;
constexpr int EXIT_USAGE = 2;

struct ExitRequest {
    int code;
    explicit ExitRequest(int exit_code);
};

struct ConfigValue {
    bool is_set;       // 偽は未設定（デフォルトの無いキーで書かれていないとき。CMP4 の 6 キーでは常に真）
    bool is_integer;   // 整数の種類のキーなら真
    long long integer; // 整数の値。is_integer が偽なら 0
    std::string text;  // パスの種類のキーの値。整数の種類なら空
    bool from_file;    // ファイルに書いてあれば真
};

struct Config {
    std::string path;                             // 設定ファイルの絶対パス（_abspath したもの）
    std::map<std::string, ConfigValue> values;    // load_config に渡したキーだけ
};

struct StartTime {
    std::chrono::system_clock::time_point wall;
    std::chrono::steady_clock::time_point mono;
    static StartTime now();   // 2 つの時計を続けて読む
};

Config load_config(const std::string& config_path,
                   const std::vector<std::string>& keys,
                   const std::vector<std::string>& required);
void start_log(const std::string& log_dir, const Config& config,
               const std::string& program, const std::vector<std::string>& args,
               const StartTime& start);
void log_info(const std::string& message);
void log_warning(const std::string& what, const std::string& action);
void log_error(const std::string& what, const std::string& action);
std::set<std::string> read_mesh_arg(const std::string& value);
std::set<std::string> read_mesh_list_file(const std::string& path, const std::string& guidance);
void check_signal();
```

- 終了コードの定数は 0・1・2 だけを持つ（HLD 3.4.3 の表。3・4 は CMP4 が返さない）。
- `ExitRequest`: 止まることを `main` の最上位へ伝える例外（1.2 の C++ の規約）。コンストラクタは `code` を入れ、`_state.started` が真のときだけ内部の状態に終了コードを記録する（`_state.has_exit_code = true`、`_state.exit_code = code`。後から作ったものが前のものを上書きする。Python の `_exit` が `start_log` の後の `sys.exit` のたびに記録するのと同じ）。`start_log` の前に作ったものは記録しない（終わりの行が無いので要らない。テストの同じプロセスで作ったものが、`fork` した子に残らないようにするため）。`std::exception` の子にしない。
- `StartTime`: `main` は最初（引数と設定の検査の前）に `StartTime::now()` を呼び、`start_log` に渡す（[HLD 5.7.2](30_HLD.md#572-処理の流れ)の 2「ファイルの名前」）。所要時間は `mono` の差で測る（時刻の補正に左右されない時計。HLD 5.7.1 の対象外の行）。
- 設定のキーの表 `_config_keys`（内部。`.cpp` の無名の名前空間の定数の配列）。行と順は 2.1.2 の `_CONFIG_KEYS` の表と同じ 12 行で、CF4・CF5 の判定と CF5 の `{keys}`（その節のキーを `・` でつないだもの）に全キーが要る。値を判定するのは次の 6 行だけで、ほかの 6 行（`fetch` の 3 つと `match` の 3 つ）は節とキーの名前だけを持つ。

  | 節 | キー | 種類 | デフォルト | 最小 | 最大 | 許容範囲の文（CF6・CF7 の `{range}`） |
  |---|---|---|---|---|---|---|
  | `paths` | `data_dir` | パス | なし（必須） | — | — | `絶対パス` |
  | `paths` | `log_dir` | パス | `<data_dir の値>/logs` | — | — | `絶対パス` |
  | `analysis` | `prominence_primary_m` | 整数 | `130` | `100` | なし（18 桁まで） | `100 以上の整数（18 桁まで）` |
  | `analysis` | `activation_zone_drop_m` | 整数 | `25` | `25` | `25` | `25` |
  | `analysis` | `delete_zone_max_drop_m` | 整数 | `250` | `200` | `300` | `200 以上 300 以下の整数` |
  | `merge` | `prominence_final_m` | 整数 | `150` | `150` | `150` | `150` |

  `load_config` の `keys` に、この 6 キーのほかの名前（`user_agent_email`・`max_parallel` など）を渡したら、呼ぶ側の誤り（`std::invalid_argument`）。パスの種類は「空でなく、先頭が `/`」。整数の種類は 2.1.2 の表の後の段落のとおり（ASCII の数字だけ、先頭の `0` を除いて 18 桁まで、`long long` に入れる。符号・小数点・全角の数字・空は型に合わない）。
- 内部の状態 `_state`（`.cpp` の無名の名前空間の 1 つの `struct` の変数）: `bool started`、`int log_fd`（`-1` は無し）、`std::string log_path`、`std::string program`、`StartTime start`、`bool broken`（ログファイルに書けなくなった）、`bool has_exit_code`、`int exit_code`、`bool signal_thrown`（`check_signal` が一度投げた）、`bool finished`（`_finish_log` が始まった）。受けたシグナルは別の変数 `volatile std::sig_atomic_t _signum`（`0` は無し。ハンドラが書く）。
- 起動のときの準備（内部。`.cpp` の無名の名前空間の、コンストラクタを持つ静的な変数 1 つ。`main` より前に動く）: `SIGPIPE` を無視にし（`signal(SIGPIPE, SIG_IGN)`。切れたパイプへの書き込みを `EPIPE` の失敗にする。Python が起動時に `SIGPIPE` を無視にするのと同じ）、`std::set_terminate(_on_terminate)` にする。

#### 6.12.3 関数の細部

関数ごとに `#####` の見出しを立てる。2.1 と同じ名前の見出しは、重複（MD024）を避けるために `（analyze_terrain_common）` を付ける。各関数の決まりの正本は 2.1.3 の同じ名前の部品で、ここには「2.1.3 の <部品> のとおり」と、C++ の細部と違いだけを書く。止まるときは、メッセージを `log_error` で出してから `throw ExitRequest(<定数>)` する（1.2 の C++ の規約）。`errno` は、失敗した呼び出しの直後に変数へ写してから使う（`{reason}` は `std::strerror` に渡した文）。

##### load_config（analyze_terrain_common）

`Config load_config(const std::string& config_path, const std::vector<std::string>& keys, const std::vector<std::string>& required)`

- 2.1.3 の `load_config` の 1〜9 のとおり。C++ の違いは次のとおり。
  - 1 の呼ぶ側の誤りと、6.12.2 の「`keys` に 6 キーのほかの名前を渡した」は、`throw std::invalid_argument("<説明>")`。
  - 2 の `path` は `_abspath(config_path)`。`os.path.exists` に当たるのは `stat(path.c_str(), &st)` が 0 を返すか（0 以外なら、`errno` によらず CF1。Python の `os.path.exists` が OS の誤りでも偽を返すのと同じ）。CF1 の対処は、いつも `--config に渡したパスを確かめる`（C++ は既定のパスを持たない。[HLD 2.3.2](30_HLD.md#232-設定ファイル)の「内部の起動口は既定パスを持たない」）。
  - 3 は `_read_file(path, data, err)`（下）で読み、失敗は CF2。
  - 4 は `_parse_ini(data, sections, error)`（下）で読む。
  - 9 の `log_dir` のデフォルトは `_join(<data_dir の値>, "logs")`。
- 返す `ConfigValue`: 整数の種類は `is_integer` が真で `integer` に値、パスの種類は `text` に値。デフォルトの値は `from_file` が偽。

##### _parse_ini（analyze_terrain_common）

`bool _parse_ini(const std::string& data, IniSections& sections, IniError& error)`（内部）

型は `.cpp` の無名の名前空間に置く。`using IniEntries = std::vector<std::pair<std::string, std::string>>;`（キー, 値の並び）、`using IniSections = std::vector<std::pair<std::string, IniEntries>>;`（節の名前と、その節のキー, 値の並びを、ファイルの順に並べたもの）、`struct IniError { std::string code; std::string reason; };`。誤りが無ければ `true` を返し、`sections` に結果を入れる。誤りがあれば `false` を返し、`error.code` に `"CF2"` か `"CF3"`、`error.reason` に `{reason}` を入れ、`sections` は空にする。止まらず、メッセージも出さない（メッセージは `load_config` が出す）。

読み方は 2.1.3 の `_parse_ini` の設定ファイルの書式の 1〜7 のとおり（テストベクトルは同じ節の CV-01〜CV-27）。バイトで扱う場合の細部: BOM は先頭の 3 バイト `EF BB BF` を 1 つだけ除く。UTF-8 として読めるかは `_decode_utf8_sig` の表（下）。NUL は 1 バイトの `00`。行は `\n` のバイトで分け、行の末尾の `\r` を 1 バイトだけ除く。前後から除くのはバイト `20` と `09` だけ。`#`・`;`・`[` は行の先頭のバイトで見る。節とキーの名前は、バイト列のまま比べる。名前が 1 字以上は、1 バイト以上。`{line_no}` は 10 進（先頭の `0` なし）、`{line}` は 4 で前後を除いた後の行のバイト列。

##### start_log（analyze_terrain_common）

`void start_log(const std::string& log_dir, const Config& config, const std::string& program, const std::vector<std::string>& args, const StartTime& start)`（`args` は `argv[1]` から後。プログラムの名前を含まない）

1. 2 回目の呼び出しは `throw std::logic_error("start_log の 2 回目")`。
2. `_make_dirs(log_dir, err)`（下）が失敗なら、2.2 の G3（`{path}` は `log_dir`、`{reason}` は `err` の文）を出して `throw ExitRequest(EXIT_ERROR)`。
3. `path = _join(log_dir, program + "_" + _local_time(start.wall, true) + "_" + std::to_string(getpid()) + ".log")`。`open(path.c_str(), O_WRONLY | O_CREAT | O_EXCL | O_CLOEXEC, 0666)`。失敗が `EEXIST` なら G4（`{path}` は `path`）、ほかの失敗は G3（`{path}` は `path`）を出して `throw ExitRequest(EXIT_ERROR)`（既にあるファイルには触れない）。
4. `_state` の `has_exit_code` を偽、`exit_code` を 0、`broken`・`signal_thrown`・`finished` を偽にしてから、`log_fd`・`log_path`・`program`・`start` を入れ、最後に `started` を真にする（`start_log` の前に作った `ExitRequest` は記録しないが、念のためここで初期化する。6.12.2 の `ExitRequest`）。続けて、次をこの順に取り付ける: `std::atexit(_finish_log)`、最後に `SIGINT` と `SIGTERM` のハンドラを `_on_signal` にする（`sigaction`、`sa_flags = SA_RESTART`、`sa_mask` は空。シグナルのハンドラを最後にする理由は 2.1.3 の `start_log` の 4 と同じ）。
5. 2.2 の L1・L2 の行を `_emit`（標準出力）で出す。L1 の `{args}` は 2.2 の引用の決まりで 1 つずつ書いて空白 1 つでつなぐ（`_quote_arg`。引数が無ければ `開始: {program}`）。L2 は `設定ファイル: {config.path}` の後、`config.values` のキーを `_config_keys` の順に `設定: [{section}] {key} = {value}（{source}）`。`{value}` は整数なら 10 進（先頭の `0` なし）、パスならその文字列、未設定なら `未設定`。`{source}` は `from_file` が真なら `ファイル`、偽なら `デフォルト`（未設定のときもデフォルト）。

##### _emit（analyze_terrain_common）

`void _emit(const std::vector<std::string>& lines, int fd, bool ignore_screen_errors)`（内部。`fd` は 1〔標準出力〕か 2〔標準エラー出力〕）

2.1.3 の `_emit` のとおり（渡された各行の中の `\n` でさらに行を分け、全行を先に画面へ時刻なしで出し、その後で全行をログファイルへ時刻付きで書く）。C++ の細部:

1. 画面: 1 行ごとに `<行>` と `\n` を `_write_all(fd, ...)`（下）で書く。失敗したとき、`ignore_screen_errors` が偽なら `throw std::system_error(errno, std::generic_category(), fd == 1 ? "標準出力" : "標準エラー出力")`（`what()` は `標準出力: Broken pipe` の形）、真なら無視して次の行へ進む。
2. ログファイル: `_state.log_fd` が `-1` でなく、`broken` と `finished` が偽のときだけ（`finished` が真なら、ログファイルは閉じたか閉じる途中）、1 行ごとに `<時刻> <行>` と `\n` を 1 回の `_write_all` で書く。時刻は書く時点の `_local_time(std::chrono::system_clock::now(), false)`（[HLD 5.7.2](30_HLD.md#572-処理の流れ)の 3「行の書式」）。失敗したら `_state.broken = true` にし、G5（`{path}` は `_state.log_path`、`{reason}` は失敗の `errno` の文）の 2 行を標準エラー出力にだけ出し（この出力の失敗は無視）、`throw ExitRequest(EXIT_ERROR)`。

##### log_info・log_warning・log_error（analyze_terrain_common）

`void log_info(const std::string& message)`・`void log_warning(const std::string& what, const std::string& action)`・`void log_error(const std::string& what, const std::string& action)`

2.1.3 の `log_info`・`log_warning`・`log_error` のとおり（出す行、出し先、`broken` の後の扱い）。`_emit` を `ignore_screen_errors` を偽にして呼ぶ（`log_info` は `fd` が 1、ほかの 2 つは 2）。`start_log` の前は画面にだけ出す（`log_fd` が `-1`）。`broken` の後は、`log_info` は何も出さず、`log_warning`・`log_error` は標準エラー出力にだけ出す。

##### _finish_log（analyze_terrain_common）

`void _finish_log()`（内部。`std::atexit` から呼ばれる）

1. `_state.finished` が真なら何もせずに戻る（2 回目の呼び出し。`std::exit` の途中で `_on_terminate` に来たとき）。偽なら真にしてから、`SIGINT`・`SIGTERM` を無視にする（`signal(sig, SIG_IGN)`）。`_state.broken` が真なら、終わりの行を書かず `_exit(EXIT_ERROR)`（HLD 5.7.2 の 4「始まりと終わりの行」の「ログファイルに書けなくなって止まるときは、終わりの行を書こうとせず」。[HLD 5.7.3](30_HLD.md#573-異常系)）。
2. 終了コード `code`: `_signum` が 0 でなければ `128 + _signum`、そうでなく `has_exit_code` が真なら `exit_code`、どちらでもなければ `EXIT_OK`。2.2 の L3 の行（シグナルを受けていれば `（{signame} を受けて止まった）` つき。`{signame}` は `SIGINT` か `SIGTERM`。`{sec}` は `start.mono` からの秒を `%.3f`。`{end}` は今の `_local_time(..., false)`）を、ログファイルへ `<時刻> <L3>` と `\n` を 1 回の `_write_all` で書き、`close(log_fd)`。書くか閉じるのに失敗したら、G6（`{path}` は `log_path`、`{reason}` は失敗の `errno` の文）の 2 行を標準エラー出力にだけ出し（失敗は無視）、`_exit(EXIT_ERROR)`（終了コード 0 などで終わるはずだったときも 1。HLD 5.7.3）。
3. 書けたら、同じ L3 の文面を標準出力へ時刻なしで出す（失敗は無視）。`_signum` が 0 でなければ `_exit(128 + _signum)`。そうでなければ戻る（プロセスは `main` が返した値で終わる。1.2 の規約で、それは記録した値と同じ）。

最後の `check_signal` の後、`_finish_log` の 1 より前にシグナルを受けたときは、完了の要約の後に、シグナルを受けて止まった形の L3 と 128＋シグナルの番号になる（Python も `finally` の後に受ければ同じ）。

画面への出力の失敗: 1〜3 の画面への出力は、失敗を無視して必ず次へ進む（`_exit` か、戻るところまで届かせる。終わる途中で、止める先も知らせる先も無い）。ログファイルへの書き込みの失敗は 2 のとおりで、これに当たらない。

##### _on_signal（analyze_terrain_common）

`void _on_signal(int signum)`（内部。シグナルのハンドラ）

`_signum` が 0 なら `_signum = signum`（2 回目からは何もしない。止まるための後始末を途中で切らないため）。ほかのことはしない（非同期シグナル安全な代入だけ）。

##### check_signal

`void check_signal()`

`_signum` が 0 でなく `_state.signal_thrown` が偽なら、`signal_thrown = true` にして `throw ExitRequest(128 + _signum)`。メッセージは出さない（終わりの行にシグナルの名前を書く）。2 回目からは何もしない（止まるための後始末の中で呼ばれても、後始末を途中で切らない）。`start_log` の前に受けたシグナルは既定の扱い（ハンドラが無いので OS がプロセスを止め、終了状態は 128＋シグナルの番号）。

##### _on_terminate

`void _on_terminate()`（内部。`std::set_terminate` で付ける処理。捕まらなかった例外と、`catch (...)` の中の `std::terminate()` が呼ぶ）

1. 今の例外を `std::current_exception()` で取り、`std::rethrow_exception` して捕まえ分ける。`ExitRequest` なら（`main` の最上位で捕まえ忘れた）、`code` を終了コードにし、メッセージを出さない。`std::exception` の子なら `{type}` は `abi::__cxa_demangle(typeid(e).name(), ...)` の結果（失敗したら `typeid(e).name()`）、`{message}` は `e.what()`。そのほかは `{type}` を `不明な型`、`{message}` を空にする。例外が無いときは `{type}` を `std::terminate`、`{message}` を `例外なしで呼ばれた` にする。
2. `ExitRequest` 以外なら、2.2 の G7 の 2 行を `_emit`（標準エラー出力、`ignore_screen_errors` は真）で出す。`start_log` の後なら、ログファイルにも出る（書けなければ `broken` になる）。`_emit` が投げる `ExitRequest` は `try` で囲んで捕まえ、次へ進む。
3. 終了コードは、`_signum` が 0 でなければ `128 + _signum`、そうでなければ、1 で取った例外が `ExitRequest` ならその `code`、ほかは `EXIT_ERROR`。`started` が真で `finished` が偽なら `has_exit_code = true`、`exit_code` にその値を入れて `_finish_log()` を呼ぶ（`finished` が真なら、終わりの行は書いたか書く途中なので呼ばない）。最後に `_exit(<終了コード>)`。

##### read_mesh_arg（analyze_terrain_common）・read_mesh_list_file（analyze_terrain_common）

`std::set<std::string> read_mesh_arg(const std::string& value)`・`std::set<std::string> read_mesh_list_file(const std::string& path, const std::string& guidance)`

2.1.3 の `read_mesh_arg`・`read_mesh_list_file`・`_parse_mesh_lines` のとおり（行の読み方とファイルの読み方の正本は 2.1.3 の段落とメッシュの読み方のテストベクトル）。C++ の違い:

- 4 桁の判定は ASCII の `0`〜`9` の 4 バイト。`os.path.abspath` は `_abspath`、`os.path.exists` は `stat`（`load_config` と同じ）、ファイルは `_read_file`（`read` が失敗する場合は、ディレクトリの `EISDIR` を含め、`{reason}` が `errno` の文）。UTF-8 として読めるかと BOM の除き方は `_decode_utf8_sig`（下）。読めなければ `{reason}` は `UTF-8 として読めない`（`read_mesh_arg` は A3、`read_mesh_list_file` は R2）。
- `guidance` が空の文字列なら既定の対処（Python の `None`）。
- 誤りの `{line}` は、前後を除いた後の行のバイト列（NUL もそのまま）。
- 内部の関数 `bool _parse_mesh_lines(const std::string& text, std::set<std::string>& meshes, long long& error_line_no, std::string& error_line)`: 誤りが無ければ `true`。行を `\n` で分けて 1 から番号を振り、各行の前後から `' '`・`'\t'`・`'\r'` を除き、空と `#` で始まる行を飛ばし、残りが ASCII の数字 4 バイトでなければ最初の行の番号と中身を返して `false`。

##### 内部の小さな関数

- `std::string _abspath(const std::string& p)`: Python の `os.path.abspath` と同じ値にする。`p` が `/` で始まらなければ、`getcwd()` と `/` を前に付ける（`getcwd()` が `/` で終われば `/` は足さない）。先頭の `/` がちょうど 2 つ（`//` で始まり `///` では始まらない）なら先頭は `//`、そうでなければ `/` とする。残りを `/` で分け、空と `.` を除き、`..` は 1 つ前の要素を除く（要素が無ければ無視）。先頭と、残りの要素を `/` でつないだものをつなぐ。例（Python の値）: `//` → `//`、`//a` → `//a`、`///a` → `/a`、`/a/../../b` → `/b`、`//..` → `//`、`/a//b` → `/a/b`。
- `std::string _join(const std::string& a, const std::string& b)`: `a` が `/` で終われば `a + b`、そうでなければ `a + "/" + b`（`b` は `/` で始まらない名前だけを渡す）。
- `bool _read_file(const std::string& path, std::string& data, int& err)`: `open(path, O_RDONLY | O_CLOEXEC)` と `read` を、`EINTR` のほかの失敗か 0 まで繰り返して全部を読み、`close`。失敗したら `err` に `errno` を入れて `false`（ディレクトリは `read` の `EISDIR`）。
- `bool _write_all(int fd, const std::string& s)`: `write` を、全部書くか `EINTR` のほかの失敗まで繰り返す。失敗したら `false`（`errno` は残す）。
- `bool _make_dirs(const std::string& path, int& err)`: `path` を `/` で区切った先頭からの各段のパス（空の要素は飛ばす）に `mkdir(<段>, 0777)` を呼ぶ。途中の段の `EEXIST` は、`stat` を見ずに次の段へ進む（途中の段がディレクトリでなければ、次の段の `mkdir` が本当の理由の `errno` で失敗する）。最後の段の `EEXIST` は、`stat` でディレクトリかを見て、ディレクトリなら成功、ディレクトリでないか `stat` が失敗すれば `err = EEXIST` で失敗。ほかの失敗はその `errno` で失敗。Python の `os.makedirs(..., exist_ok=True)` と同じ順で、同じ `{reason}` にする（`log_dir` がファイルなら `File exists`、途中の段がファイルなら `Not a directory`、`log_dir` がリンク先の無いシンボリックリンクなら `File exists`、その下の `logs` なら `No such file or directory`）。
- `std::string _quote_arg(const std::string& a)`: 2.2 の引用の決まり（バイトで判定する。`a` が空でなく、どのバイトも ASCII の英数字か `_@%+=:,./-` のどれかならそのまま。そうでなければ `'` で囲み、中の `'` を `'"'"'` に置き換える。空は `''`）。
- `std::string _local_time(std::chrono::system_clock::time_point t, bool for_name)`: `localtime_r` で求めたローカル時刻を、`for_name` が真ならファイルの名前の `YYYYMMDDTHHMMSS`、偽なら行の時刻の `YYYY-MM-DDTHH:MM:SS±HH:MM`（`strftime` の `%Y-%m-%dT%H:%M:%S` に、`tm_gmtoff` から作った `±HH:MM` を付ける）にする。
- `bool _decode_utf8_sig(const std::string& bytes, std::string& text)`: 先頭の BOM `EF BB BF` を 1 つだけ除いた残りが、次の形だけでできていれば `text` に入れて `true`、そうでなければ `false`（Python の `utf-8` の復号と同じ判定。サロゲートの符号化、U+10FFFF を超える符号位置、長すぎる符号化、途中で切れた列、5 バイト以上の列は読めない）:

  | 先頭のバイト | 続くバイト |
  |---|---|
  | `00`〜`7F` | なし |
  | `C2`〜`DF` | `80`〜`BF` が 1 つ |
  | `E0` | `A0`〜`BF` の後に `80`〜`BF` が 1 つ |
  | `E1`〜`EC`、`EE`〜`EF` | `80`〜`BF` が 2 つ |
  | `ED` | `80`〜`9F` の後に `80`〜`BF` が 1 つ |
  | `F0` | `90`〜`BF` の後に `80`〜`BF` が 2 つ |
  | `F1`〜`F3` | `80`〜`BF` が 3 つ |
  | `F4` | `80`〜`8F` の後に `80`〜`BF` が 2 つ |

#### 6.12.4 メッセージ文面

書き方は [2.2](#22-ログとメッセージの文面)。誤りの文面は 2.1.4 の CF1〜CF7・A1〜A5・R1〜R3 と同じで、ここには写さない。違いは次の 3 つ。

- CF1 の対処は、いつも `--config に渡したパスを確かめる`（C++ は既定のパスを持たない。[HLD 2.3.2](30_HLD.md#232-設定ファイル)の「内部の起動口は既定パスを持たない」）。
- CF3 の対処の `{example_path}` は、文字列 `params/config.ini.example` にする（C++ はソースツリーの場所を知らない。[HLD 2.3.2](30_HLD.md#232-設定ファイル)の「CMP4 のビルド成果物からはソースツリーの場所が定まらない」。2.2 の「対処の行に書くコマンドは、ソースツリーの根で打つ形で書く」に合わせる）。
- `{reason}` の作り方は 1.2 の C++ の規約（OS の失敗は `std::strerror`）。CF2・CF3 の書式の誤りは 2.1.3 の設定ファイルの書式の文。UTF-8 として読めないときは `UTF-8 として読めない`。

全体に共通する場面（G3〜G7）とログの行（L1〜L3）は 2.2 のとおり。G1・G2 は CMP4 が出さない（ロックを掛けない）。C++ だけのメッセージは無い（`std::invalid_argument`・`std::logic_error` は呼ぶ側の誤りで、利用者に見せる文面を持たない。捕まらなければ G7 で止まる）。

#### 6.12.5 UT 候補

すべて自動。GoogleTest のテストのケースごとに `// trace: UT-analyze_terrain_common-NN` を付ける。ログファイルの行の期待は、先頭の時刻と空白を除いた文面で書く。`start_log` を呼ぶと標準出力に L1・L2 の行が時刻なしで出るので、標準出力の期待にはこれらも含める。表の準備の列の共通の準備は次の 3 つ。ケースに固有の準備は、その後に書く。

- **同じプロセス**: テストのプロセスの中で対象の関数を直接呼ぶ。ケースごとに一時のディレクトリ（`mkdtemp`）を作る。設定ファイルを使うケースは、その下に設定ファイルを書いて絶対パスを渡す（`data_dir`・`log_dir` を書くときは、一時のディレクトリの下の絶対パス）。止まるケースは `ExitRequest` を捕まえて `code` を確かめる（`start_log` を呼ばないので、シグナルのハンドラも `atexit` も付かない）。標準出力と標準エラー出力は、呼ぶ前に `dup`・`dup2` で記述子 1・2 を一時のファイルに付け替えて捕まえ、呼んだ後に戻す。
- **子のプロセス**: 親は `fork` の直前に `std::fflush(nullptr)` を呼ぶ（GoogleTest が標準出力のバッファにためた行を、子が受け継いで付け替えた先へ書き出さないようにするため）。子の設定ファイルは、親が一時のディレクトリに置く（`data_dir` と `log_dir` を、一時のディレクトリの下の絶対パスで書く）。`fork` した子の中で、記述子 1・2 を親が読む 2 つのパイプの書く側に付け替えて、2 つのパイプの元の 4 つの記述子を閉じ、`StartTime::now()` と `load_config`（ケースが書かなければ `keys` は `data_dir` と `log_dir`、`required` は `data_dir`）を呼んでから、入力の列の処理を、1.2 の `main` の形に捕まらない例外の経路を足した形（`try { <処理>; } catch (const ExitRequest& e) { std::exit(e.code); } catch (...) { std::terminate(); } std::exit(EXIT_OK);`）で行う。`catch (...)` の中で `std::terminate()` を呼ぶのは、子の中にも GoogleTest のテストの呼び出しが残っていて、例外をそのまま外へ出すと GoogleTest が捕まえてしまうため（`catch` の中から呼べば、`_on_terminate` の `std::current_exception()` がその例外を返し、`main` から例外が出たときと同じ経路になる）。`UT-analyze_terrain_common-31` だけは `catch (const ExitRequest& e)` を置かず、`catch (...) { std::terminate(); }` だけにする（捕まえ忘れた `ExitRequest`）。`start_log` は入力の列が書く位置で 1 回だけ、`start_log(<config の log_dir>, config, "test_common", <ケースの引数>, start)` の形で呼ぶ（入力の列が `start_log` の位置を書いていないケースは、処理の最初に呼ぶ。ケースの引数が書いていなければ空）。親は `fork` の後に 2 つのパイプの書く側を閉じ、2 つのパイプを `poll` で両方が終わり（EOF）になるまで読み、`waitpid` の終了状態（シグナルで死んでいたらケースの失敗）とログファイル（`<log_dir>` の下の `test_common_*_<子の PID>.log`）を確かめる。
- **ログファイルに書けない場面**: 子の中で `start_log` の後に `SIGXFSZ` を無視にし、`setrlimit(RLIMIT_FSIZE, ...)` の `rlim_cur` を 0 にする（以後のログファイルへの書き込みが `EFBIG`〔`File too large`〕で失敗する。パイプには効かない）。終わりの行だけを失敗させるときは、`start_log` の後に `SIGXFSZ` を無視にし、`std::atexit` で同じ制限（`rlim_cur` を 0 にする）を掛ける処理を登録する（`atexit` は登録の逆順に動くので、`_finish_log` より先に動く）。画面が切れたパイプの場面は、子の中で `pipe` を作って読む側を `close` し、書く側を記述子 1（か 2）に `dup2` する。

| ID | 確かめること | 準備 | 入力 | 期待 |
|---|---|---|---|---|
| `UT-analyze_terrain_common-01` | 正しい設定を読む（`UT-common-01` の C++ 版） | 同じプロセス。CMP4 の 6 キーをすべて書いた設定ファイル（`prominence_primary_m = 120`、`activation_zone_drop_m = 25`、`delete_zone_max_drop_m = 300`、`prominence_final_m = 150`） | 6 キー（`data_dir`・`log_dir`・`prominence_primary_m`・`activation_zone_drop_m`・`delete_zone_max_drop_m`・`prominence_final_m`）の `keys` と、`required` は `data_dir` | 整数の 4 キーは `is_integer` が真で `integer` が 120・25・300・150、パスの 2 キーは `text` が書いた値、6 キーとも `is_set` と `from_file` が真。`Config.path` は設定ファイルの絶対パス |
| `UT-analyze_terrain_common-02` | デフォルト（`UT-common-02`） | 同じプロセス。`data_dir` だけを書いた設定ファイル | 6 キーの `keys` と、`required` は `data_dir` | `log_dir` の `text` が `<data_dir>/logs`、4 つの整数のキーが 130・25・250・150、この 5 つは `from_file` が偽。`data_dir` は `from_file` が真。6 キーとも `is_set` が真 |
| `UT-analyze_terrain_common-03` | 設定ファイルが無い（`UT-common-03`） | 同じプロセス。一時のディレクトリの下の存在しないパスと、その相対パス（作業ディレクトリを、そのディレクトリを含む一時のディレクトリに移して渡す。呼んだ後に戻す） | `keys` は `data_dir` と `log_dir`、`required` は `data_dir`。絶対パスと相対パスをそれぞれ渡す | どちらも `ExitRequest` の `code` が 2。標準エラー出力が `ERROR: 設定ファイルが無い: <絶対パス>` と `対処: --config に渡したパスを確かめる` の 2 行。ログファイルを作らない |
| `UT-analyze_terrain_common-04` | 読めない・INI でない（`UT-common-04`） | 同じプロセス。(a) `FF FE` だけのファイル、(b) 節の見出しより前にキーがあるファイル（CV-17 の中身）、(c) 同じキーが 2 回あるファイル（CV-19）、(d) 同じ節が 2 回あるファイル（CV-18）、(e) 設定ファイルの代わりにディレクトリ | 各パスを `load_config` に渡す（`keys` は `data_dir` と `log_dir`、`required` は `data_dir`） | どれも `code` が 2。(a) は CF2（`{reason}` は `UTF-8 として読めない`）、(b)(c)(d) は CF3 で `{reason}` が CV-17・CV-19・CV-18 の文、(e) は CF2（`{reason}` は `Is a directory`。CF1 でない） |
| `UT-analyze_terrain_common-05` | 知らない節とキー（`UT-common-05`） | 同じプロセス。5 つの設定ファイル。どれも `[paths]` に `data_dir` を書き、(a) `[DEFAULT]` の節、(b) `[foo]` の節、(c) `[fetch]` の節に書いた `data_dir` のキー、(d) `[paths]` の節に書いた `Data_Dir` のキー、(e) `[analysis]` の節に書いた `foo` のキーを足す | 各ファイルを `load_config` に渡す（`keys` は `data_dir` と `log_dir`、`required` は `data_dir`） | どれも `code` が 2。(a)(b) は CF4（`[DEFAULT]`・`[foo]`）、(c) は CF5（`[fetch] data_dir`。対処に `max_parallel・interval_ms・user_agent_email`）、(d) は CF5（`[paths] Data_Dir`。対処に `data_dir・log_dir`）、(e) は CF5（`[analysis] foo`。対処に `prominence_primary_m・activation_zone_drop_m・delete_zone_max_drop_m`）。`keys` に無い節とキーも見つける |
| `UT-analyze_terrain_common-06` | 整数のキーの境目（`UT-common-06`・`-30` の (iii)〜(vii)） | 同じプロセス。値ごとに別の設定ファイル（どれも `data_dir` を書く） | 6 キーの `keys`。(a) `prominence_primary_m` に `99`/`100`、`prominence_final_m` に `149`/`150`/`151`、`activation_zone_drop_m` に `24`/`25`/`26`、`delete_zone_max_drop_m` に `199`/`200`/`300`/`301`。(b) `prominence_primary_m` に書き方の違い（`+5`・`1.5`・全角の数字の `100`〈U+FF11、U+FF10、U+FF10〉・`-1`・空の値）。(c) `prominence_primary_m` に `1` の後に `0` を 17 個並べた 18 桁の数、`1` の後に `0` を 18 個並べた 19 桁の数、`1` の後に `0` を 4300 個並べた 4301 桁の数、`0` を 4300 個並べた後に `150` | (a) 端の内（100・150・25・200・300）は読める、外は `code` が 2 の CF6。(b) は CF6、`{value}` は書いたまま。(c) 18 桁は読めて `integer` が 100000000000000000、19 桁と 4301 桁は CF6、`0` を並べた後の `150` は 150 として読める |
| `UT-analyze_terrain_common-07` | 必須と誤りのまとめ（`UT-common-08`・`-09`） | 同じプロセス。(a) `[paths]` に `log_dir = /x` だけを書いたファイル、(b) `[paths]` に `foo = 1` と `log_dir = rel` を書き、`data_dir` を書かないファイル | 6 キーの `keys`、`required` は `data_dir` | (a) は `code` が 2 の CF7（`data_dir`）。(b) は標準エラー出力に CF5（`[paths] foo`）・CF6（`[paths] log_dir = rel`）・CF7（`data_dir`）の 3 つのメッセージ（6 行）がこの順に出て、`ExitRequest` は 1 回 |
| `UT-analyze_terrain_common-08` | 絶対パスでない（`UT-common-10`） | 同じプロセス。`data_dir = data`、`log_dir = logs` を書いた設定ファイル | `keys` は `data_dir` と `log_dir`、`required` は `data_dir` | `code` が 2。CF6 が `data_dir`、`log_dir` の順に 2 つ出る（`{range}` は `絶対パス`、`{value}` は書いたまま） |
| `UT-analyze_terrain_common-09` | 呼ぶ側の誤り（`UT-common-11`） | 同じプロセス。`data_dir` と `log_dir` を書いた正しい設定ファイル | (a) `keys` に `data_dir` が無い、(b) `keys` に `log_dir` が無い、(c) `required` に `data_dir` が無い、(d) `keys` に表に無い名前 `foo`、(e) `required` に `keys` に無い名前、(f) `keys` に `user_agent_email`、(g) `keys` に `max_parallel` | どれも `std::invalid_argument`（`ExitRequest` でない）。標準エラー出力に何も出ない |
| `UT-analyze_terrain_common-10` | NUL と BOM（`UT-common-30` の (i)(ii)・`-38` の設定） | 同じプロセス。バイト列で書いた 3 つのファイル | (i) `[`・NUL・`]` の節を足した設定、(ii) `[paths]` の `data_dir` の値の末尾に NUL を入れた設定、(iii) 先頭に BOM（`EF BB BF`）を付けた正しい設定 | (i)(ii) は `code` が 2 の CF3（`{reason}` は `NUL の文字がある`）、(iii) は読める（`data_dir` の値に BOM が付かない） |
| `UT-analyze_terrain_common-11` | 設定ファイルの書式のテストベクトル（`UT-common-44`） | 同じプロセス。[2.1.3](#213-関数の細部)の設定ファイルの書式のテストベクトル（CV-01〜CV-27）の中身ごとに一時のファイルをバイト列で書く | 各ファイルを `load_config` に渡す（`keys` は `data_dir` と `log_dir`、`required` は `data_dir`） | 表の `load_config` の結果の列のとおり（読めたら `data_dir` の `text`、止まったら `code` が 2 と、出た記号の並び。CF2・CF3 は `{reason}` も表の書式の結果の列のとおり） |
| `UT-analyze_terrain_common-12` | `--mesh` の値を読む（`UT-common-12`） | 同じプロセス。ファイルは一時のディレクトリに作る。相対パスのケースは、作業ディレクトリをその一時のディレクトリに移してから呼ぶ（呼んだ後に戻す） | `5339`、`0123`、空白と CR と空行と `#` の行と重複を含むファイル、相対パス | `{5339}`、`{0123}`、重なりを除いた集合、作業ディレクトリ基準で読む |
| `UT-analyze_terrain_common-13` | `--mesh` の誤り（`UT-common-13`・`-39` の `read_mesh_arg`） | 同じプロセス。ファイルとディレクトリは一時のディレクトリに作る | (a) 空の値、(b) 無いファイル、(c) ディレクトリ、(d) 2 行目と 4 行目が誤りのファイル、(e) 全角の数字の `5339`（U+FF15、U+FF13、U+FF13、U+FF19）の行を含むファイル、(f) 有効な行が無いファイル、(g) `533`、(h) `FF FE` だけのファイル | どれも `code` が 2。(a) は A1、(b) は A2、(c) は A3（`{reason}` は `Is a directory`）、(d) は A4 で 2 行目、(e) は A4、(f) は A5、(g) はパスとして読むので A2、(h) は A3（`{reason}` は `UTF-8 として読めない`） |
| `UT-analyze_terrain_common-14` | リストを読む（`UT-common-14`・`-39` の `read_mesh_list_file`） | 同じプロセス。ファイルとディレクトリは一時のディレクトリに作る | (a) 正しいリスト、(b) 空のファイル、(c) 無いファイルで `guidance` が `この案内` の文字列、(d) 無いファイルで `guidance` が空の文字列、(e) 誤りの行があるファイル、(f) ディレクトリ、(g) `FF FE` だけのファイル | (a) 集合、(b) 空の集合、(c) は `code` が 1 の R1 で対処が `この案内`、(d) は R1 で対処が既定（`ファイル <絶対パス> があり、読み取れることを確かめる`）、(e) は R3、(f) は R2（`Is a directory`）、(g) は R2（`UTF-8 として読めない`） |
| `UT-analyze_terrain_common-15` | メッシュの読み方のテストベクトル（`UT-common-43`） | 同じプロセス。[2.1.3](#213-関数の細部)のメッシュの読み方のテストベクトル（MV-01〜MV-21）の中身ごとに一時のファイルをバイト列で書く | 各ファイルを `read_mesh_arg` と、`guidance` を空にした `read_mesh_list_file` に渡す | テストベクトルの表の結果のとおり。誤りの行は `read_mesh_arg` が A4、`read_mesh_list_file` が R3 で、`{line_no}` が表のとおり、`{line}` は NUL を含まない行だけ表のとおり。空の集合は `read_mesh_arg` が A5、`read_mesh_list_file` が空の集合。UTF-8 として読めないものは A3・R2（`{reason}` は `UTF-8 として読めない`） |
| `UT-analyze_terrain_common-16` | `start_log` の前の出し先（`UT-common-15`） | 同じプロセス（`start_log` を呼ばない） | `log_info("x")`、`log_warning("w", "a")`、`log_error("e", "b")` | 標準出力は `x` の 1 行、標準エラー出力は `WARNING: w`・`対処: a`・`ERROR: e`・`対処: b` の 4 行。時刻は付かない |
| `UT-analyze_terrain_common-17` | ログファイルの始まり（`UT-common-16`） | 子のプロセス。`load_config` の `keys` は `data_dir`・`log_dir`・`prominence_primary_m`（設定ファイルには `data_dir` と `log_dir` だけを書く） | 子の中で引数なしの `start_log` を呼び、その後に `log_info("hello")` と `log_warning("w", "a")` | `log_dir` を作る。ログファイルの名前が正規表現 `^test_common_\d{8}T\d{6}_<子の PID>\.log$` に合う。ログファイルの先頭は `開始: test_common`、`設定ファイル: <設定ファイルの絶対パス>`、`設定: [paths] data_dir = <値>（ファイル）`、`設定: [paths] log_dir = <値>（ファイル）`、`設定: [analysis] prominence_primary_m = 130（デフォルト）` の 5 行がこの順で、その後に `hello`・`WARNING: w`・`対処: a`。各行の先頭に正規表現 `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}` に合う時刻と空白 1 つ（2 行のメッセージは各行に時刻）。標準出力は先頭の 5 行と `hello` が時刻なしで出る。標準エラー出力は `WARNING: w`・`対処: a` |
| `UT-analyze_terrain_common-18` | 終わりの行（`UT-common-17`） | 子のプロセス（3 つの子を別々に） | 子の中で `start_log` の後に、(a) 何もせず最後まで進む、(b) `throw ExitRequest(2)`、(c) `throw ExitRequest(1)` | 終了コード 0・2・1。ログファイルの最後の行が L3 で同じ終了コード、標準出力の最後の行も同じ文面の L3（行頭の時刻なし）。`{sec}` は正規表現 `\d+\.\d{3}` に合う |
| `UT-analyze_terrain_common-19` | 捕まらなかった例外（`UT-common-18`） | 子のプロセス | 子の中で `start_log` の後に `throw std::runtime_error("x")` | 終了コード 1。標準エラー出力とログファイルに G7 の 2 行（`予期しない例外で止まった: std::runtime_error: x`、`対処:` の行）。Traceback は出ない。ログファイルの最後の行は L3 で終了コード 1 |
| `UT-analyze_terrain_common-20` | シグナル（`UT-common-19`） | 子のプロセス（`SIGTERM` の子と `SIGINT` の子を別々に） | 子の中で `start_log` の後に、`try { kill(getpid(), SIGTERM); check_signal(); } catch (...) { log_info("CLEANUP"); throw; }`（`SIGINT` の子は `SIGINT`） | 終了コード 143・130。標準出力に `CLEANUP` が出る。ログファイルの最後の行が `終了: 終了コード 143（SIGTERM を受けて止まった）、…`（`SIGINT` の子は 130 と `SIGINT`） |
| `UT-analyze_terrain_common-21` | 区切りまで止まらない | 子のプロセス | 子の中で `start_log` の後に、`kill(getpid(), SIGTERM)`、`log_info("BEFORE")`、`check_signal()` | 標準出力に `BEFORE` が出る。終了コード 143 |
| `UT-analyze_terrain_common-22` | 2 回目のシグナル（`UT-common-31`） | 子のプロセス | 子の中で `start_log` の後に、`try { kill(getpid(), SIGTERM); check_signal(); } catch (...) { kill(getpid(), SIGTERM); check_signal(); log_info("MARK"); throw; }` | 標準出力に `MARK` が出る。終了コード 143。ログファイルの終わりの行は 1 つ |
| `UT-analyze_terrain_common-23` | 同じ名前のログファイル（`UT-common-20`） | 子のプロセス。子の中で `start_log` の前に、同じ `StartTime` と自分の PID から 6.12.3 の `start_log` の 3 の名前を作り、`log_dir` を作ってから、その下にその空のファイルを置く（親は子の PID を起動の前に知れないため） | 子の中で同じ名前のファイルを置いた後に `start_log` | 終了コード 1。標準エラー出力に G4。置いたファイルは空のまま変わらない |
| `UT-analyze_terrain_common-24` | ログの出力先を用意できない（`UT-common-21`） | 子のプロセス。(a) `log_dir` のパスに通常のファイルを置く、(b) `log_dir` の途中の段に通常のファイルを置く（`<ファイル>/logs`） | 子の中で `start_log` | どちらも終了コード 1。標準エラー出力に G3 だけ（(a) の `{reason}` は `File exists`、(b) は `Not a directory`）。ログファイルは作られない |
| `UT-analyze_terrain_common-25` | ログファイルに書けなくなった（`UT-common-22` の (a)(b)(c)(d)） | 子のプロセス（4 つの子を別々に）。共通の準備の `RLIMIT_FSIZE` で書き込みを失敗させる | 子の中で `start_log` の後に、(a) `log_info("x")`、(b) `try { log_info("x"); } catch (const std::exception&) { log_info("CAUGHT"); }`、(c) `try { log_info("x"); } catch (...) { log_info("要約"); throw; }`、(d) `throw std::runtime_error("x")` | どれも終了コード 1。ログファイルに終わりの行が無い。(a)(b)(c) は標準エラー出力に G5 が 1 回出る。(b) は標準出力に `CAUGHT` が出ない（`ExitRequest` は `std::exception` でない）。(c) は標準出力に `要約` が出ない（`broken` の後の `log_info` は何も出さない）。(a)(b)(c) の標準出力は L1・L2 の行と `x` だけ。(d) の標準エラー出力は、G7 の 2 行、G5 の 2 行の順 |
| `UT-analyze_terrain_common-26` | 終わりの行だけ書けなかった（`UT-common-23`） | 子のプロセス。共通の準備の `atexit` での制限 | 子の中で `start_log` の後に何もせず最後まで進む | 終了コード 1。標準エラー出力に G6（`{reason}` は `File too large`）。標準出力に L3 は出ない |
| `UT-analyze_terrain_common-27` | 始まりの行の引数（`UT-common-32`・`-33`） | 子のプロセス（2 つの子を別々に） | 子の中で、(a) 引数 `--config`・`/a b`・`it's`・空の引数、(b) 改行を 1 つ含む 1 つの引数（`x` の後に改行、その後に `y`）で `start_log` | (a) ログファイルの最初の行の、時刻と空白の後の文面が `開始: test_common --config '/a b' 'it'"'"'s' ''`（標準出力の最初の行は時刻なしの同じ文面）。(b) ログファイルの最初の 2 行が、時刻と空白の後に `開始: test_common 'x` と `y'`（2 行目にも時刻が付く）、標準出力の最初の 2 行が時刻なしの同じ 2 つの文面 |
| `UT-analyze_terrain_common-28` | 標準出力が切れたパイプ（`UT-common-40`） | 子のプロセス（2 つの子を別々に）。`start_log` の後に、共通の準備の切れたパイプを記述子 1 に付ける | (a) `throw ExitRequest(2)`、(b) `log_info("x")` | (a) 終了コード 2、ログファイルの最後の行が L3 で終了コード 2。(b) 終了コード 1、ログファイルに G7（`予期しない例外で止まった: std::system_error: 標準出力: Broken pipe`）と、最後の行の L3 で終了コード 1 |
| `UT-analyze_terrain_common-29` | 標準エラー出力が切れたパイプ（`UT-common-41`） | 子のプロセス。`start_log` の後に、共通の準備の切れたパイプを記述子 2 に付ける | `throw std::runtime_error("x")` | 終了コード 1。ログファイルに G7 の 2 行（`std::runtime_error: x`）がこの順にあり、その後が L3 で終了コード 1 |
| `UT-analyze_terrain_common-30` | G5 を画面に出せない（`UT-common-35`） | 子のプロセス。`start_log` の後に、共通の準備の `RLIMIT_FSIZE` でログファイルに書けなくし、切れたパイプを記述子 2 に付ける | `try { log_info("x"); } catch (const std::exception&) { log_info("CAUGHT"); }` | 終了コード 1。標準出力に `CAUGHT` が出ない（G5 の出力の失敗でも `ExitRequest` が上がる） |
| `UT-analyze_terrain_common-31` | 捕まえ忘れた `ExitRequest` | 子のプロセス。共通の準備の `UT-analyze_terrain_common-31` の形（`catch (...) { std::terminate(); }` だけ） | 子の中で `start_log` の後に `throw ExitRequest(2)` | 終了コード 2。G7 は出ない。ログファイルの最後の行は L3 で終了コード 2 |
| `UT-analyze_terrain_common-32` | 終了コードの定数（`UT-common-26`） | 同じプロセス。なし | `EXIT_OK`・`EXIT_ERROR`・`EXIT_USAGE` | 0・1・2 |
| `UT-analyze_terrain_common-33` | シグナルの後の後始末で例外（`UT-common-37`） | 子のプロセス | 子の中で `start_log` の後に、`try { kill(getpid(), SIGTERM); check_signal(); } catch (...) { throw std::runtime_error("cleanup"); }` | 終了コード 143。G7（`std::runtime_error: cleanup`）が標準エラー出力とログファイルに出る。ログファイルの最後の行が `SIGTERM` を受けて止まった形の L3 で終了コード 143 |
| `UT-analyze_terrain_common-34` | 前の止まり方が残らない | 同じプロセスで `load_config` を CF1 で止めて（存在しないパス）`ExitRequest` を捕まえた後に、子のプロセスを起こす | 子の中で `start_log` の後に何もせず最後まで進む | 子の終了コードが 0、ログファイルの最後の行が L3 で終了コード 0 |
| `UT-analyze_terrain_common-35` | 呼ぶ側が `ExitRequest` を捕まえて続ける（`UT-common-36`） | 子のプロセス。共通の準備の `RLIMIT_FSIZE` で書き込みを失敗させる | 子の中で `start_log` の後に、`try { log_info("x"); } catch (const ExitRequest&) { std::exit(EXIT_OK); }`（1.2 の規約に反する書き方を、わざと試す） | 終了コード 1（0 でない）。標準エラー出力に G5 が 1 回出る。ログファイルに終わりの行が無い |

Python の `UT-common-24`（ロック）・`-25`（取得完了の記録のパス）・`-27`〜`-29`（変換）・`-34`（終わる途中で画面に出せない）・`-42`（全キーの名前の一覧）に当たるケースは持たない。CMP4 にロック・取得完了の記録・全キーの名前の一覧が無く、変換は 6.10 の群が持ち、終わる途中の画面の失敗は `_finish_log` が無視するだけで別の形にならないため。`-36`（`LogWriteError` を捕まえて続ける）は `-35` が受ける。
