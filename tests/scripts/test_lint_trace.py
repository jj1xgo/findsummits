"""scripts/lint_trace.py のテスト（標準ライブラリの unittest）"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
import lint_trace as lt  # noqa: E402

URD = '''# URD

| ID | 内容 |
|---|---|
| <a id="ur-001"></a>[UR-001](#ur-001) | 一 |
| <a id="ur-002"></a>[UR-002](#ur-002) | 二 |
'''

SRS = '''# SRS

### 3.2 主要コンポーネント構成

| コンポーネント ID | 名前 |
|---|---|
| C1 | 甲 |
| C2 | 乙 |

#### FR-001: 一

- **対応 UR**: [UR-001](10_URD.md#ur-001)

#### FR-002: 二

- **対応 UR**: [UR-002](10_URD.md#ur-002)

### NFR-001: 非一

- **対応 UR**: [UR-001](10_URD.md#ur-001)

## 12. 要求追跡マトリクス

| FR/NFR | タイトル | [UR-001](10_URD.md#ur-001) | [UR-002](10_URD.md#ur-002) |
|:---|:---|:-:|:-:|
| [FR-001](#fr-001-一) | 一 | ✅ | |
| [FR-002](#fr-002-二) | 二 | | ✅ |
| [NFR-001](#nfr-001-非一) | 非一 | ✅ | |
'''

ST = '''# ST

## 3. 第1部

| ID | 手順 |
|---|---|
| `ST-FR-001-01` | a |
| `ST-FR-002-01`（異常系） | b |
| `ST-NFR-001-01` | c |

## 4. 第2部

### ST-UR-001-01: 通し

## 5. URカバレッジ表

| UR | 内容 | 対応FR/NFR（✅） | テストケース |
|---|---|---|---|
| [UR-001](10_URD.md#ur-001) | 一 | [FR-001](20_SRS.md#fr-001-一), [NFR-001](20_SRS.md#nfr-001-非一) | `ST-FR-001-01` |
| [UR-002](10_URD.md#ur-002) | 二 | [FR-002](20_SRS.md#fr-002-二) | `ST-FR-002-01` |
'''

BASE = {'docs/10_URD.md': URD, 'docs/20_SRS.md': SRS, 'docs/70_ST.md': ST}


class TraceTestCase(unittest.TestCase):
    def check(self, files, confirmed=frozenset(), retired=None, exemptions=None):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        for rel, text in files.items():
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8')
        repo = lt.Repo(root, list(files))
        return lt.run_checks(repo, confirmed=confirmed, retired=retired or {},
                             exemptions=exemptions or {})

    def keys(self, *args, **kwargs):
        return [f.key for f in self.check(*args, **kwargs)]


class SlugTest(unittest.TestCase):
    def test_symbols_are_removed(self):
        self.assertEqual(lt.github_slug('FR-004: 3×3メッシュ結合解析オーケストレーション'),
                         'fr-004-33メッシュ結合解析オーケストレーション')
        self.assertEqual(lt.github_slug('2.2.4 SRS の FR/NFR との対応'), '224-srs-の-frnfr-との対応')
        self.assertEqual(lt.github_slug('`make lint` の [対象](x.md)'), 'make-lint-の-対象')

    def test_duplicate_headings_get_suffix(self):
        self.assertEqual(lt.anchors_of('# a\n\n# a\n'), {'a', 'a-1'})

    def test_html_anchor(self):
        self.assertIn('ur-001', lt.anchors_of('| <a id="ur-001"></a>x |\n'))


class LinkTest(TraceTestCase):
    def test_links_resolve(self):
        files = dict(BASE, **{'docs/a.md': '[x](20_SRS.md#fr-001-一) [y](#t)\n\n# t\n'})
        self.assertNotIn('T2', ' '.join(self.keys(files)))

    def test_broken_anchor(self):
        files = dict(BASE, **{'docs/a.md': '[x](20_SRS.md#fr-099-無い)\n'})
        self.assertIn('T2:docs/a.md->20_SRS.md#fr-099-無い', self.keys(files))

    def test_missing_file(self):
        files = dict(BASE, **{'docs/a.md': '[x](nothing.md)\n'})
        self.assertIn('T2:docs/a.md->nothing.md', self.keys(files))

    def test_same_file_anchor(self):
        files = dict(BASE, **{'docs/a.md': '[x](#none)\n'})
        self.assertIn('T2:docs/a.md->#none', self.keys(files))

    def test_inline_code_and_fence_are_ignored(self):
        files = dict(BASE, **{'docs/a.md': '`[x](#none)`\n\n```text\n[y](nothing.md)\n```\n'})
        self.assertNotIn('T2:docs/a.md->#none', self.keys(files))
        self.assertNotIn('T2:docs/a.md->nothing.md', self.keys(files))

    def test_id_label_must_match_anchor(self):
        files = dict(BASE, **{'docs/a.md': '[UR-001](10_URD.md#ur-002) [007](20_SRS.md#fr-001-一)\n'})
        keys = self.keys(files)
        self.assertIn('T2:docs/a.md->10_URD.md#ur-002:label', keys)
        self.assertFalse([k for k in keys if k.startswith('T2:docs/a.md->20_SRS.md')])

    def test_section_label_must_match_anchor(self):
        text = '[SRS §3.2](20_SRS.md#fr-001-一) [SRS §3.2](20_SRS.md#32-主要コンポーネント構成)\n'
        files = dict(BASE, **{'docs/a.md': text})
        keys = self.keys(files)
        self.assertIn('T2:docs/a.md->20_SRS.md#fr-001-一:label', keys)
        self.assertNotIn('T2:docs/a.md->20_SRS.md#32-主要コンポーネント構成:label', keys)

    def test_external_links_are_ignored(self):
        files = dict(BASE, **{'docs/a.md': '[x](https://example.com/a#b)\n'})
        self.assertFalse([k for k in self.keys(files) if k.startswith('T2:docs/a.md')])



class StageTest(TraceTestCase):
    ADR = 'docs/decisions/ADR-X.md'

    def without(self, path):
        return {k: v for k, v in BASE.items() if k != path}

    def test_confirmed_stage_without_document(self):
        self.assertIn('T1:stage:HLD', self.keys(dict(BASE), confirmed={'SRS', 'HLD'}))

    def test_unconfirmed_stage_without_document_is_silent(self):
        self.assertEqual(self.check(dict(BASE), confirmed={'SRS'}), [])

    def test_unknown_stage_name(self):
        keys = self.keys(dict(BASE), confirmed={'SRS', 'HDL', 'URD'})
        self.assertIn('T1:stage:HDL', keys)
        self.assertIn('T1:stage:URD', keys)

    def test_confirmed_srs_missing_is_a_finding_not_a_crash(self):
        keys = self.keys(self.without('docs/20_SRS.md'), confirmed={'SRS'})
        self.assertIn('T1:stage:SRS', keys)
        self.assertNotIn('T1:doc:docs/20_SRS.md', keys)

    def test_missing_urd_is_a_finding_not_a_crash(self):
        self.assertIn('T1:doc:docs/10_URD.md', self.keys(self.without('docs/10_URD.md')))

    def test_missing_base_document_cannot_be_exempted(self):
        files = dict(self.without('docs/10_URD.md'), **{self.ADR: '# X\n'})
        keys = self.keys(files, exemptions={'T1:doc:docs/10_URD.md': self.ADR})
        self.assertIn('T1:doc:docs/10_URD.md', keys)
        self.assertIn('T1:exemption:T1:doc:docs/10_URD.md', keys)

    def test_missing_stage_document_cannot_be_exempted(self):
        files = dict(BASE, **{self.ADR: '# X\n'})
        keys = self.keys(files, confirmed={'SRS', 'HLD'}, exemptions={'T1:stage:HLD': self.ADR})
        self.assertIn('T1:stage:HLD', keys)
        self.assertIn('T1:exemption:T1:stage:HLD', keys)


class SrsTest(TraceTestCase):
    def test_base_is_clean(self):
        self.assertEqual(self.check(BASE), [])

    def test_missing_declaration(self):
        srs = SRS.replace('- **対応 UR**: [UR-002](10_URD.md#ur-002)\n\n', '', 1)
        self.assertIn('T1:FR-002', self.keys(dict(BASE, **{'docs/20_SRS.md': srs})))

    def test_declaration_without_link(self):
        srs = SRS.replace('- **対応 UR**: [UR-002](10_URD.md#ur-002)', '- **対応 UR**: UR-002', 1)
        self.assertIn('T1:FR-002', self.keys(dict(BASE, **{'docs/20_SRS.md': srs})))

    def test_unknown_parent(self):
        urd = URD.replace('| <a id="ur-002"></a>[UR-002](#ur-002) | 二 |\n', '')
        self.assertIn('T2:FR-002->UR-002', self.keys(dict(BASE, **{'docs/10_URD.md': urd})))

    def test_gap_needs_retired_entry(self):
        files = {k: v.replace('FR-002', 'FR-003').replace('fr-002', 'fr-003') for k, v in BASE.items()}
        self.assertIn('T1:FR-002', self.keys(files))
        adr = 'docs/decisions/ADR-X.md'
        keys = self.keys(dict(files, **{adr: '# X\n'}), retired={'FR-002': adr})
        self.assertNotIn('T1:FR-002', keys)
        self.assertIn('T2:FR-002->' + adr, self.keys(files, retired={'FR-002': adr}))

    def test_retired_id_still_present(self):
        adr = 'docs/decisions/ADR-X.md'
        keys = self.keys(dict(BASE, **{adr: '# X\n'}), retired={'FR-002': adr})
        self.assertIn('T1:FR-002:retired', keys)

    def test_uncovered_ur_only_when_srs_confirmed(self):
        urd = URD + '| <a id="ur-003"></a>[UR-003](#ur-003) | 三 |\n'
        files = dict(BASE, **{'docs/10_URD.md': urd})
        self.assertIn('T3:SRS:UR-003', self.keys(files, confirmed={'SRS'}))
        self.assertNotIn('T3:SRS:UR-003', self.keys(files))

    def test_matrix_cell_mismatch(self):
        srs = SRS.replace('| [FR-002](#fr-002-二) | 二 | | ✅ |', '| [FR-002](#fr-002-二) | 二 | ✅ | ✅ |')
        self.assertIn('T4:SRS-matrix:FR-002', self.keys(dict(BASE, **{'docs/20_SRS.md': srs})))

    def test_matrix_row_missing(self):
        srs = SRS.replace('| [NFR-001](#nfr-001-非一) | 非一 | ✅ | |\n', '')
        self.assertIn('T4:SRS-matrix:NFR-001', self.keys(dict(BASE, **{'docs/20_SRS.md': srs})))

    def test_matrix_columns_mismatch(self):
        urd = URD + '| <a id="ur-003"></a>[UR-003](#ur-003) | 三 |\n'
        self.assertIn('T4:SRS-matrix:columns', self.keys(dict(BASE, **{'docs/10_URD.md': urd})))


class ExemptionTest(TraceTestCase):
    def test_exempted_with_adr(self):
        urd = URD + '| <a id="ur-003"></a>[UR-003](#ur-003) | 三 |\n'
        adr = 'docs/decisions/ADR-Y.md'
        files = dict(BASE, **{'docs/10_URD.md': urd, adr: '# Y\n'})
        keys = self.keys(files, confirmed={'SRS'}, exemptions={'T3:SRS:UR-003': adr})
        self.assertNotIn('T3:SRS:UR-003', keys)

    def test_exemption_without_adr(self):
        urd = URD + '| <a id="ur-003"></a>[UR-003](#ur-003) | 三 |\n'
        adr = 'docs/decisions/ADR-Y.md'
        files = dict(BASE, **{'docs/10_URD.md': urd})
        keys = self.keys(files, confirmed={'SRS'}, exemptions={'T3:SRS:UR-003': adr})
        self.assertIn('T3:SRS:UR-003', keys)
        self.assertIn('T2:exemption->' + adr, keys)


class StTest(TraceTestCase):
    def test_coverage_table_mismatch(self):
        st = ST.replace(', [NFR-001](20_SRS.md#nfr-001-非一)', '')
        self.assertIn('T4:ST-coverage:UR-001', self.keys(dict(BASE, **{'docs/70_ST.md': st})))

    def test_coverage_row_missing(self):
        st = ST.replace('| [UR-002](10_URD.md#ur-002) | 二 | [FR-002](20_SRS.md#fr-002-二) | `ST-FR-002-01` |\n', '')
        self.assertIn('T4:ST-coverage:UR-002', self.keys(dict(BASE, **{'docs/70_ST.md': st})))

    def test_unknown_parent(self):
        st = ST.replace('| `ST-NFR-001-01` | c |', '| `ST-NFR-001-01` | c |\n| `ST-FR-009-01` | d |')
        self.assertIn('T2:ST-FR-009-01', self.keys(dict(BASE, **{'docs/70_ST.md': st})))

    def test_bad_format_and_duplicate(self):
        st = ST.replace('| `ST-NFR-001-01` | c |',
                        '| `ST-NFR-001-01` | c |\n| `ST-FR-1-1` | d |\n| `ST-FR-001-01` | e |')
        keys = self.keys(dict(BASE, **{'docs/70_ST.md': st}))
        self.assertIn('T1:ST-FR-1-1', keys)
        self.assertIn('T1:ST-FR-001-01:重複', keys)

    def test_requirement_without_st_only_when_confirmed(self):
        st = ST.replace('| `ST-FR-002-01`（異常系） | b |\n', '')
        files = dict(BASE, **{'docs/70_ST.md': st})
        self.assertIn('T3:ST:FR-002', self.keys(files, confirmed={'ST'}))
        self.assertNotIn('T3:ST:FR-002', self.keys(files))

    def test_coverage_case_refs_resolve(self):
        row_end = '| `ST-FR-001-01` |\n'
        for ref, expected in (('`ST-FR-001-09`', 'ST-FR-001-09'), ('`ST-FR-009-*`', 'ST-FR-009-*'),
                              ('`ST-FR-001-01`〜`03`', 'ST-FR-001-03')):
            st = ST.replace(row_end, f'| {ref} |\n')
            keys = self.keys(dict(BASE, **{'docs/70_ST.md': st}))
            self.assertIn(f'T2:ST-coverage:UR-001->{expected}', keys)
        st = ST.replace(row_end, '| `ST-FR-001-*`, `ST-NFR-001-01` |\n')
        self.assertEqual(self.check(dict(BASE, **{'docs/70_ST.md': st})), [])

    def test_coverage_range_checks_every_number(self):
        st = ST.replace('| `ST-FR-001-01` | a |', '| `ST-FR-001-01` | a |\n| `ST-FR-001-03` | a3 |')
        st = st.replace('| `ST-FR-001-01` |\n', '| `ST-FR-001-01`〜`03` |\n')
        keys = self.keys(dict(BASE, **{'docs/70_ST.md': st}))
        self.assertIn('T2:ST-coverage:UR-001->ST-FR-001-02', keys)
        self.assertNotIn('T2:ST-coverage:UR-001->ST-FR-001-03', keys)


HLD = '''# HLD

## 2. アーキテクチャ

### 2.1 全体

- **対応 SRS**: [SRS §3.2](20_SRS.md#32-主要コンポーネント構成)
- **担当コンポーネント**: 全体

### 2.2 横断

- **対応 SRS**: なし（横断の設計）
- **担当コンポーネント**: C1・C2

## 3. FR 設計

### 3.1 FR-001 一

- **対応 SRS**: [FR-001](20_SRS.md#fr-001-一)
- **担当コンポーネント**: C1

#### 3.1.1 目的と範囲

本文。
'''


class HldTest(TraceTestCase):
    def files(self, hld=HLD):
        return dict(BASE, **{'docs/30_HLD.md': hld})

    def test_clean(self):
        self.assertEqual(self.check(self.files()), [])

    def test_missing_component(self):
        hld = HLD.replace('- **担当コンポーネント**: C1\n', '')
        self.assertIn('T1:HLD-3.1:担当コンポーネント', self.keys(self.files(hld)))

    def test_unknown_component(self):
        hld = HLD.replace('C1・C2', 'C1・C9')
        self.assertIn('T2:HLD-2.2->C9', self.keys(self.files(hld)))

    def test_declaration_without_link(self):
        hld = HLD.replace('- **対応 SRS**: [FR-001](20_SRS.md#fr-001-一)', '- **対応 SRS**: FR-001')
        self.assertIn('T1:HLD-3.1:対応 SRS', self.keys(self.files(hld)))

    def test_declaration_after_subheading_is_not_counted(self):
        hld = HLD.replace(
            '- **対応 SRS**: [FR-001](20_SRS.md#fr-001-一)\n- **担当コンポーネント**: C1\n\n#### 3.1.1 目的と範囲\n',
            '#### 3.1.1 目的と範囲\n\n- **対応 SRS**: [FR-001](20_SRS.md#fr-001-一)\n- **担当コンポーネント**: C1\n')
        keys = self.keys(self.files(hld))
        self.assertIn('T1:HLD-3.1:対応 SRS', keys)
        self.assertIn('T1:HLD-3.1:担当コンポーネント', keys)

    def test_uncovered_requirement_only_when_hld_confirmed(self):
        keys = self.keys(self.files(), confirmed={'HLD'})
        self.assertIn('T3:HLD:FR-002', keys)
        self.assertIn('T3:HLD:NFR-001', keys)
        self.assertNotIn('T3:HLD:FR-001', keys)
        self.assertNotIn('T3:HLD:FR-002', self.keys(self.files()))


LLD = '''# LLD

## 1. モジュール

### 1.1 一のモジュール

- **ID**: LLD-one
- **対応 HLD**: [3.1](30_HLD.md#31-fr-001-一)
- **ファイル**: `src/one.cpp`
'''

UT = '''# UT

| ID | 手順 |
|---|---|
| `UT-one-01` | a |
| `UT-one-02`（手動） | b |
'''


class LldTest(TraceTestCase):
    def files(self, **over):
        files = dict(BASE, **{
            'docs/30_HLD.md': HLD, 'docs/40_LLD.md': LLD, 'docs/50_UT.md': UT,
            'src/one.cpp': '// trace: LLD-one\nint one() { return 1; }\n',
            'tests/src/test_one.cpp': '// trace: UT-one-01\n',
        })
        files.update(over)
        return files

    def test_clean_when_confirmed(self):
        self.assertEqual(self.check(self.files(), confirmed={'LLD', 'UT'}), [])

    def test_missing_file_field(self):
        lld = LLD.replace('- **ファイル**: `src/one.cpp`\n', '')
        self.assertIn('T1:LLD-one:ファイル', self.keys(self.files(**{'docs/40_LLD.md': lld})))

    def test_file_not_in_git(self):
        lld = LLD.replace('`src/one.cpp`', '`src/one.cpp`・`src/two.cpp`')
        self.assertIn('T2:LLD-one->src/two.cpp', self.keys(self.files(**{'docs/40_LLD.md': lld})))

    def test_unknown_hld_section(self):
        lld = LLD.replace('[3.1](30_HLD.md#31-fr-001-一)', '[3.9](30_HLD.md#31-fr-001-一)')
        self.assertIn('T2:LLD-one->3.9', self.keys(self.files(**{'docs/40_LLD.md': lld})))

    def test_untraced_product_file_only_when_lld_confirmed(self):
        files = self.files(**{'scripts/tool.py': 'print(1)\n'})
        self.assertIn('T5:scripts/tool.py', self.keys(files, confirmed={'LLD'}))
        self.assertNotIn('T5:scripts/tool.py', self.keys(files))

    def test_trace_not_in_file_field(self):
        files = self.files(**{'src/extra.cpp': '// trace: LLD-one\n'})
        self.assertIn('T5:src/extra.cpp->LLD-one', self.keys(files, confirmed={'LLD'}))

    def test_file_field_without_trace(self):
        files = self.files(**{'src/one.cpp': 'int one() { return 1; }\n'})
        self.assertIn('T5:LLD-one->src/one.cpp', self.keys(files, confirmed={'LLD'}))

    def test_unknown_lld_in_code(self):
        files = self.files(**{'src/one.cpp': '// trace: LLD-one\n// trace: LLD-two\n'})
        self.assertIn('T2:src/one.cpp->LLD-two', self.keys(files, confirmed={'LLD'}))

    def test_hld_section_without_lld_when_confirmed(self):
        lld = LLD.replace('[3.1](30_HLD.md#31-fr-001-一)', '[2.1](30_HLD.md#21-全体)')
        self.assertIn('T3:LLD:3.1', self.keys(self.files(**{'docs/40_LLD.md': lld}), confirmed={'LLD'}))

    def test_unimplemented_automated_case(self):
        files = self.files(**{'tests/src/test_one.cpp': '// 空\n'})
        keys = self.keys(files, confirmed={'UT'})
        self.assertIn('T5:UT-one-01', keys)
        self.assertNotIn('T5:UT-one-02', keys)

    def test_unknown_case_in_test_code(self):
        files = self.files(**{'tests/src/test_one.cpp': '// trace: UT-one-01\n// trace: UT-one-09\n'})
        self.assertIn('T2:tests/src/test_one.cpp->UT-one-09', self.keys(files))

    def test_ut_for_unknown_module(self):
        ut = UT + '| `UT-two-01` | c |\n'
        self.assertIn('T2:UT-two-01', self.keys(self.files(**{'docs/50_UT.md': ut})))

    def test_trace_in_string_literal_is_ignored(self):
        files = self.files(**{'tests/scripts/test_x.py': "X = '// trace: UT-one-09'\n"})
        self.assertNotIn('T2:tests/scripts/test_x.py->UT-one-09', self.keys(files))

    def test_trace_in_multiline_string_is_ignored(self):
        files = self.files(**{'tests/scripts/test_y.py': "X = '''\n# trace: UT-one-09\n'''\n",
                              'tests/scripts/test_z.py': "# trace: UT-one-08\n"})
        keys = self.keys(files)
        self.assertNotIn('T2:tests/scripts/test_y.py->UT-one-09', keys)
        self.assertIn('T2:tests/scripts/test_z.py->UT-one-08', keys)

    def test_missing_id_in_module_section(self):
        lld = LLD.replace('- **ID**: LLD-one\n', '')
        self.assertIn('T1:LLD:5:ID', self.keys(self.files(**{'docs/40_LLD.md': lld})))

    def test_file_outside_code_scope(self):
        lld = LLD.replace('`src/one.cpp`', '`src/one.cpp`・`src/table.json`')
        files = self.files(**{'docs/40_LLD.md': lld, 'src/table.json': '{}\n'})
        self.assertIn('T5:LLD-one->src/table.json', self.keys(files, confirmed={'LLD'}))

    def test_untraced_test_file_when_tests_confirmed(self):
        files = self.files(**{'tests/src/helper.cpp': 'int helper;\n'})
        self.assertIn('T5:tests/src/helper.cpp', self.keys(files, confirmed={'UT'}))
        self.assertNotIn('T5:tests/src/helper.cpp', self.keys(files))

    def test_module_without_ut_when_confirmed(self):
        ut = UT.replace('| `UT-one-01` | a |\n| `UT-one-02`（手動） | b |\n', '')
        files = self.files(**{'docs/50_UT.md': ut, 'tests/src/test_one.cpp': '// 空\n'})
        self.assertIn('T3:UT:LLD-one', self.keys(files, confirmed={'UT'}))


class ParserHardeningTest(TraceTestCase):
    """実装完了時のレビュー（Codex）の指摘: 宣言・コメント・フェンスの解析の抜け"""

    def hld_files(self, hld):
        return dict(BASE, **{'docs/30_HLD.md': hld})

    def test_srs_declaration_in_code_span_is_not_a_parent(self):
        srs = SRS.replace('- **対応 UR**: [UR-002](10_URD.md#ur-002)',
                          '- **対応 UR**: `[UR-002](10_URD.md#ur-002)`', 1)
        self.assertIn('T1:FR-002', self.keys(dict(BASE, **{'docs/20_SRS.md': srs})))

    def test_srs_declaration_without_anchor_is_not_a_parent(self):
        srs = SRS.replace('[UR-002](10_URD.md#ur-002)', '[UR-002](10_URD.md)', 1)
        self.assertIn('T1:FR-002', self.keys(dict(BASE, **{'docs/20_SRS.md': srs})))

    def test_srs_declaration_to_wrong_document_is_not_a_parent(self):
        srs = SRS.replace('[UR-002](10_URD.md#ur-002)', '[UR-002](20_SRS.md#ur-002)', 1)
        self.assertIn('T1:FR-002', self.keys(dict(BASE, **{'docs/20_SRS.md': srs})))

    def test_srs_declaration_to_external_url_or_other_directory_is_not_a_parent(self):
        for target in ('https://example.invalid/10_URD.md', 'other/10_URD.md', '../10_URD.md'):
            srs = SRS.replace('[UR-002](10_URD.md#ur-002)', f'[UR-002]({target}#ur-002)', 1)
            self.assertIn('T1:FR-002', self.keys(dict(BASE, **{'docs/20_SRS.md': srs})), target)

    def test_srs_declaration_to_url_with_dotdot_is_not_a_parent(self):
        for target in ('https://example.invalid/../../10_URD.md', 'file:///x/../10_URD.md', '/10_URD.md'):
            srs = SRS.replace('[UR-002](10_URD.md#ur-002)', f'[UR-002]({target}#ur-002)', 1)
            self.assertIn('T1:FR-002', self.keys(dict(BASE, **{'docs/20_SRS.md': srs})), target)

    def test_srs_declaration_target_must_be_exactly_the_document(self):
        targets = ('?x/../10_URD.md', '\\//example.invalid/../../10_URD.md',
                   'https&colon;//example.invalid/../../10_URD.md', '10_urd.md', '10_URD.md?x',
                   'a/../10_URD.md', '%31%30_URD.md', '10_URD.md ', './/10_URD.md')
        for target in targets:
            srs = SRS.replace('[UR-002](10_URD.md#ur-002)', f'[UR-002]({target}#ur-002)', 1)
            self.assertIn('T1:FR-002', self.keys(dict(BASE, **{'docs/20_SRS.md': srs})), target)

    def test_srs_declaration_to_dot_relative_path_is_a_parent(self):
        srs = SRS.replace('[UR-002](10_URD.md#ur-002)', '[UR-002](./10_URD.md#ur-002)', 1)
        self.assertNotIn('T1:FR-002', self.keys(dict(BASE, **{'docs/20_SRS.md': srs})))

    def test_hld_declaration_in_code_span_is_not_a_parent(self):
        hld = HLD.replace('- **対応 SRS**: [FR-001](20_SRS.md#fr-001-一)',
                          '- **対応 SRS**: `[FR-001](20_SRS.md#fr-001-一)`')
        self.assertIn('T1:HLD-3.1:対応 SRS', self.keys(self.hld_files(hld)))

    def test_hld_section_label_without_anchor_is_not_a_parent(self):
        hld = HLD.replace('[SRS §3.2](20_SRS.md#32-主要コンポーネント構成)', '[SRS §3.2](20_SRS.md)')
        self.assertIn('T1:HLD-2.1:対応 SRS', self.keys(self.hld_files(hld)))

    def test_lld_declaration_in_code_span_is_not_a_parent(self):
        lld = LLD.replace('[3.1](30_HLD.md#31-fr-001-一)', '`[3.1](30_HLD.md#31-fr-001-一)`')
        files = dict(BASE, **{'docs/30_HLD.md': HLD, 'docs/40_LLD.md': lld})
        self.assertIn('T1:LLD-one:対応 HLD', self.keys(files))

    def test_four_backtick_fence_may_contain_three_backtick_example(self):
        text = ('````markdown\n```text\n[x](nothing.md)\n```\n[y](nothing2.md)\n````\n'
                '[z](nothing3.md)\n')
        keys = self.keys(dict(BASE, **{'docs/a.md': text}))
        self.assertIn('T2:docs/a.md->nothing3.md', keys)
        self.assertNotIn('T2:docs/a.md->nothing.md', keys)
        self.assertNotIn('T2:docs/a.md->nothing2.md', keys)

    def test_tilde_fence_is_a_code_block(self):
        text = '~~~\n[x](nothing.md)\n~~~\n[z](nothing3.md)\n'
        keys = self.keys(dict(BASE, **{'docs/a.md': text}))
        self.assertIn('T2:docs/a.md->nothing3.md', keys)
        self.assertNotIn('T2:docs/a.md->nothing.md', keys)

    def test_fence_closing_needs_matching_char_and_no_info_string(self):
        text = '```text\n```python\n[x](nothing.md)\n```\n[z](nothing3.md)\n'
        keys = self.keys(dict(BASE, **{'docs/a.md': text}))
        self.assertIn('T2:docs/a.md->nothing3.md', keys)
        self.assertNotIn('T2:docs/a.md->nothing.md', keys)

    def files_with_cpp(self, source):
        return dict(BASE, **{'docs/30_HLD.md': HLD, 'docs/40_LLD.md': LLD, 'docs/50_UT.md': UT,
                             'src/one.cpp': '// trace: LLD-one\n', 'tests/src/test_raw.cpp': source})

    def test_trace_in_cpp_raw_string_is_ignored(self):
        keys = self.keys(self.files_with_cpp('const char* s = R"(\n// trace: UT-one-09\n)";\n'))
        self.assertNotIn('T2:tests/src/test_raw.cpp->UT-one-09', keys)

    def test_trace_in_cpp_raw_string_with_delimiter_is_ignored(self):
        keys = self.keys(self.files_with_cpp('auto s = R"x(\n)"\n// trace: UT-one-09\n)x";\n'))
        self.assertNotIn('T2:tests/src/test_raw.cpp->UT-one-09', keys)

    def test_trace_in_cpp_string_and_block_comment(self):
        source = ('const char* u = "http://x"; // trace: UT-one-07\n'
                  '/* x\n * trace: UT-one-08\n */\n'
                  "int k = 1'000; // trace: UT-one-06\n")
        keys = self.keys(self.files_with_cpp(source))
        for case_id in ('UT-one-07', 'UT-one-08', 'UT-one-06'):
            self.assertIn(f'T2:tests/src/test_raw.cpp->{case_id}', keys)


if __name__ == '__main__':
    unittest.main()
