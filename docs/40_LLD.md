# findsummits - 詳細設計書 (LLD)

| 項目 | 内容 |
|---|---|
| 作成日 | 2026-10-18 |
| 最終更新日 | 2026-10-18 |
| ステータス | ドラフト |
| 参照 HLD | [`30_HLD.md`](30_HLD.md) |

---

**読み方**: この文書は詳細設計書（LLD）である。概要設計書（HLD）が決めたプログラムと関数の名前、受け取るもの、返すものの上に、関数ごとの細部（型、内部のデータの持ち方、メッセージの文面、ファイルへの割り付け）を足す（書き分けは[文書管理ルール](CLAUDE.md#hld-と-lld-の書き分け)）。LLD の次は実装フェーズ（COD）と単体テスト（UT）で、LLD の字句と上位の文書だけで、コードと単体テストのコードを書ける細かさにすることを目標にする（2026-10-18 に持ち主が決めた）。コードを書く側は、LLD に加えて、ユーザー要件定義書（URD）、ソフトウェア要件仕様書（SRS）、HLD と、関連する文書を読める前提にする。上位の文書に決まっていることは写さずにリンクで指し、どの文書にも決まっていないことをこの文書で決め切る。章立てとモジュールの単位は、アーキテクチャ決定記録（ADR）の [ADR-LLD-001](decisions/ADR-LLD-001-lld-format-module-granularity-and-t2-timing.md) による。今は 2.1 共通部品と、2.1 が使う分の 1 章と 2.2〜2.4 だけを書いてある。ほかのモジュールの節は、書くときに足す。

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

## 1. 用語定義と規約

### 1.1 用語定義

| 用語 | 意味 |
|---|---|
| モジュール | [ADR-LLD-001](decisions/ADR-LLD-001-lld-format-module-granularity-and-t2-timing.md) の Decision 3 の単位。この文書の節 1 つに当たる。 |
| 横断の節 | 2 つ以上のモジュールにかかる決まりを置く節（2.2〜2.4）。追跡の宣言を持たず、モジュールの節から指される。 |
| 部品 | [HLD 3.9](30_HLD.md#39-共通部品) の共通部品の表の 1 行（`load_config` など）。 |
| 起動の部分 | Python のプログラムの `if __name__ == '__main__':` の中。HLD 第 3 章の「引数の解析はプログラムの起動の部分が行い」の部分。 |
| 内部の関数 | モジュールの中だけで呼ぶ関数。名前を `_` で始める。 |

### 1.2 LLD の規約

- 追跡の宣言は、文書管理ルールの[追跡の宣言](CLAUDE.md#追跡の宣言)のとおり、モジュールの見出しの直下に置く。小節は「ファイル割付」「型とデータ」「関数の細部」「メッセージ文面」「UT 候補」の 5 つをこの順に置き、書くことが無い小節も「なし」と理由を書いて残す（ADR-LLD-001 の Decision 2）。
- 横断の節の決まりに従うところは、その節へのリンクで指し、写さない。
- 関数の名前は HLD 第 3 章の名前を使う。LLD が足してよい名前は、内部の関数（`_` で始め、ほかのモジュールから呼ばない）と、型・定数・例外の名前だけ。ほかのモジュールから呼ぶ関数を足すときは、HLD 第 3 章を先に直す（文書管理ルールの[HLD と LLD の書き分け](CLAUDE.md#hld-と-lld-の書き分け)）。
- 型は、そのモジュールの言語の書き方で書く（Python は型ヒント。例 `set[str]`）。
- Python のプログラム（2.1 の内部の関数を除く）は、`sys.exit(<終了コード>)` を `sys` の属性として呼ぶか、最後まで進んで終わる。`raise SystemExit`・`os._exit`・組み込みの `exit()`・`quit()`・`from sys import exit` を書かない。`except BaseException`、裸の `except:`、`SystemExit`・`LogWriteError`・`SignalStop` を捕まえる `except` を書かない（2.1 の `start_log` が `sys.exit` の差し替えで終了コードを記録し、ログの書き込みの失敗とシグナルを `BaseException` の子の例外で伝えるため）。後始末と結果の要約は `finally` で書く（書き方の型は [2.1.3](#213-関数の細部) の前置き）。`os._exit` を呼ぶのは 2.1 の内部の関数 `_finish_log` だけ。
- 2.1 の `start_log`・`log_info`・`log_warning`・`log_error` は、メインのスレッドからだけ呼ぶ（`start_log` はシグナルのハンドラを付けるのに `signal.signal` を使い、これはメインのスレッドでしか呼べない）。ほかのスレッドで動く処理は、知らせたいことをメインのスレッドに返し、メインのスレッドが出す（行が混ざらないようにし、ログの書き込みの失敗とシグナルをメインのスレッドで受けるため）。スレッドを使うかと、シグナルで止まるときにスレッドをどう終えるかは、使うモジュールの節で決める（CMP2（タイル取得）の並列取得の形は [HLD 2.9.1](30_HLD.md#291-目的と範囲) の対象外の行で LLD に送られている）。
- LLD の記号（メッセージの記号など）は、`tools/lint_docs.py` の検査 H（1 文字の記号の残り。`C1`〜`C8`・`D` と数字・`K1`〜`K6`。コード表記の中は検査しない）に当たらない名前にする。2.1 と 2.2 の記号は、設定の誤り CF1〜CF7、`--mesh` の誤り A1〜A5、メッシュのリストの誤り R1〜R3、共通の場面 G1〜G7、ログファイルの行 L1〜L3 である。
- メッセージの文面は、[2.2](#22-ログとメッセージの文面) の書き方で、置き換える部分を `{名前}` で書く。
- UT 候補は、`ID`・確かめること・準備・入力・期待 の 5 列の表で、`UT-<モジュール名>-NN`（2 桁の連番。[テスト方針書 §6](02_test_policy.md#6-テストケースid命名の大枠)）ごとに 1 行で書く。準備には、入力を与える前に整えること（置くファイル、起こすプロセス、差し替えるもの、捕まえる出力）を書く。小節の前置きに名前を付けて書いた共通の準備で足りるときは、その名前を書き、ケースに固有の準備だけを足す。手動のケースは ID の直後に `（手動）` を付ける。単体テスト仕様書（`50_UT.md`）を作るときは、準備はケースの手順へ移る。
- 規則は、実装者が読むその関数の見出し（関数の細部の `#####` の見出し）の下に置く。2 章の横断の節には、2 つ以上のモジュールで共有するものと、どのプログラムにも属さない項目（[ADR-LLD-001](decisions/ADR-LLD-001-lld-format-module-granularity-and-t2-timing.md) の Decision 7。Makefile のターゲット名など）だけを置き、関数の見出しの下からリンクで指す。横断の節にある規則に関数ごとの扱いがあれば、その関数の見出しの下にも書く（実装者は関数の見出しの下を読み、横断の節の段落の奥までは読まないことがあるため）。

## 2. 共通部品と横断

この章は、HLD 3.9 の共通部品のモジュール（2.1）と、HLD の「目的と範囲」の「対象外」の行で繰り返し出る項目を受ける横断の節（2.2〜2.4）を置く。横断の節は追跡の宣言を持たず、モジュールの節から指す（ADR-LLD-001 の Decision 1）。2.2〜2.4 は今は 2.1 が使う項目だけを書き、ほかのモジュールの節を書くときに足す。

### 2.1 共通部品

- **ID**: LLD-common
- **対応 HLD**: [3.9](30_HLD.md#39-共通部品)・[4.1](30_HLD.md#41-fr-001-標高タイル事前取得)・[4.4](30_HLD.md#44-fr-004-33メッシュ結合解析オーケストレーション)・[4.8](30_HLD.md#48-fr-008-per-mesh-csv-統合)・[4.17](30_HLD.md#417-fr-017-n03-行政区域前処理データ準備)・[5.6](30_HLD.md#56-nfr-006-可搬性環境)・[5.7](30_HLD.md#57-nfr-007-ログ出力)・[5.11](30_HLD.md#511-nfr-011-手順文書による環境構築成果物生成の完遂性)
- **ファイル**: `scripts/common.py`

各部品の処理の正本は、[HLD 3.9](30_HLD.md#39-共通部品) の表の「定義のある節」で、この節はそれを Python で書くための細部だけを足す。[5.6](30_HLD.md#56-nfr-006-可搬性環境)（可搬性）は、`fcntl` を使うので POSIX の OS だけで動くことと、ロックは `data_dir` がローカルのファイルシステムにある前提（[HLD 2.9.3](30_HLD.md#293-同時起動の排他)）で受ける。[5.11](30_HLD.md#511-nfr-011-手順文書による環境構築成果物生成の完遂性)（手順文書）は、どのメッセージにも `対処:` の行で次の操作を書くこと（[2.2](#22-ログとメッセージの文面)）で受ける。

#### 2.1.1 ファイル割付

- 部品はすべて `scripts/common.py` 1 本に置く。プログラムは `venv/bin/python3 scripts/<名前>.py` で起動され（HLD 第 3 章）、`scripts/` が import の探索先の先頭になるので、`import common` で読む。
- UT のコードは `tests/scripts/test_common.py` に置く（[HLD 2.6.4](30_HLD.md#264-ディレクトリ構成) の `tests/scripts/`、[DEC18](30_HLD.md#266-設計判断)「テストは対象と同じ名前で分ける」）。テストの枠組みは[テスト方針書 3.4](02_test_policy.md#34-テストを先に書く進め方)で選ぶので、LLD では決めない。UT のコードの各テストには、`# trace: <UT の ID>`（例 `# trace: UT-common-01`）のコメントを付ける（文書管理ルールの[追跡の宣言](CLAUDE.md#追跡の宣言)）。
- `scripts/common.py` の親の親をソースツリーの根とする。既定の設定ファイル `params/config.ini` とその見本 `params/config.ini.example` は、その下にある（[2.1.2](#212-型とデータ)の `_DEFAULT_CONFIG_PATH`・`_EXAMPLE_CONFIG_PATH`）。

#### 2.1.2 型とデータ

- 終了コードの定数（モジュールの最上位の `int`）: `EXIT_OK = 0`・`EXIT_ERROR = 1`・`EXIT_USAGE = 2`・`EXIT_UNRESOLVED = 3`・`EXIT_DEFECT = 4`（[HLD 2.5.1](30_HLD.md#251-終了コード)）。
- ソースツリーのパス（モジュールの最上位の `str`。内部）: `_SOURCE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))`、`_DEFAULT_CONFIG_PATH = os.path.join(_SOURCE_ROOT, 'params', 'config.ini')`、`_EXAMPLE_CONFIG_PATH = os.path.join(_SOURCE_ROOT, 'params', 'config.ini.example')`。
- メッシュコード: `str` で、ASCII の数字 4 字（`re.fullmatch(r'[0-9]{4}', s)` に合うもの）。`int` にしない（`0123` のような 4 桁を書いたとおりに保ち、メッセージにそのまま出すため）。集合は `set[str]`。
- `@dataclass(frozen=True) class ConfigValue`: `value: int | str | None`（`None` は未設定。デフォルトの無いキー〈`user_agent_email`・`sota_geojson_version`〉が、必須でなく、書かれていないとき）、`from_file: bool`（ファイルに書いてあった値なら `True`、デフォルト値か未設定なら `False`）。
- `@dataclass(frozen=True) class Config`: `path: str`（設定ファイルの絶対パス。`os.path.abspath` したもの）、`values: dict[str, ConfigValue]`（キーの名前から値への対応。`load_config` に渡したキーだけ）。キーの名前は節をまたいで重ならない（[HLD 2.3.2](30_HLD.md#232-設定ファイル)の表）ので、キーの名前だけで引く。
- `@dataclass(frozen=True) class StartTime`: `wall: datetime`（`datetime.now().astimezone()`。時差付きのローカル時刻）、`mono: float`（`time.monotonic()`）。`@classmethod def now(cls) -> 'StartTime'` で両方を同時に取る。各プログラムは起動の部分の最初（設定と引数の検査の前。[HLD 5.7.2](30_HLD.md#572-処理の流れ) の 2「ファイルの名前」）に `StartTime.now()` を呼び、`start_log` に渡す。所要時間は `mono` の差で測る（時刻の補正に左右されない時計。[HLD 5.7.1](30_HLD.md#571-目的と範囲) の対象外の行）。
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

  整数の種類は、値が `re.fullmatch(r'[0-9]+', v)` に合い、先頭の `0` を除いた文字列 `d = v.lstrip('0') or '0'` の桁数（`len(d)`）が 18 以下のときだけ `int(d)` にする（`int(v)` にしない。先頭の `0` が 4300 個を超える値で `ValueError` になるため）。符号・小数点・全角の数字・空の値は型に合わず、19 桁以上は範囲の外とする。18 桁までにするのは、Python の `int` への変換の桁数の上限（既定 4300 桁）に掛からないようにし、CMP4（地形解析エンジン）の C++ の実装が 64 ビットの符号付き整数で持てるようにするため。上の表で上限の無い整数のキーの許容範囲の文に `（18 桁まで）` を付けるのはこのため。この上限は SRS の許容範囲にも HLD にも無い実装上のもので、次の HLD の改訂で [HLD 2.3.3](30_HLD.md#233-検証と記録)に足す。値は `configparser` が前後の空白を除いた文字列。空の値（`key =`）はどのキーでも型に合わない誤りで、「書いていない」とは扱わない（未設定にしたいときはキーの行を書かない）。

- モジュールの状態（内部。`_state` という 1 つの `@dataclass` のインスタンス）: `file`（ログファイルの `TextIO` か `None`）、`path`（ログファイルの絶対パスか `None`）、`program: str`、`start: StartTime | None`、`broken: bool`（ログファイルに書けなくなった）、`exit_code: int | None`（記録した終了コード）、`signum: int | None`（受けたシグナル。`_on_signal` の 1 回目で入れる）、`lock_fd: int | None`（ロックファイルの記述子。閉じないために持つ）。

#### 2.1.3 関数の細部

部品ごとに `#####` の見出し（`##### load_config` のように部品の名前だけ）を立てて書く。止まるときは、メッセージを出してから `sys.exit(<定数>)` を呼ぶ（`start_log` の終了コードの記録のため、`raise SystemExit` を書かない）。結果の要約（[HLD 5.7.2](30_HLD.md#572-処理の流れ) の 7「結果の要約」）は部品が止まるときも呼ぶ側が出す。呼ぶ側の書き方の型を、次のコードで示す（中身の要約の文面は各モジュールの節で決める）。`log_info` は、ログファイルに書けなくなった後は何も出さないので（下の `log_info`・`log_warning`・`log_error`）、その場面では要約が出ない（HLD 5.7.2 の 7「結果の要約」の「ログファイルに書けなくなって止まるときは出さない」）。

```python
def main() -> None:
    completed = False
    try:
        ...                     # 処理（部品が sys.exit で止まることもある）
        completed = True
    finally:
        if completed:
            common.log_info('<要約>')
        else:
            common.log_info('<途中で止まったことが分かる要約>')
```

##### load_config

`load_config(config_path: str, keys: Collection[str], required: Collection[str]) -> Config`

1. 次のどれかに当たれば `ValueError`（(i) `keys` に `data_dir` が無い、(ii) `keys` に `log_dir` が無い、(iii) `required` に `data_dir` が無い。呼ぶ側の誤り。利用者の誤りではない。[HLD 3.9](30_HLD.md#39-共通部品)の「`data_dir`・`log_dir` はどのバッチも使うので、どのバッチでも当たる」）。このほか、`keys` に `_CONFIG_KEYS` に無い名前があるとき、`required` に `keys` に無い名前があるときも `ValueError`。
2. `path = os.path.abspath(config_path)`（相対パスは起動した作業ディレクトリが基準。[HLD 2.3.2](30_HLD.md#232-設定ファイル)）。`os.path.isfile(path)` が偽なら CF1 を出して `EXIT_USAGE`。`path` が `_DEFAULT_CONFIG_PATH` と等しいときだけ CF1 の既定の対処にする。
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
4. ここで初めて `_state` に `file`・`path`・`program`・`start` を入れ、次を取り付ける: `sys.exit` を内部の関数 `_exit` に差し替える（`_exit(code=None)` は、`code` が `None` なら 0、`int` ならその値、それ以外なら 1 を `_state.exit_code` に記録してから、元の `sys.exit(code)` を呼ぶ）、`sys.excepthook` を `_excepthook` に、`SIGINT` と `SIGTERM` のハンドラを `_on_signal` にし、`atexit.register(_finish_log)`。
5. 2.2 の L1・L2 の行（始まりと引数、設定ファイル、設定値）を、`_emit` で標準出力とログファイルに出す。書けなければ下の `log_info`・`log_warning`・`log_error` と同じく `LogWriteError`。`argv` は起動の部分が渡す `sys.argv[1:]`（プログラムの名前を含まない）。引数に改行があれば、L1 はその改行で複数の行になる（`_emit` の行の分け方。[2.2](#22-ログとメッセージの文面)の引用の決まり）。

`sys.exit` を差し替える理由: Python の `atexit` の処理からは終了コードが読めない（2026-10-18 に CPython で確かめた）。HLD 3.9 は「プログラムが終わるときに終わりの行を書く」を `start_log` に持たせ、終わりの行には終了コードが要る（[HLD 5.7.2](30_HLD.md#572-処理の流れ) の 4「始まりと終わりの行」）。選ばなかった案: HLD 3.9 に終わりの行を書く部品を足す（確定した HLD の部品を増やすことになる）。各プログラムが終わりの行を書く（HLD 3.9 の「`start_log` が書く」と食い違う）。

##### _finish_log

`_finish_log() -> None`（内部。`atexit` から呼ばれる）

1. まず `SIGINT`・`SIGTERM` を無視にする。`_state.broken` が真なら、終わりの行を書かず（HLD 5.7.2 の 4「始まりと終わりの行」の「ログファイルに書けなくなって止まるときは、終わりの行を書こうとせず」）、標準出力と標準エラー出力を flush して `os._exit(EXIT_ERROR)`（呼ぶ側が規約に反して `LogWriteError` を捕まえて続けても、終了コードを 1 にする。[HLD 5.7.3](30_HLD.md#573-異常系)）。
2. `code = _state.exit_code`、`None` なら 0（`sys.exit` を呼ばずに最後まで進んだとき）。[2.2](#22-ログとメッセージの文面)の L3 の終わりの行を、`_state.file` へ時刻付きで直接書き、flush して閉じる（書く・flush・閉じるのどれかの `OSError` を、次の 3 の「書けなければ」とする。`_emit` は使わない。書き込みの失敗を `LogWriteError` と G5 でなく、次の 3 の G6 にするため）。書けたら、同じ文面を標準出力へ時刻なしで出す（`OSError` は無視する。終わる途中で、止める先が無いため）。
3. 書けなければ（`OSError`）G6 を標準エラー出力にだけ出し、標準出力と標準エラー出力を flush して `os._exit(EXIT_ERROR)`（終了コード 0 などで終わるはずだったときも 1。HLD 5.7.3）。
4. `_state.signum` があれば flush して `os._exit(code)`（Python は捕まらなかった例外で 1 を返すので、128＋シグナルの番号にするため）。それ以外は何もせず戻る（終了コードは Python のとおり）。

`os._exit` を呼ぶと、`start_log` より前に `atexit` に登録された処理（読み込んだライブラリが登録したもの）は動かない。`os._exit` を呼ぶのは、ログに書けなくなったとき、終わりの行を書けなかったとき、シグナルで止まるときだけで、どれもプログラムの成果物の後始末は `finally` で済んでいる。

##### _excepthook

`_excepthook(exc_type, exc, tb) -> None`（内部）

- `SignalStop`: `_state.exit_code = 128 + exc.signum`。メッセージは出さない（終わりの行にシグナルの名前を書く）。
- `LogWriteError`: `_state.exit_code = EXIT_ERROR`。メッセージは書けなくなったときに出してある。
- そのほか: `_state.exit_code = EXIT_ERROR`。2.2 の G7 を `log_error` で出し、続けて `''.join(traceback.format_exception(exc_type, exc, tb))` の末尾の改行を 1 つ除いてから改行で分けた各行（最後に空の行を出さない）を、下の `_emit` で標準エラー出力とログファイルに出す。G7 の `log_error` と Traceback の `_emit` は、別々の `try` で囲み、どちらかで `LogWriteError` が上がったら、その `try` の中で捕まえて次へ進む（G7 の書き込みが失敗しても、Traceback は画面に出る。`broken` は真になっているので、`_finish_log` が 1 で終える）。

##### _emit

`_emit(lines: list[str], stream: TextIO) -> None`（内部）

渡された各行を、画面（`stream`）に先に時刻なしで出し、続けてログファイルに時刻付きで書く。`log_info`・`log_warning`・`log_error`、`start_log` の 5 の L1・L2 の行、`_excepthook` の Traceback の行は、どれもこれで出す。

- 渡された各行の中に改行（`\n`）があれば、`str.split('\n')` でさらに行を分けてから出す（`\r` などのほかの字では分けない。画面には分けた行をそのまま、ログファイルには分けた各行に時刻を付けて書く）。`start_log` の L1 の引数の改行も、この規則で複数の行になる。
- 画面とログファイルへの書き方の細部（flush、出力先の引き方、書けないときの G5 と `LogWriteError`、`broken` の後の扱い）は、下の `log_info`・`log_warning`・`log_error` の「画面」と「ログファイル」の箇条のとおり。

##### _on_signal

`_on_signal(signum: int, frame) -> None`（内部）

`_state.signum` が `None` でなければ何もしない（2 回目から。止まるための `finally` の後始末を途中で切らないため）。1 回目は `_state.signum = signum` を入れてから `raise SignalStop(signum)`。`_excepthook` は `SignalStop` のとき `_state.signum` を入れ直さない。呼ぶ側は `SignalStop` を捕まえず（`except BaseException` を書かない）、`finally` で後始末をする。`start_log` の前に受けたシグナルは Python の既定の扱い（`SIGINT` は 130、`SIGTERM` は 143 で終わる）。

##### log_info・log_warning・log_error

`log_info(message: str) -> None`・`log_warning(what: str, action: str) -> None`・`log_error(what: str, action: str) -> None`

- 出す行: `log_info` は `message` を（改行があれば、改行で分けたそれぞれが 1 行）、`log_warning` は `WARNING: {what}` と `対処: {action}` の 2 行を、`log_error` は `ERROR: {what}` と `対処: {action}` の 2 行を出す（[HLD 2.5.3](30_HLD.md#253-利用者向けのメッセージ)）。HLD 3.9 の表は `log_warning`・`log_error` が「メッセージの内容」を 1 つ受けるとするが、HLD 2.5.3 の 2 行の書式に合わせて `what` と `action` に分ける（HLD 3.9 の表は次の HLD の改訂で直す）。`what`・`action` の中に改行があれば、改行で分けたそれぞれが 1 行で、接頭辞（`WARNING:`・`ERROR:`・`対処:`）は `what` と `action` の最初の行にだけ付け、続きの行には付けない。
- 画面: `log_info` は標準出力、ほかの 2 つは標準エラー出力に、時刻を付けずに出し、そのつど flush。出力先は、呼び出しのたびに `sys.stdout`・`sys.stderr` を引く（import のときに束縛しない。テストが差し替えて確かめるため）。画面への書き込みの失敗（標準出力のパイプ切れなど）は特別扱いしない: `OSError` はそのまま呼ぶ側へ伝わり、捕まらなければ `_excepthook` の G7 で止まる。
- ログファイル: `_state.file` があり `broken` でないときだけ、各行の先頭に `datetime.now().astimezone().isoformat(timespec='seconds')` と空白 1 つを付けて書き、flush（[HLD 5.7.2](30_HLD.md#572-処理の流れ) の 3「行の書式」）。書けなければ（`OSError`）`broken = True` にし、G5 を標準エラー出力にだけ出し、`raise LogWriteError(path) from e`。`broken` の後は、`log_info` は何も出さず（結果の要約を出さないため。HLD 5.7.2 の 7「結果の要約」）、`log_warning`・`log_error` は標準エラー出力にだけ出す。

##### read_mesh_arg

`read_mesh_arg(value: str) -> set[str]`

1. `value == ''` なら A1 で `EXIT_USAGE`。`re.fullmatch(r'[0-9]{4}', value)` なら `{value}` を返す（[HLD 2.4.3](30_HLD.md#243-メッシュ範囲)）。
2. それ以外はファイルのパス。`path = os.path.abspath(value)`。`os.path.exists(path)` が偽なら A2、`open(path, encoding='utf-8-sig', newline='')` で読めなければ（`OSError`・`UnicodeDecodeError`。ディレクトリも含む）A3 で `EXIT_USAGE`。`newline=''` で改行の変換をしないので、CR は行の区切りにならず、下の 3 で前後の空白として除かれる（[HLD 2.4.3](30_HLD.md#243-メッシュ範囲)の「行末の CR を含む」）。
3. 中身を `text.split('\n')` で行に分け、1 から番号を振る。各行の前後から `' '`・`'\t'`・`'\r'` を除き（`line.strip(' \t\r')`。全角の空白は除かない）、空なら飛ばし、`#` で始まれば飛ばす。残りが `[0-9]{4}` に合わなければ、最初に見つけた行で A4 を出して `EXIT_USAGE`。合う行の値を集合に入れる（重なりは 1 つ）。
4. 集合が空なら A5 で `EXIT_USAGE`。空でなければ返す。日本全土リストに無いコードと北方領土除外メッシュは、ここでは誤りにしない（HLD 2.4.3）。

3 の行の読み方（除く空白の字、空行と `#` の行、4 桁の数字の判定、行番号の数え方）は、bash の `run_pipeline` と C++ の CMP4 が同じ決まりで別に実装するときの正本で、それらのモジュールの節はここを指す（[DEC149](30_HLD.md#4234-設計判断)「`--mesh` は bash と Python で別に読む」・[DEC150](30_HLD.md#444-設計判断)「CMP4 は共通部品の決まりを C++ で別に実装する」）。

##### read_mesh_list_file

`read_mesh_list_file(path: str, guidance: str | None) -> set[str]`

- 行の読み方は `read_mesh_arg` の 3 と同じ（同じ内部の関数 `_parse_mesh_lines(text: str) -> tuple[set[str], int | None, str | None]`。返すのは集合と、最初の誤りの行番号とその行の中身）。違うのは止まり方で、`os.path.exists` が偽なら R1、ほかの理由で読めなければ（ディレクトリを含む。`read_mesh_arg` の 2 と同じ判定で、`newline=''` で読む）R2、誤りの行があれば R3 を出して `EXIT_ERROR`（HLD 3.9）。有効な行が 0 のときは誤りにせず空の集合を返す。`path` は呼ぶ側が渡したまま使う（`os.path.abspath` してからメッセージに出す）。
- `guidance` は R1〜R3 の `対処:` の行に入れる案内。`None` のときは既定の対処にする（HLD 3.9 の「案内の無いリストは『なし』」）。

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

`mesh` が `[0-9]{4}` に合わなければ `ValueError`。`aa = int(mesh[:2])`、`bb = int(mesh[2:])`。返すのは `((南端の緯度, 西端の経度), (北端の緯度, 東端の経度))`。式と計算の順は[2.4](#24-言語ごとに別に実装する式のテストベクトル)の決まりのとおり。範囲（3036〜6848）は見ない。

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
- **子のプロセス**: 上に書いた子のプロセスの形で動かす。子に渡す設定ファイルは、親が一時のディレクトリに置く（`data_dir` と `log_dir` を、一時のディレクトリの下の絶対パスで書く）。子の試験用のプログラムは、`StartTime.now()` と `load_config` を呼んでから、入力の列のケースの処理をする。`start_log` は、入力の列が書く位置で 1 回だけ、`start_log(<config の log_dir>, config, '<試験用の名前>', sys.argv[1:], start)` の形で呼ぶ（入力の列が `start_log` の位置を書いていないケースは、ケースの処理の最初に呼ぶ。`UT-common-24` は呼ばない）。

| ID | 確かめること | 準備 | 入力 | 期待 |
|---|---|---|---|---|
| `UT-common-01` | 正しい設定を読む | 同じプロセス。全キーを書いた設定ファイル | 全キーを書いた設定と、全キーの `keys` | 全キーの値が整数か文字列に変わり `from_file` が真 |
| `UT-common-02` | デフォルト | 同じプロセス。`data_dir` だけを書いた設定ファイル | `data_dir` だけの設定と、全キーの `keys` | 任意のキーは HLD 2.3.2 のデフォルトで `from_file` が偽、`log_dir` は `<data_dir>/logs`、`user_agent_email` と `sota_geojson_version` は `None` |
| `UT-common-03` | 設定ファイルが無い | 同じプロセス。存在しない一時のパスを 2 つ作り、一方で `common._DEFAULT_CONFIG_PATH` を差し替える（`params/config.ini` がある環境でも起こせるようにするため） | ほかのパスと、既定のパス（差し替えた `_DEFAULT_CONFIG_PATH` と同じパス） | どちらも 2、CF1 の対処が既定のパスのときだけ `config.ini.example` の案内、ログファイルを作らない |
| `UT-common-04` | 読めない・INI でない | 同じプロセス。4 つの中身をそれぞれ別の設定ファイルに書く（UTF-8 でない中身はバイト列で書く） | UTF-8 でない中身、節の見出しの無いキー、同じキーの重複、同じ節の重複 | どれも 2（CF2・CF3） |
| `UT-common-05` | 知らない節とキー | 同じプロセス。5 つの中身をそれぞれ別の設定ファイルに書き、どれにも `[paths]` の節に `data_dir` を書く。`required` は `data_dir` だけにする（CF7 を混ぜないため） | `[DEFAULT]` の節、`[foo]` の節、`[fetch]` の節に書いた `data_dir` のキー、`[paths]` の節に書いた `Data_Dir` のキー、`keys` に無い節の知らないキー（どのケースも、`keys` には `data_dir` と `log_dir` を入れる） | どれも 2（CF4・CF5）。`keys` に無くても見つける |
| `UT-common-06` | 整数のキーの境目 | 同じプロセス。値ごとに別の設定ファイル（どれも `data_dir` を書く） | 各キーの許容範囲の端とその外（`prominence_primary_m` に `99`/`100`、`prominence_final_m` に `149`/`150`/`151`、`activation_zone_drop_m` に `24`/`25`/`26`、`delete_zone_max_drop_m` に `199`/`200`/`300`/`301`、`max_parallel` に `0`/`1`/`16`/`17`、`interval_ms` に `0`/`5000`/`5001`、`sota_geojson_version` に `0`/`1`、`unmatched_summit_threshold` に `0`）と、`max_parallel` に書き方の違い（`+5`・`1.5`・全角の数字の `10`〈コードポイント U+FF11 と U+FF10〉・`-1`・空の値） | 端の内は読める、外と書き方の違いは 2（CF6）、`{value}` は書いたまま |
| `UT-common-07` | 英字とメールのキー | 同じプロセス。値ごとに別の設定ファイル（どれも `data_dir` を書く） | `provisional_code_max_prefix` に `A`・`Z`・`a`・`AA`・空、`user_agent_email` に `a@b.example`・`nomail`・`a b@c`・`a(b)@c`・空 | `provisional_code_max_prefix` は `A`・`Z` だけ、`user_agent_email` は `a@b.example` だけ読める |
| `UT-common-08` | 必須とキーの絞り込み | 同じプロセス。2 つの設定ファイル | `user_agent_email` を `required` に入れて書かない設定、`keys` に無い `max_parallel = 99` | 前者は 2（CF7）、後者は誤りにしない |
| `UT-common-09` | 誤りをまとめて出す | 同じプロセス。1 つの設定ファイル | CF5・CF6・CF7 が 1 つずつある設定 | 標準エラー出力に 3 つのメッセージが CF5・CF6・CF7 の順に出て、終了コード 2 が 1 回 |
| `UT-common-10` | 絶対パスでない | 同じプロセス。1 つの設定ファイルに 2 つのキーを書く | `data_dir = data`、`log_dir = logs` | 2（CF6、範囲の文は `絶対パス`） |
| `UT-common-11` | 呼ぶ側の誤り | 同じプロセス。`data_dir` と `log_dir` を書いた正しい設定ファイル | `keys` に `data_dir` が無い、`keys` に表に無い名前 | `ValueError` |
| `UT-common-12` | `--mesh` の値を読む | 同じプロセス。ファイルは一時のディレクトリに作る。相対パスのケースは、作業ディレクトリをその一時のディレクトリに移してから呼ぶ | `5339`、`0123`、空白と CR と空行と `#` の行と重複を含むファイル、相対パス | `{'5339'}`、`{'0123'}`、重なりを除いた集合、作業ディレクトリ基準で読む |
| `UT-common-13` | `--mesh` の誤り | 同じプロセス。ファイルとディレクトリは一時のディレクトリに作る | 空の値、無いファイル、ディレクトリ、2 行目と 4 行目が誤りのファイル、全角の数字の `5339`（コードポイント U+FF15、U+FF13、U+FF13、U+FF19）の行、有効な行が無いファイル、`533` | どれも 2。誤りの行は最初の 2 行目を示す（A1〜A5）。`533` はパスとして読む |
| `UT-common-14` | リストを読む | 同じプロセス。ファイルとディレクトリは一時のディレクトリに作る。案内ありは `guidance` に文字列、案内なしは `None` | 正しいリスト、空のファイル、無いファイル（案内あり・なし）、誤りの行、ディレクトリ | 集合、空の集合、1 と R1 の対処（案内か既定）、1 と R3、1 と R2 |
| `UT-common-15` | `start_log` の前の出し先 | 同じプロセス（`start_log` を呼ばない） | `log_info`・`log_warning`・`log_error` | 標準出力か標準エラー出力にだけ出て、`WARNING:`・`ERROR:` と `対処:` の 2 行、時刻なし |
| `UT-common-16` | ログファイルの始まり | 子のプロセス | 子のプロセスで `start_log` を呼び、その後に `log_info` を呼ぶ | `log_dir` を作る、名前が `<program>_<YYYYMMDDTHHMMSS>_<pid>.log`、L1・L2 の行、後の行の先頭に時刻と空白 1 つ（正規表現 `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}` と空白）、標準出力に L1・L2 の行が時刻なしで先に出る、画面の行には時刻なし、2 行のメッセージは各行に時刻 |
| `UT-common-17` | 終わりの行 | 子のプロセス（3 つの子を別々に） | 子のプロセスで `start_log` の後に `sys.exit(0)`・`sys.exit(3)`・`sys.exit` を呼ばずに終わる | 終了コード 0・3・0、ログファイルの最後の行が L3 で同じ終了コード、標準出力の最後の行も同じ文面の L3（行頭の時刻なし）、所要時間が 0 以上で小数 3 桁 |
| `UT-common-18` | 捕まらなかった例外 | 子のプロセス | 子のプロセスで `start_log` の後に `raise RuntimeError('x')` | 終了コード 1、G7 と Traceback が標準エラー出力とログに出る、終わりの行は 1 |
| `UT-common-19` | シグナル | 子のプロセス（`SIGTERM` の子と `SIGINT` の子を別々に。シグナルは `os.kill(os.getpid(), <シグナル>)` で送る） | 子のプロセスで `start_log` の後に自分へ `SIGTERM` を送る子と、`SIGINT` を送る子を別々に動かす（1 つの子に 2 つ送るケースは書かない。最初の 1 つで止まるため。2 回目のシグナルは `UT-common-31` で確かめる）。どちらも `try`/`finally` の中で送り、`finally` で標準出力に `CLEANUP` と書く | 終了コード 143・130、標準出力に `CLEANUP` が出る、終わりの行に `SIGTERM`・`SIGINT` |
| `UT-common-20` | 同じ名前のログファイル | 子のプロセス。子の試験用のプログラムの中で、`start_log` を呼ぶ前に、同じ `StartTime` と自分の PID（`os.getpid()`）から 2.1.3 の `start_log` の 3 の名前を作り、`os.makedirs(<log_dir>, exist_ok=True)` で `log_dir` を作ってから、その下にそのファイルを置く（親は子の PID を起動の前に知れないため） | 子の中で同じ名前のファイルを置いた後に `start_log` | 1、G4、置いたファイルは変わらない |
| `UT-common-21` | ログの出力先を用意できない | 子のプロセス。`log_dir` のパスに通常のファイルを置く | `log_dir` がファイル | 1、G3 が標準エラー出力だけに出る |
| `UT-common-22` | ログファイルに書けなくなった | 子のプロセス。書き込みの失敗は前置きの差し替え（`start_log` の後に `common._state.file` を差し替える） | 子のプロセスで、開いた後の書き込みを失敗させて `log_info('x')` を呼ぶ。(a) そのまま、(b) `try`/`except Exception` で囲んで、`except` の中で標準出力に `CAUGHT` と書いてから `sys.exit(0)`、(c) `try` の中の `log_info('x')` で書き込みが失敗し、`finally` の中の 2 つ目の `log_info('要約')` で要約を出す形 | どれも終了コード 1、G5 が標準エラー出力に 1 回出る、ログファイルに終わりの行が無い。(b) の `except Exception` は `LogWriteError` を捕まえない（標準出力に `CAUGHT` が出ない）。(c) の標準出力は L1・L2 の行と 1 つ目の `x` だけで、2 つ目の `log_info` の要約は出ない（`x` は、書き込みの失敗の前に画面へ出る） |
| `UT-common-23` | 終わりの行だけ書けなかった | 子のプロセス。前置きの `atexit.register` による差し替えで、`_state.file` を、`write`・`flush`・`close` のどれか 1 つだけが `OSError(errno.ENOSPC)` を上げる物にする（3 つを別々の子で） | 終わりの行の書き込み・flush・close のどれか 1 つだけを失敗させ、`sys.exit(0)` | 終了コード 1、G6 が標準エラー出力に出る |
| `UT-common-24` | ロック | 子のプロセス 2 つ（どちらも `start_log` を呼ばない）。1 つ目は `acquire_lock` の後、標準出力に 1 行（例 `LOCKED`）を書いて flush し、親が標準入力を閉じるまで待つ。親はその 1 行を読んでから 2 つ目を起こす。無い `data_dir` は、存在しないパスを `data_dir` に書いた設定ファイル | 1 つ目の子のプロセスがロックを持つ間に 2 つ目、無い `data_dir` | 2 つ目は 1 で G1（ロックファイルのパスを含む）、`data_dir` の下に `*.log` を作らない。無い `data_dir` は 1 で G2。終わってもロックファイルが残る |
| `UT-common-25` | 取得完了の記録のパス | 同じプロセス。なし | `/d` | `/d/tiles/<2.3 の取得完了の記録の名前>` |
| `UT-common-26` | 終了コードの定数 | 同じプロセス。なし | — | 0・1・2・3・4 |
| `UT-common-27` | メッシュ → 緯度経度 | 同じプロセス。なし | 2.4 の表 1 の行 | 期待の値と `==` で等しい |
| `UT-common-28` | 緯度経度 → タイル | 同じプロセス。なし | 2.4 の表 2 の行 | 期待の値と等しい |
| `UT-common-29` | メッシュコードの誤り | 同じプロセス。なし | `533`、`53a9` | `ValueError` |
| `UT-common-30` | 書けない字と長い数 | 同じプロセス。値ごとに別の設定ファイル（NUL を含む中身はバイト列で書く） | 値ごとに別の設定ファイルを使う（同じキーを 2 回書くと CF3 になるため）。(i) `[\x00]` という節を足した設定、(ii) `[paths]` の `data_dir` の値の末尾に NUL を入れた設定、(iii) `max_parallel` に 19 桁の数、`unmatched_summit_threshold` に次の (iv)〜(vii) をそれぞれ別の設定ファイルで、(iv) 先頭の 0 を除いて 18 桁の数、(v) 19 桁の数、(vi) 4301 桁の数、(vii) `0` を 4300 個並べた後に `1` の値 | (i)(ii) は 2（CF3）、(iii)(v)(vi) は 2（CF6）、(iv) は読める、(vii) は `1` として読める |
| `UT-common-31` | 2 回目のシグナル | 子のプロセス | 子のプロセスで `start_log` の後に `SIGTERM` を受け、`finally` の中で自分へもう 1 回 `SIGTERM` を送ってから、標準出力に `MARK` と書く | 標準出力に `MARK` が出る、終了コード 143、終わりの行は 1 つ |
| `UT-common-32` | 始まりの行の引数 | 子のプロセス。引数は `sys.executable`・`-c`・試験用のプログラムの後に並べて子を起こす（子の `sys.argv[1:]` になる） | 子のプロセスで `argv` に `--config`・`/a b`・`it's`・空の引数を渡して `start_log` | ログファイルの最初の行の、時刻と空白の後の文面が `開始: <program> --config '/a b' 'it'"'"'s' ''`（標準出力の最初の行は、時刻なしの同じ文面） |
| `UT-common-33` | 始まりの行の引数の改行 | 子のプロセス。引数は `UT-common-32` と同じく子を起こすときに並べる | 改行を 1 つ含む 1 つの引数（`x` の後に改行、その後に `y`）で `start_log` | ログファイルの最初の 2 行が、時刻と空白の後に `開始: <program> 'x` と `y'`（2 行目にも時刻が付く）、標準出力の最初の 2 行が時刻なしの同じ 2 つの文面 |

### 2.2 ログとメッセージの文面

書式と出し先の正本は[HLD 2.5.3](30_HLD.md#253-利用者向けのメッセージ)と[HLD 5.7.2](30_HLD.md#572-処理の流れ)で、ここは文面と行の形を決める。CMP4（地形解析エンジン）の C++ の `start_log` など、同じ決まりを別の言語で実装するモジュールも、ここの文面と行の形にする。今は 2.1 が使う分だけを書いてある。

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
| G2 | ロックファイルを開けない・ロックを掛けられない | `ロックファイルを開けない: {lock_path}: {reason}` | `設定ファイルの data_dir と、そのディレクトリの書き込みの権限を確かめる` | 1 |
| G3 | ログの出力先を用意できない | `ログの出力先を用意できない: {path}: {reason}`（`{path}` は `log_dir` か、開けなかったログファイル） | `設定ファイル {config_path} の log_dir と、ディレクトリの権限を確かめてから起動し直す` | 1 |
| G4 | 同じ名前のログファイルが既にある | `同じ名前のログファイルが既にある: {path}` | `1 秒以上おいて起動し直す` | 1 |
| G5 | ログファイルに書けなくなった | `ログファイルに書けなくなった: {path}: {reason}` | `ディスクの空きとログファイルの権限を確かめてから起動し直す` | 1 |
| G6 | 終わりの行だけを書けなかった | `ログファイルに終わりの行を書けなかった: {path}: {reason}` | `ディスクの空きとログファイルの権限を確かめる。終了コード 1 はログが欠けたことを示し、書き終えた成果物は消していない` | 1 |
| G7 | 捕まらなかった例外 | `予期しない例外で止まった: {type}: {message}`（`{type}` は例外のクラス名） | `このメッセージと続く Traceback をログファイルから写して開発者に知らせる` | 1 |

設定・引数の誤り（終了コード 2）の文面は、その誤りを確かめる部品か関数の節に置く（2.1 では CF1〜CF7・A1〜A5）。

### 2.3 ファイルの名前と書き方

置き場の正本は HLD（[2.6.4](30_HLD.md#264-ディレクトリ構成)、[2.9.3](30_HLD.md#293-同時起動の排他)、[4.1.2](30_HLD.md#412-処理の流れ)）で、ここは HLD が LLD に送った名前を決める。今は 2.1 が使う分だけを書いてある。

- ロックファイル: `data_dir` の直下の `findsummits.lock`。中身は空のまま使い、消さない（HLD 2.9.3）。Python は `acquire_lock`、bash は `run_pipeline` の `acquire_lock` が同じ名前を使う。
- 取得完了の記録: `data_dir` の `tiles/` の直下の `fetch_complete.txt`（HLD 4.1.2 の「取得完了の記録」）。書式の細部は CMP2 の節で決める。Python は `fetch_record_path`、bash は `run_pipeline` の `fetch_record_path` が同じ名前を使う。

### 2.4 言語ごとに別に実装する式のテストベクトル

HLD の [DEC6](30_HLD.md#225-設計判断決めたこと理由却下した案)「メッシュ・タイル変換の二重実装を許容」のとおり、`mesh_to_latlon`・`latlon_to_tile` を Python（2.1）・C++（CMP4 の「変換」の群）・JavaScript（`index.html` の「3.9 と同じ決まり」の群）で別に実装し、この節の表で一致を確かめる。テストのコードとこの表の置き場とテストのレベルは、テスト方針書で決める（[HLD 2.2.1](30_HLD.md#221-目的と範囲)の対象外の行）。今は `mesh_to_latlon`・`latlon_to_tile` の分だけを書いてある。

計算の決まり（どの言語も IEEE 754 の倍精度で、書いた順に左から計算する。式の正本は用語集の[メッシュコード → 緯度経度](00_GLOSSARY.md#mesh-to-latlon)と[緯度経度 → XYZ タイル番号](00_GLOSSARY.md#latlon-to-tile)）:

- `mesh_to_latlon`: 南端の緯度 = `(2 × aa) / 3`（`2 × aa` を整数で求め、3 で 1 回だけ割る）。北端の緯度 = `(2 × (aa + 1)) / 3`。西端の経度 = `100 + bb`、東端の経度 = `101 + bb`。
- `latlon_to_tile`: `n = 2^z`。`x = floor(((lon + 180) / 360) × n)`。`r = (lat × π) / 180`（`math.radians` のような 1 つの関数にまとめない。掛ける順で値が変わるため）。`y = floor(((1 − ln(tan(r) + 1 / cos(r)) / π) / 2) × n)`。`π` は言語の標準の定数（Python の `math.pi`、C++ の `std::numbers::pi`、JavaScript の `Math.PI`。どれも同じ倍精度の値）。`tan`・`cos`・`ln` は言語の標準のもの。

期待値の導き方: 用語集の式を上の順に倍精度で計算した値で、2026-10-18 に CPython で求めた。`tan`・`cos`・`ln` は言語で最後の桁が違いうるので、表 2 の行は、`floor` の前の値と最も近い整数の差が 0.016 以上ある点か、`floor` の前の値がちょうど整数になる点（経度 −180・0・135）だけにした（日本全土1次メッシュコードリストの 175 メッシュの四隅を、ズーム 14・15 で調べ、経度 135 度のほかは差がどれも 0.016 以上だった）。

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
