# ADR-SRS-073: SRS・用語集・ADR の字句を HLD の第 4 章までの決定に合わせる

| 項目 | 内容 |
|---|---|
| 状態 | 採用・実装済み |
| 決定日 | 2026-10-09 |

## Context

概要設計書（HLD）の各節は、ソフトウェア要件仕様書（SRS）が HLD に委ねたことを決めてきた。その中で、SRS・用語集・既存の ADR の字句を追い越した決定が、HLD の各節の「未決事項と後続」に改訂の候補として積まれていた。台帳（SRS §8.1）の参照 FR の漏れも、HLD の spec-panel の逆引きで見つかった。HLD の決定が先にあり、上位の文書の字句が食い違ったまま詳細設計（LLD）に進むと、LLD が二つの文書の間で迷う。そこで 2026-10-09 に持ち主が、フェーズゲート（HLD → LLD）の前に、HLD の第 4 章を書き終えた区切りで 1 回で直すと決めた。

## Decision

1. **方針**: HLD の決定を正とし、SRS・用語集・既存の ADR の字句を同じ意味に直す。HLD の決定そのものは変えない。
2. **直した項目**: 次の表のとおり。
3. **既存の ADR**: Decision と Consequences の本文は書き換えず、状態と決定日の表の直後に注を置き、改めた決定や字句と新しい読みを示す（[ADR-SRS-015](ADR-SRS-015-contour-overlay.md) と同じ形）。
4. **HLD の記録**: HLD の D の理由などに残る、食い違いを現在形で書いた文は、決定の時点の記録として残し、文の末尾に本 ADR で直したことを添える。
5. **範囲の外**: 試験仕様（ST）の改訂候補は、この改訂に含めず、別に追う。

| 直した文書と箇所 | 合わせた HLD の決定 |
|---|---|
| [FR-014](../20_SRS.md#fr-014-広域結合解析オーケストレーション) の入力の表に、同じ起動で書き終えた per-mesh CSV の読み戻しを足し、§8.1 の No.8 の参照 FR に [FR-014](../20_SRS.md#fr-014-広域結合解析オーケストレーション) を足した | [HLD 4.14](../30_HLD.md#414-fr-014-広域結合解析オーケストレーション)（D56「早期終了は書き終えた per-mesh CSV で判定する」） |
| [FR-001](../20_SRS.md#fr-001-標高タイル事前取得) の入力の表に、標高タイル（ローカルキャッシュ）を任意の入力として足した（§8.1 の No.5 には [FR-001](../20_SRS.md#fr-001-標高タイル事前取得) があった） | [HLD 4.1](../30_HLD.md#41-fr-001-標高タイル事前取得)（C2 が `If-Modified-Since` に mtime を入れて要求する） |
| [FR-011](../20_SRS.md#fr-011-申請書-xlsx-生成) の注 ※1 を、山岳名 JP の未入力だけを警告し、山岳名 EN は警告しない意味に直した | [HLD 4.19](../30_HLD.md#419-fr-019-html-ビューア機能仕様)（警告の表）、ADR-SRS-036 |
| [FR-020](../20_SRS.md#fr-020-公開用ビューア配信) の出力、§3・§6.1 の配信物の形式、§6.2.7 に、版の区分を示す `site.json` を足した | [HLD 4.20](../30_HLD.md#420-fr-020-公開用ビューア配信)（D166「版の区分は組み立てが書くファイルで示す」） |
| [FR-020](../20_SRS.md#fr-020-公開用ビューア配信) の入力の公開用データを、0 本でも配信する形に改めた | [HLD 4.20](../30_HLD.md#420-fr-020-公開用ビューア配信) |
| [FR-016](../20_SRS.md#fr-016-ピーク域ポリゴン生成)・[FR-018](../20_SRS.md#fr-018-per-mesh-ピーク候補-geojson-統合) の概要に [UR-016](../10_URD.md#ur-016) を宣言する理由を書き、[NFR-009](../20_SRS.md#nfr-009-観測可能性中間成果物の可視化) の「ではなく」を「だけでなく」の形に和らげた | [HLD 4.16](../30_HLD.md#416-fr-016-ピーク域ポリゴン生成)・4.18 |
| ADR-SRS-024 の「追って検討」に、広域解析の途中で止めても最後に終えた統合の組が残る旨の注を置いた | [HLD 2.10](../30_HLD.md#2105-未決事項と後続)（D79「フェーズ3 ではピーク候補 GeoJSON を統合直前に消す」） |
| [FR-008](../20_SRS.md#fr-008-per-mesh-csv-統合) に、陸地最高峰の海面確定を最終フィルタより先に当てることを書いた | [HLD 4.8](../30_HLD.md#48-fr-008-per-mesh-csv-統合)（D82） |
| §8.1 の No.10 に `params/land_highest_peaks.csv` を、[FR-008](../20_SRS.md#fr-008-per-mesh-csv-統合) の近傍一致に 30m と 2 件以上で止めることを書いた | [HLD 4.8](../30_HLD.md#48-fr-008-per-mesh-csv-統合)（D80） |
| [FR-008](../20_SRS.md#fr-008-per-mesh-csv-統合) に、陸のコルで確定したピークは陸地最高峰リストで書き換えないことを書いた。ADR-SRS-019 に注を置いた | [HLD 4.8](../30_HLD.md#48-fr-008-per-mesh-csv-統合)（D81） |
| [FR-008](../20_SRS.md#fr-008-per-mesh-csv-統合) の出力か §8.1 の No.6 に `merged_peak.csv` の 13 列を書いた | [HLD 4.8](../30_HLD.md#48-fr-008-per-mesh-csv-統合) |
| [FR-008](../20_SRS.md#fr-008-per-mesh-csv-統合) と [FR-023](../20_SRS.md#fr-023-解析パイプライン制御) の起動前提条件に、陸地最高峰リストの書式の検査を足し、[FR-023](../20_SRS.md#fr-023-解析パイプライン制御) の入力の表と §8.1 の No.10 の参照 FR を直した | [HLD 4.8](../30_HLD.md#48-fr-008-per-mesh-csv-統合)（D85）、[HLD 4.23](../30_HLD.md#423-fr-023-解析パイプライン制御) |
| [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の point-in-polygon に、点を Z15 の画素の中心に直してから判定することを書いた | [HLD 4.9](../30_HLD.md#49-fr-009-sotaリスト突合match_status-判定)（D86） |
| §7.2.4 の「正常入力の前提」に、前提に反する入力では止めることを書いた | [HLD 4.9](../30_HLD.md#49-fr-009-sotaリスト突合match_status-判定)（D88） |
| [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の市区町村・都道府県判定に、境界の上の点・どれにも入らない点・陸のコルに限る照合・エリア `ZZ` を書いた | [HLD 4.9](../30_HLD.md#49-fr-009-sotaリスト突合match_status-判定)（D91・D92） |
| [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の異常系に、確定したピークの AZ に入るサミットが 2 つ以上ある場合と連番上限の超過では出力を書かずに止めること、未確定のピークを含む重なりの帰属を書いた。ADR-SRS-033 に注を置いた | [HLD 4.9](../30_HLD.md#49-fr-009-sotaリスト突合match_status-判定)（D93） |
| [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の `peak.match_status` の 3 を、`delete` のサミットの主ピークに選ばれたピークと読める字句に直した | [HLD 4.9](../30_HLD.md#49-fr-009-sotaリスト突合match_status-判定)（D95） |
| [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) のコルの点と線を、海面で確定した場合も含めない字句に直した | [HLD 4.9](../30_HLD.md#49-fr-009-sotaリスト突合match_status-判定)（D100） |
| [FR-019](../20_SRS.md#fr-019-html-ビューア機能仕様) のピークの popup の ※2 の字句を、小数 2 桁（`0.00m`）の書き方に合わせた | [HLD 4.9](../30_HLD.md#49-fr-009-sotaリスト突合match_status-判定)（D104） |
| §6.2.6・§6.2.2 の「単一シート」を、最後に出典のシートを持つと読める字句に直した | [HLD 4.9](../30_HLD.md#49-fr-009-sotaリスト突合match_status-判定)（D102） |
| [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の metadata に `unknown` と空文字の場合を書いた。ADR-SRS-032 に注を置いた | [HLD 4.9](../30_HLD.md#49-fr-009-sotaリスト突合match_status-判定)（D98） |
| 用語集の標高バンド、[FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の変更申請判定と突合済み統合 GeoJSON の属性、[FR-012](../20_SRS.md#fr-012-サミット一覧申請内容反映版生成) の出力カラムに、150m 未満で `points`・`sota_points` を null、`is_band_change_candidate` を false にすることを書いた | [HLD 4.9](../30_HLD.md#49-fr-009-sotaリスト突合match_status-判定)（D170） |
| [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の説明と §7.2.5 の用途を、`unmatched` を含むすべてのサミットに `summit_name_jp` を付けると読める字句に直した | [HLD 4.9](../30_HLD.md#49-fr-009-sotaリスト突合match_status-判定) |
| [FR-011](../20_SRS.md#fr-011-申請書-xlsx-生成) の通常行の並びと §6.2.1 のファイル名を、HLD で決めたと読める字句に直した | [HLD 4.11](../30_HLD.md#411-fr-011-申請書-xlsx-生成)（D118・D119） |
| [FR-011](../20_SRS.md#fr-011-申請書-xlsx-生成) の変更の行の E 列の取り元を、AZ の中のサミットの点と書いた | [HLD 4.11](../30_HLD.md#411-fr-011-申請書-xlsx-生成)（D121） |
| §6.2.2 と [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の行生成モデルの `area_complete` の取り元を AZ と読める字句に直した | [HLD 4.12](../30_HLD.md#412-fr-012-サミット一覧申請内容反映版生成)（D110） |
| 未確定のピークの行の `col_margin_px`、`band_change`・`no_change` の行の `municipality`・`region_name` の取り元、通常の `delete` の行の空の列を、[FR-012](../20_SRS.md#fr-012-サミット一覧申請内容反映版生成) の出力カラムか [FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定) の行生成モデルに書いた | [HLD 4.12](../30_HLD.md#412-fr-012-サミット一覧申請内容反映版生成)（D116） |
| [FR-012](../20_SRS.md#fr-012-サミット一覧申請内容反映版生成) の入力の表に SheetJS の行を足し、出力カラムの「空文字」を空のセルと読める字句に直し、`summit_name_jp` の編集値が `add` の行にだけ効くと読める字句に直した | [HLD 4.12](../30_HLD.md#412-fr-012-サミット一覧申請内容反映版生成)（D112） |
| [FR-016](../20_SRS.md#fr-016-ピーク域ポリゴン生成) の delete判定ゾーンの閾値から、コルの標高を含めないことを書いた（用語集、ADR-SRS-011 の注も） | [HLD 4.16](../30_HLD.md#416-fr-016-ピーク域ポリゴン生成)（D70） |
| [FR-016](../20_SRS.md#fr-016-ピーク域ポリゴン生成) の塗りの対象を、範囲の中の陸地の画素に限ると書いた | [HLD 4.16](../30_HLD.md#416-fr-016-ピーク域ポリゴン生成)（D69） |
| [FR-016](../20_SRS.md#fr-016-ピーク域ポリゴン生成) の入力の表に日本全土1次メッシュコードリストと北方領土除外メッシュリストを足し、§8.1 の No.4・No.16 の参照 FR に [FR-016](../20_SRS.md#fr-016-ピーク域ポリゴン生成) を足した。異常系の「入力は全て内部トランザクション」を直した | [HLD 4.16](../30_HLD.md#416-fr-016-ピーク域ポリゴン生成)（D73） |
| ADR-SRS-010 の Decision 2 と Phase 4 に、`cv::floodFill`・`cv::findContours` を使わない旨の注を置いた | [HLD 4.16](../30_HLD.md#416-fr-016-ピーク域ポリゴン生成)（D71） |
| ゾーンを指す Polygon の字句を、Polygon か MultiPolygon と読める字句に直した（[FR-016](../20_SRS.md#fr-016-ピーク域ポリゴン生成)・[FR-018](../20_SRS.md#fr-018-per-mesh-ピーク候補-geojson-統合)・[FR-009](../20_SRS.md#fr-009-sotaリスト突合match_status-判定)・[FR-012](../20_SRS.md#fr-012-サミット一覧申請内容反映版生成)、§6.2.2・§6.2.4・§6.2.6。ADR-SRS-013・026・045 に注） | [HLD 4.16](../30_HLD.md#416-fr-016-ピーク域ポリゴン生成)（D71） |
| [FR-016](../20_SRS.md#fr-016-ピーク域ポリゴン生成) の Feature プロパティと [NFR-009](../20_SRS.md#nfr-009-観測可能性中間成果物の可視化) の凡例に、スタイルの属性は数えないこと、形でなく色と大きさで区別することを書いた（ADR-SRS-022・026 に注） | [HLD 4.16](../30_HLD.md#416-fr-016-ピーク域ポリゴン生成)（D74） |
| [FR-018](../20_SRS.md#fr-018-per-mesh-ピーク候補-geojson-統合) に、同じ種類のゾーンが 2 つ以上あるときの選び方を書いた（ADR-SRS-024 に注） | [HLD 4.18](../30_HLD.md#418-fr-018-per-mesh-ピーク候補-geojson-統合)（D75） |
| [NFR-009](../20_SRS.md#nfr-009-観測可能性中間成果物の可視化) の凡例に、`merged_peak.geojson` ではコル未確定のピークの点の色を変えることを書いた（ADR-SRS-026・024 に注） | [HLD 4.18](../30_HLD.md#418-fr-018-per-mesh-ピーク候補-geojson-統合)（D77） |
| §8.1 の No.4 の参照 FR から [FR-018](../20_SRS.md#fr-018-per-mesh-ピーク候補-geojson-統合) を外し、[FR-018](../20_SRS.md#fr-018-per-mesh-ピーク候補-geojson-統合) の入力の表のデフォルトを直した | [HLD 4.18](../30_HLD.md#418-fr-018-per-mesh-ピーク候補-geojson-統合) |
| [FR-022](../20_SRS.md#fr-022-コル充足判定) の異常系の「ピーク件数がゼロ」を見出しの行だけのファイルと書き、「読み取りエラー」に3列の見出しと値の書式の違いを含めた | [HLD 4.22](../30_HLD.md#422-fr-022-コル充足判定)（D106） |
| [FR-005](../20_SRS.md#fr-005-ピーク候補検出) と用語集の「ピーク候補」の処理済みピクセルを、近傍の成分に数えないと読める字句に直した | [HLD 4.5](../30_HLD.md#45-fr-005-ピーク候補検出)（D57） |
| [FR-007](../20_SRS.md#fr-007-per-mesh-csv-出力プロミネンス閾値適用) の `col_margin_px` の定義に海面確定の −1 と未確定の行のいつも 1 を書き、[FR-006](../20_SRS.md#fr-006-コル検出プロミネンス計算) の `key_col_resolved` の判定を合流の前の印と書いた | [HLD 4.6](../30_HLD.md#46-fr-006-コル検出プロミネンス計算)（D61・D63） |

[UR-018](../10_URD.md#ur-018) の字句は [ADR-URD-023](ADR-URD-023-ur-018-publish-wording.md) で直した。

## Alternatives

- **(a) 項目ごとに ADR を分ける**: 項目は 40 件を超え、どれも決定は HLD 側にあるので、記録が重複する。
- **(b) フェーズゲートの後に回す**: 詳細設計（LLD）が、SRS と HLD の食い違いを抱えたまま始まる。
- **(c) 試験仕様（ST）も同時に直す**: 量が倍になる。SRS の字句が固まってから ST を書く方が手戻りが無い。

## Consequences

- [SRS](../20_SRS.md)（[FR-001](../20_SRS.md#fr-001-標高タイル事前取得) を除く FR、[NFR-009](../20_SRS.md#nfr-009-観測可能性中間成果物の可視化)、§3・§6・§7・§8）、[用語集](../00_GLOSSARY.md)の標高バンド・delete判定ゾーン・ピーク候補、URD の注記（[ADR-URD-023](ADR-URD-023-ur-018-publish-wording.md)）の字句を直した。[FR-001](../20_SRS.md#fr-001-標高タイル事前取得) の入力の表と §8.1 の No.5 の参照 FR には、標高タイル（ローカルキャッシュ）がすでにあった。
- 次の ADR の状態と決定日の表の直後に、改めた決定や字句を示す注を置いた: [ADR-SRS-010](ADR-SRS-010-cpp-opencv-migration.md)、[ADR-SRS-011](ADR-SRS-011-delete-zone-polygon.md)、[ADR-SRS-013](ADR-SRS-013-merged-geojson-as-central-data.md)、[ADR-SRS-019](ADR-SRS-019-land-summit-highest-peak-handling.md)、[ADR-SRS-022](ADR-SRS-022-per-mesh-geojson-property-design.md)、[ADR-SRS-024](ADR-SRS-024-fr018-loop-reentry-and-peak-filter.md)、[ADR-SRS-026](ADR-SRS-026-intermediate-geojson-peak-col-visualization.md)、[ADR-SRS-032](ADR-SRS-032-gsi-tile-latest-date-provenance.md)、[ADR-SRS-033](ADR-SRS-033-defect-confirmation-via-xlsx.md)、[ADR-SRS-045](ADR-SRS-045-summit-xlsx-row-aggregation-model.md)、[ADR-URD-022](ADR-URD-022-split-ur-006-into-geojson-and-two-viewers.md)。
- [HLD](../30_HLD.md) の各節の「未決事項と後続」の改訂の候補の項目を、番号と題を残して「本 ADR で直した」の形に縮めた。食い違いを現在形で書いていた D の理由などの文は、決定の時点の記録として残し、文の末尾に直したことを添えた。
- 試験仕様（ST）の改訂候補は、HLD の各節の「ST の改訂の機会」の項目として残し、別に追う。
- [HLD](../30_HLD.md) の決定そのものは変えていない。
