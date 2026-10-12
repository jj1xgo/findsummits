# ADR-SRS-079: SRS §4.5 の見直しで、ゾーンの欠けたピークの異常系を足し、書き方の食い違いを直す

| 項目 | 内容 |
|---|---|
| 状態 | 採用・実装済み |
| 決定日 | 2026-10-12 |

---

## Context

2026-10-12 に、改訂した多視点のレビュー（spec-panel）で、ソフトウェア要件仕様書（SRS）の §4.5（[FR-008](../20_SRS.md#fr-008-per-mesh-csv-統合)・[FR-018](../20_SRS.md#fr-018-per-mesh-ピーク候補-geojson-統合)・[FR-022](../20_SRS.md#fr-022-コル充足判定)・[FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定)）を見直した（[#204](https://github.com/jj1xgo/findsummits/issues/204)）。照らした相手は §6〜8 の台帳と URD である。次の食い違いが見つかった。

1. [FR-018](../20_SRS.md#fr-018-per-mesh-ピーク候補-geojson-統合) は、`area_complete=true` のゾーンが見つからないピークに `area_complete=false` のゾーンをフォールバックとして含めるとだけ書き、アクティベーションゾーンか delete判定ゾーンの一方でも 1 つも見つからないピークの扱いを書いていなかった。概要設計書（HLD）は [4.18](../30_HLD.md#418-fr-018-per-mesh-ピーク候補-geojson-統合) の [DEC78](../30_HLD.md#4184-設計判断) と処理の流れで、どのピークにも 2 つの種類のゾーンが 1 つずつ選ばれていなければ止まると決めていた（per-mesh CSV を書いた後に per-mesh GeoJSON の書き込みで止まったときのように、出力が食い違った状態でだけ起きる）。システムテスト仕様書（ST）は、その振る舞いを [FR-018](../20_SRS.md#fr-018-per-mesh-ピーク候補-geojson-統合) の異常系のテストとして持っていた。
2. [FR-008](../20_SRS.md#fr-008-per-mesh-csv-統合)・[FR-018](../20_SRS.md#fr-018-per-mesh-ピーク候補-geojson-統合) の本文が、§7 と入力の表の名称「1次メッシュコードリスト」ではなく、[ADR-SRS-023](ADR-SRS-023-fr008-merge-input-mesh-list-semantics.md) のときの名称「対象1次メッシュコードリスト」を使っていた。
3. [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の、申請カテゴリ別のフィーチャ構成の表が、`band_change` / `no_change` の行に、親ピークに従属する削除候補サミットの点と線を載せていた。それらの `category` は `delete` で（[ADR-SRS-044](ADR-SRS-044-category-property-summit-centric-5class.md)）、同じ表の `delete` の行にも載っている。[ADR-SRS-043](ADR-SRS-043-matched-peak-as-delete-reference.md) のときの構成の説明が残っていた。
4. [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の入力の表が標高タイル（ローカルキャッシュ）を「必須」としていたが、説明は、PNG が 1 枚も無いか、ディレクトリをたどれないときは `gsi_tile_latest_date` を空文字にして続行するとしていた（[ADR-SRS-073](ADR-SRS-073-align-srs-wording-with-hld-decisions.md)）。
5. [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の異常系が「入力の誤り」とだけ書き、どの入力のどの誤りかを挙げていなかった。兄弟の FR は「存在しない、または読み取りエラー」を挙げる。[HLD 4.9](../30_HLD.md#49-fr-009-sotaリスト突合match_status-判定) は、必須の 3 つの入力が無いか読めないか書式が違うとき、`merged_peak.geojson` のゾーンが `merged_peak.csv` と食い違うとき（表に無いピークのゾーン、同じピークの同じ種類のゾーンが 2 つ以上、ゾーンの欠けたピーク）、N03 前処理済み地域 GeoJSON か N03 前処理済み市区町村 GeoJSON があって読めないか書式が違うときに止まる。
6. [FR-008](../20_SRS.md#fr-008-per-mesh-csv-統合) の `stability` の「`key_col_resolved=false` が 1 件でも含まれる」が、通常モード行だけで数えるのかを書いていなかった。2026-09-24 の見直しで `analysis_count` を通常モード行だけの数に直しており、HLD は同じ母集団で数えている。
7. §4.5 の導入文が、同じ節の [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定)（SOTA サミットリストとの突合）に触れていなかった。
8. [FR-022](../20_SRS.md#fr-022-コル充足判定) の異常系に括弧が 2 つ続く箇所があった。
9. [NFR-003](../20_SRS.md#nfr-003-再現性決定論的出力) が、仮サミットコードは「同一の入力 per-mesh CSV 集合」から同一になると書いていた。2026-09-24 の見直しで、[FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の採番タイミングは `merged_peak.csv`・SOTA サミットリスト CSV・N03 前処理済み地域 GeoJSON を入力に直したが、[NFR-003](../20_SRS.md#nfr-003-再現性決定論的出力) の写しが残っていた。また、仮サミットコードを付けるピーク（new・dominant）は `merged_peak.geojson` のゾーンを使う突合で決まるのに、採番タイミングの入力に `merged_peak.geojson` が無かった。

## Decision

1. [FR-018](../20_SRS.md#fr-018-per-mesh-ピーク候補-geojson-統合) の異常系に、`merged_peak.csv` のピークに、アクティベーションゾーンと delete判定ゾーンのどちらか一方でも 1 つも見つからない場合はエラー終了することを足す。両方の種類のゾーンがあり、ある種類のゾーンが `area_complete=false` のものしか無い場合は、これまでどおりその種類についてフォールバックで続行する。あわせて、[FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の不備ゲートへ渡る場合を書いた項目を、フォールバックで含めた（`area_complete=false` のゾーンしか無い）場合に限る形にそろえる。
2. 2 の名称を「1次メッシュコードリスト」に直す。ADR-SRS-023 の本文は直さない。
3. フィーチャ構成の表の `band_change` / `no_change` の行から従属する削除候補の点と線を外し、`delete` の行に載せることを添える。
4. [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の標高タイルの行を「任意」にし、無いときの扱いは説明の metadata の項を指す（兄弟の [FR-001](../20_SRS.md#fr-001-標高タイル事前取得) の同じ行と同じ形）。
5. [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の異常系に、HLD 4.9 と同じ入力の誤りの中身（ゾーンの食い違いを含む）を挙げる。
6. [FR-008](../20_SRS.md#fr-008-per-mesh-csv-統合) の `stability` で、未確定を数えるのは重複排除前の通常モード行と書く。
7. §4.5 の導入文に、フェーズ4 の突合を足す。
8. 括弧を 1 つにまとめる。
9. [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の採番タイミングの入力に `merged_peak.geojson` を足す。[NFR-003](../20_SRS.md#nfr-003-再現性決定論的出力) は入力を書き写さず、[FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の採番タイミングを指す。

要求の中身と範囲は、1 と 5 で HLD が決めた異常系を SRS に書いたことのほかは変えない。

## Alternatives

- **(a) 1 を HLD の設計の詳細として SRS に書かない**: SRS を直す箇所は減るが、ST が SRS に無い振る舞いを試すことになり、ST から外して結合テストへ移す必要が出る。ゾーンの欠けたまま進むと、[FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の不備ゲートがそのピークの `area_complete` を判定できず突合からも漏れるので、利用者に見える振る舞いとして SRS に置く。
- **(b) 3 で `band_change` / `no_change` の行を残し、`delete` の行から外す**: 山塊のまとまりは見やすいが、表の題「申請カテゴリ別」と per-feature の割り当てルールに反する。

## Consequences

- SRS の §4.5 の導入文、[FR-008](../20_SRS.md#fr-008-per-mesh-csv-統合)・[FR-018](../20_SRS.md#fr-018-per-mesh-ピーク候補-geojson-統合)・[FR-022](../20_SRS.md#fr-022-コル充足判定)・[FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定)、[NFR-003](../20_SRS.md#nfr-003-再現性決定論的出力) を直した。ツールの振る舞いは変わらない（1 と 5 は HLD がすでに決めていた異常系を SRS に書いたもの）。
- HLD の [DEC78](../30_HLD.md#4184-設計判断) は、1 で SRS の字句を変えるもとになったので、HLD の重要の基準（[ADR-HLD-006](ADR-HLD-006-hld-decision-selection-criteria-and-open-item-cleanup.md)）の「上位文書」に当たるようになる（5 のもとになった [DEC87](../30_HLD.md#494-設計判断) には、すでに「上位文書」の印がある）。DEC78 の「アクティベーションゾーンか delete判定ゾーンが 1 つも見つからなければ」は、一方でも欠ければ止まる意味だが、両方とも欠けたときとも読める。印を付けることと字句をそろえることは、HLD の追従の見直しで扱う。
- システムテスト仕様書（ST）の `ST-FR-018-10` は、1 で SRS に裏付けを持つ。5 で挙げた [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の入力の誤りと、ST の [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の異常系のケースとの対応は、ST の見直しで扱う。
