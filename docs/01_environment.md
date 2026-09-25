# 環境定義

| 項目 | 内容 |
|---|---|
| 作成日 | 2026-04-30 |
| 最終更新日 | 2026-09-25 |
| ステータス | ドラフト |

## 目次

1. [動作前提環境](#動作前提環境)
2. [参考: 開発に使っているマシン](#参考-開発に使っているマシン)
3. [Python 環境セットアップ](#python-環境セットアップ)
4. [Python パッケージ（`requirements.txt` で管理）](#python-パッケージrequirementstxt-で管理)
5. [開発環境](#開発環境)

## 動作前提環境

本ツールの最低動作条件（[SRS NFR-006](20_SRS.md#nfr-006-可搬性環境)）。以下をすべて満たす環境を前提とし、
満たさない環境での動作は保証しない。

### ハードウェアと OS

| 項目 | 条件 |
|---|---|
| OS | Linux（x86_64）。動作確認は Debian GNU/Linux testing |
| メモリ | 物理メモリ 62.72 GiB 以上（[NFR-002](20_SRS.md#nfr-002-メモリ使用量)） |
| スワップ | 48 GiB 以上（[NFR-002](20_SRS.md#nfr-002-メモリ使用量)） |
| ディスク | データ置き場に、タイルキャッシュ用として 150 GB 以上の空き（出力分は別）。置き場は `params/config.ini` の `DATA_DIR` で指定する（[README](../README.md)） |
| ネットワーク | 次の段階で HTTPS 接続できること: タイル取得（国土地理院の標高タイル配信サーバー。参照: [SOURCES.md](../ref/SOURCES.md)）、`make venv`（PyPI）、HTML ビューアの利用（背景地図タイル・ライブラリを実行時に取得）。解析・成果物生成のバッチ処理はオフラインで可（[SRS §10](20_SRS.md#10-制約前提条件)） |

ディスクの 150 GB は、全国処理範囲 175 メッシュのタイルキャッシュの見積り（2026-09-25 時点のキャッシュのファイルサイズ合計を
1 次メッシュごとに集計し、1 メッシュあたり最大 DEM5A 0.65 GB・DEM10B 0.18 GB、175 メッシュで約 145 GB。1 GB = 10^9 バイト）。
海域を含むメッシュは小さくなる。解析結果・標高地形図 PNG などの出力は別に要る。
CPU の性能下限は設けない（[ADR-SRS-057](decisions/ADR-SRS-057-no-cpu-floor-in-operating-requirements.md)）。

### ソフトウェア

| 依存 | 用途 |
|---|---|
| GNU make | ビルドと検証の入口（`Makefile`） |
| GCC（C 標準ライブラリのヘッダを含む。Debian では `libc6-dev`） | C 解析エンジン（`src/`）のコンパイラ。動作確認は 16.2 |
| libpng（開発用ヘッダを含む。Debian では `libpng-dev`） | PNG タイルのデコード |
| libm | 数学関数 |
| Python 3.13 以上と `venv` モジュール（Debian では `python3-venv`） | Python スクリプトの実行 |
| bash | `scripts/run_all.sh` の実行 |
| Web ブラウザ（JavaScript 有効） | 作業用 HTML ビューアを `file://` で直接開いて確認・編集とエクスポートを行う（HTTP サーバは不要。[SRS §6.2.5](20_SRS.md#625-作業用-html-ビューア)） |

## 参考: 開発に使っているマシン

動作条件ではない。CPU を条件にしない理由は [ADR-SRS-057](decisions/ADR-SRS-057-no-cpu-floor-in-operating-requirements.md)。
処理時間（[NFR-005](20_SRS.md#nfr-005-処理時間目標)）は CPU に依存するため、比較のために記録する（2026-09-25 時点）。

| 項目 | 値 |
|---|---|
| CPU | AMD Ryzen 7 5700X（8 コア 16 スレッド） |
| メモリ | 62.72 GiB |
| スワップ | 48 GiB |
| データディスク | 457.38 GiB ext4 |
| OS | Debian GNU/Linux testing（x86_64） |

## Python 環境セットアップ

Python スクリプトの実行にはリポジトリ直下の `venv/` を使用する。システムの `python3` は
実行依存が揃うとは限らないため、`venv/bin/python3` で呼び出す。
`git worktree` で作業するときは worktree ごとに `make venv` で作り、本体の `venv/` を共有しない
（[開発ガイド](03_development.md)）。

```bash
make venv          # venv 作成 + 依存パッケージインストール（初回 or requirements.txt 変更時）
```

以降は venv を activate せず、`venv/bin/python3` で直接呼び出す:

```bash
venv/bin/python3 scripts/prefetch_tiles.py ...
venv/bin/python3 scripts/merge.py ...
venv/bin/python3 scripts/preprocess_pref_boundaries.py ...
venv/bin/python3 scripts/output_geojson.py ...
```

## Python パッケージ（`requirements.txt` で管理）

**ランタイム依存**（本番パイプラインと `analysis/` で import するもの。計画分を含む）。版は固定しない:

| パッケージ | 用途 |
|---|---|
| requests | タイル取得（prefetch_tiles.py） |
| openpyxl | XLSX 出力（計画分。申請書 XLSX 出力は未実装で、2026-09-25 時点で import するコードは無い） |
| shapely | 都道府県/振興局 point-in-polygon 判定（merge.py, preprocess_pref_boundaries.py） |
| numpy | `analysis/` の分析スクリプト（Keyコル距離分析など。本番パイプラインでは未使用） |
| pillow | `analysis/` の PNG タイルデコード・画像生成（本番パイプラインでは未使用） |

**開発ツール**（ランタイムで import しない）。版は固定せず、PyPI の最新の安定版に追従する:

| パッケージ | 用途 |
|---|---|
| pymarkdownlnt | Markdown lint（`make lint` → `lint-md`） |
| ruff | Python 静的解析（`make lint` → `lint-py`） |
| geojson-validator | GeoJSON 構造・ジオメトリ検証（`make lint` → `lint-geojson`） |
| djlint | HTML 構文チェック（`make lint` → `lint-html`） |

「最新の安定版」は、venv の Python で pip が既定の候補選択（`--pre` を付けない）で選ぶ版を指す。通常は、プレリリースと取り下げ（yanked）版を除き、
`Requires-Python` が venv の Python に合う最も新しい版になる。Python の版や実行した時期によって、選ばれる版は変わりうる。
pip はその回に入れるツールとその依存だけで版を決めるため、venv のほかのパッケージとの衝突は警告だけで終わることがある。
衝突が気になるときは `venv/bin/python3 -m pip check` で確かめる。

`make venv` は、すでに入っているパッケージの版を上げない（`requirements.txt` を変えて再実行されても同じ）。
`venv/.installed` が `requirements.txt` より新しい間は、`make lint` は PyPI に接続しない。
既存の venv の lint ツールは、次で最新版に上げる（PyPI への接続が要る）:

```bash
make lint-latest       # lint ツールを最新版へ上げ、版を表示してから make lint を実行
```

PyPI に届かないとき、pip は警告を出さずに、導入済みの版のまま成功することもある。終了コードが 0 で警告が無くても、最新版を確認できたとは限らない。表示されるのは導入済みの版である。

新しく作る venv（初回の `make venv`、`make venv-rebuild`、新しい worktree）には、その時点の最新版が入る。
このため venv ごとに lint ツールの版がずれることがある。CI や別の worktree と lint の結果が違うときは、
先に `make lint-latest` で揃える。

版を固定しない代わりに、次を受け入れる:

- ツールの更新で新しい規則が働き、コードを変えていなくても lint が警告を出すことがある。作業の範囲外のファイルに出た警告は、その作業の変更に混ぜず、別の課題として扱う（直すか、規則の設定（`ruff.toml` など）を見直す）。
- 過去の commit を当時と同じ版で lint するには、版を指定して入れ直す（例: `venv/bin/python3 -m pip install ruff==<版>`）。
- geojson-validator は shapely と requests に依存するため、`make lint-latest` でこれらのランタイム依存が上がることがある。

GitHub Actions（`.github/workflows/lint-latest.yml`）が月 1 回と手動実行で `make lint-latest` を実行する。
CI は Python 3.13 の新しい venv で動くため、手元と選ばれる版が異なりうる。schedule は既定ブランチで走る。実行条件は同ファイルを参照。

## 開発環境

動作前提環境に加えて、開発では git を使う。並行作業は `git worktree` で分け、手順は
[開発ガイド](03_development.md) に従う。

コンテナ [c3c](https://github.com/JJ1XGO/c3c) 上でも同じ手順で動く。コンテナで動かすときは、checkout と
データ置き場をマウントし、`params/config.ini` の `DATA_DIR` をコンテナ内のパスにする。
