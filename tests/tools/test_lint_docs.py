"""tools/lint_docs.py 検査F（HLD の設計判断の題）と検査G（HLD の項目の題）のテスト（標準ライブラリの unittest）"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
import lint_docs as ld  # noqa: E402

HLD = '''# HLD

## 2. 設計

### 2.1 甲

#### 2.1.4 設計判断

- DEC1（甲は乙にする）〔境界〕: 本文。[DEC2](#214-設計判断)「`--opt` の値は丙」に従う。
- DEC2（`--opt` の値は丙）: 本文。
- DEC3（申請書の行は DEC1 の順のまま）〔上位文書・やり直し費用〕: 本文。

参照は [DEC1](#214-設計判断)「甲は乙にする」と [DEC3](#214-設計判断)「申請書の行は DEC1 の順のまま」（観点）。
'''


def lint_at(text, rel):
    """tmp/<rel> に text を書いて check_file の違反名の list を返す"""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / rel
        path.parent.mkdir(parents=True)
        path.write_text(text, encoding='utf-8')
        return [v.split(': ')[1] for v in ld.check_file(str(path))]


class CheckHldDecisionsTest(unittest.TestCase):
    def lint(self, text, name='30_HLD.md'):
        return lint_at(text, f'docs/{name}')

    def test_clean(self):
        self.assertEqual(self.lint(HLD), [])

    def test_bare_ref(self):
        self.assertEqual(self.lint(HLD + '\nDEC1「甲は乙にする」に従う。\n'), ['HLD-DEC-BARE'])

    def test_bare_ref_in_definition_body(self):
        text = HLD.replace('[DEC2](#214-設計判断)「`--opt`', 'DEC2「`--opt`')
        self.assertEqual(self.lint(text), ['HLD-DEC-BARE'])

    def test_wrong_anchor(self):
        self.assertEqual(self.lint(HLD + '\n[DEC1](#21-甲)「甲は乙にする」に従う。\n'), ['HLD-DEC-ANCHOR'])

    def test_percent_encoded_anchor(self):
        text = HLD + '\n[DEC1](#214-%E8%A8%AD%E8%A8%88%E5%88%A4%E6%96%AD)「甲は乙にする」に従う。\n'
        self.assertEqual(self.lint(text), [])

    def test_no_title(self):
        self.assertEqual(self.lint(HLD + '\n[DEC1](#214-設計判断) に従う。\n'), ['HLD-DEC-NOTITLE'])

    def test_title_not_closed(self):
        self.assertEqual(self.lint(HLD + '\n[DEC1](#214-設計判断)「甲は乙\n'), ['HLD-DEC-TITLE'])

    def test_title_mismatch(self):
        self.assertEqual(self.lint(HLD + '\n[DEC1](#214-設計判断)「甲は丁にする」。\n'), ['HLD-DEC-TITLE'])

    def test_unknown(self):
        self.assertEqual(self.lint(HLD + '\n[DEC9](#214-設計判断)「無い」と DEC8。\n'),
                         ['HLD-DEC-UNKNOWN', 'HLD-DEC-UNKNOWN'])

    def test_ignored_places(self):
        text = HLD + '\n## DEC1 について\n\n`DEC1` と「DEC1 の引用」。\n'
        self.assertEqual(self.lint(text), [])

    def test_title_length_excludes_backticks(self):
        ok = HLD.replace('甲は乙にする）', 'あ' * 28 + '`x`）').replace('「甲は乙にする」', '「' + 'あ' * 28 + '`x`」')
        self.assertEqual(self.lint(ok), [])
        long = HLD.replace('甲は乙にする）', 'あ' * 31 + '）').replace('「甲は乙にする」', '「' + 'あ' * 31 + '」')
        self.assertEqual(self.lint(long), ['HLD-DEC-LONG'])

    def test_mark(self):
        for bad in ('〔重要〕', '〔やり直し費用・上位文書〕', '〔〕', '〔境界・境界〕'):
            with self.subTest(bad=bad):
                self.assertEqual(self.lint(HLD.replace('〔境界〕', bad)), ['HLD-DEC-MARK'])

    def test_definition_outside_decision_section(self):
        self.assertEqual(self.lint(HLD + '\n## 3. 他\n\n- DEC4（外）: 本文。\n'), ['HLD-DEC-PLACE'])

    def test_definition_in_code_block_ignored(self):
        self.assertEqual(self.lint(HLD + '\n```\n- DEC4（無視）: 本文。\n```\n'), [])

    def test_duplicate_definition(self):
        text = HLD.replace('- DEC2（`--opt` の値は丙）: 本文。\n',
                           '- DEC2（`--opt` の値は丙）: 本文。\n- DEC2（`--opt` の値は丙）: 本文。\n')
        self.assertEqual(self.lint(text), ['HLD-DEC-DUP'])

    def test_other_files_not_checked(self):
        self.assertEqual(self.lint('DEC1「x」\n', name='20_SRS.md'), [])


class CheckOldSymbolsTest(unittest.TestCase):
    def test_old_symbols(self):
        self.assertEqual(lint_at('C4 と D45「題」と K1。\n', 'docs/02_test_policy.md'),
                         ['OLD-SYMBOL', 'OLD-SYMBOL', 'OLD-SYMBOL'])

    def test_not_symbols(self):
        text = ('CMP4・DEC45・PRE1・CMP4-EXT1・ADR-SRS-010・DEM5・3D・UTF-8・`C3` のセル・'
                '[x](https://example.com/C4)・[3.4](#34-cmp4-地形解析エンジン)\n')
        self.assertEqual(lint_at(text, 'docs/02_test_policy.md'), [])

    def test_joint_even_in_code(self):
        self.assertEqual(lint_at('`C4-E1` と C5-I2。\n', 'docs/30_HLD.md'), ['OLD-JOINT', 'OLD-JOINT'])

    def test_fenced_block_checked(self):
        self.assertEqual(lint_at('```text\nC1 ─→ C2\n```\n', 'docs/30_HLD.md'), ['OLD-SYMBOL', 'OLD-SYMBOL'])

    def test_adr_checked_research_not(self):
        self.assertEqual(lint_at('C4。\n', 'docs/decisions/ADR-HLD-999-x.md'), ['OLD-SYMBOL'])
        self.assertEqual(lint_at('C4。\n', 'docs/decisions/research/x.md'), [])

    def test_outside_docs_not_checked(self):
        self.assertEqual(lint_at('C4。\n', 'other/x.md'), [])

    def test_sources_checked(self):
        self.assertEqual(lint_at('（D164・D184〜D186）\n', 'ref/SOURCES.md'),
                         ['OLD-SYMBOL', 'OLD-SYMBOL', 'OLD-SYMBOL'])

    def test_joint_like_text_in_url_is_not_checked(self):
        self.assertEqual(lint_at('[資料](https://example.com/C4-E1)\n', 'docs/02_test_policy.md'), [])

    def test_symbol_inside_file_name_is_not_a_symbol(self):
        for text in ('C1.txt を読む。\n', 'C1_data を読む。\n', 'C1/x を読む。\n'):
            with self.subTest(text=text):
                self.assertEqual(lint_at(text, 'docs/02_test_policy.md'), [])

    def test_sentence_end_after_symbol_is_still_checked(self):
        self.assertEqual(lint_at('C4。\n', 'docs/02_test_policy.md'), ['OLD-SYMBOL'])
        self.assertEqual(lint_at('C4. 次\n', 'docs/02_test_policy.md'), ['OLD-SYMBOL'])


HLD_ITEMS = '''# HLD

### 4.8 節

#### 4.8.2 処理の流れ

1. **リストを読む**。本文。
2. 題の無い手順。
3. **代表行を選ぶ**。本文。
4. **`.csv` を読む**。本文。

**出力の組み立て**：次のとおり。

1. **列を並べる**。本文。

#### 4.8.6 その他

1. 対象外の箇条。

参照は [4.8.2](#482-処理の流れ) の 1「リストを読む」。
'''


class CheckHldItemRefsTest(unittest.TestCase):
    def lint(self, text, name='30_HLD.md'):
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / 'docs'
            docs.mkdir()
            path = docs / name
            path.write_text(text, encoding='utf-8')
            return [v.split(': ')[1] for v in ld.check_file(str(path))]

    def test_ok(self):
        self.assertEqual(self.lint(HLD_ITEMS), [])

    def test_bare(self):
        self.assertEqual(self.lint(HLD_ITEMS + '\n[4.8.2](#482-処理の流れ) の 3 に従う。\n'),
                         ['HLD-ITEM-BARE'])

    def test_title_mismatch(self):
        self.assertEqual(self.lint(HLD_ITEMS + '\n[4.8.2](#482-処理の流れ) の 3「代表を選ぶ」に従う。\n'),
                         ['HLD-ITEM-TITLE'])

    def test_unknown(self):
        self.assertEqual(self.lint(HLD_ITEMS + '\n[4.8.2](#482-処理の流れ) の 9「無い」に従う。\n'),
                         ['HLD-ITEM-UNKNOWN'])

    def test_item_without_title(self):
        self.assertEqual(self.lint(HLD_ITEMS + '\n[4.8.2](#482-処理の流れ) の 2「題の無い手順」に従う。\n'),
                         ['HLD-ITEM-NOTITLE'])

    def test_named_list(self):
        ok = HLD_ITEMS + '\n[4.8.2](#482-処理の流れ) の「出力の組み立て」の 1「列を並べる」に従う。\n'
        self.assertEqual(self.lint(ok), [])
        unnamed = HLD_ITEMS + '\n[4.8.2](#482-処理の流れ) の 1「列を並べる」に従う。\n'
        self.assertEqual(self.lint(unnamed), ['HLD-ITEM-TITLE'])
        missing = HLD_ITEMS + '\n[4.8.2](#482-処理の流れ) の「無い名前」の 1「列を並べる」に従う。\n'
        self.assertEqual(self.lint(missing), ['HLD-ITEM-UNKNOWN'])

    def test_range(self):
        self.assertEqual(self.lint(HLD_ITEMS + '\n[4.8.2](#482-処理の流れ) の 1〜4 に従う。\n'), [])
        self.assertEqual(self.lint(HLD_ITEMS + '\n[4.8.2](#482-処理の流れ) の 1〜9 に従う。\n'),
                         ['HLD-ITEM-UNKNOWN'] * 5)

    def test_list(self):
        ok = HLD_ITEMS + '\n[4.8.2](#482-処理の流れ) の 1「リストを読む」・3「代表行を選ぶ」に従う。\n'
        self.assertEqual(self.lint(ok), [])
        bare = HLD_ITEMS + '\n[4.8.2](#482-処理の流れ) の 1「リストを読む」・3 に従う。\n'
        self.assertEqual(self.lint(bare), ['HLD-ITEM-BARE'])

    def test_title_with_code(self):
        self.assertEqual(self.lint(HLD_ITEMS + '\n[4.8.2](#482-処理の流れ) の 4「`.csv` を読む」に従う。\n'), [])

    def test_counter_words_are_not_refs(self):
        text = HLD_ITEMS + '\n[4.8.2](#482-処理の流れ) の 5 種類と 60 行。\n'
        self.assertEqual(self.lint(text), [])

    def test_code_span_ignored(self):
        self.assertEqual(self.lint(HLD_ITEMS + '\n`[4.8.2](#482-処理の流れ) の 3` の形。\n'), [])

    def test_other_sections_not_checked(self):
        self.assertEqual(self.lint(HLD_ITEMS + '\n[4.8.6](#486-その他) の 1 に従う。\n'), [])

    def test_long_title(self):
        text = HLD_ITEMS.replace('**リストを読む**', '**' + 'あ' * 31 + '**').replace(
            '「リストを読む」', '「' + 'あ' * 31 + '」')
        self.assertEqual(self.lint(text), ['HLD-ITEM-LONG'])

    def test_range_gap(self):
        text = HLD_ITEMS.replace('2. 題の無い手順。\n', '') + '\n[4.8.2](#482-処理の流れ) の 1〜4 に従う。\n'
        self.assertEqual(self.lint(text), ['HLD-ITEM-UNKNOWN'])

    def test_range_reversed(self):
        self.assertEqual(self.lint(HLD_ITEMS + '\n[4.8.2](#482-処理の流れ) の 4〜1 に従う。\n'),
                         ['HLD-ITEM-RANGE'])
        self.assertEqual(self.lint(HLD_ITEMS + '\n[4.8.2](#482-処理の流れ) の 3〜3 に従う。\n'),
                         ['HLD-ITEM-RANGE'])

    def test_section_without_items(self):
        text = (HLD_ITEMS + '\n#### 4.8.7 処理の流れ\n\nなし。\n\n'
                '[4.8.7](#487-処理の流れ) の 1「無い」に従う。\n')
        self.assertEqual(self.lint(text), ['HLD-ITEM-UNKNOWN'])
        indented = (HLD_ITEMS + '\n#### 4.8.8 処理の流れ\n\n- 親。\n  1. **子**。本文。\n\n'
                    '[4.8.8](#488-処理の流れ) の 1「子」に従う。\n')
        self.assertEqual(self.lint(indented), ['HLD-ITEM-UNKNOWN'])

    def test_title_followed_by_parenthesis(self):
        text = HLD_ITEMS.replace('4. **`.csv` を読む**。本文。', '4. **`.csv` を読む**（注記）。本文。')
        self.assertEqual(self.lint(text + '\n[4.8.2](#482-処理の流れ) の 4「`.csv` を読む」に従う。\n'), [])

    def test_continuation_after_ref(self):
        text = HLD_ITEMS + '\n[4.8.2](#482-処理の流れ) の 1「リストを読む」（注記）・999「存在しない」に従う。\n'
        self.assertEqual(self.lint(text), ['HLD-ITEM-CONT'])
        text = HLD_ITEMS + '\n[4.8.2](#482-処理の流れ) の 3「代表行を選ぶ」 と 4 の各段に従う。\n'
        self.assertEqual(self.lint(text), ['HLD-ITEM-CONT'])
        text = HLD_ITEMS + '\n[4.8.2](#482-処理の流れ) の 3「代表行を選ぶ」と、4「`.csv` を読む」に従う。\n'
        self.assertEqual(self.lint(text), ['HLD-ITEM-CONT'])

    def test_open_items_section_rejected(self):
        text = HLD_ITEMS + '\n#### 4.8.9 未決事項と後続\n\n1. **何か**。本文。\n'
        self.assertEqual(self.lint(text), ['HLD-OPEN-SECTION'])
        text = HLD_ITEMS + '\n#### 4.8.9 未決事項と後続（他の節・LLD・ADR 候補）\n\nなし。\n'
        self.assertEqual(self.lint(text), ['HLD-OPEN-SECTION'])
        text = HLD_ITEMS + '\n### 未決事項と後続\n\nなし。\n'
        self.assertEqual(self.lint(text), ['HLD-OPEN-SECTION'])

    def test_open_items_section_heading_variants_rejected(self):
        # 章の番号の後のピリオド、2 つ以上の空白、全角の空白、行頭の 3 つまでの空白
        for heading in ['## 7. 未決事項と後続', '#### 4.8.9  未決事項と後続', '#### 4.8.9\u3000未決事項と後続',
                        '   #### 4.8.9 未決事項と後続']:
            with self.subTest(heading=heading):
                self.assertEqual(self.lint(HLD_ITEMS + '\n' + heading + '\n\nなし。\n'), ['HLD-OPEN-SECTION'])

    def test_open_items_section_in_code_block_ignored(self):
        self.assertEqual(self.lint(HLD_ITEMS + '\n```text\n#### 4.8.9 未決事項と後続\n```\n'), [])
        self.assertEqual(self.lint(HLD_ITEMS + '\n~~~\n#### 4.8.9 未決事項と後続\n~~~\n'), [])
        self.assertEqual(self.lint(HLD_ITEMS + '\n````\n```\n#### 4.8.9 未決事項と後続\n```\n````\n'), [])

    def test_open_items_section_only_in_hld(self):
        text = '# 文書\n\n#### 4.8.9 未決事項と後続\n\nなし。\n'
        self.assertEqual(self.lint(text, name='70_ST.md'), [])

    def test_open_items_items_not_checked(self):
        # 小節が残っていても、その項目は検査G で照合しない（題の違う参照で HLD-ITEM-TITLE を出さない）
        text = (HLD_ITEMS + '\n#### 4.8.5 未決事項と後続\n\n1. **テストの枠組み**。本文。\n\n'
                '[4.8.5](#485-未決事項と後続) の 1「違う題」に従う。\n')
        self.assertEqual(self.lint(text), ['HLD-OPEN-SECTION'])

    def test_huge_range_is_cheap(self):
        text = HLD_ITEMS + '\n[4.8.2](#482-処理の流れ) の 1〜1000000000 に従う。\n'
        self.assertEqual(self.lint(text), ['HLD-ITEM-RANGE'])

    def test_percent_encoded_anchor(self):
        text = HLD_ITEMS + '\n[4.8.2](#482-%E5%87%A6%E7%90%86%E3%81%AE%E6%B5%81%E3%82%8C) の 999「無い」に従う。\n'
        self.assertEqual(self.lint(text), ['HLD-ITEM-UNKNOWN'])

    def test_duplicate_list_name(self):
        text = HLD_ITEMS.replace('1. **列を並べる**。本文。\n', '1. **列を並べる**。本文。\n\n'
                                 '**出力の組み立て**：もう一度。\n\n1. **重ねて**。本文。\n')
        self.assertEqual(self.lint(text), ['HLD-ITEM-DUP'])

    def test_same_document_path_link(self):
        text = HLD_ITEMS + '\n[4.8.2](30_HLD.md#482-処理の流れ) の 999「無い」に従う。\n'
        self.assertEqual(self.lint(text), ['HLD-ITEM-UNKNOWN'])
        ok = HLD_ITEMS + '\n[4.8.2](30_HLD.md#482-処理の流れ) の 3「代表行を選ぶ」に従う。\n'
        self.assertEqual(self.lint(ok), [])

    def test_nested_ref_checks_parent(self):
        self.assertEqual(self.lint(HLD_ITEMS + '\n[4.8.2](#482-処理の流れ) の 3「代表行を選ぶ」の 2 に従う。\n'), [])

    def test_duplicate_number(self):
        text = HLD_ITEMS.replace('4. **`.csv` を読む**。本文。', '4. **`.csv` を読む**。本文。\n3. **重複**。本文。')
        self.assertEqual(self.lint(text), ['HLD-ITEM-DUP'])

    def test_other_files_not_checked(self):
        self.assertEqual(self.lint(HLD_ITEMS + '\n[4.8.2](#482-処理の流れ) の 3 に従う。\n', name='40_LLD.md'), [])


if __name__ == '__main__':
    unittest.main()
