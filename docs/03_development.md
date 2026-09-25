# 開発ガイド

| 項目 | 内容 |
|---|---|
| 作成日 | 2026-09-15 |
| 最終更新日 | 2026-09-25 |
| ステータス | 確定 |

## 目次

1. [位置づけ](#1-位置づけ)
2. [実行環境と依存管理](#2-実行環境と依存管理)
3. [検証と文書更新](#3-検証と文書更新)
4. [フェーズゲート](#4-フェーズゲート)
5. [バージョンとタグ](#5-バージョンとタグ)

## 1. 位置づけ

[共通開発規則](../AGENTS.md)から、該当作業時に読む詳細手順。特定の CLI や個人設定を前提にしない。
仕様・設計の成果物と採番は [文書管理ルール](CLAUDE.md) に従う。

仕様優先と仕様・実装の同期条件は [AGENTS.md「仕様優先と変更範囲」](../AGENTS.md#仕様優先と変更範囲) に従う。

## 2. 実行環境と依存管理

動作前提環境（最低動作条件）の正本は [01_environment.md](01_environment.md)、初期設定の手順は [README](../README.md) を参照。
Python のセットアップと実行方法は [01_environment.md「Python 環境セットアップ」](01_environment.md#python-環境セットアップ) に従う。
本節は依存変更時の手順を定め、環境構成やバージョンは同文書と `requirements.txt` に一元化する。

```bash
make venv                                  # 初回・requirements.txt 変更時
make test_mesh_analyze                     # テストプログラムのビルド
make test_analyze                          # テストプログラムのビルド
./build/test_mesh_analyze 4929              # キャッシュ等の前提を整えて実行
./build/test_mesh_analyze 4929 --save-image  # 標高地形図 PNG も出力
make clean                                 # build/ を削除
```

- `requirements.txt` を依存の正とする。新しいサードパーティ製パッケージを import したら、同じコミットで
  `requirements.txt` に追記する。`pip install` だけで済ませない。
- パッケージを削除したとき、および定期的な依存整合確認では `make venv-rebuild` で venv をクリーン再構築する。
- コンパイル済み拡張（numpy・shapely・pillow）は `make venv` がビルド済み wheel だけを許可する（`--only-binary`）。
  ソースビルドに落ちると OS の共有ライブラリに依存し、ホストとコンテナの一方でしか動かない venv になるため。
  wheel が無くて失敗したら、ソースビルドでしのがず `requirements.txt` の版を見直す。
- checkout の移動で実行ファイルの shebang が壊れた場合も `make venv-rebuild` で作り直す。
- 並行作業やリリース作業はブランチ切替でなく `git worktree` で checkout を分ける。`venv/`・`build/`・
  `params/config.ini`・`params/fetch_config.ini` は git 管理外のため worktree には無く、worktree ごとに `make venv`・
  `make`・設定ファイルの複製が要る（`DATA_DIR` はリポジトリ外なので複製不要）。ルートの `.worktreeinclude` は
  Claude Code が worktree を作るときに複製する設定ファイルの一覧で、手動の `git worktree add` には効かない。

## 3. 検証と文書更新

編集後の必須検証は [共通開発規則](../AGENTS.md#作業時の必須事項)に従う。
テスト用 make target のビルド成功は、テスト実行の成功ではない。前提データ・環境・実行したコマンドと結果を記録する。

- `make lint` の対象拡張子・使用ツール・設定・除外は `Makefile` を参照。
  新しい機械的チェックは `make lint` の依存 target に追加し、指示ファイルに別コマンドの必須規則を増やさない。
- lint ツールの構成・固定版と最新版の検証方法は
  [01_environment.md「Python パッケージ」](01_environment.md#python-パッケージrequirementstxt-で管理) に従う。
- docs の表記揺れをレビューで同種のものについて2回以上修正した場合、機械化できる規則は
  `scripts/lint_docs.py` の検査E規則テーブルに追加する。1回限りの揺れは追加不要。
- 文書の詳細規則は [docs/CLAUDE.md](CLAUDE.md) に一元化する。文書を編集した日はヘッダーの最終更新日も更新する。

## 4. フェーズゲート

ステージ本体成果物の確定後、次ステージの本体ファイルへの最初の編集前に工程完了審査を行う。
ステージと成果物の定義は [文書管理ルール](CLAUDE.md#各ステージの成果物) を参照する。
作業者が資料・観点を整理し、承認者（メンテナ）が最終判定する。

以下の6観点をすべて記録する:

1. **成果物品質**: レビュー収束・確定状況（レビュー対象の全項目完了、ステータス「確定」、lint 警告ゼロ）。
2. **未解決課題の処置**: 当該ステージの未解決課題・既知乖離の棚卸しと処置。持ち越し理由を明記する。
3. **次ステージ準備**: 入力成果物・次工程の作業項目・関連課題の紐づけの整備状況。
4. **体制**: 要員・経験値のリスク評価と軽減策。
5. **リスク管理**: リスク台帳・コンティンジェンシープランの整備状況。見送る場合も理由を記録する。
6. **総合判定**: 上記を踏まえた Go / 条件付きGo / No-Go の判定。

| 判定 | 次ステージへの移行 |
|---|---|
| Go | 進んでよい |
| 条件付きGo | 着手可能。明記した条件を次ゲートまでに消化する |
| No-Go | 当該ステージへ差し戻し、条件解消後に再審査する |

記録には対象版・実施日・6観点・判定者・条件を含め、レビュー参加者が確認できる課題または文書に保存する。
確定した記録を書き換えず、補足・訂正は追記する。個人の台帳やツールがなくても同じ審査基準を適用する。

## 5. バージョンとタグ

正本は git の annotated tag。`VERSION` ファイルや文書内の番号表は作らない。

- 採番規則の要約: 正式リリース前は `v0.x.y`。x は SRS §6 の外部 I/F・§2.2.1 の設定項目・CLI 引数の
  非追加的変更か新 FR の実装で上げ、y はそれ以外。`1.0.0` の到達条件と互換性保証対象、詳細な採番規則は
  [ADR-OPS-001](decisions/ADR-OPS-001-semver-tagging-and-release-versioning.md) を参照。
- 手順: `release/*` → main をマージした後、main のマージコミットで `git tag -a vX.Y.Z -m "<要約>"` を打ち、
  タグを push する（リリース担当者が行う）。
- 成果物への埋め込み: `git describe --tags --dirty` の文字列を `software_version` として付与
  （[SRS FR-009](20_SRS.md#fr-009-sotaリスト突合match_status-判定) 参照）。devel からの生成物は
  `-N-g<hash>` 接尾辞で区別される。
