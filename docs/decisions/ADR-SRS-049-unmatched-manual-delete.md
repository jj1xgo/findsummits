# ADR-SRS-049: 孤立要確認サミットを担当者判断で削除申請へ含める

| 状態 | 採用・未実装 |
| 決定日 | 2026-09-21 |

## Context

[ADR-SRS-037](ADR-SRS-037-unmatched-summit-needs-review.md) は全ゾーン外の孤立サミットを
unmatched として要確認にし、地形変化と解析不備を担当者が確認して削除申請へ回す方針を定めた。
しかし作業用ビューアにその操作がなく、申請書とエビデンスへ判断・根拠を同じ内容で残す経路が未定義だった。
[ADR-SRS-048](ADR-SRS-048-multiple-summits-in-one-az.md) の複数登録の保留組とは区別する必要がある。

## Decision

元のバッチ入力が feature_type=summit、match_status=unmatched、category=review、
review_reason=unmatched、review_group_id が空文字で、正式な既存 summit_code を持つ登録だけに
「削除申請に含める」と「要確認に戻す」を設ける。自動採用・一括採用は行わない。

- バッチ出力は不変とし、[FR-019](../20_SRS.md#fr-019-html-ビューア機能仕様) だけが
  現在の表示・編集状態の category を review/delete に更新する。match_status と review_reason は unmatched を保持する。
  各エクスポートは同じ現在状態を読み、独自に判断・category を再導出しない。
- 全 GeoJSON フィーチャと両一覧 XLSX に review_decision・review_note を持たせる。
  バッチ生成時は両方空文字。選択中は review_decision=delete、review_note は前後の空白を除いた根拠本文とする。
  登録値を保持し、親ピーク・距離・コル・ゾーン・接続線を作らない。
- 手動判断であることと対象コード・根拠本文を含む専用 rationale を生成する。
  根拠未記入・空白のみは件数とコードを警告し、申請書と ZIP の出力を許す。未記入の対象行を落とさず、
  rationale に「未記入（担当者補記）」を残す。地形事象を確認済みと断定しない。
- 同じ generated_at と正式コードへの再訪は適格性検証後に判断・根拠を復元する。
  取消は現在の判断・根拠・rationale を空にし、下書きは保存して再選択時に復元する。
  新しい generated_at への継承は根拠下書きだけとし、個別の再選択まで review のままにする。
  対象外・不在コードや不正保存レコードは適用せず通知する。保存失敗時は未保存と表示して、
  有効なメモリ上の状態からの出力は許す。前回保存値を無断で破棄しない。
- 申請書は通常と同じ削除列配置で 1 行。改訂一覧は元の孤立行を同じ位置で更新し、全解析属性は空欄、
  登録値は自身の値とする。GeoJSON は delete.geojson のみに入り、取消後は review.geojson のみに戻る。
  未選択の下書きは出力しない。公開用は判断・根拠と元の unmatched を閲覧できるが操作は提供しない。
- バッチの unmatched 件数・不備ゲート、通常の自動削除、複数登録の保留組への編集・採用禁止を維持する。
  一般的な採否永続化、新設ピークの同一性、判断共有、解析除外指定は本決定に含めない。

属性の正本は [共通属性](../20_SRS.md#各フィーチャのプロパティ)、状態遷移・UI は
[FR-019](../20_SRS.md#fr-019-html-ビューア機能仕様)、保存・継承は [SRS §8.2.2](../20_SRS.md#822-localstorage-編集内容詳細仕様)。
出力は [FR-011](../20_SRS.md#fr-011-申請書-xlsx-生成)・[FR-012](../20_SRS.md#fr-012-サミット一覧申請内容反映版生成)・
[FR-021](../20_SRS.md#fr-021-申請エビデンス-zip-生成)、受入条件は [ST](../70_ST.md)。
比較検討とレビュー記録は [採用時仕様案](research/unmatched-manual-delete-spec.md) に残す。

## Alternatives

| 案 | 採らない理由 |
|---|---|
| unmatched を自動削除にする | 座標だけでは解析不備と地形変化を区別できない |
| match_status を delete に書き換える | 幾何学的な突合結果と担当者判断を混同し、元の解析結果を失う |
| 出力後の申請書だけを手編集する | 一覧・GeoJSON と判断や根拠が一致しなくなる |
| 根拠未記入で出力停止する | 成果物は担当者が補記できるドラフトであり、警告して続行する既存方針と合わせる |
| 新しい解析にも判断を自動適用する | 解析・登録状態が変わっている可能性があり、今回の個別確認を省略してしまう |

## Consequences

[ADR-SRS-044](ADR-SRS-044-category-property-summit-centric-5class.md) の category 消費契約に
作業用ビューアによる限定的な更新を追加する。[ADR-SRS-045](ADR-SRS-045-summit-xlsx-row-aggregation-model.md) の
1 行 = 1 サミットを維持しつつ、親のない delete/unmatched 行を改訂一覧に認める。
review_reason の非空は現在も保留中という意味ではなくなるため、現在の申請分類は category を読む。

根拠が未記入のドラフトはありうる。表示と成果物でその状態を明示し、公式申請の最終確認を担当者に委ねる。
HLD で保存構造・UI 配置・保存失敗時の回復方法を具体化する。文書決定時点でコード・モックアップは未実装であり、
受入試験と実環境確認は設計確定後の実装に対して行う。
