"""tools/lint_docs.py 検査F（HLD の設計判断の題）と検査G（HLD の項目の題）のテスト（標準ライブラリの unittest）"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
import lint_docs as ld  # noqa: E402

HLD = '''# HLD

## 2. 設計

- D1（甲は乙にする）: 本文。D2「`--opt` の値は丙」に従う。
- D2（`--opt` の値は丙）: 本文。
- D3（申請書の行は D1 の順のまま）: 本文。

参照は D1「甲は乙にする」と D3「申請書の行は D1 の順のまま」（観点）。

## 付録 A 設計判断の一覧

| 記号 | 題 | 置き場 |
|---|---|---|
| D1 | 甲は乙にする | [2](#2-設計) |
| D2 | `--opt` の値は丙 | [2](#2-設計) |
| D3 | 申請書の行は D1 の順のまま | [2](#2-設計) |
'''


class CheckHldDecisionsTest(unittest.TestCase):
    def lint(self, text, name='30_HLD.md'):
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / 'docs'
            docs.mkdir()
            path = docs / name
            path.write_text(text, encoding='utf-8')
            return [v.split(': ')[1] for v in ld.check_file(str(path))]

    def test_clean(self):
        self.assertEqual(self.lint(HLD), [])

    def test_bare_ref(self):
        self.assertEqual(self.lint(HLD + '\nD1 に従う。\n'), ['HLD-D-BARE'])

    def test_bare_ref_in_definition_body(self):
        text = HLD.replace('- D2（`--opt` の値は丙）: 本文。', '- D2（`--opt` の値は丙）: D1 を受ける。')
        self.assertEqual(self.lint(text), ['HLD-D-BARE'])

    def test_title_not_closed(self):
        self.assertEqual(self.lint(HLD + '\nD1「甲は乙にする に従う。\n'), ['HLD-D-TITLE'])

    def test_title_mismatch(self):
        self.assertEqual(self.lint(HLD + '\nD1「甲は乙」に従う。\n'), ['HLD-D-TITLE'])

    def test_unknown(self):
        self.assertEqual(self.lint(HLD + '\nD9「何か」に従う。\n'), ['HLD-D-UNKNOWN'])

    def test_ignored_places(self):
        text = HLD + '\n### D1 の見出し\n\n`D1` と 「D1 の引用」。\n\n```text\nD1\n```\n'
        self.assertEqual(self.lint(text), [])

    def test_title_length_excludes_backticks(self):
        ok = 'あ' * 28 + '`ab`'  # 見える文字数 30、バッククォート込みで 32
        long_ = 'あ' * 31
        text = HLD.replace('甲は乙にする', ok)
        self.assertEqual(self.lint(text), [])
        text = HLD.replace('甲は乙にする', long_)
        self.assertEqual(self.lint(text), ['HLD-D-LONG'])

    def test_index_mismatch_and_missing(self):
        text = HLD.replace('| D1 | 甲は乙にする |', '| D1 | 甲は乙 |')
        self.assertEqual(self.lint(text), ['HLD-D-INDEX'])
        text = HLD.replace('| D2 | `--opt` の値は丙 | [2](#2-設計) |\n', '')
        self.assertEqual(self.lint(text), ['HLD-D-INDEX'])

    def test_index_row_outside_appendix(self):
        row = '| D2 | `--opt` の値は丙 | [2](#2-設計) |\n'
        text = HLD.replace(row, '').replace('## 付録 A', row + '\n## 付録 A')
        self.assertEqual(self.lint(text), ['HLD-D-BARE', 'HLD-D-INDEX'])

    def test_definition_in_code_block_ignored(self):
        text = HLD + '\n```text\n- D1（別の題）: 例。\n```\n'
        self.assertEqual(self.lint(text), [])

    def test_duplicate_definition(self):
        text = HLD.replace('- D3（申請書の行は D1 の順のまま）: 本文。',
                           '- D3（申請書の行は D1 の順のまま）: 本文。\n- D1（甲は乙にする）: 再掲。')
        self.assertEqual(self.lint(text), ['HLD-D-DUP'])

    def test_other_files_not_checked(self):
        self.assertEqual(self.lint(HLD + '\nD1 に従う。\n', name='40_LLD.md'), [])
        self.assertEqual(self.lint(HLD + '\nD1 に従う。\n', name='30_HLD-§2.7.md'), [])


HLD_ITEMS = '''# HLD

### 4.8 節

#### 4.8.2 処理の流れ

1. **リストを読む**。本文。
2. 題の無い手順。
3. **代表行を選ぶ**。本文。
4. **`.csv` を読む**。本文。

**出力の組み立て**：次のとおり。

1. **列を並べる**。本文。

#### 4.8.5 未決事項と後続

1. **テストの枠組み**。本文。

#### 4.8.6 その他

1. 対象外の箇条。

参照は [4.8.2](#482-処理の流れ) の 1「リストを読む」と [4.8.5](#485-未決事項と後続) の 1「テストの枠組み」。
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
        text = HLD_ITEMS + '\n[4.8.2](#482-処理の流れ) の 5 種類と [4.8.5](#485-未決事項と後続) の 60 行。\n'
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
        text = (HLD_ITEMS + '\n#### 4.8.7 未決事項と後続\n\nなし。\n\n'
                '[4.8.7](#487-未決事項と後続) の 1「無い」に従う。\n')
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
