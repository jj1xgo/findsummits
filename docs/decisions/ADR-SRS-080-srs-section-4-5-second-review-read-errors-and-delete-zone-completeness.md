# ADR-SRS-080: SRS §4.5 の 2 回目の見直しで、読めない入力の扱いと delete判定ゾーンの完結の属性を書く

| 項目 | 内容 |
|---|---|
| 状態 | 採用・実装済み |
| 決定日 | 2026-10-12 |

---

## Context

2026-10-12 に、[ADR-SRS-079](ADR-SRS-079-srs-section-4-5-zone-mismatch-and-wording-review.md) で直したソフトウェア要件仕様書（SRS）の §4.5（[FR-008](../20_SRS.md#fr-008-per-mesh-csv-統合)・[FR-018](../20_SRS.md#fr-018-per-mesh-ピーク候補-geojson-統合)・[FR-022](../20_SRS.md#fr-022-コル充足判定)・[FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定)）を、改訂した多視点のレビュー（spec-panel）でもう一度見直した（[#204](https://github.com/jj1xgo/findsummits/issues/204)）。ADR-SRS-079 の直しは新しい食い違いを生んでいなかったが、次の食い違いが残っていた。

1. SOTA 既存サミット GeoJSON について、[FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の入力の表と [§7.2.5](../20_SRS.md#725-sota-既存サミット-geojsongeojson_vn) は、無いときに `summit_name_jp` を空文字にすることだけを書いていた。このデータは 10 個のファイルに分かれている。概要設計書（HLD）は [4.9](../30_HLD.md#49-fr-009-sotaリスト突合match_status-判定) の処理の流れと [DEC99](../30_HLD.md#494-設計判断) で、ファイルの一部が無いか読めないとき、`name` から山岳名を読めない Feature、同じコードに違う山岳名があるコードは使わず、その分を空文字にして警告して続けると決め、ディレクトリごと無いときも警告していた。
2. [FR-008](../20_SRS.md#fr-008-per-mesh-csv-統合)・[FR-018](../20_SRS.md#fr-018-per-mesh-ピーク候補-geojson-統合) の異常系が、読んだ per-mesh ピーク候補 CSV・per-mesh ピーク候補 GeoJSON が読めないか、書式が違うか、1 つのファイルの中で食い違う場合を挙げていなかった。HLD は [4.8](../30_HLD.md#48-fr-008-per-mesh-csv-統合)・[4.18](../30_HLD.md#418-fr-018-per-mesh-ピーク候補-geojson-統合) で、そこで止まると決めていた（CSV の `analysis_id` がファイル名と違う、1 つのファイルに同じピークの行が 2 つ以上ある、1 つの GeoJSON に同じピークの同じ種類のゾーンが 2 つ以上ある、を含む）。システムテスト仕様書（ST）は、その振る舞いを [FR-008](../20_SRS.md#fr-008-per-mesh-csv-統合) の異常系のテストとして持っていた。兄弟の [FR-022](../20_SRS.md#fr-022-コル充足判定)・[FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) は、入力の読み取りエラー（書式の違いを含む）を挙げる。
3. [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の突合済み統合 GeoJSON の delete判定ゾーンの属性表に `area_complete` が無かった。アクティベーションゾーンの表は持ち、不備ゲートは両方の種類のゾーンの `area_complete=false` を検査し、[ADR-SRS-033](ADR-SRS-033-defect-confirmation-via-xlsx.md) は per-feature の `area_complete` を保つとしている。HLD は表にある属性だけを書くので、delete判定ゾーンだけが不完結のとき、調査用の突合済み統合 GeoJSON からその不備を確かめられなかった。

## Decision

1. [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の説明と [§7.2.5](../20_SRS.md#725-sota-既存サミット-geojsongeojson_vn) に、ディレクトリが無いとき、ファイルの一部が無いか読めない（書式の違いを含む）とき、`name` から山岳名を読めない Feature と、同じコードに違う山岳名があるコードは使わず、その分の `summit_name_jp` を空文字にして、警告して続行することを書く。止まる場面（[FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の異常系の入力の誤り）には入れない。
2. [FR-008](../20_SRS.md#fr-008-per-mesh-csv-統合)・[FR-018](../20_SRS.md#fr-018-per-mesh-ピーク候補-geojson-統合) の異常系に、読んだ per-mesh ピーク候補 CSV・per-mesh ピーク候補 GeoJSON の読み取りエラー（書式の違いと、1 つのファイルの中の食い違いを含む）を足す。「読んだ」と限るのは、名前が規則に合わず読まないファイルと、[FR-018](../20_SRS.md#fr-018-per-mesh-ピーク候補-geojson-統合) で `merged_peak.csv` が 0 行のときに読まないファイルを含めないため。
3. delete判定ゾーンの属性表に `area_complete` の行を、アクティベーションゾーンの表と同じ形で足す。サミット一覧の `area_complete` 列をアクティベーションゾーンから取ること（[ADR-SRS-045](ADR-SRS-045-summit-xlsx-row-aggregation-model.md)）は変えない。

要求の中身と範囲は、1 と 2 で HLD が決めた扱いを SRS に書いたこと、3 で突合済み統合 GeoJSON の delete判定ゾーンに `area_complete` を足すことのほかは変えない。

## Alternatives

- **(a) 1 を HLD の設計の詳細として SRS に書かない**: 属性表の「未取得時は空文字」で結果は読めるが、任意の入力が読めないときに止まるか続くかは利用者に見える振る舞いで、兄弟の標高タイル（[ADR-SRS-079](ADR-SRS-079-srs-section-4-5-zone-mismatch-and-wording-review.md)）と同じく SRS に置く。
- **(b) 2 を HLD の設計の詳細として SRS に書かない**: ST が SRS に無い振る舞いを試すことになり、ST から外して結合テストへ移す必要が出る（ADR-SRS-079 の Alternatives (a) と同じ理由で採らない）。

## Consequences

- SRS の [FR-008](../20_SRS.md#fr-008-per-mesh-csv-統合)・[FR-018](../20_SRS.md#fr-018-per-mesh-ピーク候補-geojson-統合)・[FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定)、[§7.2.5](../20_SRS.md#725-sota-既存サミット-geojsongeojson_vn) を直した。1 と 2 ではツールの振る舞いは変わらない（HLD がすでに決めていた扱いを SRS に書いたもの）。3 では、突合済み統合 GeoJSON と、それから作る出力（申請エビデンス ZIP の GeoJSON など）の delete判定ゾーンに属性が 1 つ増える。
- HLD の [DEC99](../30_HLD.md#494-設計判断) は、1 で SRS の字句を変えるもとになったので、HLD の重要の基準（[ADR-HLD-006](ADR-HLD-006-hld-decision-selection-criteria-and-open-item-cleanup.md)）の「上位文書」に当たるようになる。印を付けることは、HLD の追従の見直しで扱う。HLD が突合済み統合 GeoJSON とそれから作る出力の delete判定ゾーンに `area_complete` を書くことと食い違わないかも、そこで確かめる。
- ST は、2 で [FR-008](../20_SRS.md#fr-008-per-mesh-csv-統合) の per-mesh ピーク候補 CSV の読み取りエラーと中の食い違いのケースが SRS に裏付けを持つ。[FR-018](../20_SRS.md#fr-018-per-mesh-ピーク候補-geojson-統合) の per-mesh ピーク候補 GeoJSON の読み取りエラーのケースの有無、1 の場面のケースの有無、3 の属性を出力の確かめに入れるかは、ST の見直しで扱う。
