# findsummits - 詳細設計書 (LLD)

| 項目 | 内容 |
|---|---|
| 作成日 | 2026-10-18 |
| 最終更新日 | 2026-10-22 |
| ステータス | ドラフト |
| 参照 HLD | [`30_HLD.md`](30_HLD.md) |

---

**読み方**: この文書は詳細設計書（LLD）である。概要設計書（HLD）が決めたプログラムと関数の名前、受け取るもの、返すものの上に、関数ごとの細部（型、内部のデータの持ち方、メッセージの文面、ファイルへの割り付け）を足す（書き分けは[文書管理ルール](CLAUDE.md#hld-と-lld-の書き分け)）。LLD の次は実装フェーズ（COD）と単体テスト（UT）で、LLD の字句と上位の文書だけで、コードと単体テストのコードを書ける細かさにすることを目標にする（2026-10-18 に持ち主が決めた）。コードを書く側は、LLD に加えて、ユーザー要件定義書（URD）、ソフトウェア要件仕様書（SRS）、HLD と、関連する文書を読める前提にする。上位の文書に決まっていることは写さずにリンクで指し、どの文書にも決まっていないことをこの文書で決め切る。章立てとモジュールの単位は、アーキテクチャ決定記録（ADR）の [ADR-LLD-001](decisions/ADR-LLD-001-lld-format-module-granularity-and-t2-timing.md) による。今は 2.1 共通部品と 3.1 `preprocess_boundaries`（行政区域前処理）と 5.1 `run_pipeline`（パイプライン制御）と 5.2 `resolve_config`（設定解決）と、それらが使う分の 1 章と 2.2〜2.4 だけを書いてある。ほかのモジュールの節は、書くときに足す。

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
- [3. CMP1 行政区域前処理](#3-cmp1-行政区域前処理)
  - [3.1 `preprocess_boundaries`](#31-preprocess_boundaries)
    - [3.1.1 ファイル割付](#311-ファイル割付)
    - [3.1.2 型とデータ](#312-型とデータ)
    - [3.1.3 関数の細部](#313-関数の細部)
    - [3.1.4 メッセージ文面](#314-メッセージ文面)
    - [3.1.5 UT 候補](#315-ut-候補)
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
- 型は、そのモジュールの言語の書き方で書く（Python は型ヒント。例 `set[str]`）。
- Python のプログラム（2.1 の内部の関数を除く）は、`sys.exit(<終了コード>)` を `sys` の属性として呼ぶか、最後まで進んで終わる。`raise SystemExit`・`os._exit`・組み込みの `exit()`・`quit()`・`from sys import exit` を書かない。`except BaseException`、裸の `except:`、`SystemExit`・`LogWriteError`・`SignalStop` を捕まえる `except` を書かない（2.1 の `start_log` が `sys.exit` の差し替えで終了コードを記録し、ログの書き込みの失敗とシグナルを `BaseException` の子の例外で伝えるため）。後始末と結果の要約は `finally` で書く（書き方の型は [2.1.3](#213-関数の細部) の前置き）。`os._exit` を呼ぶのは 2.1 の内部の関数 `_finish_log` だけ。
- 利用者向けの Python のコマンド（[3.1](#31-preprocess_boundaries) の `preprocess_boundaries`・4.1 の `fetch_tiles`）は、起動の部分の内部の関数 `_parse_args` で引数を読み、bash の `run_pipeline`（[5.1.3](#513-関数の細部)の `parse_args`）と同じ受け方にする: 引数を左から 1 つずつ読む。値をとる名前は、次の引数（`--config a.ini`）か、名前の後の `=` の後（`--config=a.ini`。最初の `=` で分ける）で値を受け取り、次の引数で受け取る値は `-` で始まっていてもそのまま値にする。受け付けない引数（`--` で始まらない引数、知らない名前、値をとらない名前に `=` を付けたもの〈`--help=x`〉、`--` だけ）、値をとる名前が最後にあって値が無いこと、同じ名前を 2 回渡すこと（`--help` を除く。名前を読んだ時点で、値を受け取るより先に見る）は、その場で終了コード 2 で止める。名前の省略（`--conf`）は受けない。`--help` を読んだら、それより後の引数を読まずに、使い方の文を標準出力に出して終了コード 0 で終わる（設定を読まず、ロックを掛けない。[HLD 2.9.3](30_HLD.md#293-同時起動の排他)）。`--help` より前の引数の誤りは、先に止まる。`argparse` は使わない（名前の省略を受け、誤りのメッセージが [2.2](#22-ログとメッセージの文面) の書き方にならないため）。メッセージの文面と使い方の文は、モジュールの節に置く。3.1 と 4.1 が共有する規約なので、横断の決まりとしてここに置く。
- 2.1 の `start_log`・`log_info`・`log_warning`・`log_error` は、メインのスレッドからだけ呼ぶ（`start_log` はシグナルのハンドラを付けるのに `signal.signal` を使い、これはメインのスレッドでしか呼べない）。ほかのスレッドで動く処理は、知らせたいことをメインのスレッドに返し、メインのスレッドが出す（行が混ざらないようにし、ログの書き込みの失敗とシグナルをメインのスレッドで受けるため）。スレッドを使うかと、シグナルで止まるときにスレッドをどう終えるかは、使うモジュールの節で決める（CMP2（タイル取得）の並列取得の形は [HLD 2.9.1](30_HLD.md#291-目的と範囲) の対象外の行で LLD に送られている）。
- LLD の記号（メッセージの記号など）は、`tools/lint_docs.py` の検査 H（1 文字の記号の残り。`C1`〜`C8`・`D` と数字・`K1`〜`K6`。コード表記の中は検査しない）に当たらない名前にする。2.1 と 2.2 の記号は、設定の誤り CF1〜CF7、`--mesh` の誤り A1〜A5、メッシュのリストの誤り R1〜R3、共通の場面 G1〜G7、ログファイルの行 L1〜L3、設定の相互制約 CX1 である。5.2 の記号は、引数の誤り RA1・RA2、パスの改行 RP1、標準出力に書けないとき RW1 である。5.1 の記号は、引数の誤り PA1〜PA5、設定解決の出力の誤り RS1、起動前提条件の不足 PC1・PC2、取得完了の記録の不足 FC1・FC2、前回の出力を消せないとき CO1、単独起動の案内 PG1〜PG3、ログの行 PL1〜PL9 である。2.1.3 のメッシュの読み方のテストベクトルの ID は MV-01〜MV-21 である。3.1 の記号は、引数の誤り BA1〜BA4、N03 行政区域 ZIP が無いか探せない BZ1・BZ2、入力の検証 BV1〜BV8、生成と書き込みと置き換えの失敗 BF1〜BF4、新しい版の警告 BW1、ログの行 BL1〜BL5 である。
- メッセージの文面は、[2.2](#22-ログとメッセージの文面) の書き方で、置き換える部分を `{名前}` で書く。
- UT 候補は、`ID`・確かめること・準備・入力・期待 の 5 列の表で、`UT-<モジュール名>-NN`（2 桁の連番。[テスト方針書 §6](02_test_policy.md#6-テストケースid命名の大枠)）ごとに 1 行で書く。準備には、入力を与える前に整えること（置くファイル、起こすプロセス、差し替えるもの、捕まえる出力）を書く。小節の前置きに名前を付けて書いた共通の準備で足りるときは、その名前を書き、ケースに固有の準備だけを足す。手動のケースは ID の直後に `（手動）` を付ける。単体テスト仕様書（`50_UT.md`）を作るときは、準備はケースの手順へ移る。
- 規則は、実装者が読むその関数の見出し（関数の細部の `#####` の見出し。群の見出しで分けたモジュールでは `######` の見出し）の下に置く。2 章の横断の節には、2 つ以上のモジュールで共有するものと、どのプログラムにも属さない項目（[ADR-LLD-001](decisions/ADR-LLD-001-lld-format-module-granularity-and-t2-timing.md) の Decision 7。Makefile のターゲット名など）だけを置き、関数の見出しの下からリンクで指す。横断の節にある規則に関数ごとの扱いがあれば、その関数の見出しの下にも書く（実装者は関数の見出しの下を読み、横断の節の段落の奥までは読まないことがあるため）。

## 2. 共通部品と横断

この章は、HLD 3.9 の共通部品のモジュール（2.1）と、HLD の「目的と範囲」の「対象外」の行で繰り返し出る項目を受ける横断の節（2.2〜2.4）を置く。横断の節は追跡の宣言を持たず、モジュールの節から指す（ADR-LLD-001 の Decision 1）。2.2〜2.4 は今は 2.1・3.1・5.1・5.2 が使う項目だけを書き、ほかのモジュールの節を書くときに足す。

### 2.1 共通部品

- **ID**: LLD-common
- **対応 HLD**: [3.9](30_HLD.md#39-共通部品)・[4.1](30_HLD.md#41-fr-001-標高タイル事前取得)・[4.4](30_HLD.md#44-fr-004-33メッシュ結合解析オーケストレーション)・[4.8](30_HLD.md#48-fr-008-per-mesh-csv-統合)・[4.17](30_HLD.md#417-fr-017-n03-行政区域前処理データ準備)・[5.6](30_HLD.md#56-nfr-006-可搬性環境)・[5.7](30_HLD.md#57-nfr-007-ログ出力)・[5.11](30_HLD.md#511-nfr-011-手順文書による環境構築成果物生成の完遂性)
- **ファイル**: `scripts/common.py`

各部品の処理の正本は、[HLD 3.9](30_HLD.md#39-共通部品) の表の「定義のある節」で、この節はそれを Python で書くための細部だけを足す。[5.6](30_HLD.md#56-nfr-006-可搬性環境)（可搬性）は、`fcntl` を使うので POSIX の OS だけで動くことと、ロックは `data_dir` がローカルのファイルシステムにある前提（[HLD 2.9.3](30_HLD.md#293-同時起動の排他)）で受ける。[5.11](30_HLD.md#511-nfr-011-手順文書による環境構築成果物生成の完遂性)（手順文書）は、どのメッセージにも `対処:` の行で次の操作を書くこと（[2.2](#22-ログとメッセージの文面)）で受ける。

#### 2.1.1 ファイル割付

- 部品はすべて `scripts/common.py` 1 本に置く。プログラムは `venv/bin/python3 scripts/<名前>.py` で起動され（HLD 第 3 章）、`scripts/` が import の探索先の先頭になるので、`import common` で読む。
- UT のコードは `tests/scripts/test_common.py` に置く（[HLD 2.6.4](30_HLD.md#264-ディレクトリ構成) の `tests/scripts/`、[DEC18](30_HLD.md#266-設計判断)「テストは対象と同じ名前で分ける」）。テストの枠組みは[テスト方針書 3.4](02_test_policy.md#34-テストを先に書く進め方)で選ぶので、LLD では決めない。UT のコードの各テストには、`# trace: <UT の ID>`（例 `# trace: UT-common-01`）のコメントを付ける（文書管理ルールの[追跡の宣言](CLAUDE.md#追跡の宣言)）。
- `scripts/common.py` の親の親をソースツリーの根とする。既定の設定ファイル `params/config.ini` とその見本 `params/config.ini.example` は、その下にある（[2.1.2](#212-型とデータ)の `DEFAULT_CONFIG_PATH`・`_EXAMPLE_CONFIG_PATH`）。

#### 2.1.2 型とデータ

- 終了コードの定数（モジュールの最上位の `int`）: `EXIT_OK = 0`・`EXIT_ERROR = 1`・`EXIT_USAGE = 2`・`EXIT_UNRESOLVED = 3`・`EXIT_DEFECT = 4`（[HLD 2.5.1](30_HLD.md#251-終了コード)）。
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

  整数の種類は、値が `re.fullmatch(r'[0-9]+', v)` に合い、先頭の `0` を除いた文字列 `d = v.lstrip('0') or '0'` の桁数（`len(d)`）が 18 以下のときだけ `int(d)` にする（`int(v)` にしない。先頭の `0` が 4300 個を超える値で `ValueError` になるため）。符号・小数点・全角の数字・空の値は型に合わず、19 桁以上は範囲の外とする。18 桁までにするのは、Python の `int` への変換の桁数の上限（既定 4300 桁）に掛からないようにし、CMP4（地形解析エンジン）の C++ の実装が 64 ビットの符号付き整数で持てるようにするため。上の表で上限の無い整数のキーの許容範囲の文に `（18 桁まで）` を付けるのはこのため。この上限は [SRS 2.2.1](20_SRS.md#221-設定可能項目) の「許容範囲に上限を書いていない整数の項目は、18 桁までとする」と [HLD 2.3.3](30_HLD.md#233-検証と記録) の検査に書いてある。値は `configparser` が前後の空白を除いた文字列。空の値（`key =`）はどのキーでも型に合わない誤りで、「書いていない」とは扱わない（未設定にしたいときはキーの行を書かない）。

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
3. `open(path, encoding='utf-8-sig')` で全部を読む。`OSError` か `UnicodeDecodeError` なら CF2 で `EXIT_USAGE`。読んだ文字列に NUL（`'\x00'`）があれば、CF3（`{reason}` は `NUL の文字がある`）で `EXIT_USAGE`（4 で `default_section` に NUL を使うので、`[\x00]` の節を既定の節として読ませないため）。
4. `configparser.ConfigParser(interpolation=None, strict=True, default_section='\x00', inline_comment_prefixes=None)` を作り、`optionxform = str`（キーの大文字と小文字を区別する）にして `read_string(text, source=path)` する。`configparser.Error` なら CF3 で `EXIT_USAGE`。`default_section` をファイルに書けない名前にするので、`[DEFAULT]` もふつうの節として読まれ、下の 5 で知らない節になる。`#` と `;` で始まる行は注釈（`configparser` の既定）。行の途中の `#`・`;` は注釈にならず、値の一部になる（`data_dir = /x # 注` の値は `/x # 注` になる）。
5. ファイル全体の検査: ファイルの順に、`_CONFIG_KEYS` に無い節は CF4、ある節の中で `_CONFIG_KEYS` のその節に無いキーは CF5 を、誤りの一覧に足す（知らない節の中のキーには CF5 を出さず、その節の CF4 だけにする。別の節にあるキー、大文字の違うキーも CF5）。
6. キーごとの検査: `_CONFIG_KEYS` の順に、`keys` にあって、ファイルのその節に書いてあるキー（別の節に書いてあるものは書いていないものとして扱う）の値を [2.1.2](#212-型とデータ)の判定に掛け、合わなければ CF6 を足す。
7. 必須の検査: `_CONFIG_KEYS` の順に、`required` にあってファイルのその節に書いていないキーは CF7 を足す（`[fetch]` の節に `data_dir` のキーを書き、`[paths]` の節に書かなかったときは、5 の CF5 と、この CF7 の両方が出る）。
8. 誤りの一覧が空でなければ、一覧の順に各誤りのメッセージ（2 行ずつ）を `log_error` で出し、`EXIT_USAGE`。1 つでも誤りがあれば、全部を出してから 1 回だけ止まる。
9. `keys` の各キーについて `ConfigValue` を作る。書いてあれば `from_file=True` と判定後の値（整数は `int`）、書いていなければデフォルト（`log_dir` は `data_dir` の値から作る）と `from_file=False`、デフォルトの無いキーは `None` と `from_file=False`。`Config(path, values)` を返す。

確かめないこと: 相互制約、パスに改行を含む設定の拒否（どちらも起動口が自分で確かめる。HLD 3.9 の表の後の段落）。`keys` に無いキーの値。ログには書かない（`start_log` の前なので画面だけ）。

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

1. `path = os.path.join(data_dir, <2.3 のロックファイルの名前>)`。`fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o644)`。`OSError` なら G2 で `EXIT_ERROR`。
2. `fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)`。`BlockingIOError` なら G1、ほかの `OSError` なら G2 で `EXIT_ERROR`。成功したら `_state.lock_fd = fd` にし、閉じない（プロセスが終わるまで持つ。[HLD 2.9.3](30_HLD.md#293-同時起動の排他)）。ロックファイルは消さない。

呼ぶのは利用者向けの 2 本（`preprocess_boundaries`・`fetch_tiles`）が `start_log` の前（HLD 2.9.3 の起動時の順序）なので、メッセージは画面にだけ出る。bash の `run_pipeline` も同じファイルに `flock` を掛ける（同じ名前を [2.3](#23-ファイルの名前と書き方)から取る）。

##### fetch_record_path

`fetch_record_path(data_dir: str) -> str`

`os.path.join(data_dir, 'tiles', <2.3 の取得完了の記録の名前>)` を返す。ファイルの有無は見ない。

##### mesh_to_latlon

`mesh_to_latlon(mesh: str) -> tuple[tuple[float, float], tuple[float, float]]`

`mesh` が `[0-9]{4}` に合わなければ `ValueError`。`aa = int(mesh[:2])`、`bb = int(mesh[2:])`。返すのは `((南端の緯度, 西端の経度), (北端の緯度, 東端の経度))` で、4 つとも `float`（経度は `float(100 + bb)`・`float(101 + bb)` にする。Python では `100 + bb` が `int` になるため）。式と計算の順は[2.4](#24-言語ごとに別に実装する式のテストベクトル)の決まりのとおり。範囲（3036〜6848）は見ない。

##### latlon_to_tile

`latlon_to_tile(lat: float, lon: float, z: int) -> tuple[int, int]`

`(x, y)` を返す。式と計算の順は 2.4 の決まりのとおり。引数を検査しない（呼ぶのは CMP1（行政区域前処理）・CMP2 の関数で、渡すのは日本のメッシュの四隅。HLD 3.9 の表の「使うところ」）。

#### 2.1.4 メッセージ文面

表（記号・場面・1 行目・`対処:` の行・終了コード）で書く。`{path}` は `os.path.abspath` したパス、`{reason}` は `OSError` の `strerror`（無ければ `str(e)`）か、`UnicodeDecodeError` なら `UTF-8 として読めない`、`configparser.Error` なら `str(e)` の 1 行目。`{example_path}` は `_EXAMPLE_CONFIG_PATH`。全体に共通する場面（ロックとログ）は [2.2](#22-ログとメッセージの文面)の G1〜G7 を指し、ここに写さない。

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
| `UT-common-27` | メッシュ → 緯度経度 | 同じプロセス。なし | 2.4 の表 1 の行 | 期待の値と `==` で等しく、4 つとも `float` |
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

### 2.2 ログとメッセージの文面

書式と出し先の正本は[HLD 2.5.3](30_HLD.md#253-利用者向けのメッセージ)と[HLD 5.7.2](30_HLD.md#572-処理の流れ)で、ここは文面と行の形を決める。CMP4（地形解析エンジン）の C++ の `start_log` など、同じ決まりを別の言語で実装するモジュールも、ここの文面と行の形にする。今は 2.1・3.1・5.1・5.2 が使う分だけを書いてある。

書き方の決まり:

- 文面は日本語。1 行目は `ERROR:` か `WARNING:` と空白 1 つの後に、起きたことを先に書き、`:` と空白 1 つの後に対象（パス、キー、オプション）を書く。
- 2 行目は `対処:` と空白 1 つの後に、利用者が次にすべき操作を書く。
- 文末に句点を付けない。パスは絶対パスで出す。OS の理由（`{reason}`）は OS が返す文のまま（英語でよい）。

ログファイルの行（各行の先頭の時刻は HLD 5.7.2 の 3「行の書式」。下は時刻の後の文面）。L1〜L3 は、ログファイルにこの文面を時刻付きで書き、標準出力にも時刻なしで同じ文面を出す（[SRS NFR-007](20_SRS.md#nfr-007-ログ出力)の「通常のログは標準出力とログディレクトリに同時に出す」と、HLD 5.7.2 の 3「行の書式」の「画面に出すのと同じ文面」による）:

| 記号 | 行 | 文面 |
|---|---|---|
| L1 | 始まりと引数（ログファイルの最初の行） | `開始: {program} {args}`。`{args}` は起動の引数（プログラムの名前を含まない）を、受け取った順に、下の引用の決まりで 1 つずつ書いて空白 1 つでつないだもの。引数が無ければ `開始: {program}` |
| L2 | 設定 | `設定ファイル: {config_path}` の 1 行の後、`load_config` に渡したキーごとに `_CONFIG_KEYS` の順で `設定: [{section}] {key} = {value}（{source}）`。`{source}` は、`from_file` が真なら `ファイル`、偽なら `デフォルト`（値が `None` のときも `デフォルト`）。値が `None` なら `{value}` を `未設定` |
| L3 | 終わり | `終了: 終了コード {code}、終了時刻 {end}、所要時間 {sec} 秒`。`{end}` は先頭の時刻と同じ書式、`{sec}` は `f'{秒:.3f}'`。シグナルで止まったときは `終了: 終了コード {code}（{signame} を受けて止まった）、終了時刻 {end}、所要時間 {sec} 秒`（`{signame}` は `signal.Signals(signum).name`） |

引用の決まり（L1 の `{args}`。[HLD 5.7.2](30_HLD.md#572-処理の流れ) の 4「始まりと終わりの行」の「最初の行にプログラムの名前と、起動の引数を受け取ったとおりに書く」を、引数の切れ目と中身が読み取れる形で 1 行に書くため）: 引数が空でなく、どの字も ASCII の英数字か `_@%+=:,./-` のどれかなら、そのまま書く。それ以外は、`'` で囲み、中の `'` を `'"'"'` に置き換える（空の引数は `''`）。Python の `shlex.join` と同じ結果になる（Python は `shlex.join(argv)` を使ってよい）。引数に改行があれば、その改行でファイルの行が分かれ、分かれた各行に時刻を付ける（[2.1.3](#213-関数の細部)の `_emit`）。bash の `run_pipeline` は L2 を書かない（[HLD 3.3.3](30_HLD.md#333-関数)の `open_log`）。

全体に共通する場面のメッセージ（HLD 2.5.3 の表と[HLD 5.7.3](30_HLD.md#573-異常系)の表の場面のうち、今回の分。`{config_path}` は `start_log` に渡された `Config` の `path`〈設定ファイルの絶対パス〉）:

| 記号 | 場面 | 1 行目（`ERROR:` と空白 1 つの後） | 2 行目（`対処:` と空白 1 つの後） | 終了コード |
|---|---|---|---|---|
| G1 | 同時起動 | `同じデータ置き場で別のコマンドが動いている: {lock_path}` | `動いているコマンドが終わってから起動し直す` | 1 |
| G2 | ロックファイルを開けない・ロックを掛けられない | `ロックファイルを開けないか、ロックを掛けられない: {lock_path}: {reason}` | `設定ファイルの data_dir と、そのディレクトリの書き込みの権限を確かめる` | 1 |
| G3 | ログの出力先を用意できない | `ログの出力先を用意できない: {path}: {reason}`（`{path}` は `log_dir` か、開けなかったログファイル） | `設定ファイル {config_path} の log_dir と、ディレクトリの権限を確かめてから起動し直す` | 1 |
| G4 | 同じ名前のログファイルが既にある | `同じ名前のログファイルが既にある: {path}` | `1 秒以上おいて起動し直す` | 1 |
| G5 | ログファイルに書けなくなった | `ログファイルに書けなくなった: {path}: {reason}` | `ディスクの空きとログファイルの権限を確かめてから起動し直す` | 1 |
| G6 | 終わりの行だけを書けなかった | `ログファイルに終わりの行を書けなかった: {path}: {reason}` | `ディスクの空きとログファイルの権限を確かめる。終了コード 1 はログが欠けたことを示し、書き終えた成果物は消していない` | 1 |
| G7 | 捕まらなかった例外 | `予期しない例外で止まった: {type}: {message}`（`{type}` は例外のクラス名 `exc_type.__name__`、`{message}` は `str(exc)`。`{message}` に改行があれば、`log_error` の決まりで行が分かれる） | `このメッセージと続く Traceback をログファイルから写して開発者に知らせる` | 1 |

設定・引数の誤り（終了コード 2）の文面は、その誤りを確かめる部品か関数の節に置く（2.1 では CF1〜CF7・A1〜A5、5.2 では RA1・RA2・RP1）。2 つ以上のモジュールが確かめる誤りは、下の表に置く。

設定の相互制約（[HLD 2.3.3](30_HLD.md#233-検証と記録)）。確かめるのは、5.2 の `resolve_config`、CMP4（地形解析エンジン）の `analyze_terrain`、CMP5（統合・突合）の `merge_peaks` で、同じ文面を出す。

| 記号 | 場面 | 1 行目（`ERROR:` と空白 1 つの後） | 2 行目（`対処:` と空白 1 つの後） | 終了コード |
|---|---|---|---|---|
| CX1 | 一次フィルタ閾値が最終フィルタ閾値以上 | `プロミネンス一次フィルタ閾値が最終フィルタ閾値以上: [analysis] prominence_primary_m = {primary}（{primary_source}）、[merge] prominence_final_m = {final}（{final_source}）（{config_path}）` | `[analysis] prominence_primary_m を [merge] prominence_final_m より小さくする（100 以上 {final} 未満の整数）` | 2 |

`{primary}`・`{final}` は使う値（デフォルトのときはデフォルト値）、`{primary_source}`・`{final_source}` は L2 の `{source}` と同じく `ファイル` か `デフォルト`、`{config_path}` は設定ファイルの絶対パス（`Config` の `path`）。

### 2.3 ファイルの名前と書き方

置き場の正本は HLD（[2.6.4](30_HLD.md#264-ディレクトリ構成)、[2.9.3](30_HLD.md#293-同時起動の排他)、[4.1.2](30_HLD.md#412-処理の流れ)）で、ここは HLD が LLD に送った名前を決める。今は 2.1・3.1・5.1 が使う分だけを書いてある。

- ロックファイル: `data_dir` の直下の `findsummits.lock`。中身は空のまま使い、消さない（HLD 2.9.3）。Python は `acquire_lock`、bash は `run_pipeline` の `acquire_lock` が同じ名前を使う。
- 取得完了の記録: `data_dir` の `tiles/` の直下の `fetch_complete.txt`（HLD 4.1.2 の「取得完了の記録」）。中身は、取得を終えた 1 次メッシュのコードを 1 行 1 件で、ASCII の数字 4 字に改行（LF）を付けて書く（BOM・空白・CR・空行・`#` の行を書かない。昇順に並べる）。0 件なら空のファイル。読む側（CMP2 の `fetch_tiles` の `read_fetch_record`〈[HLD 3.2.3](30_HLD.md#323-関数)〉と、bash の `run_pipeline` の `check_fetch_record`〈[5.1](#51-run_pipeline)〉。どちらもこの読み方にする）は、空のファイルを行の無い記録（0 件）とし、そのほかは最後の LF を 1 つ除いてから LF で行に分け、どの行も ASCII の数字 4 字ちょうどでなければ書式が違うとする（最後の行の後の LF は無くてもよい。同じコードの重なりは 1 件とする）。読む側が `--mesh` のファイルの読み方（空白・`#` の行を許す）にしないのは、記録がツールだけが書くファイルで、[HLD 4.1.2](30_HLD.md#412-処理の流れ)が「4 桁の数字でない行があれば」止まると決めているため（壊れた記録を読み飛ばさない）。書き方は、下の一時ファイルの決まりに従う（CMP2 の節で指す）。Python は `fetch_record_path`、bash は `run_pipeline` の `fetch_record_path` が同じ名前を使う。
- 一時ファイル: 出力を一時ファイルに書いてから置き換えるモジュール（今は 3.1。CMP2・CMP5 の節も、書くときにこれに従う）は、出力と同じディレクトリに、出力のファイル名の後に `.tmp` を付けた名前（`regions.geojson` なら `regions.geojson.tmp`）で一時ファイルを書く。名前は固定にする（同じ `data_dir` で動く利用者向けのコマンドは 1 つだけで〈[HLD 2.9.3](30_HLD.md#293-同時起動の排他)〉、内部の起動口は CMP3 のロックの下で動くので、名前が重ならない。プロセスの番号を入れると、強制終了のたびに一時ファイルが増え、消す決まりが別に要る）。前の起動が強制終了で残した一時ファイルは、次の起動が開くときに中身を捨てて上書きする。手順は「書く」と「置き換える」の 2 段に分け、2 段の間に何をするか（いくつの一時ファイルを書き終えてから、どの順で置き換えるか）は、そのモジュールの節で決める。書く（Python）: `open(<一時ファイル>, 'wb')`（テキストは `open(<一時ファイル>, 'w', encoding='utf-8', newline='\n')`）で開き、書き、`flush()`、`os.fsync(f.fileno())`、閉じる（`fsync` は、置き換えた後に電源が落ちて中身の無いファイルが残るのを防ぐため）。開く・書く・flush・fsync・閉じるのどれかで `OSError` になったら、その一時ファイルを `os.remove` で消してから（消せないときの `OSError` は無視する）、そのモジュールのメッセージで止まる（同じ処理で先に書き終えたほかの一時ファイルも消すかは、モジュールの節で決める）。置き換える（Python）: `os.replace(<一時ファイル>, <出力>)`。

### 2.4 言語ごとに別に実装する式のテストベクトル

HLD の [DEC6](30_HLD.md#225-設計判断決めたこと理由却下した案)「メッシュ・タイル変換の二重実装を許容」のとおり、`mesh_to_latlon`・`latlon_to_tile` を Python（2.1）・C++（CMP4 の「変換」の群）・JavaScript（`index.html` の「3.9 と同じ決まり」の群）で別に実装し、`tile_to_latlon` を Python（3.1）と C++（CMP4 の「変換」の群）で別に実装し（[HLD 3.1.3](30_HLD.md#313-関数)）、この節の表で一致を確かめる。テストのコードとこの表の置き場とテストのレベルは、テスト方針書で決める（[HLD 2.2.1](30_HLD.md#221-目的と範囲)の対象外の行）。今は `mesh_to_latlon`・`latlon_to_tile`・`tile_to_latlon` の分だけを書いてある。

計算の決まり（どの言語も IEEE 754 の倍精度で、書いた順に左から計算する。式の正本は用語集の[メッシュコード → 緯度経度](00_GLOSSARY.md#mesh-to-latlon)と[緯度経度 → XYZ タイル番号](00_GLOSSARY.md#latlon-to-tile)）:

- `mesh_to_latlon`: 南端の緯度 = `(2 × aa) / 3`（`2 × aa` を整数で求め、3 で 1 回だけ割る）。北端の緯度 = `(2 × (aa + 1)) / 3`。西端の経度 = `100 + bb`、東端の経度 = `101 + bb`。
- `latlon_to_tile`: `n = 2^z`。`x = floor(((lon + 180) / 360) × n)`。`r = (lat × π) / 180`（`math.radians` のような 1 つの関数にまとめない。掛ける順で値が変わるため）。`y = floor(((1 − ln(tan(r) + 1 / cos(r)) / π) / 2) × n)`。`π` は言語の標準の定数（Python の `math.pi`、C++ の `std::numbers::pi`、JavaScript の `Math.PI`。どれも同じ倍精度の値）。`tan`・`cos`・`ln` は言語の標準のもの。
- `tile_to_latlon`: `n = 2^z`。北西端の経度 = `((x / n) × 360) − 180`。北西端の緯度 = `(atan(sinh(π × (1 − (2 × y) / n))) × 180) / π`（`2 × y` を先に求めて `n` で割り、`1` から引き、`π` を掛け、`sinh`、`atan`、`180` を掛け、`π` で割る。この順に計算する）。`x`・`y` は小数でもよい（[HLD 3.1.3](30_HLD.md#313-関数) の表の「タイル番号（小数を含む）」）。南東端は `x + 1`・`y + 1` を同じ式に入れる。`sinh`・`atan` は言語の標準のもの（Python の `math.sinh`・`math.atan`）。式の正本は用語集の[XYZ タイル番号 → 緯度経度](00_GLOSSARY.md#tile-to-latlon)。

期待値の導き方: 用語集の式を上の順に倍精度で計算した値で、2026-10-18 に CPython で求めた。`tan`・`cos`・`ln` は言語で最後の桁が違いうるので、表 2 の行は、`floor` の前の値と最も近い整数の差が 0.016 以上ある点か、`floor` の前の値がちょうど整数になる点（経度 −180・0・135）だけにした（日本全土1次メッシュコードリストの 175 メッシュの四隅を、ズーム 14・15 で調べ、経度 135 度のほかは差がどれも 0.016 以上だった）。

表 3 は、`tile_to_latlon` の式を上の順に倍精度で計算した値で、2026-10-22 に CPython 3.14.8 で求めた。経度は四則演算だけで決まるので、どの言語も `==` で等しくなる。緯度は `sinh`・`atan` を通り、言語の標準の関数で最後の桁が違いうるので、期待の値との差の絶対値が `1e-12`（度）以下なら一致とする（`floor` で丸める `latlon_to_tile` の表 2 と違い、値をそのまま比べるため。この許容差は変換の関数の値を比べるためのもので、タイルの矩形と北方領土のポリゴンが辺で接するだけか重なるかの判定〈[3.1.3](#313-関数の細部)〉が言語で同じになることまでは言わない。北方領土除外タイルリストを作るのは Python の 3.1 だけである）。

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

## 3. CMP1 行政区域前処理

この章は、CMP1（行政区域前処理）の 1 本のプログラム（[HLD 3.1.1](30_HLD.md#311-プログラム)）のモジュールを置く。CMP1 にコンポーネント内の共通部品は無い（[HLD 3.1.4](30_HLD.md#314-コンポーネント内の共通部品)）。

### 3.1 `preprocess_boundaries`

- **ID**: LLD-preprocess_boundaries
- **対応 HLD**: [3.1](30_HLD.md#31-cmp1-行政区域前処理)・[4.17](30_HLD.md#417-fr-017-n03-行政区域前処理データ準備)・[5.2](30_HLD.md#52-nfr-002-メモリ使用量)・[5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)
- **ファイル**: `scripts/preprocess_boundaries.py`

処理の正本は [HLD 4.17.2](30_HLD.md#4172-処理の流れ)（作り直しの条件と置き換えの順序の正本は [HLD 2.10.3](30_HLD.md#2103-フェーズのやり直し) の「フェーズ1」）で、関数の名前と役割と呼ぶ順は [HLD 3.1.3](30_HLD.md#313-関数) の表のとおり。この節は Python で書くための細部（型、データの持ち方、メッセージの文面、ログの行）だけを足す。[5.2](30_HLD.md#52-nfr-002-メモリ使用量)（メモリ）は、N03 の GeoJSON を読み込むときにフィーチャごとの元の辞書を捨てながら shapely のポリゴンに変えること（3.1.3 の `load_n03_features`）で受け、メモリのピークは実装の後に HLD 5.2.2 の「実測の計画」の 5 で測る。[5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)（再現性）は、出力のフィーチャとポリゴンの並びと JSON の書き方を入力の並びによらず決めること（3.1.3 の `build_regions`・`build_municipalities`・`write_temp_outputs`）と、`tile_to_latlon` を [2.4](#24-言語ごとに別に実装する式のテストベクトル) の表 3 で CMP4 とそろえることで受ける。結合のつなぎ目は `CMP1-INT1`・`CMP1-EXT1`・`CMP1-EXT2`（[HLD 3.1.5](30_HLD.md#315-結合のつなぎ目)）で、IT のケースは `60_IT.md` の `IT-CMP1-INT1-01`〜`04`・`IT-CMP1-EXT1-01`〜`05`・`IT-CMP1-EXT2-01`。

#### 3.1.1 ファイル割付

- 関数はすべて `scripts/preprocess_boundaries.py` 1 本に置く。`venv/bin/python3 scripts/preprocess_boundaries.py` で起動され（[HLD 3.1.1](30_HLD.md#311-プログラム)）、共通部品は `import common` で読む（2.1.1 と同じ）。shapely は `import shapely` と `from shapely.geometry import box, mapping, shape, MultiPolygon, Polygon` と `from shapely.geometry.polygon import orient` で読む（[環境定義](01_environment.md) の既存の依存。[HLD 4.17.2](30_HLD.md#4172-処理の流れ) の 5「市区町村の GeoJSON を展開する」）。ファイルの先頭のコメントに `# trace: LLD-preprocess_boundaries` を書く。起動の部分は `if __name__ == '__main__': main()`。
- UT のコードは `tests/scripts/test_preprocess_boundaries.py` に置く。各テストに `# trace: UT-preprocess_boundaries-NN` のコメントを付ける。テストの枠組みは 2.1.1 と同じく[テスト方針書 3.4](02_test_policy.md#34-テストを先に書く進め方)で選ぶ。

#### 3.1.2 型とデータ

- 定数（モジュールの最上位。どれも内部）:
  - `_SOURCE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))`、`_JAPAN_MESH_LIST_PATH = os.path.join(_SOURCE_ROOT, 'params', 'mesh_list_japan.txt')`（[HLD 3.1.1](30_HLD.md#311-プログラム) の「自分の置き場から求め、起動した作業ディレクトリによらない」）。既定の設定ファイルは `common.DEFAULT_CONFIG_PATH`（[2.1.2](#212-型とデータ)）。
  - `_ZIP_NAME = re.compile(r'N03-([0-9]{8})_GML\.zip')`（`fullmatch` で使う。`\d` は全角の数字にも合うので使わない）。
  - `_NT_CODES = frozenset({'01695', '01696', '01697', '01698', '01699', '01700'})`（[HLD 4.17.2](30_HLD.md#4172-処理の流れ) の「北方領土除外タイルリストと北方領土除外メッシュリスト」）。
  - `_REGIONS: tuple[tuple[str, str, str], ...]`: HLD 4.17.2 の「地域と SOTA のコード」の表の 60 行を、表の順に（N03 の名前, `assoc`, `area_code`）で持つ（表の値は写さず、HLD の表から作る。表の順は `UT-preprocess_boundaries-15` の期待に使う）。`assoc` が `JA8` の 14 行が北海道の振興局で、`N03_002` で引く。ほかの 46 行は `N03_001` で引く。
  - 出力の名前: `_OUTPUT_NAMES = ('regions.geojson', 'municipalities.geojson', 'nt_excluded_tiles.txt', 'nt_excluded_meshes.txt')`（この順を、一時ファイルの並び、置き換えの順、要約の順に使う）、`_VERSION_NAME = 'n03_version.txt'`（[HLD 4.17.2](30_HLD.md#4172-処理の流れ) の「出力の置き場」の表）。置き場はどれも `os.path.join(<data_dir>, 'boundaries')`。
  - `_TILE_ZOOM = 15`、`_LIST_LIMIT = 10`（BV5・BV6 のメッセージに並べる件数の上限。[3.1.4](#314-メッセージ文面)）。
- `@dataclass(frozen=True) class N03Feature`: `index: int`（`features` の配列の中の位置。1 から数える。メッセージに出す）、`n03_001: object`・`n03_002: object`・`n03_004: object`・`n03_005: object`・`n03_007: object`（`properties` の同じ名前の値。JSON の値のまま〈`str`・`None`・数など〉。キーが無いか `properties` がオブジェクトでなければ `None`）、`geom_type: object`（`geometry` がオブジェクトならその `type` の値、`geometry` が無いか `null` かオブジェクトでなければ `None`）、`polygons: tuple[Polygon, ...]`（`geom_type` が `'Polygon'` ならその 1 つ、`'MultiPolygon'` なら含まれるポリゴンを配列の順に。どちらも `is_empty` が真のポリゴン〈`{"type":"Polygon","coordinates":[]}` など〉は含めない。ほかの種類と `None` のときは空のタプル。空のポリゴンを除くのは、`validate_n03` の BV7・BV8 がポリゴンの数で判定し、空のポリゴンは外接矩形が NaN になって後の計算を壊すため）。`N03_003`・`N03_006` は持たない（使わない）。
- 出力のフィーチャ: `dict`（GeoJSON の Feature のオブジェクト）。キーの順は `type`（`'Feature'`）、`properties`、`geometry`。`geometry` は `shapely.geometry.mapping(<幾何>)` の値（キーの順は `type`、`coordinates`）。地域の `properties` のキーの順は `assoc`・`area_code`・`region_name`、市区町村は `prefecture`・`municipality`・`code`（[SRS §8.2.1](20_SRS.md#821-n03-前処理済みファイル詳細仕様) の並び）。
- 除外タイル: `tuple[int, int]`（`(x, y)`、ズーム 15）。除外メッシュ: `str`（[2.1.2](#212-型とデータ) のメッシュコード）。
- モジュールの状態（内部。モジュールの最上位の変数で、初めは空の文字列）: `_n03_source: str`（`load_n03_features` の 1 が入れる、メッセージの対象のファイルを示す文 `<ZIP のパス> の N03-<YYYYMMDD>.geojson`。BV3〜BV8・BF2 の `{source}`）、`_config_opt: str`（`main` が `start_log` の後に入れる、[3.1.4](#314-メッセージ文面) の `{config_opt}` の値。BW1 と `{rerun}` を使うメッセージが使う）。
- モジュールの状態の理由: HLD [3.1.3](#313-関数の細部) の表の `needs_rebuild`・`validate_n03`・`build_regions` などが受け取るものに、メッセージに要る対象のファイルと設定ファイルのパス（[HLD 4.17.3](30_HLD.md#4173-異常系) の「CMP1 の失敗」の行と「新しい版の N03 ZIP がある」の行）が無い。引数で渡すと HLD の表と食い違い、フィーチャごとに持たせるのは同じ値の重複になる。モジュールの状態は 2.1 の `_state` と同じ扱い。

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
2. 誤りは BA1（受け付けない引数）、BA2（値が無い）、BA4（同じ名前を 2 回）で、`common.log_error` で出して `sys.exit(common.EXIT_USAGE)`。
3. `--help` は、[3.1.4](#314-メッセージ文面) の使い方の文を `sys.stdout.write` で出し、`sys.stdout.flush()` の後に `sys.exit(common.EXIT_OK)`。
4. 読み終えたら、`--config` の値が空の文字列なら BA3 で `sys.exit(common.EXIT_USAGE)`。
5. `_Args(config=<値か None>, rebuild=<--rebuild を読んだか>)` を返す。

##### find_n03_zip

`find_n03_zip(ref_dir: str) -> tuple[str, str]`（返すのは（採用した ZIP の絶対パス, YYYYMMDD））。

1. `names = os.listdir(ref_dir)`。`FileNotFoundError`・`NotADirectoryError` なら候補が 0 件として 3 へ（`ref/` が無いときも ZIP を置く場所を案内するため）。ほかの `OSError` なら BZ2 で `sys.exit(common.EXIT_ERROR)`。
2. 候補は、`_ZIP_NAME.fullmatch(name)` に合い、`os.path.isfile(os.path.join(ref_dir, name))` が真の名前（同じ名前のディレクトリは候補にしない）。
3. 候補が 0 件なら BZ1 で `sys.exit(common.EXIT_ERROR)`（[HLD 4.17.3](30_HLD.md#4173-異常系) の「起動前提条件の不足」の行）。
4. YYYYMMDD（8 桁の文字列。字の順と数の順が同じ）が最大の候補を採る。`path = os.path.abspath(os.path.join(ref_dir, name))`、`size = os.path.getsize(path)`（`OSError` なら BZ2）。BL1 を `common.log_info` で出し、`(path, YYYYMMDD)` を返す。

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
2. `with zipfile.ZipFile(zip_path) as zf:` で開き（3 の展開もこの `with` の中で行う）、`namelist()` に `member` があるかを見る（ZIP の最上位だけ。`/` を含む名前の項目は見ない。[HLD 4.17.2](30_HLD.md#4172-処理の流れ) の 5「市区町村の GeoJSON を展開する」）。開けないか読めない（`OSError`・`zipfile.BadZipFile`・`zlib.error`・`EOFError`・`NotImplementedError`）なら BV1、`member` が無ければ BV2 で `sys.exit(common.EXIT_ERROR)`。
3. `with tempfile.TemporaryDirectory(prefix='findsummits-n03-') as work:` の中で、`zf.extract(member, work)` で `member` だけを展開する（`extractall` を使わない）。作業用のディレクトリを作れないか、展開の書き込みが失敗した（`OSError`）なら BF1、ZIP の中身が壊れている（`zipfile.BadZipFile`・`zlib.error`・`EOFError`・`NotImplementedError`）なら BV1 で止まる。
4. 同じ `with` の中で、展開したファイルを `open(<パス>, encoding='utf-8')` で開き、`json.load(f, parse_constant=_reject_constant)` で読む（`_reject_constant` は内部の関数で、`NaN`・`Infinity`・`-Infinity` を受けたら `ValueError(f'{name} は JSON の数でない')` を上げる）。`OSError`・`UnicodeDecodeError`・`ValueError`（`json.JSONDecodeError` を含む）・`RecursionError` なら BV3 で止まる。読み終えたら `with` を抜け、作業用のディレクトリを消す（`TemporaryDirectory` が消す。止まるときも、`SignalStop` で抜けるときも消える。[HLD 4.17.3](30_HLD.md#4173-異常系) の「シグナル」の行。消せないときの例外は `TemporaryDirectory` の既定のまま）。
5. 形を確かめる: 読んだ値がオブジェクトで、`type` が `'FeatureCollection'` で、`features` が配列であること。違えば BV3（`{reason}` は `FeatureCollection でない` か `features が配列でない`）。
6. `features` の各要素を、先頭から 1 つずつ `N03Feature` に変える。変えた要素は配列の中で `None` に置き換え（`features[i] = None`）、読んだ値の全体を持つ変数も先に捨てる（元の辞書を持ち続けないため。[HLD 5.2](30_HLD.md#52-nfr-002-メモリ使用量)）。要素がオブジェクトでなければ BV3（`{reason}` は `{index} 番目のフィーチャがオブジェクトでない`）。`geom_type` が `'Polygon'` か `'MultiPolygon'` のときは `shapely.geometry.shape(<geometry>)` でポリゴンを作り、`ValueError`・`TypeError`・`IndexError`・`KeyError`・`AttributeError`・`shapely.errors.GEOSException` なら BV3（`{reason}` は `{index} 番目のフィーチャの幾何の座標を読めない: <例外の 1 行目>`）。
7. `N03Feature` の並び（`features` の順）を返す。属性の値は検査しない（`validate_n03` が見る）。

##### validate_n03

`validate_n03(features: Sequence[N03Feature]) -> None`。次の順に確かめ、最初に当たった検証のメッセージを `common.log_error` で出して `sys.exit(common.EXIT_ERROR)`（[HLD 4.17.2](30_HLD.md#4172-処理の流れ) の「入力の検証」の 2 つ目〜6 つ目の項目。1 つ目の ZIP は `load_n03_features`）。止まるときは何も書かない。

1. 属性と幾何の欠け（BV4）: フィーチャの順に、次をこの順に見て、最初に当たったフィーチャと項目で止まる。`n03_001`・`n03_004`・`n03_007` が空でない `str` でない。`n03_002`・`n03_005` が `str` でも `None` でもない。`geom_type` が `None`（幾何が無い）。`geom_type` が `'Polygon'`・`'MultiPolygon'` でない。
2. 表に無い名前（BV5）: `n03_001 == '北海道'` のフィーチャは `n03_002` が `_REGIONS` の `JA8` の行の名前にあるか、ほかのフィーチャは `n03_001` が `JA8` でない行の名前にあるかを見る（北海道の振興局を都府県の名前で引かず、都府県を振興局の名前で引かない）。無い名前を、北海道なら `北海道/<n03_002>`（`None` なら `北海道/null`）、ほかなら `<n03_001>` の形の文字列にし、重なりを除いて昇順に並べる。
3. 同じコードでの食い違い（BV6）: `n03_007` が同じフィーチャで、`(n03_001, n03_004, n03_005)` の組が 1 つでないコードを昇順に並べる（`None` と空の文字列は違う値とする）。
4. ポリゴンの無い地域（BV7）: 2 の引き方でフィーチャを `_REGIONS` の行に割り当て、ポリゴンの数（`len(polygons)` の和）が 0 の行の名前を表の順に並べる。
5. 北方領土 6 村の欠け（BV8）: `_NT_CODES` のコードのうち、そのコードのフィーチャのポリゴンの数の和が 0 のコードを昇順に並べる（[HLD 4.17.4](30_HLD.md#4174-設計判断) の DEC38）。

##### build_regions

`build_regions(features: Sequence[N03Feature]) -> list[dict]`

1. フィーチャを `validate_n03` の 2 の引き方で `_REGIONS` の行に割り当て、行ごとにポリゴンを集める（北方領土 6 村も根室振興局に入る）。
2. 行ごとに、集めたポリゴンを `shapely.to_wkb(p, byte_order=1)` のバイト列の昇順に並べ替えてから `shapely.union_all` で合わせる（並べ替えるのは、合わせた結果が入力のフィーチャの並びによらないようにするため。[HLD 4.17.2](30_HLD.md#4172-処理の流れ) の「出力の置き場」の後の箇条の「出力の並びは入力のフィーチャの並びによらない」、[HLD 5.3](30_HLD.md#53-nfr-003-再現性決定論的出力)）。`shapely.errors.GEOSException` なら BF2（`{step}` は `地域 <表の名前> を合わせる（dissolve）`）で止まる。結果が空か、`Polygon`・`MultiPolygon` でなければ、同じ BF2（`{reason}` は `合わせた結果が面でない: <geom_type>`）で止まる。
3. 結果の各ポリゴンを `orient(p, sign=1.0)`（外側の環を反時計回り、内側の環を時計回り。RFC 7946 の右手則）でそろえる。結果が `Polygon` なら 1 つの `Polygon`、`MultiPolygon` ならそろえたポリゴンを結果の順に並べた `MultiPolygon` にする。
4. フィーチャ（`properties` は `assoc`・`area_code`・`region_name`〈表の名前〉）を作り、`(assoc, area_code)` の昇順（字の順）に並べて返す。

##### build_municipalities

`build_municipalities(features: Sequence[N03Feature]) -> list[dict]`

1. フィーチャを `n03_007` ごとに集める。
2. コードごとに、ポリゴンを `shapely.to_wkb(p, byte_order=1)` のバイト列の昇順に並べ、`MultiPolygon(<並べたポリゴン>)` にする（座標と環の向きは N03 のまま変えない。union しない。ポリゴンが 1 つでも `MultiPolygon`。[HLD 4.17.2](30_HLD.md#4172-処理の流れ) の「市区町村 GeoJSON」）。
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

- 1〜4 のどれかで `OSError`（1・2 の `FileNotFoundError` を除く）なら、BF4（`{path}` は消すか置き換えるか書くところだったパス）で `sys.exit(common.EXIT_ERROR)`。残った一時ファイルは消さない（次の起動が上書きする。版の記録が無ければ次の起動で作り直す。[HLD 2.10.3](30_HLD.md#2103-フェーズのやり直し)）。

#### 3.1.4 メッセージ文面

前置き: 書き方は [2.2](#22-ログとメッセージの文面)。ロックとログの場面（G1〜G7。`{config_path}` は `Config` の `path`）は [2.2](#22-ログとメッセージの文面)、設定の誤り（CF1〜CF7）と日本全土リストの誤り（R1〜R3。案内は `None` で既定の対処）は [2.1.4](#214-メッセージ文面) の文面のまま。L1〜L3 は [2.2](#22-ログとメッセージの文面)（`{program}` は `preprocess_boundaries`）。`{path}`・`{zip_path}`・`{ref_dir}` は `os.path.abspath` したパス、`{reason}` は [3.1.3](#313-関数の細部) の前置きのとおり、`{source}` は `_n03_source`。`{arg}`・`{value}` は [2.2](#22-ログとメッセージの文面) の引用の決まりで書いたもの（`shlex.quote`）。`{config_opt}` は `_config_opt`（`--config` を渡されたときは空白 1 つと `--config` と空白 1 つと `Config` の `path` を `shlex.quote` したもの、渡されなかったときは空）。`{rerun}` は `直してから、タイル取得とパイプライン制御を起動する前に venv/bin/python3 scripts/preprocess_boundaries.py{config_opt} --rebuild を起動し、正常に終える`（[HLD 4.17.3](30_HLD.md#4173-異常系) の「CMP1 の失敗」の行の「CMP2・CMP3 を起動する前に CMP1 を再実行する案内」。`--rebuild` を付けるのは、前の出力がそろっていても作り直させるため）。

`ERROR:`・`WARNING:` のメッセージ（2 行目は `対処:` と空白 1 つの後）:

| 記号 | 場面 | 1 行目 | 2 行目 | 終了コード |
|---|---|---|---|---|
| BA1 | 受け付けない引数 | `preprocess_boundaries の知らない引数: {arg}` | `使える引数は --config・--rebuild・--help（venv/bin/python3 scripts/preprocess_boundaries.py --help で使い方を出す）` | 2 |
| BA2 | 値が無い | `{option} の値が無い` | `{option} の後に値を書く（venv/bin/python3 scripts/preprocess_boundaries.py --help で使い方を出す）` | 2 |
| BA3 | 値が違う | `--config の値が違う: {value}` | `--config には空でないパスを渡す` | 2 |
| BA4 | 同じ名前を 2 回 | `{option} を 2 回渡した` | `{option} は 1 回だけ渡す` | 2 |
| BZ1 | N03 行政区域 ZIP が無い | `N03 行政区域 ZIP が無い: {ref_dir}/N03-YYYYMMDD_GML.zip（YYYYMMDD は半角の数字 8 桁）` | `国土数値情報の行政区域データ（全国）の ZIP を入手し、名前を変えずに {ref_dir} の直下に置いてから、もう一度起動する` | 1 |
| BZ2 | ZIP を探す場所を読めない | `N03 行政区域 ZIP を探す場所を読めない: {path}: {reason}` | `{path} の読み取りの権限を確かめてから、もう一度起動する` | 1 |
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

- **同じプロセス**: テストのプロセスの中で `scripts/` を import の探索先に入れて `import preprocess_boundaries` し、関数を直接呼ぶ（`start_log` を呼ばない。`log_info` などは画面にだけ出る）。止まるケースは `SystemExit` を捕まえて終了コードを読み、標準出力と標準エラー出力は `contextlib.redirect_stdout`・`redirect_stderr` で捕まえる。一時のディレクトリ `<tmp>` をケースごとに作り、`tempfile.tempdir` を `<tmp>/t`（作っておく）に差し替える（作業用のディレクトリの残りを見るため。ケースの後に元に戻す）。
- **小さな N03**: 次の 67 フィーチャの FeatureCollection（UTF-8 の JSON。`properties` には `N03_001`〜`N03_005`・`N03_007` の 6 つのキーを置き、書かないものは `null`）。各フィーチャの幾何は、ポリゴンを 1 つ持つ `MultiPolygon` で、ポリゴンは外側の環だけの矩形 `[[w, s], [e, s], [e, n], [w, n], [w, s]]`（反時計回り）。
  - 地域のフィーチャ 60: HLD 4.17.2 の対応表の `i` 行目（0 から）ごとに 1 つ。`JA8` の行は `N03_001` が `北海道`・`N03_002` が表の名前、ほかは `N03_001` が表の名前。`N03_004` は `市` と `i` の 2 桁（`市00`）、`N03_007` は `9` と `i` の 4 桁（`90000`）。矩形は `w = 120 + 0.2 × (i mod 10)`、`s = 25 + 0.2 × floor(i / 10)`、`e = w + 0.1`、`n = s + 0.1`。ただし根室振興局の行は `w = 147.5`、`s = 44.8`、`e = 147.6`、`n = 44.9`（メッシュ `6747` の中）。
  - 北方領土のフィーチャ 7: `k` = 0〜5 について、`N03_001` が `北海道`・`N03_002` が `根室振興局`・`N03_004` が `村` と `k`（`村0`）・`N03_007` が `1695 + k` を 0 で埋めた 5 桁（`f'{1695 + k:05d}'`。`01695`〜`01700`）で、矩形は `w = 148.1 + 0.1 × k`、`s = 45.5`、`e = w + 0.05`、`n = 45.55`（メッシュ `6848` の中）。7 つ目は `01695` の 2 つ目のフィーチャ（`N03_004` は `村0`）で、矩形は `w = 147.1`、`s = 44.8`、`e = 147.15`、`n = 44.85`（メッシュ `6747` の中。`6747` は根室振興局の矩形も持つので、除外メッシュにならない）。
  - この N03 からの出力: 地域 60、市区町村 66（`01695` は 2 つのポリゴンの `MultiPolygon`）、日本全土のリストを `3720`・`6747`・`6848` にしたときの除外メッシュは `6848` だけ。根室振興局の地域は、根室振興局の矩形と北方領土の 7 つの矩形の 8 つのポリゴンの `MultiPolygon`。
- **一時の ZIP**: 小さな N03（ケースが書き換えたものを含む）を `json.dumps(…, ensure_ascii=False)` の UTF-8 にして、`<data_dir>/ref/N03-20250101_GML.zip` の最上位の `N03-20250101.geojson` に書く（`zipfile.ZIP_DEFLATED`）。同じ ZIP の最上位に `N03-20250101_prefecture.geojson`（中身は `{}`）も置く。
- **子のプロセス**: 一時のソースツリー `<tmp>/src` を作り、`<tmp>/src/scripts/` にテストする `scripts/preprocess_boundaries.py` と `scripts/common.py` を写し、`<tmp>/src/params/mesh_list_japan.txt` に `3720\n6747\n6848\n` を書く。一時の設定 `<tmp>/c.ini` に `[paths]` の `data_dir = <tmp>/data`・`log_dir = <tmp>/logs` を書き、`<tmp>/data/ref/` に一時の ZIP を置く。`<tmp>/work` と `<tmp>/t` を作る。起動は `subprocess.run([sys.executable, '<tmp>/src/scripts/preprocess_boundaries.py', *<引数>], cwd='<tmp>/work', env={**os.environ, 'TMPDIR': '<tmp>/t'}, capture_output=True)`（ケースが書かなければ引数は `--config ../c.ini`）。終了コード、標準出力と標準エラー出力（UTF-8 で読む）、`<tmp>/logs` の下のログファイル、`<tmp>/data/boundaries/` を確かめる。

| ID | 確かめること | 準備 | 入力 | 期待 |
|---|---|---|---|---|
| `UT-preprocess_boundaries-01` | 引数の正しい形 | 同じプロセス | `_parse_args` に (a) `[]`、(b) `['--config', 'a.ini']`、(c) `['--config=a=b.ini', '--rebuild']`、(d) `['--rebuild', '--config', '--help']` | (a) `_Args(None, False)`、(b) `_Args('a.ini', False)`、(c) `_Args('a=b.ini', True)`、(d) `_Args('--help', True)` |
| `UT-preprocess_boundaries-02` | 引数の誤り | 同じプロセス | `_parse_args` に (a) `['foo']`、(b) `['--foo']`、(c) `['--rebuild=x']`、(d) `['--help=x']`、(e) `['--']`、(f) `['--conf', 'a.ini']`、(g) `['--config']`、(h) `['--config', '']`、(i) `['--config=']`、(j) `['--rebuild', '--rebuild']`、(k) `['--config', 'a', '--config', 'b']`、(l) `['--config', 'a', '--config']` | どれも 2、標準出力は空。(a)〜(f) は BA1（(a) の 1 行目は `ERROR: preprocess_boundaries の知らない引数: foo`、(f) の引数は `--conf`）、(g) は BA2（`--config の値が無い`）、(h)(i) は BA3（`ERROR: --config の値が違う: ''`）、(j) は BA4（`--rebuild を 2 回渡した`）、(k)(l) は BA4（`--config を 2 回渡した`。(l) は BA2 でない） |
| `UT-preprocess_boundaries-03` | `--help` | 子のプロセス | 引数を (a) `--rebuild --help --foo`、(b) `--foo --help` | (a) 0、標準出力は [3.1.4](#314-メッセージ文面) の使い方の文と等しい、`<tmp>/data/findsummits.lock` と `<tmp>/logs` が無い。(b) 2、BA1（`--foo`）、標準出力は空 |
| `UT-preprocess_boundaries-04` | ZIP の選び方 | 同じプロセス。`<tmp>/ref/` に空のファイル `N03-20250101_GML.zip`（3 バイト）・`N03-20260101_GML.zip`（5 バイト）・`N03-2026010_GML.zip`・`N03-20270101_GML.ZIP`・`N03-20270101_GML.zip.bak`・数字を全角にした `N03-`・8 桁・`_GML.zip`（数字はコードポイント U+FF10〜U+FF19）（数字はコードポイント U+FF10〜U+FF19）を置き、ディレクトリ `N03-20280101_GML.zip` を作る | `find_n03_zip('<tmp>/ref')` | `('<tmp>/ref/N03-20260101_GML.zip', '20260101')`、標準出力は BL1 の 1 行 `N03 行政区域 ZIP: <tmp>/ref/N03-20260101_GML.zip（版 20260101、5 バイト）` |
| `UT-preprocess_boundaries-05` | ZIP が無い・探せない | 同じプロセス | `find_n03_zip` に (a) 空のディレクトリ、(b) 無いパス、(c) 通常のファイルのパス、(d) 権限 `000` のディレクトリ（実効ユーザーが root なら飛ばす） | (a)(b)(c) は 1、BZ1（1 行目は `ERROR: N03 行政区域 ZIP が無い: <渡したパスの絶対パス>/N03-YYYYMMDD_GML.zip（YYYYMMDD は半角の数字 8 桁）`）。(d) は 1、BZ2（`{reason}` は `Permission denied`） |
| `UT-preprocess_boundaries-06` | 作り直さないときと警告 | 同じプロセス。`<tmp>/b/` に 4 つの出力の名前の空のファイルと、`n03_version.txt`（中身 `20250101\n`）を置く | `needs_rebuild('<tmp>/b', False, …)` に (a) `'20250101'`、(b) `'20260101'`、(c) `'20240101'`、(d) `rebuild` を `True` にして `'20250101'` | (a)(b)(c) は偽、(d) は真。標準出力は (a)(b)(c) が BL2 の `作り直さない: 出力と版の記録がそろっている（版 20250101）`、(d) が `作り直す: --rebuild を付けた`。(b) だけ標準エラー出力に BW1 の 2 行（`WARNING: 記録した版より新しい N03 行政区域 ZIP がある: 記録した版 20250101、置いてある最新の版 20260101` と、`対処: 新しい版を使うなら venv/bin/python3 scripts/preprocess_boundaries.py --rebuild を起動する（作り直すと取得完了の記録が消えるので、タイル取得からやり直す）`）。ほかは標準エラー出力が空 |
| `UT-preprocess_boundaries-07` | 出力が欠けたとき | 同じプロセス。06 と同じ置き方から、ケースごとに 1 つを変える | (a)〜(d) 4 つの出力のどれか 1 つを消す（別々に）、(e) `nt_excluded_tiles.txt` をディレクトリにする、(f) `<tmp>/b` を消す | どれも真で、BL2 が `作り直す: <無いファイルの絶対パス> が無い`（(f) は `regions.geojson` のパス）。ファイルは変わらない |
| `UT-preprocess_boundaries-08` | 版の記録の形 | 同じプロセス。06 と同じ置き方で、`n03_version.txt` の中身をケースごとにバイト列で書く | (a) `20250101`（改行なし）、(b) `20250101\n`、(c) `2025010\n`、(d) `20250101\n20250101\n`、(e) `20250101\r\n`、(f) `20250101\n\n`、(g) `EF BB BF` の後に `20250101\n`、(h) 空、(i) 全角の数字 8 桁（コードポイント U+FF12・U+FF10・U+FF12・U+FF15・U+FF10・U+FF11・U+FF10・U+FF11）と `\n`、(j) `n03_version.txt` を消す、(k) `n03_version.txt` をディレクトリにする。どれも `needs_rebuild('<tmp>/b', False, '20250101')` | (a)(b) は偽（BL2 の版は `20250101`）。(c)〜(i)(k) は真で、BL2 は `作り直す: 版の記録が読めないか、8 桁の数字の 1 行でない: <tmp>/b/n03_version.txt`。(j) は真で、BL2 は同じ文（版の記録は 4 つの出力の後に見るので、`が無い` の文でない） |
| `UT-preprocess_boundaries-09` | ZIP を読む | 同じプロセス。`<tmp>/data/ref/` に一時の ZIP。`zipfile.ZipFile.extract`・`zipfile.ZipFile.extractall` を、呼ばれた項目の名前を記録してから元を呼ぶ物に差し替える | `load_n03_features('<tmp>/data/ref/N03-20250101_GML.zip', '20250101')` | 67 個の `N03Feature`（`index` は 1〜67、`n03_007` などが小さな N03 のとおり、`geom_type` は `MultiPolygon`、`polygons` は 1 つ）。`extract` が `N03-20250101.geojson` の 1 回だけ呼ばれ、`extractall` は呼ばれない。`<tmp>/t` は空 |
| `UT-preprocess_boundaries-10` | ZIP と GeoJSON を読めない | 同じプロセス。ケースごとに `<tmp>/data/ref/N03-20250101_GML.zip` を作る | (a) 中身が `not a zip` のテキストのファイル、(b) 最上位に `N03-20250101.geojson` が無い ZIP（`N03-20250101_prefecture.geojson` だけ）、(c) `x/N03-20250101.geojson` だけの ZIP、(d) `N03-20250101.geojson` の中身が `FF FE`、(e) 中身が `{`、(f) 1 つ目のフィーチャの座標の 1 つを `NaN` にした JSON（字の `NaN`）、(g) 中身が `[]`、(h) `{"type":"FeatureCollection","features":{}}`、(i) `features` の 1 つ目が `1`、(j) 1 つ目のフィーチャの `coordinates` を `[[[1]]]` にした JSON | どれも 1、`<tmp>/t` は空。(a) は BV1、(b)(c) は BV2（1 行目は `ERROR: N03 行政区域 ZIP の最上位に N03-20250101.geojson が無い: <ZIP のパス>`）、(d) は BV3（`{reason}` は `UTF-8 として読めない`）、(e)(f) は BV3、(g) は BV3（`{reason}` は `FeatureCollection でない`）、(h) は BV3（`features が配列でない`）、(i) は BV3（`1 番目のフィーチャがオブジェクトでない`）、(j) は BV3（`{reason}` が `1 番目のフィーチャの幾何の座標を読めない:` と空白 1 つで始まる） |
| `UT-preprocess_boundaries-11` | シグナルでも作業用のディレクトリを消す | 子のプロセスの代わりに、`[sys.executable, '-c', <試験用の短いプログラム>]` を `cwd='<tmp>/work'`・`TMPDIR` を `<tmp>/t` にして起動する。試験用のプログラムは、`<tmp>/src/scripts` を `sys.path` の先頭に入れて `import preprocess_boundaries` し、`json.load` を「自分へ `SIGTERM` を送ってから元の `json.load` を呼ぶ物」に差し替えてから、`sys.argv = ['preprocess_boundaries.py', '--config', '<tmp>/c.ini']` にして `preprocess_boundaries.main()` を呼ぶ | 起動する | 143、`<tmp>/t` は空、`<tmp>/data/boundaries/` は作られていない、ログファイルの最後の行が `SIGTERM` を受けて止まった形の L3 で、その前の行が BL5 の `結果の要約: 途中で止まった。終えた分: なし` |
| `UT-preprocess_boundaries-12` | 属性と幾何の欠け | 同じプロセス。小さな N03 を、ケースごとに 1 か所だけ書き換えて一時の ZIP にし、`load_n03_features` で読む | 3 つ目のフィーチャの (a) `N03_001` を `null`、(b) `N03_004` を `""`、(c) `N03_007` のキーを消す、(d) `N03_002` を `1`、(e) `N03_005` を `[]`、(f) `geometry` を `null`、(g) `geometry` を `{"type":"Point","coordinates":[0,0]}`、(h) 2 つ目のフィーチャの `N03_007` を `null` にし、3 つ目の `geometry` を `null` にする | `validate_n03` がどれも 1、BV4。`{detail}` は (a) `N03_001 が空でない文字列でない`、(b) `N03_004 が空でない文字列でない`、(c) `N03_007 が空でない文字列でない`、(d) `N03_002 が文字列でも null でもない`、(e) `N03_005 が文字列でも null でもない`、(f) `幾何が無い`、(g) `幾何の種類が "Point"`。(a)〜(g) の `{index}` は 3、(h) は 2 で `N03_007` の項目 |
| `UT-preprocess_boundaries-13` | 表に無い名前 | 同じプロセス。12 と同じ作り方 | (a) 愛知県の行のフィーチャの `N03_001` を `テスト県`、(b) 石狩振興局の行の `N03_002` を `石狩支庁`、(c) 石狩振興局の行の `N03_002` を `東京都`、(d) 愛知県の行の `N03_001` を `石狩振興局`、(e) 北海道でない 11 行の `N03_001` を `県A`〜`県K`（`A`〜`K` は英大文字） | どれも 1、BV5。`{names}` は (a) `テスト県`、(b) `北海道/石狩支庁`、(c) `北海道/東京都`、(d) `石狩振興局`、(e) `県A・県B・県C・県D・県E・県F・県G・県H・県I・県J ほか 1 件`（(a)(d)(e) は、名前を変えた地域のポリゴンが無くなるが、BV5 が先に止まる） |
| `UT-preprocess_boundaries-14` | 同じコードでの食い違い | 同じプロセス | (a) `01696` のフィーチャをもう 1 つ足し（矩形は `01696` の矩形と同じ）、`N03_004` を `村9` にする、(b) 同じく足して `N03_005` を `""` にする（元は `null`） | どちらも 1、BV6、`{codes}` は `01696` |
| `UT-preprocess_boundaries-15` | ポリゴンの無い地域と北方領土の欠け | 同じプロセス | (a) 愛知県の行のフィーチャを除く、(b) 愛知県と十勝総合振興局の行のフィーチャを除く、(c) 愛知県の行の幾何を `{"type":"MultiPolygon","coordinates":[]}` にする、(d) `01698` のフィーチャを除く、(e) `01698` のフィーチャと愛知県の行のフィーチャを除く、(f) 愛知県の行の幾何を `{"type":"Polygon","coordinates":[]}` にする、(g) `01698` の幾何を `{"type":"Polygon","coordinates":[]}` にする | どれも 1。(a)(c)(f) は BV7 で `{names}` は `愛知県`、(b) は BV7 で `愛知県・十勝総合振興局`（表の順）、(d)(g) は BV8 で `{codes}` は `01698`、(e) は BV7（BV8 より先） |
| `UT-preprocess_boundaries-16` | 地域を合わせる | 同じプロセス。小さな N03 に、愛知県の行の矩形と東の辺を共有する矩形（`w = 120.1`、`s = 25.0`、`e = 120.15`、`n = 25.1`）のフィーチャ（`N03_001` は `愛知県`、`N03_004` は `市60`、`N03_007` は `90060`）を足し、宮城県の行のフィーチャの幾何を、穴を持つポリゴン 1 つの `MultiPolygon`（外側の環は宮城県の行の矩形を時計回りに書いたもの、穴は矩形の中央の 1 辺 0.02 度の正方形を反時計回りに書いたもの）に替えて一時の ZIP にし、`load_n03_features` で読む | `build_regions` | 60 フィーチャ。1 つ目は `assoc` `JA`・`area_code` `AC`、最後は `JA8`・`TC`。根室振興局の地域は 8 つのポリゴンの `MultiPolygon`。愛知県は 1 つの `Polygon`（2 つの矩形が合わさる）で、外側の環が反時計回り（`shapely.LinearRing(<環>).is_ccw` が真）。宮城県は穴を 1 つ持つ `Polygon` で、外側が反時計回り、穴が時計回り。`properties` のキーの順は `assoc`・`area_code`・`region_name` |
| `UT-preprocess_boundaries-17` | 市区町村をまとめる | 同じプロセス。小さな N03 の 1 つ目のフィーチャ（愛知県）の `N03_004` を `札幌市`・`N03_005` を `中央区` にし、2 つ目の `N03_005` を `""` にし、3 つ目の矩形の環を時計回りの順（`[[w, s], [w, n], [e, n], [e, s], [w, s]]`）にして読む | `build_municipalities` | 66 フィーチャで `code` の昇順（最初は `01695`、最後は `90059`）。`01695` は 2 つのポリゴンの `MultiPolygon`。どのフィーチャも幾何の種類が `MultiPolygon`。`90000` の `municipality` は `札幌市中央区`、`90001` は `市01`。`90002` の座標は時計回りのまま、入力と同じ値の並び。`properties` のキーの順は `prefecture`・`municipality`・`code` |
| `UT-preprocess_boundaries-18` | 出力が入力の並びによらない | 同じプロセス。小さな N03 から (a) そのまま、(b) フィーチャの並びを逆にし、`01695` の 2 つのフィーチャの順も入れ替えたもの、の 2 つの一時の ZIP を別の `<data_dir>` に作り、それぞれ読んで `build_regions`・`build_municipalities`・`split_nt_polygons`・`list_excluded_tiles`・`list_excluded_meshes`（日本全土は `{'3720', '6747', '6848'}`）・`write_temp_outputs`（`<data_dir>/boundaries`）を呼ぶ | 2 つの一時ファイルの組 | 4 つの一時ファイルのバイト列が、(a) と (b) でそれぞれ等しい |
| `UT-preprocess_boundaries-19` | 北方領土のポリゴンを分ける | 同じプロセス。小さな N03 を読む | `split_nt_polygons` | 1 つ目は 7 つのポリゴン、2 つ目は 60 のポリゴン |
| `UT-preprocess_boundaries-20` | タイル番号 → 緯度経度 | 同じプロセス | [2.4](#24-言語ごとに別に実装する式のテストベクトル) の表 3 の各行 | 経度は `==` で等しく、緯度は差の絶対値が `1e-12` 以下 |
| `UT-preprocess_boundaries-21` | 除外タイル | 同じプロセス。`(n0, w0) = tile_to_latlon(29127, 12867, 15)`、`(s0, e0) = tile_to_latlon(29128, 12868, 15)` | `list_excluded_tiles` に (a) `[box(w0, s0, e0, n0)]`（タイル 1 枚ちょうど）、(b) そのタイルの中の小さな矩形（`w0` と `e0` の間の 1/4〜3/4、`s0` と `n0` の間の 1/4〜3/4）、(c) 西の端が `w0 + (e0 − w0) × 0.5`、東の端が `e0 + (e0 − w0) × 0.5` で、南北は (b) と同じ矩形、(d) (a) と (b) の 2 つ | (a) `[(29127, 12867)]`（接するだけの隣のタイルを含まない）、(b) `[(29127, 12867)]`、(c) `[(29127, 12867), (29128, 12867)]`、(d) `[(29127, 12867)]`（重なりは 1 つ） |
| `UT-preprocess_boundaries-22` | 除外メッシュ | 同じプロセス。北方領土の矩形 `P = box(148.1, 45.5, 148.15, 45.55)`（`6848` の中） | `list_excluded_meshes` に (a) 日本全土 `{'6848', '6747', '3720'}`、`[P]`、`[box(147.5, 44.8, 147.6, 44.9)]`、(b) 日本全土 `{'6848'}`、`[P]`、`[box(148.5, 45.5, 148.6, 45.6)]`（`6848` の中のほかの陸地）、(c) 日本全土 `{'6848', '6849'}`、`[box(148.9, 45.5, 149.0, 45.6)]`（東の辺が `6849` との境目に乗る）、`[]`、(d) 日本全土 `{'6848'}`、`[P]`、`[box(147.9, 45.5, 148.0, 45.6)]`（西で `6848` の境目に接するだけ） | (a) `['6848']`、(b) `[]`、(c) `['6848']`（`6849` は接するだけ）、(d) `['6848']` |
| `UT-preprocess_boundaries-23` | 一時ファイルの書き方 | 同じプロセス。(a)(b) は `<tmp>/b/` を作らない。(b) は `<tmp>/b/nt_excluded_meshes.txt.tmp` を前の起動の残りとして置く。(c) は `<tmp>/b/` に 4 つの出力（中身 `old`）と `n03_version.txt`（`20240101\n`）を置き、`<tmp>/data/tiles/fetch_complete.txt` も置く | (a) `write_temp_outputs([], [], [(1, 2), (3, 4)], ['6848'], '<tmp>/b')`、(b) `<tmp>/b/nt_excluded_meshes.txt.tmp` に `old` を書いてから `write_temp_outputs([<地域のフィーチャ 1 つ〈properties は assoc JA・area_code TK・region_name 東京都、幾何は box(0, 0, 1, 1) の mapping〉>], [], [], [], '<tmp>/b')`、(c) `write_temp_outputs([], [], [], [], '<tmp>/b')` | (a) 返り値は `<tmp>/b/regions.geojson.tmp` など 4 つのパス（`_OUTPUT_NAMES` の順）、`<tmp>/b` が作られる、`regions.geojson.tmp` と `municipalities.geojson.tmp` は `{"type":"FeatureCollection","features":[]}\n`、タイルは `1 2\n3 4\n`、メッシュは `6848\n`。(b) `regions.geojson.tmp` は `{"type":"FeatureCollection","features":[{"type":"Feature","properties":{"assoc":"JA","area_code":"TK","region_name":"東京都"},"geometry":{"type":"Polygon","coordinates":[[[1.0,0.0],[1.0,1.0],[0.0,1.0],[0.0,0.0],[1.0,0.0]]]}}]}\n` の UTF-8（`東京都` はエスケープしない）、メッシュの一時ファイルは空（`old` が残らない）。(c) 4 つの一時ファイルができ、4 つの出力（`old`）と版の記録（`20240101\n`）と取得完了の記録のバイト列は呼ぶ前と同じ（置き換えない） |
| `UT-preprocess_boundaries-24` | 一時ファイルに書けない | 同じプロセス | (a) `<tmp>/b` を通常のファイルにして `write_temp_outputs([], [], [], [], '<tmp>/b')`、(b) `<tmp>/b/nt_excluded_tiles.txt.tmp` をディレクトリにしてから同じく呼ぶ | どちらも 1、BF3。(a) の `{path}` は `<tmp>/b`。(b) の `{path}` は `<tmp>/b/nt_excluded_tiles.txt.tmp` で、`regions.geojson.tmp`・`municipalities.geojson.tmp` は残っていない |
| `UT-preprocess_boundaries-25` | 置き換えの順と中身 | 同じプロセス。`<tmp>/data/boundaries/` に 4 つの出力（中身 `old`）と `n03_version.txt`（`20240101\n`）、`<tmp>/data/tiles/fetch_complete.txt` を置き、4 つの一時ファイルを `write_temp_outputs([], [], [], [], '<tmp>/data/boundaries')` で作る。`preprocess_boundaries` の中の `os.remove`・`os.replace` を、引数を記録してから元を呼ぶ物に差し替える | `replace_outputs(<一時ファイルのパス>, '<tmp>/data', '20250101')` | 呼ばれた順が、`os.remove(<版の記録>)`、`os.remove(<tmp>/data/tiles/fetch_complete.txt)`、`os.replace` が 4 つの一時ファイルから `_OUTPUT_NAMES` の順の出力へ、`os.replace(<版の記録の一時ファイル>, <版の記録>)`。終わった後、版の記録は `20250101\n`、取得完了の記録は無い、4 つの出力は一時ファイルの中身、`.tmp` で終わるファイルは無い |
| `UT-preprocess_boundaries-26` | 記録が無いとき・置き換えの途中の失敗 | 同じプロセス。25 と同じ置き方 | (a) 版の記録と取得完了の記録を置かずに `replace_outputs`、(b) 差し替えた `os.replace` が 3 回目の呼び出しで `OSError(errno.EACCES, …)` を上げる | (a) 止まらず、版の記録は `20250101\n`。(b) 1、BF4（`{path}` は 3 つ目の出力 `nt_excluded_tiles.txt` の一時ファイル）、版の記録が無い、取得完了の記録が無い |
| `UT-preprocess_boundaries-27` | 初めて作る | 子のプロセス。`<tmp>/data/tiles/fetch_complete.txt` を置く | 引数は既定（作業ディレクトリ `<tmp>/work` から相対パスの `--config ../c.ini`） | 0。`<tmp>/data/boundaries/` に 4 つの出力と `n03_version.txt`（`20250101\n`）。地域 60・市区町村 66 フィーチャ、除外メッシュは `6848\n`、除外タイルは 1 枚以上で各行が `^[0-9]+ [0-9]+$`、`(x, y)` の昇順で重なりが無い。取得完了の記録が無い。`<tmp>/t` は空。`<tmp>/data/findsummits.lock` がある。ログファイルの行は L1、L2（`設定ファイル: <tmp>/c.ini`、`[paths]` の `data_dir` と `log_dir` の 2 行）、BL1、BL2（`作り直す: <tmp>/data/boundaries/regions.geojson が無い`）、BL3（`結果の要約: 作り直した（版 20250101）。地域 60、市区町村 66、除外タイル <タイルの行の数>、除外メッシュ 1`）、L3（終了コード 0）の順。標準出力は同じ文面が時刻なしで同じ順 |
| `UT-preprocess_boundaries-28` | 作り直さない・新しい版の警告 | 子のプロセス。27 の後の `<tmp>/data` に、取得完了の記録を置き直す | (a) 引数は既定、(b) `<tmp>/data/ref/` に一時の ZIP を写した `N03-20260101_GML.zip`（中の名前も `N03-20260101.geojson` に変えたもの）を足して、引数は既定 | どちらも 0、4 つの出力と版の記録のバイト列と更新時刻は 27 の後と同じ、取得完了の記録が残る。(a) のログに BL2 `作り直さない: 出力と版の記録がそろっている（版 20250101）` と BL4 `結果の要約: 作り直さなかった。採用した ZIP の版 20250101、版の記録 20250101`。(b) は標準エラー出力とログに BW1（1 行目の後半は `記録した版 20250101、置いてある最新の版 20260101`、2 行目の `{config_opt}` は空白 1 つと `--config <tmp>/c.ini`）、BL1 の ZIP は `<tmp>/data/ref/N03-20260101_GML.zip`、BL4 の ZIP の版は `20260101` |
| `UT-preprocess_boundaries-29` | `--rebuild` | 子のプロセス。27 の後の `<tmp>/data` に、取得完了の記録を置き直す | `--config ../c.ini --rebuild` | 0、BL2 `作り直す: --rebuild を付けた`、取得完了の記録が無い、版の記録は `20250101\n` |
| `UT-preprocess_boundaries-30` | 検証で止まったときは何も変えない | 子のプロセス。27 の後の `<tmp>/data` に、取得完了の記録を置き直し、一時の ZIP を、13 の (a) の書き換えをした小さな N03 のものに置き換える | `--config ../c.ini --rebuild` | 1、標準エラー出力とログに BV5（2 行目に `{rerun}` が入り、`--config <tmp>/c.ini --rebuild` を含む）、ログの L3 の前の行が BL5 `結果の要約: 途中で止まった。終えた分: なし`。4 つの出力と版の記録と取得完了の記録のバイト列は起動の前と同じ。`<tmp>/t` は空 |
| `UT-preprocess_boundaries-31` | 起動の前の止まり方 | 子のプロセス | (a) `--config ../none.ini`、(b) 別のプロセスが `<tmp>/data/findsummits.lock` に `fcntl.flock` で排他ロックを掛けている間に引数は既定、(c) `<tmp>/src/params/mesh_list_japan.txt` を消して引数は既定、(d) `<tmp>/data/ref/` の ZIP を消して引数は既定 | (a) 2、CF1（`対処:` は `--config に渡したパスを確かめる`）、`<tmp>/data/findsummits.lock` と `<tmp>/logs` が無い。(b) 1、G1、`<tmp>/logs` が無い。(c) 1、R1（`{path}` は `<tmp>/src/params/mesh_list_japan.txt`）、ログに BL5（`終えた分: なし`）、`<tmp>/data/boundaries/` は作られていない。(d) 1、BZ1（`{ref_dir}` は `<tmp>/data/ref`）、ログに BL5 |
| `UT-preprocess_boundaries-32` | 置き換えに入った後の要約 | 27 の後の `<tmp>/data` で、11 と同じ形の試験用のプログラムを、`json.load` の代わりに `os.replace` を「3 回目の呼び出しでは元の `os.replace` を呼ばずに自分へ `SIGTERM` を送り、ほかの呼び出しでは元を呼ぶ物」に差し替え、`sys.argv` に `--rebuild` を足して起動する | 起動する | 143。ログの BL5 が `結果の要約: 途中で止まった。終えた分: 地域 60、市区町村 66、除外タイル <n>、除外メッシュ 1。出力の置き換えに入った後に止まった（版の記録が消えていれば、次の起動で作り直す）`。版の記録が無い。もう一度、子のプロセスで引数は既定で起動すると 0 で、BL2 が `作り直す: 版の記録が読めないか、8 桁の数字の 1 行でない: <tmp>/data/boundaries/n03_version.txt`（4 つの出力はある） |

- UT の形の理由: 純粋な関数と、`start_log` を呼ばない関数は同じプロセスで呼ぶ。`main` を通すもの（引数・ロック・ログ・要約・シグナル）は子のプロセスで起動する（[2.1.5](#215-ut-候補)・5.2.5 と同じ分け方）。小さな N03 は、DEC37 の「地域が 60 にならなければ止まる」に当たらずに通る最小の入力として、地域ごとに 1 つの矩形と北方領土 6 村の矩形で作る（全国の N03 は大きく、UT の入力にしない。実物は IT の `IT-CMP1-EXT2-01` で読む）。

## 5. CMP3 パイプライン制御

この章は、CMP3（パイプライン制御）の 2 本のプログラム（[HLD 3.3.1](30_HLD.md#331-プログラム)）のモジュールを置く。5.1 `run_pipeline` は bash、5.2 `resolve_config` は Python で書く。`resolve_config` と `run_pipeline` は、起動（`--config <絶対パス>`）、標準出力の 2 行、終了状態だけでつながる（結合のつなぎ目 `CMP3-INT1`。[HLD 3.3.5](30_HLD.md#335-結合のつなぎ目)）。

### 5.1 `run_pipeline`

- **ID**: LLD-run_pipeline
- **対応 HLD**: [3.3](30_HLD.md#33-cmp3-パイプライン制御)・[4.1](30_HLD.md#41-fr-001-標高タイル事前取得)・[4.23](30_HLD.md#423-fr-023-解析パイプライン制御)・[5.6](30_HLD.md#56-nfr-006-可搬性環境)・[5.7](30_HLD.md#57-nfr-007-ログ出力)・[5.11](30_HLD.md#511-nfr-011-手順文書による環境構築成果物生成の完遂性)
- **ファイル**: `scripts/run_pipeline.sh`

処理の正本は[HLD 4.23.2](30_HLD.md#4232-処理の流れ)（順序の正本は[HLD 2.9.3](30_HLD.md#293-同時起動の排他)）で、関数の名前と役割は[HLD 3.3.3](30_HLD.md#333-関数)の表のとおり。この節は、それを bash で書くための細部（変数、コマンド、メッセージの文面、ログの行）だけを足す。[5.6](30_HLD.md#56-nfr-006-可搬性環境)（可搬性）は、Linux のコマンド（util-linux の `flock`、GNU coreutils の `readlink`・`realpath`・`date`、GNU grep、glibc の `iconv`）と `/proc/uptime` を使うので、Linux だけで動くこと（動作の前提の環境は環境定義の Ubuntu）で受ける。[5.11](30_HLD.md#511-nfr-011-手順文書による環境構築成果物生成の完遂性)（手順文書）は、どのメッセージにも `対処:` の行で次の操作を書くことで受ける。[4.1](30_HLD.md#41-fr-001-標高タイル事前取得)は、日本全土1次メッシュコードリストと北方領土除外メッシュリストの読み方（[HLD 4.1.2](30_HLD.md#412-処理の流れ)の 2「入力を読む」）と、取得完了の記録の読み方（[2.3](#23-ファイルの名前と書き方)）で受ける。結合のつなぎ目は `CMP3-INT1`・`CMP3-EXT1`〜`CMP3-EXT6`（[HLD 3.3.5](30_HLD.md#335-結合のつなぎ目)）で、その結合テスト（IT）のケースは `60_IT.md` の `IT-CMP3-INT1-01`〜`04` と `IT-CMP3-EXT1-01`〜`IT-CMP3-EXT6-04` である。

#### 5.1.1 ファイル割付

- 関数と本体はすべて `scripts/run_pipeline.sh` 1 本に置く。1 行目は `#!/usr/bin/env bash`、2 行目は `# trace: LLD-run_pipeline`、3 行目は `set -euo pipefail`。ファイルは実行できる権限で git に入れる（利用者は `scripts/run_pipeline.sh` で起動する。[HLD 2.6.4](30_HLD.md#264-ディレクトリ構成)）。並びは、定数、関数の定義、本体の順。
- UT のコードは `tests/scripts/test_run_pipeline.py` に置き、`scripts/run_pipeline.sh` を子のプロセスで起動して確かめる（[5.1.5](#515-ut-候補)の共通の準備）。各テストに `# trace: UT-run_pipeline-NN` のコメントを付ける。テストの枠組みは[2.1.1](#211-ファイル割付)と同じくテスト方針書 3.4 で選ぶ。Python から子のプロセスで起動する形は、テスト方針書 3.4 が CMP3 の bash のテストのしかたを選ぶまでの暫定で、選んだときはそれに合わせて直す。

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
7. メッセージとログの行は、下の `log_info`・`log_warning`・`log_error` で出す。文面の書き方は[2.2](#22-ログとメッセージの文面)。引数やパスを文面に引用するときは、2.2 の引用の決まりで書く（下の `_quote`）。
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
3. PL7（`終了: <名前> 終了コード <CHILD_RC>`）を `log_info` で出す。

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

書き方は[2.2](#22-ログとメッセージの文面)。ロックとログの場面（G1〜G6。`{config_path}` は `CONFIG_PATH`）は 2.2、`--mesh` とリストの誤り（A1〜A5・R1〜R3）は[2.1.4](#214-メッセージ文面)の文面を、bash でも同じに出す。L1・L3 は 2.2（`{program}` は `run_pipeline`）。`{reason}` は[5.1.3](#513-関数の細部)の規約の 6、`{path}` は絶対パス、`{value}`・`{arg}`・`{args}`・`{output}` は `_quote` で引用した値。G7（捕まらなかった例外）は bash には無い。

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
| FC2 | 取得完了の記録が読めないか、書式が違う | `取得完了の記録が読めないか、書式が違う: {path}: {detail}`（`{detail}` は `{reason}` か `{line_no} 行目が 4 桁の数字でない: {line}`） | `{path} を消してから、venv/bin/python3 scripts/fetch_tiles.py{config_opt} を --mesh なしで起動し直す（--mesh を付けると、記録はそのメッシュだけになる）` | 1 |
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
| PL7 | 内部の起動口の終わり | `終了: {name} 終了コード {rc}` |
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
| `UT-run_pipeline-30` | ログの段と起動口の行 | 一時のソースツリーと一時の設定。`check_cols.rcs` を `3\n0`。`analyze_terrain.say` に `stub-say\n` | 通し | ログファイルに、PL4（`段の始まり: フェーズ2`）、PL5、PL6（`起動: analyze_terrain --config …`）、PL7（`終了: analyze_terrain 終了コード 0`）、…、PL8（`段の終わり: フェーズ2（充足判定の終了コード 3）`）、PL4（`フェーズ3 の N=4`）、…、PL8（`段の終わり: フェーズ4（突合の終了コード 0、ビューア生成の終了コード 0）`）、PL9（`結果の要約: 最後に終えた段: フェーズ4（突合の終了コード 0、ビューア生成の終了コード 0）`）、L3 がこの順にある。スタブが画面に出したもの（`stub-say`）は、標準出力と標準エラー出力にそれぞれ `analyze_terrain` の起動の回数（2 回）だけ出て、ログファイルには無い |
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

1. パスの改行: `data_dir` の値に `'\n'` か `'\r'` があれば RP1（`{key}` は `data_dir`）。`log_dir` は `from_file` が真で、値に `'\n'` か `'\r'` があるときだけ RP1（`{key}` は `log_dir`。デフォルトの `log_dir` は `data_dir` から作るので、`data_dir` の RP1 で足りる）。`configparser` は字下げした次の行を前の行の値の続きとして `'\n'` でつなぐので、値に改行が入りうる。`load_config` は改行を変換して読むので値に `'\r'` は残らないが、読み方に頼らず両方を見る（[HLD 2.3.2](30_HLD.md#232-設定ファイル)の「パスに改行を含む設定は、設定解決が終了コード 2 で拒否する」）。
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
| RP1 | パスに改行がある | `設定のパスに改行がある: [paths] {key}（{path}）` | `[paths] の {key} を 1 行の絶対パスにする（字下げした次の行は、前の行の値の続きとして読まれる）` | 2 |
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
| `UT-resolve_config-07` | パスの改行 | 子のプロセス。ケースごとに別の一時の設定。改行は字下げした次の行で入れる（`data_dir = <tmp>/x` の次の行に、空白 2 つで字下げした `y`） | (i) `data_dir` だけを 2 行にする（`log_dir` は書かない）、(ii) `log_dir` だけを 2 行にする、(iii) `data_dir` と `log_dir` を 2 行にし、`prominence_primary_m = 150` も書く | (i) 2、RP1（`data_dir`）が 1 つだけ。(ii) 2、RP1（`log_dir`）。(iii) 2、RP1（`data_dir`）・RP1（`log_dir`）・CX1 がこの順に出る。どれも標準出力は空 |
| `UT-resolve_config-08` | 引数の誤り | 子のプロセス。一時の設定は `data_dir` だけ | 引数をそれぞれ: (i) なし、(ii) `--config`、(iii) `--config <tmp>/config.ini --extra`、(iv) `--config=<tmp>/config.ini`、(v) `--help`、(vi) `<tmp>/config.ini`、(vii) `--config config.ini`、(viii) `--config ''`、(ix) `--config --config` | どれも 2、標準出力は空。(i)〜(vi) は RA1 で、(i) の 1 行目は `ERROR: resolve_config の引数が違う: （引数なし）`、(v) は `ERROR: resolve_config の引数が違う: --help`。(vii)(viii)(ix) は RA2 で、1 行目は `ERROR: --config のパスが絶対パスでない: config.ini`、`ERROR: --config のパスが絶対パスでない: ''`、`ERROR: --config のパスが絶対パスでない: --config` |
| `UT-resolve_config-09` | 標準出力に書けない | 一時の設定は `data_dir` だけ。共通の準備の `capture_output=True` を使わず（`stdout=` と併せると `ValueError` になる）、`<tmp>/config.ini` を読むだけで開いたもの（`open(<tmp>/config.ini, 'rb')`）を `stdout=` に、`subprocess.PIPE` を `stderr=` に渡して起動する（読むだけの記述子への書き込みは `OSError`〈`EBADF`〉になる） | 引数は既定 | 1（120 でない）、標準エラー出力は RW1 の 2 行だけで、1 行目は `ERROR: 設定解決の結果を標準出力に書けない: <os.strerror(errno.EBADF)>` |
| `UT-resolve_config-10` | 少しずつしか書けないとき・途中で書けなくなったとき | 一時の設定は `data_dir` だけ。子のプロセスを `[sys.executable, '-c', <試験用の短いプログラム>, '--config', <tmp>/config.ini]` で起動し、`capture_output=True` で受ける。試験用のプログラムは、`<ソースツリー>/scripts` を `sys.path` の先頭に入れて `import resolve_config` し、`os.write` を差し替えてから `sys.argv = ['resolve_config.py', '--config', <tmp>/config.ini]` にして `resolve_config.main()` を呼ぶ | (i) 差し替えた `os.write` は、毎回もとの `os.write` で先頭の 5 バイトまでだけを書いてその数を返す。(ii) 1 回目はもとの `os.write` で先頭の 5 バイトだけを書いて 5 を返し、2 回目は `OSError(errno.EPIPE, os.strerror(errno.EPIPE))` を上げる | (i) 0、標準出力は `UT-resolve_config-02` と同じ 2 行の全部。(ii) 1、標準出力は 2 行の UTF-8 の先頭の 5 バイト、標準エラー出力は RW1 の 2 行で、1 行目は `ERROR: 設定解決の結果を標準出力に書けない: <os.strerror(errno.EPIPE)>` |
| `UT-resolve_config-11` | 標準エラー出力が使えないときの終了コード | 子のプロセス。共通の準備の `capture_output=True` を使わず、`os.pipe()` で作ったパイプの読む側を親が閉じ（読む相手のいない標準エラー出力にする）、書く側を `stderr=` に、`subprocess.PIPE` を `stdout=` に渡して起動する（起動した後、親は書く側も閉じる）。一時の設定は入力ごとに別 | (i) 引数なし（RA1）、(ii) `[paths]` の `data_dir = data` だけの設定（CF6。`load_config` の中の誤り）、(iii) `data_dir` と `prominence_primary_m = 150` の設定（CX1） | どれも終了コード 2（120 でない）。標準出力は `b''` |
| `UT-resolve_config-12` | 標準出力も標準エラー出力も書けない | 一時の設定は `data_dir` だけ。`UT-resolve_config-09` の標準出力（`<tmp>/config.ini` を読むだけで開いたもの）と、`UT-resolve_config-11` の標準エラー出力（読む相手のいないパイプ）を組み合わせて起動する（`capture_output=True` は使わない） | 引数は既定 | 終了コード 1（120 でない） |
| `UT-resolve_config-13` | 起動の時点で標準出力が閉じているとき | 子のプロセス。共通の準備の `capture_output=True` を使わず、`stderr=subprocess.PIPE` と `preexec_fn=lambda: os.close(1)` を渡して起動する（子の記述子 1 を閉じたまま Python を起動する）。一時の設定は入力ごとに別 | (i) 引数なし（RA1）、(ii) `data_dir` と `prominence_primary_m = 150` の設定（CX1）、(iii) `data_dir` だけの設定（正しい設定） | (i)(ii) は終了コード 2、(iii) は 1。標準エラー出力は、(i) が RA1 の 2 行だけ、(ii) が CX1 の 2 行だけ、(iii) が RW1 の 2 行だけ（1 行目は `ERROR: 設定解決の結果を標準出力に書けない: <os.strerror(errno.EBADF)>`）で、どれも `Traceback` を含まない |
