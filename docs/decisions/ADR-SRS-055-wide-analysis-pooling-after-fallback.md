# ADR-SRS-055: 広域解析の max pooling を DEM フォールバック・デコード後に行う

| 状態 | 採用・未実装 |
| 決定日 | 2026-09-23 |

## Context

[FR-014](../20_SRS.md#fr-014-広域結合解析オーケストレーション) は、DEM5a/5b/5c をそれぞれ 2×2 max pooling でズームレベル14 へ間引いてから、
DEM10b と同じ解像度で [FR-002](../20_SRS.md#fr-002-dem-階層フォールバック) のフォールバック選択に渡すと書いていた。

この記述には 2 つの問題がある。

1. [FR-002](../20_SRS.md#fr-002-dem-階層フォールバック) の入力は生の RGB ピクセル値であり、pooling 済みの値を受け取る契約になっていない。
   [ADR-SRS-004](ADR-SRS-004-level14-max-pooling-isolated-peaks.md) はデコード済みの標高（NODATA は -9999.0）で pooling するとしており、
   SRS の記述と一致しない。
2. DEM 種別ごとに先に pooling すると、同じ 2×2 の中に「DEM5a の低い有効画素」と「DEM5a が NODATA で下位 DEM が補う高い画素」が
   あるとき、pooling 後の DEM5a は低い有効値となり、フォールバックで上位の DEM5a が採られて高い画素が失われる。
   通常解析（[FR-004](../20_SRS.md#fr-004-33メッシュ結合解析オーケストレーション)）の同じ地点と標高が食い違う。

## Decision

広域解析の解析範囲標高グリッドは、次の順で作る。

1. ズームレベル15 の各画素で [FR-002](../20_SRS.md#fr-002-dem-階層フォールバック) のフォールバックと
   [FR-003](../20_SRS.md#fr-003-標高デコードnodata-処理) のデコードを行う。DEM10b は通常解析と同じく Z15 の 2×2 へ最近傍で対応付ける。
2. 得た標高を 2×2 max pooling でズームレベル14 へ縮約する。NODATA（-9999m）は有効値に負けるため、4 画素すべてが NODATA のときだけ NODATA になる。
3. 採用した最大値画素のズームレベル15 座標を保持する（[ADR-SRS-004](ADR-SRS-004-level14-max-pooling-isolated-peaks.md) の規定どおり）。

処理はタイル単位で行い、ズームレベル15 の結合画像全体は作らない（[ADR-SRS-004](ADR-SRS-004-level14-max-pooling-isolated-peaks.md) のメモリ前提を維持する）。

## Alternatives

**(A) DEM 種別ごとに pooling してからフォールバックする（従来の記述）**

却下。上記の食い違いが残り、[FR-002](../20_SRS.md#fr-002-dem-階層フォールバック) の入力契約とも合わない。

**(B) SRS の記述だけを ADR-SRS-004 に合わせる（DEM ごとに標高で pooling）**

却下。入力契約の食い違いは解消するが、フォールバックの食い違いは残る。

## Consequences

- 広域解析の各画素は、通常解析の同じ 2×2 の標高の最大値に一致する。
- [FR-002](../20_SRS.md#fr-002-dem-階層フォールバック) は通常・広域とも Z15 の RGB に対してだけ適用される。
- max pooling によるコル標高の過大評価（プロミネンスの過小評価）は残る。その扱いは
  [ADR-SRS-056](ADR-SRS-056-wide-analysis-prominence-underestimate-warning.md) を参照。
- 反映先: [FR-014](../20_SRS.md#fr-014-広域結合解析オーケストレーション)、[ST](../70_ST.md) の `ST-FR-014-05`、
  [ADR-SRS-004](ADR-SRS-004-level14-max-pooling-isolated-peaks.md) Consequences 1 の注記。
