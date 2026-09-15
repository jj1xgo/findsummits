# AGENTS.md

このリポジトリの全開発者・開発エージェント向け共通規則の正本。詳細は必要な作業時に下記の公開文書で確認する。

国土地理院の標高タイル（DEM5/DEM10b）を解析し、SOTA 日本支部のサミットリスト更新申請を支援する。
成果物は申請書 XLSX、エビデンス CSV、目視確認用 GeoJSON/HTML ビューア。
要件の正は [URD](docs/10_URD.md)、機能・制約は [SRS](docs/20_SRS.md)、出典は [SOURCES](ref/SOURCES.md)。

## 仕様優先と変更範囲

- 現在のコードはプロトタイプ。URD/SRS/HLD/LLD が目標状態で、コードを正式な仕様として扱わない。
- 仕様を決めてからコードを書く。SRS/HLD/LLD のレビュー中は実装に手を入れない。
- HLD/LLD が未完成の間は、意図的な仕様とコードの乖離を許容する。設計確定後の実装・仕様変更では
  関連文書とコードを同期し、許容する乖離は ADR に記録する。詳細は [開発ガイド](docs/03_development.md)。

## 作業時の必須事項

- 開始時に branch・差分・worktree を確認し、既存の変更を保持する。
- ファイルを編集したら、そのターン内で `make lint` を実行し警告ゼロを確認してから次へ進む。
  新規ファイルは先に `git add` し、`git ls-files` による lint 対象に含める。
- 変更に関係する検証を実行し、[CI 定義](.github/workflows/lint-latest.yml)の対象と実行条件を確認する。再現・回帰確認を優先し、未実行は `not run` と理由を記録する。
  lint 成功とテスト実行・実環境の動作確認を区別する。テストの定義は [テスト方針書](docs/02_test_policy.md)。
- `docs/` または `ref/SOURCES.md` の編集前に [文書管理ルール](docs/CLAUDE.md) を読む。
  採番・書式・ADR・相互参照・更新日の規則に従う。新しいデータソースの追加は用語集と SOURCES の両方を更新する。
- 各ステージの本体成果物が確定し、次ステージの本体ファイルを初めて編集する前に
  [フェーズゲート](docs/03_development.md#4-フェーズゲート)を実施し、承認者の判定を記録する。
- Python の実行・依存変更・lint チェック追加時は [開発ガイド](docs/03_development.md) を読む。
- 完了時は変更内容、実際の検証結果、未解決事項を簡潔に報告する。

## ビルドと検証の入口

```bash
make venv               # Python の固定依存をセットアップ
make                    # build/findsummits をビルド
make test_mesh_analyze  # build/test_mesh_analyze をビルド（実行は別）
make test_analyze       # build/test_analyze をビルド（実行は別）
make lint               # Markdown/Python/GeoJSON/HTML を検証
```

環境・実行例は [README](README.md) と [開発ガイド](docs/03_development.md) を参照。

## リリース

`devel → main` の直接マージは禁止。リリースは `release/*` ブランチを介す。

## 個人運用の補足

このチェックアウトに `.claude/AGENTS.md` が存在する場合は読み、メンテナ個人の課題管理・レビュー・
保存先等の補足として適用する。共通規則を全面的に上書きする正本ではない。
補足は個人運用の手順や制約を追加できるが、共通規則を重複定義・緩和しない。矛盾する場合は公開の共通規則に従う。
存在しない場合も、本ファイルとリンク先の公開文書だけで共通開発規則は成立する。
