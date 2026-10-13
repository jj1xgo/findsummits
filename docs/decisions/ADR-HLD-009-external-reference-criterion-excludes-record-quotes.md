# ADR-HLD-009: DEC の「外部参照」に、過去の字句の記録と書式の例を数えない

| 項目 | 内容 |
|---|---|
| 状態 | 採用・実装済み |
| 決定日 | 2026-10-13 |

---

## Context

[ADR-HLD-006](ADR-HLD-006-hld-decision-selection-criteria-and-open-item-cleanup.md) の Decision 1 は、HLD の設計判断（DEC）のうち、HLD の外の文書（システムテスト仕様書（ST）・ADR・調査資料）から題付きで引かれるものを「外部参照」として重要とし、[文書管理ルール](../CLAUDE.md)の書式の例は数えないとした。印は定義の行の `〔〕` に置く（[ADR-HLD-007](ADR-HLD-007-hld-symbol-prefixes-and-decision-links.md)）。

2026-10-13 の HLD 全体の最終周回（[findsummits#31](https://github.com/jj1xgo/findsummits/issues/31)）で、次の 10 件が ADR から題付きで引かれているのに〔外部参照〕を持たないことが見つかった。

- [ADR-HLD-008](ADR-HLD-008-remove-hld-open-items-subsections.md) の付録 B（旧番号の対応表）の「題」の欄: DEC2・DEC30・DEC85・DEC108・DEC128・DEC132・DEC134・DEC141・DEC154。欄は、廃止した「未決事項と後続」の小節の項目の文を、2026-10-12 の時点のまま写したもの
- ADR-HLD-007 の Consequences: DEC85。記号の置き換えで題を縮めたという作業の記録
- ADR-HLD-007 の Decision 2・3 と ADR-HLD-006 の Alternatives: DEC45。DEC の書き方を示す書式の例

字句どおりなら 10 件に印を足すことになる。しかし「外部参照」を重要とする理由は、その DEC を変えると HLD の外の文書が古くなり、直す手間が要ることにある。付録 B の写しと作業の記録は、ある時点の字句の記録で、DEC が変わっても直さない（ADR-HLD-008 は、調査資料も過去の記録として書き換えないとした）。書式の例は DEC の中身を引いていない。

## Decision

1. **数えないもの**。「外部参照」の判定で、次は数えない。
   - 文書管理ルールと ADR の中の書式の例（DEC の書き方を示すために番号と題、またはその仮の字句を挙げたもの）
   - ADR と調査資料が、ある時点の HLD の字句（DEC の題を含む）を、変更や仕分けの記録として写したもの（ADR-HLD-008 の付録 B の「題」の欄、ADR-HLD-007 の Consequences が記録した DEC85 の縮めた題など）
2. **数えるもの**。ADR・ST・調査資料の本文が、決定の根拠・前提・影響として DEC を題付きで引くものは、これまでどおり数える（例: [ADR-SRS-024](ADR-SRS-024-fr018-loop-reentry-and-peak-filter.md) と [ADR-SRS-073](ADR-SRS-073-align-srs-wording-with-hld-decisions.md) が引く DEC79）。
3. **判定のしかた**。DEC が「外部参照」に当たるかは、Decision 1 の数えない引用を除いた残りの引用があるかで決める。1 つの引用がどちらに当たるか迷うときは、その DEC が変わったら引く側を直す必要があるかで見分ける（直す必要があれば数える。変更の記録の表の中でも、根拠として引いているもの（[ADR-SRS-073](ADR-SRS-073-align-srs-wording-with-hld-decisions.md) の DEC79 など）は数える）。
4. **印は変えない**。上の 10 件の印は今のままとする。
5. **基準の字句**。文書管理ルール「HLD の記号の書き方」の基準の行を、Decision 1 の趣旨で改める。ADR-HLD-006 には追記で本 ADR を指し、Decision 1 の表の行は過去の記録として残す。

## Alternatives

- 字句どおり 10 件に〔外部参照〕を足す: 規則を変えずに済む。しかし、記録の写しや例のためだけに重要な DEC が増え、印の意味（変えると外の文書が古くなる）と合わない。
- ADR-HLD-008 の付録 B と ADR-HLD-007 の Consequences から DEC の題を消す: 引用が無くなり基準を変えずに済むが、過去の記録を書き換えることになる。

## Consequences

- HLD の〔外部参照〕の件数（19 件）は変わらない。
- `make lint` の検査F は印の名だけを照合し、基準に当たるかは照合しない。この判定はこれまでどおり、DEC を書く・改めるときと spec-panel の周回で人が行う。
