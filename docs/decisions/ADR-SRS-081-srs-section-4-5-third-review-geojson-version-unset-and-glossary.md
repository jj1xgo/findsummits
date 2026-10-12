# ADR-SRS-081: SRS §4.5 の 3 回目の見直しで、SOTA 既存サミット GeoJSON のバージョン未設定を書き、用語集と表記をそろえる

| 項目 | 内容 |
|---|---|
| 状態 | 採用・実装済み |
| 決定日 | 2026-10-12 |

---

## Context

2026-10-12 に、[ADR-SRS-080](ADR-SRS-080-srs-section-4-5-second-review-read-errors-and-delete-zone-completeness.md) で直したソフトウェア要件仕様書（SRS）の §4.5（[FR-008](../20_SRS.md#fr-008-per-mesh-csv-統合)・[FR-018](../20_SRS.md#fr-018-per-mesh-ピーク候補-geojson-統合)・[FR-022](../20_SRS.md#fr-022-コル充足判定)・[FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定)）を、改訂した多視点のレビュー（spec-panel）で 3 回目として見直した（[#204](https://github.com/jj1xgo/findsummits/issues/204)）。ADR-SRS-080 の直しは新しい食い違いを生んでいなかったが、次の取り残しが見つかった。

1. SOTA 既存サミット GeoJSON の「省略時」が、バージョンの未設定を含むかが SRS から読めなかった。[2.2.1](../20_SRS.md#221-設定可能項目) の設定可能項目「SOTA 既存サミット GeoJSON バージョン」には既定値が無く、[7.2.5](../20_SRS.md#725-sota-既存サミット-geojsongeojson_vn) と [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) は「未存在」「ディレクトリが無いとき」の扱いだけを書いていた。概要設計書（HLD）の [2.3.2](../30_HLD.md#232-設定ファイル) は、未設定のときも `summit_name_jp` を空文字にして続行すると読んでいた。
2. [FR-018](../20_SRS.md#fr-018-per-mesh-ピーク候補-geojson-統合) の説明が、アクティベーションゾーンを英語（activation zone）で書いていた。
3. 用語集の `area_complete` の定義がアクティベーションゾーンだけを対象にしていたが、SRS では両方の種類のゾーンが持つ（[FR-016](../20_SRS.md#fr-016-ピーク域ポリゴン生成)、ADR-SRS-080 で足した [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の delete判定ゾーンの属性表）。
4. 用語集の「仮サミットコード」の定義が `new` だけを書いていたが、SRS の [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) では `new` と `dominant` の両方に付与する（[ADR-URD-007](ADR-URD-007-peak-match-status-terminology.md)）。

## Decision

1. [7.2.5](../20_SRS.md#725-sota-既存サミット-geojsongeojson_vn) の「省略時の動作」と [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の入力の表・説明に、SOTA 既存サミット GeoJSON バージョンが未設定の場合と、そのバージョンのディレクトリが無い場合に、`summit_name_jp` を空文字にして警告して続行することを書き分ける。振る舞いは変わらない（HLD が決めていた扱いを SRS が自分で書く）。
2. [FR-018](../20_SRS.md#fr-018-per-mesh-ピーク候補-geojson-統合) の「activation zone」を「アクティベーションゾーン」に直す。
3. 用語集の `area_complete` を、アクティベーションゾーンと delete判定ゾーンのプロパティとし、詳細は [FR-016](../20_SRS.md#fr-016-ピーク域ポリゴン生成)・[FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) を指す。サミット一覧の `area_complete` 列をアクティベーションゾーン由来とすること（[ADR-SRS-045](ADR-SRS-045-summit-xlsx-row-aggregation-model.md)）は変えない。
4. 用語集の「仮サミットコード」を `new`・`dominant` のピークに付与するものとし、採番の規則は [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) を指す。

要求の中身と範囲は変えない。

## Alternatives

- **(a) 1 を SRS に書かず、バージョン未設定の扱いを HLD の決定として残す**: 振る舞いは同じだが、任意の入力が無いときに続くか止まるかは利用者に見える振る舞いで、ADR-SRS-080 の Alternatives (a) と同じく SRS に置く。

## Consequences

- SRS の [7.2.5](../20_SRS.md#725-sota-既存サミット-geojsongeojson_vn)・[FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定)・[FR-018](../20_SRS.md#fr-018-per-mesh-ピーク候補-geojson-統合) と、用語集を直した。ツールの振る舞いは変わらない。
- HLD の [2.3.2](../30_HLD.md#232-設定ファイル) の「警告を出すことは本節の決定である」は、バージョンが未設定のときの分も SRS の字句の裏付けを持つようになる。HLD の追従の見直しで、その分を SRS に由来する記述に改める（HLD の決定として残す余地は無い）。
- [7.2.5](../20_SRS.md#725-sota-既存サミット-geojsongeojson_vn) はソフトウェア要件仕様書（SRS）の §1〜3・§5〜10 の見直しの範囲にあるので、その範囲の判定を見直す。
