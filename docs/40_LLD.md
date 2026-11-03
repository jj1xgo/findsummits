# findsummits - 詳細設計書 (LLD)

| 項目 | 内容 |
|---|---|
| 作成日 | 2026-10-18 |
| 最終更新日 | 2026-11-03 |
| ステータス | ドラフト |
| 参照 HLD | [`30_HLD.md`](30_HLD.md) |

---

**読み方**: この文書は詳細設計書（LLD）である。概要設計書（HLD）が決めたプログラムと関数の名前、受け取るもの、返すものの上に、関数ごとの細部（型、内部のデータの持ち方、メッセージの文面、ファイルへの割り付け）を足す（書き分けは[文書管理ルール](CLAUDE.md#hld-と-lld-の書き分け)）。LLD の次は実装フェーズ（COD）と単体テスト（UT）で、LLD の字句と上位の文書だけで、コードと単体テストのコードを書ける細かさにすることを目標にする（2026-10-18 に持ち主が決めた）。コードを書く側は、LLD に加えて、ユーザー要件定義書（URD）、ソフトウェア要件仕様書（SRS）、HLD と、関連する文書を読める前提にする。上位の文書に決まっていることは写さずにリンクで指し、どの文書にも決まっていないことをこの文書で決め切る。章立てとモジュールの単位は、アーキテクチャ決定記録（ADR）の [ADR-LLD-001](decisions/ADR-LLD-001-lld-format-module-granularity-and-t2-timing.md) による。今は 2.1 共通部品と 3.1 `preprocess_boundaries`（行政区域前処理）と 4.1 `fetch_tiles`（タイル取得）と 5.1 `run_pipeline`（パイプライン制御）と 5.2 `resolve_config`（設定解決）と 6.1 `analyze_terrain_launch`（地形解析エンジンの起動）と 6.2 `analyze_terrain_target`（地形解析エンジンの対象）と 6.3 `analyze_terrain_window`（地形解析エンジンの窓と省略）と 6.4 `analyze_terrain_grid`（地形解析エンジンのタイルとグリッド）と 6.5 `analyze_terrain_image`（地形解析エンジンの標高地形図）と 6.6 `analyze_terrain_scan`（地形解析エンジンの走査）と 6.7 `analyze_terrain_csv`（地形解析エンジンの CSV と早期終了）と 6.8 `analyze_terrain_zone`（地形解析エンジンのゾーン）と 6.9 `analyze_terrain_record`（地形解析エンジンの出力の記録）と 6.10 `analyze_terrain_convert`（地形解析エンジンの変換）と 6.11 `analyze_terrain_stage`（地形解析エンジンの段の進行）と 6.12 `analyze_terrain_common`（地形解析エンジンの共通部品）と 7.1 `cmp5_common`（統合・突合のコンポーネント内の共通部品）と 7.2 `merge_peaks`（ピーク候補の統合）と 7.3 `merge_zones`（ゾーンの統合）と 7.4 `check_cols`（コル充足判定）と 7.5 `match_summits`（SOTA リストとの突合）と、それらが使う分の 1 章と 2.2〜2.5 だけを書いてある。ほかのモジュールの節は、書くときに足す。

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
  - [6.11 `analyze_terrain_stage`](#611-analyze_terrain_stage)
    - [6.11.1 ファイル割付](#6111-ファイル割付)
    - [6.11.2 型とデータ](#6112-型とデータ)
    - [6.11.3 関数の細部](#6113-関数の細部)
    - [6.11.4 メッセージ文面](#6114-メッセージ文面)
    - [6.11.5 UT 候補](#6115-ut-候補)
  - [6.12 `analyze_terrain_common`](#612-analyze_terrain_common)
    - [6.12.1 ファイル割付](#6121-ファイル割付)
    - [6.12.2 型とデータ](#6122-型とデータ)
    - [6.12.3 関数の細部](#6123-関数の細部)
    - [6.12.4 メッセージ文面](#6124-メッセージ文面)
    - [6.12.5 UT 候補](#6125-ut-候補)
- [7. CMP5 統合・突合](#7-cmp5-統合突合)
  - [7.1 `cmp5_common`](#71-cmp5_common)
    - [7.1.1 ファイル割付](#711-ファイル割付)
    - [7.1.2 型とデータ](#712-型とデータ)
    - [7.1.3 関数の細部](#713-関数の細部)
    - [7.1.4 メッセージ文面](#714-メッセージ文面)
    - [7.1.5 UT 候補](#715-ut-候補)
  - [7.2 `merge_peaks`](#72-merge_peaks)
    - [7.2.1 ファイル割付](#721-ファイル割付)
    - [7.2.2 型とデータ](#722-型とデータ)
    - [7.2.3 関数の細部](#723-関数の細部)
    - [7.2.4 メッセージ文面](#724-メッセージ文面)
    - [7.2.5 UT 候補](#725-ut-候補)
  - [7.3 `merge_zones`](#73-merge_zones)
    - [7.3.1 ファイル割付](#731-ファイル割付)
    - [7.3.2 型とデータ](#732-型とデータ)
    - [7.3.3 関数の細部](#733-関数の細部)
    - [7.3.4 メッセージ文面](#734-メッセージ文面)
    - [7.3.5 UT 候補](#735-ut-候補)
  - [7.4 `check_cols`](#74-check_cols)
    - [7.4.1 ファイル割付](#741-ファイル割付)
    - [7.4.2 型とデータ](#742-型とデータ)
    - [7.4.3 関数の細部](#743-関数の細部)
    - [7.4.4 メッセージ文面](#744-メッセージ文面)
    - [7.4.5 UT 候補](#745-ut-候補)
  - [7.5 `match_summits`](#75-match_summits)
    - [7.5.1 ファイル割付](#751-ファイル割付)
    - [7.5.2 型とデータ](#752-型とデータ)
    - [7.5.3 関数の細部](#753-関数の細部)
    - [7.5.4 メッセージ文面](#754-メッセージ文面)
    - [7.5.5 UT 候補](#755-ut-候補)

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
  - ファイル: 群ごとのモジュールは `src/<群の名前>.hpp` と `src/<群の名前>.cpp` の 2 本（`<群の名前>` はモジュールの ID の `LLD-analyze_terrain_` の後の部分。6.12 は `src/common.hpp`・`src/common.cpp`。6.5 だけは、この 2 本に gist_earth の表のファイル `src/image_gist_earth.hpp` を足した 3 本〈[6.5.1](#651-ファイル割付)〉）。`main` は [6.1](#61-analyze_terrain_launch) の `src/analyze_terrain.cpp` に置く（6.1 だけは、この 2 本に `main` のファイルを足した 3 本）。UT のコードは `tests/src/test_<群の名前>.cpp`（[HLD 2.6.4](30_HLD.md#264-ディレクトリ構成)の DEC18「テストは対象と同じ名前で分ける」）。6.11 だけは、これに加えて、呼ぶ順などを確かめる `tests/src/flow_stage.cpp` とスタブの 2 本を持つ（[6.11.1](#6111-ファイル割付)）。どのファイルも先頭のコメントに `// trace: LLD-analyze_terrain_<群の名前>` を書き、テストの各ケースには `// trace: UT-analyze_terrain_<群の名前>-NN` を書く。ヘッダーは、先頭の trace のコメントの次の行を `#pragma once` にする。
  - 名前: ほかのモジュールから使う名前（HLD 3.4.3 の関数、LLD が足す型・定数・例外）はヘッダーに宣言し、名前空間に入れない。内部の関数・状態・定数は `.cpp` の無名の名前空間に置き、名前を `_` と英小文字で始める（`_zone_key`・`_nb_dy` のように。`k` で始めたり、大文字だけで書いたりしない。内部の型は、無名の名前空間に置き、`_` を付けずに下の `PascalCase` で書く。`_` と英大文字で始まる名前になるため。`_` で始まる名前はグローバルの名前空間では予約されているので、無名の名前空間の外に置かない。`_` と英大文字で始まる名前と、`__` を含む名前は、どこにも使わない）。型は `PascalCase`、関数と変数は `snake_case`、ほかのモジュールから使う定数は HLD の名前（`EXIT_OK` など）。
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
- LLD の記号（メッセージの記号など）は、`tools/lint_docs.py` の検査 H（1 文字の記号の残り。`C1`〜`C8`・`D` と数字・`K1`〜`K6`。バッククォートで囲んだ短いコード表記の中は検査しない。フェンスのコードブロックは検査する）に当たらない名前にする。2.1 と 2.2 の記号は、設定の誤り CF1〜CF7、`--mesh` の誤り A1〜A5、メッシュのリストの誤り R1〜R3、共通の場面 G1〜G7、ログファイルの行 L1〜L3、設定の相互制約 CX1、取得完了の記録の誤り FC2（4.1 と 5.1 が出す）である。5.2 の記号は、引数の誤り RA1・RA2、パスの改行 RP1、標準出力に書けないとき RW1 である。5.1 の記号は、引数の誤り PA1〜PA5、設定解決の出力の誤り RS1、起動前提条件の不足 PC1・PC2、取得完了の記録の不足 FC1（FC2 は 2.2）、前回の出力を消せないとき CO1、単独起動の案内 PG1〜PG3、ログの行 PL1〜PL9 である。2.1.3 のメッシュの読み方のテストベクトルの ID は MV-01〜MV-21、設定ファイルの書式のテストベクトルの ID は CV-01〜CV-27 である。3.1 の記号は、引数の誤り BA1〜BA4、N03 行政区域 ZIP が無いか探せない BZ1・BZ2、入力の検証 BV1〜BV8、生成と書き込みと置き換えの失敗 BF1〜BF4、新しい版の警告 BW1、ログの行 BL1〜BL5 である。4.1 の記号は、引数の誤り TA1〜TA4、起動前提条件の不足 TP1〜TP3、`--mesh` のコードを飛ばすときと版を取れないときの警告 TW1〜TW3、取得を止める応答 TG1・TG2、DEM10b がすべて未整備のメッシュ TD1、ファイルの書き込みと削除の失敗 TF1〜TF3、ログの行 TL1〜TL6、2.4 の取得範囲のテストベクトルの表 4 である。6.1 の記号は、引数の誤り LA1〜LA8 である。6.2 の記号は、`--mesh` のコードを飛ばすときの警告 TM1・TM2、対象にしなかった北方領土除外メッシュのログの行 TM3、コル未確定ピーク座標リストを読めないときと書式が違うとき UP1・UP2、対象ピークの所属メッシュが解析の対象でないとき UP3 である。6.3 の記号は、省略の判定に使う `.meshset` を読めないとき・書式が違うとき・置き場を読めないとき MS1〜MS3、タイルが 1 枚も無いメッシュがあるとき TT1、DEM10b のタイルの欠けが 1% を超える解析対象メッシュがあるとき TT2、パターンを省略したログの行 WN1 である。6.4 の記号は、読めない標高タイルがあるとき TR1 と、2.4 の bounding box の取得範囲のテストベクトルの表 8 である。6.5 の記号は、グリッドに陸地の画素が無いとき IM1、標高地形図を書けないとき IW1 である。6.6 はメッセージの記号を持たない（メッセージを出さない）。6.7 の記号は、per-mesh CSV を書けないとき CW1、早期終了の判定に読み戻す per-mesh CSV を読めないとき・書式が違うとき RB1・RB2 である。6.8 の記号は、per-mesh ピーク候補 GeoJSON を書けないとき ZW1 である。6.9 の記号は、`.meshset` を書けないとき MW1 である。6.10 はメッセージの記号を持たない（2.4 の変換のテストベクトルの表 5〜7 を使う）。6.11 の記号は、出力のディレクトリを作れないとき SD1、通常のログの行 SL1〜SL9 である。6.12 は新しいメッセージの記号を持たない（2.1・2.2 の記号を使う）。7.1 の記号は、`merged_peak.csv` を読めないとき・書式が違うとき MP1〜MP3、ピーク候補 GeoJSON を読めないとき・書式が違うとき・同じピークの同じ種類のゾーンが 2 つ以上あるとき ZF1〜ZF4 である。7.2 の記号は、引数の誤り MA1〜MA6、陸地最高峰リストの誤りと警告 LP1〜LP4・LW1・LW2、per-mesh CSV の誤りと警告 PM1〜PM3・PW1・PW2、広域で確定したピークを落としたときの警告 FW1、`merged_peak.csv` を書けないとき MF1、結果の要約 ML1〜ML3 である。7.3 の記号は、引数の誤り ZA1〜ZA5、対象の per-mesh ピーク候補 GeoJSON が無いときと置き場を読めないとき ZG1・ZG2、`merged_peak.csv` の座標が JSON の数の書き方でないとき ZN1、ゾーンの欠けたピークがあるとき ZM1、`merged_peak.geojson` を書けないとき ZO1、結果の要約 ZL1・ZL2 である。7.4 の記号は、引数の誤り KA1〜KA7、未確定のリストを書けないとき KW1・KW2、結果の要約 KL1〜KL3 である。7.5 の記号は、`merged_peak.geojson` のゾーンが `merged_peak.csv` と食い違うとき MZ1、SOTA サミットリスト CSV が無い・読めない・書式が違う・値が読めない・同じ SummitCode が重なるとき SS1〜SS5、登録変更リストが無い・読めない・XHTML として読めない・表を読めず列を特定できないとき UX1〜UX4、地域と市区町村の GeoJSON を読めない・書式が違うとき BD1・BD2、無いとき BN1・BN2、登録変更リストの知らせる行 UN1、2 つ以上の確定したピークの AZ に含まれるサミットがあるとき AO1、確定していないピークの AZ の重なり AO2、仮サミットコードの連番上限を超えるエリアがあるとき PN1・PN2、地域か市区町村のどれにも入らない点 RG1、`unmatched` のサミット UM1、SOTA 既存サミット GeoJSON を使わない・読めない・`name` を読めない Feature を飛ばした・同じコードに違う山岳名があるとき SN1〜SN4、算出表に無い標高 PT1、1 つの AZ に 2 件以上の登録 MR1、`software_version` か `gsi_tile_latest_date` を求められない MT1・MT2、XLSX の行を結べないか取り元のプロパティが無い XS1、XLSX に値を変えずに書けない文字列がある XS2、引数の誤り SA1〜SA5、出力を書けないとき SW1・SW2、不備ゲート GT1、結果の要約 SM1〜SM4 である。
- メッセージの文面は、[2.2](#22-ログとメッセージの文面) の書き方で、置き換える部分を `{名前}` で書く。
- UT 候補は、`ID`・確かめること・準備・入力・期待 の 5 列の表で、`UT-<モジュール名>-NN`（2 桁の連番。[テスト方針書 §6](02_test_policy.md#6-テストケースid命名の大枠)）ごとに 1 行で書く。準備には、入力を与える前に整えること（置くファイル、起こすプロセス、差し替えるもの、捕まえる出力）を書く。小節の前置きに名前を付けて書いた共通の準備で足りるときは、その名前を書き、ケースに固有の準備だけを足す。手動のケースは ID の直後に `（手動）` を付ける。単体テスト仕様書（`50_UT.md`）を作るときは、準備はケースの手順へ移る。
- 規則は、実装者が読むその関数の見出し（関数の細部の `#####` の見出し。群の見出しで分けたモジュールでは `######` の見出し）の下に置く。2 章の横断の節には、2 つ以上のモジュールで共有するものと、どのプログラムにも属さない項目（[ADR-LLD-001](decisions/ADR-LLD-001-lld-format-module-granularity-and-t2-timing.md) の Decision 7。Makefile のターゲット名など）だけを置き、関数の見出しの下からリンクで指す。横断の節にある規則に関数ごとの扱いがあれば、その関数の見出しの下にも書く（実装者は関数の見出しの下を読み、横断の節の段落の奥までは読まないことがあるため）。

## 2. 共通部品と横断

この章は、HLD 3.9 の共通部品のモジュール（2.1）と、HLD の「目的と範囲」の「対象外」の行で繰り返し出る項目を受ける横断の節（2.2〜2.4）を置く。横断の節は追跡の宣言を持たず、モジュールの節から指す（ADR-LLD-001 の Decision 1）。2.2〜2.5 は今は 2.1・3.1・4.1・5.1・5.2・6.1・6.2・6.3・6.4・6.5・6.6・6.7・6.8・6.9・6.10・6.11・6.12・7.1・7.2・7.3・7.4・7.5 が使う項目だけを書き、ほかのモジュールの節を書くときに足す。

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

`(x, y)` を返す。式と計算の順は [2.4](#24-言語ごとに別に実装する式のテストベクトル) の決まりのとおり。引数を検査しない（呼ぶのは CMP1（行政区域前処理）・CMP2 の関数で、渡すのは日本のメッシュの四隅。HLD 3.9 の表の「使うところ」）。CMP5（統合・突合）の `latlon_to_z15_pixel` と `is_valid_coord`（[7.1.3](#713-関数の細部)）も呼ぶ。`is_valid_coord` は、範囲の外の画素になる値（`85.05112878` など）も渡して、返った画素が範囲の中かを調べるので、この関数は引数が範囲の外でも画素の値を返す（止めず、範囲の中に丸めない）。

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

書式と出し先の正本は[HLD 2.5.3](30_HLD.md#253-利用者向けのメッセージ)と[HLD 5.7.2](30_HLD.md#572-処理の流れ)で、ここは文面と行の形を決める。CMP4（地形解析エンジン）の C++ の `start_log` など、同じ決まりを別の言語で実装するモジュール（[6.12](#612-analyze_terrain_common)）も、ここの文面と行の形にする。今は 2.1・3.1・4.1・5.1・5.2・6.1・6.2・6.3・6.4・6.5・6.7・6.8・6.9・6.11・6.12・7.1・7.2・7.3・7.4・7.5 が使う分だけを書いてある。

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

置き場の正本は HLD（[2.6.4](30_HLD.md#264-ディレクトリ構成)、[2.9.3](30_HLD.md#293-同時起動の排他)、[4.1.2](30_HLD.md#412-処理の流れ)）で、ここは HLD が LLD に送った名前を決める。今は 2.1・3.1・4.1・5.1・6.3・6.4・6.5・6.7・6.8・6.9・6.11・7.1・7.2・7.3・7.4・7.5 が使う分だけを書いてある。

- ロックファイル: `data_dir` の直下の `findsummits.lock`。中身は空のまま使い、消さない（HLD 2.9.3）。Python は `acquire_lock`、bash は `run_pipeline` の `acquire_lock` が同じ名前を使う。
- 取得完了の記録: `data_dir` の `tiles/` の直下の `fetch_complete.txt`（HLD 4.1.2 の「取得完了の記録」）。中身は、取得を終えた 1 次メッシュのコードを 1 行 1 件で、ASCII の数字 4 字に改行（LF）を付けて書く（BOM・空白・CR・空行・`#` の行を書かない。昇順に並べる）。0 件なら空のファイル。読む側（CMP2 の `fetch_tiles` の `read_fetch_record`〈[HLD 3.2.3](30_HLD.md#323-関数)〉と、bash の `run_pipeline` の `check_fetch_record`〈[5.1](#51-run_pipeline)〉。どちらもこの読み方にする）は、空のファイルを行の無い記録（0 件）とし、そのほかは最後の LF を 1 つ除いてから LF で行に分け、どの行も ASCII の数字 4 字ちょうどでなければ書式が違うとする（最後の行の後の LF は無くてもよい。同じコードの重なりは 1 件とする）。読む側が `--mesh` のファイルの読み方（空白・`#` の行を許す）にしないのは、記録がツールだけが書くファイルで、[HLD 4.1.2](30_HLD.md#412-処理の流れ)が「4 桁の数字でない行があれば」止まると決めているため（壊れた記録を読み飛ばさない）。書き方は、下の一時ファイルの決まりに従う（[4.1.3](#413-関数の細部) の `write_fetch_record`）。Python は `fetch_record_path`、bash は `run_pipeline` の `fetch_record_path` が同じ名前を使う。
- 標高タイルのキャッシュ: `data_dir` の `tiles/` の下の `<サービス名>/<z>/<x>/<y>.png`（[HLD 4.1.2](30_HLD.md#412-処理の流れ) の 7「タイルを次の順に取得する」、[SRS §8.1](20_SRS.md#81-内部データ一覧) の No.5）。サービス名とズームは、DEM5a が `dem5a_png`・DEM5b が `dem5b_png`・DEM5c が `dem5c_png` でズーム 15、DEM10b が `dem_png` でズーム 14（[4.1](#41-fetch_tiles) の `_KINDS` と同じ）。`<z>`・`<x>`・`<y>` は 10 進。書くのは 4.1 の `fetch_tiles` だけで、あるかを見るのは [6.3](#63-analyze_terrain_window) の `check_mesh_tiles`、読むのは [6.4](#64-analyze_terrain_grid) の `read_tile`（パスを組み立てるのは `build_tile_elevation`）。
- per-mesh CSV: `data_dir` の `results/csv/` の下の `<解析識別子>.csv`（[HLD 4.7.2](30_HLD.md#472-処理の流れ)、[SRS §8.1](20_SRS.md#81-内部データ一覧)）。書くのは [6.7](#67-analyze_terrain_csv) の `write_peak_csv` だけで、下の一時ファイルの決まりで `<解析識別子>.csv.tmp` に書いてから置き換える。読むのは、CMP5（統合・突合）の `merge_peaks`（[HLD 4.8.2](30_HLD.md#482-処理の流れ) の 2「読むファイルを選ぶ」は、名前が `.csv` で終わるものだけを選ぶので、`.tmp` で終わる名前は読まない。名前の読み分けは [7.1.3](#713-関数の細部)の `parse_analysis_id`）と、広域モードの 6.7 の `read_back_peak_csv`。置き場のディレクトリ（`results/csv`）を作るのは [6.11](#611-analyze_terrain_stage) の `run_normal_mode`・`run_wide_mode` で、書く側の関数は作らない（[6.11.3](#6113-関数の細部)）。
- per-mesh ピーク候補 GeoJSON: `data_dir` の `results/csv/` の下の `<解析識別子>.geojson`（通常解析だけ。[HLD 4.16.2](30_HLD.md#4162-処理の流れ)の「書き出し」、[SRS §8.1](20_SRS.md#81-内部データ一覧) の No.9、ADR-SRS-029）。書くのは [6.8](#68-analyze_terrain_zone) の `write_zone_geojson` だけで、下の一時ファイルの決まりで `<解析識別子>.geojson.tmp` に書いてから置き換える。読むのは CMP5（統合・突合）の `merge_zones`（[HLD 4.18.2](30_HLD.md#4182-処理の流れ)の 1「読むファイルを選ぶ」は `3-<meshcode>.geojson` の名前だけを選ぶので、`.tmp` で終わる名前は読まない。名前の読み分けは [7.1.3](#713-関数の細部)の `parse_analysis_id`、読み込みと書式の確かめは同じく `read_zone_features`）。
- 統合ピーク候補 work CSV: `data_dir` の `results/` の直下の `merged_peak.csv`（[HLD 4.8.2](30_HLD.md#482-処理の流れ)の 7「書き出す」、[SRS §8.1](20_SRS.md#81-内部データ一覧)）。書くのは [7.2](#72-merge_peaks) の `write_merged_peak` だけで、下の一時ファイルの決まりで `merged_peak.csv.tmp` に書いてから置き換える。読むのは CMP5 の `merge_zones`・`check_cols`・`match_summits`（[7.1.3](#713-関数の細部)の `read_merged_peak`）と、CMP3（パイプライン制御）の起動前提条件の検査（有無だけ）。消すのは CMP3 のフェーズ2 の段の始まりだけ（フェーズ3 の段の始まりでは消さず、その段の統合が書き直す。[HLD 2.10.3](30_HLD.md#2103-フェーズのやり直し)）。
- 統合ピーク候補 GeoJSON: `data_dir` の `results/` の直下の `merged_peak.geojson`（[HLD 4.18.2](30_HLD.md#4182-処理の流れ)の 5「書き出す」、[SRS §8.1](20_SRS.md#81-内部データ一覧) の No.11）。書くのは [7.3](#73-merge_zones) の `write_merged_peak_geojson` だけで、下の一時ファイルの決まりで `merged_peak.geojson.tmp` に書いてから置き換える。読むのは CMP5 の `match_summits`（[7.1.3](#713-関数の細部)の `read_zone_features`）と、CMP3 の起動前提条件の検査（有無だけ）。消すのは CMP3 で、フェーズ2 では段の始まり、フェーズ3 の段ではその段の統合で `merge_peaks` を起動する直前（[HLD 2.10.3](30_HLD.md#2103-フェーズのやり直し)。[DEC79](30_HLD.md#2104-設計判断)「フェーズ3 ではピーク候補 GeoJSON を統合直前に消す」）。
- 突合の出力: `data_dir` の `results/` の直下の `merged_summit.geojson` と `merged_summit.xlsx`（[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「出力の組み立て」の 6「書く」）。書くのは [7.5](#75-match_summits) の `write_summit_outputs` だけで、下の一時ファイルの決まりで `merged_summit.geojson.tmp`・`merged_summit.xlsx.tmp` に 2 つとも書き終えてから、`merged_summit.xlsx`、`merged_summit.geojson` の順に置き換える（2 つの出力はそろって置くか、どちらも置かない。[HLD 4.9.3](30_HLD.md#493-異常系)）。読むのは CMP6（可視化生成）の `generate_viewer`（GeoJSON。[HLD 3.6.5](30_HLD.md#365-結合のつなぎ目)の `CMP6-EXT1`）と利用者。消すのは CMP3 のフェーズ4 の始まり（[HLD 2.10.3](30_HLD.md#2103-フェーズのやり直し)）。
- コル未確定ピーク座標リスト: `data_dir` の `results/` の直下の `key_col_unresolved_peaks-<N>.csv`（`<N>` は 3〜6。[HLD 4.22.2](30_HLD.md#4222-処理の流れ)の 4「未確定のリストを書く」、[SRS §8.1](20_SRS.md#81-内部データ一覧) の No.7）。書くのは [7.4](#74-check_cols) の `write_unresolved_list` だけで、未確定のピークが 1 件以上のときだけ、下の一時ファイルの決まりで `key_col_unresolved_peaks-<N>.csv.tmp` に書いてから置き換える。有無を見るのは CMP3 の起動前提条件の検査と段の進め方（[5.1](#51-run_pipeline)）、中身を読むのは CMP4 の広域モードの [6.2](#62-analyze_terrain_target) の `read_unresolved_peaks`（N の段が `key_col_unresolved_peaks-<N−1>.csv` を読む。N は 4〜6）。消すのは CMP3 の段の始まり（[HLD 2.10.3](30_HLD.md#2103-フェーズのやり直し)）。
- 解析済みウィンドウメッシュ集合（`.meshset`）: `data_dir` の `results/csv/` の下の `<解析識別子>.meshset`（[HLD 4.4.2](30_HLD.md#442-処理の流れ) の「`.meshset` の形式」、[SRS §8.1](20_SRS.md#81-内部データ一覧) の No.13）。書くのは [6.9](#69-analyze_terrain_record) の `write_meshset` だけで、下の一時ファイルの決まりで `<解析識別子>.meshset.tmp` に書いてから置き換える。読むのは [6.3](#63-analyze_terrain_window) の `is_pattern_covered`（名前の一致で選ぶので、`.tmp` で終わる名前は読まない）と `read_meshset`。
- 標高地形図: `data_dir` の `images/` の下の `<解析識別子>_terrain.png`（[SRS §6.2.3](20_SRS.md#623-標高地形図)）。書くのは [6.5](#65-analyze_terrain_image) の `write_terrain_png` だけで、下の一時ファイルの決まりで `<解析識別子>_terrain.png.tmp` に書いてから置き換える。読むプログラムは無い（利用者が開く）。置き場のディレクトリ（`images`）を作るのは [6.11](#611-analyze_terrain_stage) の `run_normal_mode`・`run_wide_mode` で、書く側の関数は作らない（[6.11.3](#6113-関数の細部)）。
- 一時ファイル: 出力を一時ファイルに書いてから置き換えるモジュール（今は 3.1・4.1・6.5・6.7・6.8・6.9・7.2・7.3・7.4・7.5。CMP4〜CMP6 の節も、書くときにこれに従う）は、出力と同じディレクトリに、出力のファイル名の後に `.tmp` を付けた名前（`regions.geojson` なら `regions.geojson.tmp`）で一時ファイルを書く。名前は固定にする（同じ `data_dir` で動く利用者向けのコマンドは 1 つだけで〈[HLD 2.9.3](30_HLD.md#293-同時起動の排他)〉、内部の起動口は CMP3 のロックの下で動くので、名前が重ならない。プロセスの番号を入れると、強制終了のたびに一時ファイルが増え、消す決まりが別に要る）。前の起動が強制終了で残した一時ファイルは、次の起動が同じ出力を書くときに、開いて中身を捨てて上書きする。同じ出力をもう書かなければ（CMP2 で、止まった後に取らなくなったタイルなど）一時ファイルは残るが、読む側は正規の名前しか読まないので害は無く（CMP2 のタイルの一時ファイルは `.png` で終わらない。[HLD 4.1.2](30_HLD.md#412-処理の流れ) の表の後の段落）、消す決まりは置かない。手順は「書く」と「置き換える」の 2 段に分け、2 段の間に何をするか（いくつの一時ファイルを書き終えてから、どの順で置き換えるか）と、置き換えに失敗したときに一時ファイルを消すか残すか（3.1 は残し、4.1・6.5・6.7・6.8・6.9・7.2・7.3・7.4・7.5 は消す）は、そのモジュールの節で決める。書く（Python）: `open(<一時ファイル>, 'wb')`（テキストは `open(<一時ファイル>, 'w', encoding='utf-8', newline='\n')`）で開き、書き、`flush()`、`os.fsync(f.fileno())`、閉じる（`fsync` は、置き換えた後に電源が落ちて中身の無いファイルが残るのを防ぐため）。開く・書く・flush・fsync・閉じるのどれかで `OSError` になったら、その一時ファイルを `os.remove` で消してから（消せないときの `OSError` は無視する）、そのモジュールのメッセージで止まる（同じ処理で先に書き終えたほかの一時ファイルも消すかは、モジュールの節で決める）。置き換える（Python）: `os.replace(<一時ファイル>, <出力>)`。書く（C++）: `open(<一時ファイル>, O_WRONLY | O_CREAT | O_TRUNC | O_CLOEXEC, 0666)` で開き、`write` を全部書くか `EINTR` のほかの失敗まで繰り返し（[6.12.3](#6123-関数の細部) の `_write_all` と同じ形）、`fsync`、`close`（`fsync` の理由と、前の起動の残りを開いて中身を捨てて上書きすることは Python と同じ）。どれかが失敗したら、`errno` を控え、開くことに成功していて、まだ `close` を呼んでいなければ `close` し（結果は見ない。`close` が失敗したときはもう一度呼ばない。`open` が失敗したときは `close` するものが無いので呼ばない）、一時ファイルを `unlink` で消してから（消せないときは無視する。`unlink` は `open` が失敗したときも含め、どの失敗でも呼ぶ。一時ファイルの名前に、先の無いシンボリックリンクなどが残っていることがあるため）、そのモジュールのメッセージで止まる（`{reason}` は控えた `errno` の文。1.2 の C++ の規約）。置き換える（C++）: `rename(<一時ファイル>, <出力>)`。

### 2.4 言語ごとに別に実装する式のテストベクトル

HLD の [DEC6](30_HLD.md#225-設計判断決めたこと理由却下した案)「メッシュ・タイル変換の二重実装を許容」のとおり、`mesh_to_latlon`・`latlon_to_tile` を Python（2.1）・C++（CMP4 の「変換」の群。[6.10](#610-analyze_terrain_convert)）・JavaScript（`index.html` の「3.9 と同じ決まり」の群）で別に実装し、`tile_to_latlon` を Python（3.1）と C++（6.10）で別に実装し（[HLD 3.1.3](30_HLD.md#313-関数)）、`latlon_to_mesh`・`latlon_to_z15_pixel`・`z15_pixel_center_latlon` を Python（CMP5。[HLD 3.5.3](30_HLD.md#353-関数)・[3.5.4](30_HLD.md#354-コンポーネント内の共通部品)）と C++（6.10）で別に実装し、この節の表で一致を確かめる。後の 3 つの関数のテストベクトルは、[HLD 4.7.1](30_HLD.md#471-目的と範囲)の対象外の行が LLD に送っているものである。テストのコードとこの表の置き場とテストのレベルは、[テスト方針書 3.3](02_test_policy.md#33-期待値の根拠)で決めた（各言語の UT にこの表の行を写して期待値にする。[HLD 2.2.1](30_HLD.md#221-目的と範囲)の対象外の行）。今は `mesh_to_latlon`・`latlon_to_tile`・`tile_to_latlon`・`latlon_to_mesh`・`latlon_to_z15_pixel`・`z15_pixel_center_latlon` と、メッシュの取得範囲の決まりの分だけを書いてある。

計算の決まり（どの言語も IEEE 754 の倍精度で、書いた順に左から計算する。式の正本は用語集の[メッシュコード → 緯度経度](00_GLOSSARY.md#mesh-to-latlon)と[緯度経度 → XYZ タイル番号](00_GLOSSARY.md#latlon-to-tile)）。`n = 2^z` は倍精度の値にする。整数の値（`2 × aa`・`x`・`y`、下の取得範囲の決まりの 3 の `x_e`）は、割る前に倍精度にし、整数どうしの割り算をしない（C++ で整数の型のまま `x / n` と書くと整数の割り算になり、表 3 の (1, 1, 1) の経度が −180 になる）:

- `mesh_to_latlon`: 南端の緯度 = `(2 × aa) / 3`（`2 × aa` を整数で求め、3 で 1 回だけ割る）。北端の緯度 = `(2 × (aa + 1)) / 3`。西端の経度 = `100 + bb`、東端の経度 = `101 + bb`。
- `latlon_to_tile`: `n = 2^z`。`x = floor(((lon + 180) / 360) × n)`。`r = (lat × π) / 180`（`math.radians` のような 1 つの関数にまとめない。掛ける順で値が変わるため）。`y = floor(((1 − ln(tan(r) + 1 / cos(r)) / π) / 2) × n)`。`π` は言語の標準の定数（Python の `math.pi`、C++ の `std::numbers::pi`、JavaScript の `Math.PI`。どれも同じ倍精度の値）。`tan`・`cos`・`ln` は言語の標準のもの。
- `tile_to_latlon`: `n = 2^z`。北西端の経度 = `((x / n) × 360) − 180`。北西端の緯度 = `(atan(sinh(π × (1 − (2 × y) / n))) × 180) / π`（`2 × y` を先に求めて `n` で割り、`1` から引き、`π` を掛け、`sinh`、`atan`、`180` を掛け、`π` で割る。この順に計算する）。`x`・`y` は小数でもよい（[HLD 3.1.3](30_HLD.md#313-関数) の表の「タイル番号（小数を含む）」）。南東端は `x + 1`・`y + 1` を同じ式に入れる。`sinh`・`atan` は言語の標準のもの（Python の `math.sinh`・`math.atan`）。式の正本は用語集の[XYZ タイル番号 → 緯度経度](00_GLOSSARY.md#tile-to-latlon)。
- `latlon_to_mesh`: 上 2 桁 `aa = floor((lat × 3) / 2)`、下 2 桁 `bb = floor(lon) − 100`（`lat × 3` を先に求めて 2 で割る。2 で割るのは丸めが無いので、`lat × 1.5` と同じ値になる）。`aa` と `bb` がどちらも 0〜99 のときのコードは、それぞれを 2 桁の 10 進（1 桁なら前に `0`）でつないだ 4 桁。0〜99 に入らないとき（NaN を含む）の扱いは、各言語の節で決める（C++ は [6.10](#610-analyze_terrain_convert)、Python は [7.2.3](#723-関数の細部)の `latlon_to_mesh`）。四則演算と `floor` だけで決まるので、どの言語も同じコードになる。式の正本は用語集の[緯度経度 → メッシュコード](00_GLOSSARY.md#latlon-to-mesh)。
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
- テスト用の実行ファイルは、`tests/src/test_<群の名前>.cpp` ごとに 1 本の `build/test_<群の名前>`（6.12 は `build/test_common`、6.1 は `build/test_launch`、6.2 は `build/test_target`、6.3 は `build/test_window`、6.4 は `build/test_grid`、6.5 は `build/test_image`、6.6 は `build/test_scan`、6.7 は `build/test_csv`、6.8 は `build/test_zone`、6.9 は `build/test_record`、6.10 は `build/test_convert`、6.11 は `build/test_stage`。`<群の名前>` は 1.2 の C++ の規約のとおり）。そのテストのファイルと、`src/` の `.cpp` のうち `main` を持たないものすべてをコンパイルし、GoogleTest の `gtest_main` とリンクする（`main` は `gtest_main` のもの）。
- `main` の振る舞いを確かめるための試験用の実行ファイル `build/test_launch_main`: `src/analyze_terrain.cpp`・`src/launch.cpp`・`src/common.cpp` と `tests/src/stub_stage.cpp`（[6.1.5](#615-ut-候補) の段の進行のスタブ）をコンパイルしてリンクする（`gtest_main` はリンクしない。指定は CMP4 の実行ファイルと同じ）。`build/test_launch` が子のプロセスで起動する（6.1.5）。
- 呼ぶ順などを確かめる試験用の実行ファイル `build/flow_stage`（[6.11.1](#6111-ファイル割付)）: `tests/src/flow_stage.cpp`・`tests/src/stub_analysis.cpp` と、`src/stage.cpp`・`src/common.cpp`・`src/convert.cpp`・`src/target.cpp` をコンパイルし、GoogleTest の `gtest_main` とリンクする（指定はテスト用の実行ファイルと同じ）。`tests/src/test_<群の名前>.cpp` の形にしないのは、上の決まり（`main` を持たない `src/` の `.cpp` をすべてリンクする）を Makefile のパターンで当てたとき、スタブの定義が無く、本物をリンクした実行ファイルがリンクに失敗するのを避けるため（`build/test_launch_main` と同じ扱い）。この実行ファイルは `build/test_launch_main` と違い、それ自身がテストの実行ファイルなので、`make test` が実行する。
- コンパイルとリンクの指定は HLD 2.6.5 の表のとおりで、テスト用の実行ファイルは `pkg-config --cflags --libs gtest_main` を足す。インクルードの探索先に `src` を足す（`-I src`）。中間のファイルは `build/obj/` に置く。
- `make test` は、`build/test_launch_main`・`build/flow_stage` とテスト用の実行ファイルをすべてビルドし（`build/test_launch_main` は実行しない。`build/test_launch` が起動する）、`build/flow_stage` もテスト用の実行ファイルとして順に実行し、テスト用の実行ファイルを順に実行し、続けて `tests/scripts/` のテストを `venv/bin/python3 -m unittest discover -s tests/scripts -t .` で実行し、どれかが 0 以外で終われば 0 以外で終わる（HLD 2.6.5 の表の `make test`。Python の枠組みは[テスト方針書 3.4](02_test_policy.md#34-テストを先に書く進め方)）。

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

この章は、CMP4（地形解析エンジン）の `analyze_terrain`（[HLD 3.4.1](30_HLD.md#341-プログラム)の実行ファイル 1 本）を、[HLD 3.4.3](30_HLD.md#343-関数)の表の群ごとのモジュールに分けて置く（ADR-LLD-001 の Decision 3）。どのモジュールも 1.2 の C++ の規約に従う。6.1〜6.12 の 12 の群をすべて書いた（6.12 と 6.10 を先に書いたのは、ほかの群がその型と関数を使うため）。6.1 の `main` が呼ぶ `run_normal_mode`・`run_wide_mode` は 6.11 の関数で、その宣言の形は [6.1.2](#612-型とデータ) で決め、[6.11.2](#6112-型とデータ) も同じ形で宣言する（変えるときは 6.1 と 6.11 を同じ変更で直す）。CMP4 にコンポーネント内の共通部品は無い（[HLD 3.4.4](30_HLD.md#344-コンポーネント内の共通部品)）。

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

`std::string format_coord(double value)`。`value` が有限でないか、−180 より小さいか 180 より大きければ `std::invalid_argument`。そうでなければ `_format_fixed(value, 8)` を返す（小数点 8 桁。[HLD 4.7.2](30_HLD.md#472-処理の流れ) の 3）。使う側は、`filter_peak_rows`・`write_peak_csv`（`col_lat`・`col_lon`）と、6.8 の群の頂点（[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の頂点の段落）と `write_zone_geojson` が書くコルの座標（`col_lat`・`col_lon`）。

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

- パターンをまたいだ確定の積み上げと早期終了は 6.11 の UT 候補（`UT-analyze_terrain_stage-13`）に置き、書いた per-mesh CSV を CMP5 の `merge_peaks` が読めることは結合テスト（IT）で確かめる（[ADR-LLD-001](decisions/ADR-LLD-001-lld-format-module-granularity-and-t2-timing.md) の Decision 2）。

### 6.8 `analyze_terrain_zone`

- **ID**: LLD-analyze_terrain_zone
- **対応 HLD**: [3.4](30_HLD.md#34-cmp4-地形解析エンジン)・[4.16](30_HLD.md#416-fr-016-ピーク域ポリゴン生成)・[5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)・[5.9](30_HLD.md#59-nfr-009-観測可能性中間成果物の可視化)
- **ファイル**: `src/zone.hpp`・`src/zone.cpp`

関数の名前と役割は [HLD 3.4.3](30_HLD.md#343-関数) の表の「ゾーン」の群である。処理の正本は、塗りの準備が [HLD 4.16.2](30_HLD.md#4162-処理の流れ) の「準備」、閾値の条件と塗りが同じ節の 1「閾値の条件を決める」・2「塗る」、`area_complete` が 3「`area_complete` を決める」、輪郭が 4「輪郭を取る」と頂点の段落、GeoJSON が「Feature」と「書き出し」である。止まる場面は [HLD 4.16.3](30_HLD.md#4163-異常系) の「GeoJSON の書き込みに失敗する」の行、書き込みの失敗は [HLD 2.5.5](30_HLD.md#255-書き込みの失敗) である。ゾーンは通常モードだけで作り、広域モードでは作らない（[HLD 4.16.1](30_HLD.md#4161-目的と範囲)）。[HLD 5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)（再現性）は、Feature の順と、Polygon・環の並べ方と環の始まりの頂点を決め切ること、角を 6.10 の `tile_to_latlon` と 6.7 の `format_coord` で文字列にすること、GeoJSON の字句（空白、キーの順、数の書き方）を決め切ることで受ける。[HLD 5.9](30_HLD.md#59-nfr-009-観測可能性中間成果物の可視化)（観測可能性）は、Feature・`properties`・スタイルの属性を HLD 4.16.2 の「Feature」のとおりに書くことで受ける。メモリは、[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の「メモリ」の段落が挙げる訪問の印（画素ごとに 1 ビット）、塗った画素の番号の並び（待ち行列を兼ねる）、輪郭の辺を、[6.8.2](#682-型とデータ)・[6.8.3](#683-関数の細部) の形で持つことで受ける。段落が挙げていないものとして、解析単位の全行のゾーンの頂点の文字列（`RowZones`）を `write_zone_geojson` まで持つことと、GeoJSON の全文を 1 つの文字列に組むことと、`trace_outline` が環を分けるときの角の索引（歩みの角の数に比例する）と、`trace_outline` の `S`（塗った画素ごとに 8 バイト）、成分の番号（同じく 4 バイト）、2 のたどりのスタック（最悪で塗った画素の数に比例する）がある。大きさは [HLD 5.2.2](30_HLD.md#522-処理の流れ) の実測の計画の 1 で測る。[HLD 4.16.1](30_HLD.md#4161-目的と範囲) の対象外の行が LLD に送った項目（辺のつなぎ方と環の最初の頂点、一直線の頂点の除き方、訪問の印の持ち方、設定の値をキーにする丸め、GeoJSON の数と空白の書き方）は、この節で決める。4 つの関数は `check_signal` を呼ぶ（[HLD 3.4.3](30_HLD.md#343-関数) の表の後の段落が挙げる群に「ゾーン」が入っている）。区切りと遅れの上限は [6.8.3](#683-関数の細部) の前置きで決める。関数を呼ぶ順は 6.11 の `run_normal_mode` で決まる（[HLD 3.4.3](30_HLD.md#343-関数) の呼ぶ順: `filter_peak_rows` → `write_peak_csv` の後、フィルタの後のリストの行ごとに、アクティベーションゾーン、delete判定ゾーンの順に `fill_zone` → `judge_area_complete` → `trace_outline`、続けて `write_zone_geojson`、その後に `write_meshset`）。入力のフィルタの後のリストは 6.7 の `filter_peak_rows` が返す `PeakCsvRow` の並びで、書いた CSV の行と同じ順である（[6.7.2](#672-型とデータ)）。この節は、それを C++ で書くための細部を足す。1.2 の C++ の規約に従う。

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
- 訪問の印（[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の「準備」）は `std::vector<std::uint64_t>`（画素 p のビットは `marks[p / 64]` の `p % 64` ビット目）。6.11 が解析単位ごとに 1 回だけ、ゾーンの段の始まり（最初の `fill_zone` の前）に `(W × H + 63) / 64` 個の 0 で作り（最大の窓の約 46 億画素で約 0.54GiB）、行と種類ごとの `fill_zone` に同じものを渡す。`fill_zone` は塗った画素のビットを立て、返す前にそのビットだけを消す（正常に返るときは、いつもすべて 0 の状態で返る）。印を作る関数は足さない（1.2 の「LLD が足してよい名前」）。
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

シグナル: 4 つの関数とも、呼び出しごとに 1 つの数え（0 から）を持ち、下の表で「数える」とした走査の 1 回ごとに、その回の処理の前に、数えが 2²⁰ の倍数なら `check_signal()` を呼んでから、数えに 1 を足す（走査をまたいで数え続ける。最初の走査の 1 回目の前にも呼ぶ。6.6.3 の「2²⁰ の倍数のとき、その要素の前」と同じ考えを、関数全体の数えで行う）。表は、4 関数の本文（下の手順）に出てくる繰り返しを1 行ずつ載せたもので、「数えない」とした走査は理由を書く。手順に繰り返しを足したら、表に行を足す。

| 関数 | 手順 | 走査 | 数えるか | 数えない理由 |
|---|---|---|---|---|
| `fill_zone` | 範囲の判定 | 行・列の控えの配列の確保（H + W 個） | 数えない | `std::vector` の確保（H + W は最大の窓でも約 14 万） |
| `fill_zone` | 3 | 塗った画素 `pixels[i]` を 1 つ読む | 数える |  |
| `fill_zone` | 3 | 8 近傍を見る | 数えない | 1 画素につき 8 回で固定（`range.meshes` の探索は `find` の対数回） |
| `fill_zone` | 4 | 塗った画素の印を 1 つ消す | 数える |  |
| `fill_zone` | 5 | `ZoneFill` を返す | 数えない | `std::vector` の移し |
| `judge_area_complete` | 範囲の判定 | 行・列の控えの配列の確保（H + W 個） | 数えない | `std::vector` の確保 |
| `judge_area_complete` | 1 | 番号の範囲の確かめ（`pixels` の画素 1 つごと） | 数える |  |
| `judge_area_complete` | 1 | 外周の画素の確かめ（`pixels` の画素 1 つごと） | 数える |  |
| `judge_area_complete` | 2 | 塗った画素を 1 つ読む | 数える |  |
| `judge_area_complete` | 2 | 8 近傍を見て、1〜5 の順に判定する | 数えない | 1 画素につき 8 回で固定。判定は 1 回で済む（集合の探索は `find` の対数回） |
| `trace_outline` | 1 | `pixels` の写しと昇順の並べ替え（`S`） | 数えない | `std::vector` の写し・並べ替え |
| `trace_outline` | 1 | 番号の範囲と重なりの確かめ（`S` の要素 1 つごと） | 数える |  |
| `trace_outline` | 1〜3 | 塗った画素かと `S` の位置を二分探索（`binary_search`・`lower_bound`）で引く | 数えない | 1 回の引きは数十回で済む |
| `trace_outline` | 2 | 成分の番号の並びの確保 | 数えない | `std::vector` の確保 |
| `trace_outline` | 2 | 外側: `S` の画素を 1 つ見る（番号を付け済みで読み飛ばすときも） | 数える |  |
| `trace_outline` | 2 | 内側: たどりで画素を 1 つ取り出す | 数える |  |
| `trace_outline` | 2 | 4 近傍を見る | 数えない | 1 画素につき 4 回で固定 |
| `trace_outline` | 3 | `S` の画素 1 つごとに辺を作る（北・西・南・東） | 数える |  |
| `trace_outline` | 3 | 辺の並べ替え | 数えない | `std::vector` の並べ替え |
| `trace_outline` | 4 | 外側: 並べた辺を先頭から 1 本調べる（使った辺を読み飛ばすときも） | 数える |  |
| `trace_outline` | 4 | 内側: 辺を 1 本使う（歩みを 1 歩進める） | 数える |  |
| `trace_outline` | 4 | 次の辺を二分探索で引く | 数えない | 1 回の引きは数十回で済む |
| `trace_outline` | 5 | `walk` の角を 1 つ読む | 数える |  |
| `trace_outline` | 5 | 積んである角を索引で引く・上書きする | 数えない | 1 回の引き（`std::map` の探索は要素数の対数回。スタックを線形に探さない） |
| `trace_outline` | 5 | 索引の破棄（関数を出るとき。`ExitRequest` による巻き戻しを含む） | 数えない | 区切りを置けない破棄の間（下） |
| `trace_outline` | 5 | 環の取り出しと下ろし | 数えない | `std::vector` の範囲の写しと切り詰め |
| `trace_outline` | 6 | 一直線の角を除く（環の角 1 つごと） | 数える |  |
| `trace_outline` | 6 | 始まりの角を探す（環の角 1 つごと） | 数える |  |
| `trace_outline` | 6 | 環を回す | 数えない | `std::vector` の並べ替え（回転） |
| `trace_outline` | 7 | `A` を求める（環の角 1 つごと） | 数える |  |
| `trace_outline` | 7 | 成分の番号ごとの Polygon の並びの確保（成分の数 C 個） | 数えない | `std::vector` の確保 |
| `trace_outline` | 7 | Polygon と穴を組み立てる（環 1 つごと） | 数える |  |
| `trace_outline` | 7 | Polygon と穴の並べ替え | 数えない | `std::vector` の並べ替え |
| `trace_outline` | 8 | 角を文字列にする（環の角 1 つごと） | 数える |  |
| `trace_outline` | 8 | 環の終わりに始まりの角を置く | 数えない | 環ごとに 1 回で、同じ環の角の走査で数えが進む |
| `write_zone_geojson` | 1 | 行を 1 つ確かめる | 数える |  |
| `write_zone_geojson` | 1 | 環を 1 つ確かめる（頂点の数と、最初と最後の比べだけ） | 数える |  |
| `write_zone_geojson` | 2 | 接続線とコルの対象の行を探して、行を 1 つ調べる（対象でない行を読み飛ばすときも） | 数える |  |
| `write_zone_geojson` | 2 | 座標の組（[経度, 緯度] 1 つ。ゾーンの頂点、接続線の 2 点、コルとピークの 1 点のどれも）を書く | 数える |  |
| `write_zone_geojson` | 2 | 行・Polygon・環をたどって Feature の文字列に追記する | 数えない | 環ごとの座標の組を書くごとに数える（手順 1 を通った環には 4 つ以上の頂点がある）。追記は `std::string` の確保・写し |
| `write_zone_geojson` | 3 | 一時ファイルへの書き出し（`_write_all` の部分書き込みと `EINTR` の再試行）と置き換え | 数えない | 区切りを置けない書き出しの間（下） |

どの数えるループも、1 回の処理は、塗った画素・辺・角・行・座標の数に比例して回る走査を含まない（含む処理は、その走査の要素 1 つごとも数える）。受けてから止まるまでの遅れは、2²⁰ 回の処理の分まで。区切りを置けないのは、`std::vector` と `std::string` の確保・写し・切り詰め・並べ替え・破棄と、`trace_outline` の 5 の索引（`std::map`）の破棄と、`write_zone_geojson` の 3 の書き出しの間だけで、その後の最初の区切りまで延びる（書き出しの後に区切りは無いので、書き出しの間に受けたシグナルは、6.11 の次の区切りで止まる）。

範囲の判定（内部の `_center_code`）: 画素 (px, py) の中心が入るメッシュコードは、6.4 の `pixel_center_mesh({256 × x_min + px − 1, 256 × y_min + py − 1})`（`x_min`・`y_min` は `range.box`）である。画素ごとに呼ぶと `sinh`・`atan` を画素の数だけ通すので、呼ぶ関数の中で、行 py の上 2 桁と、列 px の下 2 桁を、それぞれ初めて要るときに 1 回だけ `pixel_center_mesh` で求めて控える。上 2 桁は、基準の列 `px0` と行 py の画素の `pixel_center_mesh` の先頭 2 字、下 2 桁は、列 px と基準の行 `py0` の画素の後ろ 2 字である（基準の画素 (px0, py0) は、その関数がはじめに受け取った画素で、`fill_zone` ではピーク、`judge_area_complete` では `pixels[0]`。中心が範囲の中にあるので、コードは空でない）。`pixel_center_mesh` が空の文字列を返したら、その行か列は「番号の範囲の外」と控え、その行か列の画素のコードは空の文字列とする。こうして求めたコードは、画素ごとに `pixel_center_mesh` を呼んだ値と同じである（中心の緯度は py だけ、経度は px だけで決まり〈2.4 の `z15_pixel_center_latlon`〉、`latlon_to_mesh` の上 2 桁は緯度だけ、下 2 桁は経度だけで決まる。[6.4.3](#643-関数の細部) の `build_tile_elevation` の 3 と同じ理由）。控えは行の数 H と列の数 W の配列で、関数を出るときに捨てる。画素の中心が範囲の中にあるとは、このコードが `range.meshes` にあることをいう。`range.meshes`・`japan_meshes`・`excluded_meshes` の「ある」「無い」は、すべて `std::set` のメンバーの `find`（要素数の対数回）で引く（`std::find` や `std::binary_search` を集合に使わない: 集合の探索を線形に走らせないため）。

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
5. `{std::move(pixels), 閾値の条件}` を返す（印は 4 で消し終えていて、`pixels` はこの後使わない。写さずに移す）。

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
- `mesh_to_latlon` の判定は、手順 2 の 4 に当たるたびに求める（コードごとの控えを持たない: 控えの型と破棄が前置きの規則に合わなくなるのを避けるため。`mesh_to_latlon` は 4 桁のコードの整数変換と加減乗除だけで、定数回で済む）。

##### trace_outline

`std::vector<ZonePolygon> trace_outline(const std::vector<std::int64_t>& pixels, const GridRange& range)`

[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の 4「輪郭を取る」と頂点の段落を、次の 1〜8 で行う（[DEC71](30_HLD.md#4164-設計判断)「輪郭は塗った画素の境界をたどる」・[DEC72](30_HLD.md#4164-設計判断)「穴は内側の環として出す」）。

1. 呼ぶ側の誤り: `range.z14` が真、`pixels` が空。W・H は、`fill_zone` の 1 の式で `range.box` から求める。`pixels` を写して昇順に並べ（`S`）、0 以上 W × H 未満でない番号か、重なる番号があれば `std::invalid_argument`。塗った画素かは、(px, py) がグリッドの中（px が 0〜W − 1、py が 0〜H − 1）のときだけ `std::binary_search(S, py × W + px)` で引き、グリッドの外は塗っていないとする。2 で成分の番号を読み書きするときの `S` の位置は、`std::lower_bound(S, 番号)` で求め、指す値が番号と等しいことを確かめて `it - S.begin()` を添字にする（`binary_search` は真偽だけなので位置には使わない。`S` を先頭から探さない）（隣は番号の足し引きでなく (px, py) から求める。px が 0 の画素の西の隣を番号 − 1 で引くと、前の行の東の端の画素と取り違えるため）。外周の画素を受けてもよい。
2. 4 連結の成分の番号: `S` の順に、まだ番号の無い画素から 4 近傍（北・西・南・東）でたどって、同じ番号を付ける（番号は 0 から、見つけた順。`S` と同じ数の `std::uint32_t` の並びで持つ）。たどりは、`S` の位置を積む `std::vector` を明示のスタックにして行う（再帰は使わない: 成分が大きいと呼び出しの深さが画素の数に比例し、スタックを使い切るため）。
3. 辺: `S` の各画素 (px, py) について、北・西・南・東の順に、隣が塗っていなければ、塗った画素を左に見る向きの単位の辺を 1 本作る。角の座標で、北は (px + 1, py) から西へ、西は (px, py) から南へ、南は (px, py + 1) から東へ、東は (px + 1, py + 1) から北へ。辺は、始まりの角・向き・その画素の成分の番号を持つ。辺を（始まりの cy、始まりの cx、向き〈東・北・西・南の順〉）の昇順に並べる。どの角でも、そこから出る辺は 1 本か 2 本で、2 本なのは塗った画素が斜めにだけ接する角だけである。
4. たどる: 並べた辺を先頭から見て、使っていない辺 e から閉じた歩みを作る。角の並び `walk = {e の始まり}`、`cur = e` にする。`cur` を使った印にし、`cur` の終わりの角 v から出る辺を、3 の並びから引く（二分探索）。1 本ならそれを、2 本なら `cur` の向きを左に 90 度回した向き（東→北→西→南→東）の辺を、次の辺にする（いまたどっている塗った画素の側に曲がり、斜めの塗った画素へは渡らない。[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の 4）。次が e なら歩みを閉じる。そうでなければ v を `walk` に足し、`cur` を次の辺にして続ける。歩みの辺は、どれも e と同じ成分の番号を持つ（左へ曲がる規則は、4 近傍でつながる画素の辺だけをたどる）。
5. 環を分ける: `walk` を先頭から読み、角をスタックに積む。積んである角がまた来たら、スタックのその角から上を、その角で閉じた 1 つの環として取り出し、その角を残してそれより上を下ろす。「積んである」かは、角 (cx, cy) からスタックの位置への索引（`std::map`。`std::unordered_map` は使わない: 最悪の引きと再配置の手間が要素数に比例し、遅れの上限を保証できないため）の 1 回の引きで決め、引いた位置がスタックの中にあって、そこの角がその角と同じときだけ積んであるとする（下ろした角の索引の項目は消さず、古い項目は位置の不一致で見分ける。角を積むたびにその位置で索引を上書きする。索引は `trace_outline` の間に 1 つだけ持ち（歩みごとに作り直さない）、関数を出るとき（`ExitRequest` による巻き戻しを含む）に捨てる。捨てる手間は要素数に比例するが、区切りを置けない。前置きのとおり）。スタックを先頭から線形に探さない。環の取り出しと下ろしは、`std::vector` の範囲の写しと切り詰めで行う（前置きの、区切りを置けない `std::vector` の操作に含む）。読み終えたら、スタックの残りを 1 つの環にする（[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の 4 の「同じ頂点を 2 度通る環は…その頂点で環を分ける」）。分けた環は、歩みの成分の番号を受け継ぐ。
6. 一直線の頂点を除く: 環ごとに、前の角から来る向きと次の角へ行く向きが同じ角を除く（環の前後をつないで見る。単位の辺の向きで判定するので、除く角は 1 回の見直しで決まる）。除くのは、環の角の並びを前から 1 度だけ読み、残す角だけを新しい並びに足して作り直す形で行う（角ごとに `erase` を呼ばない: 1 回の手間が環の長さに比例するため）。続けて、環を、cy が最小で、その中で cx が最小の角から始まるように回す（その角は曲がり角で、除かれない）。
7. 向きと Polygon: 環ごとに、角 (cx, cy) の並び（閉じる前）で `A = Σ (x_{i+1} × y_i − x_i × y_{i+1})`（添字は環の前後をつなぐ。角の座標を `std::int64_t` に直してから掛け、`std::int64_t` で足す。`int` のまま掛けない）を求める。正なら外周（地図の上で反時計回り）、負なら穴（時計回り）である。0 にはならない。各成分の外周はちょうど 1 つで、成分ごとに 1 つの Polygon を作り、同じ成分の番号の穴を、その Polygon の穴にする。成分の番号は 0 から C − 1 の連番なので、長さ C の Polygon の並びを先に確保し、環ごとにその環の成分の番号の位置へ、外周なら外周に、穴なら穴の末尾に入れる（Polygon や環を探し直さない。環 1 つの手間が環の数に比例する実装にしない）。（[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の 4 の「各穴は、それを囲む外周…のうち最も内側のもの」と同じ結果になる。理由は下の箇条）。Polygon は外周の始まりの角の (cy, cx) の昇順（北が先、同じなら西が先）、同じ Polygon の穴も始まりの角の (cy, cx) の昇順に並べる（[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の「Feature」の並べ方。環の始まりは最も北で最も西の角なので、その角を比べる）。並べ替えは安定な並べ替えにする（同じ角を始まりに持つ環は無いが、あっても結果が決まる）。
8. 角を文字列にする: 角 (cx, cy) は、全球の Z15 の画素の角 (gx, gy) = (256 × x_min + cx − 1, 256 × y_min + cy − 1) である。`c = tile_to_latlon(static_cast<double>(gx), static_cast<double>(gy), 23)` の `lat`・`lon` を `format_coord` で文字列にする（[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の頂点の段落。画素の中心でなく角なので、0.5 を足さない）。環の終わりに、始まりの角をもう一度置く。

- 穴の帰属: 穴の環の辺の左はどれも、その成分 C の塗った画素なので、穴は C の外周の内側にある。C の外周より内側にあって、この穴を囲む外周 O があるとすると、O は C の画素の一部を内側に含み、C は 4 近傍でつながっていて O の辺（O の成分の画素と、その外の画素の間の辺）を越えないので、C 全体が O の内側にあり、C の外周が O の内側に来て矛盾する。よって、穴を囲む外周のうち最も内側のものは、C の外周である。UT 18 が、乱数の塗りで、すべての画素の中心の内外を確かめる。
- 環は同じ角を 2 度通らず、外周と穴は 1 つの角で接することがある（OGC が許す。DEC71・DEC72）。

##### write_zone_geojson

`void write_zone_geojson(const std::vector<PeakCsvRow>& rows, const std::vector<RowZones>& zones, const std::string& analysis_id, const std::string& csv_dir)`

1. 呼ぶ側の誤り（ファイルに触れる前に、この順に確かめ、最初に当たったもので投げる）: `csv_dir` が空か最後のバイトが `/`。`analysis_id` が通常の解析識別子の形でない（`_check_analysis_id_normal`。広域モードは GeoJSON を書かない。[HLD 4.16.1](30_HLD.md#4161-目的と範囲)）。`zones.size()` が `rows.size()` と違う。行ごとに（`rows` の順に）: `lat_text`・`lon_text` のどちらかが `_parse_decimal` で読めない、`key_col_resolved` が真で `col_lat` か `col_lon` が有限でないか ±180 の外（`format_coord` が投げる）、`delete_zone`・`activation_zone` のどちらかが空、どれかの環の頂点が 4 つ未満か、最初と最後の頂点の `lat_text`・`lon_text` のどちらかが違う（両方が同じ文字列でなければ誤り）。`lat_text`・`lon_text` と頂点の文字列は、`format_coord` の文字列を受ける前提で、JSON の数の字句として正しいか（先頭の `+`、整数部の先頭の `0` など）は確かめない（`lat_text` の検査は、空と数でない文字列を止めるため。頂点の文字列は確かめない）。
2. 中身（下の「GeoJSON の書き方」）を組み立てる。Feature は [HLD 4.16.2](30_HLD.md#4162-処理の流れ) の「Feature」の順: delete判定ゾーン（すべての行）、アクティベーションゾーン（すべての行）、接続線（`key_col_resolved` が真で、`col_lat`・`col_lon` がどちらも 0.0 でない行）、コル（接続線と同じ行）、ピーク（すべての行）。同じ種類の中は `rows` の順。Polygon の並び、穴の並び、環の始まりの頂点は、`trace_outline` が決めた形のまま書く（`write_zone_geojson` は並べ替えず、並びを確かめる誤りも置かない。[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の「Feature」の並べ方〈北が先、同じなら西が先〉は、`trace_outline` の 7 が満たす）。
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
| `UT-analyze_terrain_zone-05` | 印を使い回す | 同じプロセス。UT 01 のグリッド | 同じ印で UT 01 の呼び出しを 2 回 | 2 回とも UT 01 の期待と同じ（閾値の条件は `{97500, false}`、塗った画素は (300,100)・(301,100)・(299,101)・(298,102)・(297,103)、先頭は (300,100)）。2 回目の後も印はすべて 0 |
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
| `UT-analyze_terrain_zone-23` | 置き場が無い | 同じプロセス。`csv_dir` は存在しないパス | UT 21 の入力（行もゾーンも空、`analysis_id` `3-5235`。UT 20 の入力は使わない） | `code` 1。`ERROR: per-mesh ピーク候補 GeoJSON を書けない: <csv_dir>/3-5235.geojson: No such file or directory` と `対処: <csv_dir> の空きと権限を確かめてから、止まったコマンドを同じ引数で起動し直す（それより前のメッシュの出力は残っていて、起動し直すと書き直す）` |
| `UT-analyze_terrain_zone-24` | 置き換えに失敗する | 同じプロセス。`3-5235.geojson` という名前の空のディレクトリ | UT 20 の入力 | `code` 1 の ZW1（`Is a directory`）。`.tmp` が無い。ディレクトリは残る |
| `UT-analyze_terrain_zone-25` | 書く途中で失敗する | 子のプロセス（書けない）。親が `3-5235.geojson` に `old` を置く。上限は (a) 0、(b) 5 | 子で UT 20 の入力 | (a)(b) とも子の終了コード 1、標準エラー出力が ZW1（`File too large`）の 2 行。`3-5235.geojson` の中身は `old` のまま。`.tmp` が無い |
| `UT-analyze_terrain_zone-26` | `write_zone_geojson` の呼ぶ側の誤り | 同じプロセス。UT 20 の入力を基本にし、1 つだけ替える | (a) `csv_dir` が空、(b) 末尾が `/`、(c) `analysis_id` が `4-5439-NW`、(d) `3-523`、(e) ゾーンが 1 つ少ない、(f) 1 行目の `lat_text` が空、(g) 1 行目の `col_lon` が NaN、(h) 2 行目の `activation_zone` が空、(i) 1 行目の delete判定ゾーンの外周の頂点が 3 つ、(j) 同じ外周の最後の頂点が最初と違う | どれも `std::invalid_argument`。標準エラー出力に何も出ない。`csv_dir` の下にファイルができない（(a)(b) を除く） |
| `UT-analyze_terrain_zone-27` | シグナルで止まる | 子のプロセス。小さいグリッドは UT 01 と同じ。子は 4 つ（関数ごと） | 子の中で `start_log` の後に、`kill(getpid(), SIGTERM)` の後で、(a) UT 01 の `fill_zone`、(b) UT 07 の `judge_area_complete`、(c) UT 12 の (a) の `trace_outline`、(d) UT 20 の入力の `write_zone_geojson` | どれも `ExitRequest` の `code` が 143（数えが 0 の区切りの `check_signal`）。子の終了コードが 143。(d) は、親が作っておいた `csv_dir` に `3-5235.geojson` も `.tmp` もできない（区切りが書き出しより前にある） |

- UT 27 のあとに: 途中の区切り（数えが 2²⁰ の倍数のとき）は、前もって送ったシグナルを入り口の区切りが必ず先に受けるので、UT から決まった点で受けさせられない。時間に頼る試験は不安定なので置かず、区切りの置き場はコードの読み合わせで確かめる（6.6.5 の UT 15 も入り口で止まることを確かめる形）。

UT 20 の入力（行は 3 つ。`PeakColRow` の書かない欄は既定の値）:

- 行 1: `lat_text` `34.99999777`、`lon_text` `135.00002146`、`key_col_resolved` 真、`col_lat` 35.01234567891、`col_lon` 135.1。
- 行 2: `36.00465613`・`139.99880075`、偽、`col_lat`・`col_lon` 0.0。
- 行 3: `34.99999777`・`135.00006437`、真、`col_lat`・`col_lon` 0.0（海面確定）。
- 環（頂点は（緯度, 経度）の文字列）: A = (`35.1`,`135.1`)・(`35.0`,`135.1`)・(`35.0`,`135.2`)・(`35.1`,`135.2`)・(`35.1`,`135.1`)。B = (`35.3`,`135.3`)・(`35.2`,`135.3`)・(`35.2`,`135.4`)・(`35.3`,`135.4`)・(`35.3`,`135.3`)。H = (`35.08`,`135.12`)・(`35.08`,`135.18`)・(`35.02`,`135.18`)・(`35.02`,`135.12`)・(`35.08`,`135.12`)。
- ゾーン: 行 1 は delete が [{A, [H]}]・真、activation が [{A}]・真。行 2 は delete が [{B}, {A}]・偽（`trace_outline` が返す並び〈北が先〉に合わせた。`write_zone_geojson` は並べ替えずに渡された順に書く）、activation が [{B}]・真。行 3 は delete が [{B}]・真、activation が [{A}]・偽。

UT 20 の期待（13 行。各行は `\n` で終わる）:

```text
{"type":"FeatureCollection","features":[
{"type":"Feature","properties":{"peak_lat":34.99999777,"peak_lon":135.00002146,"feature_type":"delete_zone","area_complete":true,"_color":"#ef6c00","_weight":2,"_opacity":1,"_fill":false},"geometry":{"type":"Polygon","coordinates":[[[135.1,35.1],[135.1,35.0],[135.2,35.0],[135.2,35.1],[135.1,35.1]],[[135.12,35.08],[135.18,35.08],[135.18,35.02],[135.12,35.02],[135.12,35.08]]]}},
{"type":"Feature","properties":{"peak_lat":36.00465613,"peak_lon":139.99880075,"feature_type":"delete_zone","area_complete":false,"_color":"#ef6c00","_weight":2,"_opacity":1,"_fill":false},"geometry":{"type":"MultiPolygon","coordinates":[[[[135.3,35.3],[135.3,35.2],[135.4,35.2],[135.4,35.3],[135.3,35.3]]],[[[135.1,35.1],[135.1,35.0],[135.2,35.0],[135.2,35.1],[135.1,35.1]]]]}},
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

- 6.7 の `filter_peak_rows` から 6.8 の 4 関数をつなぐケース（通常モードの 1 メッシュで、CSV と GeoJSON のピークの文字列が同じこと）は、複数のモジュールの関数のつながりを確かめるので、6.11 の UT 候補（`UT-analyze_terrain_stage-18`）に置く（[ADR-LLD-001](decisions/ADR-LLD-001-lld-format-module-granularity-and-t2-timing.md) の Decision 2）。書いた GeoJSON を CMP5（統合・突合）の `merge_zones` が読むケースは、結合テスト（IT）の `IT-CMP5-EXT2-02` で確かめる。ここでは、出力のバイト列（UT 20）で、`merge_zones` が受ける形を確かめる。読む側の UT（[7.1.5](#715-ut-候補)の `UT-cmp5_common-19`）は、UT 20 の期待のバイト列をそのまま入力にする。

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

- 書いた `.meshset` を 6.3 の `read_meshset` で読み戻して、同じ集合になることを確かめるケースは、2 つのモジュールの関数のつながりを確かめるので、6.11 の UT 候補（`UT-analyze_terrain_stage-17`）に置く（[ADR-LLD-001](decisions/ADR-LLD-001-lld-format-module-granularity-and-t2-timing.md) の Decision 2）。ここでは、出力のバイト列（UT-analyze_terrain_record-01〜03）で、6.3 の `read_meshset` が受ける形を確かめる。

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

### 6.11 `analyze_terrain_stage`

- **ID**: LLD-analyze_terrain_stage
- **対応 HLD**: [3.4](30_HLD.md#34-cmp4-地形解析エンジン)・[4.4](30_HLD.md#44-fr-004-33メッシュ結合解析オーケストレーション)・[4.14](30_HLD.md#414-fr-014-広域結合解析オーケストレーション)・[5.5](30_HLD.md#55-nfr-005-処理時間目標)
- **ファイル**: `src/stage.hpp`・`src/stage.cpp`

関数の名前と役割は [HLD 3.4.3](30_HLD.md#343-関数) の表の「段の進行」の群（`run_normal_mode`・`run_wide_mode`）で、処理の正本は通常モードが [HLD 4.4.2](30_HLD.md#442-処理の流れ) の 2〜5、広域モードが [4.14.2](30_HLD.md#4142-処理の流れ) の 2〜5、止める場面は [4.4.3](30_HLD.md#443-異常系)・[4.14.3](30_HLD.md#4143-異常系)、途中経過と結果の要約は [HLD 5.7.2](30_HLD.md#572-処理の流れ) の 5「途中経過」・7「結果の要約」（その中身の表の `analyze_terrain` の 2 行）である。この 2 関数は、6.1 の `main` が `start_log` の後に呼び、ほかの群の関数を [HLD 3.4.3](30_HLD.md#343-関数) の呼ぶ順のとおりに呼んで取りまとめる。宣言の形は [6.1.2](#612-型とデータ) で決めてあり、6.11.2 も同じ形で宣言する。6.2〜6.9 の各節が「6.11 が…」と書いた呼び方（引数に渡す値、ディレクトリを作ること、メッセージを出すこと、解放の順）は、6.11.3 がすべて受ける。この節は、それを C++ で書くための細部と、段の始まり・途中経過・結果の要約・出力のディレクトリを作れないときのメッセージの文面を足す。1.2 の C++ の規約に従う。

- [HLD 5.5](30_HLD.md#55-nfr-005-処理時間目標)（処理時間目標）は、メッシュごとの所要時間を、ST の手順で 1 メッシュ分の始まりから終わりまでを測る区間として測り、製品のログに内訳の行を足さない（[HLD 5.5.2](30_HLD.md#552-処理の流れ) の 4「内訳の測り方」）ことで受ける。6.11.4 の SL1・SL3 は [HLD 4.4.2](30_HLD.md#442-処理の流れ)・[4.14.2](30_HLD.md#4142-処理の流れ)・5.7.2 が求める行で、内訳の行ではない。
- [HLD 5.2](30_HLD.md#52-nfr-002-メモリ使用量)（メモリ使用量）は ADR-LLD-001 の表で 6.11 の受け手ではないので、追跡の宣言には入れない。ただし、6.5・6.6・6.8 が決めた解放の順と、訪問の印を解析単位ごとに 1 回だけ作ることは、呼ぶ側として 6.11.3 の「メモリ」で守る。
- [HLD 5.7](30_HLD.md#57-nfr-007-ログ出力)（ログ出力）の書き込みは 6.12 が受け持つ。6.11 は [2.2](#22-ログとメッセージの文面) の形で、途中経過と結果の要約の中身を決める。

#### 6.11.1 ファイル割付

- 公開の宣言は `src/stage.hpp`、定義と内部の関数は `src/stage.cpp` に置く。どちらも先頭のコメントに `// trace: LLD-analyze_terrain_stage` を書き、ヘッダーは次の行を `#pragma once` にする。
- `src/stage.hpp` は `"common.hpp"`（`Config`）・`<set>`・`<string>` を読む。`src/stage.cpp` は `"stage.hpp"`・`"common.hpp"`・`"target.hpp"`・`"window.hpp"`・`"grid.hpp"`・`"image.hpp"`・`"scan.hpp"`・`"csv.hpp"`・`"zone.hpp"`・`"record.hpp"` と、`<algorithm>`・`<cerrno>`・`<cstdint>`・`<cstring>`・`<set>`・`<string>`・`<sys/stat.h>`・`<utility>`・`<vector>` を読む。OpenCV のヘッダーは直接読まない（`grid.hpp` が core を読む）。
- UT のコードは 2 本の実行ファイルに分ける（理由は [6.11.5](#6115-ut-候補) の前置き）。各テストに `// trace: UT-analyze_terrain_stage-NN`（確かめる UT 候補の ID）のコメントを付ける。テストの枠組みは GoogleTest（[テスト方針書 3.4](02_test_policy.md#34-テストを先に書く進め方)）。
  - `tests/src/test_stage.cpp` → `build/test_stage`（[2.5](#25-ビルドとテストの名前)の決まりどおり、`main` を持たない `src/` の `.cpp` をすべてリンクする。2 つのモジュールの関数のつながりを確かめるケース）。
  - `tests/src/flow_stage.cpp` と、スタブの `tests/src/stub_analysis.hpp`・`tests/src/stub_analysis.cpp` → `build/flow_stage`（呼ぶ順などを確かめるケース。[2.5](#25-ビルドとテストの名前)）。スタブの 2 本は、先頭のコメントにスタブを使うケースの ID を並べて書く（`// trace: UT-analyze_terrain_stage-01, …, UT-analyze_terrain_stage-16`。`tools/lint_trace.py` が `tests/src/` の下のファイルごとにテストケースの ID を求めるため。[6.1.1](#611-ファイル割付) の `stub_stage.cpp` と同じ）。
  - 名前を `test_<群の名前>` の形にしないのは、[2.5](#25-ビルドとテストの名前)の「`tests/src/test_<群の名前>.cpp` ごとに 1 本、`main` を持たない `src/` の `.cpp` をすべてリンクする」を Makefile のパターンで当てたとき、本物をリンクした実行ファイルが別にできて、スタブの定義が無くリンクに失敗するのを避けるため（6.1 の `build/test_launch_main`・`tests/src/stub_stage.cpp` も形の外の名前）。

#### 6.11.2 型とデータ

`src/stage.hpp` の公開の宣言は次のとおり（名前空間に入れない。1.2 の C++ の規約）。

```cpp
#pragma once
#include <set>
#include <string>
#include "common.hpp"

void run_normal_mode(const std::string& japan_mesh_list, bool has_mesh,
                     const std::set<std::string>& mesh_codes, const Config& config);
void run_wide_mode(const std::string& japan_mesh_list, int n,
                   const std::string& unresolved, const Config& config);
```

- 宣言の形は [6.1.2](#612-型とデータ) のとおり（引数の並びは [HLD 3.4.3](30_HLD.md#343-関数) の表の受け取るものの順）。公開の型は足さない。`has_mesh` が偽なら `mesh_codes` は空で、HLD の「なし」に当たる。止まるときは `ExitRequest` を投げ、最後まで進んだら戻る。
- 内部の定数（`src/stage.cpp` の無名の名前空間）:
  - コーナーの並び `_corners`: `{"NW", "NE", "SW", "SE"}`（[HLD 4.14.2](30_HLD.md#4142-処理の流れ) の 4「対象メッシュごとに、昇順に次を行う」の 2 の順）。
  - 除外リストの案内 `_excluded_guidance`: [6.11.4](#6114-メッセージ文面) の文。
  - 段の名前（SL1 の `{stage}`）: 通常は `標高地形図`・`ピーク候補とコル`・`per-mesh CSV`・`per-mesh ピーク候補 GeoJSON`・`.meshset`。広域は `解析範囲標高グリッド`・`標高地形図`・`ピーク候補とコル`・`per-mesh CSV`・`.meshset`。
- 件数（関数の中の局所の変数。要約に使う。`std::size_t` で持ち、`std::to_string` で 10 進にする）:
  - 通常: `targets`（対象メッシュの数）、`csv_meshes`（per-mesh CSV を書いたメッシュの数）、`rows_total`（書いたピークの行の数の合計）。
  - 広域: `peaks`（対象ピークの数）、`meshes`（対象メッシュの数）、`analyzed`（解析したパターンの数）、`skipped`（省略したパターンの数）、`rows_total`。
  - `targets`・`peaks`・`meshes` は、決まる前は「未定」で、要約には `-` と書く。未定は `bool` の印で持つ（1.2。`std::optional` を使わない）。
  - 途中経過（SL3）のために、終えた対象メッシュの数 `done`（`std::size_t`、初めは 0）と、前に出した割合の整数部 `last_pct`（`std::size_t`、初めは 0）も局所の変数に持つ。対象メッシュを 1 つ終えるたびに `done` を 1 増やし、`done * 100 / total` が `last_pct` より大きいときだけ SL3 を出して `last_pct` を替える（2.2）。
- 「どこで止まったか」を示す文字列 `where`（SL6・SL9 の `{where}`。[6.11.4](#6114-メッセージ文面)）も局所の変数に持つ。モジュールの状態は持たない（2 関数とも、件数を自分の中だけで数えて自分で要約を出すので、ほかの関数に渡す必要が無い）。

#### 6.11.3 関数の細部

処理の正本は上の前置きのとおりで、この節は C++ で書くための細部を足す。

前置き（2 関数に共通）:

- **止まり方**: 1.2 の C++ の規約のとおり。6.11 自身が止める場面は SD1 だけで、ほかは呼んだ関数が出して `ExitRequest` を投げ、6.11 は捕まえずにそのまま上げる。呼ぶ側の誤り（`std::invalid_argument`）も同じ（6.11 が渡す値は、各節が決めた形に合わせて組み立てる）。
- **要約の書き方**: 本体を 1.2 の「結果の要約」の `try`/`catch (...)` の形で書く。
  - `catch (...)` の中で、途中で止まった要約（SL6・SL9）を `log_info` で出し、`throw;` で投げ直す。`try` は 1 つだけで、要約は `catch` の中で 1 回だけ出す。
  - `ExitRequest` 以外の例外（`std::invalid_argument`、`std::bad_alloc` など）でも要約が出て、その後に 6.12 の `_on_terminate` が G7 で止める。
  - 要約の `log_info` がログの書き込みの失敗で `ExitRequest` を投げたら、それがそのまま上がる（6.12 の `_emit`）。
  - 正常に終えたとき（対象が 0 件のときを含む）は、`try` を抜けた後に SL4・SL5（広域は SL7・SL8）を出して戻る。
- **件数を増やす時機**: 書き込みが成功した後にだけ増やす（[HLD 5.7.2](30_HLD.md#572-処理の流れ) の 7「結果の要約」の「そこまでに終えた分」を正しく数えるため）。`csv_meshes` と `rows_total` は `write_peak_csv` が戻った後、`analyzed` は `read_back_peak_csv` が戻った後、`skipped` は WN1 を出した後。
- **パス**: `data_dir` は `config.values.at("data_dir").text`（空でなく先頭が `/` とだけ決まっているので、末尾が `/` のことがある。6.12.2）。次のとおり、内部の `_join` で組み立てる。
  - `_join(a, b)` は 6.12.3 の `_join` と同じ決まり（`a` が `/` で終われば `a + b`、そうでなければ `a + "/" + b`）。6.12 の内部の関数は `src/common.cpp` の外から呼べないので、同じ形を置く。
  - `tiles_dir = _join(data_dir, "tiles")`、`csv_dir = _join(data_dir, "results/csv")`、`images_dir = _join(data_dir, "images")`、除外リストは `_join(data_dir, "boundaries/nt_excluded_meshes.txt")`（[HLD 4.4.2](30_HLD.md#442-処理の流れ) の 2「入力を読む」。置き場の名前は [HLD 4.17.2](30_HLD.md#4172-処理の流れ)）。
  - どれも末尾に `/` が付かない（6.3・6.4・6.9 が、末尾が `/` の `csv_dir`・`tiles_dir` を呼ぶ側の誤りにするため）。`data_dir` が `//` で終わる値のときは途中に `//` が残るが、末尾ではないので 6.3・6.4・6.9 の確かめに当たらず、OS も同じパスとして扱う。
  - 広域の per-mesh CSV の読み戻しのパスは `csv_dir + "/" + analysis_id + ".csv"`（6.7）。
- **ディレクトリを作る**: 内部の `_make_dirs`（6.12.3 の `_make_dirs` と同じ決まり。先頭からの各段に `mkdir(<段>, 0777)`。途中の段の `EEXIST` は次へ進み、最後の段の `EEXIST` は `stat` でディレクトリかを見る。同じ形を置く）で、`csv_dir`、`images_dir` の順に作る。
  - 失敗したら、SD1（`{path}` は作れなかったディレクトリ〈`csv_dir` か `images_dir`〉、`{reason}` は失敗の `errno` の `std::strerror`）を出して `throw ExitRequest(EXIT_ERROR)`。
  - 作る時機は、対象が 1 件以上と決まった後、最初の対象メッシュの前。0 件のときは作らない（[HLD 4.4.3](30_HLD.md#443-異常系)・[4.14.3](30_HLD.md#4143-異常系) の「何もせずに終わる」）。リストの読み込みなど、ここより前で止まるときも作らない。
  - 広域でも作るのは、`results/csv` は通常解析が作っているのが普通でも、`images` が無いことがある（広域の段から起動したとき）ため。作れなければ、ほかの関数の `ENOENT` による失敗より先に分かる。
- **シグナルの区切り**: 6.11 は次で `check_signal()` を呼ぶ。対象メッシュ 1 つの始まり、広域のパターン 1 つの始まり、SL1（段の始まり）を出す直前。対象メッシュとパターンの始まりでは、その繰り返しの `where`（通常の対象メッシュと広域のパターンは、識別子 `id` も）を決めてから呼ぶ（始まりで止まったときの要約の `{where}` が、まだ始めていない繰り返しを指し、前の繰り返しを指さないため）。
  - 6.11 自身は区切りの間に時間のかかる処理を置かない（件数を数え、文字列を組み、集合を和にするだけ）。そのため、受けてから止まるまでの遅れの上限は、受けた時点から次の区切り（6.11 の区切りか、呼んだ関数の中の区切り）までに残る呼び出しの所要の合計になる。
  - `check_signal` を呼ぶ群（グリッド・走査・ゾーン）の中では、その節が決めた上限。呼ばない群（標高地形図・CSV と早期終了・出力の記録・窓と省略・対象）は、区切りの間に続けて呼ぶ分の所要の合計（たとえば SL1 の「標高地形図」の直後に受けたときは、`render_terrain` と `write_terrain_png` の 2 つを終えてから、次の SL1 の前で止まる）。
- **メモリ**: 6.5・6.6・6.8 が決めた解放の順を、次のとおり守る。
  - 標高地形図の画像（`TerrainImage`）は、`write_terrain_png` の後、走査の前に捨てる。
  - 走査の順は `scan_peaks_and_cols` の後、`build_col_list` の前に捨てる。
  - 成分ごとのデータは `build_col_list` の後に捨てる。
  - 捨てるのは、変数をブロックの中に置いてブロックを抜けるか、`std::vector<T>().swap(v)` で、`clear()` だけにしない（容量が残るため）。
  - 通常モードの訪問の印は、メッシュ（解析単位）ごとに 1 回、ゾーンの段の始まり（最初の `fill_zone` の前）に作る（走査の後なので、成分ごとのデータと同時に持たない。6.8.2）。行が 0 行でも作る（作らない場合分けを足さない）。
  - 広域モードのグリッドは、`build_col_list` の後に捨てる（後の段は `range` だけを使う）。通常モードのグリッドは、ゾーンが使うので、`write_meshset` までメッシュのブロックの中に置く。

#### `run_normal_mode`

1. `where = "入力の読み込み"`、`targets` は未定、`csv_meshes = 0`、`rows_total = 0` にして、ここから `try` に入る。
2. 日本全土のリスト `japan = read_mesh_list_file(japan_mesh_list, "")`（案内は空で、既定の対処）、続けて北方領土除外メッシュのリスト `excluded = read_mesh_list_file(<除外リストのパス>, _excluded_guidance)` を読む（この順。[HLD 4.4.2](30_HLD.md#442-処理の流れ) の 2「入力を読む」）。
3. `t = select_target_meshes(japan, excluded, has_mesh, mesh_codes)`。`t.skipped` を順に、`excluded` が真なら TM2、偽なら TM1 を `log_warning` で 1 件ずつ出す（`{list_path}` は `japan_mesh_list`。6.2.4）。続けて `t.not_targeted` を順に TM3 で `log_info` に 1 件ずつ出す。`targets = t.targets.size()` にする（未定でなくなる）。
4. `t.targets` が空なら、`try` を抜けて SL5 を出し、戻る（終了コード 0。[HLD 4.4.2](30_HLD.md#442-処理の流れ) の 3「対象メッシュを決める」）。
5. `where = "出力のディレクトリの用意"`。`csv_dir`・`images_dir` を作る（前置きの「ディレクトリを作る」）。
6. `target_set` を `t.targets` の集合にする。`t.targets` を順に（昇順）、各 `code` について次を行う。
   1. `id = "3-" + code`、`where = id + " の解析"` にしてから、`check_signal()`。
   2. `window = normal_window(code, target_set)` → `check_mesh_tiles(window, tiles_dir, true)` → `GridResult g = build_grid_z15(window, tiles_dir)`。
   3. 標高地形図: `check_signal()` と SL1（`標高地形図`）→ ブロックの中で `TerrainImage image = render_terrain(g.grid, g.range, id)` → `write_terrain_png(image, id, images_dir)`。ブロックを抜けて画像を捨てる。
   4. ピーク候補とコル: `check_signal()` と SL1（`ピーク候補とコル`）→ `order = make_scan_order(g.grid)` → `components = scan_peaks_and_cols(g.grid, order)` → `order` を捨てる → `components = apply_sea_level_rule(std::move(components))` → `col_rows = build_col_list(components, g.grid.width, g.grid.height, g.range)` → `components` を捨てる。
   5. per-mesh CSV: `check_signal()` と SL1（`per-mesh CSV`）→ `rows = filter_peak_rows(col_rows, g.range, id, config.values.at("prominence_primary_m").integer, {})` → `col_rows` を捨てる → `write_peak_csv(rows, id, csv_dir)` → `csv_meshes += 1`、`rows_total += rows.size()`。
   6. ゾーン: `check_signal()` と SL1（`per-mesh ピーク候補 GeoJSON`）→ 訪問の印 `marks` を `(static_cast<std::int64_t>(g.grid.width) * g.grid.height + 63) / 64` 個の 0 の `std::vector<std::uint64_t>` で作る。
      - `rows` の各行について、アクティベーションゾーン（`ZoneKind::Activation`）、delete判定ゾーン（`ZoneKind::Delete`）の順に、`f = fill_zone(row, kind, g.grid, g.range, <activation_zone_drop_m>, <delete_zone_max_drop_m>, marks)` → `complete = judge_area_complete(f.pixels, f.threshold, g.grid, g.range, japan, excluded)` → `polygons = trace_outline(f.pixels, g.range)` を行う。
      - 設定の 2 つ（`activation_zone_drop_m`・`delete_zone_max_drop_m`）は `config.values.at(...).integer` をそのまま渡す。`japan`・`excluded` は 2 で読んだ集合を、そのまま渡す。
      - 結果を、その行の `RowZones` の `activation_zone`・`activation_complete`（または `delete_zone`・`delete_complete`）に入れる。`RowZones` を行の順に `zones` に足す（`rows` と同じ数・同じ順）。
      - 続けて `write_zone_geojson(rows, zones, id, csv_dir)`。
   7. `.meshset`: `check_signal()` と SL1（`.meshset`）→ `write_meshset(window, id, csv_dir)`。6 で止まったときは呼ばれない（例外で抜けるため。[HLD 4.16.3](30_HLD.md#4163-異常系)）。
   8. SL3 の途中経過を出す（`{done}` は終えたメッシュの数、`{total}` は `targets`。2.2 の途中経過の形で、前に出した割合の整数部より増えたときだけ出す）。
7. `try` を抜けて SL4 を出し、戻る。

#### `run_wide_mode`

1. `where = "入力の読み込み"`、`peaks`・`meshes` は未定、`analyzed = skipped = rows_total = 0` にして、ここから `try` に入る。
2. `japan`・`excluded` を `run_normal_mode` の 2 と同じに読む。`peak_list = read_unresolved_peaks(unresolved, n)`、`peaks = peak_list.size()` にする（未定でなくなる）。
3. `peak_list` が空なら、`try` を抜けて SL8 を出し、戻る（終了コード 0。[HLD 4.14.2](30_HLD.md#4142-処理の流れ) の 2「入力を読む」）。
4. `where = "対象メッシュの決定"`。`groups = group_peaks_by_mesh(peak_list, japan, excluded)`、`meshes = groups.size()` にする（未定でなくなる）。存在メッシュ `existing` を、`japan` から `excluded` を除いた集合にする（[HLD 4.14.2](30_HLD.md#4142-処理の流れ) の前置き）。
5. `where = "出力のディレクトリの用意"`。ディレクトリを作る（前置きの「ディレクトリを作る」）。
6. `groups` の鍵の順（昇順）に、各 `target` と組 `group` について次を行う。
   1. `where = target + " の 3×3 の検査"` にしてから、`check_signal()`。続けて `check_mesh_tiles(normal_window(target, existing), tiles_dir, false)`。
   2. 確定済みの集合 `confirmed`（`std::set<Z15Pixel>`）を空にする（対象メッシュごとに作り直す）。
   3. `_corners` を順に、各 `corner` について次を行う。
      1. `id = std::to_string(n) + "-" + target + "-" + corner`、`where = id + " の解析"` にしてから、`check_signal()`。
      2. `window = pattern_window(target, n, corner, existing)` → `cover = is_pattern_covered(csv_dir, target, window, n)`。`cover.covered` が真なら、WN1（`{meshset}` は `cover.meshset_path`）を `log_info` で出し、`skipped += 1` にして、次のコーナーへ進む。
      3. `check_mesh_tiles(window, tiles_dir, true)`。
      4. グリッド: `check_signal()` と SL1（`解析範囲標高グリッド`）→ `GridResult g = build_grid_z14(window, group, tiles_dir)`。
      5. 標高地形図とピーク候補とコル: `run_normal_mode` の 6 の 3・4 と同じ。ただし `build_col_list` の後に `g.grid` も捨てる。
      6. per-mesh CSV: `check_signal()` と SL1（`per-mesh CSV`）→ `rows = filter_peak_rows(col_rows, g.range, id, config.values.at("prominence_primary_m").integer, group)`（広域では読まれない値。6.7.2）→ `col_rows` を捨てる（`run_normal_mode` の 6 の 5 と同じ）→ `write_peak_csv(rows, id, csv_dir)` → `rows_total += rows.size()`。
      7. `.meshset`: `check_signal()` と SL1（`.meshset`）→ `write_meshset(window, id, csv_dir)`。
      8. 早期終了の判定: `got = read_back_peak_csv(csv_dir + "/" + id + ".csv", group, n)` → `analyzed += 1` → `confirmed` に `got` を足す（パターンをまたいだ和）。`group` のすべての `TargetPeak` の `pixel` が `confirmed` にあり、まだ行っていないコーナーがあれば、SL2 を `log_info` で出して、コーナーの繰り返しを抜ける（[HLD 4.14.2](30_HLD.md#4142-処理の流れ) の 4「対象メッシュごとに、昇順に次を行う」の 2 の 10「早期終了を判定する」）。最後のコーナー（`SE`）で確定したときは、打ち切るパターンが無いので SL2 を出さない。後ろのコーナーが 1 つでも残っていれば、それが `is_pattern_covered` で省略されるものでも SL2 を出す（省略かどうかは、そのコーナーの番になるまで分からないため）。
   4. SL3 の途中経過を出す（`{done}` は終えた対象メッシュの数、`{total}` は `meshes`）。
7. `try` を抜けて SL7 を出し、戻る。

ほかの内部の関数: `_join`・`_make_dirs`（前置き）と、要約の文を組む関数（名前は実装者が決める）。どれも無名の名前空間に置き、名前を `_` で始める（1.2）。

#### 6.11.4 メッセージ文面

書き方は [2.2](#22-ログとメッセージの文面)。TM1〜TM3 は [6.2.4](#624-メッセージ文面)、WN1 は [6.3.4](#634-メッセージ文面)、R1〜R3 は [2.1.4](#214-メッセージ文面) の文面のまま。日本全土1次メッシュコードリストの R1〜R3 の案内は空（既定の対処）。北方領土除外メッシュリストの案内 `_excluded_guidance` は、次の文にする。

`venv/bin/python3 scripts/preprocess_boundaries.py を起動して北方領土除外メッシュリストを作ってから、止まったコマンドを同じ引数で起動し直す（設定ファイルを指定して起動したときは、どちらにも同じ --config を付ける）`

6.11 は起動のしかたを知らないので、[5.1.4](#514-メッセージ文面) の除外リストの案内にある `{config_opt}` の代わりに、括弧で書く。ほかの関数が出すもの（MS1〜MS3・TT1・TT2・TR1・IM1・IW1・CW1・RB1・RB2・ZW1・MW1・UP1〜UP3）は、6.11 は出さない。

`ERROR:` のメッセージ（2 行目は `対処:` と空白 1 つの後）:

| 記号 | 場面 | 1 行目 | 2 行目 | 終了コード |
|---|---|---|---|---|
| SD1 | 出力のディレクトリを作れない | `出力のディレクトリを作れない: {path}: {reason}` | 通常: `{path} とその上のディレクトリの権限を確かめてから、止まったコマンドを同じ引数で起動し直す`。広域: `{path} とその上のディレクトリの権限を確かめてから、scripts/run_pipeline.sh --phase 3 --n {n} を起動し直す（設定ファイルを指定して起動したときは、同じ --config を付ける）` | 1 |

- `{path}` は作れなかったディレクトリ（`csv_dir` か `images_dir`）、`{reason}` は失敗の `errno` の `std::strerror`、`{n}` は `--n` の値。SD1 は 6.11 が出す（ほかの関数は出さない）。

通常のログ（`log_info`）:

| 記号 | 行 | 文面 |
|---|---|---|
| SL1 | 段の始まり | `段の始まり: {stage}（{analysis_id}）`（`{stage}` は 6.11.2 の段の名前。[HLD 4.4.2](30_HLD.md#442-処理の流れ) の 4 の 5〜9 と [4.14.2](30_HLD.md#4142-処理の流れ) の 4 の 2 の 5〜9 の各段の始まり。`ST-FR-004-01` が出力の生成の順をこの行で確かめる） |
| SL2 | 早期終了でパターンを打ち切った | `残りのパターンを行わない（組の対象ピーク {k} 件がすべて確定した）: {target}（最後に解析したパターン {analysis_id}）` |
| SL3 | 途中経過 | 2.2 の途中経過の形。`{what}` は通常が `通常解析のメッシュ（{code} まで）`、広域が `広域解析のメッシュ（{code} まで）`（`{code}` はいま終えた対象メッシュのコード。[HLD 5.7.2](30_HLD.md#572-処理の流れ) の 5「途中経過」の 2「行にはメッシュコードも書く」）。割合の整数部が増えたときだけ出す（2.2）ので、出ないメッシュもある（175 件なら約 75 件は出ない） |
| SL4 | 結果の要約（通常・終えた） | `結果の要約: 通常解析を終えた。対象メッシュ {targets}、per-mesh CSV を書いたメッシュ {csv_meshes}、ピークの行 {rows}` |
| SL5 | 結果の要約（通常・0 件） | `結果の要約: 対象メッシュが 0 件なので解析しなかった。対象メッシュ 0、per-mesh CSV を書いたメッシュ 0、ピークの行 0` |
| SL6 | 結果の要約（通常・止まった） | `結果の要約: 途中で止まった（{where}）。対象メッシュ {targets}、per-mesh CSV を書いたメッシュ {csv_meshes}、ピークの行 {rows}`（`{targets}` は未定なら `-`） |
| SL7 | 結果の要約（広域・終えた） | `結果の要約: 広域解析（N={n}）を終えた。対象ピーク {peaks}、対象メッシュ {meshes}、解析したパターン {analyzed}、省略したパターン {skipped}、ピークの行 {rows}` |
| SL8 | 結果の要約（広域・0 件） | `結果の要約: 対象ピークが 0 件なので解析しなかった（N={n}）。対象ピーク 0、対象メッシュ 0、解析したパターン 0、省略したパターン 0、ピークの行 0` |
| SL9 | 結果の要約（広域・止まった） | `結果の要約: 途中で止まった（{where}）。対象ピーク {peaks}、対象メッシュ {meshes}、解析したパターン {analyzed}、省略したパターン {skipped}、ピークの行 {rows}`（未定の数は `-`） |

- `{where}` は 6.11.3 の `where`: `入力の読み込み`・`対象メッシュの決定`（広域）・`出力のディレクトリの用意`・`<対象メッシュ> の 3×3 の検査`（広域）・`<解析識別子> の解析`。`{rows}` は `rows_total`。数は 10 進（先頭の `0` なし）。
- 要約の中身は [HLD 5.7.2](30_HLD.md#572-処理の流れ) の「結果の要約の中身」の `analyze_terrain` の 2 行だけにする（項目を足さない）。早期終了で行わなかったパターンは、解析にも省略にも数えない（省略は WN1 を出したパターンだけ）。
- SL1〜SL9 は、ログファイルに時刻付きで書き、標準出力にも時刻なしで同じ文面を出す（`log_info`）。

#### 6.11.5 UT 候補

すべて自動。ID の列の `01` などは `UT-analyze_terrain_stage-01` のことである。

- **実行ファイルを 2 本に分ける理由**: 2 関数はほかの 9 群をすべて呼ぶ。本物をつなぐと、1 メッシュでもグリッドが数億画素になり（[6.4.5](#645-ut-候補) の UT 17 は 23554 × 19202）、呼ぶ順・止まり方・要約を確かめるには重すぎる。そこで、呼ぶ順などのケース（01〜16）は、窓と省略・グリッド・標高地形図・走査・CSV と早期終了・ゾーン・出力の記録の 7 群をスタブに替えた `build/flow_stage` で確かめる。共通部品・変換・対象の 3 群は本物をリンクする（リストの読み込みと要約の出力を本物で見るため）。2 つのモジュールの関数のつながりのケース（17・18。[ADR-LLD-001](decisions/ADR-LLD-001-lld-format-module-granularity-and-t2-timing.md) の Decision 2 で 6.11 に置く）は、本物をリンクする `build/test_stage` で確かめる。

共通の準備:

- **同じプロセス**: [6.12.5](#6125-ut-候補) の同じ名前の準備と同じ。設定は、一時のディレクトリ `<tmp>` に `[paths]` の `data_dir = <tmp>/data` だけの設定ファイルを書き、`load_config(<パス>, <6.1.2 の _load_keys の 6 キー>, {"data_dir"})` で作る（デフォルトで `prominence_primary_m` が 130、`activation_zone_drop_m` が 25、`delete_zone_max_drop_m` が 250）。`<tmp>/data/boundaries/nt_excluded_meshes.txt` と日本全土のリスト `<tmp>/japan.txt` をケースの中身で書く（ケースが書かなければ、日本全土は `5235\n5236\n6848\n`、除外は `6848\n`）。止まるケースは `ExitRequest` を捕まえて `code` を確かめる。
- **子のプロセス**: 6.12.5 の同じ名前の準備と同じ形（`fork` の前の `std::fflush(nullptr)`、記述子 1・2 をパイプに付け替えること、`main` の形の `try`/`catch` と `std::exit`）で、値は次のとおりに替える。設定ファイルは「同じプロセス」と同じ中身に `log_dir = <tmp>/logs` を足したもの、`load_config` の `keys` は 6.1.2 の `_load_keys` の 6 キー（`required` は `data_dir`）、`start_log` のプログラムの名前は `flow_stage`、引数は空の並び。ログファイルは `<tmp>/logs` の下の `flow_stage_*_<子の PID>.log`。入力の列の関数は `start_log` の後に呼ぶ。
- **スタブ**（`tests/src/stub_analysis.hpp`・`.cpp`）: 7 群の、6.11 が呼ぶ関数だけを、各群のヘッダーの宣言のまま定義する。どれも最初に `log_info("stub: " + <下の表の行>)` を出す。その後、台本 `stub_script` を見て、次のどれかをしてから下の表の値を返す。
  - `fail` が `<関数名>#<k>`（その関数の k 回目の呼び出し。k は 1 から）なら、`log_error("stub", "stub")` の後に `throw ExitRequest(EXIT_ERROR)`。
  - `runtime` が同じ形で当たれば、`throw std::runtime_error("stub runtime")`。
  - `signal` が当たれば、`raise(SIGTERM)` の後に普通に返す。
  - `stub_reset()` は、台本と呼び出しの回数を初期の値に戻す（各ケースの始めに呼ぶ）。
  - 台本の項目は `fail`・`runtime`・`signal`（既定は空）、`rows`（`build_col_list` が返す行の数。既定は 2）、`cover`（`is_pattern_covered` の k 回目が `covered` を返すかの並び。足りなければ偽）、`confirm`（`read_back_peak_csv` の k 回目に返す `peaks` の添字の並びの並び。足りなければ空）、`normal_window_set`・`pattern_window_set`（`normal_window`・`pattern_window` が返す集合を、`,` でつないだメッシュコードで書いた字句。既定は空で、空のときは下の表の中心／対象メッシュだけの集合を返す。返した集合が後ろの関数に渡ることを確かめるケースだけが決める）。
  - 集合は昇順に `,` でつなぐ。空の集合と空の並びは `-`。真偽は `1`・`0`。

  | 関数 | 出す行（`stub:` と空白 1 つの後） | 返す値 |
  |---|---|---|
  | `normal_window` | `normal_window {center} {meshes}` | `normal_window_set` が空でなければその集合、空なら `{center}` だけの集合 |
  | `pattern_window` | `pattern_window {target} {n} {corner} {existing}` | `pattern_window_set` が空でなければその集合、空なら `{target}` だけの集合 |
  | `is_pattern_covered` | `is_pattern_covered {csv_dir} {target} {window} {n}` | `covered` は `cover` の k 番目、真なら `meshset_path` は `/m/{k}.meshset` |
  | `check_mesh_tiles` | `check_mesh_tiles {meshes} {tiles_dir} {check_dem10b}` | なし |
  | `build_grid_z15` | `build_grid_z15 {meshes} {tiles_dir}` | グリッドは W = 4・H = 3、`values` は 12 個の `0.0f`。`range.meshes` は `meshes`、`z14` は偽 |
  | `build_grid_z14` | `build_grid_z14 {meshes} {peaks の数} {tiles_dir}` | 同じで `z14` は真 |
  | `render_terrain` | `render_terrain {W}x{H} {analysis_id}` | 1 × 1 の画像 |
  | `write_terrain_png` | `write_terrain_png {analysis_id} {images_dir}` | なし |
  | `make_scan_order` | `make_scan_order {W}x{H}` | `{0}` |
  | `scan_peaks_and_cols` | `scan_peaks_and_cols {order の数}` | 既定の `Component` 1 つ |
  | `apply_sea_level_rule` | `apply_sea_level_rule {数}` | 受けたまま |
  | `build_col_list` | `build_col_list {components の数} {width} {height}` | 既定の `PeakColRow` を `rows` 個 |
  | `filter_peak_rows` | `filter_peak_rows {rows の数} {analysis_id} {prominence_primary_m} {peaks の数}` | `rows` と同じ数の `PeakCsvRow`。i 番目（0 から）の `lat_text` は `r{i}`、ほかは既定の値 |
  | `write_peak_csv` | `write_peak_csv {rows の数} {analysis_id} {csv_dir}` | なし |
  | `read_back_peak_csv` | `read_back_peak_csv {path} {peaks の数} {n}` | `confirm` の k 番目の添字の `peaks[i].pixel` の集合 |
  | `fill_zone` | `fill_zone {A か D} {row.lat_text} {activation_zone_drop_m} {delete_zone_max_drop_m} {marks の数}` | `pixels` は `{0}`、`threshold.exclusive` は D なら真 |
  | `judge_area_complete` | `judge_area_complete {pixels の数} {japan_meshes} {excluded_meshes}` | `threshold.exclusive` |
  | `trace_outline` | `trace_outline {pixels の数}` | 既定の `ZonePolygon` 1 つ |
  | `write_zone_geojson` | `write_zone_geojson {rows の数} {zones の数} {行ごとの印} {analysis_id} {csv_dir}` | なし |
  | `write_meshset` | `write_meshset {meshes} {analysis_id} {csv_dir}` | なし |

  `write_zone_geojson` の `{行ごとの印}` は、`zones` の各要素を `A` と `activation_complete`（`1`・`0`）、`D` と `delete_complete` を続けた 4 字（`A0D1` など）にして、順に `,` でつないだもの（`zones` が空なら `-`）。

- **期待の書き方**: 「標準出力」は時刻の無い行の並び。`<tiles>`・`<csv>`・`<images>` は `<tmp>/data/tiles`・`<tmp>/data/results/csv`・`<tmp>/data/images`。「1 メッシュの並び（`{id}`、`{w}`）」は次の行の並びのこと（`{code}` は対象メッシュのコード、`{w}` は `run_normal_mode` が `normal_window` の第 2 引数に渡す対象メッシュの集合を昇順に `,` でつないだもの、`{j}`・`{x}` は日本全土と除外のリストの集合で、既定のリストなら `5235,5236,6848`・`6848`）。
  1. `stub: normal_window {code} {w}`
  2. `stub: check_mesh_tiles {code} <tiles> 1`
  3. `stub: build_grid_z15 {code} <tiles>`
  4. SL1（`標高地形図`）
  5. `stub: render_terrain 4x3 {id}`
  6. `stub: write_terrain_png {id} <images>`
  7. SL1（`ピーク候補とコル`）
  8. `stub: make_scan_order 4x3`・`stub: scan_peaks_and_cols 1`・`stub: apply_sea_level_rule 1`・`stub: build_col_list 1 4 3`
  9. SL1（`per-mesh CSV`）
  10. `stub: filter_peak_rows 2 {id} 130 0`・`stub: write_peak_csv 2 {id} <csv>`
  11. SL1（`per-mesh ピーク候補 GeoJSON`）
  12. 行 `r0`・`r1` の順に、行ごとに `stub: fill_zone A r{i} 25 250 1`・`stub: judge_area_complete 1 {j} {x}`・`stub: trace_outline 1`・`stub: fill_zone D r{i} 25 250 1`・`stub: judge_area_complete 1 {j} {x}`・`stub: trace_outline 1`（2 行分）
  13. `stub: write_zone_geojson 2 2 A0D1,A0D1 {id} <csv>`
  14. SL1（`.meshset`）
  15. `stub: write_meshset {code} {id} <csv>`

  広域の「1 パターンの並び（`{id}`、`{corner}`、`{k}` 件のピーク）」は次の行の並びのこと。
  1. `stub: pattern_window 5235 4 {corner} 5235,5236`
  2. `stub: is_pattern_covered <csv> 5235 5235 4`
  3. `stub: check_mesh_tiles 5235 <tiles> 1`
  4. SL1（`解析範囲標高グリッド`）
  5. `stub: build_grid_z14 5235 {k} <tiles>`
  6. 通常の 4〜8 と同じ行
  7. SL1（`per-mesh CSV`）
  8. `stub: filter_peak_rows 1 {id} 130 {k}`・`stub: write_peak_csv 1 {id} <csv>`
  9. SL1（`.meshset`）
  10. `stub: write_meshset 5235 {id} <csv>`
  11. `stub: read_back_peak_csv <csv>/{id}.csv {k} 4`

  広域のケース（11〜16）は、台本の `rows` を 1 にする（11 の準備に書いた。上の 1 パターンの並びの `filter_peak_rows 1`・`write_peak_csv 1` の 1 は、この値）。

ケース（`build/flow_stage`。準備は「同じプロセス」とスタブ。10 だけ「子のプロセス」）:

| ID | 確かめること | 準備（ケースに固有のもの） | 入力 | 期待 |
|---|---|---|---|---|
| `UT-analyze_terrain_stage-01` | 通常の呼ぶ順と引数 | (a) なし。(b) 台本の `rows` を 0。(c) 台本の `normal_window_set` を `5235,5236` | `run_normal_mode("<tmp>/japan.txt", true, {"5235"}, config)` | 戻る。(a) 標準出力は TM3（`6848`）、1 メッシュの並び（`3-5235`、`5235`）、SL3（`途中経過: 通常解析のメッシュ（5235 まで） 1/1（100%）`）、SL4（`対象メッシュ 1、per-mesh CSV を書いたメッシュ 1、ピークの行 2`）の順で、ほかの行は無い。(b) 1 メッシュの並びの 8 の `build_col_list` の行（`stub: build_col_list 1 4 3`。台本の `rows` によらない）を含め、(a) と同じ行のうち、10 は `stub: filter_peak_rows 0 3-5235 130 0`・`stub: write_peak_csv 0 3-5235 <csv>`、12 の行が無く、13 は `stub: write_zone_geojson 0 0 - 3-5235 <csv>`、SL4 は `ピークの行 0`。(c) は (a) と同じ行のうち、1 メッシュの並びの 2 が `stub: check_mesh_tiles 5235,5236 <tiles> 1`、3 が `stub: build_grid_z15 5235,5236 <tiles>`、15 が `stub: write_meshset 5235,5236 3-5235 <csv>`（`normal_window` が返した集合が後ろの関数に渡る）。どれも標準エラー出力は空。`<csv>` と `<images>` がディレクトリとしてある |
| `UT-analyze_terrain_stage-02` | 飛ばしたコードの警告の順 | なし | `mesh_codes` を `{"5235", "6848", "9999"}` | 標準エラー出力は TM2（`6848`）の 2 行、TM1（`9999`、`{list_path}` は `<tmp>/japan.txt`）の 2 行の順。標準出力の最初の行は TM3（`6848`）で、その後は 01 と同じ |
| `UT-analyze_terrain_stage-03` | 対象が 0 件 | なし | `mesh_codes` を `{"9999"}` | 戻る。標準エラー出力は TM1（`9999`）の 2 行だけ。標準出力は TM3、SL5 だけ（`stub:` の行が無い）。`<tmp>/data/results` と `<tmp>/data/images` が無い |
| `UT-analyze_terrain_stage-04` | `--mesh` なしと途中経過 | (a) 既定のリスト。(b) 日本全土を `5000`〜`5149` の 150 件（1 行 1 件）、除外を空のファイル | `run_normal_mode(..., false, {}, config)` | (a) 標準出力は、最初に TM3（`6848`。`--mesh` なしでも出る）、続けて 1 メッシュの並びが `3-5235`（`{w}` は `5235,5236`）、`3-5236`（`{w}` は `5235,5236`）の順。SL3 は `（5235 まで） 1/2（50%）` と `（5236 まで） 2/2（100%）`。SL4 は `対象メッシュ 2、per-mesh CSV を書いたメッシュ 2、ピークの行 4`。(b) SL3 の行は 100 行で、最初は `（5001 まで） 2/150（1%）`、最後は `（5149 まで） 150/150（100%）`（`done` が 1 のときは 0% なので出ない） |
| `UT-analyze_terrain_stage-05` | リストの誤り | (a) 日本全土のリストを置かない。(b) 除外リストを置かない。(c) 除外リストを `68x1\n` にする | 01 と同じ | どれも `code` が 1。(a) R1 で対処は既定（`ファイル <tmp>/japan.txt があり、読み取れることを確かめる`）。(b) R1 で対処は除外リストの案内。(c) R3 で対処は除外リストの案内。どれも標準出力の最後は SL6（`途中で止まった（入力の読み込み）。対象メッシュ -、per-mesh CSV を書いたメッシュ 0、ピークの行 0`）で、`stub:` の行が無い |
| `UT-analyze_terrain_stage-06` | 途中のメッシュで止まる | 台本の `fail` を `write_zone_geojson#2` | 04 の (a) と同じ | `code` が 1。標準出力は、最初に TM3（`6848`）、続けて `3-5235` の 1 メッシュの並びと SL3（`1/2（50%）`）があり、`3-5236` の並びは `stub: write_zone_geojson` の行まで（SL1 の `.meshset` と `stub: write_meshset … 3-5236 …` が無い）。標準エラー出力は `ERROR: stub` と `対処: stub`。最後は SL6（`途中で止まった（3-5236 の解析）。対象メッシュ 2、per-mesh CSV を書いたメッシュ 2、ピークの行 4`） |
| `UT-analyze_terrain_stage-07` | ディレクトリを作れない | (a) `<tmp>/data/results` を通常のファイルにする。(b) `<tmp>/data/images` を通常のファイルにする | 01 と同じ | どちらも `code` が 1、`stub:` の行が無い。(a) SD1（通常の対処。`{path}` は `<tmp>/data/results/csv`、`{reason}` は `Not a directory`）。(b) SD1（`{path}` は `<tmp>/data/images`、`{reason}` は `File exists`。`<csv>` はできている）。どちらも最後は SL6（`途中で止まった（出力のディレクトリの用意）。対象メッシュ 1、per-mesh CSV を書いたメッシュ 0、ピークの行 0`） |
| `UT-analyze_terrain_stage-08` | `data_dir` の末尾の `/` | 設定ファイルの `data_dir` を `<tmp>/data/` にする | 01 と同じ | 01 と同じ行（`<tiles>` などに `//` が無い） |
| `UT-analyze_terrain_stage-09` | 捕まらない例外でも要約 | 台本の `runtime` を `render_terrain#1` | 01 と同じ | `std::runtime_error` が上がる。標準出力の最後は SL6（`途中で止まった（3-5235 の解析）。対象メッシュ 1、per-mesh CSV を書いたメッシュ 0、ピークの行 0`） |
| `UT-analyze_terrain_stage-10` | シグナルで止まる | 子のプロセス。(a) 台本の `signal` を `build_grid_z15#1`。(b) 台本の `signal` を `write_meshset#1` | (a) 01 と同じ。(b) 04 の (a) と同じ | (a) 子の終了コードが 143。標準出力に `stub: build_grid_z15 5235 <tiles>` はあり、`段の始まり: 標高地形図（3-5235）` と `stub: render_terrain` は無い。ログファイルの最後の 2 行は SL6（`途中で止まった（3-5235 の解析）。対象メッシュ 1、per-mesh CSV を書いたメッシュ 0、ピークの行 0`）と、`SIGTERM` を受けて止まった形の L3。(b) 子の終了コードが 143。標準出力に `stub: write_meshset 5235 3-5235 <csv>` と SL3（`（5235 まで） 1/2（50%）`）はあり、`stub: normal_window 5236 5235,5236` は無い。ログファイルの最後の 2 行は SL6（`途中で止まった（3-5236 の解析）。対象メッシュ 2、per-mesh CSV を書いたメッシュ 1、ピークの行 2`。2 つ目のメッシュの始まりの `check_signal()` で止まる）と、`SIGTERM` を受けて止まった形の L3 |
| `UT-analyze_terrain_stage-11` | 広域の呼ぶ順と引数 | 台本の `rows` を 1 にする（11〜16 のすべてで同じ。12〜16 は「11 の準備で」と書いたものを引く）。日本全土を `5235\n5236\n`、除外を空のファイル、`<tmp>/u.csv` を `peak_lat,peak_lon\n35.1,135.1\n`（所属メッシュ `5235`）。(b) は、さらに `<tmp>/u.csv` に `35.1,136.1`（所属メッシュ `5236`）の行を足す。(c) は、台本の `normal_window_set` を `5235,5335`、`pattern_window_set` を `5235,5236` にする（(c) だけ。12〜16 は引かない） | `run_wide_mode("<tmp>/japan.txt", 4, "<tmp>/u.csv", config)` | (b) は、(a) の `5235` の行（SL3 は `（5235 まで） 1/2（50%）`）の後に、`5236` について同じ形の行（`stub: normal_window 5236 5235,5236`・`stub: check_mesh_tiles 5236 <tiles> 0`、1 パターンの並びの対象メッシュの欄〈`pattern_window`・`is_pattern_covered`・`check_mesh_tiles`・`build_grid_z14`・`write_meshset` の行の最初の `5235` と、`is_pattern_covered` の窓の `5235`、解析識別子の `5235`〉を `5236` にしたもの〈存在メッシュの `5235,5236` はそのまま〉を 4 回、SL3 は `（5236 まで） 2/2（100%）`）が続き、SL7 は `対象ピーク 2、対象メッシュ 2、解析したパターン 8、省略したパターン 0、ピークの行 8`。(a) は次のとおり。戻る。標準出力は `stub: normal_window 5235 5235,5236`、`stub: check_mesh_tiles 5235 <tiles> 0`、1 パターンの並びを `4-5235-NW`・`-NE`・`-SW`・`-SE` の順に 4 回（`{k}` は 1）、SL3（`途中経過: 広域解析のメッシュ（5235 まで） 1/1（100%）`）、SL7（`広域解析（N=4）を終えた。対象ピーク 1、対象メッシュ 1、解析したパターン 4、省略したパターン 0、ピークの行 4`）の順。`stub: fill_zone`・`stub: write_zone_geojson` の行が無い。`<csv>` と `<images>` がある。(c) は (a) と同じ行のうち、3×3 の検査の行が `stub: check_mesh_tiles 5235,5335 <tiles> 0`、1 パターンの並びの 2 の窓が `5235,5236`（`stub: is_pattern_covered <csv> 5235 5235,5236 4`）、3 が `stub: check_mesh_tiles 5235,5236 <tiles> 1`、5 が `stub: build_grid_z14 5235,5236 1 <tiles>`、10 が `stub: write_meshset 5235,5236 {id} <csv>`（3×3 の窓とパターンの窓を取り違えず、それぞれの戻りが渡る） |
| `UT-analyze_terrain_stage-12` | 省略したパターン | 11 の準備で、台本の `cover` を `{false, true}` | 11 と同じ | NE は `stub: is_pattern_covered …` の次が WN1（`パターンを省略した（解析対象メッシュが /m/2.meshset に含まれる）: 4-5235-NE`）で、次の行が SW の `stub: pattern_window`。SL7 は `解析したパターン 3、省略したパターン 1、ピークの行 3` |
| `UT-analyze_terrain_stage-13` | 確定の積み上げと早期終了 | 11 の準備で、`<tmp>/u.csv` に 2 行目 `35.2,135.2`（同じく `5235`）を足す。台本の `confirm` を (a) `{{0}, {1}}`、(b) `{{0}, {}, {}, {1}}`、(c) `{{0, 1}}` | 11 と同じ | (a) NE の `stub: read_back_peak_csv` の次が SL2（`残りのパターンを行わない（組の対象ピーク 2 件がすべて確定した）: 5235（最後に解析したパターン 4-5235-NE）`）で、SW・SE の行が無い。SL7 は `対象ピーク 2、対象メッシュ 1、解析したパターン 2、省略したパターン 0、ピークの行 2`。(b) 4 パターンとも行い、SL2 が無い（SE で確定した）。(c) NW の後に SL2（`残りのパターンを行わない（組の対象ピーク 2 件がすべて確定した）: 5235（最後に解析したパターン 4-5235-NW）`）。どれも `{k}` は 2 |
| `UT-analyze_terrain_stage-14` | 対象ピークが 0 件 | 11 の準備で、`<tmp>/u.csv` を `peak_lat,peak_lon\n` だけにする | 11 と同じ | 戻る。標準出力は SL8（`（N=4）`）だけ。`<tmp>/data/results` と `<tmp>/data/images` が無い |
| `UT-analyze_terrain_stage-15` | 広域で止まる | (a) 11 の準備で、日本全土を `5235\n5236\n6848\n`、除外を `6848\n`、`<tmp>/u.csv` に `45.4,148.5`（所属メッシュ `6848`）の行を足す。(b) 11 の準備で、台本の `fail` を `check_mesh_tiles#1`。(c) 11 の準備で、`fail` を `write_meshset#2` | 11 と同じ | どれも `code` が 1。(a) UP3（6.2.4。標準エラー出力に `ERROR:` の行と `対処:` の行の 2 行）の後、最後は SL9（`途中で止まった（対象メッシュの決定）。対象ピーク 2、対象メッシュ -、解析したパターン 0、省略したパターン 0、ピークの行 0`）で、`stub:` の行が無い。(b) SL9（`途中で止まった（5235 の 3×3 の検査）。対象ピーク 1、対象メッシュ 1、解析したパターン 0、省略したパターン 0、ピークの行 0`）。(c) NE の `stub: read_back_peak_csv` が無く、SL9（`途中で止まった（4-5235-NE の解析）。対象ピーク 1、対象メッシュ 1、解析したパターン 1、省略したパターン 0、ピークの行 2`） |
| `UT-analyze_terrain_stage-16` | 広域のディレクトリの誤り | 11 の準備で、`<tmp>/data/results` を通常のファイルにする | 11 と同じ | `code` が 1。SD1 の 2 行目が広域の対処で `--n 4`。最後は SL9（`途中で止まった（出力のディレクトリの用意）。対象ピーク 1、対象メッシュ 1、解析したパターン 0、省略したパターン 0、ピークの行 0`） |

ケース（`build/test_stage`。本物をリンクする。準備は「同じプロセス」）:

| ID | 確かめること | 準備（ケースに固有のもの） | 入力 | 期待 |
|---|---|---|---|---|
| `UT-analyze_terrain_stage-17` | `.meshset` の書き戻しと省略の判定（6.9・6.3） | `<tmp>/csv` を作る | `write_meshset({"5235", "5236", "5335"}, "3-5235", "<tmp>/csv")` の後に、(a) `read_meshset("<tmp>/csv/3-5235.meshset", 4)`、(b) `is_pattern_covered("<tmp>/csv", "5235", {"5235", "5236"}, 4)`、(c) 同じく `{"5235", "5237"}` | (a) `{5235, 5236, 5335}`。(b) `covered` が真、`meshset_path` が `<tmp>/csv/3-5235.meshset`。(c) `covered` が偽 |
| `UT-analyze_terrain_stage-18` | フィルタの後のリストから CSV と GeoJSON まで（6.7・6.8） | [6.8.5](#685-ut-候補) の「基本の範囲」と「小さいグリッド」。画素 (300, 100) を 200m にする。`PeakColRow` を 1 行（`peak` が (300, 100)、`peak_elevation` 200、`key_col_resolved` 真、`col_elevation` 0、`prominence` 200）。`<tmp>/csv` を作る | `filter_peak_rows({<その行>}, <範囲>, "3-5235", 100, {})` → `write_peak_csv(rows, "3-5235", "<tmp>/csv")` → 行ごとに [6.11.3](#6113-関数の細部) の `run_normal_mode` の手順 6 の 6（ゾーン）の順で 6.8 の 3 関数（日本全土のリストは `{5235}`、除外のリストは空）→ `write_zone_geojson(rows, zones, "3-5235", "<tmp>/csv")` | `rows` は 1 行。`<tmp>/csv/3-5235.csv` のデータの行は 1 行。`<tmp>/csv/3-5235.geojson` の各 Feature の `properties` の `peak_lat`・`peak_lon` の数の字句（6.8.3 の書き方で `"peak_lat":` の後から次の `,` か `}` の前まで）が、CSV のその行の `peak_lat`・`peak_lon` の文字列と同じ。Feature は 3 つ（`delete_zone`・`activation_zone`・`peak` の順。`col_lat`・`col_lon` が 0.0 なので、[HLD 4.16.2](30_HLD.md#4162-処理の流れ) の「Feature」の 3・4 の線とコルは無い） |

- 書いた GeoJSON を CMP5（統合・突合）の `merge_zones` が読むことは、結合テスト（IT）の `IT-CMP5-EXT2-02`（`CMP5-EXT2`）で確かめ、6.11 の UT には置かない（CMP5 は Python で、6.11 の UT から呼べない）。書いた per-mesh CSV を `merge_peaks` が読むことは `CMP5-EXT1` の IT で確かめる。
- 解放の順（6.11.3 の「メモリ」）は UT で確かめない（スタブでは容量を見られない）。試し書きの読み合わせと、実装のレビューで見る。

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

## 7. CMP5 統合・突合

この章は、CMP5（統合・突合）の 4 本のプログラム（[HLD 3.5.1](30_HLD.md#351-プログラム)の `merge_peaks`・`merge_zones`・`check_cols`・`match_summits`）のモジュールと、コンポーネント内の共通部品（[HLD 3.5.4](30_HLD.md#354-コンポーネント内の共通部品)）のモジュールを置く（ADR-LLD-001 の Decision 3・4）。どのモジュールも Python で、1.2 の Python の決まりと [2.1](#21-共通部品) の共通部品に従う。今は 7.1〜7.5 を書いてある（共通部品を先に書くのは、ほかのモジュールがその型と関数を使うため）。

### 7.1 `cmp5_common`

- **ID**: LLD-cmp5_common
- **対応 HLD**: [3.5](30_HLD.md#35-cmp5-統合突合)・[4.7](30_HLD.md#47-fr-007-per-mesh-csv-出力プロミネンス閾値適用)・[4.8](30_HLD.md#48-fr-008-per-mesh-csv-統合)・[4.9](30_HLD.md#49-fr-009-sotaリスト突合match_status-判定)・[4.18](30_HLD.md#418-fr-018-per-mesh-ピーク候補-geojson-統合)・[4.22](30_HLD.md#422-fr-022-コル充足判定)・[5.2](30_HLD.md#52-nfr-002-メモリ使用量)
- **ファイル**: `scripts/cmp5_common.py`

部品の名前と役割と使うところは [HLD 3.5.4](30_HLD.md#354-コンポーネント内の共通部品)の表のとおりで、処理の正本はその表の「定義のある節」である。この節は、それを Python で書くための細部（型、止まり方、メッセージの 1 行目の文面）だけを足す。7 つの部品は `read_merged_peak`・`index_peaks_by_pixel`・`read_zone_features`・`latlon_to_z15_pixel`・`is_valid_coord`・`great_circle_m`・`parse_analysis_id` である。`z15_pixel_center_latlon` と `latlon_to_mesh` は、HLD 3.5.4 の表の後の段落のとおり `match_summits` と `merge_peaks` の関数なので、この節には入れない（7.5・7.2 で書く）。

- [4.7](30_HLD.md#47-fr-007-per-mesh-csv-出力プロミネンス閾値適用)（Z15 の画素の変換）は、`latlon_to_z15_pixel` の式を [2.4](#24-言語ごとに別に実装する式のテストベクトル) の計算の決まりと表 6 で CMP4（地形解析エンジン）とそろえることで受ける（HLD の [DEC6](30_HLD.md#225-設計判断決めたこと理由却下した案)「メッシュ・タイル変換の二重実装を許容」）。
- [5.2](30_HLD.md#52-nfr-002-メモリ使用量)（メモリ）は、`read_merged_peak` がファイルを 1 行ずつ読んで渡し、全体を一度に持たないこと（行に持つのは渡された列の組の列だけ）、`read_zone_features` が 1 回の呼び出しで 1 つのファイルだけを読むことで受ける。メモリのピークは、呼ぶプログラムを実装した後に、HLD 5.2.2 の「実測の計画」の 3「CMP5 の統合」で測る。
- 再現性（[HLD 5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)）は、この節に割り当てていないので宣言に入れない。`read_zone_features` が JSON の数の書き方を保つのは、呼ぶ `merge_zones` が再現性を受けるための前提である（7.3 で受ける）。
- 結合のつなぎ目は、この節には無い（部品はプログラムでないため。CMP5 のつなぎ目は、呼ぶプログラムの節で受ける）。
- findsummits#202（HLD を書く段で挙がった UT と IT の候補の割り当て）の「4.8.5 の 7」のうち、この節に当たるのは、「距離がちょうど 30m のピークに当てること（「以下」）は、距離を求める処理と 30m と比べる処理を分けて UT で確かめる」の前半（距離を求める処理）で、[7.1.5](#715-ut-候補) の `UT-cmp5_common-06`（`great_circle_m`）が受ける。後半（30m と比べる処理）は、[7.2.5](#725-ut-候補)の `UT-merge_peaks-17` が受ける。

#### 7.1.1 ファイル割付

- 部品はすべて `scripts/cmp5_common.py` 1 本に置く（ADR-LLD-001 の Decision 5 の「名前は LLD で決める」。名前はモジュール名と同じにする）。CMP5 の 4 本のプログラムは `venv/bin/python3 scripts/<名前>.py` で起動される（[HLD 3.5.1](30_HLD.md#351-プログラム)）ので、`scripts/` が import の探索先の先頭になり、`import cmp5_common` で読む（[2.1.1](#211-ファイル割付)と同じ）。
- `scripts/cmp5_common.py` は、共通部品を `import common` で読む（使うのは `latlon_to_tile` だけ）。ほかに読むのは、標準の `csv`・`decimal`・`json`・`math`・`os`・`re` と、`dataclasses` の `dataclass`、`typing` の `Iterable`・`Iterator` である。
- ファイルの先頭のコメントに `# trace: LLD-cmp5_common` を書く。起動の部分（`if __name__ == '__main__':`）は持たない（プログラムでなく部品のため）。
- UT のコードは `tests/scripts/test_cmp5_common.py` に置く。各テストに `# trace: UT-cmp5_common-NN` のコメントを付ける。[2.4](#24-言語ごとに別に実装する式のテストベクトル)の表 6 を写したテストには、`2.4 の表 6` もコメントに書く（[テスト方針書 3.3](02_test_policy.md#33-期待値の根拠)）。テストの枠組みは [2.1.1](#211-ファイル割付)と同じく標準の `unittest`。

#### 7.1.2 型とデータ

- 公開の定数（モジュールの最上位）:
  - 列の組（どれも `tuple[str, ...]`）:
    - `MERGED_PEAK_ALL_COLUMNS = ('peak_lat', 'peak_lon', 'peak_elev', 'col_lat', 'col_lon', 'col_elev', 'prominence', 'key_col_resolved', 'col_margin_px', 'analysis_id', 'analysis_count', 'expected_count', 'stability')`（[HLD 4.8.2](30_HLD.md#482-処理の流れ)の 7「書き出す」の 13 列。前の 10 列は [6.7.2](#672-型とデータ)の `_header` と同じ並び）。`match_summits` が使う。
    - `MERGED_PEAK_ZONE_COLUMNS = ('peak_lat', 'peak_lon', 'key_col_resolved', 'col_lat', 'col_lon', 'analysis_id')`（[HLD 4.18.2](30_HLD.md#4182-処理の流れ)の 2「`merged_peak.csv` を読む」の 6 列）。`merge_zones` が使う。
    - `MERGED_PEAK_UNRESOLVED_COLUMNS = ('peak_lat', 'peak_lon', 'key_col_resolved')`（[HLD 4.22.2](30_HLD.md#4222-処理の流れ)の 1「`merged_peak.csv` を読む」の 3 列）。`check_cols` が使う。
  - ゾーンの種類（`str`）: `ACTIVATION_ZONE = 'activation_zone'`・`DELETE_ZONE = 'delete_zone'`（[HLD 4.16.2](30_HLD.md#4162-処理の流れ)の `feature_type` の値）。
  - 解析識別子の別（`str`）: `ANALYSIS_NORMAL = 'normal'`・`ANALYSIS_WIDE = 'wide'`・`ANALYSIS_INVALID = 'invalid'`（`parse_analysis_id` が返す）。
- 内部の定数（名前は `_` で始める）:
  - `_FEATURE_TYPES = frozenset({'activation_zone', 'delete_zone', 'peak', 'key_col', 'peak_col_link'})`（HLD 4.16.2 の 5 種類）。
  - `_DECIMAL_RE = re.compile(r'[+-]?[0-9]+(\.[0-9]+)?')`・`_INTEGER_RE = re.compile(r'[+-]?[0-9]+')`（どれも `fullmatch` で使う。10 進の数と整数の字句。`[0-9]` で書くのは、`\d` が全角の数字にも合うため。字句の形は [6.2.3](#623-関数の細部)の手順 7 と同じ）。
  - `_NORMAL_ID_RE = re.compile(r'3-[0-9]{4}')`・`_WIDE_ID_RE = re.compile(r'[456]-[0-9]{4}-(NW|NE|SW|SE)')`（どちらも `fullmatch` で使う。[HLD 4.8.2](30_HLD.md#482-処理の流れ)の 2「読むファイルを選ぶ」）。
  - `_FORMULA_LAT_MAX = 89.0`（`is_valid_coord` が式に入れる緯度の絶対値の上限。[7.1.3](#713-関数の細部)の `is_valid_coord` の 3）、`_PIXEL_MAX = 8388607`（2²³ − 1）、`_EARTH_RADIUS_M = 6371008.8`（HLD 4.8.2 の 5「陸地最高峰の海面確定を当てる」）。
- `@dataclass(frozen=True) class MergedPeakRow`:
  - `path: str`: 読んだファイルの絶対パス（`os.path.abspath` したもの）。`index_peaks_by_pixel` の受け取るものにパスが無いので、重なりのメッセージに出すために行に持たせる。
  - `line_no: int`: 記録の番号。見出しの記録を 1 とし、データの記録は 2 から。CSV の 1 つの記録が複数の物理行にまたがっても 1 と数える。
  - `values: dict[str, str]`: `read_merged_peak` に渡した列の組の名前から、その行のその列の文字列への対応。キーの順は列の組の順。文字列はファイルに書いてあるまま（前後の空白も除かない）。
- `@dataclass(frozen=True) class JsonNumber`: `text: str`。JSON の数の字句のまま（`35.10` は `'35.10'`、`1e2` は `'1e2'`）。JSON の数をこの型で持ち、浮動小数にしない（[HLD 4.18.2](30_HLD.md#4182-処理の流れ)の 5「書き出す」の「読んだときの書き方を変えずに書く」と、[DEC76](30_HLD.md#4184-設計判断)「ピークは Z15 の画素で突き合わせ、ゾーンは写す」）。`str` の子にしないのは、JSON の文字列（`_color` の `"#ef6c00"` など）と見分けるため。書き出す側（7.3）は、`text` をそのまま書く。
- `@dataclass(frozen=True) class ZoneFeature`:
  - `index: int`: `features` の配列の中の位置（1 から数える）。
  - `kind: str`: `ACTIVATION_ZONE` か `DELETE_ZONE`。
  - `pixel: tuple[int, int]`: `properties` の `peak_lat`・`peak_lon` から `latlon_to_z15_pixel` で求めた (gx, gy)。
  - `area_complete: bool`。
  - `geometry: dict`: 読んだ Feature の `geometry` のオブジェクトのまま（数は `JsonNumber`）。
  - `properties: dict`: 同じく `properties` のまま（数は `JsonNumber`。キーの順はファイルの順）。
- 例外 `class InputError(Exception)`: `InputError(symbol, what)` の 2 つの位置引数で作り、属性 `symbol: str`（[7.1.4](#714-メッセージ文面)の記号。`'MP3'` など）と `what: str`（メッセージの 1 行目の `ERROR:` と空白 1 つの後の文。7.1.4 の文面）を持つ。`str(e)` は `what` と同じ。`Exception` の子にするのは、1.2 の禁止（`BaseException`・`SystemExit`・`LogWriteError`・`SignalStop` を捕まえる `except` を書かない）に当たらずに、呼ぶ側が `except cmp5_common.InputError` で捕まえるため。

#### 7.1.3 関数の細部

部品ごとに `#####` の見出し（部品の名前だけ）を立てて書く。

**止まり方**: どの部品も、画面にもログにも何も出さず、`sys.exit` を呼ばない。入力の誤りは `InputError` を上げ、呼ぶ側（7.3〜7.5 のプログラム）が捕まえて、`common.log_error(e.what, <対処>)` を呼んでから `sys.exit(common.EXIT_ERROR)` で止まる。対処の文は呼ぶプログラムの節で決める（[HLD 4.18.3](30_HLD.md#4183-異常系)・[4.22.3](30_HLD.md#4223-異常系)・[4.9.3](30_HLD.md#493-異常系)の「必ず含める内容」の案内がプログラムごとに違い、HLD 3.5.4 の表の受け取るものに案内が無いため。[2.1.3](#213-関数の細部)の `read_mesh_list_file` は案内を引数で受けるが、それは HLD 3.9 の表に案内があるため）。呼ぶ側の書き方の型を、次のコードで示す（[2.1.3](#213-関数の細部)の前置きの型の `try` の中に置く）。

```python
try:
    for row in cmp5_common.read_merged_peak(path, cmp5_common.MERGED_PEAK_UNRESOLVED_COLUMNS):
        ...
except cmp5_common.InputError as e:
    common.log_error(e.what, '<そのプログラムの対処>')
    sys.exit(common.EXIT_ERROR)
```

呼ぶ側の誤り（列の組が 3 つのどれでもない、`axis` が `'lat'`・`'lon'` でない）は `ValueError` を上げる（プログラムの誤りで、利用者の入力の誤りではないため。[2.1.3](#213-関数の細部)の `load_config` の呼ぶ側の誤りと同じ扱い）。

**10 進の数の決まり**（`read_merged_peak` と `is_valid_coord` が使い、7.2〜7.5 の読み込みもこの決まりを指す）:

- 「有限の 10 進の数」は、文字列が `_DECIMAL_RE` に `fullmatch` し、かつ `math.isfinite(float(s))` が真のこと。桁が多くて `float` が無限大になる値は読めない。0 に近すぎて倍精度で表せない値は `float` が 0.0 にするので読める（6.2.3 の手順 7 と同じなのは字句の形だけで、C++ の `std::from_chars` が範囲の外とする値の扱いは違いうる）。
- `1e5`・`35.`・`.5`・`NaN`・`inf`・`1_0`・前後の空白・全角の数字・空は読めない（Python の `float()` は `1e5`・`1_0`・前後の空白・全角の数字・`nan`・`inf` を受けるので、先に字句を決める）。
- 「整数」は `_INTEGER_RE` に `fullmatch` すること。「数として 0」は、有限の 10 進の数で、`decimal.Decimal(s) == 0` のこと（`0`・`0.0`・`-0.00000000` は 0）。
- 値の比べ（[DEC92](30_HLD.md#494-設計判断)「採番と主ピークの比べ方は 10 進の値で行う」）は呼ぶ側が `decimal.Decimal` で行い、この節の部品は文字列のまま返す。

**{reason}**: [2.1.4](#214-メッセージ文面)と同じ（`OSError` の `strerror`、無ければ `str(e)`。`UnicodeDecodeError` なら `UTF-8 として読めない`）。`{path}` は `os.path.abspath(path)`。

##### read_merged_peak

`read_merged_peak(path: str, columns: tuple[str, ...]) -> Iterator[MergedPeakRow]`

1. `columns` が `MERGED_PEAK_ALL_COLUMNS`・`MERGED_PEAK_ZONE_COLUMNS`・`MERGED_PEAK_UNRESOLVED_COLUMNS` のどれとも `==` でなければ、呼んだ時点で `ValueError` を上げる。そうでなければ、内部の生成関数 `_iter_merged_peak(path, columns)` の生成器を返す。確かめを外の関数に置くのは、生成関数の本体が最初の `next` まで動かないので、呼んだ時点で確かめるため。以下は `_iter_merged_peak` の中身で、最初の `next` から動く。
2. `abspath = os.path.abspath(path)`。`os.path.exists(abspath)` が偽なら MP1。`open(abspath, encoding='utf-8', newline='')` を `with` で開き（`OSError` は MP2。ディレクトリも MP2）、`csv.reader(f, strict=True)` で読む。
   - 記録の番号 `line_no` は、各記録を読み始める前に 1 つ増やす（初めは 0 で、見出しの記録を読み始める前に 1、次のデータの記録の前に 2）。下の `{line_no}` は、読んでいる記録のこの番号（`csv.reader` の `line_num`〈物理行の数〉は使わない。読み途中で失敗したときも、その記録の番号）。
   - BOM は除かない（`merge_peaks` が BOM を書かないので、BOM があれば見出しが違う誤りになる）。
   - 読む途中の `UnicodeDecodeError` と `OSError` は MP2、`csv.Error` は MP3（`{detail}` は `{line_no} 行目を CSV として読めない: {reason}`。`{reason}` は `str(e)`）。
3. 見出しの行（最初の記録）:
   - 記録が無い（0 バイトのファイル）なら MP3（`見出しの行が無い`）。
   - `columns` が 13 列のとき: 見出しの行が `MERGED_PEAK_ALL_COLUMNS` と同じ並びのリストでなければ MP3（`見出しの行が 13 列の並びでない: {line}`。`{line}` は見出しの記録を `,` でつないだもの）。
   - 6 列・3 列のとき: `columns` の名前を順に見て、見出しに無ければ MP3（`見出しに列 {column} が無い`）、2 つ以上あれば MP3（`見出しに列 {column} が 2 つある`）。最初に当たった名前で止まる。`columns` に無い名前は、重なっていてもよく（[DEC106](30_HLD.md#4224-設計判断)「`merged_peak.csv` は使う 3 列だけを確かめる」と HLD 4.18.3 の「見出しに 2 の列が無い」は、使う列だけを確かめる）、順も問わない。使う列の重なりを止めるのは、どの位置の値を読むかが決まらないため。
4. データの行（2 つ目の記録から）: 記録ごとに、列の数が見出しの行の列の数と違えば MP3（`{line_no} 行目の列の数が {count} で、見出しの行の {header_count} と違う`。空の行〈`csv.reader` が空のリストを返す記録〉も、列の数 0 としてここに当たる。6 列・3 列のときも全部の列の数を見るのは、記録の形が崩れると使う列の値の位置が決まらないため。HLD 4.18.3・4.22.2 の 1 の「値が読めない」の中で、形の崩れを読めないとする読み方）。合えば、`columns` の各列の文字列を見出しの位置から取り、下の 5 の確かめを当てる。最初に外れたもので MP3（`{line_no} 行目の {column} が {condition}: {value}`。`{value}` は文字列のまま〈空の文字列なら、文は `:` と空白 1 つで終わる〉。`analysis_id` が空のときだけ `{line_no} 行目の analysis_id が空` で、`: {value}` を付けない）。外れなければ `MergedPeakRow(abspath, line_no, {列: 文字列})` を渡す。
5. 列ごとの確かめ（`columns` に入っている列だけを確かめる。列の組で確かめが違うのは、HLD が読むプログラムごとに確かめる列を決めているため。HLD 3.5.4 の表の後の段落）:

   | 列 | 13 列 | 6 列 | 3 列 | `{condition}` |
   |---|---|---|---|---|
   | `peak_lat` | `is_valid_coord(v, 'lat')` | 同じ | 同じ | `座標として読めない` |
   | `peak_lon` | `is_valid_coord(v, 'lon')` | 同じ | 同じ | `座標として読めない` |
   | `peak_elev` | 有限の 10 進の数 | — | — | `有限の 10 進の数でない` |
   | `col_lat`・`col_lon` | `key_col_resolved` が `true` の行は有限の 10 進の数。`false` の行は数として 0 | `true` の行だけ、有限の 10 進の数（`false` の行は見ない） | — | `有限の 10 進の数でない`（有限の 10 進の数として読めないとき）、`数として 0 でない`（`false` の行で、有限の 10 進の数だが 0 でないとき） |
   | `col_elev`・`prominence` | `true` の行は有限の 10 進の数。`false` の行は空 | — | — | `有限の 10 進の数でない`、`空欄でない` |
   | `key_col_resolved` | `true` か `false`（文字列がちょうどその 4 字か 5 字） | 同じ | 同じ | `true か false でない` |
   | `col_margin_px` | 整数 | — | — | `整数でない` |
   | `analysis_id` | 空でない | 同じ | — | `空`（上の 4 の形） |
   | `analysis_count` | 整数 | — | — | `整数でない` |
   | `expected_count` | 整数か空 | — | — | `整数か空欄でない` |
   | `stability` | `confirmed`・`unstable`・`-` のどれか | — | — | `confirmed・unstable・- のどれでもない` |

   行ごとに、`key_col_resolved` が `columns` に入っていれば、それを最初に確かめ（外れていれば、その誤りを出す）、残りの列を `columns` の順に確かめる。`col_lat`・`col_lon`・`col_elev`・`prominence` は `key_col_resolved` の値で確かめが変わるため、`key_col_resolved` を先に見る。
6. 終わりまで読んだら止まる。データの行が 0 なら何も渡さない（見出しの行だけのファイルは誤りにしない。HLD 4.22.2 の 1・4.18.2 の 2・[4.9.2](30_HLD.md#492-処理の流れ)の 1 のどれも 0 行を認める）。

##### index_peaks_by_pixel

`index_peaks_by_pixel(rows: Iterable[MergedPeakRow]) -> dict[tuple[int, int], MergedPeakRow]`

- 行ごとに `latlon_to_z15_pixel(float(row.values['peak_lat']), float(row.values['peak_lon']))` で (gx, gy) を求め、それを鍵に表へ入れる。表の順は渡された行の順（`dict` の挿入の順。`merge_zones` の書き出しの順〈HLD 4.18.2 の 5「書き出す」の「`merged_peak.csv` の行の順」〉に使う）。
- 同じ鍵が既にあれば、MP3 で止まる（`{detail}` は `{line_a} 行目と {line_b} 行目が同じ Z15 の画素 ({gx}, {gy}) の行`。`{line_a}` は表にあった行、`{line_b}` は今の行の `line_no`。`{path}` は今の行の `path`。最初の 1 組だけ）。
- `rows` の行は `read_merged_peak` が確かめた後のもの（`peak_lat`・`peak_lon` は座標として読める）なので、`float` は失敗しない。`rows` が `read_merged_peak` の生成器なら、その `InputError` もそのまま伝わる。

##### read_zone_features

`read_zone_features(path: str) -> list[ZoneFeature]`

1. `abspath = os.path.abspath(path)`。`os.path.exists(abspath)` が偽なら ZF1。`open(abspath, 'rb')` で開いて全部を読み（`OSError` は ZF2。ディレクトリも ZF2）、`bytes.decode('utf-8')` で文字列にする（`UnicodeDecodeError` は ZF2。`{reason}` は `UTF-8 として読めない`）。BOM は除かない（`json.loads` が誤りにするので ZF3 になる）。
2. `json.loads(text, parse_float=JsonNumber, parse_int=JsonNumber, parse_constant=_reject_constant, object_pairs_hook=_unique_object)` で読む。
   - `_reject_constant(token)` は `ValueError(f'{token} は JSON の数でない')` を上げる（`NaN`・`Infinity`・`-Infinity`）。
   - `_unique_object(pairs)` は、同じキーが 2 つ以上あれば `ValueError(f'同じオブジェクトにキー {key} が 2 つある')` を上げ、無ければ `dict(pairs)` を返す。
   - `json.JSONDecodeError`（`ValueError` の子）と、この 2 つの `ValueError` は ZF3（`{detail}` は `JSON として読めない: {reason}`。`{reason}` は `str(e)`）。`RecursionError` も ZF3（`JSON として読めない: 入れ子が深すぎる`）。
3. 最上位がオブジェクトで、`type` が `'FeatureCollection'`、`features` がリストでなければ ZF3（`FeatureCollection でない`）。
4. `features` の要素を順に見る（`{index}` は 1 から）。外れたら ZF3 で止まる（最初の 1 つだけ）。
   - 要素がオブジェクトで `type` が `'Feature'` でなければ `{index} 番目の Feature がオブジェクトでないか、type が Feature でない`。
   - `properties` がオブジェクトでなければ `{index} 番目の Feature の properties がオブジェクトでない`。
   - `properties` の `feature_type` が `_FEATURE_TYPES` の文字列のどれでもなければ `{index} 番目の Feature の feature_type が activation_zone・delete_zone・peak・key_col・peak_col_link のどれでもない`。
   - `feature_type` が `peak`・`key_col`・`peak_col_link` なら、ほかを確かめずに次へ（点と線は読まない。HLD 4.18.2 の 3「ゾーンを選ぶ」・4.9.2 の 2「`merged_peak.geojson` を読む」）。
   - ゾーン（`activation_zone`・`delete_zone`。以下 `{kind}` はその値）:
     - `peak_lat`・`peak_lon`・`area_complete` のどれかのキーが無ければ `{index} 番目の Feature（{kind}）の properties に {key} が無い`（この順で最初のもの）。
     - `peak_lat` が `JsonNumber` で `is_valid_coord(v.text, 'lat')` が真でなければ `{index} 番目の Feature（{kind}）の peak_lat が座標として読めない`。`peak_lon` も同じ（`'lon'`）。
     - `area_complete` が `bool` でなければ（`type(v) is bool` で見る）`{index} 番目の Feature（{kind}）の area_complete が true か false でない`。
     - `geometry` が無いか、オブジェクトでないか、オブジェクトで `type` が `'Polygon'` か `'MultiPolygon'` でなければ（`null` と配列はオブジェクトでない）`{index} 番目の Feature（{kind}）のジオメトリが Polygon でも MultiPolygon でもない`。
     - `coordinates` が形に合わなければ `{index} 番目の Feature（{kind}）の coordinates が {type} の形でない`（`{type}` は `Polygon` か `MultiPolygon`）。形は次のとおり。
       - 位置は、要素がすべて `JsonNumber` で、2 つ以上あるリスト（RFC 7946 は 3 つ目の高さを許す。CMP4 は 2 つだけを書く〈[6.8.3](#683-関数の細部)〉）。
       - 環は、位置が 4 つ以上のリスト（RFC 7946 の線形の環。閉じているかは見ない）。
       - Polygon の `coordinates` は、環が 1 つ以上のリスト。MultiPolygon の `coordinates` は、Polygon の `coordinates` の形のものが 1 つ以上のリスト。
       - HLD 4.18.3 と 4.9.2 の 2 の書式の列挙に無い確かめを足すのは、`match_summits` がゾーンを点の内外の判定に使い（HLD 4.9.2 の「ゾーンの内外」）、形の崩れたジオメトリをそこまで運ばないため。
     - 画素 `pixel = latlon_to_z15_pixel(float(peak_lat.text), float(peak_lon.text))`。`ZoneFeature(index, kind, pixel, area_complete, geometry, properties)` を並びに足す。
5. 重なり: 4 を最後まで通ったら、`(kind, pixel)` が同じゾーンの組を探す（種類が違えば同じ画素でよい）。1 つ以上あれば、すべての組を ZF4 で止まる。最初の 1 組で止めないのは、`match_summits` のメッセージが、食い違いの「当たったピークすべての緯度経度とゾーンの種類」を求めるため（[HLD 4.9.3](30_HLD.md#493-異常系)）。
   - `{list}` は、組ごとに `{peak_lat},{peak_lon} の {kind}（{indexes} 番目）` を、組の中で最も小さい `index` の順に `、` でつないだもの。
   - `{peak_lat}`・`{peak_lon}` は、組の中で最も小さい `index` の Feature の字句（`JsonNumber` の `text`）。`{indexes}` は、組の Feature の `index` を昇順に `・` でつないだもの。
   - 書式の誤り（4）があれば先にそれで止まり、重なりは見ない。
6. ゾーンの Feature の並び（ファイルの順）を返す。ゾーンが 0 なら空のリスト。

##### latlon_to_z15_pixel（cmp5_common）

`latlon_to_z15_pixel(lat: float, lon: float) -> tuple[int, int]`

`common.latlon_to_tile(lat, lon, 23)` を返す（[2.4](#24-言語ごとに別に実装する式のテストベクトル)の計算の決まりの `latlon_to_z15_pixel`。Z15 の 1 画素は z=23 の 1 タイル）。引数を確かめない（呼ぶ側が `is_valid_coord` を通した値を渡す。HLD 3.5.4 の表の「使うところ」はどれも、読んだ座標を確かめた後に呼ぶ）。

##### is_valid_coord

`is_valid_coord(text: str, axis: str) -> bool`

`axis` は `'lat'` か `'lon'`（ほかは `ValueError`）。次の順に見て、どれかで偽を返し、最後まで通れば真を返す。例外は上げない。HLD 4.8.2 の 1「リストを読む」の座標として読める条件の (1)〜(3) に当たる。

1. (1) 有限の 10 進の数である（前置きの 10 進の数の決まり）。
2. `v = float(text)`。(2) 緯度は `-90.0 < v < 90.0`、経度は `-180.0 <= v < 180.0`（`float` にした後の値で比べる。`89.99999999999999999999` は `90.0` になって外れる）。
3. 緯度だけ: `abs(v) > _FORMULA_LAT_MAX` なら偽（式に入れない）。−90 に近い緯度では `tan(r) + 1 / cos(r)` が桁落ちし、`log(0)` の `ValueError` になるか（`-89.99999999`）、範囲の中の行に出て誤って通る（`-89.9999999999999` は gy 7895955）。89 を超える緯度は、数学上はどれも画素の行が範囲の外（Web メルカトルの限界 85.0511287798066 度の外）なので、式に入れずに外しても HLD の (3) の判定と同じになる。上限を限界の値にしないのは、限界の近くの値（`-85.05112877980662` は式で gy 8388607 になり、読める）を、HLD の「限界を定数で書かず、結果の画素で決める」のとおり式で決めるため。85.0511288〜89 度では、式が正しく範囲の外の行を返す（2026-10-31 に CPython 3.14.8 で正負 200 万点を調べた）。
4. (3) 緯度は `common.latlon_to_tile(v, 0.0, 23)` の `y`、経度は `common.latlon_to_tile(0.0, v, 23)` の `x` が、0 以上 `_PIXEL_MAX` 以下（`x` は経度だけで、`y` は緯度だけで決まる）。`85.05112878` は `y` が −1、`-85.05112878` は 8388608 で外れる（HLD 4.8.2 の 1）。

`text` は受け取った文字列のまま判定する（前後の空白を除かない）。利用者が書くファイル（陸地最高峰リスト、SOTA サミットリスト CSV、山岳データ登録変更リスト）で空白を許すかは、読むプログラムの節で決め、許すなら呼ぶ前に除く。

##### great_circle_m

`great_circle_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float`

半径 `_EARTH_RADIUS_M` の球の大円距離（m）を、haversine の式で、次の順に求める。

```python
p1 = math.radians(lat1)
p2 = math.radians(lat2)
dp = p2 - p1
dl = math.radians(lon2 - lon1)
h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
return 2 * _EARTH_RADIUS_M * math.asin(min(1.0, math.sqrt(h)))
```

- haversine にするのは、30m のような短い距離（[DEC80](30_HLD.md#484-設計判断)「陸地最高峰リストは 30m 以内の 1 件に当てる」）で、球面の余弦の式（`acos`）より桁が落ちにくいため。`min(1.0, …)` は、対蹠点の近くで丸めにより `h` が 1 を少し超えて `asin` が `ValueError` になるのを防ぐ。
- Python の 7.1 だけが実装するので（呼ぶのは `apply_land_peaks`・`match_delete_zones`）、2.4 の表には置かず、期待値は [7.1.5](#715-ut-候補) の UT 06 に置く。

##### parse_analysis_id

`parse_analysis_id(name: str) -> tuple[str, str]`

- `name` はファイル名（ディレクトリを含まない。呼ぶ側は `os.listdir` などで得た名前を渡す）。`stem` は `os.path.splitext(name)` の 1 つ目（最後の `.` から後を除く。`3-5339.csv` は `3-5339`、`3-5339.csv.tmp` は `3-5339.csv`）。
- `_NORMAL_ID_RE.fullmatch(stem)` なら `(stem, ANALYSIS_NORMAL)`、`_WIDE_ID_RE.fullmatch(stem)` なら `(stem, ANALYSIS_WIDE)`、どちらでもなければ `(stem, ANALYSIS_INVALID)` を返す。
- どちらの形でも、メッシュコードは `stem[2:6]`（呼ぶ側が `--mesh` の集合と比べるのに使う）。拡張子（`.csv`・`.geojson`）で選ぶのは呼ぶ側（`select_peak_csv_files` は `.csv` だけ、`select_zone_geojson_files` は `.geojson` だけを渡す。[HLD 4.8.2](30_HLD.md#482-処理の流れ)の 2「読むファイルを選ぶ」・[4.18.2](30_HLD.md#4182-処理の流れ)の 1「読むファイルを選ぶ」）。

#### 7.1.4 メッセージ文面

7.1 の部品はメッセージを出さない（7.1.3 の「止まり方」）。次の表は `InputError` の `what`（1 行目の `ERROR:` と空白 1 つの後）の文面で、`対処:` の行は呼ぶプログラムの節（7.3 `merge_zones`・7.4 `check_cols`・7.5 `match_summits`）で決める。終了コードは、呼ぶ側が `EXIT_ERROR`（1）で止まる（HLD 4.18.3・4.22.3・4.9.3）。`{path}` は `os.path.abspath` したパス、`{reason}` は 7.1.3 の前置きのとおり。

| 記号 | 場面 | `what` |
|---|---|---|
| MP1 | `merged_peak.csv` が無い | `merged_peak.csv が無い: {path}` |
| MP2 | `merged_peak.csv` を読めない | `merged_peak.csv を読めない: {path}: {reason}` |
| MP3 | `merged_peak.csv` の書式が違う（同じ Z15 の画素の行を含む） | `merged_peak.csv の書式が違う: {path}: {detail}`（`{detail}` は 7.1.3 の `read_merged_peak` の 2〜5 と `index_peaks_by_pixel` の文） |
| ZF1 | ピーク候補 GeoJSON が無い | `ピーク候補 GeoJSON が無い: {path}` |
| ZF2 | ピーク候補 GeoJSON を読めない | `ピーク候補 GeoJSON を読めない: {path}: {reason}` |
| ZF3 | ピーク候補 GeoJSON の書式が違う | `ピーク候補 GeoJSON の書式が違う: {path}: {detail}`（`{detail}` は 7.1.3 の `read_zone_features` の 2〜4 の文） |
| ZF4 | 1 つのファイルに同じピークの同じ種類のゾーンが 2 つ以上 | `ピーク候補 GeoJSON に同じピークの同じ種類のゾーンが 2 つ以上ある: {path}: {list}`（`{list}` は 7.1.3 の `read_zone_features` の 5） |

「ピーク候補 GeoJSON」は、per-mesh ピーク候補 GeoJSON（`merge_zones` が読む）と統合ピーク候補 GeoJSON（`merged_peak.geojson`。`match_summits` が読む）の両方を指す。

#### 7.1.5 UT 候補

すべて自動（合否をテストのコードが判定できる）。どのケースも「同じプロセス」で動かす。テストのプロセスの中で、ソースツリーの根の `scripts/` を import の探索先に入れて `import cmp5_common` し（[3.1.5](#315-ut-候補)・[4.1.5](#415-ut-候補)の「同じプロセス」と同じ。`cmp5_common` の中の `import common` も同じ探索先から読む）、対象の関数を直接呼ぶ。ファイルはケースごとに一時のディレクトリに書き、絶対パスを渡す。`InputError` は `assertRaises` で捕まえて `symbol` と `what` を比べる。7.1 の部品はメッセージを出さず `sys.exit` を呼ばないので、子のプロセスは使わない。期待の `what` の `{path}` は、渡した一時のファイルの絶対パスとする。

共通の入力に名前を付ける（下の表から名前で指す）。

- **13 列の見出し**: `peak_lat,peak_lon,peak_elev,col_lat,col_lon,col_elev,prominence,key_col_resolved,col_margin_px,analysis_id,analysis_count,expected_count,stability`
- **13 列の 3 行**（13 列の見出しの後の行。行末は LF）:
  - 行 A: `34.99999777,135.00002146,1234.5,35.01234568,135.10000000,1100.0,134.5,true,12,3-5235,3,9,confirmed`
  - 行 B: `36.00465613,139.99880075,800.0,0.00000000,0.00000000,,,false,-1,5-5439-NW,0,,-`
  - 行 C: `34.99999777,135.00006437,50.0,0.00000000,0.00000000,0.00,50.0,true,-1,3-5235,2,9,unstable`
- **ゾーンの 13 行**: [6.8.5](#685-ut-候補)の UT 20 の期待（13 行。各行は `\n` で終わる）のバイト列そのまま。読む側の UT は、書く側の UT 20 の期待を入力にする。

画素と大円距離の期待値は、[2.4](#24-言語ごとに別に実装する式のテストベクトル)の計算の決まりと 7.1.3 の式のとおりに、2026-10-31 に CPython 3.14.8 で求めた。行 A と行 B の画素は 2.4 の表 6 の行と同じで、行 C の画素は `(7340033, 3322709)` である。

| ID | 確かめること | 準備 | 入力 | 期待 |
|---|---|---|---|---|
| `UT-cmp5_common-01` | 緯度経度 → Z15 の画素（2.4 の表 6） | 同じプロセス | `latlon_to_z15_pixel` に 2.4 の表 6 の 11 行（緯度と経度は表の 10 進の表記を `float` にしたもの） | 各行の `(gx, gy)` と等しく、2 つとも `int` |
| `UT-cmp5_common-02` | 座標として読める | 同じプロセス | `is_valid_coord` に、緯度 `35.0`・`85.05112693`・`-85.0511287`・`-85.05112877980662`・`-85.0511287798066`・`85.05112877980659`・`0`・`-0`・`+35.5`・`35.00000000`、経度 `-180`・`179.99999999`・`135.0`・`-0.0` | どれも `True` |
| `UT-cmp5_common-03` | 字句で読めない | 同じプロセス | 緯度として `''`・`' 35.0'`・`'35.0 '`・`'1e3'`・`'35.'`・`'.5'`・`'NaN'`・`'nan'`・`'Infinity'`・`'inf'`・`'1_0'`・全角の数字 2 字（U+FF13 U+FF15）・`'0x10'`・`'35,0'`・`'1'` の後に `0` を 400 個並べた値 | どれも `False`（例外を上げない） |
| `UT-cmp5_common-04` | 範囲と画素と数の破綻 | 同じプロセス | 緯度 `90`・`-90`・`360`・`-360`・`89.99999999999999999999`・`85.05112878`・`-85.05112878`・`85.0511287798066`・`85.05112877980662`・`-85.0511287798067`・`89.0`・`-89.0`・`89.5`・`-89.9999999`・`-89.99999999`・`-89.9999999999999`、経度 `180`・`-180.00000001`・`179.999999999999999999`・`360` | どれも `False`（例外を上げない）。`89.0`・`-89.0`・`85.0511287798066`・`85.05112877980662`・`-85.0511287798067` は式で（`y` が −1 以下か 8388608 以上になって）、`89.5`・`-89.9999999`・`-89.99999999`・`-89.9999999999999` は 7.1.3 の `is_valid_coord` の 3 で外れる |
| `UT-cmp5_common-05` | `axis` の誤り | 同じプロセス | `is_valid_coord('35.0', 'x')`・`is_valid_coord('35.0', 'LAT')` | どちらも `ValueError` |
| `UT-cmp5_common-06` | 大円距離 | 同じプロセス | (a) (35.0, 135.0)–(35.0, 135.0)、(b) (35.0, 135.0)–(36.0, 135.0)、(c) (0.0, 0.0)–(0.0, 180.0)、(d) (34.99999777, 135.00002146)–(35.0, 135.0003)、(e) (d) の 2 点を入れ替えたもの | (a) `0.0` と `==`。(b) `111195.08023353307`、(c) `20015114.442035925`、(d) `25.372216620090683` と、差の絶対値が `1e-6` 以下。(b) は `6371008.8 * math.pi / 180`、(c) は `6371008.8 * math.pi` とも差が `1e-6` 以下。(e) は (d) と `==` |
| `UT-cmp5_common-07` | 解析識別子を読む | 同じプロセス | `3-5339.csv`・`3-0123.geojson`・`4-5339-NW.csv`・`5-5339-NE.csv`・`6-0123-SE.csv`・`4-5339-SW.geojson` | `('3-5339', 'normal')`・`('3-0123', 'normal')`・`('4-5339-NW', 'wide')`・`('5-5339-NE', 'wide')`・`('6-0123-SE', 'wide')`・`('4-5339-SW', 'wide')` |
| `UT-cmp5_common-08` | 規則に合わない名前 | 同じプロセス | `3-533.csv`・`3-53399.csv`・`7-5339-NW.csv`・`4-5339.csv`・`3-5339-NW.csv`・`4-5339-nw.csv`・`4-5339-NN.csv`・`x.csv`・`3-` の後に全角の数字 4 字（U+FF15 U+FF13 U+FF13 U+FF19）を続けて `.csv` を付けた名前・`3-5339.csv.tmp`・`.csv` | どれも 2 つ目が `'invalid'`。1 つ目は `os.path.splitext(name)` の 1 つ目（`3-5339.csv.tmp` は `'3-5339.csv'`、`.csv` は `'.csv'`） |
| `UT-cmp5_common-09` | 13 列を読む | 同じプロセス。13 列の見出しと 13 列の 3 行を書いたファイル | `read_merged_peak(path, MERGED_PEAK_ALL_COLUMNS)` を最後まで回す | 3 つの `MergedPeakRow`。`line_no` は 2・3・4、`path` は絶対パス、`values` のキーは 13 列の順、値は行 A〜C の文字列のまま（行 B の `col_elev`・`prominence`・`expected_count` は `''`） |
| `UT-cmp5_common-10` | 6 列・3 列を読む | 同じプロセス。(a) 13 列の見出しと 13 列の 3 行のファイル。(b) 見出しが `analysis_id,extra,col_lon,col_lat,key_col_resolved,peak_lon,peak_lat` で、行が `3-5235,x,135.1,35.0,true,135.00002146,34.99999777` の 1 行のファイル。(c) 13 列の見出しだけのファイル | (a) を 6 列と 3 列で、(b) を 6 列と 3 列で、(c) を 3 つの列の組で回す | (a) 6 列は 3 行で `values` のキーが 6 列の組の順、3 列は 3 行で 3 列の組の順。(b) 6 列は 1 行で `{'peak_lat': '34.99999777', 'peak_lon': '135.00002146', 'key_col_resolved': 'true', 'col_lat': '35.0', 'col_lon': '135.1', 'analysis_id': '3-5235'}`（この順）。3 列も 1 行。(c) どれも 0 行で、例外を上げない |
| `UT-cmp5_common-11` | 見出しの誤り | 同じプロセス。(a) 0 バイト、(b) 13 列の見出しの 2 列目と 3 列目を入れ替えたもの、(c) `peak_lat,peak_lon,key_col_resolved,col_lat,analysis_id`、(d) `peak_lat,peak_lon,key_col_resolved,peak_lat`、(e) 先頭に BOM（`EF BB BF`）を付けた 13 列の見出し、(f) `peak_lat,peak_lon,key_col_resolved,x,x`。どれも見出しの行だけ | (a) を 3 つの列の組で、(b)(e) を 13 列で、(c) を 6 列で、(d)(f) を 3 列で回す | (f) は誤りにせず 0 行。ほかは MP3。`what` の `{detail}` は、(a) `見出しの行が無い`、(b)(e) `見出しの行が 13 列の並びでない: <見出しの記録を , でつないだもの>`、(c) `見出しに列 col_lon が無い`、(d) `見出しに列 peak_lat が 2 つある` |
| `UT-cmp5_common-12` | 13 列の値の誤り | 同じプロセス。13 列の見出しの後に行 A を置き、行 A（または行 B）の 1 つの値だけを替えた行を 3 行目に足したファイルを、替え方ごとに作る | 行 A で、`peak_lat` を `91`、`peak_elev` を `1e3`、`peak_elev` を `1` の後に `0` を 400 個並べた値（桁が多くて `float` が無限大になる）、`key_col_resolved` を `True`、`col_lat` を `x`、`col_elev` を `''`、`col_margin_px` を `1.0`、`analysis_id` を `''`、`analysis_count` を `''`、`expected_count` を `x`、`stability` を `stable`。行 B で、`col_lat` を `0.1` にしたものと、`col_elev` を `1.0` にしたもの（別々のファイル）。行 A の `key_col_resolved` を `yes` にし、同時に `col_elev` を `''` にしたもの | どれも MP3 で、`{detail}` は `3 行目の <列> が <condition>: <値>`（`analysis_id` は `3 行目の analysis_id が空`）。`condition` は 7.1.3 の `read_merged_peak` の 5 の表のとおり（行 B の `col_lat` の `0.1` は `数として 0 でない`、`col_elev` の `1.0` は `空欄でない`）。最後のケースは `3 行目の key_col_resolved が true か false でない: yes`。2 行目の行 A は誤りにしない（`line_no` 2 の行が先に渡る） |
| `UT-cmp5_common-13` | 6 列・3 列の確かめの範囲 | 同じプロセス。13 列の見出しの後に 1 行を置いたファイル。(a) 行 B の `col_lat` を `x` にした行、(b) 行 A の `col_lat` を `x` にした行、(c) 行 A の `peak_elev` を `x`・`stability` を `x` にした行、(d) 行 A の `analysis_id` を `''` にした行 | (a)(b)(c)(d) を 6 列と 3 列で回す | (a) は 6 列でも 3 列でも誤りにしない（`false` の行の `col_lat` は 6 列では見ない）。(b) は 6 列で MP3（`2 行目の col_lat が 有限の 10 進の数でない: x`）、3 列では誤りにしない。(c) はどちらも誤りにしない。(d) は 6 列で MP3（`2 行目の analysis_id が空`）、3 列では誤りにしない |
| `UT-cmp5_common-14` | 列の数と CSV の誤り | 同じプロセス。13 列の見出しの後に、(a) 12 列の行、(b) 14 列の行、(c) 空の行の後に行 A、(d) 行 A の 1 つ目の値を `"34.99999777"x` にした行（引用符の後に字が続く）。(e) 13 列の見出しの 1 つ目を `"peak_lat"x` にしたもの（見出しの記録で失敗）。(f) 行 A の後に、`"34.99999777` で始まり、引用符を閉じずにファイルが終わる行（2 つ目のデータの記録が複数の物理行にまたがったまま切れる。最後の行に改行を付けない） | 13 列で回す | どれも MP3。(a) `2 行目の列の数が 12 で、見出しの行の 13 と違う`、(b) 14、(c) `2 行目の列の数が 0 で、見出しの行の 13 と違う`、(d) `2 行目を CSV として読めない: ',' expected after '"'`（CPython 3.14.8 の `csv.Error` の文。NUL は 3.11 から `csv` の誤りにならないので使わない）、(e) `1 行目を CSV として読めない: ',' expected after '"'`、(f) `3 行目を CSV として読めない: unexpected end of data`（行 A は先に 2 行目として渡る） |
| `UT-cmp5_common-15` | 無い・読めない | 同じプロセス。(a) 無いパス、(b) 一時のディレクトリ、(c) UTF-8 として読めないバイト列（`FF FE`）だけのファイル | 13 列で回す | (a) MP1、(b) MP2（`{reason}` は `IsADirectoryError` の `strerror`、`Is a directory`）、(c) MP2（`{reason}` は `UTF-8 として読めない`）。どれも、呼んだ時点では上げず、最初の `next` で上げる |
| `UT-cmp5_common-16` | 列の組の誤り | 同じプロセス | `read_merged_peak(path, ('peak_lat',))`・`read_merged_peak(path, list(MERGED_PEAK_ALL_COLUMNS))` | どちらも呼んだ時点で `ValueError`（`next` を呼ばない。2 つ目はリストなので `==` にならない） |
| `UT-cmp5_common-17` | 画素の表 | 同じプロセス。13 列の見出しと 13 列の 3 行のファイル | `index_peaks_by_pixel(read_merged_peak(path, MERGED_PEAK_ALL_COLUMNS))` | 鍵が行の順に `(7340032, 3322709)`（行 A。2.4 の表 6 の 4 行目）・`(7456512, 3293952)`（行 B。表 6 の 2 行目）・`(7340033, 3322709)`（行 C）の `dict`（`list(d)` がこの順）。値は、`read_merged_peak` が渡した `MergedPeakRow` と等しい（`line_no` 2・3・4） |
| `UT-cmp5_common-18` | 同じ画素の行 | 同じプロセス。13 列の見出しの後に、行 A と、行 A の `peak_lat` を `34.999997770` にした行（同じ画素で文字列が違う） | `index_peaks_by_pixel(read_merged_peak(path, MERGED_PEAK_ZONE_COLUMNS))` | MP3（`2 行目と 3 行目が同じ Z15 の画素 (7340032, 3322709) の行`） |
| `UT-cmp5_common-19` | ゾーンを読む（6.8 の出力） | 同じプロセス。ゾーンの 13 行をそのまま書いたファイル | `read_zone_features(path)` | 6 つの `ZoneFeature`（6.8.5 の UT 20 の期待の 2〜7 行目のゾーン）。`index` は 1〜6、`kind` は delete・delete・delete・activation・activation・activation、`area_complete` は真・偽・真・真・真・偽、`pixel` は 1・4 番目が `(7340032, 3322709)`、2・5 番目が `(7456512, 3293952)`、3・6 番目が `(7340033, 3322709)`。1 番目の `geometry` は `type` が `'Polygon'` で、`coordinates` は環 2 つ。1 つ目の環の位置は `135.1,35.1`・`135.1,35.0`・`135.2,35.0`・`135.2,35.1`・`135.1,35.1`、2 つ目は `135.12,35.08`・`135.18,35.08`・`135.18,35.02`・`135.12,35.02`・`135.12,35.08`（どれも経度・緯度の順の 2 つの `JsonNumber` で、`text` がこの字句）、`properties` は `peak_lat` が `JsonNumber('34.99999777')`、`_weight` が `JsonNumber('2')`、`_fill` が `False`、キーの順はファイルの順。点と線（8〜12 行目。13 行目は `]}`）は返さない |
| `UT-cmp5_common-20` | 数の書き方を保つ・空 | 同じプロセス。(a) ゾーン 1 つの FeatureCollection で、`peak_lat` が `34.99999777`、`peak_lon` が `135.00002146`、座標に `35.10`・`1e2`・`-0` を含むもの、(b) `{"type":"FeatureCollection","features":[]}` | `read_zone_features(path)` | (a) 座標の `JsonNumber` の `text` が `'35.10'`・`'1e2'`・`'-0'` のまま。(b) 空のリスト |
| `UT-cmp5_common-21` | GeoJSON の書式の誤り | 同じプロセス。ゾーンの 13 行のファイルから 1 か所だけ替えたものを、替え方ごとに作る | (a) 最上位を `[]` に、(b) `"type":"FeatureCollection"` を `"type":"Feature"` に、(c) 2 行目の `"feature_type":"delete_zone"` を `"zone"` に、(d) 2 行目の `"area_complete":true` を `"area_complete":"true"` に、(e) 2 行目の `"peak_lat":34.99999777` を `"peak_lat":"34.99999777"` に、(f) 2 行目の `"peak_lat":34.99999777,` を（後ろの `,` ごと）消す、(g) 2 行目の `"type":"Polygon"` を `"type":"LineString"` に、(h) 2 行目の `"_opacity":1` を `"_opacity":NaN` に、(i) 2 行目の `"_fill":false` の後に `,"_fill":false` を足す、(j) 最後の `]}` を消す、(k) 2 行目の最初の環の頂点を 3 つに減らす、(l) ファイル全体を `[` を 100000 個並べただけ（閉じない）にする、(m) 2 行目の `"geometry"` の値を `null` にする | どれも ZF3。`{detail}` は (a)(b) `FeatureCollection でない`、(c) `1 番目の Feature の feature_type が activation_zone・delete_zone・peak・key_col・peak_col_link のどれでもない`、(d) `1 番目の Feature（delete_zone）の area_complete が true か false でない`、(e) `1 番目の Feature（delete_zone）の peak_lat が座標として読めない`、(f) `1 番目の Feature（delete_zone）の properties に peak_lat が無い`、(g) `1 番目の Feature（delete_zone）のジオメトリが Polygon でも MultiPolygon でもない`、(h) `JSON として読めない: NaN は JSON の数でない`、(i) `JSON として読めない: 同じオブジェクトにキー _fill が 2 つある`、(j) `JSON として読めない:` で始まる、(k) `1 番目の Feature（delete_zone）の coordinates が Polygon の形でない`、(l) `JSON として読めない: 入れ子が深すぎる`（`RecursionError`）、(m) `1 番目の Feature（delete_zone）のジオメトリが Polygon でも MultiPolygon でもない` |
| `UT-cmp5_common-22` | 同じピークの同じ種類 | 同じプロセス。(a) ゾーンの 13 行のファイルの 4 行目（行 C の delete_zone）の `peak_lon` を `135.00002146` に替えたもの。(b) (a) にさらに、7 行目（行 C の activation_zone）の `peak_lon` を `135.00002146` に、6 行目（行 B の activation_zone）の `peak_lat`・`peak_lon` を `34.99999777`・`135.00002146` に替えたもの | `read_zone_features(path)` | (a) ZF4（`{list}` は `34.99999777,135.00002146 の delete_zone（1・3 番目）`）。(b) ZF4（`{list}` は `34.99999777,135.00002146 の delete_zone（1・3 番目）、34.99999777,135.00002146 の activation_zone（4・5・6 番目）`）。替える前のファイル（UT 19）では、同じ画素の delete と activation（1 番目と 4 番目）は誤りにならない |
| `UT-cmp5_common-23` | GeoJSON が無い・読めない | 同じプロセス。(a) 無いパス、(b) 一時のディレクトリ、(c) `FF FE` だけのファイル、(d) 先頭に BOM を付けたゾーンの 13 行 | `read_zone_features(path)` | (a) ZF1、(b) ZF2、(c) ZF2（`UTF-8 として読めない`）、(d) ZF3（`JSON として読めない:` で始まる） |
| `UT-cmp5_common-24` | 例外の型 | 同じプロセス | `InputError('MP1', 'x')` を作る | `Exception` の子、`symbol` が `'MP1'`、`what` と `str(e)` が `'x'` |

- UT 12 の行の番号: 見出しが 1 行目、行 A が 2 行目、替えた行が 3 行目。UT 13・14 は替えた行が 2 行目。
- UT 21 の (c)〜(k)・(m) の「1 番目」は、ゾーンの 13 行の 2 行目が `features` の 1 番目であることによる。UT 22 の (a) は、ゾーンの 13 行の 4 行目が `features` の 3 番目であることによる。

### 7.2 `merge_peaks`

- **ID**: LLD-merge_peaks
- **対応 HLD**: [3.5](30_HLD.md#35-cmp5-統合突合)・[4.7](30_HLD.md#47-fr-007-per-mesh-csv-出力プロミネンス閾値適用)・[4.8](30_HLD.md#48-fr-008-per-mesh-csv-統合)・[5.1](30_HLD.md#51-nfr-001-精度検出網羅性)・[5.2](30_HLD.md#52-nfr-002-メモリ使用量)・[5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)・[5.5](30_HLD.md#55-nfr-005-処理時間目標)
- **ファイル**: `scripts/merge_peaks.py`

関数の名前と役割と呼ぶ順は [HLD 3.5.3](30_HLD.md#353-関数) の `merge_peaks` の関数の表のとおりで、処理の正本は [HLD 4.8.2](30_HLD.md#482-処理の流れ)・[4.8.3](30_HLD.md#483-異常系) である。この節は、それを Python で書くための細部（引数の読み方、型、止まり方、メッセージの文面、UT 候補）だけを足す。`merge_peaks` は CMP3（パイプライン制御）が起動する内部の起動口で、`--config <絶対パス>` を必ず受け取る（[HLD 2.4.5](30_HLD.md#245-内部引数)）。

- [4.7](30_HLD.md#47-fr-007-per-mesh-csv-出力プロミネンス閾値適用)（Z15 の画素の変換と所属メッシュ）は、ピークの画素を [7.1](#71-cmp5_common) の `latlon_to_z15_pixel` で、所属メッシュを `latlon_to_mesh`（[2.4](#24-言語ごとに別に実装する式のテストベクトル)の計算の決まりと表 5）で、CMP4（地形解析エンジン）と同じ式で求めることで受ける（HLD の [DEC6](30_HLD.md#225-設計判断決めたこと理由却下した案)「メッシュ・タイル変換の二重実装を許容」と [DEC55](30_HLD.md#474-設計判断)「地理的範囲フィルタは CSV に書く値で判定する」）。
- [5.1](30_HLD.md#51-nfr-001-精度検出網羅性)（精度）は、`filter_by_prominence` が最終フィルタを `key_col_resolved=false` の行に当てないことと、広域で確定したピークを落としたときの警告 FW1 で受ける。
- [5.2](30_HLD.md#52-nfr-002-メモリ使用量)（メモリ）は、`read_peak_rows` が 1 行ずつ渡すこと、ピークの表が代表行の候補 1 つと 2 つの数だけを持つこと、1 つのファイルの画素の `dict` を次のファイルに持ち越さないことで受ける。メモリのピークは、実装の後に HLD 5.2.2 の「実測の計画」の 3「CMP5 の統合」で測る。
- [5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)（再現性）は、代表の比べ方が全順序であること（`_rank`）、行の順が Z15 の画素の順であること（[DEC83](30_HLD.md#484-設計判断)「`merged_peak.csv` は Z15 の画素の順」）、per-mesh CSV の 10 列を字句のまま写すことで受ける。
- [5.5](30_HLD.md#55-nfr-005-処理時間目標)（処理時間）は、per-mesh CSV を 1 回だけ読むことと、`apply_land_peaks` の計算の数（ピークの数 × 陸地最高峰リストの行の数）で受ける。所要は HLD 5.5.2 の「実測の計画」の 3 で測る。
- 結合のつなぎ目は、`CMP5-EXT1`（CMP4 → `merge_peaks`。[6.7](#67-analyze_terrain_csv) が書く 10 列と名前を `read_peak_rows` と `select_peak_csv_files` がそのまま読む）、`CMP5-EXT3`（CMP1（行政区域前処理） → `merge_peaks`。`read_target_meshes`）、`CMP5-INT1`〜`CMP5-INT3`（`write_merged_peak` が書く 13 列と行の順。[7.1](#71-cmp5_common) の `read_merged_peak` が読む）、`CMP5-EXT6`（引数と終了コード）である（[HLD 3.5.5](30_HLD.md#355-結合のつなぎ目)）。IT のケースは `60_IT.md` の `IT-CMP5-INT1-01`・`02`、`IT-CMP5-INT2-01`・`02`、`IT-CMP5-EXT1-01`・`02` ほか。
- findsummits#202（HLD を書く段で挙がった UT と IT の候補の割り当て）の「4.8.5 の 7」の後半（30m と比べる処理）は、[7.2.5](#725-ut-候補)の UT 17 が受ける（前半の距離を求める処理は [7.1.5](#715-ut-候補)の `UT-cmp5_common-06`）。
- 陸地最高峰リストのファイルの作成と最初の 3 件の座標は、CMP5 の実装の段で行う（HLD 4.8.1 の対象外の行）。この節は読み方と当て方だけを決める。

#### 7.2.1 ファイル割付

- 関数はすべて `scripts/merge_peaks.py` 1 本に置く（ADR-LLD-001 の Decision 5）。`venv/bin/python3 scripts/merge_peaks.py` で起動され（[HLD 3.5.1](30_HLD.md#351-プログラム)）、共通部品は `import common`、CMP5 の共通部品は `import cmp5_common` で読む（[2.1.1](#211-ファイル割付)・[7.1.1](#711-ファイル割付)と同じ）。7.1 の部品は `cmp5_common.great_circle_m(...)` のようにモジュールの属性として呼ぶ（`from cmp5_common import …` で名前を写さない。UT 17 が `merge_peaks.cmp5_common.great_circle_m` を差し替えて、距離を求める処理と 30m と比べる処理を分けて確かめるため）。ほかに読むのは、標準の `csv`・`decimal`・`math`・`os`・`re`・`shlex`・`sys` と、`dataclasses` の `dataclass`・`replace`、`typing` の `Iterator`・`Sequence` である。
- ファイルの先頭のコメントに `# trace: LLD-merge_peaks` を書く。起動の部分は `if __name__ == '__main__': main()`。
- UT のコードは `tests/scripts/test_merge_peaks.py` に置く。各テストに `# trace: UT-merge_peaks-NN` のコメントを付ける。[2.4](#24-言語ごとに別に実装する式のテストベクトル)の表 5 を写したテストには、`2.4 の表 5` もコメントに書く（[テスト方針書 3.3](02_test_policy.md#33-期待値の根拠)）。テストの枠組みは [2.1.1](#211-ファイル割付)と同じく標準の `unittest`。

#### 7.2.2 型とデータ

- 内部の定数（モジュールの最上位。名前は `_` で始める）:
  - ソースツリーのパス: `_SOURCE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))`、`_JAPAN_MESH_LIST_PATH = os.path.join(_SOURCE_ROOT, 'params', 'mesh_list_japan.txt')`、`_LAND_PEAKS_PATH = os.path.join(_SOURCE_ROOT, 'params', 'land_highest_peaks.csv')`（[HLD 2.3.2](30_HLD.md#232-設定ファイル)の「自分の置き場からソースツリーを求めて読む」。[3.1.2](#312-型とデータ)と同じ形）。
  - `_PEAK_CSV_COLUMNS = cmp5_common.MERGED_PEAK_ALL_COLUMNS[:10]`（per-mesh CSV の 10 列。[6.7.2](#672-型とデータ)の `_header` と同じ並び）。書き出しの見出しは `cmp5_common.MERGED_PEAK_ALL_COLUMNS`（13 列）。
  - `_LAND_HEADER = ('name', 'peak_lat', 'peak_lon')`（[SRS §8.1](20_SRS.md#81-内部データ一覧) の No.10）。
  - `_LAND_RADIUS_M = 30.0`（HLD の [DEC80](30_HLD.md#484-設計判断)「陸地最高峰リストは 30m 以内の 1 件に当てる」）。
  - 海面確定の値（[HLD 4.8.2](30_HLD.md#482-処理の流れ)の 5「陸地最高峰の海面確定を当てる」）: `_SEA_COL_ELEV = '0.00'`、`_SEA_COL_COORD = '0.00000000'`、`_SEA_COL_MARGIN = '-1'`。
  - `_DECIMAL_RE = re.compile(r'[+-]?[0-9]+(\.[0-9]+)?')`・`_INTEGER_RE = re.compile(r'[+-]?[0-9]+')`（どちらも `fullmatch` で使う。[7.1.3](#713-関数の細部)の前置きの「10 進の数の決まり」と同じ字句）。
  - `_CONFIG_KEYS_USED = ('data_dir', 'log_dir', 'prominence_primary_m', 'prominence_final_m')`（[HLD 2.3.2](30_HLD.md#232-設定ファイル)の表で CMP5 の [FR-008](20_SRS.md#fr-008-per-mesh-csv-統合) が使うキー。`load_config` に渡す）。必須は `('data_dir',)`。
- 内部の状態（モジュールの最上位）: `_config_opt: str = ''`（`main` の 5 が入れる、[7.2.4](#724-メッセージ文面)の `{config_opt}` の値。`main` を通らない同じプロセスの UT は空のまま使う）。
- `@dataclass(frozen=True) class _Args`（内部）:
  - `config: str`: `--config` の値のまま。
  - `mesh_codes: set[str] | None`: `--mesh` を `common.read_mesh_arg` で読んだ集合。無ければ `None`。
  - `check_land_peaks: bool`。
- `@dataclass(frozen=True) class LandPeak`: 陸地最高峰リストの 1 行。フィールドはこの順に並べる。
  - `name: str`。
  - `peak_lat: str`・`peak_lon: str`: ファイルの字句のまま。
  - `line_no: int`: 記録の番号。[7.1.3](#713-関数の細部)の `read_merged_peak` の 2 と同じ数え方で、見出しの記録が 1。
  - `path: str`: 読んだリストの絶対パス。LP4・LW1・LW2 の `{path}` に使う（`apply_land_peaks` はパスを受け取らないため、行に持たせる）。
- `@dataclass(frozen=True) class PeakFile`: `path: str`（絶対パス）、`analysis_id: str`（ファイル名から `.csv` を除いたもの）、`is_normal: bool`（通常なら真、広域なら偽）。
- `@dataclass(frozen=True) class PeakRow`: per-mesh CSV の 1 行。フィールドはこの順に並べる（UT が位置の引数で作るため）。
  - `peak_lat`・`peak_lon`・`peak_elev`・`col_lat`・`col_lon`・`col_elev`・`prominence`: `str`（ファイルの字句のまま）。
  - `key_col_resolved: bool`。
  - `col_margin_px: str`・`analysis_id: str`。
  - `pixel: tuple[int, int]`: `peak_lat`・`peak_lon` の Z15 の画素 (gx, gy)。
  - `is_normal: bool`。
- `@dataclass class PeakEntry`: ピークの表の値（可変。`pick_representative`・`derive_stability`・`apply_land_peaks` が書き換える）。
  - `rep: PeakRow`: その時点の代表行の候補。
  - `normal_count: int = 0`: 通常の行の数。
  - `normal_unresolved: bool = False`: 通常の行に `key_col_resolved=false` があったか。
  - `analysis_count: str = ''`・`expected_count: str = ''`・`stability: str = ''`: `derive_stability` が入れる、書き出しの文字列。
  - `sea_fixed: bool = False`: `apply_land_peaks` が海面確定に書き換えたか。
- ピークの表: `dict[tuple[int, int], PeakEntry]`（鍵は (gx, gy)。HLD 3.5.3 の「プログラムの中で受け渡す内部データは『ピークの表』1 つ」）。
- `slots=True` は付けない（7.1 の `JsonNumber` と同じく、メモリの実測〈HLD 5.2.2 の「実測の計画」の 3〉の後に決める）。

#### 7.2.3 関数の細部

関数ごとに `#####` の見出し（関数の名前だけ。ほかの節に同じ名前の見出しがあるものは `（merge_peaks）` を添える）を立てて書く。内部の関数は、使う関数の見出しの下に書く。

**止まり方**: 7.2 の関数は、誤りを見つけたら、[7.2.4](#724-メッセージ文面)のメッセージを `common.log_error` で出してから `sys.exit(common.EXIT_ERROR)` で止まる（`start_log` の前の引数と設定の誤りは `common.EXIT_USAGE`）。[2.1.3](#213-関数の細部)の前置きの型の「部品かここで `sys.exit`」にあたる。7.2 が使う 7.1 の部品（`is_valid_coord`・`latlon_to_z15_pixel`・`great_circle_m`・`parse_analysis_id`）は `InputError` を上げないので、7.2 は `cmp5_common.InputError` を捕まえない（`read_merged_peak`・`read_zone_features` は 7.2 では使わない）。警告（`WARNING:`）は、関数が中身を返し、`main` が `common.log_warning` で出す（HLD 3.5.3 の表の「警告に並べるもの」を返す形）。

**10 進の数の決まり**: [7.1.3](#713-関数の細部)の前置きの決まりと同じ字句と判定を、内部の関数で持つ（7.1 の内部の関数はほかのモジュールから呼べない〈[1.2](#12-lld-の規約)〉ので、7.2 が同じものを自分で持つ）。

- `_is_finite_decimal(s: str) -> bool`: `_DECIMAL_RE.fullmatch(s)` が合い、かつ `math.isfinite(float(s))` が真。
- `_is_integer(s: str) -> bool`: `_INTEGER_RE.fullmatch(s)` が合う。
- `_is_zero(s: str) -> bool`: 有限の 10 進の数で、`decimal.Decimal(s) == 0`。
- 値の比べ（[DEC92](30_HLD.md#494-設計判断)「採番と主ピークの比べ方は 10 進の値で行う」）は `decimal.Decimal` で行う。

**{reason}**: [2.1.4](#214-メッセージ文面)と同じ（`OSError` の `strerror`、無ければ `str(e)`。`UnicodeDecodeError` なら `UTF-8 として読めない`）。`{path}` は `os.path.abspath` したパス。

**5.1・5.2・5.3・5.5 の受け方**: 7.2 の前置きに書いた。

##### main（merge_peaks）

`main() -> None`（起動の部分）。[2.1.3](#213-関数の細部)の前置きの呼ぶ側の書き方の型に従い、次の順に行う。

1. `start = common.StartTime.now()`。
2. `args = _parse_args(sys.argv[1:])`。
3. `config = common.load_config(args.config, _CONFIG_KEYS_USED, ('data_dir',))`。`data_dir`・`log_dir`・`final_m`（`prominence_final_m` の値）を取り出す。
4. `_check_cross(config)`。
5. `common.start_log(log_dir, config, 'merge_peaks', sys.argv[1:], start)`。ロックは掛けない（内部の起動口は CMP3 のロックの下で動く。[HLD 2.9.3](30_HLD.md#293-同時起動の排他)）。`_config_opt` に [7.2.4](#724-メッセージ文面)の `{config_opt}` の値を入れる。`config.path == common.DEFAULT_CONFIG_PATH` なら空の文字列、それ以外は `' --config ' + shlex.quote(config.path)`（利用者が `run_pipeline` に `--config` を渡したかを `merge_peaks` は受け取らないので、既定のパスかで決める。[5.1](#51-run_pipeline)の `{config_opt}` と同じ形になる）。
6. `try` の前に `completed = False`、`code = common.EXIT_OK`、要約の数（`normal_files`・`wide_files`・`rows`・`peaks`・`sea`・`dropped`・`written` をどれも 0、`land_count = 0`）を置く。`try` の中で次を行う。
   1. `land = read_land_peaks(_LAND_PEAKS_PATH)`。
   2. `args.check_land_peaks` が真なら、`land_count = len(land)`、`completed = True` にし、3〜9 を行わない（`if`/`else` で分ける。`return` を使わない）。
   3. `targets = read_target_meshes(_JAPAN_MESH_LIST_PATH, os.path.join(data_dir, 'boundaries', 'nt_excluded_meshes.txt'))`（名前は [3.1.2](#312-型とデータ)の `_OUTPUT_NAMES` の北方領土除外メッシュリストと同じ）。
   4. `csv_dir = os.path.join(data_dir, 'results', 'csv')`。`files, skipped, missing = select_peak_csv_files(csv_dir, args.mesh_codes)`。`skipped` が空でなければ PW1、`missing` が空でなければ PW2 を `common.log_warning` で出す（この順）。`files` が空なら PM1 を出して `sys.exit(common.EXIT_ERROR)`。
   5. `table = {}`。`files` の順に、`is_normal` なら `normal_files`、偽なら `wide_files` を 1 増やし、`for row in read_peak_rows(f.path, f.analysis_id, f.is_normal):` で `rows` を 1 増やして `pick_representative(table, row)` を呼ぶ。
   6. `peaks = len(table)`。`derive_stability(table, targets)`。
   7. `apply_land_peaks(table, land)` の返す `(what, action)` を順に `common.log_warning` で出す。`sea` は `sea_fixed` が真の値の数。
   8. `kept, dropped, wide_dropped = filter_by_prominence(table, final_m)`。`wide_dropped` が空でなければ FW1 を出す。
   9. `written = write_merged_peak(kept, os.path.join(data_dir, 'results', 'merged_peak.csv'))`。`completed = True`。
7. `finally` で結果の要約を `common.log_info` で出す。`completed` が偽なら ML3、真で `args.check_land_peaks` なら ML2、真でなければ ML1。
8. `sys.exit(code)`。

`start_log` の前に止まる誤り（`_parse_args`・`load_config`・`_check_cross`）は、標準エラー出力だけに出て、ログファイルと `log_dir` を作らない（[HLD 3.5.3](30_HLD.md#353-関数)の「ここまでの誤りは、ログファイルを作らずに終了コード 2」）。

##### _parse_args（merge_peaks）

`_parse_args(argv: Sequence[str]) -> _Args`（内部）。[6.1.3](#613-関数の細部)の `parse_args` と同じ受け方で、最初に見つけた誤り 1 つで、[7.2.4](#724-メッセージ文面)のメッセージを `common.log_error` で出して `sys.exit(common.EXIT_USAGE)`。

1. `argv` を左から読む。
   - `--config`・`--mesh` なら、その名前がすでに出ていれば MA3（値を見る前に判定する）、最後の引数なら MA2、そうでなければ次の引数を値にして 2 つ進む（値は `-` で始まっていてもそのまま値にする）。
   - `--check-land-peaks` なら、すでに出ていれば MA3、そうでなければ印を立てて 1 つ進む。
   - ほかの引数（位置引数、知らない名前、`=` の付いた形〈`--config=/a.ini`・`--check-land-peaks=x`〉、`--help`、`--` だけ、空の引数）は MA1。`=` の形と `--help` を受けないのは、`run_pipeline` が名前と値を別の引数で渡す内部の起動口だから（[HLD 2.4.2](30_HLD.md#242-共通の書式)・[2.4.5](30_HLD.md#245-内部引数)。[5.2](#52-resolve_config)・[6.1](#61-analyze_terrain_launch)と同じ）。
2. `--config` が無ければ MA4。
3. `--config` の値が `os.path.isabs` で偽なら（空を含む）MA5。値は正規化しない。
4. `--mesh` と `--check-land-peaks` の両方があれば MA6（[HLD 2.4.2](30_HLD.md#242-共通の書式)の「組み合わせの誤り」。`--check-land-peaks` は `--mesh` を使わないので、黙って捨てない）。
5. `--mesh` があれば `common.read_mesh_arg(<値>)`（誤りは `read_mesh_arg` が A1〜A5 で止まる）。ファイルを読む処理を、引数の形の誤りより後にする（6.1.3 と同じ）。
6. `_Args(config, mesh_codes, check_land_peaks)` を返す。

##### _check_cross（merge_peaks）

`_check_cross(config: common.Config) -> None`（内部）。`prominence_primary_m` の値が `prominence_final_m` の値以上なら、[2.2](#22-ログとメッセージの文面)の CX1 を出して `sys.exit(common.EXIT_USAGE)`（どちらもデフォルトのときも比べる。[5.2](#52-resolve_config)の `_check_resolved` の 2、[6.1](#61-analyze_terrain_launch)の `_check_cross` と同じ）。`{primary}`・`{final}` は 10 進、`{primary_source}`・`{final_source}` は `from_file` が真なら `ファイル`、偽なら `デフォルト`、`{config_path}` は `config.path`。

##### read_land_peaks

`read_land_peaks(path: str) -> list[LandPeak]`

1. `abspath = os.path.abspath(path)`。`os.path.exists(abspath)` が偽なら LP1。`open(abspath, encoding='utf-8-sig', newline='')` を `with` で開き（`OSError` は LP2。ディレクトリも LP2）、`csv.reader(f, strict=True)` で読む。
   - 先頭の BOM（U+FEFF）を 1 つだけ除く（HLD 4.8.1 の対象外の行の「陸地最高峰リストの先頭の BOM の扱い」。リストは人が手で書くファイルで、表計算のソフトが BOM を付けて保存しうるため。[2.1.3](#213-関数の細部)のメッシュのリストの読み方と同じ）。
   - 読む途中の `UnicodeDecodeError` と `OSError` は LP2、`csv.Error` は LP3（`{detail}` は `{line_no} 行目を CSV として読めない: {reason}`。`{reason}` は `str(e)`）。
   - `line_no` の数え方は [7.1.3](#713-関数の細部)の `read_merged_peak` の 2 と同じ（各記録を読み始める前に 1 つ増やす。空の記録も数える）。
2. 空の記録（`csv.reader` が空のリストを返す記録。空行）は、見出しの前でも後でも飛ばす（[HLD 4.8.2](30_HLD.md#482-処理の流れ)の 1「リストを読む」の「空行は無視する」）。空白だけの行は空の記録でなく、1 列の記録になる。
3. 見出し: 最初の空でない記録が `list(_LAND_HEADER)` と等しくなければ LP3（`見出しの行が name,peak_lat,peak_lon でない: {line}`。`{line}` は記録を `,` でつないだもの）。空でない記録が 1 つも無ければ LP3（`見出しの行が無い`）。
4. データの行（見出しの後の空でない記録）: 次の順に見て、最初に外れたもので LP3。
   - 列の数が 3 でない: `{line_no} 行目の列の数が {count} で 3 でない`。
   - `name` が空の文字列: `{line_no} 行目の name が空`（空白だけの名前は空としない）。
   - `cmp5_common.is_valid_coord(peak_lat, 'lat')` が偽: `{line_no} 行目の peak_lat が 座標として読めない: {value}`。`peak_lon` も同じ（`'lon'`）。
   - 値の前後の空白は除かない（`' 35.0'` は座標として読めない）。リストの座標は解析の値や `merged_summit.xlsx` の値を桁を落とさずに写すもので（HLD の [DEC80](30_HLD.md#484-設計判断)「陸地最高峰リストは 30m 以内の 1 件に当てる」）、写し違いを黙って直さないため。CMP3 が起動時にこの関数で確かめるので、空白の誤りは解析の前に止まる。
   - 同じ名前や同じ座標の行は誤りにしない（HLD 4.8.2 の 5「陸地最高峰の海面確定を当てる」の「同じピークに 2 つ以上のリストの行が当たっても、1 回当てたのと同じになる」）。
5. 行を `LandPeak(name, peak_lat, peak_lon, line_no, abspath)` にして、ファイルの順に返す。データの行が 0 なら空のリスト。

##### read_target_meshes

`read_target_meshes(japan_path: str, nt_path: str) -> set[str]`

`guidance = _mesh_list_guidance()` とし、`japan = common.read_mesh_list_file(japan_path, guidance)`、`nt = common.read_mesh_list_file(nt_path, guidance)` の順に読み（無い・読めない・誤りの行は R1〜R3 で終了コード 1）、`japan - nt` を返す。内部の関数 `_mesh_list_guidance() -> str` は、[7.2.4](#724-メッセージ文面)の R1〜R3 の案内の文に、その時点の `_config_opt` を入れた文字列を返す（`_config_opt` は `main` の 5 で決まるので、呼ぶたびに作る）。どちらのリストも空の集合を誤りにしない（[2.1.3](#213-関数の細部)の `read_mesh_list_file` のとおり。日本全土のリストが空なら、どのピークの `expected_count` も 0 になる）。

##### select_peak_csv_files

`select_peak_csv_files(csv_dir: str, mesh_codes: set[str] | None) -> tuple[list[PeakFile], list[str], list[str]]`

1. `abspath = os.path.abspath(csv_dir)`。`names = os.listdir(abspath)`。`FileNotFoundError` なら名前が 0 として続ける（下の 5 で PM1 になる）。ほかの `OSError`（ディレクトリでない、権限が無い）は PM2（`{path}` は `abspath`）。
2. 名前を Unicode の符号位置の昇順（`sorted(names)`）に見る。`.csv` で終わらない名前（大文字の `.CSV` を含む）は見ない。`.csv` で終わる名前は `stem, kind = cmp5_common.parse_analysis_id(name)`。
   - `kind` が `ANALYSIS_INVALID` なら、`os.path.join(abspath, name)` を `skipped` に足す（HLD の [DEC84](30_HLD.md#484-設計判断)「名前の規則に合わないファイルは読まずに警告する」）。
   - `ANALYSIS_NORMAL` なら、`mesh_codes` が `None` か、`stem[2:6]` が `mesh_codes` にあれば、`PeakFile(os.path.join(abspath, name), stem, True)` を `files` に足す。無ければ黙って読まない。
   - `ANALYSIS_WIDE` なら、`mesh_codes` が `None` のときだけ `PeakFile(…, stem, False)` を足す（`--mesh` があれば広域は読まない。HLD 4.8.2 の 2「読むファイルを選ぶ」）。
   - ファイルの種類（通常のファイルか）は見ない（ディレクトリなら `read_peak_rows` の `open` で PM2）。
3. `missing`: `mesh_codes` が `None` でなければ、`mesh_codes` のうち、`files` の通常の `stem[2:6]` に無いコードを昇順に並べたもの。`None` なら空のリスト。
4. `(files, skipped, missing)` を返す。`files` と `skipped` は名前の昇順。
5. `files` が空のときの PM1 は `main` が出す（`main` の 6 の 4。警告を先に出すため）。

##### read_peak_rows

`read_peak_rows(path: str, analysis_id: str, is_normal: bool) -> Iterator[PeakRow]`（生成関数。1 行ずつ渡し、ファイルの全体を一度に持たない）

1. `open(path, encoding='utf-8', newline='')` を `with` で開き（`OSError` は PM2。ディレクトリも、選んだ後に消えたファイルも PM2）、`csv.reader(f, strict=True)` で読む。
   - BOM は除かない（CMP4 は BOM を書かないので、BOM があれば見出しが違う誤りになる）。
   - 読む途中の `UnicodeDecodeError`・`OSError` は PM2、`csv.Error` は PM3（`{line_no} 行目を CSV として読めない: {reason}`）。
   - `line_no` は [7.1.3](#713-関数の細部)の `read_merged_peak` の 2 と同じ数え方。`{path}` は `path`。
2. 見出し: 記録が無ければ PM3（`見出しの行が無い`）。最初の記録が `list(_PEAK_CSV_COLUMNS)` と等しくなければ PM3（`見出しの行が 10 列の並びでない: {line}`）。
3. データの行: 列の数が 10 でなければ PM3（`{line_no} 行目の列の数が {count} で、見出しの行の 10 と違う`。空の記録も列の数 0 としてここに当たる。CMP4 は空行を書かないため）。合えば、`key_col_resolved` を先に見て、次に下の表の列の順に見て、最初に外れたもので PM3（表の 1 行に 2 つの列があるときは左の列から、1 つの列に確かめが 2 つあるときは表に書いた順に見て、その列を終えてから次の列へ進む。たとえば `false` の行の `col_lat` は、有限の 10 進の数か、数として 0 かの順に見た後に `col_lon` へ進む。`{line_no} 行目の {column} が {condition}: {value}`。`{value}` は文字列のまま。[7.1.4](#714-メッセージ文面)の文の形と同じ）。

   | 列 | 確かめ | `{condition}` |
   |---|---|---|
   | `key_col_resolved` | 文字列がちょうど `true` か `false` | `true か false でない` |
   | `peak_lat`・`peak_lon` | `cmp5_common.is_valid_coord(v, 'lat')`・`(v, 'lon')` | `座標として読めない` |
   | `peak_elev` | 有限の 10 進の数 | `有限の 10 進の数でない` |
   | `col_lat`・`col_lon` | 有限の 10 進の数。`false` の行はさらに数として 0 | `有限の 10 進の数でない`、`数として 0 でない` |
   | `col_elev`・`prominence` | `true` の行は有限の 10 進の数、`false` の行は空 | `有限の 10 進の数でない`、`空欄でない` |
   | `col_margin_px` | 整数 | `整数でない` |
   | `analysis_id` | `analysis_id`（引数）と同じ文字列 | `ファイル名と違う` |

4. 画素: `pixel = cmp5_common.latlon_to_z15_pixel(float(peak_lat), float(peak_lon))`。このファイルの中で同じ画素がすでにあれば PM3（`{line_a} 行目と {line_b} 行目が同じ Z15 の画素 ({gx}, {gy}) の行`。`{line_a}` は先の行）。画素から行の番号への `dict` は、この呼び出しの中だけで持つ（次のファイルでは持ち越さない。HLD 4.8.2 の「メモリ」）。
5. `PeakRow(…, key_col_resolved=(値 == 'true'), …, pixel, is_normal)` を渡す。データの行が 0 なら何も渡さない（見出しだけのファイルは誤りにしない。[HLD 4.7.2](30_HLD.md#472-処理の流れ)の「0 件でも見出しの行だけのファイルを書く」）。

##### pick_representative

`pick_representative(table: dict[tuple[int, int], PeakEntry], row: PeakRow) -> dict[tuple[int, int], PeakEntry]`

1. `entry = table.get(row.pixel)`。無ければ `table[row.pixel] = PeakEntry(rep=row)` を作り、`entry` にする（代表は `row`）。
2. `row.is_normal` なら `entry.normal_count += 1`。さらに `not row.key_col_resolved` なら `entry.normal_unresolved = True`。
3. 1 で作ったのでなければ、`_rank(row) < _rank(entry.rep)` のときだけ `entry.rep = row`。
4. `table` を返す（同じオブジェクト）。

`_rank(row: PeakRow) -> tuple`（内部）は、小さいほど代表に選ぶ鍵:

```python
(
    0 if row.key_col_resolved else 1,
    decimal.Decimal(row.col_elev).copy_negate() if row.key_col_resolved else decimal.Decimal(0),
    0 if row.is_normal else 1,
    row.analysis_id,
)
```

- 符号は `copy_negate()` で反転する。単項の `-` は既定の精度 28 桁で丸めるので、`1000.0000000000000000000000001` と `1000.0000000000000000000000002` が同じ鍵になる。
- 順は [FR-008](20_SRS.md#fr-008-per-mesh-csv-統合) の代表採用の 1〜4（確定した行が先、`col_elev` の高い順、通常が先、`analysis_id` の昇順）。`col_elev` は数で比べ、`analysis_id` は文字列の順。
- `analysis_id` はピークごとに重ならない（`read_peak_rows` がファイル名と等しいことを確かめ、ファイル名は重ならない）ので、どの 2 行も同じ鍵にならない。そのため、ファイルを読む順によらず同じ行が残る（[HLD 4.8.2](30_HLD.md#482-処理の流れ)の 4「代表行を選ぶ」）。

##### derive_stability

`derive_stability(table: dict[tuple[int, int], PeakEntry], targets: set[str]) -> dict[tuple[int, int], PeakEntry]`

各 `entry` について、次を入れて `table` を返す。

- `analysis_count = str(entry.normal_count)`（代表が広域の行でも、通常の行の数。[FR-008](20_SRS.md#fr-008-per-mesh-csv-統合)）。
- `expected_count`: 代表が通常の行なら、次で求めた数を `str` にしたもの。代表が広域の行なら `''`。
  - `code = latlon_to_mesh(float(rep.peak_lat), float(rep.peak_lon))`、`aa = int(code[:2])`・`bb = int(code[2:])`。
  - `aa + da`・`bb + db`（`da`・`db` はそれぞれ −1・0・1）のうち、どちらも 0〜99 の組を `f'{a:02d}{b:02d}'` のコードにして、`targets` にあるものの数（所属メッシュを含む 9 つのうち）。
- `stability`:
  - 代表が広域の行なら、`rep.key_col_resolved` が偽なら `unstable`、真なら `-`。
  - 代表が通常の行なら、`entry.normal_unresolved` が真か、`analysis_count != expected_count` なら `unstable`、それ以外は `confirmed`。

##### latlon_to_mesh（merge_peaks）

`latlon_to_mesh(lat: float, lon: float) -> str`

[2.4](#24-言語ごとに別に実装する式のテストベクトル)の計算の決まりの `latlon_to_mesh` のとおり、`aa = math.floor((lat * 3) / 2)`、`bb = math.floor(lon) - 100`。どちらも 0〜99 なら `f'{aa:02d}{bb:02d}'` を返す。0〜99 に入らなければ `ValueError`。

- これが 2.4 の「0〜99 に入らないときの扱いは各言語の節で決める」の Python の扱い。呼ぶのは `derive_stability` だけで、渡すのは CMP4 が地理的範囲フィルタを通した per-mesh CSV の代表行の座標なので、日本の範囲（`aa` 30〜68、`bb` 22〜53）に入る。
- 範囲の外は、CMP4 の欠陥か手で書き換えたファイルで、[2.2](#22-ログとメッセージの文面)の G7 で止まる（`is_valid_coord` を通る緯度 70.0 や経度 −170.0 も当たる）。
- HLD 4.8.2 の 3「行を読む」の確かめの列挙に無い確かめを足さず、PM3 の案内でなく G7 の「開発者に知らせる」で止めるのは、CMP4 の地理的範囲フィルタ（[FR-008](20_SRS.md#fr-008-per-mesh-csv-統合) の不変条件）が破れたことを示すため。
- NaN と無限大は `read_peak_rows` の座標の確かめで来ない。

##### apply_land_peaks

`apply_land_peaks(table: dict[tuple[int, int], PeakEntry], land: list[LandPeak]) -> list[tuple[str, str]]`

`land` の順に、各行 `p` について次を行い、警告の `(what, action)` を順に並べて返す。[HLD 3.5.3](30_HLD.md#353-関数)の表の「海面確定を当てたピークの表」は、引数の `table` をその場で書き換えることで返す（戻り値は警告の並びだけ）。

1. `hits` は、`table` の値のうち `cmp5_common.great_circle_m(float(p.peak_lat), float(p.peak_lon), float(e.rep.peak_lat), float(e.rep.peak_lon)) <= _LAND_RADIUS_M` のもの（距離も控える）。`hits` は画素の (gy, gx) の昇順に並べる。距離の計算と 30m との比べを分けるのは、findsummits#202 の「4.8.5 の 7」による（UT 16・17）。
2. `hits` が 2 つ以上なら LP4 を出して `sys.exit(common.EXIT_ERROR)`。それまでの行で集めた警告（LW1・LW2）は出さない（止まる誤りを直して起動し直せば、同じ警告がまた出るため）。
3. 0 なら LW1 の `(what, action)` を足す。
4. 1 つ（`e`）なら:
   - `e.rep.key_col_resolved` が偽なら、`e.rep = replace(e.rep, key_col_resolved=True, col_elev=_SEA_COL_ELEV, prominence=e.rep.peak_elev, col_lat=_SEA_COL_COORD, col_lon=_SEA_COL_COORD, col_margin_px=_SEA_COL_MARGIN)`、`e.sea_fixed = True`。ほかの列（`peak_lat`・`peak_lon`・`peak_elev`・`analysis_id`）と、`analysis_count`・`expected_count`・`stability` は変えない（[HLD 4.8.2](30_HLD.md#482-処理の流れ)の 5。`stability` は代表採用の時点の値）。
   - 真で、`_is_zero(col_lat)` と `_is_zero(col_lon)` の両方が真なら（すでに海面確定の行）、何もしない。
   - 真で、どちらかが 0 でなければ（陸のコルで確定）、書き換えずに LW2 の `(what, action)` を足す（HLD の [DEC81](30_HLD.md#484-設計判断)「陸のコルで確定したピークは陸地最高峰リストで書き換えない」）。
5. 同じピークに 2 つ以上の行が当たったときは、2 つ目は 4 の 2 つ目（すでに海面確定）に当たるので、1 回当てたのと同じになる。

5.5（処理時間）: 行ごとに表のすべての値との距離を求める（リストは数件なので、ピークの数 × 数件の計算）。所要は HLD 5.5.2 の「実測の計画」の 3 で測る。

##### filter_by_prominence

`filter_by_prominence(table: dict[tuple[int, int], PeakEntry], final_m: int) -> tuple[dict[tuple[int, int], PeakEntry], int, list[PeakEntry]]`

`rep.key_col_resolved` が真で `decimal.Decimal(rep.prominence) < final_m` の値を落とす（`key_col_resolved=false` は落とさない。[FR-008](20_SRS.md#fr-008-per-mesh-csv-統合)）。返すのは、残った値の新しい `dict`（鍵と値は元のまま、元の順）、落とした数、落とした値のうち代表が広域の行のもの（`list[PeakEntry]`。画素の (gy, gx) の昇順）。`table` は変えない。HLD 3.5.3 の表の「警告に並べるもの（落とした広域の行）」が 3 つ目の戻り値で、2 つ目の落とした数は結果の要約 ML1 に要るので足した。海面確定を最終フィルタの前に当てるのは `main` の順で決まる（HLD の [DEC82](30_HLD.md#484-設計判断)「陸地最高峰の海面確定を最終フィルタより先に当てる」）。

##### write_merged_peak

`write_merged_peak(table: dict[tuple[int, int], PeakEntry], out_path: str) -> int`

1. 値を画素の gy の昇順、同じ gy の中は gx の昇順に並べる（`sorted(table.items(), key=lambda kv: (kv[0][1], kv[0][0]))`。HLD の [DEC83](30_HLD.md#484-設計判断)「`merged_peak.csv` は Z15 の画素の順」）。
2. 中身: 1 行目は `cmp5_common.MERGED_PEAK_ALL_COLUMNS` を `,` でつないだもの。各行は、`rep` の 10 列（`key_col_resolved` は `true` か `false`、ほかは文字列のまま）と `analysis_count`・`expected_count`・`stability` を `,` でつないだもの。行末は LF。引用符で囲まない（どの値も確かめた字句で、`,`・`"`・改行を含まない）。値が 0 件なら見出しの行だけ。
3. [2.3](#23-ファイルの名前と書き方)の一時ファイルの決まりで `out_path + '.tmp'` に書いて、`os.replace(tmp, out_path)` で置き換える。
   - 書く: `open(tmp, 'w', encoding='utf-8', newline='\n')`、書き、`flush`、`os.fsync`、閉じる。
   - 書く段の `OSError` は、2.3 のとおり一時ファイルを消してから MF1 で止まる。置き換えの `OSError` も、一時ファイルを `os.remove` で消して（消せないときは無視する）から MF1 で止まる。
   - MF1 の `{path}` はどの段でも `out_path` の絶対パス。
   - ディレクトリ（`results/`）は作らない（無ければ `open` の失敗で MF1。`results/csv/` を作るのは [6.11](#611-analyze_terrain_stage)で、その親の `results/` もある）。
4. 書いた行の数（見出しを除く）を返す。

#### 7.2.4 メッセージ文面

書き方は [2.2](#22-ログとメッセージの文面)。設定の誤り（CF1〜CF7）と `--mesh` の誤り（A1〜A5）とメッシュのリストの誤り（R1〜R3）は [2.1.4](#214-メッセージ文面)、ログの場面（G1〜G7）と設定の相互制約（CX1）は 2.2 の文面のまま（ここに写さない）。L1〜L3 は 2.2（`{program}` は `merge_peaks`）。

- `{path}` は絶対パス、`{reason}` は [7.2.3](#723-関数の細部)の前置きのとおり。
- `{arg}`・`{value}` は受け取った値を、2.2 の引用の決まり（`shlex.quote`）で書いたもの。
- `{config_opt}` は `main` の 5 で決めた値。
- `{rerun}` は `止まったコマンドを同じ引数で起動し直す`。
- `{redo}` は `scripts/run_pipeline.sh{config_opt} を --phase なしで起動して、フェーズ2 から通しでやり直す`（[HLD 4.8.3](30_HLD.md#483-異常系)の「フェーズ2 から通しでやり直す」。`--phase` を省くと通しになる。[5.1](#51-run_pipeline)）。

| 記号 | 場面 | 1 行目（`ERROR:` か `WARNING:` と空白 1 つの後） | 2 行目（`対処:` と空白 1 つの後） | 終了コード |
|---|---|---|---|---|
| MA1 | 受け付けない引数 | `merge_peaks の知らない引数: {arg}` | `merge_peaks は run_pipeline が起動する内部の起動口。使える名前は --config・--mesh（値は次の引数で渡す）と --check-land-peaks（値をとらない）` | 2 |
| MA2 | 値が無い | `{option} の値が無い` | `{option} の後に値を渡す` | 2 |
| MA3 | 同じ名前を 2 回 | `{option} を 2 回渡した` | `{option} は 1 回だけ渡す` | 2 |
| MA4 | `--config` が無い | `--config が無い` | `--config と設定ファイルの絶対パスを渡す` | 2 |
| MA5 | `--config` が絶対パスでない | `--config のパスが絶対パスでない: {value}` | `--config に設定ファイルの絶対パスを渡す` | 2 |
| MA6 | `--mesh` と `--check-land-peaks` | `--mesh は --check-land-peaks と一緒に使えない` | `陸地最高峰リストだけを確かめるときは --mesh を渡さない` | 2 |
| LP1 | 陸地最高峰リストが無い | `陸地最高峰リストが無い: {path}` | `{path} を置いてから、{rerun}` | 1 |
| LP2 | 陸地最高峰リストを読めない | `陸地最高峰リストを読めない: {path}: {reason}` | `{path} の読み取りの権限と、UTF-8 で保存されていることを確かめてから、{rerun}` | 1 |
| LP3 | 陸地最高峰リストの書式が違う | `陸地最高峰リストの書式が違う: {path}: {detail}`（`{detail}` は 7.2.3 の `read_land_peaks` の 1〜4 の文） | `{path} を name,peak_lat,peak_lon の見出しと 1 行 1 件の形に直してから、{rerun}` | 1 |
| LP4 | 1 行の 30m 以内にピークが 2 つ以上 | `陸地最高峰リストの行の 30m 以内にピークが 2 つ以上ある: {path} の {line_no} 行目 {name}（{lat},{lon}）: {peaks}`（`{lat}`・`{lon}` はリストの字句。`{peaks}` は当たったピークごとに `{peak_lat},{peak_lon} 標高 {peak_elev} 距離 {distance}m` を 7.2.3 の順に `、` でつないだもの。`{distance}` は `f'{d:.2f}'`） | `{path} の {line_no} 行目の座標を、当てたいピークの緯度経度に直してから、{rerun}。当たったピークどうしも 30m 以内にあって直せないときは、解析の欠陥として起票する` | 1 |
| LW1 | 行がどのピークにも当たらない（`WARNING:`） | `陸地最高峰リストの行の 30m 以内にピークが無い: {path} の {line_no} 行目 {name}（{lat},{lon}）` | `--mesh で範囲を絞った統合なら対処は要らない。全国の統合なら、{path} の {line_no} 行目の座標を確かめる` | 0 |
| LW2 | 当たったピークが陸のコルで確定（`WARNING:`） | `陸地最高峰リストの行に当たったピークは陸のコルで確定しているので書き換えなかった: {path} の {line_no} 行目 {name}（{lat},{lon}）: ピーク {peak_lat},{peak_lon}、コル {col_lat},{col_lon} 標高 {col_elev}` | `{path} の {line_no} 行目が島の最高峰を指しているかを確かめる` | 0 |
| PM1 | 対象の per-mesh CSV が 1 つも無い | `統合する per-mesh CSV が 1 つも無い: {path}`（`{path}` は `results/csv/` の絶対パス） | `{redo}` | 1 |
| PM2 | per-mesh CSV を読めない | `per-mesh CSV を読めない: {path}: {reason}`（`select_peak_csv_files` の 1 では `{path}` は `results/csv/`） | `{path} の権限を確かめてから、{redo}` | 1 |
| PM3 | per-mesh CSV の書式が違う | `per-mesh CSV の書式が違う: {path}: {detail}`（`{detail}` は 7.2.3 の `read_peak_rows` の 1〜4 の文） | `{redo}` | 1 |
| PW1 | 名前の規則に合わない `.csv`（`WARNING:`） | `名前が解析識別子の形に合わない .csv を読まなかった: {paths}`（`{paths}` は `skipped` を `、` でつないだもの） | `要らないファイルなら {dir} の外へ移すか消す`（`{dir}` は `results/csv/` の絶対パス） | 0 |
| PW2 | `--mesh` のコードの通常のファイルが無い（`WARNING:`） | `--mesh のコードに対応する通常の per-mesh CSV が無い: {codes}`（`{codes}` は `missing` を `・` でつないだもの） | `フェーズ2 の解析のログで、そのメッシュを解析しなかった理由を確かめる` | 0 |
| FW1 | 広域で確定したピークを最終フィルタで落とした（`WARNING:`） | `広域解析で確定したピークを最終フィルタで落とした（プロミネンスが小さく出た見込みがある）: {list}`（`{list}` は落とした値ごとに `{peak_lat},{peak_lon} ピーク標高 {peak_elev} コル標高 {col_elev} プロミネンス {prominence} {analysis_id}` を 7.2.3 の順に `、` でつないだもの） | `一覧のピークを地形図で確かめる（merged_peak.csv は変えていない）` | 0 |
| MF1 | `merged_peak.csv` を書けない | `merged_peak.csv を書けない: {path}: {reason}` | `{dir} の空きと権限を確かめてから、{rerun}`（`{dir}` は `results/` の絶対パス） | 1 |

R1〜R3 の案内（`read_target_meshes` が `guidance` に渡す文。[HLD 4.8.3](30_HLD.md#483-異常系)の「CMP1 の作り直しの手順」と [HLD 2.10.3](30_HLD.md#2103-フェーズのやり直し)）: `venv/bin/python3 scripts/preprocess_boundaries.py --rebuild{config_opt} で北方領土除外メッシュリストを作り直し、venv/bin/python3 scripts/fetch_tiles.py{config_opt} を起動してから、{redo}（日本全土1次メッシュコードリスト params/mesh_list_japan.txt が無いか壊れているときは、先にソースツリーの版に戻す）`。

通常のログ（[HLD 4.8.2](30_HLD.md#482-処理の流れ)の 7「書き出す」と [HLD 5.7.2](30_HLD.md#572-処理の流れ)の表の `merge_peaks` の行。[2.2](#22-ログとメッセージの文面)の結果の要約の形）:

| 記号 | 行 | 文面 |
|---|---|---|
| ML1 | 結果の要約（統合） | `結果の要約: 読んだ per-mesh CSV {normal_files} 件（通常）・{wide_files} 件（広域）、行 {rows}、ピーク {peaks}、海面確定 {sea}、最終フィルタで落とした {dropped}、merged_peak.csv に書いた行 {written}` |
| ML2 | 結果の要約（`--check-land-peaks`） | `結果の要約: 陸地最高峰リストの書式を確かめた（{land_count} 件）` |
| ML3 | 結果の要約（途中で止まった） | `結果の要約: 途中で止まった。merged_peak.csv は書き換えていない` |

#### 7.2.5 UT 候補

すべて自動（合否をテストのコードが判定できる）。止まるケースの期待の「メッセージ」は、標準エラー出力の 2 行（[7.2.4](#724-メッセージ文面)・[2.1.4](#214-メッセージ文面)・[2.2](#22-ログとメッセージの文面)の文面に値を入れたもの）。ログファイルの行の期待は、先頭の時刻と空白を除いた文面。共通の準備は次の 3 つ。

- **同じプロセス**: テストのプロセスの中で、ソースツリーの根の `scripts/` を import の探索先に入れて `import merge_peaks` し（`common`・`cmp5_common` も同じ探索先から読む）、関数を直接呼ぶ（`start_log` を呼ばない。`log_*` は画面にだけ出る）。止まるケースは `SystemExit` を捕まえて終了コードを読み、標準出力と標準エラー出力は `contextlib.redirect_stdout`・`redirect_stderr` で捕まえる。ファイルはケースごとに一時のディレクトリ `<tmp>` に書き、絶対パスを渡す。`merge_peaks._config_opt` は空の文字列にしておく（`main` を通らないため）。
- **子のプロセス**: 一時のソースツリー `<tmp>/src` を作り、`<tmp>/src/scripts/` にテストする `scripts/merge_peaks.py` と `scripts/common.py`・`scripts/cmp5_common.py` を写す。
  - `<tmp>/src/params/mesh_list_japan.txt` に `5237\n5238\n5239\n5337\n5338\n5339\n5437\n5438\n5439\n`、`<tmp>/src/params/land_highest_peaks.csv` に `name,peak_lat,peak_lon\n`（ケースが書けばその中身）を書く。
  - 一時の設定 `<tmp>/c.ini` に `[paths]` の `data_dir = <tmp>/data`・`log_dir = <tmp>/logs` を書く（ケースが書けば `[analysis]`・`[merge]` も）。
  - `<tmp>/data/boundaries/nt_excluded_meshes.txt` に `5438\n`、`<tmp>/data/results/csv/` にケースの per-mesh CSV を置き、`<tmp>/work` を作る。
  - 起動は `subprocess.run([sys.executable, '<tmp>/src/scripts/merge_peaks.py', '--config', '<tmp>/c.ini', *<引数>], cwd='<tmp>/work', capture_output=True)`。
  - 終了コード、標準出力と標準エラー出力（UTF-8）、`<tmp>/logs` の下のログファイル、`<tmp>/data/results/merged_peak.csv` のバイト列を確かめる。
- **per-mesh CSV の行**（`3-5338.csv` などに書く。見出しは `peak_lat,peak_lon,peak_elev,col_lat,col_lon,col_elev,prominence,key_col_resolved,col_margin_px,analysis_id`。システムテスト仕様書（ST）の `ST-FR-008-13`〜`22` の共通の前提の点。どれも 1 次メッシュ 5338）:
  - 行 U（未確定。画素 (7426886, 3312429)）: `35.36058364,138.72739077,1500.00,0.00000000,0.00000000,,,false,1,3-5338`
  - 行 L（陸のコルで確定。画素 (7426896, 3312429)）: `35.36058364,138.72781992,1600.00,35.34308245,138.74884844,1000.00,600.00,true,20,3-5338`
  - 行 S（海面確定。画素 (7427886, 3312429)）: `35.36058364,138.77030611,800.00,0.00000000,0.00000000,0.00,800.00,true,-1,3-5338`
  - 行 E2（未確定。画素 (7426888, 3312429)）: `35.36058364,138.72747660,1490.00,0.00000000,0.00000000,,,false,1,3-5338`
  - 行 B10（陸のコルで確定。画素 (7426886, 3312439)）: `35.36023365,138.72739077,1800.00,35.34308245,138.74884844,1000.00,800.00,true,20,3-5338`
  - `analysis_id` を替える行は、最後の列だけをそのファイルの解析識別子にする。

| ID | 確かめること | 準備 | 入力 | 期待 |
|---|---|---|---|---|
| `UT-merge_peaks-01` | 緯度経度 → メッシュコード（2.4 の表 5） | 同じプロセス | `latlon_to_mesh` に 2.4 の表 5 の 12 行 | 各行のコードと等しい |
| `UT-merge_peaks-02` | メッシュコードの範囲の外 | 同じプロセス | `latlon_to_mesh` に (a) (−1.0, 139.0)、(b) (35.0, 99.5)、(c) (66.7, 139.0)、(d) (35.0, 200.0) | どれも `ValueError` |
| `UT-merge_peaks-03` | 引数の正しい形 | 同じプロセス。`<tmp>/m.txt` に `5338\n5339\n` | `_parse_args` に (a) `['--config', '/a.ini']`、(b) `['--mesh', '5338', '--config', '/a.ini']`、(c) `['--config', '/a.ini', '--mesh', '<tmp>/m.txt']`、(d) `['--check-land-peaks', '--config', '/a.ini']`、(e) `['--mesh', '--x', '--config', '/a.ini']`（値が `-` で始まる） | (a) `_Args('/a.ini', None, False)`、(b) `_Args('/a.ini', {'5338'}, False)`、(c) `_Args('/a.ini', {'5338', '5339'}, False)`、(d) `_Args('/a.ini', None, True)`。(e) は `--x` を `--mesh` の値として `read_mesh_arg` に渡し、`<作業ディレクトリ>/--x` が無いので終了コード 2 で A2（名前として読まない） |
| `UT-merge_peaks-04` | 引数の誤り | 同じプロセス | `_parse_args` に (a) `[]`、(b) `['--config']`、(c) `['--config', 'a.ini']`、(d) `['--config', '/a', '--config', '/b']`、(e) `['--config', '/a', '--help']`、(f) `['--config=/a']`、(g) `['--config', '/a', '--check-land-peaks=x']`、(h) `['--config', '/a', '--check-land-peaks', '--mesh', '5338']`、(i) `['--config', '/a', '--mesh', '']`、(j) `['--config', '/a', 'x']`、(k) `['--check-land-peaks', '--check-land-peaks', '--config', '/a']`、(l) `['--config', '']` | どれも終了コード 2。メッセージは (a) MA4、(b) MA2（`{option}` は `--config`）、(c) MA5（`{value}` は `a.ini`）、(d) MA3（`--config`）、(e) MA1（`{arg}` は `--help`）、(f) MA1（`--config=/a`）、(g) MA1（`--check-land-peaks=x`）、(h) MA6、(i) A1、(j) MA1（`x`）、(k) MA3（`--check-land-peaks`）、(l) MA5（`{value}` は `''`） |
| `UT-merge_peaks-05` | 相互制約 | 同じプロセス。`common.load_config(<設定>, _CONFIG_KEYS_USED, ('data_dir',))` で読んだ設定（どれも `[paths]` に `data_dir = <tmp>/data`。(a) `[analysis]` に `prominence_primary_m = 150`、(b) `149`、(c) 書かない） | `_check_cross` | (a) 終了コード 2 で CX1（`{primary}` 150・`ファイル`、`{final}` 150・`デフォルト`、`{config_path}` は設定ファイルの絶対パス）。(b)(c) は戻る |
| `UT-merge_peaks-06` | 陸地最高峰リストを読む | 同じプロセス。(a) 先頭に BOM（`EF BB BF`）と `name,peak_lat,peak_lon\n\n試験峰,35.36058364,138.72739077\n\n試験峰2,35.36023365,138.72739077\n`、(b) `name,peak_lat,peak_lon\n`、(c) `\nname,peak_lat,peak_lon\n試験峰,35.36058364,138.72739077`（最後の改行なし） | `read_land_peaks` | (a) `[LandPeak('試験峰', '35.36058364', '138.72739077', 3, <path>), LandPeak('試験峰2', '35.36023365', '138.72739077', 5, <path>)]`、(b) `[]`、(c) `[LandPeak('試験峰', '35.36058364', '138.72739077', 3, <path>)]`（`<path>` は渡したファイルの絶対パス） |
| `UT-merge_peaks-07` | 陸地最高峰リストの誤り | 同じプロセス。(f)〜(l) のファイルは、先頭に見出しの行 `name,peak_lat,peak_lon` を置き、その後に示した行を置く。(a) 無いパス、(b) 一時のディレクトリ、(c) `FF FE` だけ、(d) 0 バイト、(e) `name,lat,lon\n`、(f) 見出しの後に `試験峰,35.36058364\n`、(g) `,35.36058364,138.72739077\n`、(h) `試験峰,NaN,138.72739077\n`、(i) `試験峰,35.36058364,180.00000000\n`、(j) `試験峰, 35.36058364,138.72739077\n`、(k) `"試験峰,35.36058364,138.72739077\n`（引用符を閉じずに終わる）、(l) `試験峰,35.36058364,138.72739077,x\n`、(m) `\n\n`（空行だけ） | `read_land_peaks` | どれも終了コード 1。(a) LP1、(b) LP2（`{reason}` は `IsADirectoryError` の `strerror`）、(c) LP2（`UTF-8 として読めない`）、(d)(m) LP3（`見出しの行が無い`）、(e) LP3（`見出しの行が name,peak_lat,peak_lon でない: name,lat,lon`）、(f) `2 行目の列の数が 2 で 3 でない`、(g) `2 行目の name が空`、(h) `2 行目の peak_lat が 座標として読めない: NaN`、(i) `2 行目の peak_lon が 座標として読めない: 180.00000000`、(j) `2 行目の peak_lat が 座標として読めない:  35.36058364`（`:` の後に空白 2 つ）、(k) `2 行目を CSV として読めない: unexpected end of data`、(l) `2 行目の列の数が 4 で 3 でない` |
| `UT-merge_peaks-08` | 解析の対象のメッシュ | 同じプロセス。日本全土のリスト `5337\n5338\n5339\n5438\n`、除外のリスト (a) `5438\n`、(b) 無いパス、(c) `54x8\n` | `read_target_meshes` | (a) `{'5337', '5338', '5339'}`。(b) 終了コード 1 で R1（`対処:` の行は 7.2.4 の R1〜R3 の案内で、`{config_opt}` は空）。(c) 終了コード 1 で R3 |
| `UT-merge_peaks-09` | 読むファイルを選ぶ | 同じプロセス。`<tmp>/csv/` に、見出しだけの `3-5338.csv`・`3-5339.csv`・`4-5338-NW.csv`・`5338.csv`・`3-5338-old.csv`・`7-5338-NW.csv`・`3-5338.CSV`、中身が `x` の `3-5338.meshset`・`3-5338.geojson`・`3-5340.csv.tmp` | `select_peak_csv_files` に (a) `mesh_codes=None`、(b) `{'5338', '5340'}`、(c) 無いディレクトリ `<tmp>/none` と `None`、(d) ファイル `<tmp>/csv/5338.csv` と `None` | (a) `files` は `3-5338.csv`・`3-5339.csv`・`4-5338-NW.csv` の順（`analysis_id` は名前から `.csv` を除いたもの、`is_normal` は真・真・偽）、`skipped` は `3-5338-old.csv`・`5338.csv`・`7-5338-NW.csv` の絶対パスの順、`missing` は空。(b) `files` は `3-5338.csv` だけ、`skipped` は (a) と同じ、`missing` は `['5340']`。(c) 3 つとも空のリスト。(d) 終了コード 1 で PM2（`{path}` は `<tmp>/csv/5338.csv`、`{reason}` は `NotADirectoryError` の `strerror`） |
| `UT-merge_peaks-10` | per-mesh CSV を読む | 同じプロセス。`3-5338.csv` に見出しと行 U・L・S。`4-5338-NW.csv` に見出しだけ | `read_peak_rows` を最後まで回す（`3-5338.csv` は `('3-5338', True)`、`4-5338-NW.csv` は `('4-5338-NW', False)`） | `3-5338.csv` は 3 つの `PeakRow`。行 U は `PeakRow('35.36058364', '138.72739077', '1500.00', '0.00000000', '0.00000000', '', '', False, '1', '3-5338', (7426886, 3312429), True)`、行 L・S も同じく字句のままで、画素は (7426896, 3312429)・(7427886, 3312429)、`key_col_resolved` は真。`4-5338-NW.csv` は何も渡さない |
| `UT-merge_peaks-11` | 値の誤り | 同じプロセス。`3-5338.csv` に見出しと、次の 1 行だけ: (a) 行 U の `col_elev` を `1000.00`、(b) 行 U の `prominence` を `500.00`、(c) 行 U の `col_lat` を `35.34308245`、(d) 行 U の `col_lon` を `138.74884844`、(e) 行 L の `analysis_id` を `3-5339`、(f) 行 L の `peak_elev` を `NaN`、(g) 行 L の `prominence` を `Infinity`、(h) 行 L の `peak_lat` を `85.10000000`、(i) 行 L の `key_col_resolved` を `True`、(j) 行 L の `col_margin_px` を `20.0`、(k) 行 L の `col_elev` を `''`、(l) 行 L の `col_lat` を `x` で同時に `key_col_resolved` を `yes`、(m) 行 U の `col_lat` を `1`（数として 0 でない）で同時に `col_lon` を `x`（有限の 10 進の数でない） | `read_peak_rows(path, '3-5338', True)` を回す | どれも終了コード 1 で PM3。`{detail}` は (a) `2 行目の col_elev が 空欄でない: 1000.00`、(b) `2 行目の prominence が 空欄でない: 500.00`、(c) `2 行目の col_lat が 数として 0 でない: 35.34308245`、(d) `2 行目の col_lon が 数として 0 でない: 138.74884844`、(e) `2 行目の analysis_id が ファイル名と違う: 3-5339`、(f) `2 行目の peak_elev が 有限の 10 進の数でない: NaN`、(g) `2 行目の prominence が 有限の 10 進の数でない: Infinity`、(h) `2 行目の peak_lat が 座標として読めない: 85.10000000`、(i) `2 行目の key_col_resolved が true か false でない: True`、(j) `2 行目の col_margin_px が 整数でない: 20.0`、(k) `2 行目の col_elev が 有限の 10 進の数でない:` と空白 1 つ（値が空なので、文は `:` と空白 1 つで終わる）、(l) `2 行目の key_col_resolved が true か false でない: yes`、(m) `2 行目の col_lat が 数として 0 でない: 1`（`col_lat` を終えてから `col_lon` へ進むので、`col_lon` の誤りは出ない） |
| `UT-merge_peaks-12` | ファイルの形の誤り | 同じプロセス。(a) 0 バイト、(b) 見出しを `lat,lon,elev`、(c) 先頭に BOM を付けた見出しと行 U、(d) 見出しの後に 9 列の行（行 U の最後の列を除く）、(e) 見出しの後に空の行と行 U、(f) 見出しの後に、行 U の 1 つ目の値を `"35.36058364"x` にした行、(g) 一時のディレクトリ、(h) 無いパス、(i) `FF FE` だけ | `read_peak_rows(path, '3-5338', True)` を回す | どれも終了コード 1。(a) PM3 `見出しの行が無い`、(b) PM3 `見出しの行が 10 列の並びでない: lat,lon,elev`、(c) PM3 `見出しの行が 10 列の並びでない:` と空白 1 つの後に U+FEFF と 10 列の見出し、(d) PM3 `2 行目の列の数が 9 で、見出しの行の 10 と違う`、(e) PM3 `2 行目の列の数が 0 で、見出しの行の 10 と違う`、(f) PM3 `2 行目を CSV として読めない: ',' expected after '"'`、(g)(h) PM2（`strerror`）、(i) PM2（`UTF-8 として読めない`） |
| `UT-merge_peaks-13` | 1 つのファイルの同じ画素 | 同じプロセス。`3-5338.csv` に見出しと行 L と、行 L の `peak_lat`・`peak_lon` を `35.36058000`・`138.72781992` にした行（同じ画素 (7426896, 3312429)） | `read_peak_rows(path, '3-5338', True)` を回す | 2 行目の `PeakRow` を先に渡した後、終了コード 1 で PM3（`2 行目と 3 行目が同じ Z15 の画素 (7426896, 3312429) の行`） |
| `UT-merge_peaks-14` | 代表を選ぶ | 同じプロセス。同じ画素 `P = (7426886, 3312429)` の `PeakRow` を位置の引数で作る: u3（行 U、`3-5338`、通常）、u4（行 U の `analysis_id` を `3-5339`、通常）、w5（行 U の `analysis_id` を `4-5338-NW`、広域）、r_a（行 L の座標を行 U のものにし、`col_elev` `1000.0`、`3-5339`、通常）、r_b（同じく `col_elev` `1000.00`、`4-5338-NW`、広域）、r_c（同じく `col_elev` `1000.5`、`5-5338-SE`、広域）、r_d（同じく `col_elev` `1000.0`、`3-5338`、通常）、r_e（同じく `col_elev` `1000.0000000000000000000000001`、`3-5339`、通常）、r_f（同じく `col_elev` `1000.0000000000000000000000002`、`4-5338-NW`、広域） | `pick_representative` に、(a) u3・w5、(b) u4・u3・w5、(c) r_a・r_b、(d) r_a・r_d、(e) r_a・r_b・r_c、(f) u3・r_b、(g) r_e・r_f を、空の表に入力の順と、その逆の順で渡す | どちらの順でも、代表は (a) u3、(b) u3、(c) r_a（`col_elev` が同じ値で通常が先）、(d) r_d（`analysis_id` の昇順）、(e) r_c（`col_elev` が最も高い）、(f) r_b（`true` が先）、(g) r_f（29 桁目で高い。`copy_negate` の確かめ）。`normal_count` は (a) 1、(b) 2、(c) 1、(d) 2、(e) 1、(f) 1、(g) 1。`normal_unresolved` は (a)(b)(f) が真、(c)(d)(e)(g) が偽 |
| `UT-merge_peaks-15` | 3 つの列 | 同じプロセス。`targets` は `{'5237', '5238', '5239', '5337', '5338', '5339', '5437', '5439'}`（5338 の 3×3 から 5438 を除いた 8 つ）。表は、空の表に次の `PeakRow`（UT 14 の行を、`analysis_id` だけ替えて作ったもの）を順に `pick_representative` で渡して作る（`PeakEntry` を直接作らない）。8 つの解析識別子 `3-5237`・`3-5238`・`3-5239`・`3-5337`・`3-5338`・`3-5339`・`3-5437`・`3-5439` を「8 つの識別子」と呼ぶ。(a) u3 の `analysis_id` を 8 つの識別子にした 8 行（どれも未確定）、(b) u3 の 1 行、(c) r_d の `analysis_id` を 8 つの識別子にした 8 行（どれも `true`）、(d) w5 の 1 行、(e) r_b の 1 行、(f) r_d の `analysis_id` を 8 つの識別子の前の 7 つにした 7 行と、u3 の `analysis_id` を `3-5439` にした 1 行 | `derive_stability` | (a) `analysis_count` `8`、`expected_count` `8`、`stability` `unstable`（未確定がある）。(b) `1`・`8`・`unstable`。(c) `8`・`8`・`confirmed`。(d) `0`・`''`・`unstable`。(e) `0`・`''`・`-`。(f) `8`・`8`・`unstable`（数は合うが未確定がある） |
| `UT-merge_peaks-16` | 海面確定を当てる | 同じプロセス。表は UT 10 の行 U・L・S と行 B10 の 4 つを `pick_representative` に渡し、`derive_stability` を当てたもの（`targets` は UT 15）。リストは (a) 行 U と同じ座標の 1 行、(b) 行 S と同じ座標の 1 行、(c) 行 L と同じ座標の 1 行、(d) `試験峰,35.36085344,138.72739077`（行 U から北へ 30.0004m）、(e) `試験峰,35.36085343,138.72739077`（行 U から北へ 29.9993m）、(f) (a) の行を 2 つ | `apply_land_peaks` | (a)(e)(f) 行 U の代表が `key_col_resolved` 真、`col_elev` `0.00`、`prominence` `1500.00`、`col_lat`・`col_lon` `0.00000000`、`col_margin_px` `-1` になり、`peak_lat`・`peak_lon`・`peak_elev`・`analysis_id`・`analysis_count`・`expected_count`・`stability`（`1`・`8`・`unstable`）は変わらず、`sea_fixed` が真。警告は空。(b) 何も変えず、警告は空。(c) 何も変えず、LW2 が 1 つ（`ピーク 35.36058364,138.72781992、コル 35.34308245,138.74884844 標高 1000.00`）。(d) 何も変えず、LW1 が 1 つ。どのケースも、当たらなかった値は変わらない |
| `UT-merge_peaks-17` | 30m ちょうど（「以下」） | 同じプロセス。UT 16 の表。`merge_peaks.cmp5_common.great_circle_m` を、(a) 常に `30.0` を返す関数、(b) 常に `math.nextafter(30.0, math.inf)` を返す関数に差し替える（ケースの後に元に戻す） | `apply_land_peaks` にリスト 1 行（行 U と同じ座標） | (a) 4 つの値すべてが当たるので、終了コード 1 で LP4。(b) どれにも当たらず、LW1 が 1 つで、表は変わらない（findsummits#202 の「4.8.5 の 7」の後半。前半の距離を求める処理は 7.1.5 の `UT-cmp5_common-06`） |
| `UT-merge_peaks-18` | 30m に 2 つ | 同じプロセス。表は行 U と行 E2 の 2 つ。リストは `<tmp>/land.csv` に見出しと `試験峰,35.36058364,138.72739077`（2 行目）を書き、`read_land_peaks` で読んだもの | `apply_land_peaks` | 終了コード 1 で LP4。1 行目は `陸地最高峰リストの行の 30m 以内にピークが 2 つ以上ある: <tmp>/land.csv の 2 行目 試験峰（35.36058364,138.72739077）: 35.36058364,138.72739077 標高 1500.00 距離 0.00m、35.36058364,138.72747660 標高 1490.00 距離 7.78m` |
| `UT-merge_peaks-19` | 最終フィルタ | 同じプロセス。表は次の 6 つ（どれも別の画素）: k1（`true`、`prominence` `150.00`、通常）、k2（`true`、`149.99`、通常）、k3（`true`、`140.00`、`4-5338-NW`）、k4（`false`、通常）、k5（`false`、広域）、k6（`true`、`150`、`5-5338-SE`） | `filter_by_prominence(table, 150)` | 残るのは k1・k4・k5・k6（元の順）、落とした数は 2、広域の一覧は k3 だけ。`table` は 6 つのまま |
| `UT-merge_peaks-20` | 書き出し | 同じプロセス。表は行 L・行 B10・行 S の代表をこの順に入れ、どれも `analysis_count` `1`、`expected_count` `8`、`stability` `confirmed` にしたもの。(a) `<tmp>/results/` を作り、前回の `merged_peak.csv`（中身 `old`）と前の起動の残りの `merged_peak.csv.tmp`（中身 `x`）を置く。(b) 空の表 | `write_merged_peak(table, <tmp>/results/merged_peak.csv)` | (a) 戻り値 3。バイト列は 13 列の見出しの行、行 L、行 S、行 B10 の順（gy の昇順、同じ gy は gx の昇順。どの行も 10 列の字句に `,1,8,confirmed` を足し、行末は LF）。`merged_peak.csv.tmp` は残らない。(b) 戻り値 0、見出しの行だけ |
| `UT-merge_peaks-21` | 書けない | 同じプロセス。(a) `<tmp>/results/` を作らない、(b) `<tmp>/results/merged_peak.csv` をディレクトリにする | `write_merged_peak` に UT 20 の表 | どちらも終了コード 1 で MF1（`{path}` は `<tmp>/results/merged_peak.csv`、`{dir}` は `<tmp>/results`）。(b) は `merged_peak.csv.tmp` が残らない |
| `UT-merge_peaks-22` | 統合の全体 | 子のプロセス。陸地最高峰リストに `試験峰,35.36058364,138.72739077`（行 U）・`試験島,35.36058364,138.81322145`（行 Q）・`遠い峰,35.0,135.0` の 3 行（2〜4 行目）。`results/csv/` に、`3-5338.csv`（見出しと行 U・行 L・行 S・行 Q。行 Q は未確定で `35.36058364,138.81322145,120.00,0.00000000,0.00000000,,,false,1,3-5338`、画素 (7428886, 3312429)）、`4-5338-NW.csv`（見出しと、行 B10 の `prominence` を `140.00`、`analysis_id` を `4-5338-NW` にした行。画素は (7426886, 3312439) で、行 U から 38.9m なので試験峰に当たらない）、`5338.csv`（中身 `x`） | 引数なし（`--config` だけ） | 終了コード 0。標準エラー出力は PW1（`<tmp>/data/results/csv/5338.csv`）、LW1（遠い峰。`{path}` は `<tmp>/src/params/land_highest_peaks.csv`、4 行目）、FW1（`35.36023365,138.72739077 ピーク標高 1800.00 コル標高 1000.00 プロミネンス 140.00 4-5338-NW`）の各 2 行がこの順。`merged_peak.csv` は見出しの行、行 U を海面確定にしたもの（`35.36058364,138.72739077,1500.00,0.00000000,0.00000000,0.00,1500.00,true,-1,3-5338,1,8,unstable`）、行 L（`…,3-5338,1,8,unstable`）、行 S（`…,3-5338,1,8,unstable`）の順（通常の per-mesh CSV が 1 つなので、`analysis_count` 1 が `expected_count` 8 と違い、どれも `unstable`）。ログファイルの最後から 2 行目が ML1（`読んだ per-mesh CSV 1 件（通常）・1 件（広域）、行 5、ピーク 5、海面確定 2、最終フィルタで落とした 2、merged_peak.csv に書いた行 3`）。行 Q は海面確定で `prominence` が `120.00` になってから最終フィルタで落ち（海面確定を最終フィルタの前に当てる。HLD の DEC82。順を逆にすると未確定のまま残る）、通常の行なので FW1 に出ない、最後が L3 で終了コード 0 |
| `UT-merge_peaks-23` | 陸地最高峰リストだけを確かめる | 子のプロセス。`results/csv/3-5338.csv` の見出しを `lat,lon,elev` にする（読めば止まる）。陸地最高峰リストを (a) 見出しの行と、UT 22 の 3 行のうち最初の 2 行（`試験峰`・`試験島`）、(b) 見出しだけ、(c) `name,lat,lon\n` | `--check-land-peaks` | (a) 終了コード 0、ML2（`2 件`）。(b) 終了コード 0、ML2（`0 件`）。(c) 終了コード 1、LP3 と ML3。どれも `merged_peak.csv` を書かず、PM3 を出さない |
| `UT-merge_peaks-24` | `start_log` の前の誤り | 子のプロセス。(a) `[analysis]` に `prominence_primary_m = 150` を書いた設定、(b) `--config` の値を `c.ini`（相対パス）にする（`--config` を共通の準備の値でなく、この値で渡す） | (a) 引数なし、(b) なし | (a) 終了コード 2 で CX1、(b) 終了コード 2 で MA5。どちらも `<tmp>/logs` を作らない |
| `UT-merge_peaks-25` | `start_log` の後の誤り | 子のプロセス。`<tmp>/data/results/merged_peak.csv` に `old` を置く。(a) `results/csv/` を空にする、(b) `3-5338.csv` を見出しと UT 11 の (e) の行にする、(c) 共通の準備のうち `<tmp>/data/boundaries/nt_excluded_meshes.txt` だけを作らない | 引数なし | どれも終了コード 1。(a) PM1（`{path}` は `<tmp>/data/results/csv`）、(b) PM3、(c) R1。どれもログファイルに同じ 2 行と ML3 があり、`merged_peak.csv` は `old` のまま |
| `UT-merge_peaks-26` | `--mesh` の範囲 | 子のプロセス。`results/csv/` に `3-5338.csv`（見出しと行 L）と `4-5338-NW.csv`（見出しと行 B10 の `analysis_id` を `4-5338-NW` にした行） | `--mesh 5338`、続けて別の回に `--mesh <tmp>/m.txt`（中身 `5338\n5339\n`） | 1 回目は終了コード 0、`merged_peak.csv` は見出しと行 L（`…,1,8,unstable`）だけ（広域を読まない）、警告なし。2 回目は終了コード 0、PW2（`5339`）が 1 つで、`merged_peak.csv` は 1 回目と同じバイト列 |
| `UT-merge_peaks-27` | 行が 0 件の統合 | 子のプロセス。`results/csv/` に `3-5338.csv`（見出しだけ）。陸地最高峰リストは見出しだけ | 引数なし | 終了コード 0、警告なし。`merged_peak.csv` は 13 列の見出しの行だけ（`peak_lat,peak_lon,peak_elev,col_lat,col_lon,col_elev,prominence,key_col_resolved,col_margin_px,analysis_id,analysis_count,expected_count,stability` と LF）。ログファイルの最後から 2 行目が ML1（`読んだ per-mesh CSV 1 件（通常）・0 件（広域）、行 0、ピーク 0、海面確定 0、最終フィルタで落とした 0、merged_peak.csv に書いた行 0`）。入力のファイルが 0 件の UT 25 (a)（PM1）と区別する |

- 画素・中心の緯度経度・所属メッシュ・距離の期待値は、[2.4](#24-言語ごとに別に実装する式のテストベクトル)の計算の決まりと [7.1.3](#713-関数の細部)の式のとおりに、2026-10-31 に CPython 3.14.8 で求めた（行 U と同じ点の画素は (7426886, 3312429)・中心 35.36058364,138.72739077 で所属メッシュ 5338、行 U と行 E2 の距離は 7.783278284108812m、`35.36085343` と `35.36085344` から行 U までの距離は 29.99932069573718m と 30.00043264665708m、`35.36058000,138.72781992` は行 L と同じ画素 (7426896, 3312429)）。
- UT 12 (f) と UT 07 (k) の `csv.Error` の文は CPython 3.14.8 のもの（[7.1.5](#715-ut-候補)の UT 14 (d) と同じ文の見込み）。
- UT 22 の行の数え方: 読んだ行は 5（`3-5338.csv` の 4 行と `4-5338-NW.csv` の 1 行）、ピークは 5（画素がどれも違う）、海面確定は行 U と行 Q の 2、最終フィルタで落とすのは行 Q と広域の行（`prominence` 140.00）の 2 で、書くのは 3 行。行 Q と行 S の距離は約 3.9km、行 Q とほかの行も 30m より遠い。行 U の `stability` は代表採用の時点の `unstable`（通常の行に未確定がある）のまま。
- UT 15 の `targets` の数は、5338 の 3×3 の 9 つから 5438 を除いた 8 つ（子のプロセスの共通の準備の日本全土のリストと除外のリストから求まる集合と同じ）。

### 7.3 `merge_zones`

- **ID**: LLD-merge_zones
- **対応 HLD**: [3.5](30_HLD.md#35-cmp5-統合突合)・[4.18](30_HLD.md#418-fr-018-per-mesh-ピーク候補-geojson-統合)・[5.2](30_HLD.md#52-nfr-002-メモリ使用量)・[5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)・[5.9](30_HLD.md#59-nfr-009-観測可能性中間成果物の可視化)
- **ファイル**: `scripts/merge_zones.py`

関数の名前と役割と呼ぶ順は [HLD 3.5.3](30_HLD.md#353-関数) の `merge_zones` の関数の表のとおりで、処理の正本は [HLD 4.18.2](30_HLD.md#4182-処理の流れ)・[4.18.3](30_HLD.md#4183-異常系) である。この節は、それを Python で書くための細部（引数の読み方、型、止まり方、JSON の書き方、メッセージの文面、UT 候補）だけを足す。`merge_zones` は CMP3（パイプライン制御）が起動する内部の起動口で、`--config <絶対パス>` を必ず受け取る（[HLD 2.4.5](30_HLD.md#245-内部引数)）。

- [5.2](30_HLD.md#52-nfr-002-メモリ使用量)（メモリ）は、`read_merged_peak` が 1 行ずつ渡すこと、`read_zone_features` が 1 回に 1 つのファイルだけを読み、その並びを `pick_zones` の後に `del` で手放すこと、候補の表がピークと種類ごとに 1 つだけを持つことで受ける（[HLD 4.18.2](30_HLD.md#4182-処理の流れ)の「メモリ」）。書き出しでは、`write_merged_peak_geojson` が全部の行の文字列を一時ファイルを開く前に組み立て終える（`TypeError` で止まるときに一時ファイルも前の出力も触らないため。7.3.3）ので、書き出す間は候補のゾーンに加えて出力の全文を持つ（HLD の「メモリ」の列挙にはこの分が無い）。メモリのピークは、実装の後に HLD 5.2.2 の「実測の計画」の 3「CMP5 の統合」で、書き出しの段を含めて測る。
- [5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)（再現性）は、ゾーンの選び方が全順序であること（`_zone_rank`）、Feature の順が `merged_peak.csv` の行の順であること、ゾーンの数を読んだ字句のまま書き、文字列と空白の書き方を 1 つに決めたこと（`_encode`）で受ける（HLD 5.3.2 の「同じ GeoJSON になる」の行）。
- [5.9](30_HLD.md#59-nfr-009-観測可能性中間成果物の可視化)（観測可能性）は、統合のたびに `merged_peak.geojson` を書き直すことと、未確定のピークの点の色（HLD の [DEC77](30_HLD.md#4184-設計判断)「コル未確定のピークの点は色を変える」）で受ける。消す時機は CMP3 にある（[HLD 2.10.3](30_HLD.md#2103-フェーズのやり直し)）。
- 結合のつなぎ目は、`CMP5-INT1`（`merge_peaks` → `merge_zones`。[7.1](#71-cmp5_common) の `read_merged_peak` が 6 列を読む）、`CMP5-EXT2`（CMP4（地形解析エンジン） → `merge_zones`。[6.8](#68-analyze_terrain_zone) が書く GeoJSON を `read_zone_features` が読み、`write_merged_peak_geojson` が数の字句を変えずに写す）、`CMP5-INT3`（`merge_zones` → `match_summits`。`merged_peak.geojson` を 7.1 の `read_zone_features` が読む）、`CMP5-EXT6`（引数と終了コード）、`CMP3-EXT3`（CMP3 の起動前提条件の検査が `merged_peak.geojson` の有無を見る）である（[HLD 3.5.5](30_HLD.md#355-結合のつなぎ目)・[3.3.5](30_HLD.md#335-結合のつなぎ目)）。IT のケースは `60_IT.md` の `IT-CMP5-INT1-01`・`02`、`IT-CMP5-EXT2-01`・`02`、`IT-CMP5-INT3-01`〜`03` ほか。

#### 7.3.1 ファイル割付

- 関数はすべて `scripts/merge_zones.py` 1 本に置く（ADR-LLD-001 の Decision 5）。`venv/bin/python3 scripts/merge_zones.py` で起動され（[HLD 3.5.1](30_HLD.md#351-プログラム)）、共通部品は `import common`、CMP5 の共通部品は `import cmp5_common` で読む（[2.1.1](#211-ファイル割付)・[7.1.1](#711-ファイル割付)と同じ）。7.1 の部品と型は `cmp5_common.read_zone_features(...)` のようにモジュールの属性として使う（[7.2.1](#721-ファイル割付)と同じ形にそろえる）。ほかに読むのは、標準の `decimal`・`json`・`os`・`re`・`shlex`・`sys` と、`dataclasses` の `dataclass`、`typing` の `Sequence` である。
- ファイルの先頭のコメントに `# trace: LLD-merge_zones` を書く。起動の部分は `if __name__ == '__main__': main()`。
- UT のコードは `tests/scripts/test_merge_zones.py` に置く。各テストに `# trace: UT-merge_zones-NN` のコメントを付ける。テストの枠組みは [2.1.1](#211-ファイル割付)と同じく標準の `unittest`。

#### 7.3.2 型とデータ

- 内部の定数（モジュールの最上位。名前は `_` で始める）:
  - `_CONFIG_KEYS_USED = ('data_dir', 'log_dir')`（[HLD 2.3.2](30_HLD.md#232-設定ファイル)の表で CMP5 の [FR-018](20_SRS.md#fr-018-per-mesh-ピーク候補-geojson-統合) が使うキー。`load_config` に渡す）。必須は `('data_dir',)`。
  - `_JSON_NUMBER_RE = re.compile(r'-?(0|[1-9][0-9]*)(\.[0-9]+)?')`（`fullmatch` で使う。RFC 8259 の数の字句のうち、指数の無い形。`merged_peak.csv` の座標を JSON に書けるかの確かめ。`_check_peak_lexemes`）。
  - `_STYLES: dict[str, tuple[tuple[str, object], ...]]`: `feature_type` から、[HLD 4.16.2](30_HLD.md#4162-処理の流れ)の表のスタイルの属性の (名前, 値) の組を表の順に並べたもの。値は、色と `CircleMarker` は `str`、数は `cmp5_common.JsonNumber`（表の字句どおり `JsonNumber('2')`・`JsonNumber('1')`・`JsonNumber('5')`・`JsonNumber('6')`）。キーは `peak_col_link`・`key_col`・`peak` の 3 つだけ（ゾーンのスタイルは per-mesh GeoJSON の `properties` のまま写すので持たない）。
  - `_UNRESOLVED_FILL = '#7b1fa2'`（HLD の [DEC77](30_HLD.md#4184-設計判断)「コル未確定のピークの点は色を変える」。`peak` の `_fillColor` だけを置き換える）。
  - 種類の並び `_ZONE_KINDS = (cmp5_common.ACTIVATION_ZONE, cmp5_common.DELETE_ZONE)`（欠けのメッセージと要約の種類の順。HLD 4.18.2 の 4 の「アクティベーションゾーンと delete判定ゾーン」の順）。
- 内部の状態（モジュールの最上位）: `_config_opt: str = ''`（`main` の 5 が入れる、[7.3.4](#734-メッセージ文面)の `{config_opt}` の値。`main` を通らない同じプロセスの UT は空のまま使う。[7.2.2](#722-型とデータ)と同じ）。
- `@dataclass(frozen=True) class _Args`（内部）: `config: str`（`--config` の値のまま）、`mesh_codes: set[str] | None`（`--mesh` を `common.read_mesh_arg` で読んだ集合。無ければ `None`）。
- `@dataclass(frozen=True) class ZoneFile`: `path: str`（絶対パス）、`analysis_id: str`（ファイル名から `.geojson` を除いたもの）。
- `@dataclass(frozen=True) class ZoneChoice`: `zone: cmp5_common.ZoneFeature`、`analysis_id: str`（そのゾーンを読んだファイルの解析識別子）。フィールドはこの順に並べる。
- ピークの表: `dict[tuple[int, int], cmp5_common.MergedPeakRow]`（`index_peaks_by_pixel` が返すもの。順は `merged_peak.csv` の行の順）。
- ゾーンの候補の表: `dict[tuple[tuple[int, int], str], ZoneChoice]`（鍵は (画素, 種類)。種類は `ACTIVATION_ZONE` か `DELETE_ZONE`）。
- Feature: `dict`（キーは `type`・`properties`・`geometry` の順。数は `JsonNumber`）。
- `slots=True` は付けない（[7.1](#71-cmp5_common)・[7.2](#72-merge_peaks)と同じく、メモリの実測〈HLD 5.2.2 の「実測の計画」の 3〉の後に決める）。

#### 7.3.3 関数の細部

関数ごとに `#####` の見出し（関数の名前だけ。ほかの節に同じ名前の見出しがあるものは `（merge_zones）` を添える）を立てて書く。内部の関数は、使う関数の見出しの下に書く。

**止まり方**: 7.3 の関数は、誤りを見つけたら、[7.3.4](#734-メッセージ文面)のメッセージを `common.log_error` で出してから `sys.exit(common.EXIT_ERROR)` で止まる（`start_log` の前の引数と設定の誤りは `common.EXIT_USAGE`）。7.1 の部品の `InputError` は、`main` が [7.1.3](#713-関数の細部)の前置きの型で捕まえ、`common.log_error(e.what, '対処の文')` の 2 行目に 7.3.4 の `{redo}` を入れて `sys.exit(common.EXIT_ERROR)` で止まる（[HLD 4.18.3](30_HLD.md#4183-異常系)の「どの場面でも案内はフェーズ2 から通しでやり直す」）。`InputError` を捕まえる `try` は、`read_merged_peak`・`index_peaks_by_pixel` を回すところと、`read_zone_features` を呼ぶところの 2 つだけにする（ほかの誤りを捕まえないため）。

**{reason}**: [2.1.4](#214-メッセージ文面)と同じ。`{path}` は `os.path.abspath` したパス。

**5.2・5.3・5.9 の受け方**: 7.3 の前置きに書いた。

##### main（merge_zones）

`main() -> None`（起動の部分）。[2.1.3](#213-関数の細部)の前置きの呼ぶ側の書き方の型に従い、次の順に行う。

1. `start = common.StartTime.now()`。
2. `args = _parse_args(sys.argv[1:])`。
3. `config = common.load_config(args.config, _CONFIG_KEYS_USED, ('data_dir',))`。`data_dir`・`log_dir` を取り出す。
4. `common.start_log(log_dir, config, 'merge_zones', sys.argv[1:], start)`。ロックは掛けない（内部の起動口は CMP3 のロックの下で動く。[HLD 2.9.3](30_HLD.md#293-同時起動の排他)）。
5. `_config_opt` に [7.3.4](#734-メッセージ文面)の `{config_opt}` の値を入れる。決め方は [7.2.3](#723-関数の細部)の `main` の 5 と同じ（`config.path == common.DEFAULT_CONFIG_PATH` なら空の文字列、それ以外は `' --config ' + shlex.quote(config.path)`）。
6. `try` の前に `completed = False`、`code = common.EXIT_OK`、要約の数（`files_read`・`peaks`・`az_false`・`dz_false` をどれも 0、`counts` を `feature_type` ごとの 0 の `dict`）を置く。`try` の中で次を行う。
   1. `csv_dir = os.path.join(data_dir, 'results', 'csv')`。`files = select_zone_geojson_files(csv_dir, args.mesh_codes)`。空なら ZG1 を出して `sys.exit(common.EXIT_ERROR)`。
   2. `merged_path = os.path.join(data_dir, 'results', 'merged_peak.csv')`。`try:` で `table = cmp5_common.index_peaks_by_pixel(cmp5_common.read_merged_peak(merged_path, cmp5_common.MERGED_PEAK_ZONE_COLUMNS))`、`except cmp5_common.InputError as e:` で `common.log_error(e.what, '対処の文')`（2 行目は `{redo}`）と `sys.exit(common.EXIT_ERROR)`。`peaks = len(table)`。
   3. `table` が空でなければ（`if`/`else` で分ける。`return` を使わない）:
      1. `_check_peak_lexemes(table)`。
      2. `candidates = {}`。`files` の順に、`try:` で `zones = cmp5_common.read_zone_features(f.path)`（`except cmp5_common.InputError` は 2 と同じ形で止まる）、`files_read` を 1 増やし、`pick_zones(table, candidates, zones, f.analysis_id)`、続けて `del zones`（次のファイルを読む間に前のファイルの並びを持たない。Python のループの変数は、次の `read_zone_features` の右辺を評価する間も前の値を指したままなので、名前を消して参照を手放す。HLD 4.18.2 の「メモリ」の「読んでいる 1 ファイルの中身」）。
      3. `check_zones_complete(table, candidates)`。
      4. `az_false`・`dz_false` は、`candidates` の値のうち、種類がそれぞれ `ACTIVATION_ZONE`・`DELETE_ZONE` で `zone.area_complete` が偽のものの数。
      5. `features = build_peak_features(table, candidates)`。
   4. `table` が空なら `features = []`（per-mesh ピーク候補 GeoJSON を読まない。HLD 4.18.2 の 2「`merged_peak.csv` を読む」。対象のファイルが 1 つ以上あることは 1 で確かめてあるので、ファイルが 1 つも無ければ、0 行でも 1 で止まる）。
   5. `counts` は、`features` の `properties` の `feature_type` ごとの数。`write_merged_peak_geojson(features, os.path.join(data_dir, 'results', 'merged_peak.geojson'))`。`completed = True`。
7. `finally` で結果の要約を `common.log_info` で出す（`completed` が真なら ZL1、偽なら ZL2）。
8. `sys.exit(code)`。

`start_log` の前に止まる誤り（`_parse_args`・`load_config`）は、標準エラー出力だけに出て、ログファイルと `log_dir` を作らない（[HLD 3.5.3](30_HLD.md#353-関数)の「ここまでの誤りは、ログファイルを作らずに終了コード 2」）。

##### _parse_args（merge_zones）

`_parse_args(argv: Sequence[str]) -> _Args`（内部）。[7.2.3](#723-関数の細部)の `_parse_args` から `--check-land-peaks` を除いた受け方（[6.1.3](#613-関数の細部)の `parse_args` と同じ）で、最初に見つけた誤り 1 つで、[7.3.4](#734-メッセージ文面)のメッセージを `common.log_error` で出して `sys.exit(common.EXIT_USAGE)`。

1. `argv` を左から読む。`--config`・`--mesh` なら、その名前がすでに出ていれば ZA3（値を見る前に判定する）、最後の引数なら ZA2、そうでなければ次の引数を値にして 2 つ進む（値は `-` で始まっていてもそのまま値にする）。ほかの引数（位置引数、知らない名前〈`--check-land-peaks` を含む〉、`=` の付いた形、`--help`、`--` だけ、空の引数）は ZA1。
2. `--config` が無ければ ZA4。
3. `--config` の値が `os.path.isabs` で偽なら（空を含む）ZA5。値は正規化しない。
4. `--mesh` があれば `common.read_mesh_arg(<値>)`（誤りは A1〜A5）。引数の形の誤りより後にする。
5. `_Args(config, mesh_codes)` を返す。

##### select_zone_geojson_files

`select_zone_geojson_files(csv_dir: str, mesh_codes: set[str] | None) -> list[ZoneFile]`

1. `abspath = os.path.abspath(csv_dir)`。`names = os.listdir(abspath)`。`FileNotFoundError` なら空のリストを返す（`main` が ZG1 で止まる）。ほかの `OSError`（ディレクトリでない、権限が無い）は ZG2（`{path}` は `abspath`）。
2. 名前を `sorted(names)` の順に見る。`.geojson` で終わらない名前（`.GEOJSON`・`.geojson.tmp` を含む）は見ない。`.geojson` で終わる名前は `stem, kind = cmp5_common.parse_analysis_id(name)`。`kind` が `ANALYSIS_NORMAL` で、`mesh_codes` が `None` か `stem[2:6]` が `mesh_codes` にあれば、`ZoneFile(os.path.join(abspath, name), stem)` を足す。ほか（広域の形、規則に合わない名前）は警告せずに読まない（HLD 4.18.2 の 1「読むファイルを選ぶ」の「`3-` で始まる名前のほかは対象にならない」。`merge_peaks` の PW1 に当たる警告は HLD 4.18 に無いので出さない。広域解析は GeoJSON を書かず、規則に合わない `.geojson` は `merge_peaks` が同じ名前の `.csv` で警告する）。ファイルの種類は見ない（ディレクトリなら `read_zone_features` が ZF2）。
3. 並びを返す（名前の昇順。通常の解析識別子は `3-` と 4 桁の数字なので、名前の昇順と解析識別子の昇順は同じ）。

##### _check_peak_lexemes

`_check_peak_lexemes(table: dict[tuple[int, int], cmp5_common.MergedPeakRow]) -> None`（内部。`main` の 6 の 3 の 1 が呼ぶ）。

表の順に、各行の `peak_lat`・`peak_lon` と、点と線を出す行（`key_col_resolved` が `true` で、`col_lat`・`col_lon` がどちらも数として 0 でない行。片方だけ 0 の行は出さない。`build_peak_features` の条件と同じ）の `col_lat`・`col_lon` を、この順に `_JSON_NUMBER_RE.fullmatch` で見る。最初に合わない値で ZN1 を出して `sys.exit(common.EXIT_ERROR)`。`{path}`・`{line_no}` は行の `path`・`line_no`、`{column}` は合わなかった列の名前（`peak_lat`・`peak_lon`・`col_lat`・`col_lon` のどれか）、`{value}` はその列の文字列（`merged_peak.csv` に書いてあった字句を `shlex.quote` で書く。[7.3.4](#734-メッセージ文面)の前置きの引用の決まりと同じ書き方）。数として 0 かの判定は `decimal.Decimal(v) == 0`（[7.1.3](#713-関数の細部)の前置きの「数として 0」。`read_merged_peak` が `true` の行の `col_lat`・`col_lon` を有限の 10 進の数と確かめてあるので失敗しない）。

- 理由: [HLD 4.18.2](30_HLD.md#4182-処理の流れ)の 5「書き出す」は点と線の座標と `peak_lat`・`peak_lon` に `merged_peak.csv` の文字列を数として書くことを求め、`read_merged_peak` の座標の確かめ（`is_valid_coord`）は `+35.1`・`035.1` のような JSON の数でない字句を通す。字句を直して書くと「文字列を数として書く」から外れ、そのまま書くと壊れた JSON になるので、ゾーンを読む前に止める。CMP4 が書く座標（[6.7](#67-analyze_terrain_csv)の `format_coord`）はこの形に合うので、止まるのは手で書き換えたファイルだけ。HLD 4.18.3 の書式の列挙に無い確かめを足すのは、7.1.3 の `read_zone_features` の形の確かめと同じく、壊れた出力を次のプログラムに運ばないため。

##### pick_zones

`pick_zones(peaks: dict[tuple[int, int], cmp5_common.MergedPeakRow], candidates: dict[tuple[tuple[int, int], str], ZoneChoice], zones: list[cmp5_common.ZoneFeature], analysis_id: str) -> dict[tuple[tuple[int, int], str], ZoneChoice]`

1. `zones` の順に、`z.pixel` が `peaks` に無ければ捨てる（ADR-SRS-024 の最終ピーク集合への絞り込み）。
2. あれば、`key = (z.pixel, z.kind)`、`new = ZoneChoice(z, analysis_id)`、`rep_id = peaks[z.pixel].values['analysis_id']`。`key` が `candidates` に無いか、`_zone_rank(new, rep_id) < _zone_rank(candidates[key], rep_id)` なら `candidates[key] = new`。
3. `candidates` を返す（同じオブジェクト）。

`_zone_rank(choice: ZoneChoice, rep_id: str) -> tuple[int, int, str]`（内部）: `(0 if choice.zone.area_complete else 1, 0 if choice.analysis_id == rep_id else 1, choice.analysis_id)`（HLD の [DEC75](30_HLD.md#4184-設計判断)「同じピークのゾーンは代表行の窓のものを優先して採る」。1 つのファイルに同じ (画素, 種類) のゾーンは 2 つ無い〈7.1.3 の ZF4〉ので、鍵はどの 2 つの候補でも違い、ファイルを渡す順によらず同じものが残る。[HLD 5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)）。

##### check_zones_complete

`check_zones_complete(peaks, candidates) -> None`（型は `pick_zones` と同じ）

表の順に、各ピークについて `_ZONE_KINDS` の順に `(pixel, kind)` が `candidates` に無い種類を集める。1 つ以上のピークに欠けがあれば、欠けたピークのすべてを ZM1 で出して `sys.exit(common.EXIT_ERROR)`（最初の 1 つで止めない。HLD の [DEC78](30_HLD.md#4184-設計判断)「ゾーンの欠けたピークがあれば止める」と 4.18.3）。

##### build_peak_features

`build_peak_features(peaks, candidates) -> list[dict]`（型は `pick_zones` と同じ）

[HLD 4.18.2](30_HLD.md#4182-処理の流れ)の 5「書き出す」の順に並べる。同じ種類の中は `peaks` の順（`merged_peak.csv` の行の順）。`r = row.values` とする。

- delete判定ゾーン（1 番目）とアクティベーションゾーン（2 番目）: 各ピークの候補の `zone` から `{'type': 'Feature', 'properties': zone.properties, 'geometry': zone.geometry}`（7.1 の `ZoneFeature` が持つ `properties` と `geometry` をそのまま使う。読んだ Feature のほかのメンバー〈`id`・`bbox` など〉は書かない。HLD 4.18.2 の 5 の「ジオメトリと `properties` ごと、そのまま写す」）。
- 接続線（3 番目）とコル（4 番目）: `r['key_col_resolved'] == 'true'` で、`col_lat`・`col_lon` がどちらも数として 0 でない行だけ（片方だけ 0 の行は出さない。HLD 4.16.2 の 3・4、[6.8.3](#683-関数の細部)の `write_zone_geojson` の 2 と同じ条件）。
  - 接続線: `properties` は `peak_lat`・`peak_lon`（`JsonNumber(r['peak_lat'])` など）、`feature_type` `'peak_col_link'`、`_STYLES['peak_col_link']` の順。`geometry` は `{'type': 'LineString', 'coordinates': [[JsonNumber(peak_lon), JsonNumber(peak_lat)], [JsonNumber(col_lon), JsonNumber(col_lat)]]}`。
  - コル: `properties` はピークの `peak_lat`・`peak_lon`、`feature_type` `'key_col'`、`_STYLES['key_col']`。`geometry` は `{'type': 'Point', 'coordinates': [JsonNumber(col_lon), JsonNumber(col_lat)]}`。
- ピーク（5 番目）: すべての行。`properties` は `peak_lat`・`peak_lon`、`feature_type` `'peak'`、`_STYLES['peak']`（`r['key_col_resolved'] == 'false'` なら `_fillColor` の値だけを `_UNRESOLVED_FILL` にする）。`geometry` は `{'type': 'Point', 'coordinates': [JsonNumber(peak_lon), JsonNumber(peak_lat)]}`。

`peaks` が空なら空のリスト（`main` は空の表のとき呼ばないが、関数としては空を返す）。

##### write_merged_peak_geojson

`write_merged_peak_geojson(features: list[dict], out_path: str) -> None`

1. 中身（全部の行の文字列を、一時ファイルを開く前に組み立て終える。`_encode` の `TypeError` で止まるときに、一時ファイルも前の `merged_peak.geojson` も触らないため。[HLD 4.18.1](30_HLD.md#4181-目的と範囲)の対象外の行の「JSON の数と空白の書き方」。行の形は 6.8.3 の `write_zone_geojson` の「GeoJSON の書き方」と同じ）: 1 行目 `{"type":"FeatureCollection","features":[`、続けて Feature を 1 行に 1 つ（最後のほかは行末に `,`）、最後の行 `]}`。どの行も LF で終える。Feature が 0 なら 1 行目と最後の行の 2 行だけ。BOM・CR・`crs` を書かない。各 Feature は内部の関数 `_encode` で 1 行の文字列にする。
2. `_encode(value: object) -> str`（内部）: `dict` は `{` と、キーの順に `json.dumps(key)`・`:`・値の `_encode` を `,` でつないだものと `}`。`list` は `[`・要素の `_encode` を `,` でつないだもの・`]`。`cmp5_common.JsonNumber` は `text` をそのまま（HLD の [DEC76](30_HLD.md#4184-設計判断)「ピークは Z15 の画素で突き合わせ、ゾーンは写す」。`1E5`・`35.10`・`-0` も読んだ字句のまま）。`str` は `json.dumps(value)`（既定の `ensure_ascii=True` で、ASCII の外の字は `\uXXXX`〈16 進は小文字〉になり、出力はいつも ASCII だけになる）。`True`・`False`・`None` は `true`・`false`・`null`（`bool` は `int` より先に見る）。ほかの型（`int`・`float` を含む）は `TypeError`（プログラムの誤り。数はどれも `JsonNumber` で持つ）。空白を書かない。
3. [2.3](#23-ファイルの名前と書き方)の一時ファイルの決まりで `out_path + '.tmp'` に書いて（テキスト。`open(tmp, 'w', encoding='utf-8', newline='\n')`、`flush`、`os.fsync`、閉じる）、`os.replace(tmp, out_path)` で置き換える。書く段の `OSError` は 2.3 のとおり一時ファイルを消してから ZO1、置き換えの `OSError` も一時ファイルを `os.remove` で消して（消せないときは無視）から ZO1 で止まる。ZO1 の `{path}` はどの段でも `out_path` の絶対パス、`{dir}` は `os.path.dirname(os.path.abspath(out_path))`。ディレクトリ（`results/`）は作らない。止まったときは前の `merged_peak.geojson` を消さない（CMP3 が統合の前に消している。[HLD 2.10.3](30_HLD.md#2103-フェーズのやり直し)）。

#### 7.3.4 メッセージ文面

書き方は [2.2](#22-ログとメッセージの文面)。設定の誤り（CF1〜CF7）と `--mesh` の誤り（A1〜A5）は [2.1.4](#214-メッセージ文面)、ログの場面（G1〜G7）は 2.2、L1〜L3 は 2.2（`{program}` は `merge_zones`）。7.1 の部品の誤り（MP1〜MP3・ZF1〜ZF4）の 1 行目は [7.1.4](#714-メッセージ文面)の `what` のまま、2 行目は `{redo}`。

- `{path}`・`{reason}` は [7.3.3](#733-関数の細部)の前置きのとおり。
- `{arg}`・`{value}` は受け取った値を、2.2 の引用の決まり（`shlex.quote`）で書いたもの。ZN1 の `{value}` は引数でなく `merged_peak.csv` の字句だが、同じ `shlex.quote` で書く。
- `{config_opt}` は `main` の 5 で決めた値。
- `{redo}` は `scripts/run_pipeline.sh{config_opt} を --phase なしで起動して、フェーズ2 から通しでやり直す`（[7.2.4](#724-メッセージ文面)と同じ文。[HLD 4.18.3](30_HLD.md#4183-異常系)の「フェーズ2 から通しでやり直す」）。

| 記号 | 場面 | 1 行目（`ERROR:` と空白 1 つの後） | 2 行目（`対処:` と空白 1 つの後） | 終了コード |
|---|---|---|---|---|
| ZA1 | 受け付けない引数 | `merge_zones の知らない引数: {arg}` | `merge_zones は run_pipeline が起動する内部の起動口。使える名前は --config・--mesh（値は次の引数で渡す）` | 2 |
| ZA2 | 値が無い | `{option} の値が無い` | `{option} の後に値を渡す` | 2 |
| ZA3 | 同じ名前を 2 回 | `{option} を 2 回渡した` | `{option} は 1 回だけ渡す` | 2 |
| ZA4 | `--config` が無い | `--config が無い` | `--config と設定ファイルの絶対パスを渡す` | 2 |
| ZA5 | `--config` が絶対パスでない | `--config のパスが絶対パスでない: {value}` | `--config に設定ファイルの絶対パスを渡す` | 2 |
| ZG1 | 対象の per-mesh ピーク候補 GeoJSON が 1 つも無い | `統合する per-mesh ピーク候補 GeoJSON が 1 つも無い: {path}`（`{path}` は `results/csv/` の絶対パス） | `{redo}` | 1 |
| ZG2 | `results/csv/` を読めない | `per-mesh ピーク候補 GeoJSON の置き場を読めない: {path}: {reason}` | `{path} の権限を確かめてから、{redo}` | 1 |
| ZN1 | `merged_peak.csv` の座標が JSON の数の書き方でない | `merged_peak.csv の書式が違う: {path}: {line_no} 行目の {column} が JSON の数の書き方でない: {value}` | `{redo}` | 1 |
| ZM1 | ゾーンの欠けたピークがある | `ゾーンの欠けたピークがある: {list}`（`{list}` は欠けたピークごとに `{peak_lat},{peak_lon} の {kinds}（代表行の analysis_id {analysis_id}）` を表の順に `、` でつないだもの。`{peak_lat}`・`{peak_lon}`・`{analysis_id}` は `merged_peak.csv` の字句、`{kinds}` は欠けた種類の `feature_type` の値を `_ZONE_KINDS` の順に `・` でつないだもの） | `{redo}` | 1 |
| ZO1 | `merged_peak.geojson` を書けない | `merged_peak.geojson を書けない: {path}: {reason}` | `{dir} の空きと権限を確かめてから、{redo}`（`{dir}` は `results/` の絶対パス。HLD 4.18.3 の「どの場面でも案内はフェーズ2 から通しでやり直す」は、同じ節の表の書き込みの失敗の行も含む。[6.8](#68-analyze_terrain_zone)の ZW1・7.2 の MF1 の `{rerun}` とは違う） | 1 |

通常のログ（[HLD 4.18.2](30_HLD.md#4182-処理の流れ)の 5「書き出す」と [HLD 5.7.2](30_HLD.md#572-処理の流れ)の表の `merge_zones` の行。2.2 の結果の要約の形）:

| 記号 | 行 | 文面 |
|---|---|---|
| ZL1 | 結果の要約 | `結果の要約: 読んだ per-mesh ピーク候補 GeoJSON {files_read} 件、ピーク {peaks}、area_complete=false のゾーンしか無かったピーク activation_zone {az_false}・delete_zone {dz_false}、merged_peak.geojson に書いたフィーチャ delete_zone {n_delete}・activation_zone {n_activation}・peak_col_link {n_link}・key_col {n_col}・peak {n_peak}` |
| ZL2 | 結果の要約（途中で止まった） | `結果の要約: 途中で止まった（読んだ per-mesh ピーク候補 GeoJSON {files_read} 件、ピーク {peaks}）。merged_peak.geojson は書き換えていない` |

- ZL1 の `area_complete=false のゾーンしか無かったピーク` は、採ったゾーンの `area_complete` が偽の数（`true` の候補があれば `true` を採るので、同じ数になる）。
- ZL2 の数は、止まった時点までのもの（HLD 5.7.2 の 7「結果の要約」の「そこまでに終えた分の件数」）。`{peaks}` は `index_peaks_by_pixel` を終える前に止まれば 0。

#### 7.3.5 UT 候補

すべて自動（合否をテストのコードが判定できる）。止まるケースの期待の「メッセージ」は、標準エラー出力の 2 行（[7.3.4](#734-メッセージ文面)・[7.1.4](#714-メッセージ文面)・[2.1.4](#214-メッセージ文面)・[2.2](#22-ログとメッセージの文面)の文面に値を入れたもの）。ログファイルの行の期待は、先頭の時刻と空白を除いた文面。共通の準備は次の 4 つ。

- **同じプロセス**: [7.2.5](#725-ut-候補)の同じ名前の準備と同じ（`merge_peaks` を `merge_zones` に読み替える）。`merge_zones._config_opt` は空の文字列にしておく。
- **子のプロセス**: 7.2.5 の同じ名前の準備から、`params/` の 2 つのファイルと `<tmp>/data/boundaries/` を除き、`<tmp>/src/scripts/` に写すものを `merge_zones.py`・`common.py`・`cmp5_common.py` にしたもの。`<tmp>/data/results/merged_peak.csv` と `<tmp>/data/results/csv/` の GeoJSON はケースが置く。1 つの UT に (a)(b)… の回が複数あるときは、回ごとに `<tmp>/data/results/` と `<tmp>/logs/` を空にしてから、その回の「準備」の列に書いたファイルだけを置く（前の回のファイルを残さない。残すと、前の回の GeoJSON が次の回のゾーンや `files_read` に入る）。起動は `subprocess.run([sys.executable, '<tmp>/src/scripts/merge_zones.py', '--config', '<tmp>/c.ini', *<引数>], cwd='<tmp>/work', capture_output=True)`。`<tmp>/c.ini` は既定のパスでないので、メッセージの `{config_opt}` は空白 1 つと `--config <tmp>/c.ini`（パスは `shlex.quote` した形）になる。
- **merged_peak.csv の行**（13 列。見出しは `cmp5_common.MERGED_PEAK_ALL_COLUMNS` を `,` でつないだもの。システムテスト仕様書（ST）の `ST-FR-018-06`〜`13` の共通の前提の点）:
  - 行 U（G0 の未確定。画素 (7426886, 3312429)）: `35.36058364,138.72739077,1500.00,0.00000000,0.00000000,,,false,1,3-5338,1,9,unstable`
  - 行 S（E1000 の海面確定。画素 (7427886, 3312429)）: `35.36058364,138.77030611,800.00,0.00000000,0.00000000,0.00,800.00,true,-1,3-5338,1,9,unstable`
  - 行 L（E2000 の陸のコルで確定。画素 (7428886, 3312429)）: `35.36058364,138.81322145,1500.00,35.34308245,138.74884844,1000.00,500.00,true,20,3-5338,1,9,unstable`
  - 行 P（G0 の陸のコルで確定）: 行 L の座標を `35.36058364,138.72739077` にしたもの。`analysis_id` を替えるときは 10 列目だけを替える。
- **ゾーン**: per-mesh ピーク候補 GeoJSON のゾーンの Feature は、`{"type":"Feature","properties":{"peak_lat":<lat>,"peak_lon":<lon>,"feature_type":"<種類>","area_complete":<true|false>,<HLD 4.16.2 の表のその種類のスタイル>},"geometry":R(n)}` の形で書く（6.8.3 の書き方）。`R(n)` は `{"type":"Polygon","coordinates":[[[n,0],[n,1],[n,2],[n,0]]]}`（`n` は 1 から数える整数の字句。どのファイルのどの Feature かを見分けるため、ケースの中で `n` を重ねない）。同じプロセスのケースは、`cmp5_common.ZoneFeature(index, kind, pixel, area_complete, geometry, properties)` を直接作ってよい（`geometry` と `properties` は上の形を `JsonNumber` で持つ `dict`）。ピークの表は `cmp5_common.MergedPeakRow(<path>, <line_no>, <6 列の dict>)` を直接作るか、`<tmp>/merged_peak.csv` を書いて `index_peaks_by_pixel(read_merged_peak(...))` で作る。

| ID | 確かめること | 準備 | 入力 | 期待 |
|---|---|---|---|---|
| `UT-merge_zones-01` | 引数の正しい形 | 同じプロセス。`<tmp>/m.txt` に `5338\n5339\n` | `_parse_args` に (a) `['--config', '/a.ini']`、(b) `['--mesh', '5338', '--config', '/a.ini']`、(c) `['--config', '/a.ini', '--mesh', '<tmp>/m.txt']` | (a) `_Args('/a.ini', None)`、(b) `_Args('/a.ini', {'5338'})`、(c) `_Args('/a.ini', {'5338', '5339'})` |
| `UT-merge_zones-02` | 引数の誤り | 同じプロセス | `_parse_args` に (a) `[]`、(b) `['--config']`、(c) `['--config', 'a.ini']`、(d) `['--config', '/a', '--config', '/b']`、(e) `['--config', '/a', '--check-land-peaks']`、(f) `['--config=/a']`、(g) `['--config', '/a', '--mesh', '']`、(h) `['--config', '']`、(i) `['--mesh', '5338', '--mesh', '5339', '--config', '/a']`、(j) `['--mesh', '--x', '--config', '/a.ini']`（値が `-` で始まる） | どれも終了コード 2。(j) は `--x` を `--mesh` の値として `read_mesh_arg` に渡し、`<作業ディレクトリ>/--x` が無いので A2（名前として読まない。7.2.5 の UT 03 (e) と同じ）。(a) ZA4、(b) ZA2（`--config`）、(c) ZA5（`a.ini`）、(d) ZA3（`--config`）、(e) ZA1（`--check-land-peaks`）、(f) ZA1（`--config=/a`）、(g) A1、(h) ZA5（`''`）、(i) ZA3（`--mesh`） |
| `UT-merge_zones-03` | 読むファイルを選ぶ | 同じプロセス。`<tmp>/csv/` に、中身が `x` の `3-5338.geojson`・`3-5339.geojson`・`4-5338-NW.geojson`・`5338.geojson`・`3-5338-old.geojson`・`3-5338.GEOJSON`・`3-5338.csv`・`3-5340.geojson.tmp` | `select_zone_geojson_files` に (a) `None`、(b) `{'5338', '5340'}`、(c) 無いディレクトリ `<tmp>/none` と `None`、(d) ファイル `<tmp>/csv/3-5338.csv` と `None` | (a) `[ZoneFile(<tmp>/csv/3-5338.geojson, '3-5338'), ZoneFile(<tmp>/csv/3-5339.geojson, '3-5339')]`（パスは絶対パス）。警告は出ない。(b) `3-5338.geojson` だけ。(c) 空のリスト。(d) 終了コード 1 で ZG2（`{path}` は `<tmp>/csv/3-5338.csv`、`{reason}` は `NotADirectoryError` の `strerror`） |
| `UT-merge_zones-04` | 座標の字句 | 同じプロセス。ピークの表を、1 行ずつ次の値で作る（どれも `path` `<tmp>/merged_peak.csv`、`line_no` 2）: (a) 行 P、(b) 行 P の `peak_lat` を `+35.36058364`、(c) 行 P の `peak_lon` を `0138.72739077`、(d) 行 P の `col_lon` を `+138.74884844`、(e) 行 U の `col_lat` を `+0`（`false` の行）、(f) 行 S の `col_lat`・`col_lon` を `-0.0`・`+0.00000000`（`true` で両方 0）、(g) 行 P の `col_lat` を `0.0`（片方だけ 0） | `_check_peak_lexemes` | (a)(e)(f)(g) は戻る（(e)〜(g) はコルを書かない行）。(b)(c)(d) は終了コード 1 で ZN1（`{column}`・`{value}` は (b) `peak_lat`・`+35.36058364`、(c) `peak_lon`・`0138.72739077`、(d) `col_lon`・`+138.74884844`） |
| `UT-merge_zones-05` | ゾーンを選ぶ（優先の順） | 同じプロセス。ピークの表は行 P の 1 行で、`analysis_id` を (a)〜(d) `3-5339`、(e) `4-5338-NW` にしたもの。`3-5338`・`3-5339`・`3-5438` の 3 つのファイルのゾーンの並びを、P の両ゾーン（`area_complete` は下）で作る | `pick_zones` を、空の候補の表に 3 つのファイルを `3-5338`・`3-5339`・`3-5438` の順に渡し、別の回にその逆の順に渡す。`area_complete`（3 つのファイルの順）は (a) 両ゾーンとも true・true・true、(b) 両ゾーンとも true・false・true、(c) 両ゾーンとも false・false・false、(d) AZ は false・false・true、DZ は true・false・true、(e) 両ゾーンとも false・true・true | どちらの順でも、採る `analysis_id` は (a) 両方 `3-5339`、(b) 両方 `3-5338`、(c) 両方 `3-5339`、(d) AZ は `3-5438`、DZ は `3-5338`、(e) 両方 `3-5339`（`ST-FR-018-06`・`07` と同じ）。候補の `zone` は、採ったファイルの Feature と同じオブジェクト |
| `UT-merge_zones-06` | 表に無いピークのゾーン | 同じプロセス。ピークの表は行 P だけ。1 つのファイルのゾーンの並びに、P の AZ と、E10（画素 (7426896, 3312429)、`35.36058364,138.72781992`）の AZ・DZ | `pick_zones(table, {}, zones, '3-5338')` | 候補の表は `((7426886, 3312429), 'activation_zone')` の 1 つだけ |
| `UT-merge_zones-07` | 欠けを確かめる | 同じプロセス。ピークの表は、行 L の座標を G0（M1）・E1000（M2）・E2000（M3）にした 3 行（この順、どれも `3-5338`）。候補の表は M1 の AZ と M3 の両ゾーンだけ。(b) は M1・M2・M3 の両ゾーンがそろったもの | `check_zones_complete` | (a) 終了コード 1 で ZM1。1 行目は `ゾーンの欠けたピークがある: 35.36058364,138.72739077 の delete_zone（代表行の analysis_id 3-5338）、35.36058364,138.77030611 の activation_zone・delete_zone（代表行の analysis_id 3-5338）`、2 行目は `{redo}`（`{config_opt}` は空）。(b) 戻る |
| `UT-merge_zones-08` | 並べ方とスタイル | 同じプロセス。ピークの表は行 U・S・L の順。候補の表は 3 つのピークの両ゾーン（どれも `area_complete` 真。`R(1)`〜`R(6)`） | `build_peak_features` | 11 個。`feature_type` は `delete_zone`（U・S・L）、`activation_zone`（U・S・L）、`peak_col_link`（L）、`key_col`（L）、`peak`（U・S・L）の順（`ST-FR-018-09`）。ゾーンの `properties` と `geometry` は候補の `zone` のものと同じオブジェクト。`peak` の `_fillColor` は U が `#7b1fa2`、S・L が `#d32f2f` で、ほかのスタイルは 3 つとも HLD 4.16.2 の表のとおり。L の `peak_col_link` の `coordinates` の字句は `[['138.81322145', '35.36058364'], ['138.74884844', '35.34308245']]`（`JsonNumber` の `text`） |
| `UT-merge_zones-09` | 書き出しのバイト列 | 同じプロセス。`<tmp>/results/` を作り、前回の `merged_peak.geojson`（中身 `old`）と前の起動の残りの `merged_peak.geojson.tmp`（中身 `x`）を置く。Feature の並びは (a) 次の 2 つ: F1 = `{'type': 'Feature', 'properties': {'peak_lat': JsonNumber('35.10'), 's': 'é"', 'n': None, 'b': False, 'a': [JsonNumber('1E5'), JsonNumber('-0')]}, 'geometry': {'type': 'Point', 'coordinates': [JsonNumber('138.7274766'), JsonNumber('35.10')]}}`、F2 = F1 の `b` を `True` にしたもの。(b) 空の並び。(c) F1 の `peak_lat` を `1.5`（`float`） | `write_merged_peak_geojson(features, <tmp>/results/merged_peak.geojson)` | (a) バイト列は `{"type":"FeatureCollection","features":[\n{"type":"Feature","properties":{"peak_lat":35.10,"s":"\u00e9\"","n":null,"b":false,"a":[1E5,-0]},"geometry":{"type":"Point","coordinates":[138.7274766,35.10]}},\n` と同じ形の F2（`"b":true`、行末に `,` なし）と `\n]}\n`。`merged_peak.geojson.tmp` は残らない。(b) `{"type":"FeatureCollection","features":[\n]}\n`。(c) `TypeError` で、`merged_peak.geojson` は `old`、`merged_peak.geojson.tmp` は `x` のまま（一時ファイルを開く前に止まる） |
| `UT-merge_zones-10` | 書けない | 同じプロセス。(a) `<tmp>/results/` を作らない、(b) `<tmp>/results/merged_peak.geojson` をディレクトリにする | UT 09 の (a) の並び | どちらも終了コード 1 で ZO1（`{path}` は `<tmp>/results/merged_peak.geojson`、`{dir}` は `<tmp>/results`、`{reason}` は (a) `FileNotFoundError`、(b) `IsADirectoryError` の `strerror`）。(b) は `merged_peak.geojson.tmp` が残らない |
| `UT-merge_zones-11` | 統合の全体 | 子のプロセス。`merged_peak.csv` に見出しと行 U・S・L。`3-5338.geojson` に、DZ（L・U・S の順。`R(1)`〜`R(3)`）、AZ（L・U・S。アクティベーションゾーンの U だけ頂点の書き方を `[[[1.50,0],[1.50,1],[1.50,2],[1.50,0]]]` にする）、3 つのピークの `peak` の点、L の `key_col` の点と `peak_col_link` の線（どれも `area_complete` 真、6.8.3 の書き方）。`3-5339.geojson` に、L の両ゾーン（`area_complete` 偽）と、E10 の両ゾーン | 引数なし（`--config` だけ） | 終了コード 0。`merged_peak.geojson` は 13 行（1 行目、11 個の Feature、最後の行）。ゾーンの 6 行は `3-5338.geojson` の該当の Feature の行と同じ文字列（行末の `,` を除く。`1.50` も同じ字句）で、DZ・AZ とも U・S・L の順。接続線・コル・ピークの行は、`{"type":"Feature","properties":{"peak_lat":35.36058364,"peak_lon":138.81322145,"feature_type":"peak_col_link","_color":"#616161","_weight":2,"_opacity":1},"geometry":{"type":"LineString","coordinates":[[138.81322145,35.36058364],[138.74884844,35.34308245]]}}` の形（コル・ピークも HLD 4.16.2 の表の順のスタイル。U のピークの `_fillColor` は `#7b1fa2`）。ログファイルの最後から 2 行目が ZL1（`読んだ per-mesh ピーク候補 GeoJSON 2 件、ピーク 3、area_complete=false のゾーンしか無かったピーク activation_zone 0・delete_zone 0、merged_peak.geojson に書いたフィーチャ delete_zone 3・activation_zone 3・peak_col_link 1・key_col 1・peak 3`）、最後が L3 |
| `UT-merge_zones-12` | 0 行と対象なし | 子のプロセス。(a) `merged_peak.csv` は見出しだけ、`3-5338.geojson` の中身は `x`。(b) (a) の `merged_peak.csv` で、`results/csv/` は空 | 引数なし | (a) 終了コード 0。`merged_peak.geojson` は `{"type":"FeatureCollection","features":[\n]}\n`、ZL1 の数はどれも 0（`読んだ … 0 件`）（`ST-FR-018-11`）。(b) 終了コード 1 で ZG1（`{path}` は `<tmp>/data/results/csv`）と ZL2（`0 件、ピーク 0`）。`merged_peak.geojson` は書かれない |
| `UT-merge_zones-13` | `start_log` の後の誤り | 子のプロセス。どの回も `<tmp>/data/results/merged_peak.geojson` に `old` を置く。(a) `merged_peak.csv` を置かず、`3-5338.geojson` に行 P の両ゾーン。(b) `merged_peak.csv` に見出しと行 P、`3-5338.geojson` の中身は `x`、`3-5339.geojson` に P の両ゾーン（`ST-FR-018-13`）。(c) `merged_peak.csv` に見出しと M1・M2・M3（UT 07 の 3 行）、`3-5338.geojson` に M1 の AZ と M3 の両ゾーン（`ST-FR-018-10`）。(d) `merged_peak.csv` に見出しと、行 P の `peak_lat` を `+35.36058364` にした行、`3-5338.geojson` の中身は `x` | 引数なし | どれも終了コード 1 で、`merged_peak.geojson` は `old` のまま。ログファイルの終わりの 4 行は、(a)〜(d) のどれも、標準エラー出力と同じ 2 行（エラーの行と `{redo}` の行。(b)(c)(d) も (a) と同じく、標準エラー出力とログファイルの両方を比べる）、ZL2、L3 の順。(a) 1 行目は 7.1.4 の MP1（`{path}` は `<tmp>/data/results/merged_peak.csv`）、2 行目は `{redo}`（`scripts/run_pipeline.sh --config <tmp>/c.ini を --phase なしで起動して、フェーズ2 から通しでやり直す`）。ZL2 は `0 件、ピーク 0`。(b) ZF3（`{path}` は `<tmp>/data/results/csv/3-5338.geojson`、`{detail}` は `JSON として読めない: Expecting value: line 1 column 1 (char 0)`。CPython 3.14.8 の文）。ZL2 は `0 件、ピーク 1`。(c) ZM1（UT 07 の (a) の 1 行目）。ZL2 は `1 件、ピーク 3`。(d) ZF3 でなく ZN1（`2 行目の peak_lat が JSON の数の書き方でない: +35.36058364`。ゾーンを読む前に止まる）。ZL2 は `0 件、ピーク 1` |
| `UT-merge_zones-14` | `start_log` の前の誤り | 子のプロセス。`--config` の値を `c.ini`（相対パス）にする（共通の準備の値でなく、この値で渡す） | なし | 終了コード 2 で ZA5。`<tmp>/logs` を作らない |
| `UT-merge_zones-15` | `--mesh` の範囲 | 子のプロセス。`merged_peak.csv` に見出しと行 P（`analysis_id` `3-5339`）。`3-5338.geojson` に P の両ゾーン（`area_complete` 真、`R(1)`・`R(2)`）、`3-5339.geojson` に P の両ゾーン（`area_complete` 偽、`R(3)`・`R(4)`） | (a) 引数なし、(b) `--mesh 5339` | どちらも終了コード 0。(a) ゾーンは `3-5338.geojson` のもの（`true` が先）、ZL1 は `2 件` で `activation_zone 0・delete_zone 0`。(b) ゾーンは `3-5339.geojson` のもの（`3-5338.geojson` を読まない）、ZL1 は `1 件` で `activation_zone 1・delete_zone 1` |

- 画素・中心の緯度経度は、[7.2.5](#725-ut-候補)の求め方と同じ、[2.4](#24-言語ごとに別に実装する式のテストベクトル)の計算の決まりのとおりに、2026-10-31 に CPython 3.14.8 で求めた（G0 (7426886, 3312429)、E10 (7426896, 3312429)、E1000 (7427886, 3312429)、E2000 (7428886, 3312429)。ST の共通の前提と同じ）。
- UT 09 の (a) のバイト列は、`json.dumps('é"')` が `"\u00e9\""` になること（16 進は小文字）を CPython 3.14.8 で確かめた。

### 7.4 `check_cols`

- **ID**: LLD-check_cols
- **対応 HLD**: [3.5](30_HLD.md#35-cmp5-統合突合)・[4.22](30_HLD.md#422-fr-022-コル充足判定)
- **ファイル**: `scripts/check_cols.py`

関数の名前と役割と呼ぶ順は [HLD 3.5.3](30_HLD.md#353-関数) の `check_cols` の関数の表のとおりで、処理の正本は [HLD 4.22.2](30_HLD.md#4222-処理の流れ)・[4.22.3](30_HLD.md#4223-異常系) である。この節は、それを Python で書くための細部（引数の読み方、型、止まり方、リストの書き方、メッセージの文面、UT 候補）だけを足す。`check_cols` は CMP3（パイプライン制御）が起動する内部の起動口で、`--config <絶対パス>` と `--n <3|4|5|6>` を受け取る（[HLD 2.4.5](30_HLD.md#245-内部引数)）。処理の目的は [FR-022](20_SRS.md#fr-022-コル充足判定) のコル充足判定で、`merged_peak.csv` の未確定のピークを `key_col_unresolved_peaks-<N>.csv` に書き、未確定の有無を終了コード（0 か 3）で返す。

- メモリ（[HLD 4.22.2](30_HLD.md#4222-処理の流れ)の「メモリ」）は、`read_merged_peak` が 1 行ずつ渡し、`collect_unresolved` が未確定の組の文字列だけを持つことで受ける。リストの中身は一時ファイルを開く前に組み立てるので、書き出す間はその全文も持つ（未確定の組と同じ大きさ）。
- リストの字句と順（HLD の [DEC107](30_HLD.md#4224-設計判断)「未確定のリストは `merged_peak.csv` のまま書く」）は、`collect_unresolved` が文字列を直さず、並べ替えも重なりの除去もしないことで受ける。
- 件数のログと、警告を出さないこと（HLD の [DEC105](30_HLD.md#4224-設計判断)「未確定の件数は CMP5 が、警告と案内は CMP3 が出す」）は、結果の要約（KL1〜KL3）を通常のログに出し、`WARNING:` を出さないことで受ける。
- 結合のつなぎ目は、`CMP5-INT2`（`merge_peaks` → `check_cols`。[7.1](#71-cmp5_common) の `read_merged_peak` が 3 列を読む）、`CMP5-EXT6`（引数と終了コード 0・1・2・3）、`CMP3-EXT4`（CMP3 がリストの有無を見る。[HLD 3.3.5](30_HLD.md#335-結合のつなぎ目)）、`CMP4-EXT4`（リストの中身を [6.2](#62-analyze_terrain_target) の `read_unresolved_peaks` が読む。7.4 が書く見出しと、CMP4（地形解析エンジン）が書いた座標の字句は、その読み方に収まる。7.1 が受けても 6.2 が読まない極小の値の差は 7.1.3 の「10 進の数の決まり」に書いてあり、7.4 は字句を直さない。[HLD 3.4.5](30_HLD.md#345-結合のつなぎ目)）である（[HLD 3.5.5](30_HLD.md#355-結合のつなぎ目)）。IT のケースは `60_IT.md` の `IT-CMP5-INT2-01`・`02`、`IT-CMP3-EXT4-01`・`02`、`IT-CMP4-EXT4-01` ほか。

#### 7.4.1 ファイル割付

- 関数はすべて `scripts/check_cols.py` 1 本に置く（ADR-LLD-001 の Decision 5）。`venv/bin/python3 scripts/check_cols.py` で起動され（[HLD 3.5.1](30_HLD.md#351-プログラム)）、共通部品は `import common`、CMP5 の共通部品は `import cmp5_common` で読む（[2.1.1](#211-ファイル割付)・[7.1.1](#711-ファイル割付)と同じ）。7.1 の部品と型は `cmp5_common.read_merged_peak(...)` のようにモジュールの属性として使う（[7.2.1](#721-ファイル割付)・[7.3.1](#731-ファイル割付)と同じ形）。ほかに読むのは、標準の `os`・`shlex`・`sys` と、`dataclasses` の `dataclass`、`typing` の `Iterable`・`Iterator`・`Sequence` である。
- ファイルの先頭のコメントに `# trace: LLD-check_cols` を書く。起動の部分は `if __name__ == '__main__': main()`。
- UT のコードは `tests/scripts/test_check_cols.py` に置く。各テストに `# trace: UT-check_cols-NN` のコメントを付ける。テストの枠組みは [2.1.1](#211-ファイル割付)と同じく標準の `unittest`。

#### 7.4.2 型とデータ

- 内部の定数（モジュールの最上位。名前は `_` で始める）:
  - `_CONFIG_KEYS_USED = ('data_dir', 'log_dir')`（[HLD 2.3.2](30_HLD.md#232-設定ファイル)の表で CMP5 の [FR-022](20_SRS.md#fr-022-コル充足判定) が使うキー。`load_config` に渡す）。必須は `('data_dir',)`。
  - `_N_VALUES = ('3', '4', '5', '6')`（`--n` の値として受ける文字列。HLD 2.4.5 の `--n <3|4|5|6>`。`03`・`+3`・前後の空白は受けない）。
  - `_LIST_HEADER = 'peak_lat,peak_lon'`（[HLD 4.22.2](30_HLD.md#4222-処理の流れ)の 4「未確定のリストを書く」の見出しの行）。
- 内部の状態（モジュールの最上位）: `_config_opt: str = ''`（`main` の 5 が入れる、[7.4.4](#744-メッセージ文面)の `{config_opt}` の値。`main` を通らない同じプロセスの UT は空のまま使う。[7.2.2](#722-型とデータ)・[7.3.2](#732-型とデータ)と同じ）。
- `@dataclass(frozen=True) class _Args`（内部）: `config: str`（`--config` の値のまま）、`n: int`（`--n` の値を `int` にしたもの。3〜6）。
- `@dataclass class _Counter`（内部。`frozen` にしない）: `peaks: int = 0`（`read_merged_peak` が渡した行の数）、`unresolved: int = 0`（そのうち `key_col_resolved` が `false` の行の数）。
- 未確定の組の並び: `list[tuple[str, str]]`（`(peak_lat, peak_lon)` の文字列。`merged_peak.csv` の字句のまま、行の順）。
- リストの名前は `f'key_col_unresolved_peaks-{n}.csv'`（`n` は `_Args.n`。[HLD 4.22.2](30_HLD.md#4222-処理の流れ)の 4「未確定のリストを書く」。[5.1](#51-run_pipeline) の `run_pipeline` が見る名前と同じ）。
- `slots=True` は付けない（[7.1](#71-cmp5_common)〜[7.3](#73-merge_zones)と同じく、メモリの実測〈HLD 5.2.2 の「実測の計画」の 3〉の後に決める）。

#### 7.4.3 関数の細部

関数ごとに `#####` の見出し（関数の名前だけ。ほかの節に同じ名前の見出しがあるものは `（check_cols）` を添える）を立てて書く。内部の関数は、使う関数の見出しの下に書く。

**止まり方**: 7.4 の関数は、誤りを見つけたら、[7.4.4](#744-メッセージ文面)のメッセージを `common.log_error` で出してから `sys.exit(common.EXIT_ERROR)` で止まる（`start_log` の前の引数と設定の誤りは `common.EXIT_USAGE`）。7.1 の部品の `InputError` は、`main` が [7.1.3](#713-関数の細部)の前置きの型で捕まえ、`common.log_error(e.what, _redo(args.n, e.symbol))` を出して `sys.exit(common.EXIT_ERROR)` で止まる（[HLD 4.22.3](30_HLD.md#4223-異常系)の 2 つ目の表の 1 行目）。`InputError` を捕まえる `try` は、`collect_unresolved` を呼ぶところの 1 つだけにする（`read_merged_peak` の生成器は、`collect_unresolved` が回す間に `InputError` を上げる）。

**{reason}**: [2.1.4](#214-メッセージ文面)と同じ。`{path}` は `os.path.abspath` したパス。

**終了コード 3**: [2.1.3](#213-関数の細部)の前置きの型のとおり、`try` の中で `code = common.EXIT_UNRESOLVED` を入れて `completed = True` にし、`try`/`finally` の後の `sys.exit(code)` で終える（`try` の中で `sys.exit(3)` を呼ぶと `completed` が偽のままになり、終えた実行に途中で止まった要約が出るため）。

**メモリ**: 7.4 の前置きに書いた。

##### main（check_cols）

`main() -> None`（起動の部分）。[2.1.3](#213-関数の細部)の前置きの呼ぶ側の書き方の型に従い、次の順に行う。

1. `start = common.StartTime.now()`。
2. `args = _parse_args(sys.argv[1:])`。
3. `config = common.load_config(args.config, _CONFIG_KEYS_USED, ('data_dir',))`。`data_dir`・`log_dir` を取り出す。
4. `common.start_log(log_dir, config, 'check_cols', sys.argv[1:], start)`。ロックは掛けない（内部の起動口は CMP3 のロックの下で動く。[HLD 2.9.3](30_HLD.md#293-同時起動の排他)）。
5. `_config_opt` に [7.4.4](#744-メッセージ文面)の `{config_opt}` の値を入れる。決め方は [7.2.3](#723-関数の細部)の `main` の 5 と同じ（`config.path == common.DEFAULT_CONFIG_PATH` なら空の文字列、それ以外は `' --config ' + shlex.quote(config.path)`）。
6. `try` の前に `completed = False`、`code = common.EXIT_OK`、`counter = _Counter()`、`list_path = ''` を置く。`try` の中で次を行う。
   1. `results_dir = os.path.join(data_dir, 'results')`、`merged_path = os.path.join(results_dir, 'merged_peak.csv')`。
   2. `try:` で `pairs = collect_unresolved(_count_rows(cmp5_common.read_merged_peak(merged_path, cmp5_common.MERGED_PEAK_UNRESOLVED_COLUMNS), counter))`、`except cmp5_common.InputError as e:` で `common.log_error(e.what, _redo(args.n, e.symbol))` と `sys.exit(common.EXIT_ERROR)`。
   3. `pairs` が空でなければ（`if` で分ける。`return` を使わない）、`write_unresolved_list(pairs, args.n, results_dir)`、`list_path = os.path.join(os.path.abspath(results_dir), <リストの名前>)`、`code = common.EXIT_UNRESOLVED`。空なら何も書かない（前からあるリストを消さない。消すのは CMP3 の段の始まり。[HLD 4.22.1](30_HLD.md#4221-目的と範囲)の「決定済みで参照だけするもの」の段の始まりの削除）。
   4. `completed = True`。
7. `finally` で結果の要約を `common.log_info` で出す（`completed` が偽なら KL3、真で `code` が `common.EXIT_OK` なら KL1、`common.EXIT_UNRESOLVED` なら KL2）。`WARNING:` のメッセージは出さない（HLD の [DEC105](30_HLD.md#4224-設計判断)「未確定の件数は CMP5 が、警告と案内は CMP3 が出す」）。
8. `sys.exit(code)`。

`start_log` の前に止まる誤り（`_parse_args`・`load_config`）は、標準エラー出力だけに出て、ログファイルと `log_dir` を作らない（[HLD 3.5.3](30_HLD.md#353-関数)の「ここまでの誤りは、ログファイルを作らずに終了コード 2」）。`--n` の誤りを `merged_peak.csv` を読む前に止めるのは、[HLD 4.22.2](30_HLD.md#4222-処理の流れ)の「処理を始める前に終了コード 2 で止まる」のため。

`_count_rows(rows: Iterable[cmp5_common.MergedPeakRow], counter: _Counter) -> Iterator[cmp5_common.MergedPeakRow]`（内部の生成関数）: `rows` の行ごとに `counter.peaks` を 1 増やし、`row.values['key_col_resolved'] == 'false'` なら `counter.unresolved` も 1 増やしてから、その行を渡す。途中で `InputError` が出たときは、その時点までに渡した行の数が残る（[HLD 5.7.2](30_HLD.md#572-処理の流れ)の 7「結果の要約」の「そこまでに終えた分の件数」）。ピークの数と未確定の数は HLD の表の `collect_unresolved` の返すものに無いので、`main` がこの関数で数える。

`_redo(n: int, symbol: str) -> str`（内部）: [7.4.4](#744-メッセージ文面)の `{redo}` の文を返す。`n` が 3 なら `{redo_phase2}`、`n` が 4〜6 で `symbol` が `'MP1'` なら `{redo_missing}`、ほか（`'MP2'`・`'MP3'`・`'KW1'`・`'KW2'`）なら `{redo_stage}`（3 つの文は 7.4.4）。`_config_opt` を読む。

##### _parse_args（check_cols）

`_parse_args(argv: Sequence[str]) -> _Args`（内部）。[7.3.3](#733-関数の細部)の `_parse_args` の受け方で、受ける名前を `--config`・`--n` にしたもの。最初に見つけた誤り 1 つで、[7.4.4](#744-メッセージ文面)のメッセージを `common.log_error` で出して `sys.exit(common.EXIT_USAGE)`。

1. `argv` を左から読む。`--config`・`--n` なら、その名前がすでに出ていれば KA3（値を見る前に判定する）、最後の引数なら KA2、そうでなければ次の引数を値にして 2 つ進む（値は `-` で始まっていてもそのまま値にする）。ほかの引数（位置引数、知らない名前〈`--mesh` を含む〉、`=` の付いた形、`--help`、`--` だけ、空の引数）は KA1。
2. `--config` が無ければ KA4。
3. `--config` の値が `os.path.isabs` で偽なら（空を含む）KA5。値は正規化しない。
4. `--n` が無ければ KA6。
5. `--n` の値が `_N_VALUES` のどれとも `==` でなければ KA7（空を含む）。
6. `_Args(config, int(n))` を返す。

##### collect_unresolved

`collect_unresolved(rows: Iterable[cmp5_common.MergedPeakRow]) -> list[tuple[str, str]]`

`rows` の順に、`row.values['key_col_resolved'] == 'false'` の行の `(row.values['peak_lat'], row.values['peak_lon'])` を並びの末尾に足し、全部を見た後に並びを返す（[HLD 4.22.2](30_HLD.md#4222-処理の流れ)の 2「未確定のピークを拾う」）。文字列は直さない。並べ替えも、同じ組の重なりの除去もしない（HLD の [DEC107](30_HLD.md#4224-設計判断)「未確定のリストは `merged_peak.csv` のまま書く」）。持つのは未確定の組だけ（HLD 4.22.2 の「メモリ」）。`rows` が `read_merged_peak` の生成器なら、その `InputError` はそのまま伝わる（並びを返さずに抜ける。リストを書く前に全部を読み終えるので、読み途中で止まってもリストを書かない）。

##### write_unresolved_list

`write_unresolved_list(pairs: list[tuple[str, str]], n: int, out_dir: str) -> None`

1. `path = os.path.join(os.path.abspath(out_dir), f'key_col_unresolved_peaks-{n}.csv')`、`tmp = path + '.tmp'`。中身は、`_LIST_HEADER` と LF、続けて組ごとに `peak_lat`・`,`・`peak_lon`・LF（BOM・CR・引用符を書かない。値に `,`・`"`・改行は入らない〈`read_merged_peak` が `is_valid_coord` で確かめた字句〉ので引用しない）。中身は一時ファイルを開く前に組み立て終える。`pairs` が空なら見出しの行だけ（`main` は空のとき呼ばないが、関数としてはそう書く）。
2. [2.3](#23-ファイルの名前と書き方)の一時ファイルの決まりで `tmp` に書く（`open(tmp, 'w', encoding='utf-8', newline='\n')`、書く、`flush`、`os.fsync`、閉じる）。どれかで `OSError` になったら、下の「止まり方」へ。
3. `os.replace(tmp, path)`。`OSError` なら、下の「止まり方」へ。
4. ディレクトリ（`results/`）は作らない（`merged_peak.csv` と同じ置き場で、`merge_peaks` が先に書いている）。同じ名前のリストがあれば置き換える（[HLD 4.22.2](30_HLD.md#4222-処理の流れ)の 4「未確定のリストを書く」）。

止まり方（2・3 の `OSError` を `e` とする）: `os.remove(tmp)` で一時ファイルを消す。消せたら KW1。`os.remove` が `OSError`（`r`）になったときは、`os.path.lexists(tmp)` が偽（一時ファイルが無い。開く前に失敗したときや、`results` がディレクトリでなく `NotADirectoryError` になったとき）なら KW1、真なら KW2（`{tmp}` は `tmp`、`{remove_reason}` は `r` の 2.1.4 の `{reason}`）。どちらも `{path}` は `path`、`{reason}` は `e` の `{reason}`、`{dir}` は `os.path.abspath(out_dir)`、2 行目の案内は `_redo(n, 'KW1')`（KW2 も同じ文）。出してから `sys.exit(common.EXIT_ERROR)`。2.3 の「消せないときの `OSError` は無視する」と違い KW2 で知らせるのは、[HLD 4.22.3](30_HLD.md#4223-異常系)の 2 つ目の表の 2 行目が、消せなかった書きかけのリストのパスを必ず含めると決めているため。

- `SIGINT`・`SIGTERM` で書く途中に止まったとき（2.1 の `SignalStop`）は、一時ファイルが残りうるが、正規の名前ではないので CMP3 も CMP4 も読まない（2.3 の「読む側は正規の名前しか読まない」）。次の起動が同じリストを書くときに上書きする。`SignalStop` を捕まえない（[1.2](#12-lld-の規約)）。

#### 7.4.4 メッセージ文面

書き方は [2.2](#22-ログとメッセージの文面)。設定の誤り（CF1〜CF7）は [2.1.4](#214-メッセージ文面)、ログの場面（G1〜G7）は 2.2、L1〜L3 は 2.2（`{program}` は `check_cols`）。7.1 の部品の誤り（MP1〜MP3）の 1 行目は [7.1.4](#714-メッセージ文面)の `what` のまま、2 行目は `{redo}`。

- `{path}`・`{reason}` は [7.4.3](#743-関数の細部)の前置きのとおり。`{arg}`・`{value}`・`{option}` は受け取った値を、2.2 の引用の決まり（`shlex.quote`）で書いたもの。
- `{config_opt}` は `main` の 5 で決めた値。`{n}` は `--n` の値（10 進）。
- `{redo}` は `_redo` が返す次の 3 つの文のどれか（[HLD 4.22.3](30_HLD.md#4223-異常系)の 2 つ目の表の 1 行目）。`check_cols` は起動の形（通しか単独起動か、`--mesh` の有無）を受け取らないので、起動の形ごとの手順を並べる。
  - `{redo_phase2}`（N が 3。MP1〜MP3、KW1・KW2）: `止まったときと同じ起動の形で scripts/run_pipeline.sh{config_opt} を起動し直し、フェーズ2 からやり直す（通しで止まったなら --phase なし、--phase 2 で止まったなら --phase 2。--mesh を付けていたなら同じ値を付ける）`
  - `{redo_stage}`（N が 4〜6。MP2・MP3、KW1・KW2）: `scripts/run_pipeline.sh --phase 3 --n {n}{config_opt} を起動し直し、その後はその段の結果の案内（未確定あり・未確定なし）に従って続ける。通しの実行に --mesh を付けていたときは、代わりに scripts/run_pipeline.sh{config_opt} を同じ --mesh で --phase なしで起動し、フェーズ2 から通しでやり直す`
  - `{redo_missing}`（N が 4〜6。MP1）: `merged_peak.csv が無いので --phase 3 は起動前提条件で止まる。フェーズ2 からやり直す。通しで止まったなら同じ通し（--mesh を付けていたなら同じ値）で、--phase 3 で止まったなら --phase 2（--mesh なし）か通しで、scripts/run_pipeline.sh{config_opt} を起動する`

| 記号 | 場面 | 1 行目（`ERROR:` と空白 1 つの後） | 2 行目（`対処:` と空白 1 つの後） | 終了コード |
|---|---|---|---|---|
| KA1 | 受け付けない引数 | `check_cols の知らない引数: {arg}` | `check_cols は run_pipeline が起動する内部の起動口。使える名前は --config・--n（値は次の引数で渡す）` | 2 |
| KA2 | 値が無い | `{option} の値が無い` | `{option} の後に値を渡す` | 2 |
| KA3 | 同じ名前を 2 回 | `{option} を 2 回渡した` | `{option} は 1 回だけ渡す` | 2 |
| KA4 | `--config` が無い | `--config が無い` | `--config と設定ファイルの絶対パスを渡す` | 2 |
| KA5 | `--config` が絶対パスでない | `--config のパスが絶対パスでない: {value}` | `--config に設定ファイルの絶対パスを渡す` | 2 |
| KA6 | `--n` が無い | `--n が無い` | `--n と生成段階タグ（3・4・5・6 のどれか）を渡す` | 2 |
| KA7 | `--n` の値が違う | `--n の値が 3・4・5・6 のどれでもない: {value}` | `--n に 3・4・5・6 のどれかを渡す` | 2 |
| KW1 | リストを書けない（書きかけは消した） | `key_col_unresolved_peaks-{n}.csv を書けない: {path}: {reason}` | `{dir} の空きと権限を確かめてから、{redo}` | 1 |
| KW2 | リストを書けず、書きかけも消せない | `key_col_unresolved_peaks-{n}.csv を書けない: {path}: {reason}。書きかけのリストも消せなかった: {tmp}: {remove_reason}` | `{tmp} を消し、{dir} の空きと権限を確かめてから、{redo}` | 1 |

- KW2 は、[HLD 4.22.3](30_HLD.md#4223-異常系)の 2 つ目の表の 2 行目の「消せなかった書きかけのリストのパスと、それを消してから止まった段をやり直す案内」を含める。残るのは `.tmp` で終わる一時ファイルで、次の段は読まないので、「広域解析が進みうる」の類の警告は書かない。

通常のログ（[HLD 4.22.2](30_HLD.md#4222-処理の流れ)の 4 の後の段落と [HLD 5.7.2](30_HLD.md#572-処理の流れ)の表の `check_cols` の行。2.2 の結果の要約の形）:

| 記号 | 行 | 文面 |
|---|---|---|
| KL1 | 結果の要約（未確定なし） | `結果の要約: N={n}、ピーク {peaks}、未確定のピーク 0。key_col_unresolved_peaks-{n}.csv は書いていない` |
| KL2 | 結果の要約（未確定あり） | `結果の要約: N={n}、ピーク {peaks}、未確定のピーク {unresolved}、書いたリスト {list_path}` |
| KL3 | 結果の要約（途中で止まった） | `結果の要約: 途中で止まった（N={n}、読んだピーク {peaks}、そのうち未確定 {unresolved}）。key_col_unresolved_peaks-{n}.csv は書いていない` |

- `{peaks}`・`{unresolved}` は `_Counter` の値、`{list_path}` は `main` の 6 の 3 の値。KL3 の数は止まった時点までのもの（HLD 5.7.2 の 7「結果の要約」）。

#### 7.4.5 UT 候補

すべて自動（合否をテストのコードが判定できる）。止まるケースの期待の「メッセージ」は、標準エラー出力の 2 行（[7.4.4](#744-メッセージ文面)・[7.1.4](#714-メッセージ文面)・[2.1.4](#214-メッセージ文面)・[2.2](#22-ログとメッセージの文面)の文面に値を入れたもの）。ログファイルの行の期待は、先頭の時刻と空白を除いた文面。共通の準備は次の 3 つ。

- **同じプロセス**: [7.2.5](#725-ut-候補)の同じ名前の準備と同じ（`merge_peaks` を `check_cols` に読み替える）。`check_cols._config_opt` は空の文字列にしておく。
- **子のプロセス**: [7.3.5](#735-ut-候補)の同じ名前の準備と同じ（`merge_zones` を `check_cols` に読み替え、`<tmp>/src/scripts/` に写すものを `check_cols.py`・`common.py`・`cmp5_common.py` にする。`<tmp>/data/results/` を作り、`merged_peak.csv` などはケースが置く。回ごとに `<tmp>/data/results/` と `<tmp>/logs/` を空にしてから、その回の「準備」の列に書いたファイルだけを置く）。起動は `subprocess.run([sys.executable, '<tmp>/src/scripts/check_cols.py', '--config', '<tmp>/c.ini', *<引数>], cwd='<tmp>/work', capture_output=True)`。`<tmp>/c.ini` は既定のパスでないので、メッセージの `{config_opt}` は空白 1 つと `--config <tmp>/c.ini`（パスは `shlex.quote` した形）になる。
- **merged_peak.csv の行**（13 列。見出しは `cmp5_common.MERGED_PEAK_ALL_COLUMNS` を `,` でつないだもの。システムテスト仕様書（ST）の `ST-FR-022-05` の R1〜R5。`<lat>,<lon>` の後の列は、`false` の行は `1500.00,0.00000000,0.00000000,,,false,1,3-5338,1,9,unstable`、`true` の行は `1500.00,35.34308245,138.74884844,1000.00,500.00,true,20,3-5338,1,9,unstable`）:
  - R1: `35.36058364,138.73168230` で `false`。R2: `35.36058364,138.72739077` で `true`。R3: `35.32557747,138.72739077` で `false`。R4: R1 と同じ行。R5: `35.40000000,138.80000000` で `false`、`peak_elev`（3 列目）を `abc` にしたもの。
  - 同じプロセスのケースは、`cmp5_common.MergedPeakRow(<path>, <line_no>, {'peak_lat': …, 'peak_lon': …, 'key_col_resolved': …})` を直接作ってよい。

| ID | 確かめること | 準備 | 入力 | 期待 |
|---|---|---|---|---|
| `UT-check_cols-01` | 引数の正しい形 | 同じプロセス | `_parse_args` に (a) `['--config', '/a.ini', '--n', '3']`、(b) `['--n', '6', '--config', '/a.ini']` | (a) `_Args('/a.ini', 3)`、(b) `_Args('/a.ini', 6)` |
| `UT-check_cols-02` | 引数の誤り | 同じプロセス | `_parse_args` に (a) `[]`、(b) `['--config', '/a', '--n']`、(c) `['--config', 'a.ini', '--n', '3']`、(d) `['--config', '/a', '--n', '3', '--n', '4']`、(e) `['--config', '/a', '--n', '3', '--mesh', '5338']`、(f) `['--config', '/a', '--n=3']`、(g) `['--config', '/a']`、(h) `['--config', '/a', '--n', <v>]` を `<v>` が `'2'`・`'7'`・`'03'`・`'+3'`・`' 3'`・`''` のそれぞれで、(i) `['--n', 'x', '--config', 'a.ini']`、(j) `['--n', '--config', '--config', '/a']`（`--n` の値が `-` で始まる） | どれも終了コード 2。(a) KA4、(b) KA2（`--n`）、(c) KA5（`a.ini`）、(d) KA3（`--n`）、(e) KA1（`--mesh`）、(f) KA1（`--n=3`）、(g) KA6、(h) KA7（`{value}` は `2`・`7`・`03`・`+3`・`' 3'`・`''`）、(i) KA5（`--n` の値より `--config` の確かめが先）、(j) KA7（`--config` を `--n` の値として読み、`{value}` は `--config`） |
| `UT-check_cols-03` | 未確定を拾う | 同じプロセス | `collect_unresolved` に (a) R1〜R5 の 3 列の行の並び（R5 の `peak_elev` は 3 列に入らない）、(b) 空の並び | (a) `[('35.36058364', '138.73168230'), ('35.32557747', '138.72739077'), ('35.36058364', '138.73168230'), ('35.40000000', '138.80000000')]`（R2 を除き、行の順のまま、R4 の重なりを残し、末尾の 0 を落とさない）、(b) `[]` |
| `UT-check_cols-04` | 書き出しのバイト列 | 同じプロセス。`<tmp>/results/` を作り、前のリスト `key_col_unresolved_peaks-4.csv`（`peak_lat,peak_lon\n35.00000000,139.00000000\n`）と前の起動の残りの `key_col_unresolved_peaks-4.csv.tmp`（中身 `x`）を置く | `write_unresolved_list` に (a) `[('35.36058364', '138.73168230'), ('+35.1', '035.10')]` と 4 と `<tmp>/results`、(b) `[]` と 5 と `<tmp>/results` | (a) `key_col_unresolved_peaks-4.csv` のバイト列が `peak_lat,peak_lon\n35.36058364,138.73168230\n+35.1,035.10\n`（前の行は残らない）。`.tmp` は残らない。(b) `key_col_unresolved_peaks-5.csv` が `peak_lat,peak_lon\n` |
| `UT-check_cols-05` | 書けない | 同じプロセス。`check_cols._config_opt` は空。(a) `<tmp>/results/` を作らない、(b) `<tmp>/results/key_col_unresolved_peaks-4.csv` をディレクトリにする、(c) `<tmp>/results/` を作り、`unittest.mock.patch('os.fsync', side_effect=OSError(28, 'No space left on device'))`（書いた後の失敗）、(d) (c) に加えて `unittest.mock.patch('os.remove', side_effect=OSError(13, 'Permission denied'))` | `write_unresolved_list([('35.36058364', '138.73168230')], 4, <tmp>/results)`、(e) は (c) を `n` が 3 で | どれも終了コード 1。(a) KW1（`{reason}` は `FileNotFoundError` の `strerror`）、(b) KW1（`IsADirectoryError` の `strerror`）。(c) KW1（`No space left on device`）で、`key_col_unresolved_peaks-4.csv` も `.tmp` も無い（`ST-FR-022-10` の (a)）。(a)〜(c) の `{path}` は `<tmp>/results/key_col_unresolved_peaks-4.csv`、`{dir}` は `<tmp>/results`、2 行目は `<tmp>/results の空きと権限を確かめてから、scripts/run_pipeline.sh --phase 3 --n 4 を起動し直し、その後はその段の結果の案内（未確定あり・未確定なし）に従って続ける。通しの実行に --mesh を付けていたときは、代わりに scripts/run_pipeline.sh を同じ --mesh で --phase なしで起動し、フェーズ2 から通しでやり直す`（`{redo_stage}` を `n` 4・`{config_opt}` 空で展開した全文）。(d) KW2 で、1 行目の後半が `書きかけのリストも消せなかった: <tmp>/results/key_col_unresolved_peaks-4.csv.tmp: Permission denied`、2 行目が `<tmp>/results/key_col_unresolved_peaks-4.csv.tmp を消し、<tmp>/results の空きと権限を確かめてから、` と `{redo_stage}`。`.tmp` が残り、`key_col_unresolved_peaks-4.csv` は無い（`ST-FR-022-10` の (b)）。(e) KW1 で、2 行目の案内が `{redo_phase2}` |
| `UT-check_cols-06` | 未確定ありの全体 | 子のプロセス。`merged_peak.csv` に見出しと R1〜R5。`key_col_unresolved_peaks-4.csv` に `peak_lat,peak_lon\n35.00000000,139.00000000\n` を置く（`ST-FR-022-05`） | `--n 4` | 終了コード 3。`key_col_unresolved_peaks-4.csv` のバイト列が `peak_lat,peak_lon\n35.36058364,138.73168230\n35.32557747,138.72739077\n35.36058364,138.73168230\n35.40000000,138.80000000\n`。ログファイルの最後から 2 行目が KL2（`N=4、ピーク 5、未確定のピーク 4、書いたリスト <tmp>/data/results/key_col_unresolved_peaks-4.csv`）、最後が L3。標準出力・標準エラー出力・ログファイルに `WARNING:` で始まる行が無い（`ST-FR-022-09`） |
| `UT-check_cols-07` | 未確定なしと 0 行 | 子のプロセス。(a) `merged_peak.csv` に見出しと R2、(b) 見出しだけ | `--n 4` | どちらも終了コード 0 で、`key_col_unresolved_peaks-4.csv` を書かない。ログファイルの最後から 2 行目が KL1 で、(a) `結果の要約: N=4、ピーク 1、未確定のピーク 0。key_col_unresolved_peaks-4.csv は書いていない`、(b) `結果の要約: N=4、ピーク 0、未確定のピーク 0。key_col_unresolved_peaks-4.csv は書いていない`、最後が L3（`ST-FR-022-02`・`03`・`09`）。`WARNING:` で始まる行が無い |
| `UT-check_cols-08` | 読めないときの案内 | 子のプロセス。(a) `merged_peak.csv` を置かない、(b) `merged_peak.csv` の見出しから `key_col_resolved` を除き、R1・R3 から同じ列を除いた 2 行、(c) 0 バイトのファイル、(d) 見出しと R1・R3 で、R3 の `key_col_resolved` を `TRUE` にしたもの、(e) 見出しと R1・R3 で、R3 の `peak_lat` を `abc` にしたもの、(f) `merged_peak.csv` をディレクトリにする | (a)〜(f) を `--n 3` と `--n 5` のそれぞれで | どれも終了コード 1 で、リスト（`-3.csv`・`-5.csv`）も `.tmp` も無い。1 行目は 7.1.4 の (a) MP1、(b) MP3（`見出しに列 key_col_resolved が無い`）、(c) MP3（`見出しの行が無い`）、(d) MP3（`3 行目の key_col_resolved が true か false でない: TRUE`）、(e) MP3（`3 行目の peak_lat が 座標として読めない: abc`）、(f) MP2（`{reason}` は `IsADirectoryError` の `strerror`）。2 行目は、`--n 3` はどれも `{redo_phase2}`、`--n 5` は (a) が `{redo_missing}`、(b)〜(f) が `{redo_stage}`（`--n 5`）。どれも `{config_opt}` は空白 1 つと `--config <tmp>/c.ini`（期待の文は 7.4.4 の文を展開した全文で書く）。ログファイルの終わりの 4 行は、標準エラー出力と同じ 2 行、KL3、L3 の順で、KL3 は (a)〜(c)・(f) が `結果の要約: 途中で止まった（N=<n>、読んだピーク 0、そのうち未確定 0）。key_col_unresolved_peaks-<n>.csv は書いていない`、(d)(e) が `読んだピーク 1、そのうち未確定 1` の同じ形（`<n>` は 3 か 5。`ST-FR-022-04`・`06`・`08`） |
| `UT-check_cols-09` | `start_log` の前の誤り | 子のプロセス。`merged_peak.csv` を置かない | (a) `--n 2`、(b) `--n 7` | どちらも終了コード 2 で KA7。`<tmp>/logs` を作らない（`merged_peak.csv` を読む前に止まる。`ST-FR-022-07`） |

- `ST-FR-022-01` は UT 06、`ST-FR-022-10` は UT 05 の (c)(d) が受ける（`ST-FR-022-10` の (b) は、一時ファイルの書き方に合わせて直した字句。[HLD 4.22.3](30_HLD.md#4223-異常系)の 2 つ目の表の 2 行目と同じ）。

### 7.5 `match_summits`

- **ID**: LLD-match_summits
- **対応 HLD**: [3.5](30_HLD.md#35-cmp5-統合突合)・[4.7](30_HLD.md#47-fr-007-per-mesh-csv-出力プロミネンス閾値適用)・[4.9](30_HLD.md#49-fr-009-sotaリスト突合match_status-判定)・[4.12](30_HLD.md#412-fr-012-サミット一覧申請内容反映版生成)・[5.2](30_HLD.md#52-nfr-002-メモリ使用量)・[5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)
- **ファイル**: `scripts/match_summits.py`

関数の名前と役割と呼ぶ順は [HLD 3.5.3](30_HLD.md#353-関数) の `match_summits` の関数の表のとおりで、処理の正本は [HLD 4.9.2](30_HLD.md#492-処理の流れ)・[4.9.3](30_HLD.md#493-異常系)（`merged_summit.xlsx` の規則は [4.12.2](30_HLD.md#4122-処理の流れ)）である。この節は、それを Python で書くための細部（型、止まり方、読み方の細部、メッセージの文面、UT 候補）だけを足す。`match_summits` は CMP3（パイプライン制御）がフェーズ4 で起動する内部の起動口で、`--config <絶対パス>` だけを受け取る（[HLD 2.4.5](30_HLD.md#245-内部引数)）。処理の目的は [FR-009](20_SRS.md#fr-009-sotaリスト突合match_status-判定) の突合で、`merged_peak.csv` と `merged_peak.geojson` と SOTA サミットリスト CSV と山岳データ登録変更リストから、`merged_summit.geojson` と `merged_summit.xlsx` を作る。

**この節は 5 回に分けて書いた**（関数が 22 あり、元になる HLD の文が 7.2 の 3.5〜4 倍あるため。2026-11-01 に持ち主が決めた。はじめは 3 回に分ける予定だったが、残りの元の文が 1 回目の約 3 倍あったので、同じ日に 4 回に分け直した。2026-11-03 に、4 回目の範囲の元の文が約 70〜80 KB あり、3 回目〈約 18 KB〉の約 4 倍になるので、持ち主が 5 回に分け直した）。5 回の分担は、1 回目が読み込みの 6 関数（`match_zones_to_peaks`・`read_summits_list`・`find_updatelist`・`read_updatelist`・`read_boundaries`・`build_spatial_indexes`）、2 回目が突き合わせの 4 関数（`is_in_zone`・`z15_pixel_center_latlon`・`match_activation_zones`・`match_delete_zones`）と照合と採番の 2 関数（`locate_regions`・`assign_provisional_codes`）、3 回目が属性と申請済みの判定の 5 関数（`read_sota_names`・`derive_attributes`・`build_rationale`・`match_pending_applications`・`build_pending_note`）、4 回目が組み立ての 3 関数（`build_metadata`・`build_summit_features`・`build_summit_sheets`）、5 回目が書き出しの群の 2 関数（`write_summit_outputs`・`check_defect_gate`）と起動の部分（`main`・`_parse_args`）である。関数は [HLD 3.5.3](30_HLD.md#353-関数)の表の 22 と起動の部分で、すべてこの節に書いてある。[HLD 4.7](30_HLD.md#47-fr-007-per-mesh-csv-出力プロミネンス閾値適用)（Z15 の画素の変換）は、`z15_pixel_center_latlon` の式を [2.4](#24-言語ごとに別に実装する式のテストベクトル)の計算の決まりと表 7 で CMP4（地形解析エンジン）とそろえることで受ける（[7.1](#71-cmp5_common)の `latlon_to_z15_pixel` と同じ形）。

- [5.2](30_HLD.md#52-nfr-002-メモリ使用量)（メモリ）は、`build_spatial_indexes` の細部（ゾーンのジオメトリを持ち続けたまま索引用の形を作るので、2 つの形で持つ）と、[main](#mainmatch_summits)が `read_zone_features` の並びを `match_zones_to_peaks` の後に `del` で手放すこと（[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「メモリ」の持つものは、ゾーンの索引と表で、読んだ並びではない）で受ける。メモリのピークは、実装の後に [HLD 5.2.2](30_HLD.md#522-処理の流れ)の「実測の計画」の 4「CMP5 の突合」で測る。
- [5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)（再現性）は、`merged_summit.geojson` のフィーチャの並びとキーの順・数の書き方と、`merged_summit.xlsx` の行の並び・数の書き方を [build_summit_features](#build_summit_features)・[build_summit_sheets](#build_summit_sheets)、警告ログの並びを [main](#mainmatch_summits)の「警告を出す時機と順」、登録変更リストの申請の並びと知らせる行の並びを [match_pending_applications](#match_pending_applications)、仮サミットコードの採番の順と主ピークの比べ方を [assign_provisional_codes](#assign_provisional_codes)・[match_delete_zones](#match_delete_zones)で受ける。`generated_at` などの時刻と `software_version` は再現性の対象外（[HLD 5.3.2](30_HLD.md#532-処理の流れ)の表）。XLSX の文書のプロパティは [#188](https://github.com/jj1xgo/findsummits/issues/188)「XLSX の文書のプロパティを `NFR-003` の内容に入れるか」で決める。
- 結合のつなぎ目は、`CMP5-INT3`（`merge_peaks`・`merge_zones` → `match_summits`。`read_merged_peak` の 13 列と `read_zone_features` と `match_zones_to_peaks` の MZ1）、`CMP5-EXT4`（CMP1（行政区域前処理） → `match_summits`。`read_boundaries` と BN1・BN2）、`CMP5-EXT5`（CMP2（タイル取得） → `match_summits`。`build_metadata` の `_tile_latest_date`）、`CMP5-EXT6`（CMP3（パイプライン制御） → `match_summits`。`--config` と終了コード 0・1・2・4）、`CMP5-EXT7`（利用者 → `match_summits`。`read_summits_list`・`read_sota_names`・`read_updatelist`）である。渡す側の `CMP6-EXT1`（`merged_summit.geojson`。CMP6（可視化生成）の `generate_viewer` が読む）も、書き方は [write_summit_outputs](#write_summit_outputs)と [build_summit_features](#build_summit_features)が決める（[HLD 3.5.5](30_HLD.md#355-結合のつなぎ目)・[3.6.5](30_HLD.md#365-結合のつなぎ目)）。IT のケースは `60_IT.md` の `IT-CMP5-INT3-01`〜`03`、`IT-CMP5-EXT4-01`・`02`、`IT-CMP5-EXT5-01`・`02`、`IT-CMP5-EXT6-01`〜`04`、`IT-CMP5-EXT7-01`、`IT-CMP6-EXT1-01`・`02`。
- 読み込みの関数は警告を出さず、`Boundaries.warnings`・`UpdateList.notices` に並べて返す。警告を出すのは [main](#mainmatch_summits) である。登録変更リストの知らせる行を出す順は [HLD 4.9.2](30_HLD.md#492-処理の流れ)の「申請済みの判定」の 7「知らせる行をまとめる」が決め、地域と市区町村に入らない点の警告は 7「地域と市区町村を照合する」が `assign_provisional_codes` の後と決めている。地域と市区町村の GeoJSON が無いときの警告（BN1・BN2）を出す時機は HLD に定めが無い（4「地域と市区町村の GeoJSON を読み、索引を作る」が、7 の点ごとの警告をこの警告 1 つにまとめると決めるだけ）ので、[main](#mainmatch_summits)の「警告を出す時機と順」が決める。読み込みの関数の中で出すと、これらの順を [main](#mainmatch_summits) が決められなくなるため、読み込みの関数は出さない。突き合わせと照合・採番の関数も同じ理由で警告を出さず、警告の材料を返り値に並べて返す（`ActivationMatch.overlaps`・`DeleteMatch.unmatched`・`RegionMatch.outside`）。属性と申請済みの判定の関数も同じ理由で警告を出さず、材料を返り値に並べて返す（`SotaNames.warnings`・`Attributes.null_points`・`Attributes.groups`・`Pending.notices`）。組み立ての `build_metadata` も同じ理由で警告を出さず、材料を `Metadata.warnings` に並べて返す。ただし、2 つ以上の確定したピークの AZ に含まれるサミットがあるとき（AO1）と、仮サミットコードの連番上限を超えるエリアがあるとき（PN1・PN2）は入力の誤りで止まる場面なので、`match_activation_zones` と `assign_provisional_codes` が [7.5.4](#754-メッセージ文面)のメッセージを出して止まる。`build_summit_sheets` も、XLSX の行を結べないとき（XS1）と書けない文字列があるとき（XS2）に、書き出しの前に同じ形で止まる。

#### 7.5.1 ファイル割付

- 関数はすべて `scripts/match_summits.py` 1 本に置く（ADR-LLD-001 の Decision 5）。`venv/bin/python3 scripts/match_summits.py` で起動され（[HLD 3.5.1](30_HLD.md#351-プログラム)）、共通部品は `import common`、CMP5 の共通部品は `import cmp5_common` で読む（[2.1.1](#211-ファイル割付)・[7.1.1](#711-ファイル割付)と同じ）。7.1 の部品と型は `cmp5_common.is_valid_coord(...)` のようにモジュールの属性として使う（[7.2.1](#721-ファイル割付)・[7.3.1](#731-ファイル割付)・[7.4.1](#741-ファイル割付)と同じ形）。
- 7.5 の関数が読む標準のモジュールは、`csv`・`datetime`・`decimal`・`json`・`math`・`os`・`re`・`shlex`（`_config_opt`。[main](#mainmatch_summits)の 5）・`subprocess`・`sys`・`unicodedata`・`xml.etree.ElementTree`（`ET` として）・`xml.parsers.expat`、`dataclasses` の `dataclass`（型と `_Args` が使う）、`collections.abc` の `Sequence`（`build_pending_note`・`build_metadata`・`_parse_args` の宣言が使う。`typing` からは読まない。`ruff.toml` が選ぶ `UP` の UP035 が、`typing` の `Sequence` の import を止めるため）である（`collections.abc` の `Iterable` は、7.5 の関数の宣言が使わないので読まない）。ほかに `shapely`（`import shapely`・`import shapely.errors`・`import shapely.geometry`。`requirements.txt` にある。使う版は 2.x で、`STRtree` の `query` が添字の配列を返す。突き合わせと照合の関数が使う `shapely.Point`・`shapely.contains_xy`・`shapely.covers` と `STRtree` の `geometries` は、`import shapely` で使える）。`subprocess` は `build_metadata` の `git describe` が使う。ほかに `openpyxl`（`import openpyxl` と `import openpyxl.cell.cell`。`requirements.txt` にある。使う版は 3.1。`build_summit_sheets` が `openpyxl.Workbook` と `openpyxl.cell.cell.ILLEGAL_CHARACTERS_RE` を使う）。import の並びは `ruff` の I001（isort の既定）が決めるとおりにする: 標準のモジュール、その次に `cmp5_common`・`common`・`openpyxl`・`shapely` を同じ区画に名前の順で並べる（`common`・`cmp5_common` は `ruff` から見て第三者のモジュールで、`shapely` と区画を分けない）。
- ファイルの先頭のコメントに `# trace: LLD-match_summits` を書く。起動の部分は `if __name__ == '__main__': main()`（[main](#mainmatch_summits)を呼ぶ）。
- UT のコードは `tests/scripts/test_match_summits.py` に置く。各テストに `# trace: UT-match_summits-NN` のコメントを付ける。ID は 01 から通しで付ける。テストの枠組みは [2.1.1](#211-ファイル割付)と同じく標準の `unittest`。

#### 7.5.2 型とデータ

- 内部の定数（モジュールの最上位。名前は `_` で始める）。どれも `fullmatch` で使う。数字は `[0-9]` で書く（`\d` は全角の数字にも合うため）:
  - SOTA サミットリスト CSV: `_SUMMITS_COLUMNS = ('SummitCode', 'SummitName', 'AltM', 'Latitude', 'Longitude', 'ValidTo')`（[SRS §7.2.4](20_SRS.md#724-sota-サミットリスト-csv)の使用カラム）。`_SUMMITS_DATE_RE = re.compile(r'SOTA Summits List \(Date=([0-9]{2})/([0-9]{2})/([0-9]{4})\)')`（1 行目の基準日）。`_DMY_RE = re.compile(r'([0-9]{2})/([0-9]{2})/([0-9]{4})')`（`ValidTo`）。`_INTEGER_RE = re.compile(r'[+-]?[0-9]+')`（`AltM`。[7.1.3](#713-関数の細部)の「整数」と同じ字句）。`_SUMMIT_CODE_RE = re.compile(r'([^/]+)/([^-]+)-.+')`（アソシエーションと地域コードを切り出す。1 つ目の組がアソシエーション、2 つ目の組が地域コード）。
  - 登録変更リスト: `_UPDATELIST_RE = re.compile(r'sota_updatelist_([0-9]{4})\.xhtml')`（ファイル名の全体。[DEC188](30_HLD.md#494-設計判断)「登録変更リストのファイル名は ASCII の年だけ」）。`_TITLE_YEAR_RE = re.compile(r'([0-9]{4})年')`・`_TITLE_FULL_RE = re.compile(r'([0-9]{4})年 ?山岳データ登録変更リスト')`・`_TITLE_TEXT = '山岳データ登録変更リスト'`（題の行）。`_UPDATE_DATE_RE = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}')`（Update の日付）。`_APPLIED_RE = re.compile(r'(?<![0-9/])([0-9]{4})/([0-9]{1,2})/([0-9]{1,2})(?![0-9/])')`（申請日。前後が数字や `/` に隣り合うものは日付としない）。`_SPAN_RE = re.compile(r'[1-9][0-9]*')`（`rowspan`・`colspan`）。`_SPAN_MAX = 100`（`rowspan`・`colspan` の上限。[7.5.3](#753-関数の細部)の `read_updatelist` の 4）。`_SUMMIT_ID_RE = re.compile(r'[A-Z0-9]+/[A-Z0-9]+-[0-9]+')`（山岳 ID）。`_ELEV_RE = re.compile(r'[0-9]+(\.[0-9]+)?')`（変更後の標高）。`_ACTIONS = {'追加': 'add', '変更': 'change', '削除': 'delete'}`。
  - 見出しの文字（空白をすべて除いた後の形。列を引くのに使う）: アクション `アクション`、山岳 ID か県名 `既存山岳IDもしくは県名`、変更後 `変更後` と標高 `標高m`、新規追加詳細 `新規追加詳細` と位置 `位置`、申請者・申請日 `申請者・申請日`。UX4 のメッセージの `{name}` は、比べるための空白を除いた形でなく、ページの見出しの書き方のまま `既存山岳ID もしくは 県名` と書く（[7.5.3](#753-関数の細部)の `read_updatelist` の 5）。
  - 知らせる行の `reason`: [7.5.4](#754-メッセージ文面)の表の 9 つの文を定数にする（`_REASON_ACTION`・`_REASON_POSITION`・`_REASON_ID`・`_REASON_ELEV`・`_REASON_DATE`・`_REASON_UPDATE`・`_REASON_UNKNOWN_ID`・`_REASON_AMBIGUOUS_REGION`・`_REASON_UNMATCHED_ADD`）。
  - 照合と採番: `_ZZ = 'ZZ'`（地域に入らないピークのアソシエーションとエリアの両方の値。コードは `ZZ/ZZ-A00` の形になる）、`_CODE_PER_PREFIX = 100`（仮サミットコードの接頭の文字 1 つが受け持つ連番の数。`00`〜`99`）。
  - 属性と申請済みの判定: `_BANDS = ((1500, 10), (1100, 8), (850, 6), (650, 4), (500, 2), (150, 1))`（用語集の[標高バンド](00_GLOSSARY.md#標高バンドpoints-算出表)の表。`(下限, ポイント)` の組を下限の降順に並べる）。`_ACTION_JA = {'add': '追加', 'change': '変更', 'delete': '削除'}`（`pending_note` の語）。`_ACTION_ORDER = {'add': 0, 'change': 1, 'delete': 2}`（`pending_applications` の並びでアクションを比べる順）。`_KIND_ORDER = {'unreadable_row': 0, 'unknown_id': 1, 'ambiguous_region': 2, 'unmatched_add': 3, 'unreadable_update': 4}`（知らせる行の同じ行の中で `kind` を比べる順）。
  - metadata・GeoJSON・XLSX の組み立て（4 回目）:
    - metadata の固定の文字列: `_ATTRIBUTION = '地理院タイル（標高タイル）を加工して作成。出典: 国土地理院'`、`_SOURCE_URL = 'https://maps.gsi.go.jp/development/ichiran.html'`、`_LICENSE_URL = 'https://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html'`（[FR-009](20_SRS.md#fr-009-sotaリスト突合match_status-判定)の「metadata 付与」の字句のまま）。
    - XLSX の列の名前と順: `_SHEET_COLUMNS: tuple[str, ...]` は次の 37 列（[FR-012](20_SRS.md#fr-012-サミット一覧申請内容反映版生成)の「出力カラム」の表の順）。`category`・`match_status`・`review_reason`・`review_group_id`・`review_decision`・`review_note`・`application_exclusion`・`exclusion_note`・`pending_match`・`pending_note`・`pending_return`・`stability`・`summit_code`・`summit_name`・`summit_name_jp`・`peak_lat`・`peak_lon`・`peak_elev`・`points`・`col_lat`・`col_lon`・`col_elev`・`prominence`・`key_col_resolved`・`col_margin_px`・`analysis_count`・`expected_count`・`sota_lat`・`sota_lon`・`sota_alt_m`・`sota_points`・`is_band_change_candidate`・`municipality`・`region_name`・`area_complete`・`dominant_peak_code`・`dominant_peak_dist_m`。
    - XLSX のシートの名前と文: `_SHEET_NAME = 'サミット一覧'`、`_SOURCE_SHEET_NAME = '出典'`、`_SOURCE_SHEET_TEXT = '地理院タイル（標高タイル）を加工して作成。出典: 国土地理院 (https://maps.gsi.go.jp/development/ichiran.html)'`（[FR-012](20_SRS.md#fr-012-サミット一覧申請内容反映版生成)の出典シートの文の全体）。
    - 数のセルの表示形式: `_NUMBER_FORMATS = {'peak_lat': '0.00000000', 'peak_lon': '0.00000000', 'col_lat': '0.00000000', 'col_lon': '0.00000000', 'peak_elev': '0.00', 'col_elev': '0.00', 'prominence': '0.00', 'dominant_peak_dist_m': '0.0'}`（ほかの数には付けない）。
    - 列の取り元: `_SHEET_SOURCES: dict[str, dict[str, tuple[str, str] | None]]`。鍵は `_SHEET_COLUMNS` の列の名前、値は行の種類（`'P'`＝ピークの点の行、`'A'`＝`ambiguous` のサミットの点の行、`'S'`＝ほかのサミットの点の行）から `(取り元, 取るもの)` か `None`（空にする列）への辞書。取り元は `'self'`（行を生む点）・`'peak'`（結んだピークの点）・`'col'`（結んだコルの点）・`'az'`（結んだ AZ）・`'az_summit'`（結んだ AZ の中のサミットの点）の 5 つで、取るものは、プロパティの名前か、点の座標の緯度 `'lat'`・経度 `'lon'`（`geometry['coordinates']` の 2 番目と 1 番目。[HLD 4.12.2](30_HLD.md#4122-処理の流れ)の 3「列の値を取る」の表）。値は次の表のとおり。表の `self`・`peak`・`col`・`az`・`az_summit` は、その列の名前を取るものにした `(取り元, 列の名前)` の略（たとえば `category` の `self` は `('self', 'category')`）。

      | 列 | `'P'` | `'A'` | `'S'` |
      |---|---|---|---|
      | `category`・`match_status`・`review_reason`・`review_group_id`・`review_decision`・`review_note`・`application_exclusion`・`exclusion_note`・`pending_match`・`pending_note`・`pending_return`・`summit_code`・`summit_name`・`summit_name_jp`・`municipality`・`region_name` | `self` | `self` | `self` |
      | `peak_lat`・`peak_lon` | `('self', 'lat')`・`('self', 'lon')` | `('peak', 'lat')`・`('peak', 'lon')` | `None` |
      | `peak_elev`・`prominence`・`points`・`stability`・`key_col_resolved`・`analysis_count`・`expected_count` | `self` | `peak` | `None` |
      | `col_lat`・`col_lon` | `('col', 'lat')`・`('col', 'lon')` | 同じ | `None` |
      | `col_elev`・`col_margin_px` | `col` | `col` | `None` |
      | `area_complete` | `az` | `az` | `None` |
      | `sota_lat`・`sota_lon` | `('az_summit', 'lat')`・`('az_summit', 'lon')` | `('self', 'lat')`・`('self', 'lon')` | 同じ |
      | `sota_alt_m`・`sota_points` | `az_summit` | `self` | `self` |
      | `is_band_change_candidate` | `self` | `None` | `None` |
      | `dominant_peak_code`・`dominant_peak_dist_m` | `None` | `self` | `self` |

      `'az_summit'` は `match_status` が `matched` のピークの行にだけあり、ほかのピークの行は空にする。結んだ `key_col` の点が 0 個のとき（`key_col_resolved=false` のピークと海面で確定したピーク）は、`'col'` の列を空にする。
  - 起動と書き出し:
    - `_CONFIG_KEYS_USED = ('data_dir', 'log_dir', 'provisional_code_max_prefix', 'unmatched_summit_threshold', 'sota_geojson_version')`（[HLD 3.5.2](30_HLD.md#352-入力処理出力)の設定の 3 つと、どのバッチも使う置き場の 2 つ。`load_config` に渡す。必須は `('data_dir',)`）。
    - `_DEFECT_COLUMNS = {'unmatched_over_threshold': 'match_status', 'is_area_incomplete': 'area_complete', 'is_key_col_unresolved': 'key_col_resolved'}`（警告 GT1 の「確かめる列」。[HLD 2.5.3](30_HLD.md#253-利用者向けのメッセージ)の不備ゲートの行の「`merged_summit.xlsx` の確認すべき列」。どれも `_SHEET_COLUMNS` にある列）。
- 内部の状態（モジュールの最上位）: `_config_opt: str = ''`（[main](#mainmatch_summits)の 5 が入れる、[7.5.4](#754-メッセージ文面)の `{config_opt}` の値。`main` を通らない同じプロセスの UT は空のまま使う。[7.2.2](#722-型とデータ)・[7.3.2](#732-型とデータ)・[7.4.2](#742-型とデータ)と同じ）。
- 数の字句は文字列のまま持ち、比べるときに `decimal.Decimal` にする（[7.1.3](#713-関数の細部)の「10 進の数の決まり」、[DEC92](30_HLD.md#494-設計判断)「採番と主ピークの比べ方は 10 進の値で行う」）。
- 型はどれも `@dataclass(frozen=True)` で、項目はこの順に並べる（UT が位置引数で作るため）:
  - `PeakZones(activation, delete)`: どちらも `cmp5_common.ZoneFeature`。1 つのピークの AZ と delete判定ゾーン。
  - `Summit(code, name, alt_m, lat, lon, line_no)`: すべて `str`、`line_no` は `int`。現役のサミット 1 件。`name` は `SummitName`、`alt_m` は `AltM`、`lat`・`lon` は `Latitude`・`Longitude` の字句のまま。`line_no` は CSV の記録の番号（1 行目の基準日の記録を 1 とする。[7.1.3](#713-関数の細部)の `read_merged_peak` の 2 と同じ数え方）。
  - `SummitsList(ref_date, summits, retired_count, retired_codes, region_assocs)`: `ref_date` は `datetime.date`、`summits` は `list[Summit]`（現役。ファイルの順）、`retired_count` は `int`（廃止済みとして除いた `JA` の行の数）、`retired_codes` は `frozenset[str]`（廃止済みの `SummitCode`）、`region_assocs` は `dict[str, frozenset[str]]`（地域コード → その地域コードを持つアソシエーションの集合。`JA` で始まる全行〈廃止済みを含む〉から作る。`_SUMMIT_CODE_RE` に合わない `SummitCode` は入れない）。
  - `Application(action, summit_id, lat, lon, new_elev, applicant, applied_on, years, first_seen, action_text, target_text)`: 登録変更リストの申請 1 件。`action` は `'add'`・`'change'`・`'delete'`。`summit_id` は変更・削除の山岳 ID（追加は `None`）。`lat`・`lon` は追加の位置（変更・削除は `None`）。`new_elev` は変更後の標高から末尾の `m` を除いた字句（変更だけ。ほかは `None`）。`applicant`（空文字がありうる）・`applied_on`（`YYYY-MM-DD`）。`years` は載っている年の表の年の `tuple[int, ...]`（ファイルに現れる順）。`first_seen` は最初に現れた年の表の年と、その表の中の申請の行の通し番号の `tuple[int, int]`。`action_text`・`target_text` は最初に現れた行のアクションの欄と「既存山岳ID もしくは 県名」の欄の、揃えた後の文字列（`match_pending_applications` が知らせる行 `Notice` に使う）。座標・標高・日付の字句は、最初に現れた行のものを残す。
  - `YearUpdate(year, update)`: `year` は `int`、`update` は `YYYY-MM-DD` か空文字。
  - `Notice(kind, reason, year, row, action, target, applicant, applied_on, value)`: 登録変更リストの知らせる行 1 件。`kind` は `'unreadable_row'`・`'unknown_id'`・`'ambiguous_region'`・`'unmatched_add'`・`'unreadable_update'`（`read_updatelist` が作るのは `'unreadable_row'` と `'unreadable_update'`、`match_pending_applications` が作るのは残りの 3 つ）。`row` は年の表の中の申請の行の通し番号（`'unreadable_update'` は `None`）。項目の名前と並びは [HLD 4.9.2](30_HLD.md#492-処理の流れ)の「出力の組み立て」の 3「metadata を作る」の `updatelist_notices` と同じ（[build_metadata](#build_metadata) がそのまま JSON に書く）。
  - `UpdateList(file_name, applications, updates, notices, row_count)`: `file_name` はパスを含まないファイル名、`applications` は `list[Application]`（同じ申請を重ね合わせた後。最初に現れた順）、`updates` は `list[YearUpdate]`（年の表がファイルに現れる順）、`notices` は `list[Notice]`（[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「申請済みの判定」の 7「知らせる行をまとめる」の並び）、`row_count` は `int`（アクションの欄が `追加`・`変更`・`削除` の行の数。重ね合わせの前で、読めない欄のある行も数える。[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「行の分け方と揃え方」が、この 3 つのアクションの行を申請の行と呼ぶのに合わせ、[main](#mainmatch_summits)の結果の要約の「申請の行の数」に使う。通し番号の最大とは違う）。
  - `RegionFeature(assoc, area_code, region_name, geometry)`・`MunicipalityFeature(municipality, code, geometry)`: 項目は `str`、`geometry` は GeoJSON の `geometry` のオブジェクトの `dict`（`json.load` が返した数のまま）。地域は (`assoc`, `area_code`) の順、市区町村は `code` の順に並ぶファイルを、読んだ順のまま持つ（[HLD 4.17.2](30_HLD.md#4172-処理の流れ)）。
  - `Boundaries(regions, municipalities, warnings)`: `regions: list[RegionFeature] | None`・`municipalities: list[MunicipalityFeature] | None`（`None` はファイルが無い印）、`warnings: list[tuple[str, str]]`（無いファイルの警告の記号〈`'BN1'`・`'BN2'`〉と 1 行目の文の組。2 行目は記号で [7.5.4](#754-メッセージ文面)の文を選んで足す。出すのは [main](#mainmatch_summits)）。
  - `SpatialIndex(tree, keys)`: `tree` は `shapely.STRtree`、`keys` は `tree` の位置 `i` のジオメトリの持ち主を指す `list`（ゾーンの索引は Z15 の画素 `tuple[int, int]`、地域と市区町村の索引は `regions`・`municipalities` の並びの位置 `int`）。
  - `SpatialIndexes(activation, delete, regions, municipalities)`: `activation`・`delete` は `SpatialIndex`、`regions`・`municipalities` は `SpatialIndex | None`（地域か市区町村が `None` なら、その索引も `None`）。
  - 突き合わせの結果（Z15 の画素は `tuple[int, int]`）:
    - `AzOverlap(summit, pixels, chosen)`: `summit` は `Summit`、`pixels` は `tuple[tuple[int, int], ...]`（そのサミットを含む AZ のピークの画素。`peaks` の鍵の順）、`chosen` は `tuple[int, int]`（AZ に含めたピークの画素）。2 つ以上のピークの AZ に含まれるサミットの 1 件で、警告 AO2 の材料。
    - `ActivationMatch(summit_peak, peak_summits, peak_status, overlaps)`: `summit_peak` は `dict[str, tuple[int, int]]`（AZ に含まれるサミットの `code` → 含めた AZ のピークの画素。サミットの順）、`peak_summits` は `dict[tuple[int, int], list[Summit]]`（AZ にサミットがあるピークだけ。鍵は `peaks` の鍵の順、値はサミットの順）、`peak_status` は `dict[tuple[int, int], str]`（`peak_summits` と同じ鍵で、値は `'matched'`・`'ambiguous'`）、`overlaps` は `list[AzOverlap]`（サミットの順）。`match_activation_zones` が返す。
    - `DominantPeak(pixel, dist_m)`: `pixel` は `tuple[int, int]`（主ピークの画素）、`dist_m` は `float`（`cmp5_common.great_circle_m` の値のまま。丸めは [7.5.3](#753-関数の細部)の `derive_attributes` が行う）。
    - `DeleteMatch(summit_status, dominant, peak_status, unmatched)`: `summit_status` は `dict[str, str]`（受け取ったサミットの `code` → `'delete'`・`'unmatched'`。受け取った順）、`dominant` は `dict[str, DominantPeak]`（`'delete'` のサミットだけ）、`peak_status` は `dict[tuple[int, int], str]`（AZ にサミットが無いピーク → `'dominant'`・`'new'`。鍵は `peaks` の鍵の順）、`unmatched` は `list[Summit]`（`'unmatched'` のサミット。受け取った順。警告 UM1 の材料）。`match_delete_zones` が返す。
  - 照合の結果:
    - `LocatePoint(kind, key, lat, lon)`: `kind` は `str`（`'peak'`・`'col'`・`'summit'`）、`key` は親のピークの画素 `tuple[int, int]`（`'peak'`・`'col'`）かサミットの `code` `str`（`'summit'`）、`lat`・`lon` は `str`（元の字句。ピークは `peak_lat`・`peak_lon`、コルは `col_lat`・`col_lon`、サミットは `Latitude`・`Longitude`）。
    - `Location(region, municipality)`: `region` は `RegionFeature | None`（どの地域にも入らないか、地域の GeoJSON が無いとき `None`）、`municipality` は `str`（入らないか、市区町村の GeoJSON が無いとき空文字）。
    - `OutsidePoint(point, layers)`: `point` は `LocatePoint`、`layers` は `tuple[str, ...]`（入らなかった層の名前。`'地域'`・`'市区町村'` のこの順の部分列）。警告 RG1 の材料。
    - `RegionMatch(locations, outside)`: `locations` は `dict[tuple[str, object], Location]`（鍵は `(point.kind, point.key)`。点の順）、`outside` は `list[OutsidePoint]`（点の順）。`locate_regions` が返す。
  - 属性の結果:
    - `SotaNames(names, warnings)`: `names` は `dict[str, str]`（`SummitCode` → 山岳名。同じコードに違う山岳名があるものは空文字）、`warnings` は `list[tuple[str, str]]`（警告の記号〈`'SN1'`〜`'SN4'`〉と 1 行目の文の組。`Boundaries.warnings` と同じ形で、2 行目は記号で [7.5.4](#754-メッセージ文面)の文を選んで足す。出すのは [main](#mainmatch_summits)）。`read_sota_names` が返す。
    - `PeakAttrs(points, is_band_change_candidate, category, review_reason, review_group_id, summit_name_jp, rationale)`: `points` は `int | None`、`is_band_change_candidate` は `bool | None`、ほかは `str`。1 つのピークの属性。
    - `SummitAttrs(match_status, sota_points, category, review_reason, review_group_id, summit_name_jp, dominant_peak_code, dominant_peak_dist_m, rationale)`: `match_status` は `str`（`'matched'`・`'ambiguous'`・`'delete'`・`'unmatched'`）、`sota_points` は `int | None`、`dominant_peak_dist_m` は `float | None`、ほかは `str`。1 つのサミットの属性。
    - `ReviewGroup(group_id, pixel, az_codes, held_codes)`: `group_id` は `str`、`pixel` は `tuple[int, int]`（`ambiguous` のピークの画素）、`az_codes`・`held_codes` は `tuple[str, ...]`（AZ の中のサミットの `code` と、そのピークを主ピークに選んだ AZ の外の `delete` のサミットの `code`。どちらも文字列の順）。警告 MR1 の材料。
    - `NullPoints(peaks, summits, band_false)`: `peaks` は `tuple[tuple[int, int], ...]`（`points` が `None` のピークの画素。`peaks` の鍵の順）、`summits` は `tuple[Summit, ...]`（`sota_points` が `None` のサミット。サミットの順。PT1 が `code` と `alt_m` を出すので `Summit` のまま持つ）、`band_false` は `tuple[tuple[int, int], ...]`（`points` か AZ の中のサミットの `sota_points` が `None` で、`is_band_change_candidate` を `False` にした `matched` のピークの画素。`peaks` の鍵の順）。警告 PT1 の材料。
    - `Attributes(peaks, summits, groups, null_points)`: `peaks` は `dict[tuple[int, int], PeakAttrs]`（すべてのピーク。`peaks` の鍵の順）、`summits` は `dict[str, SummitAttrs]`（すべてのサミット。サミットの順）、`groups` は `list[ReviewGroup]`（`group_id` の文字列の順）、`null_points` は `NullPoints`。`derive_attributes` が返す。
  - 申請済みの判定の結果:
    - `PendingRow(applications, match, note)`: `applications` は `tuple[dict, ...]`（[DEC189](30_HLD.md#494-設計判断)「申請の情報は申請ごとの配列で持つ」の配列の要素。並びは `match_pending_applications` の 5）、`match` は `str`（`'same'`・`'different'`・`''`）、`note` は `str`。1 つの行の申請の値。
    - `Pending(rows, notices, taken)`: `rows` は `dict[tuple[str, object], PendingRow]`（行の鍵 → 値。申請が 1 つ以上当たった行だけ。鍵は `('peak', 画素)` を `peaks` の鍵の順、続けて `('summit', code)` をサミットの順）、`notices` は `list[Notice]`（[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「申請済みの判定」の 7「知らせる行をまとめる」の並び）、`taken` は `int`（取り込んだ申請の数。[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「登録変更リストの読み方」の「取り込む申請」〈追加、削除、バンドをまたぐ変更〉の選別を通った申請の数で、数え方は [match_pending_applications](#match_pending_applications) の「取り込んだ申請の数」）。結果の要約の「取り込んだ申請の数」（[7.5.4](#754-メッセージ文面)の SM3）に使う。`match_pending_applications` が返す。
  - 組み立ての結果（4 回目）:
    - `Metadata(items, warnings)`: `items` は `dict`（`merged_summit.geojson` の `metadata` のオブジェクト。値は `str`・`list`・`dict`・`int`・`None`）、`warnings` は `list[tuple[str, str]]`（警告の記号〈`'MT1'`・`'MT2'`〉と 1 行目の文の組。`SotaNames.warnings` と同じ形で、2 行目は記号で [7.5.4](#754-メッセージ文面)の文を選んで足す。出すのは [main](#mainmatch_summits)）。`build_metadata` が返す。
    - `SummitFeatures(features, text)`: `features` は `list[dict]`（Feature の `dict` を出力の順に並べたもの。数は `cmp5_common.JsonNumber`・`int`・`float`、真偽は `bool`、空欄は `None`）、`text` は `str`（`merged_summit.geojson` の中身の全体。[write_summit_outputs](#write_summit_outputs)がこのまま書く）。`build_summit_features` が返す。
  - 起動の引数: `_Args(config)`（内部）: `config: str`（`--config` の値のまま。`--config` は必須なので `None` は持たない。[7.2.2](#722-型とデータ)の `_Args` と同じ形）。
- `slots=True` は付けない（[7.1](#71-cmp5_common)〜[7.4](#74-check_cols)と同じく、メモリの実測〈HLD 5.2.2 の「実測の計画」の 4〉の後に決める）。

#### 7.5.3 関数の細部

関数ごとに `#####` の見出し（関数の名前だけ）を立てて書く。内部の関数は、使う関数の見出しの下に書く。HLD 3.5.3 の表の「呼ぶ順」で並べる。

**止まり方**: 7.5 の関数は、誤りを見つけたら、[7.5.4](#754-メッセージ文面)のメッセージを `common.log_error(<1 行目>, <2 行目>)` で出してから `sys.exit(common.EXIT_ERROR)` で止まる（[7.2.3](#723-関数の細部)の「止まり方」と同じ）。7.5 の関数は、`main` を除いて、`InputError` を上げる 7.1 の部品を呼ばない（`is_valid_coord` は上げない）ので、`cmp5_common.InputError` を捕まえない。属性と申請済みの判定の 5 関数（`read_sota_names`・`derive_attributes`・`build_rationale`・`match_pending_applications`・`build_pending_note`）は、誤りを見つけても止まらず、不備は警告の材料として返り値に並べる。組み立ての `build_metadata`・`build_summit_features` も止まらない（`build_metadata` は不備を `Metadata.warnings` に並べる。`build_summit_features` の内部の関数 `_encode_json` が対応しない型で上げる `TypeError` はプログラムの誤りで、捕まえない）。`build_summit_sheets` は、結べない行と取り元のプロパティの欠けを `XS1`、値を変えずに書けない文字列を `XS2` で、すべての行を見てから止まる（書き出しの前に止まる）。`write_summit_outputs` は、書き込みの失敗で SW1 か SW2 を出して止まる（置いた出力を消してから止まる）。`check_defect_gate` は止まらず、当たった条件を返すだけで、終了コード 4 は `main` が決める。`read_merged_peak`・`index_peaks_by_pixel`・`read_zone_features` を呼び、その `InputError` を捕まえて止まるのは [main](#mainmatch_summits)（案内の文を選ぶ内部の関数 `_input_error_advice` は、1 回目の `match_zones_to_peaks` の下に書いてある）。

**{reason}・{path}**: [2.1.4](#214-メッセージ文面)と同じ（`OSError` の `strerror`、無ければ `str(e)`。`UnicodeDecodeError` なら `UTF-8 として読めない`）。`{path}` は `os.path.abspath` したパス。

**5.2・5.3 の受け方**: 7.5 の前置きに書いた。

**10 進の数と整数**: [7.1.3](#713-関数の細部)の「10 進の数の決まり」の判定を、7.1 の内部の関数に頼らず、7.5 の内部の関数で持つ（7.1 の内部の関数はほかのモジュールから呼べない〈[1.2](#12-lld-の規約)〉）。座標が読めるかは `cmp5_common.is_valid_coord` で確かめる。`AltM` の整数は `_INTEGER_RE.fullmatch(s)` が合うこと。

##### match_zones_to_peaks

`match_zones_to_peaks(peaks: dict[tuple[int, int], cmp5_common.MergedPeakRow], zones: list[cmp5_common.ZoneFeature], path: str) -> dict[tuple[int, int], PeakZones]`

`path` は `merged_peak.geojson` の絶対パスで、MZ1 の `{path}` にだけ使う（[HLD 3.5.3](30_HLD.md#353-関数)の表の受け取るものに無いが、止まるときのメッセージに要る。処理は変えない）。`peaks` は `index_peaks_by_pixel` の返すピークの表、`zones` は `read_zone_features` の返すゾーンである（[HLD 4.9.2](30_HLD.md#492-処理の流れ)の 2「`merged_peak.geojson` を読む」）。

1. `zones` を順に見て、`(zone.pixel, zone.kind)` を鍵に、AZ（`cmp5_common.ACTIVATION_ZONE`）と delete判定ゾーン（`cmp5_common.DELETE_ZONE`）を入れる表を作る。同じ画素の同じ種類が 2 つ以上来ることは、`read_zone_features` が ZF4 で止めているので、ここでは確かめない（1 つのファイルの中の重なりは ZF4 が、表との食い違いはここが受け持つ。[DEC87](30_HLD.md#494-設計判断)「ゾーンは Z15 の画素でピークに突き合わせる」）。
2. 食い違いを、止める前にすべて集める。
   - 表に無いピークのゾーン: `zone.pixel` が `peaks` に無いゾーンを、`zones` の順（`index` の順）に集める。
   - ゾーンの欠けたピーク: `peaks` の鍵の順（`merged_peak.csv` の行の順）に、AZ と delete判定ゾーンのうち 1 の表に無いものを、AZ・delete判定ゾーンの順に集める。
3. 2 で 1 つでも集まれば、MZ1 を出して止まる。`{list}` は、表に無いピークのゾーンを先に、欠けたピークを後に、`、` でつなぐ。緯度経度の字句は、表に無いピークのゾーンは `zone.properties['peak_lat']`・`['peak_lon']` の `JsonNumber.text`、欠けたピークは `peaks[key].values['peak_lat']`・`['peak_lon']`。
4. 無ければ、`peaks` の鍵の順に `PeakZones(activation, delete)` を入れた辞書を返す。`peaks` が空で `zones` も空なら、空の辞書を返す（0 行でも続ける。[HLD 4.9.2](30_HLD.md#492-処理の流れ)の 1「`merged_peak.csv` を読む」）。`peaks` が空で `zones` が空でなければ、すべてのゾーンが「表に無いピークのゾーン」になって MZ1 で止まる。

`_input_error_advice(symbol: str) -> str`（内部）: 7.1 の `InputError` の `symbol`（`'MP1'`〜`'MP3'`・`'ZF1'`〜`'ZF4'`）に対する 2 行目の文を返す。どれも [7.5.4](#754-メッセージ文面)の `{redo}`（フェーズ2 から通しでやり直す）を返す（[HLD 4.9.3](30_HLD.md#493-異常系)の「やり直しの案内」の 1 つ目。起動の形で分かれないので、[7.4.3](#743-関数の細部)の `_redo` と違い `symbol` だけを受け取る）。それ以外の `symbol` は `ValueError` を上げる（呼ぶ側の誤り）。`_config_opt` を読む。MZ1 の 2 行目は `_input_error_advice` を呼ばず、`{redo}` の文をそのまま使う（MZ1 は 7.1 の `symbol` でないので、渡すと `ValueError` になる）。

##### read_summits_list

`read_summits_list(path: str) -> SummitsList`

[HLD 4.9.2](30_HLD.md#492-処理の流れ)の 3「SOTA サミットリスト CSV と登録変更リストを読む」のうち、SOTA サミットリスト CSV の部分である（[DEC88](30_HLD.md#494-設計判断)「サミットリスト CSV の JA の行の誤りで止める」、[ADR-SRS-054](decisions/ADR-SRS-054-summitslist-validto-reference-date.md)）。

1. `abspath = os.path.abspath(path)`。`os.path.exists(abspath)` が偽なら SS1。`open(abspath, encoding='utf-8-sig', newline='')` を `with` で開き（`OSError` は SS2。ディレクトリも SS2）、`csv.reader(f, strict=True)` で読む。
   - 先頭の BOM（U+FEFF）を 1 つだけ除く（[HLD 4.9.1](30_HLD.md#491-目的と範囲)の対象外の「CSV の引用符と BOM」。利用者が表計算のソフトで保存し直しうるため。[7.2.3](#723-関数の細部)の `read_land_peaks` と同じ）。
   - 読む途中の `UnicodeDecodeError` と `OSError` は SS2、`csv.Error` は SS3（`{detail}` は `{line_no} 行目を CSV として読めない: {reason}`。`{reason}` は `str(e)`）。記録を 1 つずつ読みながら確かめるので、SS3 と SS4 は、ファイルの順で先に見つけた方で止まる（値の誤りの行より後に CSV として読めない行があっても SS4）。
   - `line_no` の数え方は [7.1.3](#713-関数の細部)の `read_merged_peak` の 2 と同じ（各記録を読み始める前に 1 つ増やす。空の記録も数える）。
2. 1 行目（最初の記録）。記録が 1 つも無ければ SS3（`基準日の行が無い`）。最初の欄が `_SUMMITS_DATE_RE` に合わなければ SS3（`1 行目が SOTA Summits List (Date=DD/MM/YYYY) の形でない: {line}`。`{line}` は最初の欄）。合っても `datetime.date(年, 月, 日)` が作れなければ SS3（`基準日が暦に無い: {line}`）。2 つ目からの欄は見ない（表計算のソフトで保存し直すと、空の欄が続きうるため）。
3. 2 行目（見出し）。2 つ目の記録が無ければ SS3（`見出しの行が無い`）。`_SUMMITS_COLUMNS` の名前ごとに、見出しの記録の中で最初に `==` になる位置を引く。無い名前があれば、`_SUMMITS_COLUMNS` の順で最初のものを SS3（`見出しに列 {name} が無い`）。
4. 3 行目からのデータの記録。空の記録（空行）は飛ばす。`SummitCode` の位置の欄が `JA` で始まる記録だけを確かめる（欄が `SummitCode` の位置まで無い記録、`JA` で始まらない記録は確かめない。`JA` で始まらない行の誤りでは止めない。[SRS §7.2.4](20_SRS.md#724-sota-サミットリスト-csv)）。`JA` で始まる記録は、次の順に見て、ファイルの順で最初に外れたもので、その場で SS4 を出して止まる（`{detail}` は次の文）。
   - 欄の数が、使う 6 列の位置の最大 + 1 より少ない: `{line_no} 行目の欄が足りない: 使う列は {need} 欄目まで、この行は {have} 欄`（`{need}` は最大の位置 + 1、`{have}` は欄の数。使わない列だけが欠ける記録は止めない）。
   - `Latitude` が `cmp5_common.is_valid_coord(値, 'lat')` で偽: `{line_no} 行目の Latitude が 座標として読めない: {value}`。`Longitude` も同じ（`'lon'`）。値の前後の空白は除かない（`' 34.5'` は座標として読めない。写し違いを黙って直さないため。[7.2.3](#723-関数の細部)の `read_land_peaks` と同じ。[HLD 4.9.2](30_HLD.md#492-処理の流れ)の 3 が「[4.8.2](30_HLD.md#482-処理の流れ)の 1『リストを読む』の意味で座標として読めない」で止めるため）。
   - `AltM` が `_INTEGER_RE` に合わない: `{line_no} 行目の AltM が 整数として読めない: {value}`。
   - `ValidTo` が `_DMY_RE` に合わないか、`datetime.date(年, 月, 日)` が作れない: `{line_no} 行目の ValidTo が DD/MM/YYYY の日付として読めない: {value}`。
5. 4 を通った記録について、`SummitCode` ごとに記録の番号を集める。すべての記録を読み終えてから、同じ `SummitCode` が 2 つ以上あるものがあれば、SS5 を出して止まる。`{list}` は、最初に現れた順に、`{code}（{line_no}、{line_no} 行目）` を `、` でつなぐ（4 で止まらなかったときだけ、ここに来る。廃止済みの行も数える。同じ `SummitCode` のどれを採るかの規則は設けない。[SRS §7.2.4](20_SRS.md#724-sota-サミットリスト-csv)の正常入力の前提）。
6. 4 を通った記録（`JA` で始まる記録だけ。`JA` で始まらない記録は、`summits`・`retired_count`・`retired_codes` に入れない）のうち、`ValidTo` の日付が基準日以降の記録を現役とし（基準日と同じ日は現役。`>=`）、`Summit(code, name, alt_m, lat, lon, line_no)` をファイルの順に並べる。基準日より前の記録は廃止済みとし、`retired_count` に数え、`SummitCode` を `retired_codes` に入れる。`JA` で始まる全記録（廃止済みを含む）について、`_SUMMIT_CODE_RE.fullmatch(SummitCode)` が合えば、2 つ目の組（地域コード）をキーに、1 つ目の組（アソシエーション）を `region_assocs` に足す（合わない記録は入れるだけで止めない。[HLD 4.9.2](30_HLD.md#492-処理の流れ)の 3 の止まる条件に無いため）。`SummitsList(ref_date, summits, retired_count, retired_codes, region_assocs)` を返す。

##### find_updatelist

`find_updatelist(ref_dir: str) -> str`

[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「登録変更リストの読み方」の「ファイルの選び方」である（[DEC188](30_HLD.md#494-設計判断)「登録変更リストのファイル名は ASCII の年だけ」）。

1. `abspath = os.path.abspath(ref_dir)`。`os.listdir(abspath)` の名前のうち、`_UPDATELIST_RE.fullmatch(名前)` が合い、`os.path.isfile(os.path.join(abspath, 名前))` が真のものを集める（ディレクトリや、名前の全体が合わないもの〈`.bak` を足したもの、全角の数字、4 桁でない年〉は採らない）。`os.listdir` が `OSError` になるときは、集まらなかったものとして扱う。
2. 1 つも集まらなければ UX1 を出して止まる（`{dir}` は `abspath`）。
3. 集まったものの年（4 桁の数を `int` にしたもの）が最大のものの絶対パスを返す（同じ年は 1 つしか無い）。

##### read_updatelist

`read_updatelist(path: str) -> UpdateList`

[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「登録変更リストの読み方」の、構文の検査と正規化までを行い、申請の並びを作る（バンドの比べによる変更の選別は [match_pending_applications](#match_pending_applications)）。実物の形は、2026-10-19 と 2026-11-01 に確かめたもの（UTF-8、外部の DTD の宣言だけで内部サブセットと実体の宣言は無い、`table` は 1 つ、`<br/>` は無い、年の表は新しい年から 3 つ、題の行は「`2026年`」と「`山岳データ登録変更リスト`」が別々のセル、見出しの 2 行だけが `rowspan`・`colspan` を持つ、反映済みの目印の行はアクションの欄が空）に合わせてある。

1. **読む**: `abspath = os.path.abspath(path)`。`open(abspath, 'rb')` で全体をバイト列で読む（`OSError` は UX2。無いファイルとディレクトリも UX2）。
   - 実体と内部サブセットの検査は、バイト列の検索でなく、`xml.parsers.expat.ParserCreate()` の読みで行う（バイト列の `b'<!ENTITY'` や DOCTYPE の正規表現では、UTF-16 の文書の宣言を見つけられず、`ET.fromstring` が内部実体を展開してしまう。expat は符号化の宣言と BOM で読むので、符号化によらず当たる）。`parser.StartDoctypeDeclHandler` に、4 つ目の引数 `has_internal_subset` が真なら内部の例外 `_UnsafeXml('内部サブセットがある')` を上げる関数を、`parser.EntityDeclHandler` に、呼ばれたら `_UnsafeXml('実体の宣言がある')` を上げる関数を設定し、`parser.Parse(data, True)` を呼ぶ。内部サブセットが無ければ実体の宣言は来ないので、後者は通常は呼ばれない（念のための検査）。`_UnsafeXml`（`Exception` の子の内部の例外）は UX3（`{detail}` は例外の文）、`xml.parsers.expat.ExpatError` も UX3（`{detail}` は `str(e)`）。外部の DTD と外部の実体は、expat も `xml.etree.ElementTree` も取りに行かない（DOCTYPE が外部の DTD だけを指すのは通る。実物がその形）。
   - 通ったら、`root = ET.fromstring(data)` で木にする。`ET.ParseError` は UX3（`{detail}` は `str(e)`）。外部の DTD を取りに行かないので、名前付きの文字参照（`&nbsp;` など）は、expat の読みは通っても、ここで `undefined entity` として ParseError になる（[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「読み方」。2026 年版の実物には無い）。
2. **表と行**: 名前空間を除いた局所名（`tag` の最後の `}` より後ろ）で要素を見る。`root.iter()` で最初の `table` を探し、無ければ UX4（`{detail}` は `表が無い`）。`tr` は、`table` の直下の `tr` と、`table` の直下の `thead`・`tbody`・`tfoot` の直下の `tr` を、文書の順に集める（入れ子の表は見ない。[SRS §7.2.9](20_SRS.md#729-山岳データ登録変更リスト)の「表が 1 つ」）。`tr` の直下の `td`・`th` をセルとする。
3. **セルの文字**: セルの中の文字を文書の順につなぐ（局所名が `br` の要素は空白 1 つとして読む。`JA1ABC<br/>2026/10/19` が `JA1ABC2026/10/19` にならないように）。つないだ文字を `unicodedata.normalize('NFKC', …)` で揃え、空白の並び（`str.split()` の区切り）を 1 つの半角の空白にして前後を除く（内部の関数 `_norm`）。全角の数字・英字・`，`・全角の空白・`／` が半角になる。`、` は NFKC で変わらないので、座標の区切りは別に扱う（7）。見出しは、さらに空白をすべて除いてから比べる。
4. **格子**: `rowspan`・`colspan` は `_SPAN_RE.fullmatch` に合えばその数、無いか合わなければ 1。行ごとに、上の行から延びている `rowspan` の列を飛ばしながらセルを置き、`colspan` の列にはその文字を写し、`rowspan` が 2 以上なら下の行の同じ列にも写す（[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「格子への展開」。`変更後`〈`colspan=3`〉の下の 2 行目の `標高m` を、上の行の文字との組で引くために、結合したセルが覆う位置へ文字を写す）。格子は、最初の題の行（5）から表の終わりまで作る。最初の題の行より前の行は申請として読まない（5）ので、展開せず、下の 2 つの検査も掛けない（前書きの体裁が変わっても止めない）。HLD は格子の次の 2 つの異常を決めていないので、ここで決める（実物には無い）。どちらも格子を作れず、見出しの文字で列を引けないので、[HLD 4.9.3](30_HLD.md#493-異常系)の「使う列を見出しの文字で特定できない」に当たるものとして、`read_updatelist` の他の構造の誤りと同じく UX4 で止める。
   - 上限: 合った数が `_SPAN_MAX` を超えるときは、格子を作る前に UX4（`{detail}` は `rowspan か colspan の値が {max} を超える: {value}`。`{max}` は `_SPAN_MAX`、`{value}` は合った文字列）。大きな値で格子の展開が時間と記憶を使い切らないための歯止め。
   - 重なり: セルの `colspan` が覆う列に、上の行から延びている `rowspan` の文字が既にあるときは、UX4（`{detail}` は `セルが重なる`）。
   - 題の行・Update の行・見出しの行（5）かどうかは、その行自身のセルの文字だけで決める（上から延びてきた文字は見ない）。申請の行の値（6）と見出しの列を引く文字（5 の「列」）は、格子の文字で読む。題の行なら、上から延びている `rowspan` を捨ててから、その行のセルを置く（年の表をまたいで写さない。実物は見出しの行にしか `rowspan` が無いので、効くのは書式が変わったときだけ）。
   - 反映済みの目印の行（ADR-SRS-086 の Context の「ここまでは…反映済」）と題の行・Update の行は、実物ではアクションの欄（列 0）が空なので、6 の「アクションの欄が空の行は読み飛ばす」で扱う（目印の行のための別の決まりは置かない）。
   - 見出しの `rowspan=2` を写すので、見出しの 2 行目のアクションの欄も `アクション` になる。見出しの 2 行は 5 で見出しとして扱い、申請の行にしない。
5. **年の表と見出し**: 行を上から見て、次の順に年の表を切る。最初の題の行の前の行は、申請として読まない（4 のとおり、格子に展開せず、上限と重なりの検査も掛けない）。題の行が 1 つも無ければ UX4（`年の表の題の行が無い`）。
   - 題の行: その行のセルのうち、`_TITLE_YEAR_RE.fullmatch` に合うセルと、空白を除くと `_TITLE_TEXT` に等しいセルの両方がある行。または、1 つのセルが `_TITLE_FULL_RE.fullmatch` に合う行。年は `int` にする。`fullmatch` にして年の後の語まで見るので、実物の備考の `2022年分再申請` のような申請の行の文は題の行にならない。
   - Update の行: 題の行の後、見出しの行より前で、`Update` に等しいセルと、`_UPDATE_DATE_RE.fullmatch` に合い `datetime.date.fromisoformat` で読めるセルの両方がある最初の行。その日付を `YearUpdate(年, 日付)` にする。無ければ `YearUpdate(年, '')` にし、その年の表の知らせる行の先頭に `unreadable_update`（`reason` は `_REASON_UPDATE`、`row` は `None`、`year` はその年、ほかの文字列は空文字）を足す。
   - 見出し: 題の行の後で最初に、空白を除くと `アクション` に等しいセルを持つ行と、その次の行の 2 行。年の表の見出しの行が無い（次の題の行か表の終わりが先に来る、または 2 行目が無い。`アクション` のセルを持つ行が無いのも同じ）ときは UX4（`{year} 年の表に見出しの行（アクション のセルを持つ行）が無い`）。
   - 列: 見出しの上の行と下の行の文字（空白を除く）の組で引く。`アクション` は上が `アクション`、山岳 ID か県名は上が `既存山岳IDもしくは県名`、変更後の標高は上が `変更後` で下が `標高m`、位置は上が `新規追加詳細` で下が `位置`、申請者・申請日は上が `申請者・申請日`。同じ条件に合う列が複数あれば最初の列。年の表ごとに引き、引けない列があれば、この順で最初のものを UX4（`{year} 年の表の見出しで {name} の列を特定できない`。`{name}` は `アクション`・`既存山岳ID もしくは 県名`・`変更後の標高`・`位置`・`申請者・申請日`）。見出しはあるが申請の行が 0 の年の表は止めない。
6. **申請の行**: 見出しの 2 行の後、次の題の行（または表の終わり）までの行。[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「年の表と Update の日付」のとおり、見出しの後のすべての行に、年の表ごとに 1 から通し番号を付ける（アクションの欄が空で読み飛ばす行も数える。利用者がページの元の行を数えて探せるように）。アクションの欄（`_norm` した文字）が空の行は、読み飛ばす。ほかの行は次の順に扱う。
   1. 申請者と申請日: 申請者・申請日の欄を `_APPLIED_RE.search` する。最初の一致があり、`datetime.date(年, 月, 日)` が作れれば、申請日は `YYYY-MM-DD`（月と日は 2 桁にそろえる）、申請者は `_norm(欄[:一致の始め] + ' ' + 欄[一致の終わり:])`（一致の部分を除いた残り。分割はしない）。一致が無いか暦に無ければ、申請日は空文字、申請者は欄の文字全体。知らせる行の `applicant`・`applied_on` に使うので、どの読めない理由のときも先に求めておく。
   2. アクションの欄が `_ACTIONS` のどれでもなければ `unreadable_row`（`reason` は `_REASON_ACTION`、`value` はアクションの欄、`year`・`row` はその行、`action` はアクションの欄、`target` は「既存山岳ID もしくは 県名」の欄、`applicant`・`applied_on` は 1 の値）。この行は `row_count` に数えない。
   3. `row_count` を 1 増やす。アクションが `変更` で、変更後の標高の欄が空なら、ほかの欄を読まずに、この行を取り込まず知らせない（[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「取り込む申請」は、読み込みの時点で決めるのを変更後の標高の欄が空の変更までとし、[SRS §7.2.9](20_SRS.md#729-山岳データ登録変更リスト)も名称・座標だけの変更を取り込まない行とする。山岳 ID や申請日が読めなくても知らせない）。
   4. 欄の読み。読めない欄があれば、次の順で最初のものを `reason` と `value` にして `unreadable_row` を作る（1 行 1 件。項目は 2 と同じ）。
      - 追加の位置: `re.split(r'[,、 ]+', 欄)` の空でない部分が、ちょうど 2 つで、1 つ目が `is_valid_coord(…, 'lat')`、2 つ目が `is_valid_coord(…, 'lon')` を通ること。ほかは `_REASON_POSITION`（`value` は位置の欄）。
      - 変更・削除の山岳 ID: 「既存山岳ID もしくは 県名」の欄が `_SUMMIT_ID_RE.fullmatch` に合うこと。ほかは `_REASON_ID`（`value` はその欄）。
      - 変更後の標高（変更だけ。空の行は 2 で除いてある）: 欄の末尾の `m` を 1 つ除き、前後の空白を除いたものが `_ELEV_RE.fullmatch` に合うこと。ほかは `_REASON_ELEV`（`value` は標高の欄）。
      - 申請日: 3 で申請日が空文字なら `_REASON_DATE`（`value` は申請者・申請日の欄）。
   5. 読めない欄が無ければ、`Application` を作る（`action` は `_ACTIONS` の値、追加は `lat`・`lon` に位置の 2 つの字句、変更・削除は `summit_id` に山岳 ID、変更は `new_elev` に標高から末尾の `m` を除いた字句、`years` は `(年,)`、`first_seen` は `(年, 通し番号)`、`action_text`・`target_text` はこの行の欄の文字）。
7. **重ね合わせ**: 鍵は (`action`、`summit_id` か (`Decimal(lat)`, `Decimal(lon)`)、`Decimal(new_elev)` か `None`、`applicant`、`applied_on`)。同じ鍵の 2 つ目からは、先の `Application` の `years` に年を足すだけにする（先の字句を残す。frozen なので `years` を足した新しい `Application` に置き換える）。その年がすでに `years` にあるとき（同じ年の表に同じ申請が 2 度出たとき）は足さない。座標と標高は 10 進の値で比べる（`35.10` と `35.1` は同じ。[DEC104](30_HLD.md#494-設計判断)「入力から来る数は 10 進の値を変えずに書く」の値の同じさ）。`applications` は、最初に現れた順に並べる。
8. **知らせる行の並び**: 年の表がファイルに現れる順に、その年の表の中では `unreadable_update` を先に、`unreadable_row` を通し番号の順に並べる（[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「申請済みの判定」の 7「知らせる行をまとめる」）。
9. `UpdateList(os.path.basename(abspath), applications, updates, notices, row_count)` を返す。

##### read_boundaries

`read_boundaries(regions_path: str, municipalities_path: str) -> Boundaries`

[HLD 4.9.2](30_HLD.md#492-処理の流れ)の 4「地域と市区町村の GeoJSON を読み、索引を作る」のうち、読む部分である（索引は `build_spatial_indexes`）。地域、市区町村の順に同じ手順で読む（`{target}` は `地域`・`市区町村`）。

1. `os.path.exists(abspath)` が偽なら、そのファイルは `None` にし、`warnings` に BN1（地域）か BN2（市区町村）の記号と 1 行目の組を足す（[HLD 4.9.3](30_HLD.md#493-異常系)の「必ず含める内容」の「無いファイルのパスと、…」。止めない）。
2. ある: `open(abspath, encoding='utf-8')` と `json.load(f, parse_constant=_reject_constant)` で読む（`_reject_constant(token)` は内部の関数で、`ValueError(f'{token} は JSON の数でない')` を上げる。[3.1.3](#313-関数の細部)と同じ）。`OSError`・`UnicodeDecodeError`・`ValueError`（`json.JSONDecodeError` を含む）・`RecursionError` は BD1。
3. 書式の検査。最初に外れたもので BD2（`{detail}` は次の文）。最上位を確かめた後、`features` の要素ごとに（1 から数える）、次の 3 つをこの順に確かめ、最初に外れた要素の最初に外れたもので止まる。
   - 最上位が `dict` で `type` が `FeatureCollection`、`features` が `list` であること: `FeatureCollection でない`。
   - `properties` が `dict` で、地域なら `assoc`・`area_code`・`region_name`、市区町村なら `municipality`・`code` が、すべて `str` であること: `{n} 番目の Feature の properties に {name} が無いか文字列でない`。要素が `dict` でない、または `properties` が `dict` でないときは、`{name}` を必須の名前の最初のもの（地域は `assoc`、市区町村は `municipality`）にする。
   - `geometry` が `dict` で `type` が `Polygon` か `MultiPolygon` であること: `{n} 番目の Feature の geometry が Polygon でも MultiPolygon でもない`。要素が `dict` でない、または `geometry` が無いときも同じ文。
   - `_to_shape(geometry)`（`build_spatial_indexes` の内部の関数）で形を作れること。作れなければ（`ValueError`・`TypeError`・`KeyError`・`shapely.errors.ShapelyError`。座標が文字列のときは `ValueError`、`coordinates` が無いときは `KeyError`、座標が有限でないとき〈`1e999` など〉は `ValueError`〈`座標が有限の数でない`〉。`{reason}` は `str(e)`）: `{n} 番目の Feature の geometry を作れない: {reason}`。作った形は捨てる（索引は `build_spatial_indexes` が作る。形を作る手間が 2 度かかるが、座標の誤りを書式の誤りとして 4.9.3 の表の「書式が違う」で止めるため。形を直さない）。
4. `RegionFeature`・`MunicipalityFeature` を、ファイルの順に並べる（並びは確かめない。CMP1〔行政区域前処理〕が (`assoc`, `area_code`) と `code` の順に書く。[HLD 4.17.2](30_HLD.md#4172-処理の流れ)）。0 件でもよい（空の `list`）。
5. `Boundaries(regions, municipalities, warnings)` を返す。

##### build_spatial_indexes

`build_spatial_indexes(peak_zones: dict[tuple[int, int], PeakZones], boundaries: Boundaries) -> SpatialIndexes`

[HLD 4.9.2](30_HLD.md#492-処理の流れ)の 4「地域と市区町村の GeoJSON を読み、索引を作る」の索引の部分である（[DEC94](30_HLD.md#494-設計判断)「ゾーンと地域は空間索引で引く」。[ADR-SRS-008](decisions/ADR-SRS-008-dominant-peak-identification.md)の空間インデックス）。

1. `_to_shape(geometry: dict) -> shapely.Geometry`（内部）: `{'type': geometry['type'], 'coordinates': _plain(geometry['coordinates'])}` を `shapely.geometry.shape` に渡して返す。`_plain` は、`list` の要素を再帰して、`cmp5_common.JsonNumber` を `float(n.text)` に替え、`int`・`float` はそのままにする（ゾーンの座標は `JsonNumber`、地域と市区町村の座標は `json.load` の数）。替えた数と `int`・`float` が有限でなければ（`math.isfinite` が偽。`1e999` は `float` で無限大になる）、`ValueError('座標が有限の数でない')` を上げる（無限大のまま形を作ると、`shapely` は例外を上げずに（実測: `inf`・`nan` を含む環は `is_valid` が偽の形になる）、不正な形で内外を判定してしまう。7.1 の `read_zone_features` は座標を `JsonNumber` であることだけ見て有限性を見ないので、ここで見る）。形を直さない（`make_valid` などを呼ばない。[HLD 4.9.2](30_HLD.md#492-処理の流れ)の 2 の「形を変える修正をしない」）。ゾーンの形を作れないときは、例外のまま伝える。ゾーンは `merge_zones` が書く内部の中間ファイル（[SRS §8.1](20_SRS.md#81-内部データ一覧)）で、手で書き直す入力ではない。JSON として読めないことや、型・位置の形・種類の誤りは 7.1 の `read_zone_features` が [HLD 4.9.3](30_HLD.md#493-異常系)の「書式が違う」の行で止めているので、ここまで来て形を作れないのは、`merge_zones` か 7.1 の欠陥である（作れないときの行が HLD の表に無いのは、このため）。
2. AZ と delete判定ゾーンの索引: `peak_zones` の鍵の順に、`_to_shape(zones.activation.geometry)`・`_to_shape(zones.delete.geometry)` を並べ、`shapely.STRtree` にする。`keys` は `peak_zones` の鍵の順の Z15 の画素。
3. 地域と市区町村の索引: `boundaries.regions`・`boundaries.municipalities` が `None` でなければ、`_to_shape(feature.geometry)` の並びを `shapely.STRtree` にする。`keys` は並びの位置（0 から）。`None` なら、その索引も `None`。
4. `SpatialIndexes(activation, delete, regions, municipalities)` を返す。
5. メモリ（[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「メモリ」。実測は [HLD 5.2.2](30_HLD.md#522-処理の流れ)の「実測の計画」の 4「CMP5 の突合」）: `build_summit_features` が写すために `ZoneFeature.geometry`（`JsonNumber` の `dict`）も持ち続けるので、ゾーンのジオメトリは、`dict` と `shapely` の形の 2 つの形で持つ。

##### is_in_zone

`is_in_zone(lat: float, lon: float, zone: shapely.Geometry) -> bool`

[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「ゾーンの内外」である（[DEC86](30_HLD.md#494-設計判断)「ゾーンの内外は Z15 の画素の中心で判定する」）。`lat`・`lon` は、呼ぶ側が `cmp5_common.is_valid_coord` を通した字句を `float` にした値（範囲の中なので `cmp5_common.latlon_to_z15_pixel` を安全に呼べる）。`zone` は `build_spatial_indexes` が作った `shapely` の形（Polygon か MultiPolygon）。

1. `pixel = cmp5_common.latlon_to_z15_pixel(lat, lon)`（点が入る全球の Z15 の画素 (gx, gy)）。
2. `center_lat, center_lon = z15_pixel_center_latlon(pixel)`（その画素の中心）。
3. `bool(shapely.contains_xy(zone, center_lon, center_lat))` を返す（`x` が経度、`y` が緯度。引数の順に注意。`contains_xy` は numpy の真偽値を返すので、Python の `bool` にして返す）。元の `lat`・`lon` を形に当てない。

- 画素の中心は画素の内側にあって輪郭の線の上に乗らない（ゾーンは塗った画素の境界をたどる形で、画素の境目は輪郭の線の上にしか無い）ので、輪郭の上を外とする `contains` と内とする `covers` は同じ結果になる。ここでは `contains_xy` を使う。
- 元の点がゾーンの輪郭の線の上にあっても、見るのは画素の中心なので、結果はその画素が塗られているかだけで決まる。経度が画素の西端にちょうど乗る点は、東の画素（画素の座標が 1 大きい方）に入る（[2.4](#24-言語ごとに別に実装する式のテストベクトル)の `latlon_to_tile` の `floor`。画素の経度の境目は `gx / 2²³ × 360 − 180` で丸めが無い）。

##### z15_pixel_center_latlon（match_summits）

`z15_pixel_center_latlon(pixel: tuple[int, int]) -> tuple[float, float]`

[2.4](#24-言語ごとに別に実装する式のテストベクトル)の計算の決まりの `z15_pixel_center_latlon` のとおり、式を書いた順に左から計算する（[7.2.3](#723-関数の細部)の `latlon_to_mesh` と同じ形で、7.5 の中に式を写す。`tile_to_latlon` は [3.1](#31-preprocess_boundaries) の関数で、[1.2](#12-lld-の規約)により 7.5 からは呼べない）。返すのは（緯度, 経度）の順。

```python
gx, gy = pixel
n = float(2 ** 23)
x = gx + 0.5
y = gy + 0.5
lon = ((x / n) * 360) - 180
lat = (math.atan(math.sinh(math.pi * (1 - (2 * y) / n))) * 180) / math.pi
return (lat, lon)
```

引数を確かめない。呼ぶのは `is_in_zone` と内部の関数 `_zones_containing` だけで、どちらが渡すのも `cmp5_common.latlon_to_z15_pixel` が返した画素である。期待値は [2.4](#24-言語ごとに別に実装する式のテストベクトル)の表 7 で、経度は `==`、緯度は差の絶対値が `1e-12` 度以下で比べる。

##### match_activation_zones

`match_activation_zones(summits: list[Summit], peaks: dict[tuple[int, int], cmp5_common.MergedPeakRow], index: SpatialIndex) -> ActivationMatch`

[HLD 4.9.2](30_HLD.md#492-処理の流れ)の 5「AZ と突き合わせる」である。`index` は `SpatialIndexes.activation`（AZ のジオメトリは `index.tree.geometries`）。HLD 3.5.3 の表の「AZ とその索引」を、索引がジオメトリを持つのでこの 1 つで受ける（`PeakZones` の `geometry` は `dict` で、内外の判定は `shapely` の形が要るため）。

内部の関数 `_zones_containing(lat: float, lon: float, index: SpatialIndex, rank: dict[tuple[int, int], int]) -> list[tuple[int, int]]`: 点を含むゾーンの持ち主（Z15 の画素）を、`peaks` の鍵の順に並べて返す。`match_delete_zones` も使う。

1. `center_lat, center_lon = z15_pixel_center_latlon(cmp5_common.latlon_to_z15_pixel(lat, lon))`。`positions = index.tree.query(shapely.Point(center_lon, center_lat))`（画素の中心の点の外接矩形に合うゾーンの添字の配列）。
2. `positions` のうち `is_in_zone(lat, lon, index.tree.geometries[i])` が真の `i` の `index.keys[i]` を集め、`rank`（`peaks` の鍵 → `peaks` の中の順番〈0 から〉）の昇順に並べて返す。

並びは `peaks` の鍵の順（`merged_peak.csv` の行の順）で、`STRtree.query` が返す順にも、索引を作った並び（`build_spatial_indexes` が `peak_zones` の鍵の順に作る）にも頼らない。`STRtree.query` の順は `shapely` の版や木の作りで変わりうるので、決定論的な出力（[HLD 5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)）のために並べ直す。

手順:

1. `rank = {key: i for i, key in enumerate(peaks)}`（この関数で 1 回だけ作る）。
2. サミットを順に見て、`candidates = _zones_containing(float(s.lat), float(s.lon), index, rank)`。
   - 0 件: AZ の外。何も控えず、次へ（`match_delete_zones` が受け持つ）。
   - 1 件: そのピークを含めたピークとする。
   - 2 件以上: 候補のうち `peaks[p].values['key_col_resolved'] == 'true'`（確定）のものを数える。
     - 確定が 2 つ以上: AO1 の材料に `(s, candidates)` を控える（この場では止めない）。
     - 確定が 1 つ: そのピークを含めたピークとする。
     - 確定が 0: 候補のうち次の key が最小のピークを含めたピークとする（`peak_elev` の降順、`peak_lat` の降順、`peak_lon` の昇順。HLD 4.9.2 の 5）。
     - 確定が 1 つ以下のときは、`AzOverlap(s, tuple(candidates), <含めたピーク>)` を `overlaps` に足す（確定が 1 つでも足す。HLD 4.9.2 の 5 が「どちらの場合も重なりを警告に並べて続ける」と決めている）。
   - 含めたピークを `summit_peak[s.code]` に入れる。
3. 全サミットを見た後、AO1 の材料があれば、すべてを挙げて AO1 で止まる（[DEC93](30_HLD.md#494-設計判断)「入力の誤りは書かずに止め、不備ゲートは書いて止める」の (2)。1 つ目で止まらない）。
4. `peak_summits` は、`summit_peak` の値ごとにサミットを集めた後で、`peaks` の鍵の順に回して作る（サミットの順に回して足すと、辞書の鍵の順がサミットの順になるため）。値のサミットの並びはサミットの順。AZ にサミットがあるピークだけを入れる。
5. `peak_status` は、`peak_summits` と同じ鍵の順で、サミットが 1 つなら `'matched'`、2 つ以上なら `'ambiguous'`（[ADR-SRS-048](decisions/ADR-SRS-048-multiple-summits-in-one-az.md)）。`SummitCode` は SS5 で重ならないことが分かっているので、サミットの数が `SummitCode` の数である。
6. `ActivationMatch(summit_peak, peak_summits, peak_status, overlaps)` を返す。`summits` が空、または `peaks` が空で索引が空（`shapely.STRtree([])`）なら、どのサミットも AZ の外になり、すべて空の辞書とリストを持つ `ActivationMatch` を返す。

確定が 0 のときの key は次のとおり（比べるのは `decimal.Decimal` にした値で、浮動小数にしない。[DEC92](30_HLD.md#494-設計判断)「採番と主ピークの比べ方は 10 進の値で行う」）。降順は `copy_negate()` で作る（単項の `-` は既定の精度 28 桁で丸めるので、`1000.0000000000000000000000001` と `1000.0000000000000000000000002` のような 28 桁を超える差が同じ鍵になる。[7.2.3](#723-関数の細部)の代表採用の鍵と同じ決まり）:

```python
def key(p):
    v = peaks[p].values
    return (decimal.Decimal(v['peak_elev']).copy_negate(),
            decimal.Decimal(v['peak_lat']).copy_negate(),
            decimal.Decimal(v['peak_lon']))
chosen = min(candidates, key=key)
```

この関数は警告を出さない（AO2 の材料を `overlaps` に並べて返し、出すのは [main](#mainmatch_summits)）。

##### match_delete_zones

`match_delete_zones(summits: list[Summit], peaks: dict[tuple[int, int], cmp5_common.MergedPeakRow], activation: ActivationMatch, index: SpatialIndex) -> DeleteMatch`

[HLD 4.9.2](30_HLD.md#492-処理の流れ)の 6「delete判定ゾーンと突き合わせ、主ピークを選ぶ」である。`summits` は AZ に含まれないサミットで、呼ぶ側が `activation.summit_peak` に無いものをサミットの順で渡す。`index` は `SpatialIndexes.delete`。

1. `rank` を `match_activation_zones` と同じ作り方で作る。
2. サミットを順に見て、`candidates = _zones_containing(float(s.lat), float(s.lon), index, rank)`（`matched`・`ambiguous` のピークも候補になる。[ADR-SRS-043](decisions/ADR-SRS-043-matched-peak-as-delete-reference.md)）。
   - 0 件: `summit_status[s.code] = 'unmatched'`、`unmatched` に `s` を足す。
   - 1 件以上: `summit_status[s.code] = 'delete'`。候補のうち次の key が最小のピークを主ピークとし（`prominence` の最小。`key_col_resolved` が確定でないピークは最大として扱う。同じなら `peak_lat` の降順、`peak_lon` の昇順。[FR-009](20_SRS.md#fr-009-sotaリスト突合match_status-判定)の主ピーク特定）、`dominant[s.code] = DominantPeak(<主ピークの画素>, cmp5_common.great_circle_m(float(peak_lat), float(peak_lon), float(s.lat), float(s.lon)))`（主ピークからサミットへ。`peak_lat`・`peak_lon` は主ピークの行の字句）。
3. `peak_status`: `peaks` の鍵の順に、`activation.peak_summits` に無い（AZ にサミットが無い）ピークだけを入れる。`dominant` のどれかに主ピークとして 1 回以上選ばれたピークは `'dominant'`、選ばれなかったピークは `'new'`（[DEC95](30_HLD.md#494-設計判断)「`dominant` は削除の候補の主ピークとする」）。
4. `DeleteMatch(summit_status, dominant, peak_status, unmatched)` を返す。`summits` が空なら `summit_status`・`dominant`・`unmatched` は空で、`peak_status` はすべて `'new'`。`peaks` が空で索引が空なら、すべてのサミットが `'unmatched'`、`peak_status` は空。

主ピークの key は次のとおり。確定していない行の `prominence` は空欄なので `Decimal` にしない（key の 3 つ目の `0` は使わない値の詰め物）。この形にするのは、字句を読み直さずに、確定は小さい順（最小の `prominence`）、確定していないものは最大として扱う（先頭の `0` と `1` が確定と未確定を分ける）ためである。採番の順（`assign_provisional_codes`）では未確定が末尾（最小として扱う）で、主ピークと扱いが逆になる。

```python
def key(p):
    v = peaks[p].values
    lat = decimal.Decimal(v['peak_lat']).copy_negate()
    lon = decimal.Decimal(v['peak_lon'])
    if v['key_col_resolved'] == 'true':
        return (0, decimal.Decimal(v['prominence']), lat, lon)
    return (1, decimal.Decimal(0), lat, lon)
dominant_peak = min(candidates, key=key)
```

##### locate_regions

`locate_regions(points: list[LocatePoint], boundaries: Boundaries, indexes: SpatialIndexes) -> RegionMatch`

[HLD 4.9.2](30_HLD.md#492-処理の流れ)の 7「地域と市区町村を照合する」である（[DEC91](30_HLD.md#494-設計判断)「地域と市区町村は境界の上を内とし、並びの最初のものを採る」）。点を作るのは内部の関数 `_region_points`（[main](#mainmatch_summits)が呼ぶ）。

内部の関数 `_region_points(peaks: dict[tuple[int, int], cmp5_common.MergedPeakRow], summits: list[Summit]) -> list[LocatePoint]`: 照合する点の並びを作る。

1. すべてのピーク（`peaks` の鍵の順）。`LocatePoint('peak', <画素>, peak_lat, peak_lon)`。
2. 続けて陸のコル。`key_col_resolved` が `'true'` で、`decimal.Decimal(col_lat)` と `decimal.Decimal(col_lon)` が**どちらも** 0 でないピークのコルだけ（ピークの順）。`LocatePoint('col', <親のピークの画素>, col_lat, col_lon)`。海面確定のコルは位置を持たず、緯度経度が 0 になる。片方だけ 0 のコルは入れない。値で比べるので、`'0'`・`'0.0'`・`'0.00000000'` は同じ 0 として扱う。
3. 続けてすべてのサミット（サミットの順）。`LocatePoint('summit', s.code, s.lat, s.lon)`。

陸のコルの条件は [7.3.3](#733-関数の細部)の `build_peak_features` と [6.8.3](#683-関数の細部)の `write_zone_geojson` の「`col_lat`・`col_lon` がどちらも 0 でない行だけ」と同じにする。HLD の同じ字句「`col_lat`・`col_lon` が 0.0 でない」を LLD がそう読んでいて、[build_summit_features](#build_summit_features)のコルの点の条件ともそろうので、照合したコルと出力するコルの点が食い違わない。並べ方（ピーク → コル → サミット）は HLD 4.9.2 の 7 の列挙の順で、警告 RG1 の順になる。

`locate_regions` の手順:

1. 点を順に見て、`Location` を作る。地域と市区町村を、それぞれ次の手順で照合する。
   - `boundaries` のその層（`regions`・`municipalities`）が `None`（ファイルが無い）なら照合しない。`region` は `None`、`municipality` は空文字にし、`outside` に入れない（[HLD 4.9.2](30_HLD.md#492-処理の流れ)の 4「地域と市区町村の GeoJSON を読み、索引を作る」が、無いファイルについて 7 の点ごとの警告を出さないと決めている）。
   - ある層は、元の緯度経度の点 `shapely.Point(float(point.lon), float(point.lat))`（画素の中心ではない）で `index.tree.query(point)` を引き、得た添字を昇順に並べて、`shapely.covers(index.tree.geometries[i], point)` が最初に真になる `i` を採る（境界の上を内とし、ファイルの順の最初を採る。添字の昇順がファイルの順）。採った `i` で `boundaries.regions[index.keys[i]]`（`RegionFeature`）か `boundaries.municipalities[index.keys[i]].municipality`（`str`）を得る。どれも真にならなければ、入らなかった。
   - ファイルがあって Feature が 0 件（空の `list`）の層は、どの点も入らない。
2. 入らなかった層の名前（`'地域'`・`'市区町村'` の順）を `layers` に集め、空でなければ `OutsidePoint(point, tuple(layers))` を `outside` に足す。
3. `locations[(point.kind, point.key)]` に `Location(region, municipality)` を入れる。`RegionMatch(locations, outside)` を返す。`points` が空なら、空の `RegionMatch` を返す。

この関数は警告を出さない（RG1 の材料を `outside` に並べて返す。RG1 を出すのは [main](#mainmatch_summits) で、`assign_provisional_codes` の後）。

##### assign_provisional_codes

`assign_provisional_codes(peak_status: dict[tuple[int, int], str], peaks: dict[tuple[int, int], cmp5_common.MergedPeakRow], locations: dict[tuple[str, object], Location], max_prefix: str, regions_missing: bool) -> dict[tuple[int, int], str]`

[HLD 4.9.2](30_HLD.md#492-処理の流れ)の 8「仮サミットコードを付ける」である。HLD 3.5.3 の表の「`new`・`dominant` のピークとその地域」は、`peak_status`（`DeleteMatch.peak_status`）と `locations`（`RegionMatch.locations`）で渡す。`max_prefix` は設定の `provisional_code_max_prefix`（大文字 1 字）、`regions_missing` は `boundaries.regions is None`。

1. 対象は `peak_status` のすべてのピーク（`'new'` と `'dominant'` を区別しない。[FR-009](20_SRS.md#fr-009-sotaリスト突合match_status-判定)の採番順序）。ピークの地域は `locations[('peak', pixel)].region`。エリアは `(region.assoc, region.area_code)`、`None` なら `(_ZZ, _ZZ)`。
2. エリアごとにピークを集め、次の key の昇順に並べる（`peak_elev` の降順、`prominence` の降順で `key_col_resolved` が確定でないものは最後、`peak_lat` の降順、`peak_lon` の昇順。降順は `copy_negate()`）。

   ```python
   def key(p):
       v = peaks[p].values
       elev = decimal.Decimal(v['peak_elev']).copy_negate()
       lat = decimal.Decimal(v['peak_lat']).copy_negate()
       lon = decimal.Decimal(v['peak_lon'])
       if v['key_col_resolved'] == 'true':
           return (elev, 0, decimal.Decimal(v['prominence']).copy_negate(), lat, lon)
       return (elev, 1, decimal.Decimal(0), lat, lon)
   ```

3. エリアの `i` 番目（0 から）のピークに `f'{assoc}/{area_code}-{chr(ord("A") + i // _CODE_PER_PREFIX)}{i % _CODE_PER_PREFIX:02d}'` を付ける（`A00`〜`A99`、その次は `B00`）。
4. エリアごとの上限は `(ord(max_prefix) - ord('A') + 1) * _CODE_PER_PREFIX` 件（`max_prefix` が `'A'` なら 100 件、`'B'` なら 200 件）。件数が上限を超えるエリアが 1 つでもあれば、すべてのエリアを数え終えてから、超えたエリアをすべて挙げて止まる（[ADR-SRS-031](decisions/ADR-SRS-031-provisional-code-limit-configurable.md)、[DEC93](30_HLD.md#494-設計判断)の (2)）。並びはエリアの `f'{assoc}/{area_code}'` の文字列の昇順。`regions_missing` が真なら PN2、偽なら PN1（地域の GeoJSON が無いと全ピークが `ZZ` に入るので、超えるのは `ZZ` のエリアだけになる）。
5. 返す辞書は `peak_status` の鍵の順（鍵はピークの画素、値は仮サミットコード）。`peak_status` が空なら空の辞書。

`peak_status` の鍵が `peaks` と `locations` に無いのは呼ぶ側の誤りで、例外のまま伝える。

##### read_sota_names

`read_sota_names(ref_dir: str, version: int | None) -> SotaNames`

[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「出力の組み立て」の 1「SOTA 既存サミット GeoJSON を読む」である（[DEC99](30_HLD.md#494-設計判断)「SOTA 既存サミット GeoJSON の不備では止めない」、[HLD 2.3.2](30_HLD.md#232-設定ファイル)の `sota_geojson_version`、[SRS §7.2.5](20_SRS.md#725-sota-既存サミット-geojsongeojson_vn)）。`ref_dir` は `$DATA_DIR/ref/`、`version` は設定の `sota_geojson_version`（`ConfigValue.value`。未設定は `None`）。この関数は止まらず、不備は `SotaNames.warnings` に並べて返す。

1. 版の確かめ。`version` が `None` なら SN1（未設定）を 1 件足し、空の `names` で返す。`os.path.isdir(os.path.join(os.path.abspath(ref_dir), f'geojson_v{version}'))` が偽なら SN1（ディレクトリが無い。`{dir}` はそのディレクトリの絶対パス）を 1 件足し、空の `names` で返す。ディレクトリがあれば、次へ進む。
2. ファイルを読む。`ja0_v<version>.geojson`〜`ja9_v<version>.geojson` を、この順に 1 つずつ読む。次のどれかなら、そのファイルを使わず、SN2 を足して次のファイルへ進む。読み方と理由の文は `read_boundaries` の 1・2 にそろえる（`{path}` は `os.path.abspath` したパス）。
   - `os.path.exists` が偽: 理由は `ファイルが無い`。
   - `open(abspath, encoding='utf-8')` と `json.load(f, parse_constant=_reject_constant)` で、`OSError` なら `{reason}` の決まり（ディレクトリも）、`UnicodeDecodeError` なら `UTF-8 として読めない`、`ValueError`（`json.JSONDecodeError` と `_reject_constant` が上げるものの両方を含む）なら `str(e)`、`RecursionError` なら `入れ子が深すぎる`。
   - 最上位が `dict` でない、`type` が `'FeatureCollection'` でない、`features` が `list` でない: 理由は `FeatureCollection でない`。
   - キーが重なる JSON は拒まない（`json.load` の既定のとおり後のキーが勝つ。ここは山岳名だけを読み、[DEC99](30_HLD.md#494-設計判断)が不備で止めないと決めているので、書き出す GeoJSON の検査の決まりである [7.1](#71-cmp5_common)の `_unique_object` は使わない）。
3. `features` の要素ごとに、`name` を読む。次のどれかなら、その Feature を飛ばして、そのファイルの飛ばした件数を 1 増やす。
   - 要素が `dict` でない、`properties` が `dict` でない、`properties` に `name` が無いか `str` でない。
   - `i = name.find('(')` が `-1`（`(` が無い）、`name` が `')'` で終わらない。
   - `code = name[:i]` が空文字、`jp = name[i + 1:-1]` が空文字。

   飛ばさなければ、`code` を最初の `(` の前、`jp` をその直後から末尾の `)` の直前までとする（`JA/XX-002(山(北))` なら `JA/XX-002` と `山(北)`）。`code`・`jp` の前後の空白は除かない（字句のまま）。`code` ごとに、違う `jp` を最初に現れた順に集める（同じ `jp` は 2 度入れない）。1 つのファイルを読み終えたとき、飛ばした件数が 1 以上なら SN3（`{path}` と件数）を足す。
4. すべてのファイルを読み終えた後、`names` を作る。`code` に違う `jp` が 1 つだけなら、その `jp`。2 つ以上なら空文字にして、SN4 の材料に入れる（同じ `jp` が何度出ても、違うものは数えない）。SN4 は材料があれば 1 件だけ足す（`{list}` は、コードを文字列の順に、`{code}（{jp}・{jp}）` を `、` でつなぐ。`jp` は最初に現れた順）。
5. `warnings` の並びは、SN1、ファイルの順に SN2・SN3、最後に SN4。`SotaNames(names, warnings)` を返す。`names` の鍵は最初に現れた順。

##### derive_attributes

`derive_attributes(peaks: dict[tuple[int, int], cmp5_common.MergedPeakRow], summits: list[Summit], activation: ActivationMatch, deletion: DeleteMatch, codes: dict[tuple[int, int], str], regions: RegionMatch, names: dict[str, str]) -> Attributes`

[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「出力の組み立て」の 2「値を求める」の、`rationale` を除く属性の値を求める。`summits` は `SummitsList.summits`（現役のすべて）、`codes` は `assign_provisional_codes` の返り値、`regions` は `locate_regions` の返り値、`names` は `SotaNames.names`。`category` と確認用の属性の割り当ては [FR-009](20_SRS.md#fr-009-sotaリスト突合match_status-判定) の `category` の算出と per-feature の割り当てルールのとおり。この関数は止まらず、警告を出さない。

内部の関数（モジュールの最上位）:

- `_band_points(h: int) -> int | None`: `_BANDS` を前から見て、`h >= 下限` となる最初の組の点を返す。どれにも当たらなければ `None`（[DEC170](30_HLD.md#494-設計判断)「算出表に無い標高のポイントは null にする」）。
- `_floor_m(text: str) -> int`: `int(decimal.Decimal(text).to_integral_value(rounding=decimal.ROUND_FLOOR))`（小数点以下の切り捨て。`peak_elev` と変更後の標高の字句に使う。浮動小数にしない。`'149.99'` は 149、`'150.00'` は 150）。サミットの `AltM` は `_INTEGER_RE` を通った整数の字句なので `int(alt_m)`。

手順:

1. 状態。`pstatus = {p: activation.peak_status.get(p) or deletion.peak_status[p] for p in peaks}`（`peaks` の鍵の順。AZ にサミットがあるピークは `activation.peak_status`、無いピークは `deletion.peak_status`）。
2. ポイント。ピークの `points = _band_points(_floor_m(peak_elev))`、サミットの `sota_points = _band_points(int(alt_m))`。
3. ピークの属性（`peaks` の鍵の順に `PeakAttrs` を作る）:
   - `new`・`dominant`: `category='add'`、`review_reason=''`、`review_group_id=''`、`is_band_change_candidate=None`、`summit_name_jp=''`、`rationale=build_rationale('add', <ピークの行>, regions.locations[('peak', p)], None, None, points, '')`。
   - `matched`: AZ の中のサミット `s = activation.peak_summits[p][0]`。`points` と `s` の `sota_points` のどちらかが `None` なら `is_band_change_candidate=False`（`NullPoints.band_false` に `p` を入れる）、どちらもあれば `points != sota_points`。`category` は真なら `'band_change'`、偽なら `'no_change'`。`review_reason=''`、`review_group_id=''`、`summit_name_jp=names.get(s.code, '')`。`rationale` は `band_change` のときだけ `build_rationale('change', <ピークの行>, regions.locations[('peak', p)], s, <s の sota_points>, points, '')`、`no_change` は空文字。
   - `ambiguous`: `category='review'`、`review_reason='multiple_summits_in_az'`、`review_group_id='az:' + '|'.join(sorted(<AZ の中のサミットの code>))`（[SRS §6.2.4](20_SRS.md#624-突合済み統合-geojson)の `review_group_id` の形。`sorted` は文字列の順＝符号位置の順）、`is_band_change_candidate=None`、`summit_name_jp=''`、`rationale=''`。
4. サミットの属性（サミットの順に `SummitAttrs` を作る。`summit_name_jp = names.get(code, '')`、`sota_points` はすべてのサミットで求める）:
   - `match_status`: `activation.summit_peak` にあれば、そのピークの `pstatus`（`'matched'`・`'ambiguous'`）、無ければ `deletion.summit_status[code]`（`'delete'`・`'unmatched'`）。
   - `matched`・`ambiguous`: `category`・`review_reason`・`review_group_id` は親のピーク（`activation.summit_peak[code]`）と同じ。`dominant_peak_code=''`、`dominant_peak_dist_m=None`、`rationale=''`（※5 はピークに付ける）。
   - `delete`: 主ピーク `d = deletion.dominant[code]`。`dominant_peak_dist_m=round(d.dist_m, 1)`。
     - 主ピークが `ambiguous`（`pstatus[d.pixel]`）: `category='review'`、`review_reason='ambiguous_parent'`、`review_group_id` はそのピークの `review_group_id`、`dominant_peak_code=''`（[FR-009](20_SRS.md#fr-009-sotaリスト突合match_status-判定)の主ピーク特定。距離は保持する）、`rationale=''`。
     - 主ピークが `matched`: `category='delete'`、`review_reason=''`、`review_group_id=''`、`dominant_peak_code` は主ピークの AZ の中のサミットの `code`（`activation.peak_summits[d.pixel][0].code`）、`rationale=build_rationale('delete', <主ピークの行>, None, None, None, None, <その code>)`。
     - 主ピークが `dominant`: 同じく `category='delete'` で、`dominant_peak_code=codes[d.pixel]`、`rationale=build_rationale('delete', <主ピークの行>, None, None, None, None, '')`（`parent_code` に空文字を渡して、`build_rationale` に追加申請するピークの座標で書かせる。仮サミットコードは申請書に出さないため）。
   - `unmatched`: `category='review'`、`review_reason='unmatched'`、`review_group_id=''`、`dominant_peak_code=''`、`dominant_peak_dist_m=None`、`rationale=''`。
5. `groups`。`pstatus` が `ambiguous` のピークごと（`peaks` の鍵の順に集める）に、`ReviewGroup(<review_group_id>, p, <AZ の中のサミットの code を文字列の順>, <deletion.dominant のうち d.pixel が p のサミットの code を文字列の順>)`。集めた後で `group_id` の文字列の順に並べ直す。
6. `null_points`。`NullPoints(<points が None のピークの画素。peaks の鍵の順>, <sota_points が None のサミット。サミットの順>, <手順 3 の band_false>)`。
7. `Attributes(<手順 3 の辞書>, <手順 4 の辞書>, groups, null_points)` を返す。`peaks`・`summits` が空なら、空の辞書と空の `groups`・空の `NullPoints` を持つ `Attributes` を返す。

**定数の確認用の属性は持たない（Ruling）**: `review_decision`・`review_note`・`application_exclusion`・`exclusion_note`（すべて空文字）と `pending_return`（すべて `false`）は、[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「出力の組み立て」の 2 が入力によらず固定と決める値なので、`PeakAttrs`・`SummitAttrs` に持たせない。持たせると全件同じ値の項目が 5 つ増えるだけで、UT が何も確かめられない。フィーチャへ書くのは [build_summit_features](#build_summit_features) である。

**距離の丸め（Ruling）**: `round(d.dist_m, 1)`。`float` の 2 進の値を正しく丸めた `float` を返す（`10.25` は 2 進で正確に表せるので、偶数側の `10.2`。`1234.56` は `1234.6`）。距離は人の確かめ用の値で（[FR-009](20_SRS.md#fr-009-sotaリスト突合match_status-判定)）、入力の字句から来る数ではないので、[DEC104](30_HLD.md#494-設計判断)「入力から来る数は 10 進の値を変えずに書く」の「入力から来る数」に当たらない。同じ `float` からは同じ値になるので、[HLD 5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)の再現性を保つ。[build_summit_features](#build_summit_features) は、これを JSON の数として書く。

##### build_rationale

`build_rationale(kind: str, peak: cmp5_common.MergedPeakRow, location: Location | None, summit: Summit | None, sota_points: int | None, peak_points: int | None, parent_code: str) -> str`

[FR-009](20_SRS.md#fr-009-sotaリスト突合match_status-判定)の「rationale プロパティ生成」の ※2・※4・※5 を作る（[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「出力の組み立て」の 2 の rationale の数・海面・標高・所在地）。行は `'\n'` でつなぎ、末尾に改行を付けない。`{peak_lat}` などの数は `peak.values` の字句のまま入れる（[DEC104](30_HLD.md#494-設計判断)）。`kind` ごとに使う引数は次のとおりで、使わない引数は見ない（呼ぶ側は `None`・空文字を渡す）。`kind` は `'add'`・`'change'`・`'delete'` のどれか（ほかは渡されない。検査しない）。

- `kind='add'`（※2。`peak` は対象のピーク、`location` はそのピークの点の `regions.locations[('peak', p)]`）。6 行:
  1. `国土地理院標高タイルで解析`
  2. `{peak_lat},{peak_lon}`
  3. `所在地：{region_name} {municipality}`。`{region_name}` は `location.region` が `None` なら空文字、そうでなければ `location.region.region_name`。`{municipality}` は `location.municipality`。空文字は空のまま入れ、間の空白 1 つは残す（両方空なら、3 行目は `所在地：` の後に空白 1 つだけが続く）。
  4〜6. コルの 3 行は、`key_col_resolved` と値で 3 つの形に分ける。
     - 未確定（`peak.values['key_col_resolved']` が `'true'` でない）: `コル位置：未確定`・`コル標高：未確定`・`プロミネンス：未確定`。
     - 海面（確定で、陸のコルの条件に当たらない）: `コル位置：海面`・`コル標高：{col_elev}m`・`プロミネンス：{prominence}m`。陸のコルの条件は [`_region_points`](#753-関数の細部)と同じ、`decimal.Decimal(col_lat)` と `decimal.Decimal(col_lon)` が**どちらも** 0 でないこと（片方だけ 0 は海面として扱う。[DEC100](30_HLD.md#494-設計判断)「海面で確定したコルは点にせず、XLSX でも空欄にする」の条件を、[7.3.3](#733-関数の細部)の `build_peak_features` の「どちらも 0 でない」の裏として読む）。
     - 陸: `コル位置：{col_lat},{col_lon}`・`コル標高：{col_elev}m`・`プロミネンス：{prominence}m`。
- `kind='change'`（※5。`peak` は `matched` のピーク、`summit` は AZ の中のサミット、`location` はそのピークの点の `regions.locations[('peak', p)]`、`sota_points` と `peak_points` はどちらも `None` でない）。2 行:
  1. `国土地理院 DEM 解析による標高再測定: {summit.alt_m}m ({sota_points}pt) → {_floor_m(peak.values['peak_elev'])}m ({peak_points}pt)`
  2. `座標: {peak_lat},{peak_lon}（{region_name} {municipality}）`。`{region_name}`・`{municipality}` は `add` の 3 行目と同じ。
- `kind='delete'`（※4。`peak` は主ピーク、`location` は `None`）。1 行: `国土地理院標高タイルを解析し、{親の参照}に従属している事を確認`。`{親の参照}` は `parent_code` が空文字でなければ `parent_code`（主ピークが `matched`）、空文字なら `追加申請するピーク（{peak_lat},{peak_lon}）`（主ピークが `dominant`。座標は ※2 の 2 行目と同じ表記）。

**所在地にピークの点の `location` を使う（Ruling）**: ※5 の所在地は、AZ の中のサミットの点の所在地でなく、ピークの点の所在地である（[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「出力の組み立て」の 2 の「rationale の所在地」が「※2・※5 ともピークの点の」と決めている）。

##### match_pending_applications

`match_pending_applications(updatelist: UpdateList, summits_list: SummitsList, peaks: dict[tuple[int, int], cmp5_common.MergedPeakRow], activation: ActivationMatch, deletion: DeleteMatch, index: SpatialIndex, attrs: Attributes) -> Pending`

[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「申請済みの判定」の 1「山岳 ID を照合する」・2「追加の申請を当てる」・3「削除と変更の申請を当てる」・4「当たり方をまとめる」・6「同じ行のフィーチャへ写す」・7「知らせる行をまとめる」である（[ADR-SRS-086](decisions/ADR-SRS-086-pending-applications-input-and-state.md)、[DEC189](30_HLD.md#494-設計判断)「申請の情報は申請ごとの配列で持つ」）。`index` は `SpatialIndexes.activation`（HLD 3.5.3 の表の「AZ とその索引」を、`match_activation_zones` と同じく、ジオメトリを持つ索引の 1 つで受ける）。申請の並びは `UpdateList` ごと受ける（知らせる行をまとめる 7 で、読み込みの知らせと年の表の順が同じ型にあるため）。この関数は止まらず、警告を出さない。

**行の鍵**: 申請が当たる行は、フィーチャでなく「行の鍵」で数える（フィーチャを作るのは [build_summit_features](#build_summit_features)）。`('peak', 画素)` は `add`・`band_change` のピークの行（`matched` のピークの行は、AZ の中のサミットの点も含む）、`('summit', code)` は `delete` と `unmatched` のサミットの行。HLD の 6「同じ行のフィーチャへ写す」は、この関数が行ごとに 1 つの値を持つことで「写した値は同じ行のどのフィーチャでも同じ」を満たす。[build_summit_features](#build_summit_features) は、行の鍵に無い行を `[]`・`''`・`''`（`pending_applications`・`pending_match`・`pending_note`）にし、行のフィーチャすべてに同じ値を書く。

内部の関数:

- `_json_number_text(text: str) -> str`: 先頭の `+` を除き、整数部の先頭の余分な `0` を除く（整数部が `0` だけになるものは `0` を残す。先頭の `-` と小数部は変えない）。`+35.10` は `35.10`、`035.1` は `35.1`、`0150` は `150`、`0.5` は `0.5`、`-035.1` は `-35.1`。**Ruling**: `is_valid_coord` が通す字句の `_DECIMAL_RE`（[7.1.3](#713-関数の細部)）は `+35.10`・`035.1` を、`_ELEV_RE` は `0150` を通すが、`cmp5_common.JsonNumber` は書き出す側が `text` をそのまま書く型（[7.1.2](#712-型とデータ)）なので、そのままでは `merged_summit.geojson` が JSON として読めなくなる。除くのは JSON の数の文法が許さない字だけで、10 進の値と末尾の `0` は変えない（[DEC104](30_HLD.md#494-設計判断)）。[build_summit_features](#build_summit_features) の `_num` がこれを通して `JsonNumber` にする。

手順:

1. 準備。`rank = {key: i for i, key in enumerate(peaks)}`。現役のサミットを `code` で引く表。現役のサミットの `code` を `code.partition('/')` で分けた後ろ（`/` が無い `code` は入れない）からサミットを引く表。廃止済みの `retired_codes` の後ろの集合。
2. 追加の申請（`action='add'`）を当てる。`_zones_containing(float(lat), float(lon), index, rank)` の候補のうち `attrs.peaks[p].category == 'add'` のものを取る。
   - 取ったものが 1 つ以上: 2 回目の AZ の重なりの key `(peak_elev の降順, peak_lat の降順, peak_lon の昇順)`（`decimal.Decimal` にした値で、降順は `copy_negate()`。`match_activation_zones` の確定が 0 のときと同じ）の最小のピーク `p` の行 `('peak', p)` に、`match` が `'same'`（「同じ内容」）の申請として当てる。
   - 取ったものが無く、候補が 1 つ以上ある（`matched`・`ambiguous` のピークの AZ にだけ入る）: 当てず、知らせない。
   - 候補が 0: 知らせる行 `unmatched_add` を作る（`value` は `f'{lat},{lon}'`。字句のまま）。

   どの分かれでも、追加の申請は取り込んだ申請として `taken` に 1 を足す（追加は ID を照合せず、バンドの比べも無いので、読めて `UpdateList.applications` に入ったものはすべて取り込む。当たらなかった `unmatched_add` も、取り込んだ後に当たらなかったものとして数える）。
3. 変更・削除の申請の山岳 ID の照合。`summit_id` を `sid`、`/` の後ろを `tail`、`tail` の `-` の前を地域コード `rc` とし、次の順に見て、最初に当たったもので決める。
   1. 現役の `code == sid` → そのサミット。
   2. `sid in summits_list.retired_codes` → 取り込まず、知らせない（反映済み）。
   3. `len(summits_list.region_assocs.get(rc, frozenset())) >= 2` → 知らせる行 `ambiguous_region`（`value` は `sid`）。
   4. 現役の `code` の `/` の後ろが `tail` → そのサミット（`rc` はここまでで 1 つのアソシエーションにしか無いので、`tail` に当たる現役のサミットは高々 1 件）。アソシエーションの部分だけ違う `JA/KC-027` と `JA5/KC-027` を同じものとして扱う。
   5. 廃止済みの `code` の `/` の後ろが `tail` → 取り込まず、知らせない。
   6. どれにも当たらない → 知らせる行 `unknown_id`（`value` は `sid`）。

   当たったサミットの `code` を、`pending_applications` の `summit_code` にする（SOTA サミットリストの表記）。変更は続けて、今のバンド `_band_points(int(alt_m))` と変更後のバンド `_band_points(_floor_m(new_elev))` を比べる。どちらかが `None`、または同じなら、取り込まず、知らせない。違えば変更後のバンドを `new_points` にする。この分かれで取り込む申請を `taken` に数える（下の「取り込んだ申請の数」）。
4. 変更・削除の申請を行に当てる。3 で決めたサミットの `code` で、次の表のとおりに行の鍵と当たり方を決める。サミットの状態は、`activation.summit_peak` にあれば `p = activation.summit_peak[code]` と親のピークの `attrs.peaks[p].category`、無ければ `deletion.summit_status[code]` と `attrs.summits[code].category` で見る。

   | サミットの状態 | 削除の申請 | 変更の申請 |
   |---|---|---|
   | `delete` で `attrs.summits[code].category` が `'delete'` | `('summit', code)` に `same` | `('summit', code)` に `different` |
   | `delete` で `attrs.summits[code].category` が `'review'`（主ピークが `ambiguous`。`ambiguous_parent`） | 当てない | 当てない |
   | `matched` で親のピークの `category` が `'band_change'` | `('peak', p)` に `different` | `('peak', p)` に、`new_points` が `attrs.peaks[p].points` と同じなら `same`、違えば `different` |
   | `matched` で親のピークの `category` が `'no_change'` | 当てない | 当てない |
   | `ambiguous` | 当てない | 当てない |
   | `unmatched` | `('summit', code)` に `held` | `('summit', code)` に `held` |

   当てない申請は、行にも知らせる行にも入らない。この表は [HLD 4.9.2](30_HLD.md#492-処理の流れ)の「申請済みの判定」の 3「削除と変更の申請を当てる」を行ごとに写したもの。
5. 当たり方をまとめる。申請を行ごとに集め、行ごとに `applications` を作る。申請 1 つは DEC189 のキーの順の `dict`: `action`・`summit_code`（追加は空文字）・`lat`・`lon`（追加は `cmp5_common.JsonNumber(_json_number_text(<字句>))`、変更・削除は `None`）・`new_alt_m`（変更は `cmp5_common.JsonNumber(_json_number_text(new_elev))`、ほかは `None`）・`new_points`（変更は `int`、ほかは `None`）・`applicant`・`applied_on`・`years`（`sorted(Application.years, reverse=True)` の `list[int]`）・`match`（`'same'`・`'different'`・`'held'`）。行の `applications` は、key `(applied_on, _ACTION_ORDER[action], <summit_code> か (Decimal(lat), Decimal(lon)), applicant)` の昇順に並べる（アクションが同じ申請の中でだけ 3 つ目を比べるので、型は揃う）。key が同じ申請〔同じサミット・申請日・申請者で変更後の標高だけが違う 2 つの申請、アソシエーションだけ違う ID を同じ `code` に揃えた 2 つの申請、`35.1` と `35.10` の追加など〕は、`updatelist.applications` の順のまま（`sorted` は安定）。行の `match` は、`applications` に `same` が 1 つでもあれば `'same'`、無くて `different` があれば `'different'`、`held` だけなら `''`。`note = build_pending_note(applications)`。`PendingRow(tuple(applications), match, note)` を作る。
6. `rows` を、鍵が `('peak', p)` を `peaks` の鍵の順、続けて `('summit', code)` を `summits_list.summits` の順に並べた辞書にする（申請が当たった行だけ）。
7. 知らせる行をまとめる。2・3 の知らせる行を `Notice(kind, reason, year, row, action, target, applicant, applied_on, value)` で作る（`year, row = Application.first_seen`、`action = action_text`、`target = target_text`、`reason` は `_REASON_UNKNOWN_ID`・`_REASON_AMBIGUOUS_REGION`・`_REASON_UNMATCHED_ADD`）。`updatelist.notices` と合わせ、key `(<year の updates の中の位置>, 0 if kind == 'unreadable_update' else 1, row or 0, _KIND_ORDER[kind])` の昇順に並べる（`sorted` は安定）。`<year の updates の中の位置>` は、その年が `updatelist.updates` で最初に現れる位置（0 から）。
8. `Pending(rows, notices, taken)` を返す。申請が 0 件なら、空の `rows` と `updatelist.notices` を同じ並びにしたものと、`taken` が 0 のものを返す。

**取り込んだ申請の数（`taken`）**: [HLD 4.9.2](30_HLD.md#492-処理の流れ)の「登録変更リストの読み方」の「取り込む申請」（追加、削除、バンドをまたぐ変更だけを取り込む）の選別を通った申請の数である。読み込み（`read_updatelist`）の時点で除く変更後の標高の欄が空の変更は、`UpdateList.applications` に入らないので数えない。重ね合わせの後の `UpdateList.applications` の 1 件を 1 と数え、行に当てるかどうかや `pending_match` は関係しない（`no_change`・`review`・`ambiguous` に当たって行に載らない申請も、取り込んだものとして数える）。分かれ（HLD の「申請済みの判定」の 1「山岳 ID を照合する」・2「追加の申請を当てる」の「取り込まず」の語に 1 つずつ合わせた）:

| 申請 | 場面 | `taken` |
|---|---|---|
| 追加 | AZ に当たる、`matched`・`ambiguous` の AZ にだけ入って当てない、どの AZ にも入らず `unmatched_add` になる（手順 2 の 3 つ） | 数える |
| 削除・変更 | 山岳 ID が現役の `code` に一致する（手順 3 の 1）、または地域コードと番号が現役の `code` の `/` の後ろに一致する（4） | 削除は数える。変更は、バンドを比べて違うときだけ数える（同じ、または今のバンドか変更後のバンドが `None` のときは数えない） |
| 削除・変更 | 山岳 ID が廃止済みの `code` に一致する（手順 3 の 2・5。反映済み） | 数えない |
| 削除・変更 | 地域コードが 2 つ以上のアソシエーションにある（3。`ambiguous_region`） | 数えない |
| 削除・変更 | どれにも当たらない（6。`unknown_id`） | 数えない |

**Ruling**: 数え方を `main` に置かず、選別の決まりがある `match_pending_applications` の中で数えて返す（`UpdateList.applications` の件数は選別の前の数で、HLD の「取り込む申請」と違う数になる。`main` が選別を数え直すと、決まりが 2 か所になる）。このため、型 `Pending` の項目に末尾の `taken` を足した（`Pending` を位置引数で作る [7.5.5](#755-ut-候補)の UT 候補も 3 つ目の値を渡す）。

**同じ年の表が 2 つあるファイル（Ruling）**: `Notice` は年だけを持ち、年の表の位置を持たない。同じ年の題の表が 2 つあるファイルは `read_updatelist` が止めないが、その 2 つ目の表の知らせる行は、1 つ目の表の位置に並ぶ。同じ年の 2 つの表は実物に無く、`Notice` に表の位置を足すと 1 回目の型が変わる。

**行の鍵と `match` の関係**: `unmatched` のサミットの行は、`match` が `held` の申請だけを持つので、行の `match` は空文字になる。`no_change`・`review` に当たった申請は行に載らない（候補の判定を付けない）。

##### build_pending_note

`build_pending_note(applications: Sequence[dict]) -> str`

[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「申請済みの判定」の 5「`pending_note` を作る」である。`applications` は `PendingRow.applications` の並び（`dict`）。申請ごとに `f'{_ACTION_JA[a["action"]]} {a["applied_on"]}（{"・".join(str(y) for y in a["years"])}年の表）'` を作り、`'／'` でつなぐ。`years` は新しい順のまま使う（複数の年の表に載る申請は `（2026・2025年の表）`）。申請者を含めない。`applications` が空なら空文字を返す。

##### build_metadata

`build_metadata(ref_date: datetime.date, tiles_dir: str, repo_dir: str, updatelist: UpdateList, notices: Sequence[Notice], now: datetime.datetime) -> Metadata`

[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「出力の組み立て」の 3「metadata を作る」である。`ref_date` は `SummitsList.ref_date`、`tiles_dir` は `$DATA_DIR/tiles/` の絶対パス、`repo_dir` は CMP5 のスクリプトのあるディレクトリ、`updatelist` は `read_updatelist` の返り値、`notices` は `Pending.notices`（読み込みの知らせと照合の知らせを 1 つの並びにしたもの）、`now` は出力を組み立てた時刻（時差の付いた `datetime.datetime`。時差の無い `now` は渡されず、検査しない）。この関数は止まらず、警告を出さず、求められなかったものを警告の材料として `Metadata.warnings` に並べて返す。

**`now` を引数で受ける（Ruling）**: [HLD 3.5.3](30_HLD.md#353-関数)の表の「受け取るもの」に出力を組み立てた時刻は無いが、時刻を関数の中で取ると、UT が出力を比べられない。`updatelist` と `notices` を別々に受けるのは、HLD の表が採った登録変更リストのファイル名と年の表ごとの Update の日付（`UpdateList` が持つ）と、知らせる行（`Pending.notices` の並びで、`updatelist.notices` と同じではない）を別に挙げるため。`now` を作って渡すのは [main](#mainmatch_summits) で、`tiles_dir`・`repo_dir` も `main` が作る。

`items` のキーはこの順に並べる（**Ruling**: [FR-009](20_SRS.md#fr-009-sotaリスト突合match_status-判定)の「metadata 付与」の列挙の順。SRS がスキーマの正本で、同じ入力から同じ文字列にするために順を 1 つに決める）。

1. `summitslist_date`: `ref_date.isoformat()`（`YYYY-MM-DD`）。
2. `generated_at`: `now.astimezone(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')`（秒より下は切り捨てる。UTC でない時差の `now` も UTC に直す）。
3. `updatelist_file`: `updatelist.file_name`。
4. `updatelist_updates`: `updatelist.updates` の順のまま（ファイルに年の表が現れる順で、実物は新しい年から。[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「新しい年から」はこの順を指す）、`{'year': u.year, 'update': u.update}` の `list`。`update` が空文字の年は空文字のまま。
5. `updatelist_notices`: `notices` の順のまま、`Notice` の 9 項目（`kind`・`reason`・`year`・`row`・`action`・`target`・`applicant`・`applied_on`・`value`）を、同じ名前の同じ順の `dict` にした `list`。`row` が `None` のものは `None`。
6. `gsi_tile_latest_date`: 内部の関数 `_tile_latest_date(tiles_dir)` の値。理由が返ったら（`None` でなければ）、警告の材料 `('MT2', <1 行目>)`（[7.5.4](#754-メッセージ文面)）を `warnings` に足す。
7. `attribution`・`source_url`・`license_url`: `_ATTRIBUTION`・`_SOURCE_URL`・`_LICENSE_URL`。
8. `software_version`: 内部の関数 `_software_version(repo_dir)` の値。理由が返ったら、警告の材料 `('MT1', <1 行目>)` を `warnings` に足す。

`warnings` の並びは `MT1`、`MT2`（`items` の `gsi_tile_latest_date`・`software_version` の順とは逆。この回が決める）。出す順は [main](#mainmatch_summits) が決める。

内部の関数（モジュールの最上位）:

- `_tile_latest_date(tiles_dir: str) -> tuple[str, str | None]`: 値と、求められなかったときの理由を返す（[ADR-SRS-032](decisions/ADR-SRS-032-gsi-tile-latest-date-provenance.md)、[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「出力の組み立て」の 3）。
  1. `os.walk(tiles_dir, onerror=<OSError を控える関数>)` でたどる（`followlinks` は既定の `False`）。ループの中で `dirnames.sort()`・`filenames.sort()` をして、名前の順にたどる（理由の文を環境の並びに依らせないため。理由には最初に当たった `OSError` を使う）。
  2. 名前が `.png`（小文字だけ。CMP2 が書く名前。`.PNG` は見ない）で終わるファイルごとに、`os.stat(os.path.join(dirpath, name)).st_mtime` を取る。`os.stat` の `OSError` も控える。
  3. `OSError` を 1 つでも控えたら、値は空文字、理由は `ディレクトリをたどれない: {path}: {reason}`（最初に控えた `OSError` の `filename`〈無ければ `tiles_dir`〉と `strerror`〈無ければ `str(e)`〉。**Ruling**: 一部だけ読めたときの最大は過小になりうるので、[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「ディレクトリをたどれなければ」を「1 つでも読めない所があれば」と読む）。
  4. `.png` が 0 枚なら、値は空文字、理由は `PNG が 1 枚も無い`。
  5. あれば、最大の `st_mtime` を `datetime.datetime.fromtimestamp(<最大>, datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')`（秒より下は切り捨てる）にした文字列と `None`。
- `_software_version(repo_dir: str) -> tuple[str, str | None]`: 値と、求められなかったときの理由を返す（[DEC98](30_HLD.md#494-設計判断)「版の文字列は出力を組み立てるときに git から取る」）。
  1. `subprocess.run(['git', 'describe', '--tags', '--dirty', '--always'], cwd=repo_dir, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=60, check=False)`。`git` はリポジトリの中のどのディレクトリからでも同じ値を返す。
  2. `OSError`（`git` が無い、`cwd` が無い）は、値 `unknown`、理由 `{reason}`（`strerror`、無ければ `str(e)`）。`subprocess.TimeoutExpired` は、値 `unknown`、理由 `60 秒で終わらない`。`returncode != 0` は、値 `unknown`、理由 `git describe の終了コード {rc}: {stderr の最初の行}`（`stderr` が空なら `{rc}` の後のコロンと空白 1 つの後は空）。`stdout.strip()` が空なら、値 `unknown`、理由 `git describe の出力が空`。
  3. 成功なら `stdout.strip()` と `None`。

##### build_summit_features

`build_summit_features(peaks: dict[tuple[int, int], cmp5_common.MergedPeakRow], zones: dict[tuple[int, int], PeakZones], summits: list[Summit], activation: ActivationMatch, deletion: DeleteMatch, codes: dict[tuple[int, int], str], regions: RegionMatch, attrs: Attributes, pending: Pending, metadata: dict) -> SummitFeatures`

[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「出力の組み立て」の 4「`merged_summit.geojson` を組み立てる」と、「申請済みの判定」の 6「同じ行のフィーチャへ写す」である。`zones` は `match_zones_to_peaks` の返り値、`summits` は `SummitsList.summits`、`codes` は `assign_provisional_codes` の返り値、`regions` は `locate_regions` の返り値、`attrs` は `derive_attributes` の返り値、`pending` は `match_pending_applications` の返り値、`metadata` は `Metadata.items`。この関数は止まらず、警告を出さない（内部の関数 `_encode_json` が、7.5.3 の対応しない型で上げる `TypeError` はプログラムの誤り）。

**返す文字列は [write_summit_outputs](#write_summit_outputs) がそのまま書く（Ruling）**: [HLD 3.5.3](30_HLD.md#353-関数)の表は返すものを「GeoJSON の中身」とするが、JSON の数の書き方（[HLD 4.9.2](30_HLD.md#492-処理の流れ)の 4 の「数」と [DEC104](30_HLD.md#494-設計判断)「入力から来る数は 10 進の値を変えずに書く」）はこの関数の範囲で、`SummitFeatures.text` として文字列にして返す。`write_summit_outputs` は、この文字列を一時ファイルに書くだけにする。

**行の鍵と、ピークの状態**: `status(p) = activation.peak_status.get(p) or deletion.peak_status[p]`（`'matched'`・`'ambiguous'`・`'dominant'`・`'new'`）。サミットは `{s.code: s for s in summits}` で `code` から引く。

内部の関数（モジュールの最上位）:

- `_num(text: str) -> cmp5_common.JsonNumber`: `cmp5_common.JsonNumber(_json_number_text(text))`。**字句の正規化（Ruling）**: `merged_peak.csv` と SOTA サミットリスト CSV から来る数（座標、標高、`prominence`、`col_margin_px`、`analysis_count`、`expected_count`、`AltM`）は、すべて `_num` を通す。[7.1.3](#713-関数の細部)の `read_merged_peak` と 7.5 の `read_summits_list` は `+35.10`・`035.1`・`+12` を通すが、`JsonNumber` は書き出す側が `text` をそのまま書く型で、そのままでは JSON として読めなくなる。正規の字句は変えず、10 進の値と末尾の `0` も変えない（[HLD 4.9.2](30_HLD.md#492-処理の流れ)の 4 が「10 進の値を変えずに（末尾の 0 の有無は問わない）」と字句の変化を許す）。[7.3.3](#733-関数の細部)の `_check_peak_lexemes` が正規でない座標の字句を止める（[HLD 4.18.2](30_HLD.md#4182-処理の流れ)が文字列をそのまま数として書くため）のとは作りが違う。`merged_peak.geojson` から写すゾーンのジオメトリは、JSON として読んだ字句なので通さない。
- `_encode_json(value: object) -> str`: [7.3.3](#733-関数の細部)の `write_merged_peak_geojson` の `_encode` を、この回の値の型に広げたもの（7.3 の内部の関数は呼べない〈[1.2](#12-lld-の規約)〉ので 7.5 に持つ）。`dict` は `{` とキーの順に `json.dumps(key)`・`:`・値を `,` でつないだものと `}`。`list`・`tuple` は `[`・要素を `,` でつないだもの・`]`。`cmp5_common.JsonNumber` は `text` のまま。`str` は `json.dumps(value)`（既定の `ensure_ascii=True`。ASCII の外の字は `\uXXXX`）。`bool` は `true`・`false`（`int` より先に見る）。`None` は `null`。`int` は `str(value)`（`points`・`sota_points`・`new_points`・`years`・`year`・`row`）。`float` は `json.dumps(value, allow_nan=False)`（`dominant_peak_dist_m`。`1234.6` は `1234.6`、`0.0` は `0.0`。`NaN` と無限大は `ValueError`）。ほかの型は `TypeError`。空白を書かない。

手順:

1. **並び**（[HLD 4.9.2](30_HLD.md#492-処理の流れ)の 4、[FR-009](20_SRS.md#fr-009-sotaリスト突合match_status-判定)の「複数登録の警告ログ・出力順序」、[DEC96](30_HLD.md#494-設計判断)「フィーチャはピークごとに CSV の行の順に並べる」。点と線は対にして置く: [DEC135](30_HLD.md#4194-設計判断)「除外の属性は鍵と終点の座標でそろえる」の理由の文が、削除のサミットの点とそれへの線を「`SummitCode` の順に対で置く」と読んでいる）。次の 3 つの塊をこの順に並べる。
   1. `status(p) != 'ambiguous'` のピークを `peaks` の鍵の順に、ピークごとに次の順に置く。ピークの点、コルの点、AZ、delete判定ゾーン、ピークとコルを結ぶ線、（`matched` なら）AZ の中のサミット `activation.peak_summits[p][0]` の点とそれへの `coord_diff`、`deletion.dominant` でこのピークを主ピークに選んだサミットのうち `attrs.summits[code].category == 'delete'` のものを `code` の文字列の順に、点とそれへの `coord_diff` の対。
   2. `deletion.unmatched` のサミットの点を `code` の文字列の順に（`deletion.unmatched` は受け取った順なので並べ直す）。
   3. `attrs.groups` の順（`group_id` の順）に、組ごとに、ピーク `g.pixel` の点、コルの点、AZ、delete判定ゾーン、ピークとコルを結ぶ線、`g.az_codes` の順に AZ の中のサミットの点とそれへの `coord_diff` の対、`g.held_codes` の順に保留した削除の候補の点とそれへの `coord_diff` の対。

   コルの点とピークとコルを結ぶ線は、`r['key_col_resolved'] == 'true'` で `decimal.Decimal(col_lat)` と `decimal.Decimal(col_lon)` がどちらも 0 でないピークにだけ置く（[7.3.3](#733-関数の細部)の `build_peak_features` と同じ条件。片方だけ 0 も置かない。[DEC100](30_HLD.md#494-設計判断)「海面で確定したコルは点にせず、XLSX でも空欄にする」）。`r = peaks[p].values`。
2. **ジオメトリ**。ピークの点は `{'type': 'Point', 'coordinates': [_num(peak_lon), _num(peak_lat)]}`、コルの点は `[_num(col_lon), _num(col_lat)]`、サミットの点は `[_num(s.lon), _num(s.lat)]`。線は `{'type': 'LineString', 'coordinates': [<ピークの点の座標>, <相手の点の座標>]}`（相手はコルの点か、サミットの点）。AZ と delete判定ゾーンは `zones[p].activation.geometry`・`zones[p].delete.geometry` をそのまま（[7.3.3](#733-関数の細部)の `build_peak_features` と同じく、`merged_peak.geojson` のスタイルのプロパティは写さない）。Feature は `{'type': 'Feature', 'properties': <プロパティ>, 'geometry': <ジオメトリ>}` の順。
3. **プロパティのキーと順**（**Ruling**: [FR-009](20_SRS.md#fr-009-sotaリスト突合match_status-判定)の「各フィーチャのプロパティ」の各表の行の順に、続けて「全フィーチャ共通の確認用属性」の表の 10 個を表の順に。同じ入力から同じ文字列にするために順を 1 つに決める。表に無いものは書かない〈[HLD 4.9.2](30_HLD.md#492-処理の流れ)の 4 の「プロパティ」〉）。共通の 10 個は `review_reason`・`review_group_id`・`review_decision`・`review_note`・`application_exclusion`・`exclusion_note`・`pending_applications`・`pending_match`・`pending_note`・`pending_return`。
   - `peak`: `feature_type`・`category`・`match_status`・`summit_code`・`summit_name`・`summit_name_jp`・`peak_elev`・`prominence`・`stability`・`key_col_resolved`・`points`・`is_band_change_candidate`・`rationale`・`analysis_count`・`expected_count`・`municipality`・`region_name`。
   - `key_col`: `feature_type`・`category`・`summit_code`・`col_elev`・`points`・`col_margin_px`・`municipality`・`region_name`。
   - `summit`: `feature_type`・`category`・`match_status`・`summit_code`・`summit_name`・`summit_name_jp`・`sota_alt_m`・`sota_points`・`rationale`・`municipality`・`region_name`・`dominant_peak_code`・`dominant_peak_dist_m`。
   - `activation_zone`: `feature_type`・`category`・`summit_code`・`area_complete`・`points`。
   - `delete_zone`: `feature_type`・`category`・`summit_code`・`area_complete`。
   - `peak_col_link`: `feature_type`・`category`・`summit_code`。
   - `coord_diff`: `feature_type`・`category`・`summit_code`・`match_status`。
4. **値**（`a = attrs.peaks[p]`）。
   - ピークの点: `category = a.category`、`match_status = status(p)`、`summit_code` は `matched` なら AZ の中のサミットの `code`、`new`・`dominant` なら `codes[p]`、`ambiguous` なら空文字（仮のコードも付けない）。`summit_name` は `matched` なら AZ の中のサミットの `name`、ほかは空文字。`summit_name_jp = a.summit_name_jp`。`peak_elev = _num(r['peak_elev'])`。`prominence` は `r['key_col_resolved'] == 'true'` なら `_num(r['prominence'])`、ほかは `None`（キーは残す）。`stability = r['stability']`（文字列）。`key_col_resolved = (r['key_col_resolved'] == 'true')`。`points = a.points`、`is_band_change_candidate = a.is_band_change_candidate`、`rationale = a.rationale`。`analysis_count = _num(r['analysis_count'])`。`expected_count` は空文字なら `None`、ほかは `_num(...)`。
   - 所在地: ピークの点は `regions.locations[('peak', p)]`、コルの点は `regions.locations[('col', p)]`（コル自身の座標の照合。親の継承ではない）、サミットの点は `regions.locations[('summit', code)]`。`municipality = loc.municipality`、`region_name` は `loc.region` が `None` なら空文字、そうでなければ `loc.region.region_name`。
   - コルの点: 親のピークの `category = a.category`・`summit_code`（ピークの点と同じ値）・`points = a.points`、`col_elev = _num(r['col_elev'])`、`col_margin_px = _num(r['col_margin_px'])`。
   - AZ: 親の `category`・`summit_code`・`points`、`area_complete = zones[p].activation.area_complete`。delete判定ゾーン: 親の `category`・`summit_code`、`area_complete = zones[p].delete.area_complete`。ピークとコルを結ぶ線: 親の `category`・`summit_code`。
   - サミットの点（`t = attrs.summits[code]`、`s` はそのサミット）: `category = t.category`、`match_status = t.match_status`、`summit_code = code`、`summit_name = s.name`、`summit_name_jp = t.summit_name_jp`、`sota_alt_m = _num(s.alt_m)`、`sota_points = t.sota_points`、`rationale = t.rationale`。`dominant_peak_code` は `t.match_status == 'delete'` なら `t.dominant_peak_code`（主ピークが `ambiguous` のときは空文字のまま）、ほかは `None`（SRS の「それ以外は空欄」。`SummitAttrs` は空文字で持つので、ここで `None` に直す）。`dominant_peak_dist_m = t.dominant_peak_dist_m`（丸め済みの `float` か `None`。`float` はそのまま JSON の数として書く）。
   - `coord_diff`（親のピーク `p`、終点のサミット `code`）: `category` は終点のサミットの `t.category`、`summit_code` は親のピークの点の `summit_code`、`match_status = status(p)`。**Ruling**: [FR-009](20_SRS.md#fr-009-sotaリスト突合match_status-判定)の per-feature の割り当てルール（「親ピーク→matched summit は親ピーク継承、親ピーク→delete summit は `delete`、ambiguous 親からの線は `review`」）と「`coord_diff` の理由は終点登録」は、どちらも終点のサミットの属性と一致するので、1 つの決まりで書ける。
   - 確認用の属性: ピークの点とその地形のフィーチャ（コルの点・AZ・delete判定ゾーン・ピークとコルを結ぶ線）は `a.review_reason`・`a.review_group_id`、サミットの点は `t.review_reason`・`t.review_group_id`、`coord_diff` は `review_reason = t.review_reason`・`review_group_id = a.review_group_id`（親のピークから）。`review_decision`・`review_note`・`application_exclusion`・`exclusion_note` はすべて空文字、`pending_return` はすべて `False`（[derive_attributes](#derive_attributes)の「定数の確認用の属性」）。
5. **申請済みの属性の写し先**（[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「申請済みの判定」の 6「同じ行のフィーチャへ写す」、DEC135 の範囲）。行の鍵 `k` の `pending.rows.get(k)` が `None` なら `pending_applications = []`・`pending_match = ''`・`pending_note = ''`、あれば `list(row.applications)`・`row.match`・`row.note`。鍵とフィーチャは次のとおり。
   - `('peak', p)`: 並びの 1 のピーク `p` の点・コルの点・AZ・delete判定ゾーン・ピークとコルを結ぶ線と、`matched` なら AZ の中のサミットの点とそれへの `coord_diff`。
   - `('summit', code)`: 並びの 1 の削除のサミットの点とそれへの `coord_diff`、並びの 2 の `unmatched` のサミットの点。
   - 並びの 3（保留組）のフィーチャは行の鍵を引かず、すべて `[]`・`''`・`''`（[match_pending_applications](#match_pending_applications)の当てる表で、`review` には申請を当てない）。
   - **Ruling**: このプログラムは各フィーチャをどの行のために作ったかを知っているので、DEC135 の「同じ `summit_code` と `category`、終点の座標」で探し直さない。範囲は DEC135 と同じ。
6. `text` を組み立てる。1 行目 `{"type":"FeatureCollection","metadata":<metadata の _encode_json>,"features":[`、続けて Feature を 1 行に 1 つ（最後のほかは行末に `,`）、最後の行 `]}`。どの行も LF で終える。Feature が 0 のときは 1 行目と最後の行だけ。BOM・CR・`crs` を書かない。最上位のキーの順は `type`・`metadata`・`features`（[HLD 4.9.2](30_HLD.md#492-処理の流れ)の 4）。行の形は [7.3.3](#733-関数の細部)の `write_merged_peak_geojson` と同じにする（差分を行単位で見られる）。
7. `SummitFeatures(<並べた Feature の list>, <text>)` を返す。

##### build_summit_sheets

`build_summit_sheets(features: list[dict]) -> openpyxl.Workbook`

[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「出力の組み立て」の 5「`merged_summit.xlsx` を組み立てる」と、[HLD 4.12.2](30_HLD.md#4122-処理の流れ)の 1〜5 の規則（[DEC110](30_HLD.md#4124-設計判断)「列の値は行を生む点と鍵で結んだフィーチャから取る」、[DEC111](30_HLD.md#4124-設計判断)「2 つの一覧は同じ規則を別々に実装し、同値の試験でそろえる」）である。`features` は `build_summit_features` の `SummitFeatures.features`。

**`Workbook` を返す（Ruling）**: [HLD 3.5.3](30_HLD.md#353-関数)の表は返すものを「シートの行」とするが、処理の正本の欄が [HLD 4.12.2](30_HLD.md#4122-処理の流れ)の 1〜5 で、4「セルを書く」のセルの型と表示形式と 5「シートを組み立てる」のシートの名前と文までがこの関数の受け持ち。それを運ぶ形を `openpyxl.Workbook` にして、`write_summit_outputs` は保存だけにする。UT がセルの `data_type` と `number_format` を直接確かめられる。**結ぶ相手は、自分が作ったフィーチャから探す**（[HLD 4.9.2](30_HLD.md#492-処理の流れ)の 5 の「結び付かない行」、[DEC114](30_HLD.md#4124-設計判断)「結び付かない行があればエクスポートを止める」）。`Attributes` や判定の結果から行を直接作らない。文書のプロパティ（作成日時など）は触らない（[#188](https://github.com/jj1xgo/findsummits/issues/188)「XLSX の文書のプロパティを `NFR-003` の内容に入れるか」で決める。`openpyxl` の既定のまま）。列の幅・書式・固定の枠も触らない（[HLD](30_HLD.md#4122-処理の流れ)に定めが無く、DEC111 の同値の試験がセルの値と表示形式とシートの名前と順を比べるため）。

止まり方は、結べない行か取り元のプロパティが無いものを XS1、値を変えずに書けない文字列を XS2 で止まる（[7.5.4](#754-メッセージ文面)。どちらも `common.log_error` の後に `sys.exit(common.EXIT_ERROR)`。書き出しの前なので、[DEC93](30_HLD.md#494-設計判断)「入力の誤りは書かずに止め、不備ゲートは書いて止める」と同じく何も書かずに止まる）。

内部の関数（モジュールの最上位）:

- `_index_features(features: list[dict]) -> dict[tuple[str, str, str], list[dict]]`: 鍵は `(feature_type, 鍵の名前, 鍵の値)`、鍵の名前は `'summit_code'` と `'review_group_id'`。値は、その鍵のフィーチャを `features` の順に並べた `list`。**鍵の扱い**（argon の並走の I2。2026-11-03）: 鍵の値が空でない `str` のフィーチャだけを入れる（保留組の地形のフィーチャは `summit_code` が空文字なので、ピークの点の行の索引に入らない。入れると、保留組が 1 組のとき空文字の鍵で別の行に黙って結ばれる）。フィーチャに `properties`・`feature_type` が無いときは `KeyError` にせず、索引に入れない。
- `_cell_text_problem(value: str) -> str | None`: `openpyxl.cell.cell.ILLEGAL_CHARACTERS_RE.search(value)` が当たれば `書けない制御文字を含む`、`len(value) > 32767` なら `32767 字を超える`、どちらでもなければ `None`（制御文字を先に見る）。
- `_write_cell(ws, row: int, col: int, value: object, number_format: str | None) -> str | None`: セルを書く（手順 4）。文字列が書けないときは、書かずに `_cell_text_problem` の文を返し（呼ぶ側が問題として控える）、書いたときと空のセルのときは `None` を返す。

手順:

1. **行を生む点を選ぶ**（[HLD 4.12.2](30_HLD.md#4122-処理の流れ)の 1、[DEC109](30_HLD.md#4124-設計判断)「行を生む点はバッチから変わらない属性で選ぶ」）。`features` を並びのまま見て、`feature_type == 'peak'` で `match_status` が `new`・`dominant`・`matched` の点（行の種類 `'P'`）と、`feature_type == 'summit'` で `match_status` が `delete`・`unmatched`（`'S'`）・`ambiguous`（`'A'`）の点を、その順のまま拾う。行はこの順に並べる（[DEC97](30_HLD.md#494-設計判断)「XLSX の行は行を生む点の順に並べる」）。`properties` か `feature_type`・`match_status` が無いフィーチャは選ばない。
2. **結ぶ**（4.12.2 の 2）。先に `_index_features` で索引を作る。
   - `'P'` の行: 同じ `summit_code` の `key_col`（取り元 `'col'`。0 個か 1 個）と `activation_zone`（`'az'`。1 個）。`match_status == 'matched'` なら、同じ `summit_code` で `match_status == 'matched'` の `summit`（`'az_summit'`。1 個）。
   - `'A'` の行: 同じ `review_group_id` の `peak`（`'peak'`。1 個）、`key_col`（0 個か 1 個）、`activation_zone`（1 個）。
   - `'S'` の行: 結ばない。
   - 行を生む点自身の鍵（`'P'` の行の `summit_code`、`'A'` の行の `review_group_id`）が空文字か、鍵のプロパティが無いときは、相手を引かず、結ぶ相手が 0 個の問題として控える（1 個が要るものについて）。
   - 数が合わない行（`key_col` が 2 個以上、ほかが 0 個か 2 個以上）は、行を生む点ごとの問題として控える。
3. **列の値を取る**（4.12.2 の 3）。列の順（`_SHEET_COLUMNS`）に、その行の種類の `_SHEET_SOURCES[列][種類]` を引く。`None` の列と、取り元のフィーチャが 0 個の列（`key_col` が 0 個の `'col'` の列、`matched` でないピークの行の `'az_summit'` の列）は空にする。取り元のフィーチャが 1 個なら、取るものがプロパティの名前なら `properties[名前]`、`'lat'`・`'lon'` なら `geometry['coordinates']` の 2 番目・1 番目（`JsonNumber`）を取る。結ぶ相手が数が合わなかったものは、値を取らない。**取り元のフィーチャのプロパティに名前が無い**ときは、問題として控える（値が `None` か空文字なのは、無いことに当たらない）。
4. **セルを書く**（4.12.2 の 4、[DEC112](30_HLD.md#4124-設計判断)「空文字と null はどちらも空のセルにする」、[DEC104](30_HLD.md#494-設計判断)）。`_write_cell` は、値が `None` か空文字か、3 で空とした列は、セルを置かない（`ws.cell` を呼ばない）。`bool` は文字列の `true`・`false` にする（`bool` は `int` の子なので、`int` より先に見る。逆にすると数のセル 1・0 になる）。`cmp5_common.JsonNumber` は `decimal.Decimal(v.text)` の数のセルにする。`int`・`float` はそのまま数のセルにする。表示形式は `_NUMBER_FORMATS` の列だけに付ける（数のセルにだけ。ほかの数には付けない）。`str`（`bool` の文字列を含む）は、置く前に `_cell_text_problem` を見て、当たれば問題として控える。置くときは `cell.value = s` の後に `cell.data_type = 's'` にする（**Ruling**: `openpyxl` は `=` で始まる文字列を式として書く〈`data_type` が `'f'`〉。[FR-009](20_SRS.md#fr-009-sotaリスト突合match_status-判定)の「登録変更リスト由来の文字列は…コードとして実行しない」と同じ扱いを、SOTA サミットリストの名前などにも当てる。見出しと「出典」の文にも同じ）。改行は文字列のまま残す。
   - **書けない文字列は暫定で止める（Ruling。持ち主の決定、2026-11-03）**: `openpyxl` 3.1.5 は、制御文字を含む文字列で `IllegalCharacterError` を上げ、32,768 字以上の文字列は代入の時に黙って 32,767 字に切り詰める。HLD 4.9.3 にこの場合の行は無いので、値を黙って変えず、例外の生の出力にもしないよう、すべての行を見てから XS2 で止まる（32,767 字ちょうどは書ける）。HLD での扱いは [#330](https://github.com/jj1xgo/findsummits/issues/330)「SOTA サミットリストなどの文字列が XLSX に値を変えずに書けないときの扱いを HLD 4.9.3 に決める」で決め、決まったらこの Ruling と XS2 を直す。
5. **止まる**。手順 2〜4 で控えた問題がすべての行を見た後に 1 つ以上あれば、XS1 の問題（結べない相手と取り元のプロパティ）があれば XS1 だけを、なければ XS2 を出して止まる（プログラムの誤りを先に直すため。XS1 と XS2 の両方に当たるときは XS1 だけ）。当たったものは省かずすべて並べる（[HLD 4.9.3](30_HLD.md#493-異常系)の「すべて」。件数と最初の数件にしない）。並びは行を生む点の順、同じ点の中は列の順（XS1 は結べない相手を先に、取り元のプロパティが無い列をその後に）。
6. **シートを組み立てる**（4.12.2 の 5、[DEC115](30_HLD.md#4124-設計判断)「データのシートは『サミット一覧』、最後のシートは『出典』」、[DEC102](30_HLD.md#494-設計判断)「`merged_summit.xlsx` にも出典のシート」）。`wb = openpyxl.Workbook()`、`wb.active.title = _SHEET_NAME`、1 行目に `_SHEET_COLUMNS` の見出し、2 行目から 1 の順に 1 行ずつ。`wb.create_sheet(_SOURCE_SHEET_NAME)` の `A1` に `_SOURCE_SHEET_TEXT`。シートは 2 つだけ。`wb` を返す。行を生む点が 0 個なら、見出しの 1 行だけのシートと「出典」を返す。

##### write_summit_outputs

`write_summit_outputs(text: str, workbook: openpyxl.Workbook, results_dir: str) -> None`

[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「出力の組み立て」の 6「書く」である（[DEC101](30_HLD.md#494-設計判断)「2 つの出力はそろって置くか、どちらも置かない」）。`text` は `build_summit_features` が返した `SummitFeatures.text`、`workbook` は `build_summit_sheets` が返した `openpyxl.Workbook` で、この関数は組み立て直さず、書くだけにする。出力は `<results_dir>/merged_summit.geojson` と `<results_dir>/merged_summit.xlsx`、一時ファイルは [2.3](#23-ファイルの名前と書き方)の一時ファイルの決まりで、同じディレクトリの `merged_summit.geojson.tmp` と `merged_summit.xlsx.tmp`（名前は固定）。ディレクトリ（`results/`）は作らない（`merged_peak.csv` の置き場として、この時点であるため。無ければ `open` の失敗で SW1）。

1. GeoJSON の一時ファイルを書く。`open(tmp, 'w', encoding='utf-8', newline='\n')` で開き、`text` を書き、`flush()`、`os.fsync(f.fileno())`、閉じる。
2. XLSX の一時ファイルを書く。`open(tmp, 'wb')` で開き、`workbook.save(f)`、`flush()`、`os.fsync(f.fileno())`、閉じる（`openpyxl` 3.1 の `Workbook.save` は `ZipFile` に渡されたファイルオブジェクトへ書き、閉じない。閉じるのはこの関数）。
3. 本来の名前へ置き換える。`xlsx_started = True` にしてから `os.replace(<xlsx の一時>, <xlsx>)`、続けて `geo_started = True` にしてから `os.replace(<geojson の一時>, <geojson>)`（この順。HLD の 6「書く」）。`xlsx_started`・`geo_started` は、置き換えの呼び出しに入る直前に立て、「中断」の片づけが、置き換えが済んだかを一時ファイルの有無で調べるために使う。XLSX の置き換えが済んだら、以降の `OSError` で消せるように `placed_xlsx = True` にする。2 つ目の置き換えまで済んだら `done = True` にする。

**失敗**: どの段の `OSError` も（`workbook.save` が上げる `OSError` を含む）、次の順に片づけて止まる。

1. 2 つの一時ファイルを `os.remove` で消す（無いものと、消せない誤りは無視する。[2.3](#23-ファイルの名前と書き方)の決まり）。
2. `placed_xlsx` が真なら、置いた `merged_summit.xlsx` を `os.remove` で消す。消せたら 3 の SW1。消せなければ（`OSError`）3 の SW2 にする。
3. SW1 か SW2 を `common.log_error` で出して `sys.exit(common.EXIT_ERROR)`。`{path}` は失敗した段の出力の本来の名前の絶対パス（一時ファイルの段の失敗でも `merged_summit.geojson` か `merged_summit.xlsx`。[7.2.3](#723-関数の細部)の `write_merged_peak` の MF1 と同じ）、`{reason}` は [2.1.4](#214-メッセージ文面)のとおり。SW2 の `{xlsx_path}`・`{xlsx_reason}` は、消せなかった `merged_summit.xlsx` の絶対パスとその理由。

**中断**: `OSError` 以外の例外で抜けるとき（`SignalStop`〈[2.1.3](#213-関数の細部)の `_on_signal` が `SIGINT`・`SIGTERM` で上げる〉、`workbook.save` が上げる `OSError` 以外の例外）と、`OSError` の片づけの途中で `SignalStop` が上がったときも、止める前に片づける。作りは、本体を `try` で囲み、`OSError` を捕まえる `except` の後に `finally` を置く。`OSError` の `except` は、SW1 か SW2 を出し終えて `sys.exit` を呼ぶ直前に `handled = True` にする。`finally` は、`done` も `handled` も偽のときだけ、次の順に片づける。

1. 置き換えが済んだ出力を決める（一時ファイルを消す前に決める）。出力ごとに（XLSX と GeoJSON。`xlsx_started` と `xlsx_path`・`xlsx_tmp`、`geo_started` と `geo_path`・`geo_tmp` の組）、その組の `*_started` が真で、一時ファイルがもう無い（`os.path.lexists(<一時ファイル>)` が偽。置き換えが済んで一時ファイルが本来の名前になった）ものを、置いた出力とする。置き換えの呼び出しに入る前に止まったときは一時ファイルがまだあるので、置いた出力に入れず、本来の名前のファイルには触れない。
2. 2 つの一時ファイルを `os.remove` で消す（無いものと、消せない誤りは無視する）。
3. 1 で決めた置いた出力を、XLSX、GeoJSON の順に `os.remove` で消す。無いもの（`FileNotFoundError`）は無視する。ほかの `OSError` で消せなければ、SW3 を `common.log_warning` で出して次へ進む（`sys.exit` しない。止まる原因は中断で、終了コードは共通部品が決める）。

抜けた例外はそのまま伝え、置き換えない（`SignalStop` を捕まえない。[1.2](#12-lld-の規約)）。`OSError` の片づけの途中で `SignalStop` が上がったときは、`handled` が偽のままなので、`finally` が上の 1〜3 をやり直す（片づけは何度行っても同じ結果になる）。`done` が真（2 つとも置き終えた）ときは、片づけない。

**Ruling**:

- 中断でも片づける。HLD の [DEC101](30_HLD.md#494-設計判断)「2 つの出力はそろって置くか、どちらも置かない」は、XLSX の置き換えと GeoJSON の置き換えの間で止まっても守る。[7.4.3](#743-関数の細部)の `write_unresolved_list` が書く途中の `SignalStop` で一時ファイルを残してよいとしたのは出力が 1 つで、正規の名前のファイルが残らないため。7.5 は XLSX だけが正規の名前で残ると、利用者が片方だけを使うおそれがある。片づけたあとの『そろえて置いていない』は、[main](#mainmatch_summits)の SM4 の `{state}` が知らせる。
- 中断の片づけは、置いたかどうかを「フラグ」でなく「一時ファイルがもう無いか」で決める（spec-panel 7.5-5 の確認限定巡の指摘 1。持ち主が、許す残りにせず直すと決めた、2026-11-03）。`os.replace` が済んでからフラグを立てると、その間（数バイトコードの窓）に届いたシグナルで、置いた出力が残る。置き換えの呼び出しに入る前にフラグ（`xlsx_started`・`geo_started`）を立て、置き換えが済んだかは一時ファイルの有無で見れば、窓が無い（`os.replace` は一時ファイルを本来の名前にするので、済んだ後は一時ファイルが無い）。`OSError` の片づけの `placed_xlsx` は、そのまま（`OSError` は置き換えの呼び出しの結果で分かるため）。GeoJSON も同じ窓があるので、同じ見方で消す（2 つ目の置き換えが済んで `done` を立てるまでの間に止まったときも、2 つとも消す。『そろえて置いていない』と SM4 が知らせる）。
- 中断の片づけで消せなかったものは、SW3（`WARNING:`）で知らせる。SW2 と違い、`sys.exit` はしない（止まる原因は中断で、終了コード 128＋シグナルの番号と終わりの行は共通部品が書く）。消せなかったものは次のフェーズ4 の始まりに CMP3 も消す（[HLD 2.10.3](30_HLD.md#2103-フェーズのやり直し)）が、利用者が片方だけを使わないよう、いま知らせる。
- 中断の終了コードと SM4 を、子のプロセスで確かめる（UT-79。`SIGTERM` の 143 と `SIGINT` の 130）。シグナルは、置き換えの呼び出しの中（`os.replace` の差し替えが、本物を呼んだ直後に自分へ `SIGTERM` を送る）で当てるので、時機が決まり、安定する。共通部品の終了コードの決まりは `UT-common-19` が確かめる。
- 一時ファイルを書く順を GeoJSON → XLSX にした。HLD は置き換えの順（`merged_summit.xlsx` → `merged_summit.geojson`）だけを決める。どちらの順でも、本来の名前へ置く前に両方を書き終える。
- 置き換えの前（1・2）の失敗では、本来の名前のファイルに触れない。フェーズ4 の始まりに CMP3 が前回の 2 つの出力を消しているので（[HLD 2.10.3](30_HLD.md#2103-フェーズのやり直し)、[HLD 4.9.3](30_HLD.md#493-異常系)の表の後の段落）、残っているファイルは前回のものでなく、触らない方が単純である。
- SW2 を分けたのは、置いた `merged_summit.xlsx` を消せないと DEC101 の「どちらも置かない」が守れず、利用者が残った XLSX を知らずに使うおそれがあるため。2.3 の「消せない誤りは無視」は一時ファイルの決まりで、置いた出力にはかけない（[7.4.3](#743-関数の細部)の KW2 が、消せないことを知らせる前例）。

##### check_defect_gate

`check_defect_gate(peaks: dict[tuple[int, int], cmp5_common.MergedPeakRow], zones: dict[tuple[int, int], PeakZones], deletion: DeleteMatch, threshold: int) -> list[tuple[str, int]]`

[HLD 4.9.2](30_HLD.md#492-処理の流れ)の 9「書き出し、不備ゲートを検査する」の、書いた後に調べる不備ゲートの 3 条件（[FR-009](20_SRS.md#fr-009-sotaリスト突合match_status-判定)の「異常系」）である。`peaks` は `index_peaks_by_pixel` が返した表、`zones` は `match_zones_to_peaks` が返した表（`PeakZones.activation`・`delete` の `cmp5_common.ZoneFeature.area_complete` が `bool`〈[7.1.2](#712-型とデータ)〉）、`threshold` は設定の `unmatched_summit_threshold`（整数）。この関数は何も出さず、止まらない。

返すのは、当たった条件の `(種類, 件数)` を次の順に並べた `list`（当たらない条件は入れない。空なら不備なし）。種類の文字列は [FR-009](20_SRS.md#fr-009-sotaリスト突合match_status-判定)の印の名前に合わせた（Ruling: 文面と UT が同じ名前で指せる）。

1. `'unmatched_over_threshold'`: `len(deletion.unmatched) > threshold` のとき。件数は `len(deletion.unmatched)`。しきい値と同じ数は当たらない（SRS の「超える」）。
2. `'is_area_incomplete'`: AZ か delete判定ゾーンの `area_complete` が偽のピークの数が 1 以上のとき。1 つのピークは、AZ と delete判定ゾーンの片方が偽でも両方が偽でも 1 と数える。`peaks` の鍵の順に、`zones[p].activation.area_complete` と `zones[p].delete.area_complete` を見る。
3. `'is_key_col_unresolved'`: `peak.values['key_col_resolved'] != 'true'` のピークの数が 1 以上のとき。

`peak.match_status` が `ambiguous` のピークも、3 つの条件で数える（[FR-009](20_SRS.md#fr-009-sotaリスト突合match_status-判定)の「異常系」が、全ピーク検査から除外しないと決めている）。複数登録の組の数は条件に入れない（警告 MR1 だけで、止めない。[HLD 4.9.3](30_HLD.md#493-異常系)）。GT1 を出して終了コード 4 にするのは `main` である。

##### main（match_summits）

`main() -> None`（起動の部分）。[2.1.3](#213-関数の細部)の前置きの呼ぶ側の書き方の型と [7.3.3](#733-関数の細部)の `main` に従い、[HLD 3.5.3](30_HLD.md#353-関数)の `match_summits` の表の「呼ぶ順」のとおりに次の順に行う。パスはどれも `os.path.join(data_dir, …)` で作る（`data_dir` は `load_config` が絶対パスの検査を済ませている。[2.1.3](#213-関数の細部)の `load_config` の 2 と設定の表）。

1. `start = common.StartTime.now()`。
2. `args = _parse_args(sys.argv[1:])`。
3. `config = common.load_config(args.config, _CONFIG_KEYS_USED, ('data_dir',))`。`data_dir`・`log_dir`・`provisional_code_max_prefix`・`unmatched_summit_threshold`・`sota_geojson_version` の値を `config.values[<キー>].value` で取り出す（`sota_geojson_version` は `int` か `None`）。
4. `common.start_log(log_dir, config, 'match_summits', sys.argv[1:], start)`。ロックは掛けない（内部の起動口は CMP3 のロックの下で動く。[HLD 2.9.3](30_HLD.md#293-同時起動の排他)）。
5. `_config_opt` に [7.5.4](#754-メッセージ文面)の `{config_opt}` の値を入れる。決め方は [7.2.3](#723-関数の細部)の `main` の 5 と同じ（`config.path == common.DEFAULT_CONFIG_PATH` なら空の文字列、それ以外は `' --config ' + shlex.quote(config.path)`）。
6. `try` の前に `completed = False`、`code = common.EXIT_OK`、`written = False`、結果の要約の材料（下の「結果の要約」）を `None` で置く。`try` の中で次を行う。
   1. 表を読む。`merged_path = os.path.join(data_dir, 'results', 'merged_peak.csv')`。`try:` で `peaks = cmp5_common.index_peaks_by_pixel(cmp5_common.read_merged_peak(merged_path, cmp5_common.MERGED_PEAK_ALL_COLUMNS))`、`except cmp5_common.InputError as e:` で `common.log_error(e.what, _input_error_advice(e.symbol))` と `sys.exit(common.EXIT_ERROR)`。`peak_count = len(peaks)` を材料に入れる。
   2. ゾーンを読む。`geojson_path = os.path.join(data_dir, 'results', 'merged_peak.geojson')`。`try:` で `zones = cmp5_common.read_zone_features(geojson_path)`（`except` は 1 と同じ形）。続けて `peak_zones = match_zones_to_peaks(peaks, zones, os.path.abspath(geojson_path))`、`del zones`（ゾーンの並びを持ち続けない。[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「メモリ」の持つものは、ピークごとのゾーンの索引と表で、読んだ並びではない）。`InputError` を捕まえる `try` は、1 と 2 の 2 つだけにする（ほかの誤りを捕まえないため。[7.3.3](#733-関数の細部)の前置きと同じ）。
   3. 参照の入力を読む。`ref_dir = os.path.join(data_dir, 'ref')`。`summits_list = read_summits_list(os.path.join(ref_dir, 'summitslist.csv'))`（現役のサミットの数 `len(summits_list.summits)` と廃止済みの数 `summits_list.retired_count` を材料に入れる）。`updatelist = read_updatelist(find_updatelist(ref_dir))`（`updatelist.file_name` と `updatelist.row_count` を材料に入れる）。
   4. 境界を読み、索引を作る。`boundaries = read_boundaries(os.path.join(data_dir, 'boundaries', 'regions.geojson'), os.path.join(data_dir, 'boundaries', 'municipalities.geojson'))`。BN1・BN2 を出す（下の「警告を出す時機と順」）。`indexes = build_spatial_indexes(peak_zones, boundaries)`。
   5. AZ と delete判定ゾーンに突き合わせる。`activation = match_activation_zones(summits_list.summits, peaks, indexes.activation)`。AO2 を出す。`deletion = match_delete_zones([s for s in summits_list.summits if s.code not in activation.summit_peak], peaks, activation, indexes.delete)`（AZ に含まれないサミットだけを、サミットの順で渡す。[match_delete_zones](#match_delete_zones)が、呼ぶ側が `activation.summit_peak` に無いものを渡すと決めている）。UM1 を出す。
   6. 所在地と仮サミットコード。`regions = locate_regions(_region_points(peaks, summits_list.summits), boundaries, indexes)`。`codes = assign_provisional_codes(deletion.peak_status, peaks, regions.locations, provisional_code_max_prefix, boundaries.regions is None)`（`deletion.peak_status` は `new`・`dominant` のピークだけを持つ。[assign_provisional_codes](#assign_provisional_codes)が、`matched`・`ambiguous` のピークは渡さないと決めている）。RG1 を出す。エリアごとの仮サミットコードの数を材料に入れる。
   7. 属性。`names = read_sota_names(ref_dir, sota_geojson_version)`。SN1〜SN4 を出す。`attrs = derive_attributes(peaks, summits_list.summits, activation, deletion, codes, regions, names.names)`。PT1・MR1 を出す。`peak.match_status` ごとの数と `summit.match_status` ごとの数を材料に入れる。
   8. 申請済みの判定。`pending = match_pending_applications(updatelist, summits_list, peaks, activation, deletion, indexes.activation, attrs)`。UN1 を出す。取り込んだ申請の数 `pending.taken`、`pending_match` が `same` と `different` の候補の数、知らせる行の数 `len(pending.notices)` を材料に入れる。
   9. metadata。`now = datetime.datetime.now(datetime.UTC)`、`metadata = build_metadata(summits_list.ref_date, os.path.join(data_dir, 'tiles'), os.path.dirname(os.path.abspath(__file__)), updatelist, pending.notices, now)`。MT1・MT2 を出す。
   10. 組み立て。`summit_features = build_summit_features(peaks, peak_zones, summits_list.summits, activation, deletion, codes, regions, attrs, pending, metadata.items)`。`workbook = build_summit_sheets(summit_features.features)`（XS1・XS2 はこの中で止まる。`main` は何もしない）。
   11. 書く。`write_summit_outputs(summit_features.text, workbook, os.path.join(data_dir, 'results'))`（失敗はこの中で止まる）。続けて `written = True`。
   12. 不備ゲート。`defects = check_defect_gate(peaks, peak_zones, deletion, unmatched_summit_threshold)`。`defects` が空でなければ GT1 を出し、`code = common.EXIT_DEFECT`。`if` の外で（当たったときも当たらないときも）`completed = True`（不備ゲートでも 2 つの出力は書き終えているので、要約は終えた形にする。[2.1.3](#213-関数の細部)の前置きの「処理を終えて 0 以外の終了コードで終わるとき」と同じ形）。
7. `finally` で結果の要約を `common.log_info` で出す（下の「結果の要約」）。
8. `sys.exit(code)`。

`start_log` の前に止まる誤り（`_parse_args`・`load_config`）は、標準エラー出力だけに出て、ログファイルと `log_dir` を作らない（[HLD 3.5.3](30_HLD.md#353-関数)の「ここまでの誤りは、ログファイルを作らずに終了コード 2」）。

**Ruling（`build_metadata` に渡す値）**: `tiles_dir` は `$DATA_DIR/tiles/` の絶対パスで、`os.path.join(data_dir, 'tiles')`（末尾に `/` を付けない。`data_dir` は絶対パスなので、そのまま `os.path.join` する）、`repo_dir` はこのスクリプトのあるディレクトリ（`git describe` はリポジトリの中のどのディレクトリからでも同じ値を返す。[`_software_version`](#build_metadata)）、`now` は `build_metadata` を呼ぶ直前に取る UTC の時差付きの時刻（`generated_at` は「本 FR 実行時」の時刻で、ログの開始時刻〈ローカル時刻〉とは別に取る。時差の無い値を渡さない）。

**警告を出す時機と順**: 警告は、その材料を返す関数を呼んだ直後に、`common.log_warning(<1 行目>, <2 行目>)` で出す。HLD が時機を決めているもの（RG1 は `assign_provisional_codes` の後。[HLD 4.9.2](30_HLD.md#492-処理の流れ)の 7「地域と市区町村を照合する」）はそれに従う。**Ruling**: [HLD 4.9.2](30_HLD.md#492-処理の流れ)の 9「書き出し、不備ゲートを検査する」の後の段落（`unmatched` のサミットと複数登録の組と登録変更リストの知らせる行を「警告に並べる」）は、出す先の区分（通常のログか警告か）を挙げたもので、時機は決めていない。HLD も SRS も、種類の違う警告どうしの順を決めていない（決めているのは、RG1 を `assign_provisional_codes` の後に出すこと、UN1 を `updatelist_notices` と同じ並びで出すこと、MR1 の中身の並び）。そこで、呼ぶ順にそろえる。同じ入力から同じ並びになり（[HLD 5.3.2](30_HLD.md#532-処理の流れ)の「警告ログの並び」）、止まる場面（AO1・PN1・PN2・XS1・XS2）より前の警告がログに残り、材料を後まで持ち越さずに済む。並びは次のとおり（番号は上の 6 の手順）。

- 4: BN1 → BN2（`Boundaries.warnings` の順）。
- 5: AO2（`ActivationMatch.overlaps` の順。サミット 1 件ごとに 1 組）→ UM1（`DeleteMatch.unmatched` が空でなければ 1 組）。
- 6: RG1（`RegionMatch.outside` の順。点 1 つごとに 1 組）。
- 7: SN1〜SN4（`SotaNames.warnings` の順）→ PT1（`NullPoints` の三つの件数がすべて 0 なら出さない）→ MR1（`Attributes.groups` が空なら出さない）。
- 8: UN1（`Pending.notices` の順。知らせる行 1 件ごとに 1 組）。
- 9: MT1 → MT2（`Metadata.warnings` の順）。
- 12: GT1（`defects` が空でないとき）。

2 行目は、`warnings` の組（記号、1 行目）を持つもの（BN・SN・MT）は組の記号で [7.5.4](#754-メッセージ文面)の 2 行目を選ぶ。ほかは 7.5.4 の表の 2 行目の文。

- 無い層の点は RG1 に入らない。`locate_regions` が、`boundaries` の層が `None` なら照合せず、`outside` に入れない（その層は BN1・BN2 が受け持つ）。ある層の外の点は、もう一方の層が無くても RG1 に出る（`OutsidePoint.layers` は、ある層の名前だけ）。`main` は `outside` をそのまま出す。
- RG1 の `{status}`・`{codes}`（[7.5.4](#754-メッセージ文面)の RG1 の行）: 点がピーク（`point.kind == 'peak'`、`p = point.key`）のとき、`status = activation.peak_status.get(p) or deletion.peak_status[p]`（[build_summit_features](#build_summit_features)の「ピークの状態」と同じ式）。`{codes}` は、`status` が `new`・`dominant` なら `仮サミットコード <codes[p]>`、`matched`・`ambiguous` なら `AZ の中のサミット <activation.peak_summits[p] の code を順に、でつなぐ>`。点がコルのときの `{peak_lat}`・`{peak_lon}` は `peaks[point.key].values['peak_lat']`・`['peak_lon']`、サミットのときの `{code}` は `point.key`。
- `_region_points` を呼ぶのは `main` である（[locate_regions](#locate_regions)の送りの受け）。

**結果の要約**（`finally`。[HLD 5.7.2](30_HLD.md#572-処理の流れ)の 7「結果の要約」と、[HLD 4.9.2](30_HLD.md#492-処理の流れ)の 9「書き出し、不備ゲートを検査する」の後の段落。形は [2.2](#22-ログとメッセージの文面)の結果の要約）。要約の材料は、`try` の前に `None` で置き、上の 6 のそれぞれの手順の直後に入れる。止まった実行では、そこまでに入った材料だけを書く。

- 終えたとき（`completed` が真。不備ゲートの終了コード 4 も含む）は、3 行を次の順に出す: SM1（ピークとサミットの数と、`peak.match_status`・`summit.match_status` ごとの数）、SM2（エリアごとの仮サミットコードの数）、SM3（登録変更リストの数）。
- 途中で止まったとき（`completed` が偽）は、SM4 の 1 行だけを出す。`None` の材料は書かない。**Ruling**: [7.3.4](#734-メッセージ文面)の ZL2 は、まだ数えていない数を 0 と書くが、7.5 は書かない。0 件と、まだ数えていないこととを見分けるため（突合は材料の数が多く、どこで止まったかで分かる数が大きく違う）。7.3 は直さない。
- 材料と入れる時機: ピークの数（1 の後）、現役のサミットの数と廃止済みとして除いた数（3 の `read_summits_list` の直後。登録変更リストの読み込みで止まっても残す）、登録変更リストの採ったファイル名と申請の行の数（3 の `read_updatelist` の直後）、エリアごとの仮サミットコードの数（6 の後。`codes` の値 `<assoc>/<area_code>-<接頭の文字><2 桁の数>` の `-` の前を、文字列の順に）、`peak.match_status` ごとの数（`matched`・`ambiguous`・`dominant`・`new` の順。`activation.peak_status` と `deletion.peak_status` から数える）と `summit.match_status` ごとの数（`matched`・`ambiguous`・`delete`・`unmatched` の順。`attrs.summits` から数える）（7 の後。ピークの状態は 5 の後に分かるが、サミットの状態が `derive_attributes` の後なので、まとめて 7 の後に入れる）、取り込んだ申請の数と `pending_match` が `same`・`different` の候補の数（`pending.rows` の値の `match` で数える）と知らせる行の数（8 の後）。
- SM4 の `{state}`（出力の状態）: `written` が偽なら `merged_summit.geojson と merged_summit.xlsx はそろえて置いていない`（書き込みの失敗のときも同じ文。SW2 で XLSX が残ったときと両立させるため、「どちらも無い」とは書かない。残ったものは直前の SW2 が知らせる）。`written` が真なら `merged_summit.geojson と merged_summit.xlsx は書いた`（書いた後の不備ゲートの検査か GT1 の出力の間に、シグナルなどで止まったとき）。

##### _parse_args（match_summits）

`_parse_args(argv: Sequence[str]) -> _Args`（内部）。[7.3.3](#733-関数の細部)の `_parse_args` から `--mesh` を除いた受け方（`--config` だけを受ける。[HLD 2.4.5](30_HLD.md#245-内部引数)の「設定解決: `--config <絶対パス>` だけ」）で、最初に見つけた誤り 1 つで、[7.5.4](#754-メッセージ文面)のメッセージを `common.log_error` で出して `sys.exit(common.EXIT_USAGE)`。

1. `argv` を左から読む。`--config` なら、すでに出ていれば SA3（値を見る前に判定する）、最後の引数なら SA2、そうでなければ次の引数を値にして 2 つ進む（値は `-` で始まっていてもそのまま値にする）。ほかの引数（位置引数、知らない名前〈`--mesh` を含む〉、`=` の付いた形、`--help`、`--` だけ、空の引数）は SA1。
2. `--config` が無ければ SA4。
3. `--config` の値が `os.path.isabs` で偽なら（空を含む）SA5。値は正規化しない。
4. `_Args(config)` を返す。

#### 7.5.4 メッセージ文面

書き方は [2.2](#22-ログとメッセージの文面)。設定の誤り（CF1〜CF7）は [2.1.4](#214-メッセージ文面)、ログの場面（G1〜G7）と L1〜L3 は 2.2（L1〜L3 の `{program}` は `match_summits`）。引数の誤り（SA1〜SA5）、読み込み・突き合わせ・照合と採番・属性と申請済みの判定・組み立ての関数の材料が出すメッセージ、書き出しの関数のメッセージ（SW1〜SW3）、不備ゲート（GT1）、結果の要約（SM1〜SM4）は、この節の表に置く。7.1 の部品の誤り（MP1〜MP3・ZF1〜ZF4）の 1 行目は [7.1.4](#714-メッセージ文面)の `what` のまま、2 行目は `{redo}`（`_input_error_advice`）。

- `{path}`・`{reason}` は [7.5.3](#753-関数の細部)の前置きのとおり。`{dir}` は、`find_updatelist` では探した `$DATA_DIR/ref/` の絶対パス、`read_updatelist` では `{path}` の置き場のディレクトリの絶対パス、`read_sota_names` の SN1 では `geojson_v<版>` のディレクトリの絶対パス。`{detail}`・`{list}`・`{target}` は、メッセージごとに下に書いた文。
- `{arg}`・`{value}` は受け取った値を、2.2 の引用の決まり（`shlex.quote`）で書いたもの。`{option}` は `--config`。
- `{config_opt}` は [main](#mainmatch_summits) の 5 が決める値（[7.2.3](#723-関数の細部)の `main` の 5 と同じ。既定の設定ファイルなら空の文字列、そうでなければ、空白 1 つに続けて `--config <パス>`）。
- 案内の文（2 行目に入れる）:
  - `{redo}` は `scripts/run_pipeline.sh{config_opt} を --phase なしで起動して、フェーズ2 から通しでやり直す`（[7.3.4](#734-メッセージ文面)・[7.2.4](#724-メッセージ文面)と同じ文。[HLD 4.9.3](30_HLD.md#493-異常系)の「やり直しの案内」の 1 つ目の、`merged_peak.csv` と `merged_peak.geojson` の場面）。
  - `{rerun4}` は `scripts/run_pipeline.sh --phase 4{config_opt} を起動し直す`（`--phase 4` は引数なので、`{config_opt}` はその後ろに入れる。[7.4.4](#744-メッセージ文面)の `{redo_stage}` と同じ形）。
  - `{cmp1_rebuild}` は `venv/bin/python3 scripts/preprocess_boundaries.py --rebuild{config_opt} で地域と市区町村の GeoJSON を作り直し、venv/bin/python3 scripts/fetch_tiles.py{config_opt} を起動して取得完了の記録を作り直してから、{redo}`（[HLD 2.10.3](30_HLD.md#2103-フェーズのやり直し)の「フェーズ1」の CMP1 の作り直しの手順と、「フェーズ1 をやり直したら、フェーズ2 から通しでやり直す」の決まり〈除外リストやタイルが変わると、前回のフェーズ2 以降の結果は新しい入力と合わないため〉。[7.2.4](#724-メッセージ文面)の R1〜R3 の案内と同じ形。CMP1 が取得完了の記録も消すので、CMP2 の起動を添える）。
  - `{summits_advice}` は `SOTA サミットリスト CSV を提供元から落とし直して {path} に置いてから、{rerun4}`。
  - `{update_advice}` は `登録変更リストのページを元のまま保存し直して {dir} に置く（ブラウザの保存の種類によっては、HTML に作り直されて XHTML として読めなくなる）。直してから、{rerun4}`。
  - `{report_analysis}` は `AZ が互いに素であるという前提に反する、解析の欠陥の可能性がある。このメッセージを添えて解析の欠陥として起票し、原因を調べる`（[HLD 4.9.3](30_HLD.md#493-異常系)の AZ の重なりの行。確定したピークの AZ は互いに素であると [FR-009](20_SRS.md#fr-009-sotaリスト突合match_status-判定)が前提にするため、利用者が直せる入力の誤りではない）。

| 記号 | 場面 | 1 行目（`ERROR:` か `WARNING:` と空白 1 つの後） | 2 行目（`対処:` と空白 1 つの後） | 終了コード |
|---|---|---|---|---|
| MZ1 | `merged_peak.geojson` のゾーンが `merged_peak.csv` と食い違う | `merged_peak.geojson のゾーンが merged_peak.csv と食い違う: {path}: {list}`（`{list}` は [7.5.3](#753-関数の細部)の `match_zones_to_peaks` の 3 の順に、表に無いピークのゾーンは `{peak_lat},{peak_lon} の {kind}（ピークが merged_peak.csv に無い）`、欠けたピークは `{peak_lat},{peak_lon} の {kinds}（ゾーンが merged_peak.geojson に無い）` を `、` でつなぐ。`{kind}` は `activation_zone`・`delete_zone`、`{kinds}` は欠けた種類をこの順に `・` でつなぐ。緯度経度は入力の字句のまま） | `{redo}` | 1 |
| SS1 | SOTA サミットリスト CSV が無い | `SOTA サミットリスト CSV が無い: {path}` | `{summits_advice}` | 1 |
| SS2 | SOTA サミットリスト CSV を読めない | `SOTA サミットリスト CSV を読めない: {path}: {reason}` | `{path} の読み取りの権限と、UTF-8 で保存されていることを確かめるか、提供元から落とし直して {path} に置いてから、{rerun4}`（[HLD 4.9.3](30_HLD.md#493-異常系)の「必ず含める内容」が、読めないときも落とし直す案内を求めるため） | 1 |
| SS3 | SOTA サミットリスト CSV の書式が違う（基準日の行、見出し、CSV として読めない） | `SOTA サミットリスト CSV の書式が違う: {path}: {detail}`（`{detail}` は [7.5.3](#753-関数の細部)の `read_summits_list` の 1〜3 の文） | `{summits_advice}` | 1 |
| SS4 | `JA` で始まる行の値が読めない | `SOTA サミットリスト CSV の値が読めない: {path}: {detail}`（`{detail}` は 7.5.3 の `read_summits_list` の 4 の文） | `{summits_advice}` | 1 |
| SS5 | 同じ `SummitCode` の行が 2 つ以上 | `SOTA サミットリスト CSV に同じ SummitCode の行が 2 つ以上ある: {path}: {list}`（`{list}` は 7.5.3 の `read_summits_list` の 5 の文） | `{summits_advice}` | 1 |
| UX1 | 登録変更リストが無い | `登録変更リストが無い: {dir}（ファイル名が sota_updatelist_<4 桁の年>.xhtml の形のもの）` | `{update_advice}` | 1 |
| UX2 | 登録変更リストを読めない | `登録変更リストを読めない: {path}: {reason}` | `{path} の読み取りの権限を確かめてから、{rerun4}` | 1 |
| UX3 | 登録変更リストが XHTML として読めない（整形式でない、内部サブセットか実体の宣言がある） | `登録変更リストが XHTML として読めない: {path}: {detail}`（`{detail}` は 7.5.3 の `read_updatelist` の 1 の文） | `{update_advice}` | 1 |
| UX4 | 登録変更リストの表を読めず、使う列を見出しの文字で特定できない（表が無い、`rowspan`・`colspan` が使えず格子を作れない、年の表の題や見出しが無い、見出しの文字で列を引けない） | `登録変更リストの表を読めず、使う列を見出しの文字で特定できない: {path}: {detail}`（`{detail}` は 7.5.3 の `read_updatelist` の 2・4・5 の文） | `{update_advice}` | 1 |
| BD1 | 地域か市区町村の GeoJSON を読めない | `{target}の GeoJSON を読めない: {path}: {reason}`（`{target}` は `地域` か `市区町村`。`NaN` などは `{reason}` が `NaN は JSON の数でない`） | `{cmp1_rebuild}` | 1 |
| BD2 | 地域か市区町村の GeoJSON の書式が違う | `{target}の GeoJSON の書式が違う: {path}: {detail}`（`{detail}` は 7.5.3 の `read_boundaries` の 3 の文） | `{cmp1_rebuild}` | 1 |
| BN1 | 地域の GeoJSON が無い（`WARNING:`） | `地域の GeoJSON が無い: {path}。仮サミットコードのエリアがすべて ZZ になり、region_name が空文字になる（全国の実行では仮サミットコードの連番上限で止まりうる）` | `{cmp1_rebuild}` | 0 |
| BN2 | 市区町村の GeoJSON が無い（`WARNING:`） | `市区町村の GeoJSON が無い: {path}。municipality が空文字になる` | `{cmp1_rebuild}` | 0 |
| UN1 | 登録変更リストに知らせる行がある（`WARNING:`。知らせる行 1 件ごとに 1 組） | `登録変更リストの知らせる行: {kind}: {reason}: {where}、アクション {action}、山岳 ID か県名 {target}、申請者 {applicant}、申請日 {applied_on}、問題の値 {value}（全体で {total} 件）` | `止まらずに続ける。ページの元の行を確かめて、直すか放置するかを決める` | 0 |
| AO1 | 2 つ以上の確定したピークの AZ に含まれるサミットがある | `2 つ以上の確定したピークの AZ に含まれるサミットがある: {list}`（`{list}` は、当たったサミットすべてをサミットの順に、`{code}（{lat},{lon}）: {peaks}` として `；` でつなぐ。`{peaks}` は、そのサミットを含む AZ のピークすべて〈確定していないピークも含む〉を `peaks` の鍵の順に、`{peak_lat},{peak_lon}（key_col_resolved={値}）` として `、` でつなぐ。緯度経度は入力の字句のまま） | `{report_analysis}` | 1 |
| PN1 | 仮サミットコードの連番が上限を超えるエリアがある（地域の GeoJSON はある） | `仮サミットコードの連番が上限を超えるエリアがある（provisional_code_max_prefix={prefix}、1 エリアの上限 {limit} 件）: {list}`（`{prefix}` は今の設定の値、`{limit}` は `(ord(prefix) - ord('A') + 1) * 100`。`{list}` は、超えたエリアすべてをエリアの `{assoc}/{area_code}` の文字列の昇順に、`{assoc}/{area_code}（{count} 件、上限を {over} 件超える）` として `、` でつなぐ。`{count}` はそのエリアのピークの件数、`{over}` は `{count}` から `{limit}` を引いた件数） | `provisional_code_max_prefix を上げてから、{rerun4}` | 1 |
| PN2 | 地域の GeoJSON が無く、全ピークが `ZZ` のエリアに入って連番が上限を超える | `地域の GeoJSON が無いため、すべてのピークが ZZ のエリアに入り、仮サミットコードの連番が上限を超える（provisional_code_max_prefix={prefix}、1 エリアの上限 {limit} 件）: {list}`（`{prefix}`・`{limit}`・`{list}` は PN1 と同じ。`{path}` は入れない。`assign_provisional_codes` が受け取るのは地域の GeoJSON の有無だけで、無いファイルのパスは同じ実行の BN1 が出すため） | `{cmp1_rebuild}` | 1 |
| AO2 | 確定していないピークの AZ が重なり、2 つ以上の AZ に含まれるサミットがある（`WARNING:`。サミット 1 件ごとに 1 組） | `確定していないピークの AZ が重なる: {code}（{lat},{lon}）: {peaks}、含めた AZ のピーク {peak_lat},{peak_lon}`（`{peaks}` は AO1 と同じ形。`AzOverlap` の項目から作る） | `key_col_resolved=false のピークがあるので、続く不備ゲートで止まる。AZ に含めたピークのまま続ける` | 0 |
| RG1 | 地域か市区町村のどれにも入らない点がある（`WARNING:`。点 1 つごとに 1 組） | `地域か市区町村のどれにも入らない点: {kind} {lat},{lon}: 入らなかった層 {layers}: {what}`（`{kind}` は `ピーク`・`コル`・`サミット`。`{layers}` は `OutsidePoint.layers` を `・` でつなぐ。`{what}` は、サミットなら `サミット {code}`、コルなら `親のピーク {peak_lat},{peak_lon}`、ピークなら `match_status {status}、{codes}`。`{status}` は `peak.match_status`、`{codes}` は `new`・`dominant` なら `仮サミットコード <コード>`、`matched`・`ambiguous` なら `AZ の中のサミット <コードすべて を、でつなぐ>`。`{status}`・`{codes}` は [main](#mainmatch_summits) が渡す値） | `止まらずに続ける。点が海上や境界の外にあるか、地域と市区町村の GeoJSON が古いかを確かめる` | 0 |
| UM1 | `unmatched` のサミットがある（`WARNING:`。1 組） | `unmatched のサミットがある（{count} 件）: {list}`（`{list}` は、`DeleteMatch.unmatched` のサミットすべてをその順に、`{code}（{name}、{lat},{lon}）` として `、` でつなぐ。`{count}` は件数） | `止まらずに続ける。件数が unmatched_summit_threshold を超えると、続く不備ゲートで止まる。出力のそれぞれのサミットを確かめる` | 0 |
| SN1 | SOTA 既存サミット GeoJSON を使わない（`WARNING:`。1 組）。`sota_geojson_version` が未設定か、`geojson_v<版>` のディレクトリが無い | 未設定のとき `SOTA 既存サミット GeoJSON を使わない: 設定の sota_geojson_version が未設定。すべてのサミットの summit_name_jp が空文字になる`、ディレクトリが無いとき `SOTA 既存サミット GeoJSON を使わない: {dir} が無い。すべてのサミットの summit_name_jp が空文字になる`（`{dir}` はそのディレクトリの絶対パス） | `止まらずに続ける。山岳名が要るときは、sota_geojson_version を設定して $DATA_DIR/ref/geojson_v<版>/ に SOTA 既存サミット GeoJSON を置いてから、{rerun4}` | 0 |
| SN2 | SOTA 既存サミット GeoJSON のファイルが無いか、読めないか、FeatureCollection でない（`WARNING:`。ファイル 1 つごとに 1 組） | `SOTA 既存サミット GeoJSON を使わない: {path}: {reason}`（`{reason}` は [7.5.3](#753-関数の細部)の `read_sota_names` の 2 の文。ファイルが無いときは `ファイルが無い`、FeatureCollection でないときは `FeatureCollection でない`） | `止まらずに続ける。このファイルのサミットの summit_name_jp は空文字になる。ファイルを置き直してから、{rerun4}` | 0 |
| SN3 | SOTA 既存サミット GeoJSON の `name` を読めない Feature を飛ばした（`WARNING:`。ファイル 1 つごとに 1 組） | `SOTA 既存サミット GeoJSON の name を読めない Feature を飛ばした: {path}: {count} 件`（`{count}` は飛ばした件数） | `止まらずに続ける。飛ばした Feature の山岳名は使われない。name が コード(山岳名) の形になっているかを確かめる` | 0 |
| SN4 | SOTA 既存サミット GeoJSON の同じコードに違う山岳名がある（`WARNING:`。1 組） | `SOTA 既存サミット GeoJSON の同じコードに違う山岳名がある: {list}`（`{list}` は、コードを文字列の順に、`{code}（{jp}・{jp}）` を `、` でつなぐ。`{jp}` は違う山岳名を最初に現れた順に `・` でつなぐ） | `止まらずに続ける。該当するコードの summit_name_jp は空文字にした` | 0 |
| PT1 | 標高が算出表に無く、ポイントを null にしたピークかサミットがある（`WARNING:`。1 組。三つの件数がすべて 0 のときは出さない） | `標高が算出表に無く、ポイントを null にした: ピーク {n_peak} 件（{peak_list}）；サミット {n_summit} 件（{summit_list}）；is_band_change_candidate を false にした matched のピーク {n_band} 件（{band_list}）`（`{peak_list}` は `NullPoints.peaks` を `peaks` の鍵の順に `{peak_lat},{peak_lon}（peak_elev={peak_elev}）` として `、` でつなぐ。`{summit_list}` は `NullPoints.summits` をその順に `{code}（AltM={alt_m}）` として `、` でつなぐ。`{band_list}` は `NullPoints.band_false` をその順に `{peak_lat},{peak_lon}` として `、` でつなぐ。件数が 0 のものは `なし` と書く） | `止まらずに続ける。算出表に無い標高のポイントは null で、バンドの比べには使わない。出力の標高を確かめる` | 0 |
| MR1 | 1 つの AZ に 2 件以上の登録がある（`WARNING:`。1 組。`Attributes.groups` が空のときは出さない） | `1 つの AZ に 2 件以上の登録がある: {group_count} 組（AZ 内の登録 {az_count} 件、保留した AZ 外の削除候補 {held_count} 件）: {list}`（`{group_count}` は `groups` の件数、`{az_count}` は `az_codes` の長さの合計、`{held_count}` は `held_codes` の長さの合計。`{list}` は `groups` の順に、`{group_id}（ピーク {peak_lat},{peak_lon}、AZ 内 {az_codes}、保留した削除候補 {held_codes}）` を `；` でつなぐ。`{az_codes}`・`{held_codes}` は `、` でつなぎ、`held_codes` が空なら `なし`） | `止まらずに続ける。複数登録のフィーチャは category=review で、出力の末尾に review_group_id の順に並ぶ。登録の重なりを確かめる` | 0 |
| MT1 | `software_version` を求められない（`WARNING:`。1 組） | `software_version を求められない: {reason}。unknown を書く`（`{reason}` は [7.5.3](#753-関数の細部)の `_software_version` が返す理由の文のまま） | `止まらずに続ける。リポジトリの中の git が使えるか（git が入っているか、スクリプトのあるディレクトリがリポジトリの中か）を確かめてから、{rerun4}` | 0 |
| MT2 | `gsi_tile_latest_date` を求められない（`WARNING:`。1 組） | `gsi_tile_latest_date を求められない: {reason}。空文字を書く`（`{reason}` は 7.5.3 の `_tile_latest_date` が返す理由の文のまま。`PNG が 1 枚も無い` か `ディレクトリをたどれない: {path}: {reason}`） | `止まらずに続ける。標高タイルのディレクトリ（$DATA_DIR/tiles/）の読み取りの権限と、タイルを取得済みかを確かめてから、{rerun4}` | 0 |
| XS1 | `merged_summit.xlsx` の行を生む点に、結ぶべき相手が無いか 2 つ以上ある、または取り元のフィーチャにプロパティが無い（プログラムの誤り） | `XLSX の行を結べないか、取り元のプロパティが無い: {list}`（`{list}` は、当たった行を生む点すべてを行を生む点の順に `；` でつなぐ。1 つの点は `{what}: {items}`。`{what}` は、ピークの点なら `peak {lat},{lon}`（点の座標の 2 番目と 1 番目の `JsonNumber` の `text`）、サミットの点なら `summit {summit_code}`（`summit_code` のプロパティが無ければ `?`）。`{items}` は、同じ点の中の問題を、結べなかった相手を先に（ピークの点の行は `key_col`・`activation_zone`・`summit`、`ambiguous` のサミットの点の行は `peak`・`key_col`・`activation_zone` の順）、取り元のプロパティが無い列をその後に（`_SHEET_COLUMNS` の順）、`、` でつなぐ。結べなかった相手は `{feature_type} が {n} 個`（`{feature_type}` は `key_col`・`activation_zone`・`peak`・`summit`。`{n}` は結んだ個数）、欠けたプロパティは `{feature_type} のプロパティ {name} が無い`（`{feature_type}` は取り元のフィーチャの `feature_type`、無ければ取り元の名前。`{name}` は無かったプロパティの名前）） | `プログラムの欠陥として起票して調べる。このメッセージを添える` | 1 |
| XS2 | `merged_summit.xlsx` に、値を変えずに書けない文字列がある（暫定。持ち主の決定、2026-11-03。XS1 と同時に当たるときは XS1 だけを出す） | `XLSX に値を変えずに書けない文字列がある: {list}`（`{list}` は、当たった行を生む点すべてを行を生む点の順に `；` でつなぐ。1 つの点は `{what}: {items}`。`{what}` は XS1 と同じ。`{items}` は、同じ点の当たった列を列の順に `、` でつなぎ、`{column}（{why}）` と書く。`{column}` は列の名前、`{why}` は `書けない制御文字を含む` か `32767 字を超える`） | `入力のファイルの該当の値を直して、{rerun4}`（[#330](https://github.com/jj1xgo/findsummits/issues/330) で HLD の扱いが決まったら、この行を直す） | 1 |
| SA1 | 受け付けない引数 | `match_summits の知らない引数: {arg}` | `match_summits は run_pipeline が起動する内部の起動口。使える名前は --config（値は次の引数で渡す）` | 2 |
| SA2 | 値が無い | `{option} の値が無い` | `{option} の後に値を渡す` | 2 |
| SA3 | 同じ名前を 2 回 | `{option} を 2 回渡した` | `{option} は 1 回だけ渡す` | 2 |
| SA4 | `--config` が無い | `--config が無い` | `--config と設定ファイルの絶対パスを渡す` | 2 |
| SA5 | `--config` が絶対パスでない | `--config のパスが絶対パスでない: {value}` | `--config に設定ファイルの絶対パスを渡す` | 2 |
| SW1 | `merged_summit.geojson` か `merged_summit.xlsx` を書けない（一時ファイルと置いたファイルは消した） | `merged_summit.geojson か merged_summit.xlsx を書けない: {path}: {reason}。2 つの出力はどちらも置いていない` | `{dir} の空きと権限を確かめてから、{rerun4}`（`{dir}` は `results/` の絶対パス） | 1 |
| SW2 | 出力を書けず、置いた `merged_summit.xlsx` も消せない | `merged_summit.geojson か merged_summit.xlsx を書けない: {path}: {reason}。置いた merged_summit.xlsx も消せなかった: {xlsx_path}: {xlsx_reason}` | `{xlsx_path} を手で消し、{dir} の空きと権限を確かめてから、{rerun4}`（`{dir}` は SW1 と同じ） | 1 |
| SW3 | 中断（`SIGINT`・`SIGTERM` など）で、置いた出力を消せなかった（`WARNING:`。消せなかった出力 1 つごとに 1 組。`write_summit_outputs` の `finally` が出す） | `中断のため、置いた {name} を消せなかった: {path}: {reason}`（`{name}` は `merged_summit.xlsx` か `merged_summit.geojson`、`{path}` はその絶対パス） | `{path} を手で消してから、{rerun4}`（次のフェーズ4 の始まりにも消える） | 0（このメッセージは終了コードを決めない。止まる終了コードは共通部品が 128＋シグナルの番号にする） |
| GT1 | 不備ゲートの条件に当たった（`ERROR:`。`main` が出す。2 つの出力は書いてある） | `不備ゲートに当たった: {list}`（`{list}` は、`check_defect_gate` が返した条件をその順に `；` でつなぐ。1 つの条件は `{kind} {count} 件（確かめる列 {column}）`。`{kind}` は `unmatched_over_threshold`・`is_area_incomplete`・`is_key_col_unresolved`、`{count}` は返された件数、`{column}` は `_DEFECT_COLUMNS` の値。`unmatched_over_threshold` だけ、`（` の後に `unmatched_summit_threshold={threshold}、` を足す） | `merged_summit.geojson と merged_summit.xlsx は調査用に書いた。merged_summit.xlsx の確かめる列を見て原因を調べ、直してから、{rerun4}`。`defects` に `is_area_incomplete` があるときだけ、`確かめる列を見て` の後ろの `原因を調べ` の前に `、merged_summit.geojson の activation_zone と delete_zone の area_complete=false も見て` を足す（XLSX の `area_complete` 列は AZ の値だけで、delete判定ゾーンだけが不完結のときは全部 `true` になるため。[ADR-SRS-080](decisions/ADR-SRS-080-srs-section-4-5-second-review-read-errors-and-delete-zone-completeness.md) の 3） | 4 |

- MT1・MT2 の警告を出すのは [main](#mainmatch_summits) で、`build_metadata` は文面の材料（`Metadata.warnings`）だけを返す（BN1・BN2・SN1〜SN4 と同じ形）。2 行目は、`warnings` の組の記号を `main` が見て足す。XS1・XS2 は、`build_summit_sheets` が出して止まる（AO1・PN1・PN2 と同じ形）。
- AO2・RG1・UM1 の警告を出すのは [main](#mainmatch_summits) で、`match_activation_zones`・`locate_regions`・`match_delete_zones` は文面の材料（`ActivationMatch.overlaps`・`RegionMatch.outside`・`DeleteMatch.unmatched`）だけを返す（BN1・BN2 と同じ形）。AO2 は `overlaps` の順、RG1 は `outside` の順（ピーク → コル → サミット）、UM1 は 1 組。RG1 は `assign_provisional_codes` の後に出す。AO1・PN1・PN2 は、`match_activation_zones` と `assign_provisional_codes` が出して止まる。
- BN1・BN2 の 2 行目は、`read_boundaries` が返す `warnings` の組の記号を、[main](#mainmatch_summits) が見て足す（`warnings` が持つのは 1 行目だけ）。SN1〜SN4 も同じ形で、`read_sota_names` が返す `SotaNames.warnings` の組の記号を `main` が見て 2 行目を足す。
- SN1〜SN4・PT1・MR1 の警告を出すのは [main](#mainmatch_summits) で、`read_sota_names`・`derive_attributes` は文面の材料（`SotaNames.warnings`・`Attributes.null_points`・`Attributes.groups`）だけを返す（BN1・BN2・AO2 と同じ形）。出す時機と順は [main](#mainmatch_summits) の「警告を出す時機と順」が決める。PT1 は三つの件数がすべて 0 なら、MR1 は `groups` が空なら出さない。
- UN1 の項目は `Notice` の項目で、`{kind}` は `Notice.kind` の英語の名前のまま、`{where}` は `{year} 年の表の {row} 行目`（`row` が `None` の `unreadable_update` は `{year} 年の表`）、`{total}` は `Pending.notices` の件数（読み込みの知らせと照合の知らせを合わせた件数）。空の値は `（空）` と書く。UN1 を出すのは [main](#mainmatch_summits) で、出す順は `Pending.notices` の順（読み込みの知らせ `UpdateList.notices` は 1 回目の `read_updatelist` が、照合の知らせ〈`unknown_id`・`ambiguous_region`・`unmatched_add`〉は 3 回目の `match_pending_applications` が作り、後者が両方を 1 つの並びにする。[HLD 4.9.2](30_HLD.md#492-処理の流れ)の「申請済みの判定」の 7「知らせる行をまとめる」）。
- 知らせる行の `reason` の文（`Notice.reason`。UN1 の `{reason}` にもなる）:

| 定数 | 場面 | 文 |
|---|---|---|
| `_REASON_ACTION` | アクションの欄の語が違う | `アクションの欄の語が 追加・変更・削除 のどれでもない` |
| `_REASON_POSITION` | 追加の位置が読めない | `追加の位置が 緯度,経度 の形で読めない` |
| `_REASON_ID` | 変更・削除の山岳 ID が読めない | `山岳 ID が アソシエーション/地域コード-番号 の形で読めない` |
| `_REASON_ELEV` | 変更後の標高が読めない | `変更後の標高が数として読めない` |
| `_REASON_DATE` | 申請日が読めない | `申請日が読めない` |
| `_REASON_UPDATE` | Update の日付が読めない | `Update の日付が読めない` |
| `_REASON_UNKNOWN_ID` | 変更・削除の山岳 ID が SOTA サミットリストに無い | `山岳 ID が SOTA サミットリストに無い` |
| `_REASON_AMBIGUOUS_REGION` | 山岳 ID の地域コードが 2 つ以上のアソシエーションにある | `山岳 ID の地域コードが 2 つ以上のアソシエーションにあり、サミットを決められない` |
| `_REASON_UNMATCHED_ADD` | 追加の位置がどの AZ にも入らない | `追加の位置がどのピークの AZ にも入らない` |

通常のログ（[HLD 4.9.2](30_HLD.md#492-処理の流れ)の 9「書き出し、不備ゲートを検査する」の後の段落と [HLD 5.7.2](30_HLD.md#572-処理の流れ)の表の `match_summits` の行。2.2 の結果の要約の形。出す時機と材料は [main](#mainmatch_summits)の「結果の要約」）:

| 記号 | 行 | 文面 |
|---|---|---|
| SM1 | 結果の要約（ピークとサミット） | `結果の要約: ピーク {peaks} 件（matched {pm}・ambiguous {pa}・dominant {pd}・new {pn}）、現役のサミット {summits} 件（matched {sm}・ambiguous {sa}・delete {sd}・unmatched {su}。廃止済みとして除いた {retired} 件）` |
| SM2 | 結果の要約（仮サミットコード） | `結果の要約: 仮サミットコードの数（エリアごと）: {areas}`（`{areas}` は `{assoc}/{area_code} {n} 件` を文字列の順に `、` でつなぐ。0 件なら `なし`） |
| SM3 | 結果の要約（登録変更リスト） | `結果の要約: 登録変更リスト {file_name}、申請の行 {row_count} 件、取り込んだ申請 {taken} 件、pending_match が same の候補 {same} 件・different の候補 {different} 件、知らせる行 {notices} 件` |
| SM4 | 結果の要約（途中で止まった） | `結果の要約: 途中で止まった（{items}）。{state}` |

- 終えたとき（不備ゲートの終了コード 4 も含む）は SM1〜SM3 をこの順に出す。途中で止まったとき（`completed` が偽）は SM4 の 1 行だけを出す。
- SM4 の `{items}` は、[main](#mainmatch_summits)が材料を入れた順に、入った材料だけを `、` でつなぐ。入っていないものは書かない（0 と書かない）。材料が 1 つも無いときは `まだ数えたものが無い`。
  1. `ピーク {peaks} 件`
  2. `現役のサミット {summits} 件（廃止済みとして除いた {retired} 件）`
  3. `登録変更リスト {file_name}、申請の行 {row_count} 件`
  4. `仮サミットコードの数（エリアごと）: {areas}`
  5. `peak.match_status は matched {pm}・ambiguous {pa}・dominant {pd}・new {pn}、summit.match_status は matched {sm}・ambiguous {sa}・delete {sd}・unmatched {su}`
  6. `取り込んだ申請 {taken} 件、pending_match が same の候補 {same} 件・different の候補 {different} 件、知らせる行 {notices} 件`
- SM4 の `{state}` は、出力の状態の文。`merged_summit.geojson と merged_summit.xlsx はそろえて置いていない`（`written` が偽）か、`merged_summit.geojson と merged_summit.xlsx は書いた`（`written` が真）。

#### 7.5.5 UT 候補

すべて自動（合否をテストのコードが判定できる）。`main` を通る場面（引数の誤り、起動の場面、入力の誤り、書き込みの失敗）は子のプロセスで起動し、ほかの関数は同じプロセスで直接呼ぶ。止まるケースの期待の「メッセージ」は、標準エラー出力の 2 行（[7.5.4](#754-メッセージ文面)・[7.1.4](#714-メッセージ文面)・[2.2](#22-ログとメッセージの文面)の文面に値を入れたもの）。`{path}` は渡した絶対パス。共通の準備は次の 13 個。

- **同じプロセス**: [7.2.5](#725-ut-候補)の同じ名前の準備と同じ（`merge_peaks` を `match_summits` に読み替える）。`match_summits._config_opt` は空の文字列にしておく（このとき `{rerun4}` は `scripts/run_pipeline.sh --phase 4 を起動し直す`、`{redo}` は `scripts/run_pipeline.sh を --phase なしで起動して、フェーズ2 から通しでやり直す`）。ファイルはケースごとに一時のディレクトリ `<tmp>` に書く。
- **SOTA サミットリスト CSV**: 1 行目 `SOTA Summits List (Date=18/10/2026)`、2 行目（見出しの 17 列）`SummitCode,AssociationName,RegionName,SummitName,AltM,AltFt,GridRef1,GridRef2,Longitude,Latitude,Points,BonusPoints,ValidFrom,ValidTo,ActivationCount,ActivationDate,ActivationCall`。データの行は `row(code, name, alt, lon, lat, valid_to)` で書く: `{code},A,R,{name},{alt},0,0,0,{lon},{lat},1,0,01/01/2020,{valid_to},0,,`（17 欄。使う列は 0・3・4・8・9・13 欄目）。改行は LF。記録の番号は、1 行目が 1、見出しが 2、最初のデータの行が 3。
- **登録変更リストの XHTML**: UTF-8 の次の組み立てを使う（実物の形を縮めたもの）。`xhtml(*rows)` は `<?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml"><body><table><tbody>` + 行 + `</tbody></table></body></html>`。行は次の関数で作る（`<tr>` の文字列）。
  - `title(y)`: `<td></td><td>{y}年</td><td>山岳データ登録変更リスト</td>`。`upd(d)`: `<td></td><td>{d}</td><td>Update</td>`。`marker()`: `<td></td><td></td><td>↑↑↑↑↑ ここまでは2025年7月1日版に反映済 ↑↑↑↑↑</td>`。
  - `head()`: 2 行。1 行目は `<td rowspan="2">アクション</td><td rowspan="2">既存山岳ID もしくは 県名</td><td colspan="3">変更前</td><td colspan="3">変更後</td><td rowspan="2">備考</td><td rowspan="2">申請者・申請日</td><td colspan="6">新規追加詳細</td>`、2 行目は `山岳名(日本語)`・`山岳名(英文読み)`・`標高m` を 2 組と、`位置`・`所在地`・`コル位置`・`比較SOTA-ID`・`コル標高`・`プロミネンス` を、それぞれ `<td>` に入れた 12 個。格子にすると、アクション・山岳 ID か県名・変更後の標高・備考・申請者・申請日・位置が 0・1・7・8・9・10 列目になる。
  - `app(action, target, elev, who, pos, note='')`: 16 個の `<td>` を、0 列目 `action`、1 列目 `target`、7 列目 `elev`、8 列目 `note`、9 列目 `who`、10 列目 `pos` にし、ほかを空にしたもの。
- **ピークとゾーン**: `cmp5_common.MergedPeakRow(<path>, <n>, {'peak_lat': …, 'peak_lon': …})` を直接作る（鍵は使う 2 つだけでよい）。ゾーンは `cmp5_common.ZoneFeature(index, kind, pixel, area_complete, geometry, properties)` を直接作る。`properties` は `{'peak_lat': JsonNumber(…), 'peak_lon': JsonNumber(…)}` を持つ `dict`、`geometry` は `{'type': 'Polygon', 'coordinates': [[[x, 0], [x + 1, 0], [x + 1, 1], [x, 1], [x, 0]]]}`（x を左端とする一辺 1 の四角。数は `JsonNumber`）。ピークは P1（画素 (1, 1)、`35.10000000`・`138.10000000`）と P2（画素 (2, 2)、`35.20000000`・`138.20000000`）、画素 (9, 9) の `36.00000000`・`139.00000000` は表に無いピーク。
- **地域と市区町村の GeoJSON**: `{"type":"FeatureCollection","features":[…]}`。地域の Feature は `{"type":"Feature","properties":{"assoc":"JA","area_code":"HS","region_name":"広島県"},"geometry":{"type":"Polygon","coordinates":[[[0,0],[1,0],[1,1],[0,0]]]}}`、市区町村の Feature は `properties` が `{"municipality":"廿日市市","code":"34210"}` で `geometry` が `MultiPolygon`（`"coordinates":[[[[0,0],[1,0],[1,1],[0,0]]]]`）。
- **突き合わせ以降の入力**（`UT-match_summits-21` から）: 索引は `match_summits.SpatialIndex(shapely.STRtree(<shapely の形の並び>), <keys>)` をケースの中で直接作る（1 回目の関数〈`build_spatial_indexes` など〉を呼ばない）。形の座標は（経度, 緯度）の順で、四角は `shapely.box(<西の経度>, <南の緯度>, <東の経度>, <北の緯度>)`。ピークの鍵は Z15 の画素の形の `K1 = (1, 1)`・`K2 = (2, 2)`・`K3 = (3, 3)`（実際の画素と合っていなくてよい。鍵は同一性にだけ使う）。ピークの行は `cmp5_common.MergedPeakRow(<path>, <n>, {...})` に使う列だけを入れる: `peak_lat`・`peak_lon`・`peak_elev`・`prominence`・`key_col_resolved`（`'true'`・`'false'`）・`col_lat`・`col_lon`（陸のコルが無いものは `0.00000000`）。サミットは `match_summits.Summit(<code>, 'n', '100', <lat>, <lon>, <line_no>)`。四角は `AZ_1 = box(138.0, 35.0, 138.2, 35.2)`、`AZ_2 = box(138.1, 35.1, 138.3, 35.3)`（`AZ_1` と重なる部分は経度 138.1〜138.2、緯度 35.1〜35.2）、`AZ_3 = box(139.0, 36.0, 139.2, 36.2)`、`DZ = box(138.0, 35.0, 138.5, 35.5)`。サミットの点は四角の境目から画素 1 つの大きさ（約 4.3×10⁻⁵ 度）より十分に離す。止まるケースの期待は、標準エラー出力の 2 行（2 行目は [7.5.4](#754-メッセージ文面)の案内の文）と `SystemExit` の `code`。
- **SOTA 既存サミット GeoJSON**（`UT-match_summits-38` から）: 版 `V = 3`。ケースごとの一時のディレクトリ `<tmp>` の下に `geojson_v3/` を作り、`ja<N>_v3.geojson`（`N` は 0〜9）を UTF-8 で書く。中身は `json.dumps({"type": "FeatureCollection", "features": […]}, ensure_ascii=False)`。Feature は、テストの中の関数 `nf(name)` で `{"type": "Feature", "properties": {"name": name}}` を作る。読むのは `read_sota_names('<tmp>', 3)`。`<tmp>` は絶対パスで、警告の組の `{path}` は `<tmp>/geojson_v3/ja<N>_v3.geojson`。
- **属性の入力**（`UT-match_summits-41` から）: ピークの行は、テストの中の関数 `row(n, peak_lat, peak_lon, peak_elev, prominence, key_col_resolved, col_lat, col_lon, col_elev)` で `cmp5_common.MergedPeakRow('p', n, {…その 8 つの鍵…})` を作る。鍵は Z15 の画素の形の `K1 = (1, 1)`〜`K6 = (6, 6)`（同一性にだけ使う）。`peaks` はこの順の辞書: `K1 = row(2, '35.10', '138.10', '1000.60', '50', 'true', '35.00', '138.00', '950.40')`、`K2 = row(3, '35.20', '138.20', '1200.00', '60', 'true', '0.00000000', '0.00000000', '0.00')`、`K3 = row(4, '35.30', '138.30', '149.99', '5', 'false', '0.0', '0.0', '')`、`K4 = row(5, '35.40', '138.40', '1300.50', '9', 'true', '35.1', '138.1', '1100.00')`、`K5 = row(6, '35.50', '138.50', '1000.0', '9', 'true', '35.2', '138.2', '900')`、`K6 = row(7, '35.60', '138.60', '800.9', '9', 'true', '35.3', '138.3', '700')`。サミットは `match_summits.Summit(<code>, 'n', <alt>, <lat>, <lon>, <行>)` で、この順: `JA/AB-010`（`140`・`35.31`・`138.31`・3）、`JA/AB-002`（`900`・`35.41`・`138.41`・4）、`JA/AB-020`（`1000`・`35.51`・`138.51`・5）、`JA/AB-003`（`1001`・`35.52`・`138.52`・6）、`JA/AB-030`（`700`・`35.61`・`138.61`・7）、`JA/CD-001`（`600`・`36.0`・`139.0`・8）、`JA/CD-002`（`149`・`36.1`・`139.1`・9）、`JA/CD-003`（`500`・`36.2`・`139.2`・10）、`JA/CD-004`（`300`・`36.3`・`139.3`・11）。判定の結果は直接作る: `ActivationMatch({'JA/AB-010': K3, 'JA/AB-002': K4, 'JA/AB-020': K5, 'JA/AB-003': K5, 'JA/AB-030': K6}, {K3: [JA/AB-010], K4: [JA/AB-002], K5: [JA/AB-020, JA/AB-003], K6: [JA/AB-030]}, {K3: 'matched', K4: 'matched', K5: 'ambiguous', K6: 'matched'}, [])`、`DeleteMatch({'JA/CD-001': 'delete', 'JA/CD-002': 'delete', 'JA/CD-003': 'delete', 'JA/CD-004': 'unmatched'}, {'JA/CD-001': DominantPeak(K2, 1234.56), 'JA/CD-002': DominantPeak(K4, 0.04), 'JA/CD-003': DominantPeak(K5, 10.25)}, {K1: 'new', K2: 'dominant'}, [JA/CD-004])`、`codes = {K1: 'JA/HS-A01', K2: 'JA/HS-A00'}`。`RH = RegionFeature('JA', 'HS', '広島県', {})`、`regions = RegionMatch(<鍵 ('peak', K1)〜('peak', K5) が Location(RH, '廿日市市')、('peak', K6) が Location(None, '')>, [])`、`names = {'JA/AB-002': '山B', 'JA/AB-010': '山J', 'JA/AB-003': '山三'}`。
- **申請の入力**（`UT-match_summits-46` から）: 申請はテストの中の関数 `ap(action, summit_id=None, lat=None, lon=None, new_elev=None, applicant='X', applied_on='2026-10-01', years=(2026,), row=1)` で `Application(action, summit_id, lat, lon, new_elev, applicant, applied_on, years, (years[0], row), <アクションの語>, <summit_id か空文字>)` を作る（アクションの語は `追加`・`変更`・`削除`）。`UpdateList('f.xhtml', <申請>, [YearUpdate(2026, '2026-10-14'), YearUpdate(2025, '')], <読み込みの知らせ>, 0)` を直接作る（`<読み込みの知らせ>` は、書いていないケースでは空の `list`）。`SummitsList(datetime.date(2026, 10, 18), <サミット>, 4, frozenset({'JA/ZZ-777', 'JA/KC-050', 'JA/MM-900', 'JA5/MM-100'}), {'AB': frozenset({'JA'}), 'CD': frozenset({'JA'}), 'KC': frozenset({'JA'}), 'ZZ': frozenset({'JA'}), 'MM': frozenset({'JA', 'JA5'})})`（`region_assocs` は `read_summits_list` の 6 と同じく廃止済みの行も数えて作った値にする。`MM` の `JA5` は廃止済みの `JA5/MM-100` から来る。`KC` に廃止済みのほかのアソシエーションの行を足すと、`KC` が 2 つのアソシエーションになり、UT-46 の `JA5/KC-027` の期待が変わる）。サミットは `属性の入力` の 9 件の後ろに `JA/KC-027`（`700`・`36.5`・`139.5`・12）と `JA/MM-200`（`700`・`36.6`・`139.6`・13）をこの順に足したもの。ピークは `K1`・`K2`（`add`）、`K4`（`band_change`）、`K5`（`ambiguous`）、`K6`（`no_change`）の 5 つで、`peak_lat`・`peak_lon`・`peak_elev` は `K1` が `35.10000000`・`138.10000000`・`1000.60`、`K2` が `35.20000000`・`138.20000000`・`1200.00`、`K4`・`K5`・`K6` は `属性の入力` と同じ。`ActivationMatch` は `{'JA/AB-002': K4, 'JA/AB-020': K5, 'JA/AB-003': K5, 'JA/AB-030': K6}`・`{K4: [JA/AB-002], K5: [JA/AB-020, JA/AB-003], K6: [JA/AB-030]}`・`{K4: 'matched', K5: 'ambiguous', K6: 'matched'}`、`DeleteMatch` は `属性の入力` の `summit_status` に `'JA/KC-027': 'unmatched'`・`'JA/MM-200': 'unmatched'` をこの順に足し、`unmatched` にも `JA/KC-027`・`JA/MM-200` の `Summit` を `JA/CD-004` の後ろにこの順に足したもの（`unmatched` は `[JA/CD-004, JA/KC-027, JA/MM-200]`）。`Attributes` は直接作る（使う項目だけ値を入れる。`PeakAttrs(points, None, category, '', '', '', '')`・`SummitAttrs(match_status, None, category, '', '', '', '', None, '')` の形）: ピーク `K1`・`K2` が `category='add'`、`K4` が `'band_change'` で `points=8`、`K5` が `'review'`、`K6` が `'no_change'` で `points=4`。サミット `JA/AB-002` が `matched`・`band_change`、`JA/AB-030` が `matched`・`no_change`、`JA/AB-020` が `ambiguous`・`review`、`JA/CD-001` が `delete`・`delete`、`JA/CD-004`・`JA/KC-027`・`JA/MM-200` が `unmatched`・`review`。追加の申請のための索引は、`match_summits.SpatialIndex(shapely.STRtree([AZ_1, AZ_2, AZ_3]), [K1, K2, K4])`（四角は共通の準備の `AZ_1`〜`AZ_3`）を直接作る。
- **組み立ての入力（metadata）**（`UT-match_summits-55` から）: ケースごとの一時のディレクトリ `<tmp>` の下に、空のファイルを `os.utime` で mtime を決めて置く。タイルは `<tmp>/tiles/15/1/a.png`（mtime `1700000000`）、`<tmp>/tiles/15/2/b.png`（`1760000000.7`）、`<tmp>/tiles/15/2/c.PNG`（`1790000000`）、`<tmp>/tiles/15/2/d.txt`（`1795000000`）。最大の `.png` は `b.png` で、値は `2025-10-09T08:53:20Z`（`a.png` だけなら `2023-11-14T22:13:20Z`）。版は、`<tmp>/repo` で `git init` し、追跡するファイル `f` を作って commit し、`git tag -a v0.1.0 -m v0.1.0` する（`git` の呼び出しは `-c user.name=u -c user.email=u@example.com` を付けて `subprocess.run(['git', ...], cwd=..., check=True)`）。UT の `git` の子のプロセスと `build_metadata` の呼び出しは、`unittest.mock.patch.dict(os.environ, {'GIT_CONFIG_GLOBAL': os.devnull, 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CEILING_DIRECTORIES': <一時ディレクトリの親>, 'LC_ALL': 'C'})` の下で動かす（`git` のメッセージを英語に固定する。利用者の設定〈`commit.gpgsign` など〉と、一時ディレクトリの上のリポジトリに頼らない）。`ref_date` は `datetime.date(2026, 10, 18)`、`updatelist` は `UpdateList('sota_updatelist_2026.xhtml', [], [YearUpdate(2026, '2026-10-14'), YearUpdate(2025, '')], [], 0)`、`notices` は `[Notice('unreadable_row', '追加の位置が 緯度,経度 の形で読めない', 2026, 3, '追加', '東京都', 'A', '2026-01-01', 'abc'), Notice('unreadable_update', 'Update の日付が読めない', 2025, None, '', '', '', '', '')]`、`now` は `datetime.datetime(2026, 11, 3, 9, 5, 7, 987654, tzinfo=datetime.timezone(datetime.timedelta(hours=9)))`。
- **組み立ての入力（フィーチャと XLSX）**（`UT-match_summits-59` から）: 1 つの場面をテストの中で直接作る（前の回の関数を呼ばない）。ピークの行は、テストの中の関数 `prow(n, peak_lat, peak_lon, peak_elev, prominence, key_col_resolved, col_lat, col_lon, col_elev, col_margin_px, stability, analysis_count, expected_count)` で `cmp5_common.MergedPeakRow('p', n, {…その 12 の鍵…})` を作る。鍵は Z15 の画素の形の `K1 = (1, 1)`〜`K5 = (5, 5)`（同一性にだけ使う）。`peaks` はこの順の辞書: `K1 = prow(2, '35.10000000', '138.10000000', '1000.60', '50.00', 'true', '35.00000000', '138.00000000', '950.40', '120', 'confirmed', '4', '')`（`new`。陸のコル、`expected_count` は空）、`K2 = prow(3, '35.20000000', '138.20000000', '900.00', '60.00', 'true', '0.00000000', '0.00000000', '0.00', '0', '-', '1', '1')`（`dominant`。海面のコル）、`K3 = prow(4, '35.30000000', '138.30000000', '1200.50', '70.00', 'true', '35.20000000', '138.20000000', '1100.00', '30', 'unstable', '2', '2')`（`matched`、`band_change`）、`K4 = prow(5, '35.40000000', '138.40000000', '700.00', '', 'false', '0.00000000', '0.00000000', '', '', 'unstable', '3', '3')`（`matched`、`no_change`。コルが未確定）、`K5 = prow(6, '35.50000000', '138.50000000', '1300.00', '80.00', 'true', '35.30000000', '138.30000000', '1250.00', '40', 'confirmed', '5', '5')`（`ambiguous`）。
  - ゾーン: `zones` は `K1`〜`K5` の順（添字 `i` を 0〜4 とする）に `PeakZones(cmp5_common.ZoneFeature(2 * i + 1, 'activation_zone', K, True, <AZ の形>, <properties>), cmp5_common.ZoneFeature(2 * i + 2, 'delete_zone', K, <area_complete>, <delete判定ゾーンの形>, <properties>))`。形は `poly(x)` ＝ `{'type': 'Polygon', 'coordinates': [[[x, 0], [x + 1, 0], [x + 1, 1], [x, 1], [x, 0]]]}`（数は `JsonNumber`。AZ は `poly(10 * i)`、delete判定ゾーンは `poly(10 * i + 5)`）。`properties` は `{'peak_lat': JsonNumber(<そのピークの peak_lat>), 'peak_lon': JsonNumber(<peak_lon>)}`。delete判定ゾーンの `area_complete` は `K4` だけ `False`、ほかは `True`（AZ は全部 `True`）。
  - サミット（この順。`Summit(code, name, alt_m, lat, lon, line_no)`）: `JA/HS-011`（`Mt D1`・`100`・`35.2100`・`138.2100`・3）、`JA/HS-010`（`Mt D2`・`0200`・`+35.2200`・`138.2200`・4）、`JA/HS-003`（`Mt A3`・`1000`・`35.3100`・`138.3100`・5）、`JA/HS-013`（`Mt D3`・`300`・`35.3200`・`138.3200`・6）、`JA/HS-004`（`Mt A4`・`650`・`35.4100`・`138.4100`・7）、`JA/HS-005`（`Mt A5`・`800`・`35.5100`・`138.5100`・8）、`JA/HS-006`（`Mt A6`・`900`・`35.5200`・`138.5200`・9）、`JA/HS-020`（`Mt H1`・`400`・`35.6000`・`138.6000`・10）、`JA/HS-032`（`Mt U1`・`120`・`35.7000`・`138.7000`・11）、`JA/HS-031`（`Mt U2`・`500`・`35.7100`・`138.7100`・12）。
  - 突き合わせの結果: `ActivationMatch({'JA/HS-003': K3, 'JA/HS-004': K4, 'JA/HS-005': K5, 'JA/HS-006': K5}, {K3: [JA/HS-003], K4: [JA/HS-004], K5: [JA/HS-005, JA/HS-006]}, {K3: 'matched', K4: 'matched', K5: 'ambiguous'}, [])`。`DeleteMatch` の `summit_status` は `JA/HS-011`・`JA/HS-010`・`JA/HS-013`・`JA/HS-020` が `'delete'`、`JA/HS-032`・`JA/HS-031` が `'unmatched'`（この順）、`dominant` は `JA/HS-011`→`DominantPeak(K2, 1234.6)`、`JA/HS-010`→`DominantPeak(K2, 20.0)`、`JA/HS-013`→`DominantPeak(K3, 0.0)`、`JA/HS-020`→`DominantPeak(K5, 55.5)`、`peak_status` は `{K1: 'new', K2: 'dominant'}`、`unmatched` は `[JA/HS-032, JA/HS-031]`（受け取った順）。`codes` は `{K1: 'JA/HS-A00', K2: 'JA/HS-A01'}`。
  - 所在地: `R = RegionFeature('JA', 'HS', '広島県', {})`。`RegionMatch` の `locations` は、`('peak', K1)`〜`('peak', K5)` と `('summit', <10 件の code>)` が `Location(R, '廿日市市')`（ただし `('summit', 'JA/HS-031')` は `Location(None, '')`、`('summit', 'JA/HS-003')`〈`K3` の AZ の中の `matched` のサミット〉と `('summit', 'JA/HS-005')`〈`ambiguous` のサミット〉は `Location(R, '大竹市')`。ピークの行の所在地を結んだサミットから取る誤りと、`ambiguous` の行の所在地を親のピークから取る誤りを、UT-60・63 が見つけられるようにするため）、`('col', K1)`・`('col', K3)`・`('col', K5)` が `Location(R, '大竹市')`、`outside` は `[]`。
  - 属性: `Attributes` は直接作る。`PeakAttrs(points, is_band_change_candidate, category, review_reason, review_group_id, summit_name_jp, rationale)` は、`K1 = PeakAttrs(6, None, 'add', '', '', '', 'R-add')`、`K2 = PeakAttrs(6, None, 'add', '', '', '', 'R-add2')`、`K3 = PeakAttrs(8, True, 'band_change', '', '', 'A3山', 'R-change')`、`K4 = PeakAttrs(4, False, 'no_change', '', '', 'A4山', '')`、`K5 = PeakAttrs(10, None, 'review', 'multiple_summits_in_az', GID, '', '')`（`GID = 'az:JA/HS-005|JA/HS-006'`）。`SummitAttrs(match_status, sota_points, category, review_reason, review_group_id, summit_name_jp, dominant_peak_code, dominant_peak_dist_m, rationale)` は、`JA/HS-011 = SummitAttrs('delete', 1, 'delete', '', '', 'D1山', 'JA/HS-A01', 1234.6, 'R-del1')`、`JA/HS-010 = SummitAttrs('delete', 2, 'delete', '', '', '', 'JA/HS-A01', 20.0, 'R-del2')`、`JA/HS-003 = SummitAttrs('matched', 6, 'band_change', '', '', 'A3山', '', None, '')`、`JA/HS-013 = SummitAttrs('delete', 4, 'delete', '', '', '', 'JA/HS-003', 0.0, 'R-del3')`、`JA/HS-004 = SummitAttrs('matched', 4, 'no_change', '', '', 'A4山', '', None, '')`、`JA/HS-005`・`JA/HS-006 = SummitAttrs('ambiguous', 6, 'review', 'multiple_summits_in_az', GID, '', '', None, '')`、`JA/HS-020 = SummitAttrs('delete', 1, 'review', 'ambiguous_parent', GID, '', '', 55.5, '')`、`JA/HS-032 = SummitAttrs('unmatched', 1, 'review', 'unmatched', '', '', '', None, '')`、`JA/HS-031 = SummitAttrs('unmatched', 2, 'review', 'unmatched', '', '', '', None, '')`。`groups` は `[ReviewGroup(GID, K5, ('JA/HS-005', 'JA/HS-006'), ('JA/HS-020',))]`、`null_points` は `NullPoints((), (), ())`。
  - 申請済み: `Pending` の `rows`（この順）は、`('peak', K1)` が `PendingRow((<add の申請>,), 'same', '追加 2026-10-04（2026年の表）')`、`('peak', K3)` が `PendingRow((<change の申請>,), 'same', '変更 2026-10-01（2026年の表）')`、`('summit', 'JA/HS-013')` が `PendingRow((<delete の申請>,), 'same', '削除 2026-10-03（2025年の表）')`、`('summit', 'JA/HS-031')` が `PendingRow((<held の申請>,), '', '削除 2026-10-02（2026・2025年の表）')`、`notices` は `[]`、`taken` は `4`（4 つの申請）。申請は DEC189 のキーの順の `dict`（`action`・`summit_code`・`lat`・`lon`・`new_alt_m`・`new_points`・`applicant`・`applied_on`・`years`・`match`）で、`<add の申請>` は `('add', '', JsonNumber('35.1'), JsonNumber('138.1'), None, None, 'W', '2026-10-04', [2026], 'same')`、`<change の申請>` は `('change', 'JA/HS-003', None, None, JsonNumber('1200'), 8, 'X', '2026-10-01', [2026], 'same')`、`<delete の申請>` は `('delete', 'JA/HS-013', None, None, None, None, 'Z', '2026-10-03', [2025], 'same')`、`<held の申請>` は `('delete', 'JA/HS-031', None, None, None, None, 'Y', '2026-10-02', [2026, 2025], 'held')`。
  - 呼び方: `metadata` は `{'summitslist_date': '2026-10-18', 'n': 1}`（`build_summit_features` の引数。`Metadata.items` でなくてよい）。`SummitFeatures` の `features` を、`feature_type`・`summit_code`・終点のサミットの `code`（`coord_diff` の終点の座標を、サミットの点の座標と比べて引く。ほかは空文字）の 3 つ組にしたものを「並び」と呼ぶ。`build_summit_sheets` には `features` をそのまま渡す。

- **子のプロセス**: [7.3.5](#735-ut-候補)の同じ名前の準備と同じ形で、`<tmp>/src/scripts/` に `match_summits.py`・`common.py`・`cmp5_common.py` を写す。`<tmp>/c.ini` は `[paths]` の `data_dir = <tmp>/data` と `log_dir = <tmp>/logs`（ケースによって `[match]` の値を足す）。作業ディレクトリは `<tmp>/work/`。起動は `subprocess.run([sys.executable, '<tmp>/src/scripts/match_summits.py', *<引数>], cwd='<tmp>/work', capture_output=True, env=<環境>)`。`_parse_args` のケースは `<引数>` を書く。ほかのケースは `<引数>` が `['--config', '<tmp>/c.ini']`。`<環境>` は `os.environ` に `GIT_CEILING_DIRECTORIES=<tmp>` と `LC_ALL=C` を足したもの（`<tmp>/src` が git のリポジトリの外になり、`software_version` が `unknown` で MT1 が出ることを決まった結果にする。一時のディレクトリが git のリポジトリの中に作られる環境〈`TMPDIR` を checkout の下にしたときなど〉でも結果を変えないため。`<tmp>` がリポジトリの外なら無くても同じだが、外さない）。`c.ini` は既定のパスでないので、メッセージの `{config_opt}` は空白 1 つに続けて `--config <tmp>/c.ini`（パスは `shlex.quote` した形）。1 つの UT に (a)(b)… の回が複数あるときは、回ごとに `<tmp>/data/` と `<tmp>/logs/` を作り直す。
- **起動の場面**: 子のプロセスのケースが使う入力を、次のとおり `<tmp>/data/` の下に書く（ケースが「置かない」「替える」と書いたものを除く）。数や座標は書いたとおりの字句にする（浮動小数の計算で作らない）。
  - `results/merged_peak.csv`: 見出し（`cmp5_common.MERGED_PEAK_ALL_COLUMNS` を `,` でつないだもの）と、`K2`・`K1` の 2 行（この順。Z15 の画素の順）。`K2` は `35.36058364,138.77030611,800.00,0.00000000,0.00000000,0.00,800.00,true,-1,3-5338,1,9,unstable`（海面で確定したコル。`new` になる）、`K1` は `35.36058364,138.81322145,1500.00,35.34308245,138.74884844,1000.00,500.00,true,20,3-5338,1,9,unstable`（陸のコルで確定。`matched` になる）。行末は LF。
  - `results/merged_peak.geojson`: 1 行目 `{"type":"FeatureCollection","features":[`、続けて次の 4 つの Feature を 1 行に 1 つ（最後のほかは行末に `,`）、最後の行 `]}`。どの行も LF。Feature は `{"type":"Feature","properties":{"peak_lat":35.36058364,"peak_lon":<経度>,"feature_type":"<種類>","area_complete":true},"geometry":{"type":"Polygon","coordinates":[[[<西>,<南>],[<東>,<南>],[<東>,<北>],[<西>,<北>],[<西>,<南>]]]}}` の形で、`<経度>`・`<種類>`・`<西>`・`<南>`・`<東>`・`<北>` は次の表のとおり（数は字句のまま）。

    | 順 | `<経度>` | `<種類>` | `<西>` | `<南>` | `<東>` | `<北>` |
    |---|---|---|---|---|---|---|
    | 1 | `138.77030611` | `activation_zone` | `138.7683` | `35.3586` | `138.7723` | `35.3626` |
    | 2 | `138.77030611` | `delete_zone` | `138.7603` | `35.3506` | `138.7803` | `35.3706` |
    | 3 | `138.81322145` | `activation_zone` | `138.8112` | `35.3586` | `138.8152` | `35.3626` |
    | 4 | `138.81322145` | `delete_zone` | `138.8032` | `35.3506` | `138.8232` | `35.3706` |

  - `ref/summitslist.csv`: 1 行目 `SOTA Summits List (Date=18/10/2026)`、2 行目は共通の準備「SOTA サミットリスト CSV」の見出し、続けて `row('JA/HS-001', 'S1', '1500', '138.8142', '35.3610', '31/12/2099')` と `row('JA/HS-002', 'S2', '600', '138.95', '35.45', '31/12/2099')`（S1 は `K1` の AZ の中で、`K1` の delete判定ゾーンの中。S2 はどのゾーンにも入らず、`unmatched` になる）。
  - `ref/sota_updatelist_2026.xhtml`: `xhtml(title(2026), upd('2026-10-14'), head(), app('追加', '県', '', 'A 2026/1/1', 'abc'), app('変更', 'JA/HS-001', '1400', 'B 2026/10/1', ''))`（読めない行 1 つ〈UN1 が 1 組〉と、S1 へのバンドをまたぐ変更の申請 1 つ）。
  - `boundaries/regions.geojson`・`boundaries/municipalities.geojson`: 共通の準備「地域と市区町村の GeoJSON」の形で Feature を 1 つずつ。地域は `JA`・`HS`・`広島県` の `Polygon`、市区町村は `廿日市市`・`34210` の `MultiPolygon`（座標は同じで、リング `[[138.74,35.335],[138.83,35.335],[138.83,35.37],[138.80,35.37],[138.80,35.355],[138.74,35.355],[138.74,35.335]]`）。このリングは `K1`・`K1` のコル・S1 を含み、`K2` と S2 を含まない。
  - `tiles/` は作らない（MT2）。`sota_geojson_version` は書かない（SN1）。`unmatched_summit_threshold` は書かない（既定の 10）。

| ID | 確かめること | 準備 | 入力 | 期待 |
|---|---|---|---|---|
| `UT-match_summits-01` | ゾーンをピークに突き合わせる | 同じプロセス。ピークの表は P1・P2（この順）。ゾーンは、P1 の AZ（`index` 1）・P1 の delete判定ゾーン（2）・P2 の AZ（3）・P2 の delete判定ゾーン（4） | `match_zones_to_peaks(<ピークの表>, <ゾーン>, <path>)` | 辞書で、鍵が (1, 1)・(2, 2) の順、値が `PeakZones(<index 1>, <index 2>)`・`PeakZones(<index 3>, <index 4>)`。ゾーンの並びを 4・3・2・1 にしても同じ（鍵の順は `peaks` の順） |
| `UT-match_summits-02` | 食い違いをすべて挙げて 1 回で止まる | 同じプロセス。(a) P1・P2 のピークの表で、ゾーンは P1 の両方と、画素 (9, 9) の AZ、P2 の AZ だけ。(b) ゾーンは P1 の両方と P2 の両方に加えて、(9, 9) の AZ と delete判定ゾーン（この順）。(c) ゾーンは P1 の両方だけ | (a)(b)(c) を `match_zones_to_peaks` に | どれも終了コード 1 で MZ1。1 行目は `merged_peak.geojson のゾーンが merged_peak.csv と食い違う: <path>:` の後に空白 1 つを挟んで、(a) `36.00000000,139.00000000 の activation_zone（ピークが merged_peak.csv に無い）、35.20000000,138.20000000 の delete_zone（ゾーンが merged_peak.geojson に無い）`、(b) `36.00000000,139.00000000 の activation_zone（ピークが merged_peak.csv に無い）、36.00000000,139.00000000 の delete_zone（ピークが merged_peak.csv に無い）`、(c) `35.20000000,138.20000000 の activation_zone・delete_zone（ゾーンが merged_peak.geojson に無い）`。2 行目は `{redo}` |
| `UT-match_summits-03` | 空の入力 | 同じプロセス | (a) 空のピークの表と空のゾーンの並び、(b) P1 だけのピークの表と空のゾーンの並び、(c) 空のピークの表と P1 の両方のゾーン | (a) 空の辞書（止まらない）。(b) MZ1 で、`35.10000000,138.10000000 の activation_zone・delete_zone（ゾーンが merged_peak.geojson に無い）`。(c) MZ1 で、`35.10000000,138.10000000 の activation_zone（ピークが merged_peak.csv に無い）、35.10000000,138.10000000 の delete_zone（ピークが merged_peak.csv に無い）` |
| `UT-match_summits-04` | SOTA サミットリスト CSV の読み方 | 同じプロセス。(a) 1・2 行目の後に次のデータの行と空行を書く: 3 行目 `row('JA/HS-001', '山A', '100', '132.5', '34.5', '31/12/2099')`、4 行目 `JA/HS-002`（山B、200、132.6、34.6）の `ValidTo` が `18/10/2026`、5 行目 `JA/HS-003`（山C、300、132.7、34.7）が `17/10/2026`、6 行目 `JA5/KC-001`（山D、400、132.8、34.8）が `31/12/2099`、7 行目 `JA/KC-002`（山E、500、132.9、34.9）が `01/01/2000`、8 行目 `row('W7W/LC-001', 'Peak', 'x', 'xx', 'yy', 'bad')`、9 行目は空行。(b) (a) の先頭に BOM（U+FEFF）を付けたもの | `read_summits_list` に (a)(b) | どちらも `SummitsList` で、`ref_date` が `datetime.date(2026, 10, 18)`、`summits` が `Summit('JA/HS-001', '山A', '100', '34.5', '132.5', 3)`・`Summit('JA/HS-002', '山B', '200', '34.6', '132.6', 4)`・`Summit('JA5/KC-001', '山D', '400', '34.8', '132.8', 6)`（`ValidTo` が基準日と同じ日は現役。`W7W/LC-001` の誤りは見ない）、`retired_count` が 2、`retired_codes` が `frozenset({'JA/HS-003', 'JA/KC-002'})`、`region_assocs` が `{'HS': frozenset({'JA'}), 'KC': frozenset({'JA', 'JA5'})}` |
| `UT-match_summits-05` | 読めないときと書式の誤り | 同じプロセス。(a) 無いパス、(b) ディレクトリ、(c) 中身が `b'\xff\xfe\x00'`、(d) 0 バイトのファイル、(e) 1 行目が `Hello`、(f) 1 行目が `SOTA Summits List (Date=31/02/2026)`、(g) 1 行目だけ、(h) 2 行目の見出しから `ValidTo` を除いたもの、(i) 3 行目が `JA/HS-001,"abc"x`（引用符の後に文字） | それぞれ `read_summits_list` に | どれも終了コード 1。(a) SS1、(b) SS2（`{reason}` は `Is a directory`）、(c) SS2（`UTF-8 として読めない`）、(d) SS3（`基準日の行が無い`）、(e) SS3（`1 行目が SOTA Summits List (Date=DD/MM/YYYY) の形でない: Hello`）、(f) SS3（`基準日が暦に無い: SOTA Summits List (Date=31/02/2026)`）、(g) SS3（`見出しの行が無い`）、(h) SS3（`見出しに列 ValidTo が無い`）、(i) SS3（`3 行目を CSV として読めない:` で始まる）。SS1 以外の 2 行目は `対処: {summits_advice}`、SS2 の 2 行目は `<path> の読み取りの権限と、UTF-8 で保存されていることを確かめるか、提供元から落とし直して <path> に置いてから、{rerun4}` |
| `UT-match_summits-06` | `JA` の行の値の誤り | 同じプロセス。1・2 行目の後に、3 行目として次の 1 行（それ以外は誤りのない行）を置く。(a) `Latitude` が `34.5` の前に空白を 1 つ付けたもの、(b) `Longitude` が `abc`、(c) `AltM` が `1.5`、(d) `ValidTo` が `1/1/2020`、(e) `ValidTo` が `31/02/2026`、(f) `JA/HS-001,A,R,山A,100,0,0,0,132.5,34.5`（10 欄）、(g) 14 欄までで使わない列だけが欠ける行（`JA/HS-001,A,R,山A,100,0,0,0,132.5,34.5,1,0,01/01/2020,31/12/2099`）、(h) 3 行目の `Latitude` が `abc` で、4 行目の `AltM` も `1.5` | `read_summits_list` に | (a)〜(f)(h) は終了コード 1 で SS4。`{detail}` は (a) `3 行目の Latitude が 座標として読めない:` の後に空白を 2 つ挟んで `34.5`（値の前の空白がそのまま残る）、(b) `3 行目の Longitude が 座標として読めない: abc`、(c) `3 行目の AltM が 整数として読めない: 1.5`、(d) `3 行目の ValidTo が DD/MM/YYYY の日付として読めない: 1/1/2020`、(e) 同じ文で `31/02/2026`、(f) `3 行目の欄が足りない: 使う列は 14 欄目まで、この行は 10 欄`、(h) `3 行目の Latitude が 座標として読めない: abc`（最初の行だけ）。(g) は止まらず、`summits` が 1 件 |
| `UT-match_summits-07` | 重複 | 同じプロセス。(a) 3〜7 行目が `JA/HS-001`・`JA/HS-002`・`JA/HS-001`・`JA/HS-002`・`JA/HS-002`（どれも誤りのない行）、(b) 3 行目が `JA/HS-001`（現役）、4 行目が `JA/HS-001` で `ValidTo` が `01/01/2000`、(c) (a) の 8 行目に、`JA/HS-009` で `AltM` が `1.5` の行を足す、(d) `W7W/LC-001` が 2 行 | `read_summits_list` に | (a) SS5 で `{list}` が `JA/HS-001（3、5 行目）、JA/HS-002（4、6、7 行目）`。(b) SS5 で `JA/HS-001（3、4 行目）`（廃止済みの行も数える）。(c) SS4（`8 行目の AltM が 整数として読めない: 1.5`。重複より先に値の誤りで止まる）。(d) 止まらない（`JA` で始まらない行は確かめない） |
| `UT-match_summits-08` | 登録変更リストのファイルを選ぶ | 同じプロセス。`<tmp>/ref/` に `sota_updatelist_2024.xhtml`・`sota_updatelist_2025.xhtml`（どれも中身は空のファイル）、年が全角の数字（U+FF12・U+FF10・U+FF12・U+FF16）の `sota_updatelist_<年>.xhtml`、`sota_updatelist_2026.xhtml.bak`、ディレクトリの `sota_updatelist_2027.xhtml`、`sota_updatelist_202.xhtml`、`Sota_updatelist_2028.xhtml` を置く | (a) `find_updatelist('<tmp>/ref')`、(b) 2025 と 2024 のファイルを消して (a)、(c) `find_updatelist('<tmp>/none')` | (a) `<tmp>/ref/sota_updatelist_2025.xhtml`（年が最大の、名前の全体が合うファイル）。(b)(c) 終了コード 1 で UX1（1 行目は `登録変更リストが無い: <ref の絶対パス>（ファイル名が sota_updatelist_<4 桁の年>.xhtml の形のもの）`、2 行目は `{update_advice}`） |
| `UT-match_summits-09` | 登録変更リストの読み方（標準の形と重ね合わせ） | 同じプロセス。`sota_updatelist_2026.xhtml` に、`title(2026)`・`upd('2026-10-14')`・`head()`・`app('追加', '東京都', '', '7M3XYZ 2026/10/19', '35.1,138.2')`・`app('変更', 'JA/HS-185', '468m', 'JK1VUZ 2026/02/14', '')`・`app('削除', 'JA/YG-263', '', 'JA1ABC 2026/3/5', '')`・`marker()`、続けて `title(2025)`・`upd('2026-02-04')`・`head()`・`app('追加', '東京都', '', '7M3XYZ 2026/10/19', '35.10,138.20')`・`app('変更', 'JA/HS-185', '468', 'JK1VUZ 2026/02/14', '')` | `read_updatelist('<tmp>/sota_updatelist_2026.xhtml')` | `UpdateList` で、`file_name` が `sota_updatelist_2026.xhtml`、`updates` が `[YearUpdate(2026, '2026-10-14'), YearUpdate(2025, '2026-02-04')]`、`applications` が 3 件: `Application('add', None, '35.1', '138.2', None, '7M3XYZ', '2026-10-19', (2026, 2025), (2026, 1), '追加', '東京都')`・`Application('change', 'JA/HS-185', None, None, '468', 'JK1VUZ', '2026-02-14', (2026, 2025), (2026, 2), '変更', 'JA/HS-185')`・`Application('delete', 'JA/YG-263', None, None, None, 'JA1ABC', '2026-03-05', (2026,), (2026, 3), '削除', 'JA/YG-263')`、`notices` が空、`row_count` が 5（目印の行は数えない） |
| `UT-match_summits-10` | 揃え方 | 同じプロセス。`title(2026)`・`upd('2026-10-14')`・`head()` の後に、次の行を順に置く: (1) `app('追加', '県', '', <who>, <pos>)`（`<who>` は `7M3XYZ 2026/10/19`、`<pos>` は `35.1,138.2` を、どちらも ASCII の `!`〜`~` を `chr(ord(c) + 0xFEE0)` で全角にし、空白を U+3000 にしたもの）、(2) `app('追加', '県', '', 'A 2026/1/2', '35.1、138.2')`、(3) `app('追加', '県', '', 'B 2026/1/3', '35.1 138.2')`、(4) `app('変更', 'JA/HS-185', <elev>, 'C 2026/1/4', '')`（`<elev>` は `123m` を (1) と同じ方法で全角にしたもの）、(5) `app('変更', 'JA/HS-186', '123 m', 'D 2026/1/5', '')`、(6) `app('追加', '県', '', 'E 2026/10/190', '35.1,138.2')`、(7) `app('追加', '県', '', 'JG2WGK 2025/01/08JQ3AJX', '35.2,138.3')`、(8) `app('追加', '県', '', '2026/1/6', '35.3,138.4')` | `read_updatelist` に | `applications` が 7 件（(6) を除く。順は (1)(2)(3)(4)(5)(7)(8)）で、(1) は `lat` が `35.1`・`lon` が `138.2`・`applicant` が `7M3XYZ`・`applied_on` が `2026-10-19`、(2)(3) は同じ位置で `applicant` が `A`・`B`、`applied_on` が `2026-01-02`・`2026-01-03`、(4)(5) は `new_elev` が `123`、`applicant` が `C`・`D`、(7) は `applicant` が `JG2WGK JQ3AJX`・`applied_on` が `2025-01-08`、(8) は `applicant` が空文字・`applied_on` が `2026-01-06`。`notices` が `[Notice('unreadable_row', '申請日が読めない', 2026, 6, '追加', '県', 'E 2026/10/190', '', 'E 2026/10/190')]`（日付の後ろに数字が続くものは日付としない）。`row_count` が 8 |
| `UT-match_summits-11` | 読めない行と、知らせない行 | 同じプロセス。`title(2026)`・`upd('2026-10-14')`・`head()` の後に、次の 11 行（通し番号 1〜11）を置く: (1) `app('追加', '県', '', 'A 2026/1/1', 'abc')`、(2) `app('追加', '県', '', 'A 2026/1/2', '35.1,138.2,5')`、(3) `app('変更', 'JA/HS', '100', 'A 2026/1/3', '')`、(4) `app('変更', 'JA/HS-185', '1.2.3', 'A 2026/1/4', '')`、(5) `app('削除', 'JA/YG-263', '', '', '')`、(6) `app('移動', 'JA/YG-263', '', 'A 2026/1/6', '')`、(7) `app('変更', '', '', '', '')`、(8) `app('変更', 'JA/HS-185', '', '2026/13/45', '')`、(9) `app('', '', '', 'memo', '')`、(10) `app('追加', '県', '', 'A 2026/1/10', '35.5,138.5')`、(11) `app('削除', 'JA/YG-263', '', 'A 2026/1/11', '')` | `read_updatelist` に | `notices` が通し番号 1〜6 の 6 件で、(1) `Notice('unreadable_row', '追加の位置が 緯度,経度 の形で読めない', 2026, 1, '追加', '県', 'A', '2026-01-01', 'abc')`、(2) 同じ理由で `value` が `35.1,138.2,5`・`row` が 2・`applied_on` が `2026-01-02`、(3) `山岳 ID が アソシエーション/地域コード-番号 の形で読めない`・`value` が `JA/HS`・`target` が `JA/HS`、(4) `変更後の標高が数として読めない`・`value` が `1.2.3`、(5) `Notice('unreadable_row', '申請日が読めない', 2026, 5, '削除', 'JA/YG-263', '', '', '')`、(6) `アクションの欄の語が 追加・変更・削除 のどれでもない`・`action` が `移動`・`value` が `移動`・`applied_on` が `2026-01-06`。(7)(8)(9) は知らせない（(7)(8) は変更後の標高が空、(9) はアクションの欄が空）。`applications` が (10)(11) の 2 件。`row_count` が 9（(6)(9) は数えない） |
| `UT-match_summits-12` | 題の行・目印の行・格子 | 同じプロセス。(a) 2 つのセルの `title(2026)`。(b) `<tr><td>2026年 山岳データ登録変更リスト</td></tr>`（1 つのセルの題の行）。どちらも `upd('2026-10-14')`・`head()`・`app('追加', '県', '', 'A 2026/1/1', '35.1,138.2')`。(c)〜(e)(g) も、(a) の `title(2026)`・`upd('2026-10-14')`・`head()` の後に置く（(f) は自分の行をすべて書いている）。(c)(d) は (a) の `app` を残して続きを足し、(e)(g) は (a) の `app` を書いた行に替える。(c) (a) の後に `app('変更', 'JA/HS-185', '468', 'A 2026/1/2', '', '2022年分再申請')`。(d) (a) の `app` の後に `marker()` と `app('追加', '県', '', 'B 2026/1/3', '35.2,138.3')`。(e) `app('追加', '県', '', 'C 2026/1/4', '35.3,138.4')` の末尾に、空の `<td>` を 5 つと `<td>追加</td>` を足した行。(f) `title(2026)`・`upd('2026-10-14')`・`head()` の後に、0 列目が `<td rowspan="4">追加</td>` の行 1 つ（ほかは `app('追加', '県', '', 'D 2026/1/5', '35.4,138.5')` の 1 列目以降）を置き、続けて `title(2025)`・`upd('2025-01-31')`・`head()`・`app('追加', '県', '', 'E 2025/1/6', '35.5,138.6')`。(g) `app('追加', '県', '', 'F<br/>2026/1/7', '35.6,138.7')` | `read_updatelist` に (a)〜(g) | (a)(b) `applications` が `[Application('add', None, '35.1', '138.2', None, 'A', '2026-01-01', (2026,), (2026, 1), '追加', '県')]`、`updates` が `[YearUpdate(2026, '2026-10-14')]`、`notices` が空、`row_count` が 1。(c) 2 件目が `Application('change', 'JA/HS-185', None, None, '468', 'A', '2026-01-02', (2026,), (2026, 2), '変更', 'JA/HS-185')`（備考の `2022年分再申請` を題の行と取り違えない）。(d) 2 件目の `first_seen` が `(2026, 3)`、`row_count` が 2（目印の行は知らせず、通し番号は数える）。(e) 申請が 1 件でアクションが `add`（後ろの `追加` を読まない）。(f) 2025 年の表の申請が `Application('add', None, '35.5', '138.6', None, 'E', '2025-01-06', (2025,), (2025, 1), '追加', '県')`（2026 年の表の `rowspan` が 2025 年の表へ延びない）で、`updates` が 2 件。(g) `applicant` が `F`・`applied_on` が `2026-01-07` |
| `UT-match_summits-13` | 年の表の構造の誤りと Update | 同じプロセス。(a) `title(2026)`・`upd('2026-10-14')`・`head()` だけ。(b) 表の無い XHTML（`<html xmlns="http://www.w3.org/1999/xhtml"><body><p>x</p></body></html>`）。(c) `head()` と `app('追加', '県', '', 'A 2026/1/1', '35.1,138.2')` だけ（題の行が無い）。(d) `title(2026)`・`upd('2026-10-14')` だけ（見出しが無い）。(e) (a) の `head()` の `申請者・申請日` を `申請者` にしたもの。(f) `title(2026)`・`head()`・`app('追加', '県', '', 'A 2026/1/1', '35.1,138.2')`（Update の行が無い）。(g) (f) の `title(2026)` の後に `upd('2026-13-45')` を足したもの。(h) (a) の `head()` の 1 行目の `<td rowspan="2">アクション</td>` を `<td rowspan="101">アクション</td>` にしたもの。(i) (a) の `head()` の 2 行目の 1 つ目のセル `山岳名(日本語)` を `<td colspan="8">山岳名(日本語)</td>` にしたもの（2 行目の 1 つ目は 2 列目から 9 列目を覆い、8・9 列目は 1 行目の `rowspan` の文字が既にある） | `read_updatelist` に | (a) 止まらず、`applications` が空、`updates` が `[YearUpdate(2026, '2026-10-14')]`、`notices` が空、`row_count` が 0。(b) UX4（`{detail}` は `表が無い`）。(c) UX4（`年の表の題の行が無い`）。(d) UX4（`2026 年の表に見出しの行（アクション のセルを持つ行）が無い`）。(e) UX4（`2026 年の表の見出しで 申請者・申請日 の列を特定できない`）。(f)(g) 止まらず、`updates` が `[YearUpdate(2026, '')]`、`notices` が `[Notice('unreadable_update', 'Update の日付が読めない', 2026, None, '', '', '', '', '')]`、`applications` が 1 件。(h) UX4（`{detail}` は `rowspan か colspan の値が 100 を超える: 101`）。(i) UX4（`{detail}` は `セルが重なる`）。UX4 の 2 行目は `{update_advice}`（`{dir}` は `<tmp>`） |
| `UT-match_summits-14` | 危うい入力 | 同じプロセス。外側を `<?xml version="1.0" encoding="{enc}"?>{doctype}<html xmlns="http://www.w3.org/1999/xhtml"><body><table><tbody></tbody></table></body></html>` とする。(a) `{enc}` が `UTF-8`、`{doctype}` が `<!DOCTYPE html [<!ENTITY e "X">]>`。(b)(c)(d) (a) の `UTF-8` を `UTF-16` にし、それぞれ `.encode('utf-16')`（BOM あり）、`.encode('utf-16-le')`、`.encode('utf-16-be')` のバイト列。(e) `{doctype}` が `<!DOCTYPE html [<!ELEMENT html ANY>]>`。(f) `{doctype}` が `<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1 plus MathML 2.0//EN" "http://www.w3.org/Math/DTD/mathml2/xhtml-math11-f.dtd">`（外部の DTD の宣言だけ）で、`<tbody>` の中に `title(2026)`・`upd('2026-10-14')`・`head()`。(g) (f) の `<body>` の中に `<p>a&nbsp;b</p>` を足したもの。(h) `<html><body></html>`。(i) 0 バイトのファイル | `read_updatelist` に (a)〜(i) | (a)〜(e) 終了コード 1 で UX3、`{detail}` は `内部サブセットがある`（符号化によらず当たる）。(f) 止まらず（外部の DTD は取りに行かない）、`updates` が 1 件。(g) UX3（`{detail}` は `undefined entity` で始まる）。(h) UX3（`mismatched tag` で始まる）。(i) UX3（`no element found` で始まる）。UX3 の 2 行目は `{update_advice}` |
| `UT-match_summits-15` | 読めない | 同じプロセス。(a) 無いパス、(b) ディレクトリ | `read_updatelist` に | どちらも終了コード 1 で UX2。`{reason}` は (a) `No such file or directory`、(b) `Is a directory`。2 行目は `<path> の読み取りの権限を確かめてから、{rerun4}` |
| `UT-match_summits-16` | 地域と市区町村の GeoJSON の読み方 | 同じプロセス。(a) 地域に 2 つの Feature（`JA`・`HS`・`広島県`、`JA`・`YN`・`山梨県`。ジオメトリは `Polygon`）、市区町村に 2 つの Feature（`廿日市市`・`34210`、`南巨摩郡富士川町`・`19364`。ジオメトリは `MultiPolygon` と `Polygon`）。(b) どちらのファイルも無い。(c) 地域はあり、市区町村が無い。(d) どちらも `features` が空 | `read_boundaries(<地域>, <市区町村>)` に | (a) `regions` が `RegionFeature` の 2 件（ファイルの順）、`municipalities` が `MunicipalityFeature` の 2 件、`geometry` は読んだ `dict` のまま、`warnings` が空。(b) `regions`・`municipalities` が `None`、`warnings` が `[('BN1', '地域の GeoJSON が無い: <地域のパス>。仮サミットコードのエリアがすべて ZZ になり、region_name が空文字になる（全国の実行では仮サミットコードの連番上限で止まりうる）'), ('BN2', '市区町村の GeoJSON が無い: <市区町村のパス>。municipality が空文字になる')]`。(c) `regions` が 2 件、`municipalities` が `None`、`warnings` が BN2 の 1 組だけ。(d) どちらも空の `list`（`None` でない）、`warnings` が空 |
| `UT-match_summits-17` | 地域と市区町村の GeoJSON の誤り | 同じプロセス。(a)〜(j)(l) は、地域のファイルを次のものにして、市区町村のファイルは正しいものを置く（`{target}` は `地域`）。(k) は、地域のファイルを正しいものにして、市区町村のファイルに (a) の中身を入れたものと、(e) の中身を入れたものの 2 つ（`{target}` は `市区町村`。(g)(h) の市区町村版は確かめない）。BD1: (a) 中身が `x`、(b) 中身に `NaN`（`{"type":"FeatureCollection","features":[{"a":NaN}]}`）、(c) ディレクトリ、(d) `b'\xff\xfe\x00'`。BD2: (e) `{"type":"Feature"}`、(f) `{"type":"FeatureCollection"}`、(g) 2 つ目の Feature の `region_name` が無い、(h) `region_name` が数 `5`、(i) `geometry` が `Point`、(j) `geometry` が `Polygon` で `coordinates` が `"x"`、(l) `geometry` が `Polygon` で `coordinates` が `[[[0,0],[1e999,0],[1,1],[0,0]]]` | `read_boundaries` に | どれも終了コード 1。BD1 は 1 行目が `地域の GeoJSON を読めない: <path>:` の後に空白 1 つを挟んで、(a) `Expecting value: line 1 column 1 (char 0)`、(b) `NaN は JSON の数でない`、(c) `Is a directory`、(d) `UTF-8 として読めない`。BD2 は 1 行目が `地域の GeoJSON の書式が違う: <path>:` の後に空白 1 つを挟んで、(e)(f) `FeatureCollection でない`、(g) `2 番目の Feature の properties に region_name が無いか文字列でない`、(h) `1 番目の Feature の properties に region_name が無いか文字列でない`（(h) は 1 つ目の Feature で）、(i) `1 番目の Feature の geometry が Polygon でも MultiPolygon でもない`、(j) `1 番目の Feature の geometry を作れない:` で始まる、(l) `1 番目の Feature の geometry を作れない: 座標が有限の数でない`。2 行目は `{cmp1_rebuild}`。(k) は市区町村のファイルで、(a) が BD1（`Expecting value: line 1 column 1 (char 0)`）、(e) が BD2（`FeatureCollection でない`）になり、`{target}` が `市区町村` |
| `UT-match_summits-18` | 空間索引 | 同じプロセス。`peak_zones` は、鍵 (1, 1)（AZ が x も y も 0〜1 の四角、delete判定ゾーンが 0〜2 の四角）と鍵 (2, 2)（AZ が 10〜11、delete判定ゾーンが 10〜12 の四角）。座標の数は `JsonNumber`。`boundaries` は地域が 2 つの四角（x も y も 0〜1 と 10〜11）で、市区町村が `None` | `build_spatial_indexes(<peak_zones>, <boundaries>)` | `activation.keys` が `[(1, 1), (2, 2)]`、`activation.tree.query(shapely.Point(0.5, 0.5), predicate='intersects')` が添字 `[0]`、`Point(10.5, 10.5)` が `[1]`、`Point(5, 5)` が空。`delete.tree.query(shapely.Point(1.5, 1.5), predicate='intersects')` が `[0]`。`regions.keys` が `[0, 1]`、`municipalities` が `None` |
| `UT-match_summits-19` | 7.1 の誤りの案内の文 | 同じプロセス | `_input_error_advice` に (a) `'MP1'`・`'MP2'`・`'MP3'`・`'ZF1'`〜`'ZF4'` のそれぞれ（`_config_opt` は空）、(b) (a) の `'MP3'` を `_config_opt` が空白 1 つに続けて `--config /a.ini` のとき、(c) `'XX'` | (a) どれも `scripts/run_pipeline.sh を --phase なしで起動して、フェーズ2 から通しでやり直す`。(b) `scripts/run_pipeline.sh --config /a.ini を --phase なしで起動して、フェーズ2 から通しでやり直す`。(c) `ValueError` |
| `UT-match_summits-20` | 格子の上限の境目と前書き、ゾーンの座標の有限性 | 同じプロセス。(a) 表の先頭（最初の題の行より前）に `<tr><td rowspan="101">前書き</td><td>x</td></tr>` を置き、続けて `title(2026)`・`upd('2026-10-14')`・`head()`・`app('追加', '県', '', 'A 2026/1/1', '35.1,138.2')`。(b) 表の先頭に `<tr><td>x</td><td rowspan="2">a</td></tr><tr><td colspan="3">b</td></tr>`（2 行目の `colspan` が 1 行目から延びる `rowspan` の列を覆う）を置き、続けて (a) と同じ 4 行。(c) UT-13 (a) の `head()` の 1 行目の `<td rowspan="2">アクション</td>` を `<td rowspan="100">アクション</td>` にしたもの。(d) `build_spatial_indexes` に、AZ のジオメトリの座標の 1 つが `cmp5_common.JsonNumber('1e999')` のゾーンを持つ `peak_zones`（鍵 (1, 1) の 1 件。ほかの座標は UT-18 と同じ）と、`regions`・`municipalities` が `None` の `Boundaries` | (a)〜(c) は `read_updatelist`、(d) は `build_spatial_indexes` | (a)(b) 止まらず、`applications` が `[Application('add', None, '35.1', '138.2', None, 'A', '2026-01-01', (2026,), (2026, 1), '追加', '県')]`、`updates` が `[YearUpdate(2026, '2026-10-14')]`、`notices` が空、`row_count` が 1（前書きは格子に展開せず、`rowspan` の上限も重なりも見ない）。(c) 止まらず（上限は 100 を超えるときだけ。100 は通る）、`applications` が空、`updates` が `[YearUpdate(2026, '2026-10-14')]`、`row_count` が 0。(d) 終了コード 1 にせず、`ValueError`（`座標が有限の数でない`）が上がる（例外のまま伝える） |
| `UT-match_summits-21` | `z15_pixel_center_latlon` の表 7 | 同じプロセス | `z15_pixel_center_latlon((gx, gy))` に [2.4](#24-言語ごとに別に実装する式のテストベクトル)の表 7 の 9 行の (gx, gy) | 戻り値が（緯度, 経度）で、経度は表 7 の値と `==`、緯度は差の絶対値が `1e-12` 以下（[7.2.5](#725-ut-候補)の `UT-merge_peaks-01` の形）。(0, 0) → (85.05112692872285, -179.99997854232788)、(7456512, 3293952) → (36.004656128107385, 139.99880075454712)、(7340031, 3322709) → (34.99999776698518, 134.99997854232788)、(7340032, 3322709) → (34.99999776698518, 135.00002145767212)、(7153617, 3553537) → (26.50001530614219, 126.99995756149292)、(7153618, 3553537) → (26.50001530614219, 127.00000047683716)、(7374984, 3685299) → (21.333373174657144, 136.49999856948853)、(7374984, 3685300) → (21.333333199888905, 136.49999856948853)、(7666176, 2984192) → (46.004578351228716, 148.99660348892212) |
| `UT-match_summits-22` | 点がゾーンの中にあるか | 同じプロセス。`AZ_1`（共通の準備）。穴のある Polygon `P_hole` は外側が `AZ_1` と同じ四角、穴が `box(138.08, 35.08, 138.12, 35.12)`。`M` は `MultiPolygon` で、1 つ目が `box(138.0, 35.0, 138.1, 35.1)`、2 つ目が `box(139.0, 36.0, 139.1, 36.1)` | `is_in_zone(lat, lon, zone)` に、(a) `35.05`・`138.05`・`AZ_1`、(b) `37.0`・`140.0`・`AZ_1`、(c) `35.1`・`138.1`・`P_hole`、(d) `35.02`・`138.02`・`P_hole`、(e) `36.05`・`139.05`・`M`、(f) `35.05`・`138.05`・`M`、(g) `36.5`・`139.5`・`M` | (a) 真、(b) 偽、(c) 偽（穴の中）、(d) 真、(e) 真（2 つ目の多角形の中）、(f) 真、(g) 偽 |
| `UT-match_summits-23` | 輪郭の線の上の点は画素の中心で見る（DEC86） | 同じプロセス。画素 (7340032, 3322709)（表 7 の 4 行目）の中心の緯度 `34.99999776698518` を `lat_c` とする。ゾーンは `box(135.0, lat_c - 0.0001, 135.00004291534424, lat_c + 0.0001)`（経度が画素の西端 `7340032 / 2²³ × 360 − 180 = 135.0` から東端 `7340033 / 2²³ × 360 − 180 = 135.00004291534424` まで。緯度は画素の中心の緯度の ±0.0001 度で、画素の北端と南端の外まで少し広いが、点の緯度を画素の中心にするので結果に響かない） | (a) `is_in_zone(lat_c, 135.0, <ゾーン>)`、(b) `is_in_zone(lat_c, 135.00004291534424, <ゾーン>)`、(c) `shapely.contains_xy(<ゾーン>, 135.0, lat_c)` | (a) 真（点はゾーンの西の辺の上。経度の画素の境目の点は、`floor` で東の画素、つまり画素 (7340032, 3322709) に入り、その中心はゾーンの中）、(b) 偽（経度が東端ちょうどの点は東隣の画素 (7340033, 3322709) に入り、その中心はゾーンの外）、(c) 偽（元の点を形に当てると輪郭の上で `contains` が偽。(a) が画素の中心で見ていることの確かめ） |
| `UT-match_summits-24` | AZ とサミットの突き合わせ（`matched`・`ambiguous`・AZ の外と順） | 同じプロセス。ピークの表は、`K1`（行 2、`35.10000000`・`138.10000000`・標高 `1000`・`prominence` `300`・`true`）、`K2`（行 3、`36.10000000`・`139.10000000`・標高 `900`・`prominence` `200`・`true`）の順。索引は `[(K1, AZ_1), (K2, AZ_3)]`。サミットはこの順: `JA/HS-002`（`36.05`・`139.05`、行 4）、`JA/HS-001`（`35.05`・`138.05`、行 3）、`JA/HS-003`（`36.15`・`139.15`、行 5）、`JA/HS-004`（`37.0`・`140.0`、行 6） | `match_activation_zones(<サミット>, <ピークの表>, <索引>)` | `summit_peak` が `{'JA/HS-002': K2, 'JA/HS-001': K1, 'JA/HS-003': K2}`（鍵の順はサミットの順）、`peak_summits` が `{K1: [JA/HS-001], K2: [JA/HS-002, JA/HS-003]}`（鍵の順は `K1`・`K2` のピークの順で、サミットの順でない。値はサミットの順）、`peak_status` が `{K1: 'matched', K2: 'ambiguous'}`（鍵の順は同じ）、`overlaps` が空。`JA/HS-004` はどこにも入らず、`summit_peak` に無い |
| `UT-match_summits-25` | 確定した 2 つ以上のピークの AZ に含まれるサミット（AO1。全サミットを挙げて止まる） | 同じプロセス。ピークの表は `K1`（`35.10000000`・`138.10000000`・標高 `1000`・`prominence` `300`・`true`）、`K2`（`35.20000000`・`138.20000000`・標高 `900`・`prominence` `200`・`true`）。索引は `[(K1, AZ_1), (K2, AZ_2)]`。サミットはこの順: `JA/HS-001`（`35.15`・`138.15`。`AZ_1` と `AZ_2` の重なりの中）、`JA/HS-002`（`35.05`・`138.05`。`AZ_1` だけ）、`JA/HS-003`（`35.12`・`138.12`。重なりの中） | `match_activation_zones` に | 終了コード 1 で AO1。1 行目は `2 つ以上の確定したピークの AZ に含まれるサミットがある: JA/HS-001（35.15,138.15）: 35.10000000,138.10000000（key_col_resolved=true）、35.20000000,138.20000000（key_col_resolved=true）；JA/HS-003（35.12,138.12）: 35.10000000,138.10000000（key_col_resolved=true）、35.20000000,138.20000000（key_col_resolved=true）`（`JA/HS-001` で止まらず `JA/HS-003` も挙げる。`JA/HS-002` は挙げない）。2 行目は `{report_analysis}` |
| `UT-match_summits-26` | 確定していないピークの AZ の重なり | 同じプロセス。サミットは `JA/HS-001`（`35.15`・`138.15`。重なりの中）の 1 件。索引は `[(K1, AZ_1), (K2, AZ_2)]` と、並びを入れ替えた `[(K2, AZ_2), (K1, AZ_1)]` の 2 つで試す。ピークの表は `K1`・`K2` の順で、ピークごとの `peak_lat`・`peak_lon`・`peak_elev`・`key_col_resolved` を次のようにする（`prominence` は `K1` が `300`、`K2` が `200`）。(a) `K1` が `35.10000000`・`138.10000000`・`1000`・`false`、`K2` が `35.20000000`・`138.20000000`・`1001`・`false`。(b) (a) の `K2` の標高を `1000` に替える。(c) `K1` が `35.10000000`・`138.20000000`・`1000`・`false`、`K2` が `35.10000000`・`138.10000000`・`1000`・`false`。(d) `K1` が `35.10000000`・`138.10000000`・`1000`・`true`、`K2` が `35.20000000`・`138.20000000`・`1001`・`false`。(e) `K1` が `35.10000000`・`138.10000000`・`1001`・`false`、`K2` が `35.20000000`・`138.20000000`・`1000`・`true`。(f) `K1` が `35.20000000`・`138.20000000`・`1000.0000000000000000000000001`・`false`、`K2` が `35.10000000`・`138.10000000`・`1000.0000000000000000000000002`・`false` | `match_activation_zones` に (a)〜(f) を、2 つの索引それぞれで | どれも止まらず、2 つの索引で戻り値が等しい。含めたピークは (a) `K2`（標高が高い）、(b) `K2`（標高が同じで緯度が高い）、(c) `K2`（標高と緯度が同じで経度が小さい）、(d) `K1`（確定が 1 つなので、標高が低くても確定した方）、(e) `K2`（同じ）、(f) `K2`（標高の差が 28 桁を超えて小さいが、降順の鍵を `copy_negate()` で作るので、`K2` が先。単項の `-` なら差が潰れて緯度の高い `K1` になる）。どれも `summit_peak` が `{'JA/HS-001': <含めたピーク>}`、`peak_summits` が `{<含めたピーク>: [JA/HS-001]}`、`peak_status` が `{<含めたピーク>: 'matched'}`、`overlaps` が `[AzOverlap(<サミット>, (K1, K2), <含めたピーク>)]`（含む AZ のピークは `peaks` の鍵の順の `(K1, K2)`。確定が 1 つの (d)(e) も入る） |
| `UT-match_summits-27` | 索引の並びによらない順と、空の入力 | 同じプロセス。(a) UT-24 の入力で、索引を `[(K2, AZ_3), (K1, AZ_1)]`（`STRtree` に渡す形の並びと `keys` を一緒に入れ替えたもの）にしたもの。(b) ピークが `{}`、索引が `shapely.STRtree([])`（`keys` は `[]`）、サミットが `JA/HS-001`（`35.05`・`138.05`）の 1 件。(c) ピークが `K1` だけ、索引が `[(K1, AZ_1)]`、サミットが 0 件 | `match_activation_zones` に | (a) UT-24 の戻り値と `==`（`peak_summits`・`peak_status` の鍵の順も同じ）。(b)(c) 止まらず、`ActivationMatch({}, {}, {}, [])` |
| `UT-match_summits-28` | delete判定ゾーンとの突き合わせ（`delete`・`unmatched`・`dominant`・`new`） | 同じプロセス。ピークの表は `K1`（`35.10000000`・`138.10000000`・標高 `1000`・`prominence` `10.5`・`true`）、`K2`（`35.20000000`・`138.20000000`・標高 `900`・`prominence` `9.75`・`true`）、`K3`（`36.10000000`・`139.10000000`・標高 `800`・`prominence` `5`・`true`）の順。索引は `[(K1, DZ), (K2, DZ), (K3, AZ_3)]`。`activation` は `ActivationMatch({}, {K3: [Summit('JA/HS-009', 'n', '100', '36.15', '139.15', 9)]}, {K3: 'matched'}, [])`。サミットはこの順: `JA/HS-001`（`35.30`・`138.30`、行 3。`DZ` の中で `K1`・`K2` の両方に含まれる）、`JA/HS-002`（`37.0`・`140.0`、行 4。どこにも入らない） | `match_delete_zones(<サミット>, <ピークの表>, <activation>, <索引>)` | `summit_status` が `{'JA/HS-001': 'delete', 'JA/HS-002': 'unmatched'}`。`dominant` が `{'JA/HS-001': DominantPeak(K2, cmp5_common.great_circle_m(35.2, 138.2, 35.3, 138.3))}`（`prominence` を `Decimal` で比べて `9.75` の `K2` が主ピーク。字句の順なら `10.5` の `K1`）で、`dist_m` が `great_circle_m(35.2, 138.2, 35.3, 138.3)` の値と `==`（主ピークからサミットへ）。`peak_status` が `{K1: 'new', K2: 'dominant'}`（`K3` は `activation.peak_summits` にあるので入らない。鍵の順は `K1`・`K2`）。`unmatched` が `[Summit('JA/HS-002', 'n', '100', '37.0', '140.0', 4)]` |
| `UT-match_summits-29` | 主ピークの選び方（key） | 同じプロセス。サミットは `JA/HS-001`（`35.30`・`138.30`）の 1 件。索引は `[(K1, DZ), (K2, DZ)]`、`activation` は `ActivationMatch({}, {}, {}, [])`（(d)(e) だけ下のとおり）。ピークは `K1`・`K2` の順で、各ケースの列は次のとおり（記載のない列は `peak_elev` が `1000`・`900`、`col_lat`・`col_lon` が `0.00000000`）。(a) `K1` が `prominence` 空・`key_col_resolved` `false`、`K2` が `prominence` `9999`・`true`。(b) `K1` が `10.5`・`peak_lat` `35.10000000`、`K2` が `10.50`・`35.20000000`（どちらも `true`、`peak_lon` は `138.10000000`・`138.20000000`）。(c) `K1` が `10.5`・`peak_lat` `35.10`・`peak_lon` `138.2`、`K2` が `10.5`・`35.1`・`138.1`（どちらも `true`）。(d) `K1` が `prominence` `5`・`true`、`K2` が `6`・`true`。`activation` は `ActivationMatch({}, {K1: [<サミット 1 件>], K2: [<サミット 2 件>]}, {K1: 'matched', K2: 'ambiguous'}, [])`。(e) (d) の `prominence` を `K1` が `6`、`K2` が `5` に替えたもの。(f) `K1` が `prominence` 空・`key_col_resolved` `false`・`peak_lat` `35.10000000`・`peak_lon` `138.10000000`、`K2` が `prominence` 空・`false`・`35.20000000`・`138.20000000`（候補がすべて未確定）。(g) `K1` が `prominence` 空・`false`・`peak_lat` `35.10`・`peak_lon` `138.2`、`K2` が `prominence` 空・`false`・`35.1`・`138.1`（候補がすべて未確定） | `match_delete_zones` に (a)〜(g) を | 主ピークは (a) `K2`（確定していないピークは最大として扱う。`peak_status` は `{K1: 'new', K2: 'dominant'}`）、(b) `K2`（`10.5` と `10.50` は同じ値で、`peak_lat` の降順）、(c) `K2`（`peak_lat` の `35.10` と `35.1` は同じ値で、`peak_lon` の昇順。字句の順なら `K1`）、(d) `K1`（`matched` のピークも候補で、主ピークに選ばれる）、(e) `K2`（`ambiguous` のピークも同じ）、(f) `K2`（未確定のピーク同士は `prominence` を見ず、`peak_lat` の降順）、(g) `K2`（`35.10` と `35.1` は同じ値で、`peak_lon` の昇順。空の `prominence` を `Decimal` にしない）。(f)(g) の `peak_status` は `{K1: 'new', K2: 'dominant'}`。(d)(e) の `peak_status` は空の辞書（どちらのピークも AZ にサミットがある） |
| `UT-match_summits-30` | 空の入力（delete判定ゾーン） | 同じプロセス。(a) ピークが `{}`、索引が `shapely.STRtree([])`（`keys` は `[]`）、サミットが `JA/HS-001`（`35.30`・`138.30`、行 3）の 1 件。(b) ピークが `K1`（`35.1`・`138.1`・標高 `1`・`prominence` `1`・`true`）だけ、索引が `[(K1, DZ)]`、サミットが 0 件 | `match_delete_zones` に（`activation` は `ActivationMatch({}, {}, {}, [])`） | (a) 止まらず、`summit_status` が `{'JA/HS-001': 'unmatched'}`、`dominant` が空、`peak_status` が空、`unmatched` が 1 件。(b) 止まらず、`summit_status`・`dominant`・`unmatched` が空、`peak_status` が `{K1: 'new'}` |
| `UT-match_summits-31` | 照合する点の並びと陸のコル | 同じプロセス。ピークの表は次の順。`K1`（`35.1`・`138.1`、標高 `1000`、`prominence` `10`、`true`、`col_lat` `35.0`・`col_lon` `138.0`）、`K2`（`35.2`・`138.2`、`900`、`9`、`true`、コルは `0.0`・`0.0`）、`K3`（`35.3`・`138.3`、`800`、`8`、`true`、コルは `0`・`0.00000000`）、`(4, 4)`（`35.4`・`138.4`、`700`、`prominence` 空、`false`、コルは `35.1`・`138.1`）、`(5, 5)`（`35.5`・`138.5`、`600`、`7`、`true`、コルは `0`・`138.0`）、`(6, 6)`（`35.6`・`138.6`、`500`、`6`、`true`、コルは `35.0`・`0.00`）。サミットは `JA/HS-001`（`35.05`・`138.05`）、`JA/HS-002`（`36`・`139`） | `_region_points(<ピークの表>, <サミット>)` | `LocatePoint` を `(kind, key, lat, lon)` で書くと、`('peak', K1, '35.1', '138.1')`・`('peak', K2, '35.2', '138.2')`・`('peak', K3, '35.3', '138.3')`・`('peak', (4, 4), '35.4', '138.4')`・`('peak', (5, 5), '35.5', '138.5')`・`('peak', (6, 6), '35.6', '138.6')`・`('col', K1, '35.0', '138.0')`・`('summit', 'JA/HS-001', '35.05', '138.05')`・`('summit', 'JA/HS-002', '36', '139')` のこの順（ピーク → コル → サミット）。コルは `K1` だけ（`K2` は両方 0、`K3` は値で両方 0、`(4, 4)` は確定していない、`(5, 5)` と `(6, 6)` は片方だけ 0 なので入らない） |
| `UT-match_summits-32` | 地域と市区町村への照合 | 同じプロセス。`R1 = RegionFeature('JA', 'HS', '広島県', {})`、`R2 = RegionFeature('JA', 'YN', '山梨県', {})`、`M1 = MunicipalityFeature('廿日市市', '34210', {})`。`boundaries` は `Boundaries([R1, R2], [M1], [])`。索引は `SpatialIndexes(None, None, <地域の索引>, <市区町村の索引>)`（`activation`・`delete` は使わない）で、地域の索引は `[(0, box(0, 0, 10, 10)), (1, box(5, 5, 15, 15))]`、市区町村の索引は `[(0, box(0, 0, 8, 8))]`。点はこの順: `LocatePoint('peak', K1, '5', '10')`（`R1` の東の辺の上で、`R2` の南の辺の上でもある）、`LocatePoint('peak', K2, '12', '12')`、`LocatePoint('summit', 'JA/HS-001', '20', '20')`、`LocatePoint('col', K1, '9', '12')`、`LocatePoint('peak', K3, '3', '3')` | `locate_regions(<点>, <boundaries>, <索引>)` | `locations` の鍵が点の順に `('peak', K1)`・`('peak', K2)`・`('summit', 'JA/HS-001')`・`('col', K1)`・`('peak', K3)`。値は順に `Location(R1, '')`（辺の上は内で、`R1` と `R2` の両方に当たるが、ファイルの順の最初の `R1`）、`Location(R2, '')`、`Location(None, '')`、`Location(R2, '')`、`Location(R1, '廿日市市')`。`outside` は順に `OutsidePoint(<K1 のピークの点>, ('市区町村',))`、`OutsidePoint(<K2 のピークの点>, ('市区町村',))`、`OutsidePoint(<サミットの点>, ('地域', '市区町村'))`、`OutsidePoint(<コルの点>, ('市区町村',))`（`K3` は両方に入るので入らない） |
| `UT-match_summits-33` | 無いファイルと空の入力（照合） | 同じプロセス。UT-32 の点・`R1`・`box(0, 0, 10, 10)` を使う。(a) `Boundaries(None, None, [])` と `SpatialIndexes(None, None, None, None)`。(b) `Boundaries([R1], None, [])` と、地域の索引が `[(0, box(0, 0, 10, 10))]`、市区町村の索引が `None` の `SpatialIndexes`。点は UT-32 の先頭の 3 つ。(c) UT-32 の `boundaries` と索引で、点が空の並び。(d) `Boundaries([], [], [])` と、どちらの索引も `shapely.STRtree([])`（`keys` は `[]`）の `SpatialIndexes`。点は `LocatePoint('peak', K1, '5', '10')` の 1 つ | `locate_regions` に | (a) すべての点が `Location(None, '')`、`outside` が空（ファイルが無い層は照合せず、警告の材料にも入れない）。(b) `Location(R1, '')`（`K1`）・`Location(None, '')`（`K2`）・`Location(None, '')`（サミット）、`outside` が `K2` のピークの点とサミットの点の 2 件でどちらも `('地域',)`（市区町村は無いので `layers` に入らない）。(c) `RegionMatch({}, [])`。(d) `Location(None, '')`、`outside` が `OutsidePoint(<ピークの点>, ('地域', '市区町村'))`（ファイルがあって Feature が 0 件の層は、どの点も入らない） |
| `UT-match_summits-34` | 仮サミットコードの採番の順 | 同じプロセス。`RH = RegionFeature('JA', 'HS', '広島県', {})`。ピークの表（`peak_lat`・`peak_lon`・標高・`prominence`・`key_col_resolved`、`peak_status` の値）は、`K1`（`35.10000000`・`138.10000000`・`1000`・`50`・`true`・`new`）、`K2`（`35.20000000`・`138.20000000`・`1000`・`60`・`true`・`dominant`）、`K3`（`35.30000000`・`138.30000000`・`1000`・空・`false`・`new`）、`(4, 4)`（`35.40000000`・`138.40000000`・`1100`・`10`・`true`・`new`）、`(5, 5)`（`35.20000000`・`138.10000000`・`1000`・`60`・`true`・`new`）。`max_prefix` は `'A'`。(a) `locations`（鍵は `('peak', <画素>)`）のすべてが `Location(RH, '')`。(b) (a) の `K3` と `(5, 5)` を `Location(None, '')` に替える。(c) `peak_status` が空 | `assign_provisional_codes(<peak_status>, <ピークの表>, <locations>, 'A', False)` に (a)(b)(c) を | (a) `{K1: 'JA/HS-A03', K2: 'JA/HS-A02', K3: 'JA/HS-A04', (4, 4): 'JA/HS-A00', (5, 5): 'JA/HS-A01'}`（標高の降順で `(4, 4)` が先。標高が同じ中では `prominence` の降順で、`prominence` が `60` の `K2` と `(5, 5)` は `peak_lat` も同じなので `peak_lon` の昇順で `(5, 5)` が先、`50` の `K1` が続き、確定していない `K3` が末尾。`new` と `dominant` は区別しない）。鍵の順は `peak_status` の順。(b) `{K1: 'JA/HS-A02', K2: 'JA/HS-A01', K3: 'ZZ/ZZ-A01', (4, 4): 'JA/HS-A00', (5, 5): 'ZZ/ZZ-A00'}`（地域に入らないピークは `ZZ/ZZ` のエリアに入り、エリアごとに `A00` から）。(c) 空の辞書 |
| `UT-match_summits-35` | 連番の上限（100 件までは止まらず、超えたエリアをすべて挙げて止まる） | 同じプロセス。`RH`（UT-34）と `RY = RegionFeature('JA', 'YN', '山梨県', {})`。ピークは鍵 `(i, i)`（`i` は 0 から）、`peak_lat` `35.10000000`・`peak_lon` `138.10000000`・`peak_elev` `str(5000 - i)`・`prominence` `1`・`true`、`peak_status` は `'new'` | (a) 100 件すべて `RH`、`max_prefix` `'A'`。(b) 101 件すべて `RH`、`'B'`。(c) 101 件すべて `RH`、`'A'`。(d) 203 件で、`i` が 0〜100 の 101 件が `RH`、101〜202 の 102 件が `RY`、`'A'`。(e) 101 件すべて `Location(None, '')`、`'A'`、`regions_missing` が真（(a)〜(d) は偽）。いずれも `assign_provisional_codes` に | (a) 止まらず、`(0, 0)` が `JA/HS-A00`、`(99, 99)` が `JA/HS-A99`。(b) 止まらず、`(99, 99)` が `JA/HS-A99`、`(100, 100)` が `JA/HS-B00`。(c) 終了コード 1 で PN1。1 行目は `仮サミットコードの連番が上限を超えるエリアがある（provisional_code_max_prefix=A、1 エリアの上限 100 件）: JA/HS（101 件、上限を 1 件超える）`、2 行目は `provisional_code_max_prefix を上げてから、{rerun4}`。(d) 終了コード 1 で PN1。1 行目の `{list}` が `JA/HS（101 件、上限を 1 件超える）、JA/YN（102 件、上限を 2 件超える）`（2 つとも挙げ、エリアの文字列の順）。(e) 終了コード 1 で PN2。1 行目は `地域の GeoJSON が無いため、すべてのピークが ZZ のエリアに入り、仮サミットコードの連番が上限を超える（provisional_code_max_prefix=A、1 エリアの上限 100 件）: ZZ/ZZ（101 件、上限を 1 件超える）`、2 行目は `{cmp1_rebuild}` |
| `UT-match_summits-36` | 採番の順で 28 桁を超える標高の差を潰さない | 同じプロセス。`RH`（UT-34）。ピークの表は `K1`（`35.20000000`・`138.20000000`・標高 `1000.0000000000000000000000001`・`prominence` `1`・`true`）、`K2`（`35.10000000`・`138.10000000`・標高 `1000.0000000000000000000000002`・`1`・`true`）。`peak_status` は `{K1: 'new', K2: 'dominant'}`、`locations` はどちらも `Location(RH, '')` | `assign_provisional_codes(<peak_status>, <ピークの表>, <locations>, 'A', False)` | `{K1: 'JA/HS-A01', K2: 'JA/HS-A00'}`（標高が高い `K2` が先。降順の鍵を `copy_negate()` で作るので差が潰れない。単項の `-` なら差が潰れて `peak_lat` の高い `K1` が先になる） |
| `UT-match_summits-37` | 標高バンドの境目と切り捨て | 同じプロセス | (a) `_band_points(h)` に 149・150・499・500・649・650・849・850・1099・1100・1499・1500、(b) `_floor_m(text)` に `'149.99'`・`'150.00'`・`'1000.60'`・`'0150'`、(c) `_band_points(_floor_m('149.99'))` と `_band_points(_floor_m('150.00'))` | (a) 順に `None`・1・1・2・2・4・4・6・6・8・8・10。(b) 順に 149・150・1000・150（`Decimal` の切り捨てで、浮動小数にしない）。(c) `None` と 1 |
| `UT-match_summits-38` | SOTA 既存サミット GeoJSON を使わない（SN1）と全ファイルが無い | 同じプロセス。(a) `<tmp>` に何も置かない。(b) `<tmp>/geojson_v3/` を作るだけで、ファイルは置かない | (a) `read_sota_names('<tmp>', None)` と `read_sota_names('<tmp>', 3)`、(b) `read_sota_names('<tmp>', 3)` | (a) どちらも止まらず、`names` が空の辞書。`warnings` は前者が `[('SN1', 'SOTA 既存サミット GeoJSON を使わない: 設定の sota_geojson_version が未設定。すべてのサミットの summit_name_jp が空文字になる')]`、後者が `[('SN1', 'SOTA 既存サミット GeoJSON を使わない: <tmp>/geojson_v3 が無い。すべてのサミットの summit_name_jp が空文字になる')]`。(b) 止まらず、`names` が空の辞書。`warnings` は `ja0`〜`ja9` の 10 件の `('SN2', 'SOTA 既存サミット GeoJSON を使わない: <tmp>/geojson_v3/ja<N>_v3.geojson: ファイルが無い')`（`N` の順） |
| `UT-match_summits-39` | `name` の読み方と同じコードの山岳名 | 同じプロセス。`ja0_v3.geojson` の Feature をこの順に 13 件: `nf('JA/XX-001(山岳名)')`・`nf('JA/XX-002(山(北))')`・`nf('JA/XX-003')`・`nf('JA/XX-004(xy')`・`nf('JA/XX-005()')`・`nf('(abc)')`・`{"type": "Feature", "properties": {"name": 5}}`・`{"type": "Feature"}`・`nf('JA/XX-006( 山 )')`・`nf('JA/XX-007(甲)')`・`nf('JA/XX-007(乙)')`・`nf('JA/XX-007(甲)')`・`nf('JA/XX-008(丙)')`。`ja3_v3.geojson` は `nf('JA/XX-008(丙)')`・`nf('JA/XX-009(丁)')`。ほかの `ja<N>` は置かない | `read_sota_names('<tmp>', 3)` | 止まらず、`names` が `{'JA/XX-001': '山岳名', 'JA/XX-002': '山(北)', 'JA/XX-006': ' 山 ', 'JA/XX-007': '', 'JA/XX-008': '丙', 'JA/XX-009': '丁'}`（鍵はこの順。内側の `(` を含む山岳名は `山(北)`。空白は除かず `' 山 '`。同じコードに違う山岳名がある `JA/XX-007` は空文字。同じ山岳名の重なり〈`JA/XX-008` が 2 つのファイルに〉は空にしない）。`warnings` は、`('SN3', 'SOTA 既存サミット GeoJSON の name を読めない Feature を飛ばした: <tmp>/geojson_v3/ja0_v3.geojson: 6 件')`（3〜8 番目の 6 件）、`ja1`・`ja2`・`ja4`〜`ja9` の SN2（`ファイルが無い`。この順）、最後に `('SN4', 'SOTA 既存サミット GeoJSON の同じコードに違う山岳名がある: JA/XX-007（甲・乙）')` |
| `UT-match_summits-40` | 読めないファイルと FeatureCollection でないファイル | 同じプロセス。(a) `ja1` の中身が `{"type":"FeatureCollection","features":[{"a":NaN}]}`、(b) `ja2` が `b'\xff\xfe\x00'`、(c) `ja3` が `x`、(d) `ja4` がディレクトリ、(e) `ja5` が `{"type":"Feature"}`、(f) `ja6` が `{"type":"FeatureCollection"}`、(g) `ja7` が `{"type":"FeatureCollection","features":[]}`、(h) `ja0` が `nf('JA/XX-001(山岳名)')` の 1 件。`ja8`・`ja9` は置かない | `read_sota_names('<tmp>', 3)` | 止まらず、`names` が `{'JA/XX-001': '山岳名'}`。`warnings` は (a)〜(f) の順に SN2 で、`{reason}` が (a) `NaN は JSON の数でない`、(b) `UTF-8 として読めない`、(c) `Expecting value: line 1 column 1 (char 0)`、(d) `Is a directory`、(e)(f) `FeatureCollection でない`。(g) は警告なし（Feature が 0 件でよい）。続けて `ja8`・`ja9` の SN2（`ファイルが無い`） |
| `UT-match_summits-41` | ピークの属性（`category`・ポイント・`review_group_id`・所属する山岳名） | 同じプロセス。属性の入力 | `derive_attributes(<peaks>, <summits>, <activation>, <deletion>, <codes>, <regions>, <names>)` の `peaks` | 鍵は `K1`〜`K6` の順。`PeakAttrs(points, is_band_change_candidate, category, review_reason, review_group_id, summit_name_jp, rationale)` で、`K1` が `(6, None, 'add', '', '', '', <UT-44 (a) の文字列>)`、`K2` が `(8, None, 'add', '', '', '', <UT-44 (b) の文字列>)`、`K3` が `(None, False, 'no_change', '', '', '山J', '')`（ピークの標高 `149.99` は 149 で算出表に無く、`is_band_change_candidate` は `false`、`rationale` は空）、`K4` が `(8, True, 'band_change', '', '', '山B', <UT-45 (a) の文字列>)`、`K5` が `(6, None, 'review', 'multiple_summits_in_az', <ID>, '', '')`（`<ID>` は `az:` の後ろに `JA/AB-003`、縦棒 U+007C、`JA/AB-020` を続けた文字列。AZ の中の 2 件のコードが入力の順〈020、003〉と文字列の順〈003、020〉で違い、文字列の順につなぐ）、`K6` が `(4, False, 'no_change', '', '', '', '')`（`JA/AB-030` は山岳名の表に無く空文字。標高 `800.9` は 800 で `points` が 4、AZ の中のサミットの `sota_points` も 4 で同じ） |
| `UT-match_summits-42` | サミットの属性・`groups`・`NullPoints` | 同じプロセス。属性の入力 | UT-41 の戻り値の `summits`・`groups`・`null_points` | `SummitAttrs(match_status, sota_points, category, review_reason, review_group_id, summit_name_jp, dominant_peak_code, dominant_peak_dist_m, rationale)` で、鍵はサミットの順。`JA/AB-010` が `('matched', None, 'no_change', '', '', '山J', '', None, '')`、`JA/AB-002` が `('matched', 6, 'band_change', '', '', '山B', '', None, '')`、`JA/AB-020` が `('ambiguous', 6, 'review', 'multiple_summits_in_az', <K5 の review_group_id>, '', '', None, '')`、`JA/AB-003` が `('ambiguous', 6, 'review', 'multiple_summits_in_az', <同じ>, '山三', '', None, '')`、`JA/AB-030` が `('matched', 4, 'no_change', '', '', '', '', None, '')`、`JA/CD-001` が `('delete', 2, 'delete', '', '', '', 'JA/HS-A00', 1234.6, <UT-45 (c) の文字列>)`（主ピークが `dominant` で、仮サミットコードが `dominant_peak_code`）、`JA/CD-002` が `('delete', None, 'delete', '', '', '', 'JA/AB-002', 0.0, <UT-45 (b) の文字列>)`（主ピークが `matched` で、AZ の中のサミットのコード。`AltM` が 149 でポイントは `None`）、`JA/CD-003` が `('delete', 2, 'review', 'ambiguous_parent', <K5 の review_group_id>, '', '', 10.2, '')`（主ピークが `ambiguous`。コードは空文字で距離は保持。`10.25` は 2 進で正確に表せ、偶数側の `10.2`）、`JA/CD-004` が `('unmatched', 1, 'review', 'unmatched', '', '', '', None, '')`。`groups` は `[ReviewGroup(<K5 の review_group_id>, K5, ('JA/AB-003', 'JA/AB-020'), ('JA/CD-003',))]`。`null_points` は `NullPoints((K3,), (<JA/AB-010 の Summit>, <JA/CD-002 の Summit>), (K3,))` |
| `UT-match_summits-43` | `groups` の並びと空の入力 | 同じプロセス。(a) `peaks` が `K1`・`K2` の 2 つの `ambiguous` のピーク（`peak_summits` は `K1` が `JA/ZZ-009`・`JA/ZZ-001`、`K2` が `JA/AA-005`・`JA/AA-002`。標高は 1000 と 900）、サミットはこの 4 件（`AltM` は 600）、`DeleteMatch` は空。(b) すべて空の入力 | `derive_attributes` に (a)(b) を（`regions.locations` は (a) では `K1`・`K2` の `Location(RH, '市')`） | (a) `groups` が `K2` のグループ（`group_id` が `az:` の後ろに `JA/AA-002`、縦棒、`JA/AA-005`）、`K1` のグループ（`az:` の後ろに `JA/ZZ-001`、縦棒、`JA/ZZ-009`）の順（`peaks` の鍵の順でなく、`group_id` の文字列の順）。(b) 止まらず、`Attributes({}, {}, [], NullPoints((), (), ()))` |
| `UT-match_summits-44` | rationale の追加根拠（※2） | 同じプロセス | `build_rationale('add', <ピーク>, <Location>, None, None, <points>, '')`（`<points>` は (a) が 6、(b) が 8、(c)〜(e) が 1。`add` は使わない値）に、(a) `K1` と `Location(RH, '廿日市市')`、(b) `K2` と同じ `Location`、(c) `row(1, '35.10', '138.20', '300', '12.5', 'true', '35.0', '0', '10.5')`（陸のコルの片方だけ 0）と `Location(RH, '市')`、(d) `row(1, '35.10', '138.20', '300', '12.5', 'true', '0.0', '138.0', '10.5')` と `Location(RH, '市')`、(e) `row(1, '35.10', '138.20', '300', '', 'false', '0.0', '0.0', '')` と `Location(None, '')` | 戻り値は全文の文字列（行を `\n` でつなぐ。末尾に改行なし）。(a) `国土地理院標高タイルで解析\n35.10,138.10\n所在地：広島県 廿日市市\nコル位置：35.00,138.00\nコル標高：950.40m\nプロミネンス：50m`。(b) `国土地理院標高タイルで解析\n35.20,138.20\n所在地：広島県 廿日市市\nコル位置：海面\nコル標高：0.00m\nプロミネンス：60m`。(c)(d) 海面として `国土地理院標高タイルで解析\n35.10,138.20\n所在地：広島県 市\nコル位置：海面\nコル標高：10.5m\nプロミネンス：12.5m`。(e) `国土地理院標高タイルで解析\n35.10,138.20\n所在地： \nコル位置：未確定\nコル標高：未確定\nプロミネンス：未確定`（所在地の行は `所在地：` の後に空白 1 つだけ。数は字句のまま） |
| `UT-match_summits-45` | rationale の変更根拠（※5）と削除根拠（※4） | 同じプロセス | (a) `build_rationale('change', K4, Location(RH, '廿日市市'), <JA/AB-002 の Summit>, 6, 8, '')`、(b) `build_rationale('delete', K4, None, None, None, None, 'JA/AB-002')`、(c) `build_rationale('delete', K2, None, None, None, None, '')` | (a) `国土地理院 DEM 解析による標高再測定: 900m (6pt) → 1300m (8pt)\n座標: 35.40,138.40（広島県 廿日市市）`（`1300.50` の切り捨てが 1300）。(b) `国土地理院標高タイルを解析し、JA/AB-002に従属している事を確認`。(c) `国土地理院標高タイルを解析し、追加申請するピーク（35.20,138.20）に従属している事を確認` |
| `UT-match_summits-46` | 山岳 ID の照合（変更・削除の申請） | 同じプロセス。申請の入力。申請は削除の `ap('delete', 'JA/AB-002')`（現役と一致）・`ap('delete', 'JA/ZZ-777')`（廃止済みと一致）・`ap('delete', 'JA5/KC-027')`（アソシエーションだけ違う）・`ap('delete', 'JA5/MM-001')`（地域コード `MM` が 2 つのアソシエーションにある）・`ap('delete', 'JA6/KC-050')`（廃止済みの `JA/KC-050` と後ろが同じ）・`ap('delete', 'JA/XX-999')`（どれにも無い）・`ap('delete', 'JA/MM-900')`（廃止済みと一致し、地域コード `MM` が 2 つのアソシエーションにある）・`ap('delete', 'JA5/MM-200')`（地域コード `MM` が 2 つのアソシエーションにあり、後ろが現役の `JA/MM-200` と同じ）を、`row` を 1〜8 にして順に | `match_pending_applications(<updatelist>, <summits_list>, <peaks>, <activation>, <deletion>, <index>, <attrs>)` | `rows` の鍵が `('peak', K4)` と `('summit', 'JA/KC-027')` の 2 つ。`('peak', K4)` の申請の `summit_code` が `JA/AB-002`、`('summit', 'JA/KC-027')` の申請の `summit_code` が `JA/KC-027`（SOTA サミットリストの表記に揃える。`JA5/KC-027` は書かれていない）で、その申請の `match` が `held`（行の `match` は空文字）。`notices` は、`JA5/MM-001` の `Notice('ambiguous_region', <_REASON_AMBIGUOUS_REGION>, 2026, 4, '削除', 'JA5/MM-001', 'X', '2026-10-01', 'JA5/MM-001')` と、`JA/XX-999` の `Notice('unknown_id', <_REASON_UNKNOWN_ID>, 2026, 6, '削除', 'JA/XX-999', 'X', '2026-10-01', 'JA/XX-999')` と、`JA5/MM-200` の `Notice('ambiguous_region', <_REASON_AMBIGUOUS_REGION>, 2026, 8, '削除', 'JA5/MM-200', 'X', '2026-10-01', 'JA5/MM-200')` の 3 件だけ（`JA/ZZ-777`・`JA/MM-900`・`JA6/KC-050` は反映済みで、知らせない。`JA/MM-900` は廃止済みの一致が地域コードの重なりより先、`JA5/MM-200` は地域コードの重なりが後ろの一致より先なので、`JA/MM-200` の行は作らない。`JA5/KC-027` は `KC` が `JA` だけにあるので、現役の後ろの一致で `JA/KC-027` に当たる） |
| `UT-match_summits-47` | 変更のバンドの選別 | 同じプロセス。申請の入力。申請は `JA/AB-002`（`900` で 6 pt）への変更で、`new_elev` が (a) `'0150'`、(b) `'1300.99'`、(c) `'950'`（同じバンド）、(d) `'149.99'`（算出表に無い）、(e) `'1500'`（10 pt）。(f) 申請は `JA/CD-004`（`unmatched`）への変更で、`new_elev` が `'1300'`。`JA/CD-004` の `Summit` の `AltM` を `'140'`（算出表に無い）に替える（`summits_list.summits` と `deletion.unmatched` の同じ `Summit` を替える） | それぞれ別の呼び出しで `match_pending_applications` | (a) `rows` に `('peak', K4)` があり、申請が `new_points` 1、`new_alt_m` が `JsonNumber('150')`、`match` が `different`（ピークの `points` 8 と違う）。(b) `new_points` 8、`match` が `same`。(c)(d) 取り込まず、知らせない（`rows` が空、`notices` は読み込みの知らせだけ）。(e) `new_points` 10、`match` が `different`。(f) 取り込まず、知らせない（`rows` が空、`notices` は読み込みの知らせだけ。今のバンドが算出表に無いときも、(c)(d) と同じく取り込まない） |
| `UT-match_summits-48` | 当てる表（削除・変更の申請と、サミットの状態） | 同じプロセス。申請の入力。申請は削除と変更（`new_elev` が `'2000'` で 10 pt）を、(a) `JA/CD-001`（`delete`）、(b) `JA/AB-002`（`matched` で親が `band_change`。削除と、`new_elev` が `'1300'` の変更〈8 pt〉）、(c) `JA/AB-030`（親が `no_change`）、(d) `JA/AB-020`（`ambiguous`）、(e) `JA/CD-004`（`unmatched`）のそれぞれにつき 1 つずつ | `match_pending_applications` に (a)〜(e) をそれぞれ別の呼び出しで | (a) `('summit', 'JA/CD-001')` に削除が `same`、変更が `different`（行の `applications` の並びは、申請日が同じなのでアクションで決まり、変更、削除の順。UT-50 (a) と同じ）。(b) `('peak', K4)` に削除が `different`、変更が `same`（並びは (a) と同じで、変更、削除の順）。(c)(d) `rows` が空で、`notices` も空（候補の判定を付けず、知らせもしない）。(e) `('summit', 'JA/CD-004')` に削除と変更がどちらも `held` で、行の `match` が空文字 |
| `UT-match_summits-49` | 追加の申請を AZ に当てる | 同じプロセス。申請の入力。追加の申請は (a) `ap('add', lat='35.05', lon='138.05')`（`AZ_1` だけ）、(b) `lat='35.15'`・`lon='138.15'`（`AZ_1` と `AZ_2` の重なり）、(c) `lat='36.10'`・`lon='139.10'`（`AZ_3`。`K4` は `matched`）、(d) `lat='40.0'`・`lon='140.0'`（どこにも入らない）。(b) の別の呼び出しで、`peaks` の `K1`・`K2` の `peak_elev` を入れ替える | `match_pending_applications` に (a)〜(d) をそれぞれ別の呼び出しで | (a) `('peak', K1)` に当たり、申請の `match` が `same`、行の `match` が `same`。(b) `K2`（`peak_elev` が高い方）に当たる。入れ替えると `K1` に当たる。(c) 当てず、知らせない（`rows` が空、`notices` も空）。(d) `rows` が空で、`notices` が `[Notice('unmatched_add', <_REASON_UNMATCHED_ADD>, 2026, 1, '追加', '', 'X', '2026-10-01', '40.0,140.0')]` |
| `UT-match_summits-50` | `pending_applications` の並びと数の字句 | 同じプロセス。申請の入力。(a) `JA/CD-001` への申請を、`ap('delete', 'JA/CD-001', applicant='F', row=2)`・`ap('change', 'JA/CD-001', new_elev='2000', applicant='G', row=3)`・`ap('change', 'JA/CD-001', new_elev='1800', applicant='G', row=4)` の順に。(b) 追加の申請 `ap('add', lat='+35.050', lon='0138.050', applicant='B', applied_on='2026-10-02')` と、`ap('add', lat='35.15', lon='138.15', applicant='A', applied_on='2026-10-02')`（`K2` に当たる）。(c) `JA/AB-002` への変更 `ap('change', 'JA/AB-002', new_elev='0150', applied_on='2026-09-02', years=(2026, 2025))` と `ap('delete', 'JA/AB-002', applied_on='2026-09-01')` と `ap('change', 'JA/AB-002', new_elev='1300', applied_on='2026-09-01')` の順に。(d) `K1` に当たる追加 2 つを、`ap('add', lat='35.07', lon='138.05', applicant='A', row=2)`・`ap('add', lat='35.05', lon='138.07', applicant='B', row=3)` の順に（どちらも `AZ_1` だけに入る）。(e) `K1` に当たる追加 2 つを、`ap('add', lat='35.05', lon='138.07', applicant='A', row=2)`・`ap('add', lat='35.05', lon='138.05', applicant='B', row=3)` の順に。(f) `K1` に当たる追加 2 つを、`ap('add', lat='35.05', lon='138.05', applicant='B', row=2)`・`ap('add', lat='35.050', lon='138.050', applicant='A', row=3)` の順に | それぞれ別の呼び出しで | (a) 行の `applications` の並びが、変更〈`2000`〉、変更〈`1800`〉、削除（申請日が同じなので、アクション〈変更が削除より先〉で決まる。変更の 2 つは key が全部同じ〈山岳 ID も申請者も同じ〉で、`updatelist.applications` の順のまま）。`dict` のキーの順は `action`・`summit_code`・`lat`・`lon`・`new_alt_m`・`new_points`・`applicant`・`applied_on`・`years`・`match`。(b) `('peak', K1)` の申請の `lat` が `JsonNumber('35.050')`（先頭の `+` を除き、末尾の 0 は変えない）、`lon` が `JsonNumber('138.050')`（先頭の余分な 0 を除く）、`summit_code` が空文字、`new_alt_m`・`new_points` が `None`。`('peak', K2)` の `lat` が `JsonNumber('35.15')`。(c) `('peak', K4)` の `applications` が 2026-09-01 の変更〈`1300`、`new_alt_m` が `JsonNumber('1300')`〉、2026-09-01 の削除、2026-09-02 の変更〈`new_alt_m` が `JsonNumber('150')`。先頭の余分な 0 を除く〉の順で、最後の申請の `years` が `[2026, 2025]`（新しい順の `list`）。`match` は `same`・`different`・`different` で、行の `match` は `same`。(d) `('peak', K1)` の `applications` の `lat`・`lon` が、`35.05`・`138.07`〈B〉、`35.07`・`138.05`〈A〉の順（緯度が先に決め、申請者より座標が先）。(e) `138.05`〈B〉、`138.07`〈A〉の順（緯度が同じなら経度の昇順で、申請者より先）。(f) `35.050`〈A〉、`35.05`〈B〉の順（座標は 10 進の値で比べて等しく、申請者の `A` が先。字句の文字列で比べると逆になる） |
| `UT-match_summits-51` | 知らせる行の並び | 同じプロセス。申請の入力。`updatelist.notices` を `Notice('unreadable_row', …, 2025, 2, …)`・`Notice('unreadable_update', …, 2025, None, …)`・`Notice('unreadable_row', …, 2026, 16, …)` の順にし、申請は `ap('delete', 'JA/XX-999', row=20)`・`ap('delete', 'JA5/MM-001', row=17)`・`ap('add', lat='40.0', lon='140.0', row=4)` の順 | `match_pending_applications` | `notices` の `(year, row, kind)` が、`(2026, 4, 'unmatched_add')`・`(2026, 16, 'unreadable_row')`・`(2026, 17, 'ambiguous_region')`・`(2026, 20, 'unknown_id')`・`(2025, None, 'unreadable_update')`・`(2025, 2, 'unreadable_row')` の順（年の表が `updates` に現れる順 → その年の表の中では Update の知らせが先 → 通し番号の順）。読み込みの知らせと照合の知らせが 1 つの並びになる |
| `UT-match_summits-52` | 申請が 0 件 | 同じプロセス。申請の入力。`updatelist.applications` が空で、`notices` が `Notice('unreadable_update', …, 2026, None, …)` の 1 件 | `match_pending_applications` | 止まらず、`rows` が空の辞書、`notices` が同じ 1 件 |
| `UT-match_summits-53` | `pending_note` の文 | 同じプロセス | `build_pending_note` に (a) 空の並び、(b) `{'action': 'change', 'applied_on': '2026-01-02', 'years': [2026]}` の 1 件、(c) (b) の後ろに `{'action': 'delete', 'applied_on': '2026-03-05', 'years': [2026]}`、(d) `{'action': 'add', 'applied_on': '2026-10-19', 'years': [2026, 2025]}` の 1 件 | (a) 空文字。(b) `変更 2026-01-02（2026年の表）`。(c) `変更 2026-01-02（2026年の表）／削除 2026-03-05（2026年の表）`。(d) `追加 2026-10-19（2026・2025年の表）`（年は新しい順のまま `・` でつなぐ。申請者を含めない） |
| `UT-match_summits-54` | 片側だけポイントが null の `matched` | 同じプロセス。属性の入力の `row` だけを使い、`K1`・`K2` はこの UT だけの値（属性の入力の `K1`・`K2` とは別）。`K1 = row(2, '35.10', '138.10', '800.90', '50', 'true', '35.00', '138.00', '700')`、`K2 = row(3, '35.20', '138.20', '149.99', '5', 'false', '0.0', '0.0', '')`。サミットは `JA/AB-001`（`140`・`35.11`・`138.11`・3）、`JA/AB-002`（`800`・`35.21`・`138.21`・4）をこの順に。判定の結果は直接作る: `ActivationMatch({'JA/AB-001': K1, 'JA/AB-002': K2}, {K1: [JA/AB-001], K2: [JA/AB-002]}, {K1: 'matched', K2: 'matched'}, [])`、`DeleteMatch({}, {}, {}, [])`、`RegionMatch({('peak', K1): Location(None, ''), ('peak', K2): Location(None, '')}, [])` | `derive_attributes(peaks, [JA/AB-001, JA/AB-002], <ActivationMatch>, <DeleteMatch>, {}, <RegionMatch>, {})` | `peaks` の `K1` が `PeakAttrs(4, False, 'no_change', '', '', '', '')`（ピークは 800 で 4pt、サミットは 140 で `None`）、`K2` が `PeakAttrs(None, False, 'no_change', '', '', '', '')`（ピークが `None`、サミットは 800 で 4pt）。`summits` の `JA/AB-001` が `('matched', None, 'no_change', '', '', '', '', None, '')`、`JA/AB-002` が `('matched', 4, 'no_change', '', '', '', '', None, '')`。`null_points` が `NullPoints((K2,), (<JA/AB-001 の Summit>,), (K1, K2))`（`is_band_change_candidate` を `False` にするのは、どちらか一方でも `None` のとき。両方が `None` のときだけにしない） |
| `UT-match_summits-55` | metadata の項目と順 | 同じプロセス。組み立ての入力（metadata）。(a) 上の入力のまま（`tiles_dir` は `<tmp>/tiles`、`repo_dir` は `<tmp>/repo`）。(b) (a) の `now` を `datetime.datetime(2026, 11, 3, 0, 5, 7, tzinfo=datetime.UTC)` にしたもの。(c) (a) の `updatelist` の `notices` を `[<notices の 1 つ目>]` にし、引数の `notices` を `[]` にしたもの（引数の `notices` の方が書かれることを見る） | `build_metadata(<ref_date>, <tiles_dir>, <repo_dir>, <updatelist>, <notices>, <now>)` | (a) `Metadata` で、`list(items)` が `summitslist_date`・`generated_at`・`updatelist_file`・`updatelist_updates`・`updatelist_notices`・`gsi_tile_latest_date`・`attribution`・`source_url`・`license_url`・`software_version`。値は `'2026-10-18'`、`'2026-11-03T00:05:07Z'`（`+09:00` の 09:05:07.987654 を UTC に直し、秒より下を切り捨てる）、`'sota_updatelist_2026.xhtml'`、`[{'year': 2026, 'update': '2026-10-14'}, {'year': 2025, 'update': ''}]`、`updatelist_notices` は `[{'kind': 'unreadable_row', 'reason': '追加の位置が 緯度,経度 の形で読めない', 'year': 2026, 'row': 3, 'action': '追加', 'target': '東京都', 'applicant': 'A', 'applied_on': '2026-01-01', 'value': 'abc'}, {'kind': 'unreadable_update', 'reason': 'Update の日付が読めない', 'year': 2025, 'row': None, 'action': '', 'target': '', 'applicant': '', 'applied_on': '', 'value': ''}]`（各 `dict` のキーの順は `kind`・`reason`・`year`・`row`・`action`・`target`・`applicant`・`applied_on`・`value`）、`'2025-10-09T08:53:20Z'`、`'地理院タイル（標高タイル）を加工して作成。出典: 国土地理院'`、`'https://maps.gsi.go.jp/development/ichiran.html'`、`'https://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html'`、`'v0.1.0'`。`warnings` は `[]`。(b) `generated_at` が `'2026-11-03T00:05:07Z'`。(c) `updatelist_notices` が `[]` |
| `UT-match_summits-56` | タイルの最新の日付 | 同じプロセス。組み立ての入力（metadata）のタイルを使う。(a) 4 つのファイルすべて。(b) (a) から `b.png` を除いたもの。(c) `a.png`・`b.png` を除き、`c.PNG`・`d.txt` だけにしたもの。(d) `<tmp>/tiles` が空のディレクトリ。(e) `<tmp>/none`（無いディレクトリ）。(f) `build_metadata` を、`tiles_dir` を (c) のものと (e) のものにして 2 回呼ぶ（`repo_dir` は正しい `<tmp>/repo`）。(g) (a) に、権限を `os.chmod(<tmp>/tiles/15/3, 0)` にしたディレクトリ `<tmp>/tiles/15/3` を足したもの（`os.geteuid() == 0` ならこのケースを飛ばす。後始末で `0o755` に戻す） | (a)〜(e)(g) `_tile_latest_date(<tiles_dir>)`、(f) `build_metadata` | (a) `('2025-10-09T08:53:20Z', None)`（最大の mtime は `b.png` で、秒より下は切り捨て。`.PNG`・`.txt` は見ない）。(b) `('2023-11-14T22:13:20Z', None)`。(c)(d) `('', 'PNG が 1 枚も無い')`。(e) `('', 'ディレクトリをたどれない: <tmp>/none: No such file or directory')`。(f) どちらも `items['gsi_tile_latest_date']` が `''`、`warnings` が 1 つめ `[('MT2', 'gsi_tile_latest_date を求められない: PNG が 1 枚も無い。空文字を書く')]`、2 つめ `[('MT2', 'gsi_tile_latest_date を求められない: ディレクトリをたどれない: <tmp>/none: No such file or directory。空文字を書く')]`（`MT1` は無い）。(g) `('', 'ディレクトリをたどれない: <tmp>/tiles/15/3: Permission denied')`（一部だけ読めないときも、読めた分の最大を返さない） |
| `UT-match_summits-57` | 版の文字列 | 同じプロセス。組み立ての入力（metadata）の `<tmp>/repo`（タグ付きの commit 1 つ）。環境は `patch.dict` の下。(a) そのまま。(b) もう 1 つ commit する。(c) (b) の後（commit が 2 つある状態）で、追跡している `f` を書き換える（commit しない）。(d) `<tmp>/ng`（リポジトリでない空のディレクトリ）。(e) `<tmp>/nodir`（無いディレクトリ）。(f) `unittest.mock.patch('match_summits.subprocess.run', ...)` で、`side_effect=FileNotFoundError(2, 'No such file or directory')`、`side_effect=subprocess.TimeoutExpired('git', 60)`、戻り値 `subprocess.CompletedProcess(['git'], 0, stdout='\n', stderr='')`、戻り値 `subprocess.CompletedProcess(['git'], 128, stdout='', stderr='')` の 4 通り。(g) `build_metadata` を `repo_dir` が (d) で、ほかは UT-55 (a) と同じ。(h) `build_metadata` を `tiles_dir` が UT-56 (e) の `<tmp>/none`、`repo_dir` が (e) の `<tmp>/nodir` で、ほかは UT-55 (a) と同じ（`MT1` と `MT2` が両方当たる） | (a)〜(f) `_software_version(<repo_dir>)`、(g)(h) `build_metadata` | (a) `('v0.1.0', None)`。(b) `('v0.1.0-1-g<7 桁以上の 16 進>', None)`（`re.fullmatch(r'v0\.1\.0-1-g[0-9a-f]{7,}', 値)`）。(c) 値が `re.fullmatch(r'v0\.1\.0-1-g[0-9a-f]{7,}-dirty', 値)` に合い、理由は `None`。(d) 値 `unknown`、理由は `git describe の終了コード 128: fatal: not a git repository` で始まる。(e) `('unknown', 'No such file or directory')`。(f) 順に `('unknown', 'No such file or directory')`、`('unknown', '60 秒で終わらない')`、`('unknown', 'git describe の出力が空')`、`('unknown', 'git describe の終了コード 128: ')`。(g) `items['software_version']` が `'unknown'`、`warnings` が 1 件で、記号が `'MT1'`、文が `software_version を求められない: git describe の終了コード 128: fatal: not a git repository` で始まり `。unknown を書く` で終わる。(h) `items['gsi_tile_latest_date']` が `''`、`items['software_version']` が `'unknown'`、`warnings` が 2 件でこの順（`MT1` が先、`MT2` が後。`items` の計算の順の逆）: `('MT1', 'software_version を求められない: No such file or directory。unknown を書く')`、`('MT2', 'gsi_tile_latest_date を求められない: ディレクトリをたどれない: <tmp>/none: No such file or directory。空文字を書く')` |
| `UT-match_summits-58` | JSON の書き方（`_encode_json`） | 同じプロセス | `_encode_json` に (a) `{'a': [1, 2.5, 0.0, True, None, 'é', cmp5_common.JsonNumber('1.50')]}`、(b) `(1, 'x')`（タプル）、(c) `True` と `1`、(d) `1234.6`・`1.0`、(e) `set()`、(f) `float('nan')`・`float('inf')` | (a) 次の 1 つの文字列（空白なし。`é` は字そのままでなく、バックスラッシュ・`u`・`0`・`0`・`e`・`9` の 6 文字で書く。出力は ASCII だけ）: `{"a":[1,2.5,0.0,true,null,"é",1.50]}`。(b) `[1,"x"]`。(c) `true` と `1`（`True` が `1` にならない）。(d) `1234.6`・`1.0`。(e) `TypeError`。(f) どちらも `ValueError` |
| `UT-match_summits-59` | フィーチャの並び | 同じプロセス。組み立ての入力（フィーチャと XLSX）。(a) 場面のまま。(b) (a) の `summits` の並びと `deletion.summit_status`・`deletion.dominant`・`deletion.unmatched` の並びを逆にしたもの（`peaks` の並びは変えない） | `build_summit_features(<peaks>, <zones>, <summits>, <activation>, <deletion>, <codes>, <regions>, <attrs>, <pending>, <metadata>)` | (a)(b) とも `features` が 39 件で、並び（`種類:summit_code`。`coord_diff` は `→終点のサミットの code` を添える）が次のとおり。`K1`: `peak:JA/HS-A00`・`key_col:JA/HS-A00`・`activation_zone:JA/HS-A00`・`delete_zone:JA/HS-A00`・`peak_col_link:JA/HS-A00`。`K2`（海面のコルなのでコルの点と線が無い）: `peak:JA/HS-A01`・`activation_zone:JA/HS-A01`・`delete_zone:JA/HS-A01`、続けて `code` の順に `summit:JA/HS-010`・`coord_diff:JA/HS-A01→JA/HS-010`・`summit:JA/HS-011`・`coord_diff:JA/HS-A01→JA/HS-011`。`K3`: `peak:JA/HS-003`・`key_col:JA/HS-003`・`activation_zone:JA/HS-003`・`delete_zone:JA/HS-003`・`peak_col_link:JA/HS-003`・`summit:JA/HS-003`・`coord_diff:JA/HS-003→JA/HS-003`・`summit:JA/HS-013`・`coord_diff:JA/HS-003→JA/HS-013`。`K4`（コルが未確定でコルの点と線が無い）: `peak:JA/HS-004`・`activation_zone:JA/HS-004`・`delete_zone:JA/HS-004`・`summit:JA/HS-004`・`coord_diff:JA/HS-004→JA/HS-004`。`unmatched` が `code` の順に `summit:JA/HS-031`・`summit:JA/HS-032`（受け取った順は `JA/HS-032`・`JA/HS-031`）。保留組（`K5` は `ambiguous` なので、ここまでに出ない）: `peak:`（空）・`key_col:`・`activation_zone:`・`delete_zone:`・`peak_col_link:`、`summit:JA/HS-005`・`coord_diff:→JA/HS-005`・`summit:JA/HS-006`・`coord_diff:→JA/HS-006`・`summit:JA/HS-020`・`coord_diff:→JA/HS-020`（AZ の中の登録の後に保留した削除の候補）。保留組の地形のフィーチャの `summit_code` は空文字。AZ と delete判定ゾーンのジオメトリは `zones` のものと `is` で同じ（形を変えない） |
| `UT-match_summits-60` | プロパティのキーの順と値 | 同じプロセス。UT-59 (a) の `features`（0 始まりの添字で指す。UT-59 の並びの順） | `features[i]['properties']` | **キーの順**（`list(properties)`）: `peak`（添字 0・5・12・21・28）は `feature_type`・`category`・`match_status`・`summit_code`・`summit_name`・`summit_name_jp`・`peak_elev`・`prominence`・`stability`・`key_col_resolved`・`points`・`is_band_change_candidate`・`rationale`・`analysis_count`・`expected_count`・`municipality`・`region_name` に続けて、共通の 10 個（`review_reason`・`review_group_id`・`review_decision`・`review_note`・`application_exclusion`・`exclusion_note`・`pending_applications`・`pending_match`・`pending_note`・`pending_return`）。`key_col`（1・13・29）は `feature_type`・`category`・`summit_code`・`col_elev`・`points`・`col_margin_px`・`municipality`・`region_name` と共通の 10 個。`summit`（8・10・17・19・24・26・27・33・35・37）は `feature_type`・`category`・`match_status`・`summit_code`・`summit_name`・`summit_name_jp`・`sota_alt_m`・`sota_points`・`rationale`・`municipality`・`region_name`・`dominant_peak_code`・`dominant_peak_dist_m` と共通の 10 個。`activation_zone`（2・6・14・22・30）は `feature_type`・`category`・`summit_code`・`area_complete`・`points` と共通の 10 個。`delete_zone`（3・7・15・23・31）は `feature_type`・`category`・`summit_code`・`area_complete` と共通の 10 個。`peak_col_link`（4・16・32）は `feature_type`・`category`・`summit_code` と共通の 10 個。`coord_diff`（9・11・18・20・25・34・36・38）は `feature_type`・`category`・`summit_code`・`match_status` と共通の 10 個。**値**（数は `cmp5_common.JsonNumber`、`==` で比べる）。添字 0（`new` のピーク）: `category` `'add'`、`match_status` `'new'`、`summit_code` `'JA/HS-A00'`、`summit_name`・`summit_name_jp` が `''`、`peak_elev` `JsonNumber('1000.60')`、`prominence` `JsonNumber('50.00')`、`stability` `'confirmed'`、`key_col_resolved` `True`、`points` `6`、`is_band_change_candidate` `None`、`rationale` `'R-add'`、`analysis_count` `JsonNumber('4')`、`expected_count` `None`、`municipality` `'廿日市市'`、`region_name` `'広島県'`。5（`dominant`）: `summit_code` `'JA/HS-A01'`、`stability` `'-'`、`expected_count` `JsonNumber('1')`、`rationale` `'R-add2'`。12（`band_change`）: `summit_name` `'Mt A3'`、`summit_name_jp` `'A3山'`、`points` `8`、`is_band_change_candidate` `True`、`rationale` `'R-change'`。21（`no_change`）: `prominence` `None`、`key_col_resolved` `False`、`points` `4`、`is_band_change_candidate` `False`、`rationale` `''`。28（`ambiguous`）: `category` `'review'`、`summit_code` `''`、`review_reason` `'multiple_summits_in_az'`、`review_group_id` `GID`。2（`K1` の `activation_zone`）: `area_complete` `True`。3（`K1` の `delete_zone`）: `area_complete` `True`。23（`K4` の `delete_zone`）: `area_complete` `False`（`delete_zone` の `area_complete` は `zones` の `ZoneFeature.area_complete` をそのまま写すので、`K4` だけが `False` で、ほかの 4 つは `True`）。13（`K3` のコル）: `col_elev` `JsonNumber('1100.00')`、`points` `8`、`col_margin_px` `JsonNumber('30')`、`municipality` `'大竹市'`（コル自身の所在地）。17（`matched` のサミット）: `sota_alt_m` `JsonNumber('1000')`、`sota_points` `6`、`dominant_peak_code` `None`、`dominant_peak_dist_m` `None`、`municipality` `'大竹市'`（サミット自身の所在地。親のピーク `K3` の `'廿日市市'` ではない）、`region_name` `'広島県'`。8（`JA/HS-010`）: `category` `'delete'`、`sota_alt_m` `JsonNumber('200')`、`dominant_peak_code` `'JA/HS-A01'`、`dominant_peak_dist_m` `20.0`。37（保留した削除の候補）: `category` `'review'`、`review_reason` `'ambiguous_parent'`、`review_group_id` `GID`、`dominant_peak_code` `''`、`dominant_peak_dist_m` `55.5`。26（`JA/HS-031`）: `municipality`・`region_name` が `''`（`region` が `None`）、`review_reason` `'unmatched'`。33（`JA/HS-005`）: `municipality` `'大竹市'`（サミット自身の所在地。親のピーク `K5` の `'廿日市市'` ではない）、`region_name` `'広島県'`。`coord_diff`: 9 は `category` `'delete'`・`summit_code` `'JA/HS-A01'`・`match_status` `'dominant'`・`review_reason` `''`・`review_group_id` `''`、18 は `'band_change'`・`'JA/HS-003'`・`'matched'`、20 は `'delete'`・`'JA/HS-003'`・`'matched'`・`review_reason` `''`、34 は `'review'`・`''`・`'ambiguous'`・`'multiple_summits_in_az'`・`GID`、38 は `'review'`・`''`・`'ambiguous'`・`'ambiguous_parent'`・`GID`。全フィーチャで `review_decision`・`review_note`・`application_exclusion`・`exclusion_note` が `''`、`pending_return` が `False`。`area_complete` は添字 23 だけ `False`、ほかのゾーンは `True` |
| `UT-match_summits-61` | 申請済みの属性の写し先 | 同じプロセス。UT-59 (a) の `features` | `features[i]['properties']` の `pending_applications`・`pending_match`・`pending_note` | `('peak', K1)` の行: 添字 0〜4 が `pending_applications` が `[<add の申請>]`、`pending_match` `'same'`、`pending_note` `'追加 2026-10-04（2026年の表）'`。`('peak', K3)` の行: 添字 12〜18（ピークの点・コル・AZ・delete判定ゾーン・線と、AZ の中のサミットの点 17 とそれへの `coord_diff` 18）が `[<change の申請>]`・`'same'`・`'変更 2026-10-01（2026年の表）'`。`('summit', 'JA/HS-013')` の行: 添字 19（削除のサミットの点）と 20（`K3` からそれへの `coord_diff`）が `[<delete の申請>]`・`'same'`・`'削除 2026-10-03（2025年の表）'`。`unmatched` の `JA/HS-031`（添字 26）: `[<held の申請>]`（`match` が `'held'`）、`pending_match` `''`、`pending_note` `'削除 2026-10-02（2026・2025年の表）'`（`pending_match` が空文字でも `pending_applications` は空でない）。ほかは `[]`・`''`・`''`: 添字 5〜11（`K2` と、その点・線と `delete` のサミット 2 件）、21〜25（`K4`）、27（`JA/HS-032`）、保留組の 28〜38。`pending_applications` は `list`（`PendingRow.applications` のタプルでなく、その要素を並べたリストで、要素は同じ `dict`） |
| `UT-match_summits-62` | 数の字句と `text` の形 | 同じプロセス。組み立ての入力（フィーチャと XLSX）。(a) 場面のまま。(b) (a) の `K1` の行を `prow(2, '35.10000000', '138.10000000', '1000.60', '50.00', 'true', '35.00000000', '138.00000000', '950.40', '+0120', 'confirmed', '+12', '')` にしたもの（`col_margin_px` と `analysis_count` に先頭の `+` と余分な `0`）。(c) `peaks` から `activation`・`deletion` まで、すべてが空の入力（`peaks` が `{}`、`zones` が `{}`、`summits` が `[]`、`ActivationMatch({}, {}, {}, [])`、`DeleteMatch({}, {}, {}, [])`、`codes` が `{}`、`RegionMatch({}, [])`、`Attributes({}, {}, [], NullPoints((), (), ()))`、`Pending({}, [], 0)`）で `metadata` が `{'a': 1}` | `build_summit_features` に (a)(b)(c) | (a) 添字 8（`JA/HS-010`）の点の `geometry['coordinates']` が `[JsonNumber('138.2200'), JsonNumber('35.2200')]`（入力は `138.2200`・`+35.2200`）、`sota_alt_m` が `JsonNumber('200')`（入力は `0200`）。ピークの点（添字 0）の座標は `[JsonNumber('138.10000000'), JsonNumber('35.10000000')]`、`peak_elev` は `JsonNumber('1000.60')`（そのまま。10 進の値も末尾の `0` も変えない）。(b) 添字 1 の `col_margin_px` が `JsonNumber('120')`、添字 0 の `analysis_count` が `JsonNumber('12')`。(c) `features` が `[]`、`text` が `'{"type":"FeatureCollection","metadata":{"a":1},"features":[\n]}\n'`。(a) の `text` は、`'\n'` で分けた最後の空を除いて 41 行で、1 行目が `{"type":"FeatureCollection","metadata":{"summitslist_date":"2026-10-18","n":1},"features":[`、最後の行が `]}`、2 行目から 40 行目が Feature を 1 行に 1 つ（最後の Feature の行だけ行末の `,` が無い）、`text` の末尾が LF で、CR・BOM が無く、`text.isascii()` が真、`json.loads(text)` が読めて `features` が 39 件。`text` に `"peak_elev":1000.60`・`"points":6`・`"dominant_peak_dist_m":20.0`・`"dominant_peak_dist_m":1234.6`・`"dominant_peak_dist_m":0.0`・`"expected_count":null`・`"key_col_resolved":true`・`"municipality":"\u5eff\u65e5\u5e02\u5e02"`（`_encode_json` は ASCII の外の字を `\uXXXX`〈16 進は小文字〉で書くので、`廿日市市` の字そのものは含まれない）が含まれる |
| `UT-match_summits-63` | XLSX の行の並びと全 37 列の値 | 同じプロセス。組み立ての入力（フィーチャと XLSX）。UT-59 (a) の `features`（`build_summit_features` の返り値）を `build_summit_sheets` に渡し、返った `Workbook` のシート「サミット一覧」を `ws` とする。値はセルの `value` を比べる（`JsonNumber` 由来の数のセルは `decimal.Decimal` で、`==` で比べる。`int`・`float` 由来の数のセル〈`points`・`sota_points`・`dominant_peak_dist_m`〉は、そのまま `int`・`float` で比べる） | `ws` の 1 行目と 2〜13 行目 | 1 行目は `_SHEET_COLUMNS` の 37 列の見出しの順。`ws.max_row` は 13。行の並び（`summit_code`）は 2〜13 行目が `JA/HS-A00`・`JA/HS-A01`・`JA/HS-010`・`JA/HS-011`・`JA/HS-003`・`JA/HS-013`・`JA/HS-004`・`JA/HS-031`・`JA/HS-032`・`JA/HS-005`・`JA/HS-006`・`JA/HS-020`（ピークの行の後にそのピークを主ピークとする削除の行、`unmatched`、保留組〈AZ の中の登録の後に保留した削除の候補〉）。各行のセルが入る列は次のとおりで、書いていない列は空（セルが無い）。全行に `pending_return='false'` がある。「所在地」は `municipality='廿日市市'` と `region_name='広島県'` の 2 列（`JA/HS-005` の行だけ `municipality='大竹市'`。この行の所在地は行を生むサミット自身の値で、親のピークの値ではない。ピークの行の所在地は、結んだサミットの値でなくピーク自身の値）。2 行目（ピークの点の行・`new`）: `category='add'`・`match_status='new'`・`pending_match='same'`・`pending_note='追加 2026-10-04（2026年の表）'`・`stability='confirmed'`・`summit_code='JA/HS-A00'`・`peak_lat=35.10000000`・`peak_lon=138.10000000`・`peak_elev=1000.60`・`points=6`・`col_lat=35.00000000`・`col_lon=138.00000000`・`col_elev=950.40`・`prominence=50.00`・`key_col_resolved='true'`・`col_margin_px=120`・`analysis_count=4`・所在地・`area_complete='true'`。3 行目（`dominant`。海面のコルなのでコルの列が空）: `category='add'`・`match_status='dominant'`・`stability='-'`・`summit_code='JA/HS-A01'`・`peak_lat=35.20000000`・`peak_lon=138.20000000`・`peak_elev=900.00`・`points=6`・`prominence=60.00`・`key_col_resolved='true'`・`analysis_count=1`・`expected_count=1`・所在地・`area_complete='true'`。4 行目（通常の削除の行。ピークとコルの列が空）: `category='delete'`・`match_status='delete'`・`summit_code='JA/HS-010'`・`summit_name='Mt D2'`・`sota_lat=35.2200`・`sota_lon=138.2200`・`sota_alt_m=200`・`sota_points=2`・所在地・`dominant_peak_code='JA/HS-A01'`・`dominant_peak_dist_m=20.0`。5 行目: 同じ形で `summit_code='JA/HS-011'`・`summit_name='Mt D1'`・`summit_name_jp='D1山'`・`sota_lat=35.2100`・`sota_lon=138.2100`・`sota_alt_m=100`・`sota_points=1`・`dominant_peak_dist_m=1234.6`。6 行目（`band_change`）: `category='band_change'`・`match_status='matched'`・`pending_match='same'`・`pending_note='変更 2026-10-01（2026年の表）'`・`stability='unstable'`・`summit_code='JA/HS-003'`・`summit_name='Mt A3'`・`summit_name_jp='A3山'`・`peak_lat=35.30000000`・`peak_lon=138.30000000`・`peak_elev=1200.50`・`points=8`・`col_lat=35.20000000`・`col_lon=138.20000000`・`col_elev=1100.00`・`prominence=70.00`・`key_col_resolved='true'`・`col_margin_px=30`・`analysis_count=2`・`expected_count=2`・`sota_lat=35.3100`・`sota_lon=138.3100`・`sota_alt_m=1000`・`sota_points=6`・`is_band_change_candidate='true'`・所在地・`area_complete='true'`。7 行目: `category='delete'`・`match_status='delete'`・`pending_match='same'`・`pending_note='削除 2026-10-03（2025年の表）'`・`summit_code='JA/HS-013'`・`summit_name='Mt D3'`・`sota_lat=35.3200`・`sota_lon=138.3200`・`sota_alt_m=300`・`sota_points=4`・所在地・`dominant_peak_code='JA/HS-003'`・`dominant_peak_dist_m=0.0`（0.0 も数のセルが置かれる）。8 行目（`no_change`。コルが未確定でコルの列と `prominence` が空）: `category='no_change'`・`match_status='matched'`・`stability='unstable'`・`summit_code='JA/HS-004'`・`summit_name='Mt A4'`・`summit_name_jp='A4山'`・`peak_lat=35.40000000`・`peak_lon=138.40000000`・`peak_elev=700.00`・`points=4`・`key_col_resolved='false'`・`analysis_count=3`・`expected_count=3`・`sota_lat=35.4100`・`sota_lon=138.4100`・`sota_alt_m=650`・`sota_points=4`・`is_band_change_candidate='false'`・所在地・`area_complete='true'`。9 行目（`unmatched`。`pending_match` は空文字なのでセルが無く、`pending_note` はある。所在地が空文字）: `category='review'`・`match_status='unmatched'`・`review_reason='unmatched'`・`pending_note='削除 2026-10-02（2026・2025年の表）'`・`summit_code='JA/HS-031'`・`summit_name='Mt U2'`・`sota_lat=35.7100`・`sota_lon=138.7100`・`sota_alt_m=500`・`sota_points=2`。10 行目: `category='review'`・`match_status='unmatched'`・`review_reason='unmatched'`・`summit_code='JA/HS-032'`・`summit_name='Mt U1'`・`sota_lat=35.7000`・`sota_lon=138.7000`・`sota_alt_m=120`・`sota_points=1`・所在地。11 行目（`ambiguous` の行。ピークとコルを反復）: `category='review'`・`match_status='ambiguous'`・`review_reason='multiple_summits_in_az'`・`review_group_id=GID`・`stability='confirmed'`・`summit_code='JA/HS-005'`・`summit_name='Mt A5'`・`peak_lat=35.50000000`・`peak_lon=138.50000000`・`peak_elev=1300.00`・`points=10`・`col_lat=35.30000000`・`col_lon=138.30000000`・`col_elev=1250.00`・`prominence=80.00`・`key_col_resolved='true'`・`col_margin_px=40`・`analysis_count=5`・`expected_count=5`・`sota_lat=35.5100`・`sota_lon=138.5100`・`sota_alt_m=800`・`sota_points=6`・`municipality='大竹市'`・`region_name='広島県'`・`area_complete='true'`（`is_band_change_candidate` は空）。12 行目: 11 行目と同じで `summit_code='JA/HS-006'`・`summit_name='Mt A6'`・`sota_lat=35.5200`・`sota_lon=138.5200`・`sota_alt_m=900`（所在地は `JA/HS-006` 自身の `municipality='廿日市市'`・`region_name='広島県'`）。13 行目（保留した削除の候補。`dominant_peak_code` が空文字でセルが無く、距離はある）: `category='review'`・`match_status='delete'`・`review_reason='ambiguous_parent'`・`review_group_id=GID`・`summit_code='JA/HS-020'`・`summit_name='Mt H1'`・`sota_lat=35.6000`・`sota_lon=138.6000`・`sota_alt_m=400`・`sota_points=1`・所在地・`dominant_peak_dist_m=55.5` |
| `UT-match_summits-64` | セルの型・表示形式・シート | 同じプロセス。UT-63 の `Workbook` を `save(io.BytesIO())` して `openpyxl.load_workbook` で読み直したもの（読み直したシートを `ws2`、`zipfile.ZipFile` で開いた `xl/worksheets/sheet1.xml` を `xml`）。見出しの列の位置は 1 行目の名前で引く。(f) だけ、`build_summit_sheets([])` | (a)〜(f) | (a) 空の値の列にセルを置かない: `xml` に 2 行目の `expected_count`（27 列目の `AA2`）の `<c r="AA2"` が無く、2 行目の `category`（`A2`）の `<c r="A2"` がある。`ws2` の 2〜13 行目の値が `None` でないセルの数が 221。(b) 表示形式: 2 行目の `peak_lat`・`peak_lon`・`col_lat`・`col_lon` が `0.00000000`、`peak_elev`・`col_elev`・`prominence` が `0.00`、`points`・`col_margin_px`・`analysis_count` が `General`（数のセルで `data_type` が `n`）。5 行目の `dominant_peak_dist_m` が `0.0` で値が 1234.6、`sota_lat` が `General`。(c) 真偽は文字列: 2 行目の `key_col_resolved`・`area_complete` が `'true'`（`data_type` が `s`）、8 行目の `key_col_resolved`・`is_band_change_candidate` が `'false'`、6 行目の `is_band_change_candidate` が `'true'`、全行の `pending_return` が `'false'`（数のセル 1・0 でない）。(d) 式にならない文字列: `features` のうち `JA/HS-010` のサミットの点の `summit_name` を `'=1+1'` にして作り直した `Workbook` の 4 行目の `summit_name` セルが、値 `'=1+1'`・`data_type` が `'s'`（保存して読み直しても `'s'`）。(e) シート: `wb.sheetnames` が `['サミット一覧', '出典']`、「出典」の `A1` が `地理院タイル（標高タイル）を加工して作成。出典: 国土地理院 (https://maps.gsi.go.jp/development/ichiran.html)`、「サミット一覧」の 1 行目が `_SHEET_COLUMNS` と同じ 37 個の文字列。(f) `wb.sheetnames` が `['サミット一覧', '出典']`、「サミット一覧」の `max_row` が 1（見出しだけ）、「出典」の `A1` が (e) と同じ |
| `UT-match_summits-65` | 結べない行は XS1 で止まる | 同じプロセス。UT-59 (a) の `features` を `copy.deepcopy` して直したものを `build_summit_sheets` に渡す。(a) `JA/HS-A00` の `activation_zone` を除く。(b) `JA/HS-A00` の `key_col` を 1 つ複製して 2 つにする。(c) `JA/HS-A01` の `peak` の点の `prominence` のキーを消す。(d) (a)(b)(c) に加えて、`review_group_id` が `GID` の `activation_zone` を除く（保留組の AZ が 0 個）。(e) `JA/HS-004` の `matched` のサミットの点を除く。(f) (a) に加えて `JA/HS-010` のサミットの点の `summit_name` を `'a\x01b'` にする（XS1 と XS2 の両方） | `build_summit_sheets` に (a)〜(f)（`assertRaises(SystemExit)` と標準エラー出力） | どれも終了コード 1 で、2 行目は `対処: プログラムの欠陥として起票して調べる。このメッセージを添える`。1 行目は `ERROR: XLSX の行を結べないか、取り元のプロパティが無い:` に空白 1 つを挟んで、(a)(f) `peak 35.10000000,138.10000000: activation_zone が 0 個`、(b) `peak 35.10000000,138.10000000: key_col が 2 個`、(c) `peak 35.20000000,138.20000000: peak のプロパティ prominence が無い`、(d) `peak 35.10000000,138.10000000: key_col が 2 個、activation_zone が 0 個；peak 35.20000000,138.20000000: peak のプロパティ prominence が無い；summit JA/HS-005: activation_zone が 0 個；summit JA/HS-006: activation_zone が 0 個`（当たった点すべてを、行を生む点の順に `；` でつなぐ。(d) の 4 つの点は省かれない。同じ点の中は結べなかった相手が先）、(e) `peak 35.40000000,138.40000000: summit が 0 個`。(f) は XS2 でなく XS1 だけ（XS2 の `JA/HS-010` は出ない） |
| `UT-match_summits-66` | 書けない文字列は XS2 で止まる | 同じプロセス。UT-59 (a) の `features` を `copy.deepcopy` して直したものを `build_summit_sheets` に渡す。(a) `JA/HS-010` のサミットの点の `summit_name` を `'a\x01b'`、`JA/HS-013` のサミットの点の `summit_name_jp` を `'x' * 32768` にする。(b) (a) の `JA/HS-013` の `summit_name_jp` を `'x' * 32767` にし、`JA/HS-010` の `summit_name` を元に戻す。(c) `JA/HS-010` の `summit_name` を `'a\x01b'`、`summit_name_jp` を `'\x02'` にし、`JA/HS-A00` のピークの点の `stability` を `'\x0b'`、`rationale` を `'a\nb\t'`（改行とタブは書ける）にする。(d) `JA/HS-A00` のピークの点の `summit_name` を `'=1+1'`、`JA/HS-010` の `summit_name` を `'\n'` で始まる文字列にする | `build_summit_sheets` に (a)〜(d) | (a) 終了コード 1。1 行目は `ERROR: XLSX に値を変えずに書けない文字列がある: summit JA/HS-010: summit_name（書けない制御文字を含む）；summit JA/HS-013: summit_name_jp（32767 字を超える）`、2 行目は `対処: 入力のファイルの該当の値を直して、scripts/run_pipeline.sh --phase 4 を起動し直す`。(b) 止まらず、保存して読み直した 7 行目の `summit_name_jp` の長さが 32767。(c) 終了コード 1 で、1 行目は `... : peak 35.10000000,138.10000000: stability（書けない制御文字を含む）；summit JA/HS-010: summit_name（書けない制御文字を含む）、summit_name_jp（書けない制御文字を含む）；summit JA/HS-013: summit_name_jp（32767 字を超える）`（`JA/HS-013` は (a) のまま。当たった点と列がすべて、行を生む点の順、同じ点の中は列の順）。`rationale` の改行とタブは当たらない。(d) 止まらず、`JA/HS-A00` の行の `summit_name` が `'=1+1'`（`data_type` が `'s'`）、`JA/HS-010` の行の `summit_name` が先頭の改行を持つ文字列のまま |
| `UT-match_summits-67` | 結ぶ鍵の扱い | 同じプロセス。UT-59 (a) の `features` を `copy.deepcopy` して直したものを `build_summit_sheets` に渡す。(a) `JA/HS-A00` のピークの点の `summit_code` を空文字にする（保留組の `activation_zone` が `summit_code` 空文字なので、結ばれてはならない）。(b) `JA/HS-005` のサミットの点の `review_group_id` のキーを消す。(c) `JA/HS-003` のピークの点の `summit_code` のキーを消す。(d) 末尾に、`properties` が無い Feature と、`properties` が `{'summit_code': 'JA/HS-A00'}` だけ（`feature_type` が無い）の Feature を足す | (a)〜(d) | (a) 終了コード 1 で XS1。`peak 35.10000000,138.10000000: activation_zone が 0 個`（保留組の AZ に結ばれず、`KeyError` や誤った結び付きにならない。`key_col` は 0 個でよい）。(b) XS1。`summit JA/HS-005: peak が 0 個、activation_zone が 0 個、summit のプロパティ review_group_id が無い`。(c) XS1。`peak 35.30000000,138.30000000: activation_zone が 0 個、summit が 0 個、peak のプロパティ summit_code が無い`。(d) 止まらず、行の数と値は UT-63 と同じ（`properties` や `feature_type` の無い Feature は、行を生む点にも索引にも入らず、`KeyError` にならない） |
| `UT-match_summits-68` | 引数の正しい形 | 同じプロセス | `_parse_args` に (a) `['--config', '/a.ini']`、(b) `['--config', '/a b.ini']` | (a) `_Args('/a.ini')`、(b) `_Args('/a b.ini')`（値は正規化しない） |
| `UT-match_summits-69` | 引数の誤り（`start_log` の前で止まる） | 子のプロセス。`<引数>` を (a)〜(j) のとおりに書く（`['--config', '<tmp>/c.ini']` を足さない） | (a) `[]`、(b) `['--config']`、(c) `['--config', 'a.ini']`、(d) `['--config', '/a', '--config', '/b']`、(e) `['--config', '/a', '--mesh', '5338']`、(f) `['--config=/a']`、(g) `['--config', '']`、(h) `['x']`、(i) `['--config', '/a', '--help']`、(j) `['--config', '/a', '']` | どれも終了コード 2、標準出力は空、標準エラー出力は 2 行、`<tmp>/logs` を作らない。(a) SA4（`ERROR: --config が無い`）。(b) SA2（`--config の値が無い`）。(c) SA5（`--config のパスが絶対パスでない: a.ini`）。(d) SA3（`--config を 2 回渡した`）。(e) SA1（`match_summits の知らない引数: --mesh`）。(f) SA1（`--config=/a`）。(g) SA5（`--config のパスが絶対パスでない: ''`）。(h) SA1（`x`）。(i) SA1（`--help`）。(j) SA1（`''`）。2 行目は SA1 が `対処: match_summits は run_pipeline が起動する内部の起動口。使える名前は --config（値は次の引数で渡す）`、SA2 が `対処: --config の後に値を渡す`、SA3 が `対処: --config は 1 回だけ渡す`、SA4 が `対処: --config と設定ファイルの絶対パスを渡す`、SA5 が `対処: --config に設定ファイルの絶対パスを渡す` |
| `UT-match_summits-70` | 起動の場面の全体（警告の順、出力、要約） | 子のプロセス。起動の場面のまま | `<引数>` が `['--config', '<tmp>/c.ini']` | 終了コード 0。標準エラー出力の警告の 1 行目の記号の並びが UM1 → RG1（`K2`）→ RG1（S2）→ SN1 → UN1 → MT1 → MT2（[main](#mainmatch_summits)の「警告を出す時機と順」）で、他の警告は出ない。UM1 は `WARNING: unmatched のサミットがある（1 件）: JA/HS-002（S2、35.45,138.95）`。RG1 は `WARNING: 地域か市区町村のどれにも入らない点: ピーク 35.36058364,138.77030611: 入らなかった層 地域・市区町村: match_status new、仮サミットコード ZZ/ZZ-A00` と `WARNING: 地域か市区町村のどれにも入らない点: サミット 35.45,138.95: 入らなかった層 地域・市区町村: サミット JA/HS-002`（`K1`・`K1` のコル・S1 は入るので出ない）。SN1 は `WARNING: SOTA 既存サミット GeoJSON を使わない: 設定の sota_geojson_version が未設定。すべてのサミットの summit_name_jp が空文字になる`。UN1 は `WARNING: 登録変更リストの知らせる行: unreadable_row: 追加の位置が 緯度,経度 の形で読めない: 2026 年の表の 1 行目、アクション 追加、山岳 ID か県名 県、申請者 A、申請日 2026-01-01、問題の値 abc（全体で 1 件）`。MT1 の 1 行目は `WARNING: software_version を求められない:` で始まる。MT2 は `WARNING: gsi_tile_latest_date を求められない: ディレクトリをたどれない: <tmp>/data/tiles: No such file or directory。空文字を書く`。`<tmp>/data/results/` に `merged_summit.geojson` と `merged_summit.xlsx` があり、`.tmp` で終わる名前が無い。`merged_summit.geojson` は、`"generated_at":"…"` の引用符の中を `T` に置き換えた全文が、1 行目は `{"type":"FeatureCollection","metadata":{"summitslist_date":"2026-10-18","generated_at":"T","updatelist_file":"sota_updatelist_2026.xhtml","updatelist_updates":[{"year":2026,"update":"2026-10-14"}],` に続けて、`updatelist_notices` が UN1 と同じ知らせる行 1 件（`{"kind":"unreadable_row","reason":…,"year":2026,"row":1,"action":…,"target":…,"applicant":"A","applied_on":"2026-01-01","value":"abc"}`。日本語は `\uXXXX` の ASCII）、`gsi_tile_latest_date` が空文字、`attribution`・`source_url`・`license_url`（[7.5.2](#752-型とデータ)の `_ATTRIBUTION`・`_SOURCE_URL`・`_LICENSE_URL`）、`software_version` が `unknown` の順で、行末が `},"features":[`、続く 11 個の Feature の行（`feature_type`・`category`・`summit_code` の並びと、`peak`・`summit`・`coord_diff` が持つ `match_status`（ほかの `feature_type` は持たない）が、`peak`・`add`・`ZZ/ZZ-A00`・`new`、`activation_zone`・`add`・`ZZ/ZZ-A00`、`delete_zone`・`add`・`ZZ/ZZ-A00`、`peak`・`no_change`・`JA/HS-001`・`matched`、`key_col`・`no_change`・`JA/HS-001`、`activation_zone`・`no_change`・`JA/HS-001`、`delete_zone`・`no_change`・`JA/HS-001`、`peak_col_link`・`no_change`・`JA/HS-001`、`summit`・`no_change`・`JA/HS-001`・`matched`、`coord_diff`・`no_change`・`JA/HS-001`・`matched`、`summit`・`review`・`JA/HS-002`・`unmatched`）、最後の行 `]}` の 13 行で、どの行も LF で終わる（LF は 13 個で、最後の LF の後は空）。UTF-8 のバイト数が 7077 で、SHA-256 が `f470a019d37d0c96e9dd0fa44fdeda67196861f80cdab47629209a012e058ce3`。S1 の `summit` の `match_status` が `matched` のまま（`delete` にならない。`match_delete_zones` に AZ の中のサミットを渡していない確かめ）。`merged_summit.xlsx` を `openpyxl.load_workbook` で開くとシートの名前が `サミット一覧`・`出典` で、`サミット一覧` の行が見出しを含めて 4。ログファイルは `<tmp>/logs/` に 1 つで、最後から 4〜2 行目が（先頭の時刻と空白を除いて）SM1 `結果の要約: ピーク 2 件（matched 1・ambiguous 0・dominant 0・new 1）、現役のサミット 2 件（matched 1・ambiguous 0・delete 0・unmatched 1。廃止済みとして除いた 0 件）`、SM2 `結果の要約: 仮サミットコードの数（エリアごと）: ZZ/ZZ 1 件`（`matched` の `K1` に仮サミットコードを付けていない）、SM3 `結果の要約: 登録変更リスト sota_updatelist_2026.xhtml、申請の行 2 件、取り込んだ申請 1 件、pending_match が same の候補 0 件・different の候補 0 件、知らせる行 1 件`、最後の行が `終了:` で始まる |
| `UT-match_summits-71` | 地域か市区町村の GeoJSON が無い（BN1・BN2、RG1 の層） | 子のプロセス。起動の場面から、(a) `boundaries/regions.geojson` を置かない、(b) `boundaries/municipalities.geojson` を置かない | `<引数>` が `['--config', '<tmp>/c.ini']` | どちらも終了コード 0。(a) 標準エラー出力の先頭が BN1（1 行目 `WARNING: 地域の GeoJSON が無い: <tmp>/data/boundaries/regions.geojson。仮サミットコードのエリアがすべて ZZ になり、region_name が空文字になる（全国の実行では仮サミットコードの連番上限で止まりうる）`、2 行目は `対処: {cmp1_rebuild}`）。続く警告は UT-70 と同じ UM1 → RG1 2 組 → SN1 → UN1 → MT1 → MT2 で、RG1 の `入らなかった層` は `市区町村` だけ（地域の層は照合しないので入れない。BN1 が 1 つにまとめる）。(b) 先頭が BN2（`WARNING: 市区町村の GeoJSON が無い: <tmp>/data/boundaries/municipalities.geojson。municipality が空文字になる`）。RG1 の `入らなかった層` は `地域` だけ。どちらも `merged_summit.geojson` と `merged_summit.xlsx` を書く。SM2 は `結果の要約: 仮サミットコードの数（エリアごと）: ZZ/ZZ 1 件` |
| `UT-match_summits-72` | 不備ゲート（書いてから終了コード 4。同数は当たらない） | 子のプロセス。起動の場面から、(a) `c.ini` に `[match]` の `unmatched_summit_threshold = 0`、(b) `unmatched_summit_threshold = 1`、(c) `merged_peak.geojson` の 2 つ目の Feature（`K2` の delete判定ゾーン）の `area_complete` を `false` にして、設定は既定 | `<引数>` が `['--config', '<tmp>/c.ini']` | (a) 終了コード 4。`merged_summit.geojson` と `merged_summit.xlsx` がある。標準エラー出力の最後の 2 行が GT1 で、1 行目は `ERROR: 不備ゲートに当たった: unmatched_over_threshold 1 件（unmatched_summit_threshold=0、確かめる列 match_status）`、2 行目は `対処: merged_summit.geojson と merged_summit.xlsx は調査用に書いた。merged_summit.xlsx の確かめる列を見て原因を調べ、直してから、scripts/run_pipeline.sh --phase 4 --config <tmp>/c.ini を起動し直す`。ログの要約は SM1〜SM3（終えた形）で、最後の行は `終了: 終了コード 4` で始まる。(b) 終了コード 0（`unmatched` の 1 件はしきい値と同じで、当たらない）。GT1 を出さない。(c) 終了コード 4。GT1 の 1 行目は `ERROR: 不備ゲートに当たった: is_area_incomplete 1 件（確かめる列 area_complete）`、2 行目は `対処: merged_summit.geojson と merged_summit.xlsx は調査用に書いた。merged_summit.xlsx の確かめる列を見て、merged_summit.geojson の activation_zone と delete_zone の area_complete=false も見て原因を調べ、直してから、scripts/run_pipeline.sh --phase 4 --config <tmp>/c.ini を起動し直す`。出力を書いてある。`merged_summit.geojson` の `delete_zone` の Feature に `area_complete` が `false` のものがあり、`merged_summit.xlsx` の `area_complete` 列はすべて `true`（delete判定ゾーンだけが不完結のため。GT1 の案内に GeoJSON を足した理由の確かめ） |
| `UT-match_summits-73` | 入力の誤りは書かずに止まる | 子のプロセス。起動の場面から、(a) `results/merged_peak.csv` を置かない、(b) `ref/summitslist.csv` を置かない | `<引数>` が `['--config', '<tmp>/c.ini']` | どちらも終了コード 1、`merged_summit.geojson`・`merged_summit.xlsx`・`.tmp` が無い。(a) 標準エラー出力の 2 行は `ERROR: merged_peak.csv が無い: <tmp>/data/results/merged_peak.csv` と `対処: scripts/run_pipeline.sh --config <tmp>/c.ini を --phase なしで起動して、フェーズ2 から通しでやり直す`（`{redo}`）。ログの要約は SM4 の 1 行で、`結果の要約: 途中で止まった（まだ数えたものが無い）。merged_summit.geojson と merged_summit.xlsx はそろえて置いていない`（ピークの数を書かない）。(b) SS1（`ERROR: SOTA サミットリスト CSV が無い: <tmp>/data/ref/summitslist.csv`、2 行目は `対処: {summits_advice}`）。SM4 は `結果の要約: 途中で止まった（ピーク 2 件）。merged_summit.geojson と merged_summit.xlsx はそろえて置いていない`（途中までの材料のピークの数が入る） |
| `UT-match_summits-74` | 途中までの材料（登録変更リストが無い） | 子のプロセス。起動の場面から `ref/sota_updatelist_2026.xhtml` を置かない（`summitslist.csv` は正しい） | `<引数>` が `['--config', '<tmp>/c.ini']` | 終了コード 1、UX1（`ERROR: 登録変更リストが無い: <tmp>/data/ref（ファイル名が sota_updatelist_<4 桁の年>.xhtml の形のもの）`）。SM4 は `結果の要約: 途中で止まった（ピーク 2 件、現役のサミット 2 件（廃止済みとして除いた 0 件））。merged_summit.geojson と merged_summit.xlsx はそろえて置いていない`（登録変更リストの数は入らない） |
| `UT-match_summits-75` | 書き込みの失敗（子のプロセス） | 子のプロセス。起動の場面で、`<tmp>/data/results/merged_summit.geojson` という名前のディレクトリを先に作る | `<引数>` が `['--config', '<tmp>/c.ini']` | 終了コード 1。標準エラー出力の最後の 2 行が SW1 で、1 行目は `ERROR: merged_summit.geojson か merged_summit.xlsx を書けない: <tmp>/data/results/merged_summit.geojson: Is a directory。2 つの出力はどちらも置いていない`、2 行目は `対処: <tmp>/data/results の空きと権限を確かめてから、scripts/run_pipeline.sh --phase 4 --config <tmp>/c.ini を起動し直す`。`<tmp>/data/results/` に `merged_summit.xlsx` が無い（置いた後に消した）。`.tmp` で終わる名前が無い。ログの要約は SM4 の 1 行で、`結果の要約: 途中で止まった（ピーク 2 件、現役のサミット 2 件（廃止済みとして除いた 0 件）、登録変更リスト sota_updatelist_2026.xhtml、申請の行 2 件、仮サミットコードの数（エリアごと）: ZZ/ZZ 1 件、peak.match_status は matched 1・ambiguous 0・dominant 0・new 1、summit.match_status は matched 1・ambiguous 0・delete 0・unmatched 1、取り込んだ申請 1 件、pending_match が same の候補 0 件・different の候補 0 件、知らせる行 1 件）。merged_summit.geojson と merged_summit.xlsx はそろえて置いていない`（`written` が偽なので `そろえて置いていない`。終えた材料がすべて入る） |
| `UT-match_summits-76` | 取り込んだ申請の数（`Pending.taken`） | 同じプロセス。申請の入力。(a) 申請は 12 件で、`row` を 1〜12 にして順に、`ap('add', lat='35.05', lon='138.05')`（`AZ_1` だけ。当たる）、`ap('add', lat='40.0', lon='140.0')`（どこにも入らず `unmatched_add`）、`ap('add', lat='36.10', lon='139.10')`（`AZ_3`。`K4` は `matched` で、当てず知らせない）、`ap('change', 'JA/AB-002', new_elev='1300.99')`（6 pt → 8 pt。バンドをまたぐ）、`ap('change', 'JA/AB-002', new_elev='950')`（同じバンド）、`ap('change', 'JA/AB-002', new_elev='149.99')`（算出表に無い）、`ap('delete', 'JA/ZZ-777')`（廃止済み）、`ap('delete', 'JA/XX-999')`（`unknown_id`）、`ap('delete', 'JA5/MM-001')`（`ambiguous_region`）、`ap('delete', 'JA/CD-001')`（`delete`）、`ap('delete', 'JA/AB-030')`（`matched` の `no_change` で、当てない）、`ap('delete', 'JA5/KC-027')`（地域コードと番号が現役の `JA/KC-027` と一致。`unmatched` で `held`）。(b) 申請は `ap('delete', 'JA/CD-001', years=(2026, 2025))` の 1 件（複数の年の表に載る 1 つの申請）。(c) 申請が 0 件 | `match_summits.match_pending_applications` に (a)(b)(c) をそれぞれ別の呼び出しで | `taken` が (a) 7（1・2・3・4・10・11・12 件目を数え、5〜9 件目は数えない）、(b) 1（`UpdateList.applications` の 1 件を 1 と数える）、(c) 0。(a) の `notices` は `unmatched_add`（2 件目）・`unknown_id`（8 件目）・`ambiguous_region`（9 件目）の 3 件で、`taken` の数と食い違わない（知らせる行になった `unknown_id`・`ambiguous_region` は数えず、`unmatched_add` は数える） |
| `UT-match_summits-77` | `write_summit_outputs`（成功、書き込みの失敗、中断） | 同じプロセス。`text` は `'{"a":"é"}\n'`、`workbook` は `openpyxl.Workbook()`、`results_dir` は `<tmp>`（`match_summits._config_opt` は空）。(a) そのまま。(b) `<tmp>/merged_summit.xlsx.tmp` というディレクトリを先に作る。(c) `<tmp>/merged_summit.geojson` というディレクトリを先に作る。(d) `unittest.mock.patch.multiple('match_summits.os', replace=…, remove=…)` で、`os.replace` の 2 回目〈GeoJSON〉を `OSError(errno.EIO, 'Input/output error')` にし、`os.remove` の `merged_summit.xlsx` への呼び出しだけを `OSError(errno.EACCES, 'Permission denied')` にする（ほかの呼び出しは本物に渡す）。(e) (d) から `os.remove` の差し替えを除く。(f) (e) の `os.replace` の差し替えで、2 回目〈GeoJSON〉を `OSError` でなく `common.SignalStop(15)` を上げるもの（本物は呼ばない）にする（XLSX を置いた後の中断）。(g) `workbook.save` を `ValueError('x')` を上げるものに差し替える（`unittest.mock.patch.object(workbook, 'save', side_effect=ValueError('x'))`）。(h) `os.replace` の 1 回目〈XLSX〉を、本物を呼んで置いた直後に `common.SignalStop(15)` を上げるものにする（XLSX を置いてから `placed_xlsx` を立てるまでの窓）。(i) 2 回目〈GeoJSON〉を、本物を呼んで置いた直後に `common.SignalStop(15)` を上げるものにする（GeoJSON を置いてから `done` を立てるまでの窓）。(j) (f) に、(d) の `os.remove` の差し替え（`merged_summit.xlsx` への呼び出しだけを `OSError(errno.EACCES, 'Permission denied')` にする）を足す | `write_summit_outputs(text, workbook, <tmp>)` | (a) 戻り値は `None`。`<tmp>` に `merged_summit.geojson` と `merged_summit.xlsx` だけがある（`.tmp` が無い）。GeoJSON のバイト列が `text` の UTF-8 と同じ、XLSX が `openpyxl.load_workbook` で読める。(b) `SystemExit` の `code` が 1、SW1（1 行目 `ERROR: merged_summit.geojson か merged_summit.xlsx を書けない: <tmp>/merged_summit.xlsx: Is a directory。2 つの出力はどちらも置いていない`、2 行目 `対処: <tmp> の空きと権限を確かめてから、scripts/run_pipeline.sh --phase 4 を起動し直す`）。`merged_summit.geojson.tmp` と `merged_summit.geojson`・`merged_summit.xlsx` が無い（ディレクトリ `merged_summit.xlsx.tmp` は消せないので残る）。(c) `code` が 1、SW1 の `{path}` が `<tmp>/merged_summit.geojson`（`Is a directory`）。`merged_summit.xlsx` が無い（置いた後に消した）、`.tmp` が無い。(d) `code` が 1、SW2（1 行目 `ERROR: merged_summit.geojson か merged_summit.xlsx を書けない: <tmp>/merged_summit.geojson: Input/output error。置いた merged_summit.xlsx も消せなかった: <tmp>/merged_summit.xlsx: Permission denied`、2 行目 `対処: <tmp>/merged_summit.xlsx を手で消し、<tmp> の空きと権限を確かめてから、scripts/run_pipeline.sh --phase 4 を起動し直す`。「どちらも置いていない」を含まない）。`merged_summit.xlsx` が残り、`.tmp` が無い。(e) `code` が 1、SW1（`<tmp>/merged_summit.geojson: Input/output error`）、`<tmp>` が空。(f) `common.SignalStop` が伝わり（`SystemExit` にならない）、標準エラー出力に何も出さない。`<tmp>` が空（置いた `merged_summit.xlsx` を消し、`.tmp` も無い）。(g) `ValueError` が伝わり（`SystemExit` にならない）、標準エラー出力に何も出さない。`<tmp>` が空（`merged_summit.geojson.tmp` も `merged_summit.xlsx.tmp` も残らない）。(h) `common.SignalStop` が伝わり、標準エラー出力に何も出さず、`<tmp>` が空（置いた `merged_summit.xlsx` を消した）。(i) `common.SignalStop` が伝わり、標準エラー出力に何も出さず、`<tmp>` が空（置いた 2 つとも消した。『そろえて置いていない』）。(j) `common.SignalStop` が伝わり、標準エラー出力が SW3 の 2 行（1 行目 `WARNING: 中断のため、置いた merged_summit.xlsx を消せなかった: <tmp>/merged_summit.xlsx: Permission denied`、2 行目 `対処: <tmp>/merged_summit.xlsx を手で消してから、scripts/run_pipeline.sh --phase 4 を起動し直す`）。`merged_summit.xlsx` が残り、`.tmp` が無い |
| `UT-match_summits-78` | `check_defect_gate`（3 条件と同数・件数の数え方） | 同じプロセス。ピークは `K1 = (1, 1)`・`K2 = (2, 2)`（この順）で、`cmp5_common.MergedPeakRow('p', n, {'peak_lat': 'x', 'peak_lon': 'y', 'key_col_resolved': 'true'})`。ゾーンの表は `{K1: PeakZones(<K1 の AZ>, <K1 の delete判定ゾーン>), K2: PeakZones(…)}`（`cmp5_common.ZoneFeature(index, kind, pixel, area_complete, {}, {})` を直接作る。`area_complete` は書かない限り `True`）。`DeleteMatch` は `summit_status`・`dominant`・`peak_status` を空にし、`unmatched` に `Summit` を `n` 件（`n` は書いたとおり）。しきい値は書かない限り 2 | `check_defect_gate(<ピーク>, <ゾーン>, <DeleteMatch>, <しきい値>)` | (a) `unmatched` 2 件・しきい値 2: `[]`（同数は当たらない）。(b) `unmatched` 3 件: `[('unmatched_over_threshold', 3)]`。(c) `K1` の delete判定ゾーンだけ `area_complete=False`: `[('is_area_incomplete', 1)]`。(d) `K1` の AZ と delete判定ゾーンの両方が `False`: `[('is_area_incomplete', 1)]`（1 つのピークは 1 と数える）。(e) `K1` の AZ と `K2` の delete判定ゾーンが `False`: `[('is_area_incomplete', 2)]`。(f) `K2` の `key_col_resolved` が `'false'`（このピークが `ambiguous` でも除外しない。この関数は `activation` を受け取らない）: `[('is_key_col_unresolved', 1)]`。(g) `unmatched` 3 件、`K1` の AZ・delete判定ゾーンと `K2` の delete判定ゾーンが `False`、`K1`・`K2` の `key_col_resolved` が `'false'`: `[('unmatched_over_threshold', 3), ('is_area_incomplete', 2), ('is_key_col_unresolved', 2)]`（3 条件すべて、この順）。(h) 空のピークと空のゾーンの表、`unmatched` 0 件、しきい値 0: `[]` |
| `UT-match_summits-79` | 中断（`SIGTERM`・`SIGINT`）で止まる（XLSX を置いた直後。終了コードと SM4） | 子のプロセス。(a) `SIGTERM`、(b) `SIGINT` を、別々の子で送る。起動の場面で、`python3 <tmp>/src/scripts/match_summits.py` の代わりに、`-c` で次のドライバを動かす（cwd は `<tmp>`）: `sys.path` の先頭に `<tmp>/src/scripts` を入れ、`sys.argv = ['match_summits.py', '--config', '<tmp>/c.ini']` にし、`import os, signal, match_summits` した後、`real = os.replace` を控えて、`os.replace` を「`real(src, dst)` を呼び、`os.path.basename(dst)` が `merged_summit.xlsx` なら `os.kill(os.getpid(), <シグナル>)` を送る」関数に差し替え、`match_summits.main()` を呼ぶ（`<シグナル>` は (a) `signal.SIGTERM`、(b) `signal.SIGINT`） | ドライバを終わるまで待つ | 終了コード (a) 143、(b) 130。`<tmp>/data/results/` に `merged_summit.xlsx`・`merged_summit.geojson`・`.tmp` で終わる名前が無い（置いた XLSX を消した）。標準エラー出力に `ERROR:` で始まる行が無く、SW3 も無い。ログの最後から 2 番目の行が、UT-75 の SM4 と同じ文（`written` が偽の `merged_summit.geojson と merged_summit.xlsx はそろえて置いていない`）で、最後の行は `終了:` で始まり、(a) `SIGTERM`、(b) `SIGINT` を含む |
