# ADR-SRS-045: サミット一覧 XLSX の行集約モデル（geojson クラスタ → サミット行）

| 状態 | 採用・未実装 |
| 決定日 | 2026-06-29 |

## 2026-09-21 追補

1行=1サミットを維持する。AZ 内複数登録は登録ごとの行に同じピーク・コル・解析属性を反復し、AZ 外保留削除候補は自身の登録値・距離と組 ID を保持する。後者の主ピーク情報は同じ review_group_id の AZ 内行で照合する。以下の review=孤立のみ・ピーク属性空欄という初回表をこの範囲で拡張する。
現行の決定は [ADR-SRS-048](ADR-SRS-048-multiple-summits-in-one-az.md)、出力契約は
[FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) を参照。以下は初回決定時の記録。

## 2026-09-21 担当者指定削除の追補

担当者指定削除の改訂一覧は元の孤立サミット行を同じ位置で delete/unmatched 行へ更新し、1 行を維持する。全解析属性・主ピーク情報は空欄、登録値は自身の値とし、両一覧へ review_decision・review_note 列を追加する（バッチは空文字）。詳細は [ADR-SRS-049](ADR-SRS-049-unmatched-manual-delete.md)。

以下は当初の決定記録（既存追補を除く）。

## Context

`merged_summit.geojson` は 5 カテゴリ（add/band_change/no_change/delete/review）のクラスタに
peak/col Point・AZ/delete_zone Polygon・各種サミット Point・LineString を大量に束ねている。

`merged_summit.xlsx`（[FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) バッチ出力）および
`merged_summit_revised.xlsx`（[FR-012](../20_SRS.md#fr-012-サミット一覧申請内容反映版生成) ブラウザ生成）は、
これを**申請の主語（サミット）中心にほどいて 1 行ずつ**カラム化する。

[ADR-SRS-041](ADR-SRS-041-merged-geojson-schema-extension-for-fr012.md) は
「全カラムが `merged_summit.geojson` から生成可能」（スキーマ拡張）を定めたが、
geojson クラスタ → サミット行への非対称なアンフォールド規則（行の単位・各カラムの取得元フィーチャ）が
SRS 未定義だった。本 ADR はその欠落を補完する。

あわせて、現 SRS の `sota_*` 注記「matched・dominant のみ」が
[ADR-SRS-044](ADR-SRS-044-category-property-summit-centric-5class.md) の 5 カテゴリモデルと矛盾している
（dominant ピークは `add`＝新設で既存登録なし、sota_* は空が正）ことが判明したため、本 ADR で統一する。

## Decision

### 基本規則

- **1 行 = 1 サミット**（申請の主語）
- **1 Point = 1 行ではない**: peak Point・col Point・AZ 内 matched サミット Point は同一サミット行に集約する
- **Polygon・LineString は行を生まない**

### カラム群 × category の対応（取得元フィーチャ）

| category | 行の主語 | 行を生むフィーチャ | peak_\* | col_\* | sota_\* | dominant_\* | area_complete | is_band_change_candidate |
|---|---|---|---|---|---|---|---|---|
| add (new) | 新設＝ピーク | peak Point | このピーク | このコル | 空 | 空 | このピーク | 空 |
| add (dominant) | 新設＝ピーク | peak Point | このピーク | このコル | 空 | 空 | このピーク | 空 |
| band_change | 既存サミット | matched peak Point | このピーク | このコル | AZ 内既存サミット | 空 | このピーク | true |
| no_change | 既存サミット | matched peak Point | このピーク | このコル | AZ 内既存サミット | 空 | このピーク | false |
| delete | 削除対象既存サミット | delete summit Point | 空 | 空 | この削除サミット | 主ピーク (code + dist) | 空 | 空 |
| review | 孤立既存サミット | unmatched summit Point | 空 | 空 | この孤立サミット | 空 | 空 | 空 |

### delete 行の詳細

- `peak_*`・`col_*` は空（行内に主ピーク自身の属性を混在させない）
- `sota_*` にこの削除サミット自身の座標・標高を出力する
- `dominant_peak_code`・`dominant_peak_dist_m` で主ピークを参照する
- 主ピークは `matched` / `dominant` のどちらもありうる
  （[ADR-SRS-043](ADR-SRS-043-matched-peak-as-delete-reference.md) 参照）
- 主ピークの座標・標高は delete 行には載らない。主ピーク行を `dominant_peak_code` で辿ることで取得する
- `dominant_peak_dist_m`（主ピーク ↔ 削除候補サミット間の Haversine 距離）は XLSX 単体での
  判定妥当性確認に使う（ビューアなしで delete 申請の根拠を行内で検証できる）

### sota_* の値を持つ category

- `matched`（band_change / no_change）のみ `sota_*` に値を持つ
- `new`・`dominant`（ともに add）は `sota_*` を空とする
  （`dominant` ピークは `add` カテゴリ＝既存登録なし。旧注記「matched・dominant のみ」は誤り）
- `delete`・`review` は `sota_*` に削除 / 孤立サミット自身の値を持つ

## Alternatives

**1 Point = 1 行モデル**（各 Point が独立した行になる）

- peak/col/sota が別行に散り、申請単位（サミット）と行が一致しない
- XLSX を参照する申請担当者が同一クラスタを手動で紐付ける必要が生じる
- 却下

## Consequences

- [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) スキーマ正本（`merged_summit.xlsx` の行生成モデル）に本 ADR の規則を追記する（SRS 更新）
- [FR-012](../20_SRS.md#fr-012-サミット一覧申請内容反映版生成) の「Point フィーチャのみが行に変換される」の文言を本 ADR を参照する記述へ修正する（SRS 更新）
- [FR-012](../20_SRS.md#fr-012-サミット一覧申請内容反映版生成) カラム表の `sota_*` 注記を「matched のみ（band_change/no_change）」へ修正する（SRS 更新）
- 6.2.7（サミット一覧（突合後））の「含む情報」を本 ADR に整合する文言へ修正する（SRS 更新）
- `ADR-SRS-041` の Consequences（「`merged_summit.xlsx` のカラム統一が維持される」）は本 ADR の
  行モデルが前提として成立する（相互補完関係。既存 ADR の本文変更は不要）
- [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定)・[FR-012](../20_SRS.md#fr-012-サミット一覧申請内容反映版生成) の実装は本 ADR の規則に従って行集約を実装する（実装フェーズ）

## 2026-09-21 申請除外の追補

1行=1サミットと行数・行位置を維持し、除外された候補も両一覧へ保持する。application_exclusion・exclusion_note 列を追加し、バッチは空文字、改訂一覧は現在状態の値を転記する。除外によって登録・解析属性や行の生成元を変えない。
詳細は [ADR-SRS-050](ADR-SRS-050-persistent-exclusion-decisions.md) と [FR-019](../20_SRS.md#fr-019-html-ビューア機能仕様) を参照。
