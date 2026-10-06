"""tools/lint_docs.py 検査F（HLD の設計判断の題）のテスト（標準ライブラリの unittest）"""
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


if __name__ == '__main__':
    unittest.main()
