# AGENTS.md

国土地理院の標高タイル（DEM5/DEM10b）を解析し、SOTA 日本支部のサミットリスト更新申請に必要な成果物（申請書 XLSX・エビデンス CSV・GeoJSON/HTML ビューア）を生成する支援ツール。要件の正は [`docs/10_URD.md`](docs/10_URD.md)。

## 仕様優先原則

現在のコードはプロトタイプであり正式な仕様ではない。URD/SRS/HLD/LLD が目標状態で、コードはその暫定的な副産物。コードと仕様の乖離は意図的かつ正常であり、コードを正にしてはならない。仕様を決めてからコードを書く。

## ビルド・テスト

```bash
make                    # build/findsummits をビルド
make test_mesh_analyze  # build/test_mesh_analyze をビルド
make clean              # build/ ディレクトリごと削除
```

依存: `libpng`, `libm`, `pthread`（GCC / C99）。

## ブランチ運用

`devel → main` の直接マージ禁止。リリースは `release/*` ブランチを介す。push・PR 作成はユーザーの別途指示があるまで行わない。

## 開発運用規範の詳細

このチェックアウトに `.claude/AGENTS.md` が存在する場合は、そちらを開発運用規範の正本として読み、本ファイルより優先して従うこと（課題管理・文書更新・lint 等の詳細ルール）。`.claude/AGENTS.md` はメンテナ個人の運用リポジトリ（非公開）に属し、このリポジトリを fresh clone しただけの環境には存在しない。存在しない場合は、本ファイルと [`README.md`](README.md)・[`docs/`](docs/) 配下の文書に従うこと。
