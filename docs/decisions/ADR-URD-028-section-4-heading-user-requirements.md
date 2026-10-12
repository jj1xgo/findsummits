# ADR-URD-028: URD §4 の見出しを「ユーザーニーズ」から「ユーザー要件」に改める

| 項目 | 内容 |
|---|---|
| 状態 | 採用・実装済み |
| 決定日 | 2026-10-12 |

---

## Context

2026-10-12 に、改訂した多視点のレビュー（spec-panel）で URD の全体を見直した（[#204](https://github.com/jj1xgo/findsummits/issues/204)）。そのとき、[ADR-OPS-002](ADR-OPS-002-reference-standards-and-intended-deviations.md) が用語の補助に挙げる ISO/IEC/IEEE 24765 のオンライン版 SEVOCAB（[SOURCES「開発プロセスの参照規格」](../../ref/SOURCES.md#開発プロセスの参照規格)）で、URD の用語を引いた。

SEVOCAB の user need の項の注記は、ニーズと要求を分けている。user need は、解決の手段から独立した、利用者が成果を得るための前提で、user requirements はそれを変換して得る要求とされる（同じ項には、ニーズを要求の集合とする別の規格の定義も並んでいる）。requirement は、ニーズとそれに伴う制約と条件を表す文とされる（ISO/IEC/IEEE 12207:2026 ほか）。引いた日は 2026-10-12 で、SEVOCAB は版を固定しない。user need と user requirements の項の出典は ADR-OPS-002 の表に無い規格で、24765:2017 は出典に挙がっていなかった。

[URD §4](../10_URD.md#4-ユーザー要件) の見出しは「ユーザーニーズ」だったが、表の列名は「要件」、文書の題名は「ユーザー要件定義書」で、各 UR は「〜できること」の形の要求である。[UR-016](../10_URD.md#ur-016)〜[UR-018](../10_URD.md#ur-018) のように、成果物（GeoJSON・HTML ビューア）を指定する UR もある。見出しだけが、中身と違う語になっていた。

## Decision

[URD §4](../10_URD.md#4-ユーザー要件) の見出しを「ユーザー要件」に改め、目次と、旧見出しのアンカー（`#4-ユーザーニーズ`）を指していた ADR のリンクを新しいアンカーに直す。各 UR の字句と要求の範囲は変えない。確定済みの URD の補足として、§4 に注記を置く。

## Alternatives

- **(a) 今のままにする**: 見出しと表の列名・題名が食い違ったままになる。§4 をニーズの節と読むと、成果物を指定する UR が節の趣旨から外れて見える。
- **(b) ニーズの節を別に設け、§4 を要求の節にする**: 利用者のニーズは [§1](../10_URD.md#1-目的背景) と [§3.1](../10_URD.md#31-ステークホルダー) の「主な関心事」に書いてある。節を増やすと同じ内容を 2 か所で持つことになる。

## Consequences

- URD の §4 の見出しと目次を直し、§4 に注記を置いた。[ADR-URD-020](ADR-URD-020-requirement-traceability-and-consistency.md) と [ADR-URD-022](ADR-URD-022-split-ur-006-into-geojson-and-two-viewers.md) のリンクのアンカーを新しい見出しに合わせた（リンクの文字列は変えない）。
- [ADR-URD-017](ADR-URD-017-viewer-marker-rendering-performance.md) の Consequences の「ユーザーニーズに追加」は、当時の見出しを地の文で書いたもので、リンクではないので直さない。
- SRS・概要設計書（HLD）・ST は URD §4 の見出しを引いていないので直さない。ツールの振る舞いは変わらない。
