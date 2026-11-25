"""tools/lint_trace.py のテスト（標準ライブラリの unittest）"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
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
| CMP1 | 甲 |
| CMP2 | 乙 |

#### FR-001: 一

- **対応 UR**: [UR-001](10_URD.md#ur-001)

#### FR-002: 二

- **対応 UR**: [UR-002](10_URD.md#ur-002)

## 5. 非機能要件

| 特性 | 対応する副特性と NFR | NFR を持たない理由 |
|---|---|---|
| 機能適合性（Functional suitability） | 機能正確性（functional correctness）: [NFR-001](#nfr-001-非一) | — |
| 性能効率性（Performance efficiency） | — | 理由 |
| 互換性（Compatibility） | — | 理由 |
| 相互作用能力（Interaction capability） | — | 理由 |
| 信頼性（Reliability） | — | 理由 |
| セキュリティ（Security） | — | 理由 |
| 保守性（Maintainability） | — | 理由 |
| 柔軟性（Flexibility） | — | 理由 |
| 安全性（Safety） | — | 理由 |

### NFR-001: 非一

- **対応 UR**: [UR-001](10_URD.md#ur-001)

## 12. 要求追跡マトリクス

| FR/NFR | タイトル | [UR-001](10_URD.md#ur-001) | [UR-002](10_URD.md#ur-002) |
|:---|:---|:-:|:-:|
| [FR-001](#fr-001-一) | 一 | ✅ | |
| [FR-002](#fr-002-二) | 二 | | ✅ |
| [NFR-001](#nfr-001-非一) | 非一 | ✅ | |

## 13. 検証

| FR/NFR | 検証方法 | 検証先 |
|:---|:---|:---|
| [FR-001](#fr-001-一) | 試験 | [ST の FR-001](70_ST.md#fr-001-一) |
| [FR-002](#fr-002-二) | 試験・実演 | [ST の FR-002](70_ST.md#fr-002-二) |
| [NFR-001](#nfr-001-非一) | 分析 | [ST §3.8](70_ST.md#38-非機能要件) |
'''

ST = '''# ST

## 3. 第1部

#### FR-001: 一

| ID | 手順 |
|---|---|
| `ST-FR-001-01` | a |

#### FR-002: 二

| ID | 手順 |
|---|---|
| `ST-FR-002-01`（異常系） | b |

### 3.8 非機能要件

| ID | 手順 |
|---|---|
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
    def check(self, files, confirmed=frozenset(), implemented=frozenset(), retired=None, exemptions=None):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        for rel, text in files.items():
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8')
        repo = lt.Repo(root, list(files))
        return lt.run_checks(repo, confirmed=confirmed, implemented=implemented, retired=retired or {},
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
        self.assertEqual(set(lt.anchors_of('# a\n\n# a\n')), {'a', 'a-1'})

    def test_anchor_keeps_section_number(self):
        anchors = lt.anchors_of('# 3.11 a\n\n# 6. b\n\n# c\n')
        self.assertEqual(anchors, {'311-a': '3.11', '6-b': '6', 'c': None})

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

    def test_section_label_keeps_dots(self):
        heads = '# 3.11 a\n\n# 3.1.1 b\n\n'
        keys = self.keys(dict(BASE, **{
            'docs/a.md': heads + '[3.11](#311-a) [3.1.1](#311-b)\n',
            'docs/b.md': heads + '[3.1.1](#311-a) [3.11](#311-b)\n',
        }))
        self.assertNotIn('T2:docs/a.md->#311-a:label', keys)
        self.assertNotIn('T2:docs/a.md->#311-b:label', keys)
        self.assertIn('T2:docs/b.md->#311-a:label', keys)
        self.assertIn('T2:docs/b.md->#311-b:label', keys)

    def test_plain_number_label_must_match_numbered_heading(self):
        text = '# 6. a\n\n# 7. b\n\n[6](#7-b) [7](#7-b)\n'
        keys = self.keys(dict(BASE, **{'docs/a.md': text}))
        self.assertEqual([k for k in keys if k.endswith(':label')], ['T2:docs/a.md->#7-b:label'])

    def test_external_links_are_ignored(self):
        files = dict(BASE, **{'docs/a.md': '[x](https://example.com/a#b)\n'})
        self.assertFalse([k for k in self.keys(files) if k.startswith('T2:docs/a.md')])



class DuplicateTest(TraceTestCase):
    def test_duplicate_requirement_heading(self):
        srs = SRS.replace('### NFR-001: 非一', '#### FR-002: 二の重複\n\n### NFR-001: 非一')
        self.assertIn('T1:FR-002:重複', self.keys(dict(BASE, **{'docs/20_SRS.md': srs})))

    def test_duplicate_ur_anchor(self):
        urd = URD + '| <a id="ur-001"></a>UR-001 | 一の重複 |\n'
        self.assertIn('T1:UR-001:重複', self.keys(dict(BASE, **{'docs/10_URD.md': urd})))

    def test_ur_anchor_example_in_backtick_fence_is_not_counted(self):
        urd = URD + '\n```\n<a id="ur-001"></a>\n```\n'
        self.assertNotIn('T1:UR-001:重複', self.keys(dict(BASE, **{'docs/10_URD.md': urd})))

    def test_ur_anchor_example_in_tilde_fence_is_not_counted(self):
        urd = URD + '\n~~~\n<a id="ur-001"></a>\n~~~\n'
        self.assertNotIn('T1:UR-001:重複', self.keys(dict(BASE, **{'docs/10_URD.md': urd})))

    def test_ur_anchor_in_fence_is_not_a_requirement(self):
        urd = URD + '\n```\n<a id="ur-099"></a>\n```\n'
        keys = self.keys(dict(BASE, **{'docs/10_URD.md': urd}))
        self.assertFalse([k for k in keys if 'UR-099' in k])

    def test_no_duplicates_in_base(self):
        self.assertFalse([k for k in self.keys(dict(BASE)) if k.endswith(':重複')])


class ReadErrorTest(unittest.TestCase):
    def test_unreadable_files_are_findings(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        for rel, text in BASE.items():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_text(text, encoding='utf-8')
        (root / 'tests/src').mkdir(parents=True)
        (root / 'tests/src/bad.cpp').write_bytes(b'// \xff\n')
        repo = lt.Repo(root, list(BASE) + ['tests/src/bad.cpp', 'docs/gone.md'])
        keys = [f.key for f in lt.run_checks(repo, confirmed=frozenset(), retired={}, exemptions={})]
        self.assertIn('T1:tests/src/bad.cpp:read', keys)
        self.assertIn('T1:docs/gone.md:read', keys)

    def test_read_error_cannot_be_exempted(self):
        keys = [f.key for f in lt.check_unexemptable({'T1:docs/gone.md:read': 'docs/decisions/ADR-X.md'})]
        self.assertEqual(keys, ['T1:exemption:T1:docs/gone.md:read'])


class GapTest(TraceTestCase):
    """#114: 分岐ごとの負例"""

    def lld_files(self, lld):
        return dict(BASE, **{'docs/30_HLD.md': HLD, 'docs/40_LLD.md': lld, 'src/one.cpp': '// trace: LLD-one\n'})

    def test_hld_points_to_unknown_requirement(self):
        hld = HLD.replace('[FR-001]', '[FR-099]')
        self.assertIn('T2:HLD-4.1->FR-099', self.keys(dict(BASE, **{'docs/30_HLD.md': hld})))

    def test_lld_id_format(self):
        lld = LLD.replace('- **ID**: LLD-one', '- **ID**: LLD one')
        self.assertIn('T1:LLD:7:ID', self.keys(self.lld_files(lld)))

    def test_lld_duplicate_id(self):
        lld = LLD + '\n### 1.2 二つ目\n\n- **ID**: LLD-one\n'
        self.assertIn('T1:LLD-one:重複', self.keys(self.lld_files(lld)))

    def test_lld_without_hld_declaration(self):
        lld = '\n'.join(x for x in LLD.split('\n') if not x.startswith('- **対応 HLD**'))
        self.assertIn('T1:LLD-one:対応 HLD', self.keys(self.lld_files(lld)))

    def test_srs_matrix_missing(self):
        srs = SRS.replace('## 12. 要求追跡マトリクス', '## 12. 別の表')
        self.assertIn('T4:SRS-matrix:table', self.keys(dict(BASE, **{'docs/20_SRS.md': srs})))

    def test_srs_matrix_row_without_declaration(self):
        srs = SRS.replace('#### FR-002: 二\n\n- **対応 UR**', '#### FR-002: 二\n\n- **別のラベル**')
        self.assertIn('T4:SRS-matrix:FR-002', self.keys(dict(BASE, **{'docs/20_SRS.md': srs})))

    def test_python_that_does_not_tokenize_falls_back_to_lines(self):
        files = dict(BASE, **{'tests/scripts/test_bad.py': "x = '''\n# trace: UT-one-009\n"})
        self.assertIn('T2:tests/scripts/test_bad.py->UT-one-009', self.keys(files))

    def test_manual_mark_must_follow_the_id(self):
        ut = UT.replace('| `UT-one-001` | a |', '| `UT-one-001` 説明（手動） | a |')
        files = self.lld_files(LLD)
        files.update({'docs/50_UT.md': ut, 'tests/src/test_one.cpp': '// trace: UT-one-002\n'})
        self.assertIn('T5:UT-one-001', self.keys(files, confirmed={'SRS', 'HLD', 'LLD', 'UT'}, implemented={'UT'}))


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

    def test_missing_srs_without_confirming_it_is_a_finding(self):
        self.assertIn('T1:doc:docs/20_SRS.md', self.keys(self.without('docs/20_SRS.md')))

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


    def test_stage_needs_its_upper_stages(self):
        keys = self.keys(dict(BASE, **{'docs/50_UT.md': UT}), confirmed={'SRS', 'UT'})
        self.assertIn('T1:stage:UT:order', keys)

    def test_stage_needs_all_upper_stages_not_only_the_direct_one(self):
        keys = self.keys(dict(BASE, **{'docs/50_UT.md': UT}), confirmed={'SRS', 'LLD', 'UT'})
        self.assertIn('T1:stage:UT:order', keys)

    def test_st_needs_only_srs(self):
        self.assertNotIn('T1:stage:ST:order', self.keys(dict(BASE), confirmed={'SRS', 'ST'}))

    def test_stage_with_its_upper_stages_is_in_order(self):
        files = dict(BASE, **{'docs/30_HLD.md': HLD})
        self.assertNotIn('T1:stage:HLD:order', self.keys(files, confirmed={'SRS', 'HLD'}))

    def test_implemented_stage_must_be_confirmed(self):
        self.assertIn('T1:stage:ST:implemented', self.keys(dict(BASE), confirmed={'SRS'}, implemented={'ST'}))
        keys = self.keys(dict(BASE), confirmed={'SRS', 'ST'}, implemented={'ST'})
        self.assertNotIn('T1:stage:ST:implemented', keys)

    def test_implemented_stage_must_be_lld_or_a_test_level(self):
        files = dict(BASE, **{'docs/30_HLD.md': HLD})
        keys = self.keys(files, confirmed={'SRS', 'HLD'}, implemented={'HLD'})
        self.assertIn('T1:stage:HLD:implemented', keys)

    def test_lld_can_be_implemented_only_when_confirmed(self):
        files = dict(BASE, **{'docs/30_HLD.md': HLD, 'docs/40_LLD.md': LLD})
        self.assertIn('T1:stage:LLD:implemented', self.keys(files, confirmed={'SRS', 'HLD'}, implemented={'LLD'}))
        self.assertNotIn('T1:stage:LLD:implemented',
                         self.keys(files, confirmed={'SRS', 'HLD', 'LLD'}, implemented={'LLD'}))

    def test_implemented_stage_finding_cannot_be_exempted(self):
        files = dict(BASE, **{self.ADR: '# X\n'})
        keys = self.keys(files, confirmed={'SRS'}, implemented={'ST'},
                         exemptions={'T1:stage:ST:implemented': self.ADR})
        self.assertIn('T1:stage:ST:implemented', keys)
        self.assertIn('T1:exemption:T1:stage:ST:implemented', keys)

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


class VerifyTest(TraceTestCase):
    ROW_FR1 = '| [FR-001](#fr-001-一) | 試験 | [ST の FR-001](70_ST.md#fr-001-一) |\n'
    ROW_NFR1 = '| [NFR-001](#nfr-001-非一) | 分析 | [ST §3.8](70_ST.md#38-非機能要件) |\n'

    def srs(self, old, new):
        self.assertIn(old, SRS)
        return dict(BASE, **{'docs/20_SRS.md': SRS.replace(old, new, 1)})

    def texts(self, files, key):
        return [f.text for f in self.check(files) if f.key == key]

    def assert_text(self, files, key, part):
        texts = self.texts(files, key)
        self.assertTrue(any(part in t for t in texts), texts)

    def test_table_missing(self):
        files = dict(BASE, **{'docs/20_SRS.md': SRS.split('## 13. 検証')[0]})
        self.assertIn('T4:SRS-verify:table', self.keys(files))

    def test_row_missing(self):
        self.assert_text(self.srs(self.ROW_NFR1, ''), 'T4:SRS-verify:NFR-001', '行がありません')

    def test_row_duplicated(self):
        files = self.srs(self.ROW_FR1, self.ROW_FR1 + self.ROW_FR1)
        self.assert_text(files, 'T4:SRS-verify:FR-001', '2 つ以上')

    def test_row_without_heading(self):
        row = '| [FR-009](#fr-001-一) | 試験 | [ST の FR-001](70_ST.md#fr-001-一) |\n'
        files = self.srs(self.ROW_NFR1, self.ROW_NFR1 + row)
        self.assert_text(files, 'T4:SRS-verify:FR-009', '見出しがありません')

    def test_row_pipes_doubled(self):
        files = self.srs(self.ROW_FR1, '|' + self.ROW_FR1.rstrip('\n') + '|\n')
        self.assertIn('T4:SRS-verify:row', self.keys(files))

    def test_row_not_link(self):
        row = '| FR-001 | 試験 | [ST の FR-001](70_ST.md#fr-001-一) |\n'
        files = self.srs(self.ROW_NFR1, self.ROW_NFR1 + row)
        self.assertIn('T4:SRS-verify:row', self.keys(files))

    def test_row_extra_column(self):
        files = self.srs(self.ROW_FR1, self.ROW_FR1.replace(' |\n', ' | 余分 |\n'))
        self.assertIn('T4:SRS-verify:row', self.keys(files))

    def test_row_two_ids(self):
        files = self.srs('| [FR-001](#fr-001-一) | 試験 |', '| [FR-001](#fr-001-一)・[FR-002](#fr-002-二) | 試験 |')
        self.assertIn('T4:SRS-verify:row', self.keys(files))

    def test_row_same_id_twice(self):
        files = self.srs('| [FR-001](#fr-001-一) | 試験 |', '| [FR-001](#fr-001-一)[FR-001](#fr-001-一) | 試験 |')
        self.assertIn('T4:SRS-verify:row', self.keys(files))

    def test_row_link_other_file(self):
        files = self.srs('| [FR-001](#fr-001-一) | 試験 |', '| [FR-001](70_ST.md#fr-001-一) | 試験 |')
        self.assertIn('T4:SRS-verify:row', self.keys(files))

    def test_unknown_method(self):
        files = self.srs('| 試験・実演 | [ST の FR-002]', '| 確認 | [ST の FR-002]')
        self.assert_text(files, 'T4:SRS-verify:FR-002', '検証方法')

    def test_empty_method(self):
        files = self.srs('| 試験・実演 | [ST の FR-002]', '|  | [ST の FR-002]')
        self.assert_text(files, 'T4:SRS-verify:FR-002', '検証方法')

    def test_wrong_separator(self):
        files = self.srs('| 試験・実演 | [ST の FR-002]', '| 試験、実演 | [ST の FR-002]')
        self.assert_text(files, 'T4:SRS-verify:FR-002', '検証方法')

    def test_wrong_order(self):
        files = self.srs('| 試験・実演 | [ST の FR-002]', '| 実演・試験 | [ST の FR-002]')
        self.assert_text(files, 'T4:SRS-verify:FR-002', '検証方法')

    def test_duplicate_method(self):
        files = self.srs('| 試験・実演 | [ST の FR-002]', '| 試験・試験・実演 | [ST の FR-002]')
        self.assert_text(files, 'T4:SRS-verify:FR-002', '検証方法')

    def test_spaced_method(self):
        files = self.srs('| 試験・実演 | [ST の FR-002]', '| 試験 ・ 実演 | [ST の FR-002]')
        self.assert_text(files, 'T4:SRS-verify:FR-002', '検証方法')

    def test_combined_methods_pass(self):
        self.assertNotIn('T4:SRS-verify:FR-002', self.keys(BASE))

    def test_target_not_st(self):
        files = self.srs('[ST の FR-002](70_ST.md#fr-002-二)', '[UR-002](10_URD.md#ur-002)')
        self.assert_text(files, 'T4:SRS-verify:FR-002', 'アンカー付き')

    def test_target_without_anchor(self):
        files = self.srs('[ST の FR-002](70_ST.md#fr-002-二)', '[ST の FR-002](70_ST.md)')
        self.assert_text(files, 'T4:SRS-verify:FR-002', 'アンカー付き')

    def test_target_other_fr(self):
        files = self.srs('[ST の FR-002](70_ST.md#fr-002-二)', '[ST の FR-001](70_ST.md#fr-001-一)')
        self.assert_text(files, 'T4:SRS-verify:FR-002', 'テストケースを持つ ST の節')

    def test_target_extra_wrong_link(self):
        old = '[ST の FR-001](70_ST.md#fr-001-一) |'
        files = self.srs(old, old[:-2] + '[ST の FR-002](70_ST.md#fr-002-二) |')
        self.assert_text(files, 'T4:SRS-verify:FR-001', 'テストケースを持つ ST の節')

    def test_target_mixed_with_non_st_link(self):
        old = '[ST の FR-001](70_ST.md#fr-001-一) |'
        files = self.srs(old, old[:-2] + '・[UR-002](10_URD.md#ur-002) |')
        self.assert_text(files, 'T4:SRS-verify:FR-001', 'アンカー付き')

    def test_target_mixed_with_anchorless_link(self):
        old = '[ST の FR-001](70_ST.md#fr-001-一) |'
        files = self.srs(old, old[:-2] + '・[ST](70_ST.md) |')
        self.assert_text(files, 'T4:SRS-verify:FR-001', 'アンカー付き')

    def test_nfr_target_other_section(self):
        files = self.srs('[ST §3.8](70_ST.md#38-非機能要件)', '[ST §4](70_ST.md#4-第2部)')
        self.assert_text(files, 'T4:SRS-verify:NFR-001', 'テストケースを持つ ST の節')


class QualityTest(TraceTestCase):
    FS_ROW = ('| 機能適合性（Functional suitability） | 機能正確性（functional correctness）: '
              '[NFR-001](#nfr-001-非一) | — |\n')
    SAFETY_ROW = '| 安全性（Safety） | — | 理由 |\n'

    def srs(self, old, new):
        self.assertIn(old, SRS)
        return dict(BASE, **{'docs/20_SRS.md': SRS.replace(old, new, 1)})

    def assert_text(self, files, key, part):
        texts = [f.text for f in self.check(files) if f.key == key]
        self.assertTrue(any(part in t for t in texts), texts)

    def test_table_missing(self):
        head = '| 特性 | 対応する副特性と NFR | NFR を持たない理由 |\n'
        start = SRS.index(head)
        end = SRS.index(self.SAFETY_ROW) + len(self.SAFETY_ROW)
        files = dict(BASE, **{'docs/20_SRS.md': SRS[:start] + SRS[end:]})
        self.assertIn('T4:SRS-quality:table', self.keys(files))

    def test_row_missing(self):
        self.assert_text(self.srs(self.SAFETY_ROW, ''), 'T4:SRS-quality:Safety', '行がありません')

    def test_row_duplicated(self):
        files = self.srs(self.SAFETY_ROW, self.SAFETY_ROW + self.SAFETY_ROW)
        self.assert_text(files, 'T4:SRS-quality:Safety', '2 つ以上')

    def test_unknown_characteristic(self):
        files = self.srs('互換性（Compatibility）', '使用性（Usability）')
        self.assertIn('T4:SRS-quality:row', self.keys(files))

    def test_row_extra_column(self):
        files = self.srs(self.SAFETY_ROW, self.SAFETY_ROW.replace(' |\n', ' | 余分 |\n'))
        self.assertIn('T4:SRS-quality:row', self.keys(files))

    def test_nfr_unmapped(self):
        files = self.srs(self.FS_ROW, '| 機能適合性（Functional suitability） | — | 理由 |\n')
        self.assert_text(files, 'T4:SRS-quality:NFR-001', 'どの行にもありません')

    def test_unknown_nfr(self):
        files = self.srs('[NFR-001](#nfr-001-非一) | — |', '[NFR-001](#nfr-001-非一)・[NFR-009](#nfr-001-非一) | — |')
        self.assert_text(files, 'T4:SRS-quality:Functional suitability', 'SRS にありません')

    def test_reason_with_nfr(self):
        files = self.srs('[NFR-001](#nfr-001-非一) | — |', '[NFR-001](#nfr-001-非一) | 理由 |')
        self.assert_text(files, 'T4:SRS-quality:Functional suitability', '「—」にします')

    def test_no_nfr_no_reason(self):
        files = self.srs(self.SAFETY_ROW, '| 安全性（Safety） | — | — |\n')
        self.assert_text(files, 'T4:SRS-quality:Safety', '理由を書きます')

    def test_no_nfr_cell2_text(self):
        files = self.srs(self.SAFETY_ROW, '| 安全性（Safety） | 何か | 理由 |\n')
        self.assert_text(files, 'T4:SRS-quality:Safety', '理由を書きます')

    def test_header_changed(self):
        head = '| 特性 | 対応する副特性と NFR | NFR を持たない理由 |'
        files = self.srs(head, '| NFR を持たない理由 | 特性 | 対応する副特性と NFR |')
        self.assertIn('T4:SRS-quality:head', self.keys(files))

    def test_nfr_link_other_file(self):
        files = self.srs('[NFR-001](#nfr-001-非一) | — |', '[NFR-001](https://example.com/#x) | — |')
        self.assert_text(files, 'T4:SRS-quality:Functional suitability', 'ファイル名なし')

    def test_nfr_code_span(self):
        files = self.srs('[NFR-001](#nfr-001-非一) | — |', '[NFR-001](#nfr-001-非一)・`NFR-001` | — |')
        self.assert_text(files, 'T4:SRS-quality:Functional suitability', 'ファイル名なし')

    def test_nfr_code_span_link(self):
        old = '[NFR-001](#nfr-001-非一) | — |'
        files = self.srs(old, '[NFR-001](#nfr-001-非一)・`[NFR-001](#nfr-001-非一)` | — |')
        self.assert_text(files, 'T4:SRS-quality:Functional suitability', 'ファイル名なし')

    def test_nfr_link_extra_label(self):
        old = '[NFR-001](#nfr-001-非一) | — |'
        files = self.srs(old, '[NFR-001](#nfr-001-非一)・[NFR-001 補足](https://example.com/) | — |')
        self.assert_text(files, 'T4:SRS-quality:Functional suitability', 'ファイル名なし')

    def test_two_names_in_first_column(self):
        files = self.srs(self.SAFETY_ROW, '| 安全性（Safety）・使用性（Usability） | — | 理由 |\n')
        self.assertIn('T4:SRS-quality:row', self.keys(files))

    def test_header_pipes_doubled(self):
        head = '| 特性 | 対応する副特性と NFR | NFR を持たない理由 |'
        files = self.srs(head, '|' + head + '|')
        self.assertIn('T4:SRS-quality:head', self.keys(files))

    def test_row_pipes_doubled(self):
        files = self.srs(self.SAFETY_ROW, '|| 安全性（Safety） | — | 理由 ||\n')
        self.assertIn('T4:SRS-quality:row', self.keys(files))

    def test_nfr_only_in_reason(self):
        files = self.srs(self.FS_ROW, '| 機能適合性（Functional suitability） | — | [NFR-001](#nfr-001-非一) |\n')
        self.assert_text(files, 'T4:SRS-quality:NFR-001', 'どの行にもありません')


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

    def test_confirmed_st_has_t3_but_no_t5_until_implemented(self):
        st = ST.replace('| `ST-FR-002-01`（異常系） | b |\n', '')
        keys = self.keys(dict(BASE, **{'docs/70_ST.md': st}), confirmed={'SRS', 'ST'})
        self.assertIn('T3:ST:FR-002', keys)
        self.assertEqual([k for k in keys if k.startswith('T5:')], [])

    def test_implemented_st_reports_case_without_test_code(self):
        keys = self.keys(dict(BASE), confirmed={'SRS', 'ST'}, implemented={'ST'})
        self.assertIn('T5:ST-FR-001-01', keys)

    def test_untraced_test_file_without_lld_or_ut(self):
        files = dict(BASE, **{'tests/src/helper.cpp': 'int helper;\n'})
        self.assertIn('T5:tests/src/helper.cpp', self.keys(files, confirmed={'SRS', 'ST'}, implemented={'ST'}))

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


    def test_case_id_without_backquotes(self):
        st = ST.replace('| `ST-FR-001-01` | a |', '| ST-FR-001-01 | a |')
        self.assertIn('T1:ST-FR-001-01:コード表記', self.keys(dict(BASE, **{'docs/70_ST.md': st})))

    def test_case_number_00(self):
        st = ST.replace('`ST-NFR-001-01`', '`ST-NFR-001-00`')
        self.assertIn('T1:ST-NFR-001-00', self.keys(dict(BASE, **{'docs/70_ST.md': st})))

    def test_reversed_case_range(self):
        st = ST.replace('| `ST-FR-001-01` |\n', '| `ST-FR-001-03`〜`01` |\n')
        keys = self.keys(dict(BASE, **{'docs/70_ST.md': st}))
        self.assertIn('T1:ST-coverage:UR-001:ST-FR-001-03〜01', keys)

HLD = '''# HLD

## 2. アーキテクチャ

### 2.1 全体

- **対応 SRS**: [SRS §3.2](20_SRS.md#32-主要コンポーネント構成)
- **担当コンポーネント**: 全体

### 2.2 横断

- **対応 SRS**: なし（横断の設計）
- **担当コンポーネント**: CMP1・CMP2

## 4. FR 設計

### 4.1 FR-001 一

- **対応 SRS**: [FR-001](20_SRS.md#fr-001-一)
- **担当コンポーネント**: CMP1

#### 4.1.1 目的と範囲

本文。

## 6. 要求追跡マトリクス

| FR/NFR | タイトル | CMP1 | CMP2 | 設計の節 |
|:---|:---|:-:|:-:|:---|
| [FR-001](20_SRS.md#fr-001-一) | 一 | ✅ | | [4.1](#41-fr-001-一) |
| [FR-002](20_SRS.md#fr-002-二) | 二 | | | |
| [NFR-001](20_SRS.md#nfr-001-非一) | 非一 | | | |
'''

HLD_PROGRAM = HLD.replace('## 4. FR 設計', '''## 3. プログラム構造

### 3.1 CMP1 一

- **対応 SRS**: [FR-001](20_SRS.md#fr-001-一)
- **担当コンポーネント**: CMP1

## 4. FR 設計''').replace('- **担当コンポーネント**: CMP1・CMP2\n', '''- **担当コンポーネント**: CMP1・CMP2

#### 2.2.4 SRS の FR/NFR との対応

| コンポーネント ID | FR | 処理方式の節 |
|---|---|---|
| CMP1 | [FR-001](20_SRS.md#fr-001-一) | [4.1](#41-fr-001-一) |
''')

HLD_NFR = HLD.replace('| [NFR-001](20_SRS.md#nfr-001-非一) | 非一 | | | |',
                      '| [NFR-001](20_SRS.md#nfr-001-非一) | 非一 | ✅ | ✅ | [5.1](#51-nfr-001-非一) |') + '''
## 5. NFR 設計

### 5.1 NFR-001 非一

- **対応 SRS**: [NFR-001](20_SRS.md#nfr-001-非一)
- **担当コンポーネント**: 全体
'''


class HldTest(TraceTestCase):
    def files(self, hld=HLD):
        return dict(BASE, **{'docs/30_HLD.md': hld})

    def test_clean(self):
        self.assertEqual(self.check(self.files()), [])

    def test_missing_component(self):
        hld = HLD.replace('- **担当コンポーネント**: CMP1\n', '')
        self.assertIn('T1:HLD-4.1:担当コンポーネント', self.keys(self.files(hld)))

    def test_unknown_component(self):
        hld = HLD.replace('CMP1・CMP2', 'CMP1・CMP9')
        self.assertIn('T2:HLD-2.2->CMP9', self.keys(self.files(hld)))

    def test_declaration_without_link(self):
        hld = HLD.replace('- **対応 SRS**: [FR-001](20_SRS.md#fr-001-一)', '- **対応 SRS**: FR-001')
        self.assertIn('T1:HLD-4.1:対応 SRS', self.keys(self.files(hld)))

    def test_declaration_after_subheading_is_not_counted(self):
        hld = HLD.replace(
            '- **対応 SRS**: [FR-001](20_SRS.md#fr-001-一)\n- **担当コンポーネント**: CMP1\n\n#### 4.1.1 目的と範囲\n',
            '#### 4.1.1 目的と範囲\n\n- **対応 SRS**: [FR-001](20_SRS.md#fr-001-一)\n- **担当コンポーネント**: CMP1\n')
        keys = self.keys(self.files(hld))
        self.assertIn('T1:HLD-4.1:対応 SRS', keys)
        self.assertIn('T1:HLD-4.1:担当コンポーネント', keys)

    def test_uncovered_requirement_only_when_hld_confirmed(self):
        keys = self.keys(self.files(), confirmed={'HLD'})
        self.assertIn('T3:HLD:FR-002', keys)
        self.assertIn('T3:HLD:NFR-001', keys)
        self.assertNotIn('T3:HLD:FR-001', keys)
        self.assertNotIn('T3:HLD:FR-002', self.keys(self.files()))


    def test_duplicate_section_number(self):
        hld = HLD + '\n### 4.1 FR-001 二つ目\n'
        self.assertIn('T1:HLD-4.1:重複', self.keys(self.files(hld)))

    def test_program_chapter_section_is_clean(self):
        self.assertEqual(self.check(self.files(HLD_PROGRAM)), [])

    def test_program_chapter_section_needs_declarations(self):
        hld = HLD.replace('## 4. FR 設計', '## 3. プログラム構造\n\n### 3.1 CMP1 一\n\n本文。\n\n## 4. FR 設計')
        keys = self.keys(self.files(hld))
        self.assertIn('T1:HLD-3.1:対応 SRS', keys)
        self.assertIn('T1:HLD-3.1:担当コンポーネント', keys)

    def test_program_chapter_declaration_does_not_cover_requirement(self):
        hld = HLD_PROGRAM.replace('### 3.1 CMP1 一\n\n- **対応 SRS**: [FR-001](20_SRS.md#fr-001-一)',
                                  '### 3.1 CMP1 一\n\n- **対応 SRS**: [FR-002](20_SRS.md#fr-002-二)')
        self.assertIn('T3:HLD:FR-002', self.keys(self.files(hld), confirmed={'HLD'}))

    def test_nfr_chapter_declaration_covers_requirement(self):
        self.assertNotIn('T3:HLD:NFR-001', self.keys(self.files(HLD_NFR), confirmed={'HLD'}))

    def test_program_chapter_declaration_rejects_nfr(self):
        hld = HLD_PROGRAM.replace(
            '### 3.1 CMP1 一\n\n- **対応 SRS**: [FR-001](20_SRS.md#fr-001-一)',
            '### 3.1 CMP1 一\n\n- **対応 SRS**: [FR-001](20_SRS.md#fr-001-一)・[NFR-001](20_SRS.md#nfr-001-非一)')
        keys = self.keys(self.files(hld))
        self.assertEqual(keys, ['T1:HLD-3.1:対応 SRS:NFR-001'])

    def test_nfr_chapter_declaration_is_not_rejected(self):
        self.assertFalse([k for k in self.keys(self.files(HLD_NFR)) if ':対応 SRS:NFR-' in k])

    def test_program_chapter_unknown_nfr_is_rejected(self):
        hld = HLD_PROGRAM.replace(
            '### 3.1 CMP1 一\n\n- **対応 SRS**: [FR-001](20_SRS.md#fr-001-一)',
            '### 3.1 CMP1 一\n\n- **対応 SRS**: [FR-001](20_SRS.md#fr-001-一)・[NFR-999](20_SRS.md#nfr-999-無い)')
        keys = self.keys(self.files(hld))
        self.assertIn('T1:HLD-3.1:対応 SRS:NFR-999', keys)
        self.assertIn('T2:HLD-3.1->NFR-999', keys)


HLD_TWO_SECTIONS = HLD.replace('- **対応 SRS**: なし（横断の設計）\n- **担当コンポーネント**: CMP1・CMP2',
                               '- **対応 SRS**: [FR-001](20_SRS.md#fr-001-一)\n- **担当コンポーネント**: CMP1・CMP2')


class HldMatrixTest(TraceTestCase):
    def files(self, hld=HLD):
        return dict(BASE, **{'docs/30_HLD.md': hld})

    def test_clean(self):
        self.assertEqual(self.check(self.files()), [])

    def test_table_missing(self):
        hld = HLD.split('\n## 6. 要求追跡マトリクス')[0] + '\n'
        self.assertIn('T4:HLD-matrix:table', self.keys(self.files(hld)))

    def test_no_hld_no_finding(self):
        self.assertNotIn('T4:HLD-matrix:table', self.keys(dict(BASE)))

    def test_mark_mismatch(self):
        hld = HLD.replace('| [FR-001](20_SRS.md#fr-001-一) | 一 | ✅ | |',
                          '| [FR-001](20_SRS.md#fr-001-一) | 一 | | ✅ |')
        self.assertIn('T4:HLD-matrix:FR-001', self.keys(self.files(hld)))

    def test_sections_mismatch(self):
        hld = HLD.replace('| ✅ | | [4.1](#41-fr-001-一) |', '| ✅ | | |')
        keys = self.keys(self.files(hld))
        self.assertIn('T4:HLD-matrix:FR-001:sections', keys)
        self.assertNotIn('T4:HLD-matrix:FR-001', keys)

    def test_section_link_to_other_document(self):
        hld = HLD.replace('| ✅ | | [4.1](#41-fr-001-一) |', '| ✅ | | [4.1](20_SRS.md#fr-001-一) |')
        self.assertIn('T4:HLD-matrix:FR-001:sections', self.keys(self.files(hld)))

    def test_row_missing(self):
        hld = HLD.replace('| [FR-002](20_SRS.md#fr-002-二) | 二 | | | |\n', '')
        self.assertIn('T4:HLD-matrix:FR-002', self.keys(self.files(hld)))

    def test_duplicate_row(self):
        row = '| [FR-002](20_SRS.md#fr-002-二) | 二 | | | |\n'
        hld = HLD.replace(row, row + row)
        self.assertIn('T4:HLD-matrix:FR-002:duplicate', self.keys(self.files(hld)))

    def test_row_for_unknown_requirement(self):
        hld = HLD + '| [FR-003](20_SRS.md#fr-003-三) | 三 | | | |\n'
        self.assertIn('T4:HLD-matrix:FR-003', self.keys(self.files(hld)))

    def test_row_without_requirement_link(self):
        hld = HLD + '| `FR-010` | 欠番 | | | |\n'
        self.assertIn('T4:HLD-matrix:row', self.keys(self.files(hld)))

    def test_row_with_two_requirements(self):
        hld = HLD.replace('| [FR-002](20_SRS.md#fr-002-二) | 二 |',
                          '| [FR-002](20_SRS.md#fr-002-二)・[NFR-001](20_SRS.md#nfr-001-非一) | 二 |')
        self.assertIn('T4:HLD-matrix:row', self.keys(self.files(hld)))

    def test_row_with_wrong_cell_count(self):
        hld = HLD.replace('| [FR-002](20_SRS.md#fr-002-二) | 二 | | | |', '| [FR-002](20_SRS.md#fr-002-二) | 二 | | |')
        self.assertIn('T4:HLD-matrix:FR-002', self.keys(self.files(hld)))

    def test_columns_mismatch(self):
        srs = SRS.replace('| CMP2 | 乙 |\n', '| CMP2 | 乙 |\n| CMP3 | 丙 |\n')
        files = dict(self.files(), **{'docs/20_SRS.md': srs})
        self.assertIn('T4:HLD-matrix:columns', self.keys(files))

    def test_columns_out_of_order(self):
        hld = HLD.replace('| FR/NFR | タイトル | CMP1 | CMP2 | 設計の節 |',
                          '| FR/NFR | タイトル | CMP2 | CMP1 | 設計の節 |')
        self.assertIn('T4:HLD-matrix:columns', self.keys(self.files(hld)))

    def test_all_components_mark_every_column(self):
        self.assertEqual(self.check(self.files(HLD_NFR)), [])
        hld = HLD_NFR.replace('| 非一 | ✅ | ✅ |', '| 非一 | ✅ | |')
        self.assertIn('T4:HLD-matrix:NFR-001', self.keys(self.files(hld)))

    def test_row_with_same_requirement_linked_twice(self):
        hld = HLD.replace('| [FR-002](20_SRS.md#fr-002-二) | 二 |',
                          '| [FR-002](20_SRS.md#fr-002-二)・[FR-002](20_SRS.md#fr-002-二) | 二 |')
        self.assertIn('T4:HLD-matrix:row', self.keys(self.files(hld)))

    def test_row_with_requirement_link_outside_srs(self):
        hld = HLD.replace('| [FR-002](20_SRS.md#fr-002-二) | 二 |', '| [FR-002](https://example.com/#fr-002-二) | 二 |')
        self.assertIn('T4:HLD-matrix:row', self.keys(self.files(hld)))

    def test_section_number_outside_link(self):
        hld = HLD.replace('| ✅ | | [4.1](#41-fr-001-一) |', '| ✅ | | [4.1](#41-fr-001-一)・4.2 |')
        self.assertIn('T4:HLD-matrix:FR-001:sections', self.keys(self.files(hld)))

    def test_sections_in_number_order(self):
        hld = HLD_TWO_SECTIONS.replace('| ✅ | | [4.1](#41-fr-001-一) |',
                                       '| ✅ | ✅ | [2.2](#22-横断)・[4.1](#41-fr-001-一) |')
        self.assertEqual(self.check(self.files(hld)), [])
        hld = HLD_TWO_SECTIONS.replace('| ✅ | | [4.1](#41-fr-001-一) |',
                                       '| ✅ | ✅ | [4.1](#41-fr-001-一)・[2.2](#22-横断) |')
        self.assertIn('T4:HLD-matrix:FR-001:sections', self.keys(self.files(hld)))

    def test_sections_without_separator(self):
        hld = HLD_TWO_SECTIONS.replace('| ✅ | | [4.1](#41-fr-001-一) |',
                                       '| ✅ | ✅ | [2.2](#22-横断)[4.1](#41-fr-001-一) |')
        self.assertIn('T4:HLD-matrix:FR-001:sections', self.keys(self.files(hld)))

    def test_component_cell_other_than_mark(self):
        hld = HLD.replace('| [FR-001](20_SRS.md#fr-001-一) | 一 | ✅ | |',
                          '| [FR-001](20_SRS.md#fr-001-一) | 一 | ✅（主） | |')
        self.assertIn('T4:HLD-matrix:FR-001', self.keys(self.files(hld)))

    def test_program_chapter_does_not_mark(self):
        hld = HLD_PROGRAM.replace(
            '### 3.1 CMP1 一\n\n- **対応 SRS**: [FR-001](20_SRS.md#fr-001-一)\n',
            '### 3.1 CMP1 一\n\n- **対応 SRS**: [FR-001](20_SRS.md#fr-001-一)・[FR-002](20_SRS.md#fr-002-二)\n')
        self.assertNotIn('T4:HLD-matrix:FR-002', self.keys(self.files(hld)))


PROGRAM_ROW = '| CMP1 | [FR-001](20_SRS.md#fr-001-一) | [4.1](#41-fr-001-一) |\n'


class HldProgramTableTest(TraceTestCase):
    def files(self, hld=HLD_PROGRAM):
        return dict(BASE, **{'docs/30_HLD.md': hld})

    def test_clean(self):
        self.assertEqual(self.check(self.files()), [])

    def test_no_program_chapter_needs_no_table(self):
        self.assertNotIn('T4:HLD-program:table', self.keys(self.files(HLD)))

    def test_table_missing(self):
        hld = HLD_PROGRAM.split('\n#### 2.2.4 ')[0] + '\n' + HLD_PROGRAM.split(PROGRAM_ROW, 1)[1]
        self.assertIn('T4:HLD-program:table', self.keys(self.files(hld)))

    def test_fr_mismatch(self):
        hld = HLD_PROGRAM.replace('| CMP1 | [FR-001](20_SRS.md#fr-001-一) |',
                                  '| CMP1 | [FR-002](20_SRS.md#fr-002-二) |')
        self.assertIn('T4:HLD-program:CMP1', self.keys(self.files(hld)))

    def test_sections_mismatch(self):
        hld = HLD_PROGRAM.replace(PROGRAM_ROW, '| CMP1 | [FR-001](20_SRS.md#fr-001-一) | |\n')
        keys = self.keys(self.files(hld))
        self.assertIn('T4:HLD-program:CMP1:sections', keys)
        self.assertNotIn('T4:HLD-program:CMP1', keys)

    def test_section_link_to_other_document(self):
        hld = HLD_PROGRAM.replace(PROGRAM_ROW,
                                  '| CMP1 | [FR-001](20_SRS.md#fr-001-一) | [4.1](20_SRS.md#fr-001-一) |\n')
        self.assertIn('T4:HLD-program:CMP1:sections', self.keys(self.files(hld)))

    def test_section_number_outside_link(self):
        hld = HLD_PROGRAM.replace(PROGRAM_ROW, '| CMP1 | [FR-001](20_SRS.md#fr-001-一) | [4.1](#41-fr-001-一)・4.2 |\n')
        self.assertIn('T4:HLD-program:CMP1:sections', self.keys(self.files(hld)))

    def test_fr_cell_with_extra_text(self):
        hld = HLD_PROGRAM.replace(PROGRAM_ROW,
                                  '| CMP1 | [FR-001](20_SRS.md#fr-001-一)・`FR-002` | [4.1](#41-fr-001-一) |\n')
        self.assertIn('T4:HLD-program:CMP1', self.keys(self.files(hld)))

    def test_fr_cell_with_link_outside_srs(self):
        hld = HLD_PROGRAM.replace(PROGRAM_ROW,
                                  '| CMP1 | [FR-001](20_SRS.md#fr-001-一)・[FR-002](https://example.com/#fr-002-二) '
                                  '| [4.1](#41-fr-001-一) |\n')
        self.assertIn('T4:HLD-program:CMP1', self.keys(self.files(hld)))

    def test_fr_cell_with_nfr(self):
        hld = HLD_PROGRAM.replace(PROGRAM_ROW,
                                  '| CMP1 | [FR-001](20_SRS.md#fr-001-一)・[NFR-001](20_SRS.md#nfr-001-非一) '
                                  '| [4.1](#41-fr-001-一) |\n')
        self.assertIn('T4:HLD-program:CMP1', self.keys(self.files(hld)))

    def test_duplicate_section(self):
        hld = HLD_PROGRAM.replace(PROGRAM_ROW, '| CMP1 | [FR-001](20_SRS.md#fr-001-一) '
                                               '| [4.1](#41-fr-001-一)・[4.1](#41-fr-001-一) |\n')
        self.assertIn('T4:HLD-program:CMP1:sections', self.keys(self.files(hld)))

    def test_sections_need_not_be_in_number_order(self):
        hld = HLD_PROGRAM.replace('- **対応 SRS**: なし（横断の設計）\n- **担当コンポーネント**: CMP1・CMP2',
                                  '- **対応 SRS**: [FR-001](20_SRS.md#fr-001-一)\n- **担当コンポーネント**: CMP1・CMP2')
        hld = hld.replace('| ✅ | | [4.1](#41-fr-001-一) |', '| ✅ | ✅ | [2.2](#22-横断)・[4.1](#41-fr-001-一) |')
        hld = hld.replace(PROGRAM_ROW,
                          '| CMP1 | [FR-001](20_SRS.md#fr-001-一) | [4.1](#41-fr-001-一)・[2.2](#22-横断) |\n')
        self.assertEqual(self.check(self.files(hld)), [])

    def test_row_with_wrong_cell_count(self):
        hld = HLD_PROGRAM.replace(PROGRAM_ROW, '| CMP1 | [FR-001](20_SRS.md#fr-001-一) |\n')
        self.assertIn('T4:HLD-program:CMP1', self.keys(self.files(hld)))

    def test_columns_mismatch(self):
        hld = HLD_PROGRAM.replace('| コンポーネント ID | FR | 処理方式の節 |',
                                  '| 処理方式の節 | FR | コンポーネント ID |')
        self.assertIn('T4:HLD-program:columns', self.keys(self.files(hld)))

    def test_row_missing(self):
        hld = HLD_PROGRAM.replace(PROGRAM_ROW, '')
        self.assertIn('T4:HLD-program:CMP1', self.keys(self.files(hld)))

    def test_duplicate_row(self):
        hld = HLD_PROGRAM.replace(PROGRAM_ROW, PROGRAM_ROW + PROGRAM_ROW)
        self.assertIn('T4:HLD-program:CMP1:duplicate', self.keys(self.files(hld)))

    def test_row_without_program_chapter_section(self):
        hld = HLD_PROGRAM.replace(PROGRAM_ROW, PROGRAM_ROW + '| CMP2 | [FR-002](20_SRS.md#fr-002-二) | |\n')
        self.assertIn('T4:HLD-program:CMP2', self.keys(self.files(hld)))

    def test_unknown_component_row(self):
        hld = HLD_PROGRAM.replace(PROGRAM_ROW, PROGRAM_ROW + '| CMP9 | | |\n')
        self.assertIn('T4:HLD-program:row', self.keys(self.files(hld)))

    def test_shared_section_adds_no_row(self):
        hld = HLD_PROGRAM.replace('## 4. FR 設計', '''### 3.9 共通部品

- **対応 SRS**: なし（横断の設計）
- **担当コンポーネント**: CMP1・CMP2

## 4. FR 設計''', 1)
        self.assertEqual(self.check(self.files(hld)), [])


LLD = '''# LLD

## 1. モジュール

### 1.1 一のモジュール

- **ID**: LLD-one
- **対応 HLD**: [4.1](30_HLD.md#41-fr-001-一)
- **ファイル**: `src/one.cpp`
'''

LLD_UT = LLD + '''
#### 1.1.5 UT 候補

| ID | 確かめること |
|---|---|
| `UT-one-001` | a |
| `UT-one-002`（手動） | b |

##### 群（UT 候補）

| ID | 確かめること |
|---|---|
| `UT-one-003` | c |
| `UT-one-009` | d |
| `UT-one-008` | e |
'''

LLD_TWO = '''
### 1.2 二のモジュール

- **ID**: LLD-two
- **対応 HLD**: [4.1](30_HLD.md#41-fr-001-一)
- **ファイル**: `src/two.cpp`

#### 1.2.5 UT 候補

| ID | 確かめること |
|---|---|
'''

LLD_REF = LLD + '''
#### 1.1.5 UT 候補

ケースは単体テスト仕様書の [1.1](50_UT.md#11-一)（`UT-one-001`〜`UT-one-002`）にある。
'''

UT = '''# UT

### 1.1 一

| ID | 手順 |
|---|---|
| `UT-one-001` | a |
| `UT-one-002`（手動） | b |
'''


HLD_SEAM = HLD_PROGRAM.replace('- **担当コンポーネント**: CMP1\n\n## 4. FR 設計', '''- **担当コンポーネント**: CMP1

#### 3.1.5 結合のつなぎ目

**内部結合**

| ID | つなぎ目 | 渡すもの | 確かめること |
|---|---|---|---|
| `CMP1-INT1` | a → b | x | y |

**外部結合**

| ID | つなぎ目 | 渡すもの | 確かめること |
|---|---|---|---|
| `CMP1-EXT1` | c → a | z | w |

## 4. FR 設計''')

ST_MOVED = ST.replace('`ST-FR-002-01`（異常系）', '`ST-FR-002-01`（異常系。UT/IT で実施）')

IT = '''# IT

## 3. 第1部 内部結合

#### CMP1-INT1

| ID | 前提条件 | 手順 | 期待結果 | 合否判定基準 |
|---|---|---|---|---|
| `IT-CMP1-INT1-01` | a | b | c | d |

## 4. 第2部 外部結合

#### CMP1-EXT1

| ID | 前提条件 | 手順 | 期待結果 | 合否判定基準 |
|---|---|---|---|---|
| `IT-CMP1-EXT1-01` | a | b | c | d |

## 5. ST から移したケースの対応表

| ST のケース | 移した先 | 理由 |
|---|---|---|
| `ST-FR-002-01` | `IT-CMP1-EXT1-01` | r |
'''

TO_UT = 'UT（`50_UT.md` で作る）'


class ItTest(TraceTestCase):
    def files(self, **over):
        files = dict(BASE, **{'docs/30_HLD.md': HLD_SEAM, 'docs/60_IT.md': IT, 'docs/70_ST.md': ST_MOVED})
        files.update(over)
        return files

    def it_keys(self, files, **kwargs):
        return [k for k in self.keys(files, **kwargs) if 'IT' in k]

    def test_clean(self):
        self.assertEqual(self.check(self.files()), [])

    def test_bad_format(self):
        it = IT.replace('`IT-CMP1-INT1-01`', '`IT-CMP9-INT1-01`').replace('`IT-CMP1-EXT1-01` | a', '`IT-foo-01` | a')
        keys = self.it_keys(self.files(**{'docs/60_IT.md': it}))
        self.assertIn('T1:IT-CMP9-INT1-01', keys)
        self.assertIn('T1:IT-foo-01', keys)

    def test_unknown_seam(self):
        it = IT.replace('`IT-CMP1-INT1-01`', '`IT-CMP1-INT2-01`')
        self.assertIn('T2:IT-CMP1-INT2-01', self.it_keys(self.files(**{'docs/60_IT.md': it})))

    def test_seams_only_from_seam_tables(self):
        hld = HLD_SEAM.replace('#### 3.1.5 結合のつなぎ目', '#### 3.1.4 共通部品\n\n| ID | 説明 |\n|---|---|\n'
                               '| `CMP1-INT8` | 別の小節 |\n\n#### 3.1.5 結合のつなぎ目')
        it = IT.replace('`IT-CMP1-INT1-01`', '`IT-CMP1-INT8-01`')
        self.assertIn('T2:IT-CMP1-INT8-01', self.it_keys(self.files(**{'docs/30_HLD.md': hld, 'docs/60_IT.md': it})))

    def test_seam_table_under_subheading(self):
        hld = HLD_SEAM.replace('**外部結合**', '##### 補足\n\n| ID | つなぎ目 | 渡すもの | 確かめること |\n'
                               '|---|---|---|---|\n| `CMP1-INT5` | d → e | v | u |\n\n**外部結合**')
        files = self.files(**{'docs/30_HLD.md': hld})
        self.assertIn('T3:IT:CMP1-INT5', self.it_keys(files, confirmed={'SRS', 'HLD', 'IT'}))
        self.assertNotIn('T3:IT:CMP1-EXT1', self.it_keys(files, confirmed={'SRS', 'HLD', 'IT'}))

    def test_seam_without_it_only_when_confirmed(self):
        it = IT.replace('| `IT-CMP1-EXT1-01` | a | b | c | d |\n', '').replace('`IT-CMP1-EXT1-01` | r', TO_UT + ' | r')
        files = self.files(**{'docs/60_IT.md': it})
        self.assertIn('T3:IT:CMP1-EXT1', self.it_keys(files, confirmed={'SRS', 'HLD', 'IT'}))
        self.assertNotIn('T3:IT:CMP1-EXT1', self.it_keys(files))

    def test_confirmed_it_has_no_t5_until_implemented(self):
        confirmed = {'SRS', 'HLD', 'IT'}
        self.assertEqual([k for k in self.keys(self.files(), confirmed=confirmed) if k.startswith('T5:')], [])
        self.assertIn('T5:IT-CMP1-INT1-01', self.keys(self.files(), confirmed=confirmed, implemented={'IT'}))

    def test_t5_is_selective_by_implemented_level(self):
        confirmed = {'SRS', 'HLD', 'IT', 'ST'}
        keys = self.keys(self.files(), confirmed=confirmed, implemented={'IT'})
        self.assertIn('T5:IT-CMP1-INT1-01', keys)
        self.assertNotIn('T5:ST-FR-001-01', keys)
        keys = self.keys(self.files(), confirmed=confirmed, implemented={'ST'})
        self.assertIn('T5:ST-FR-001-01', keys)
        self.assertNotIn('T5:IT-CMP1-INT1-01', keys)

    def test_moved_row_missing(self):
        st = ST_MOVED.replace('`ST-FR-001-01` | a', '`ST-FR-001-01`（UT/IT で実施） | a')
        self.assertIn('T4:IT-moved:ST-FR-001-01', self.it_keys(self.files(**{'docs/70_ST.md': st})))

    def test_moved_row_without_mark(self):
        it = IT + '| `ST-NFR-001-01` | ' + TO_UT + ' | r |\n'
        self.assertIn('T4:IT-moved:ST-NFR-001-01', self.it_keys(self.files(**{'docs/60_IT.md': it})))

    def test_mark_outside_note_is_not_counted(self):
        st = ST_MOVED.replace('`ST-FR-001-01` | a', '`ST-FR-001-01` | UT/IT で実施')
        self.assertNotIn('T4:IT-moved:ST-FR-001-01', self.it_keys(self.files(**{'docs/70_ST.md': st})))

    def test_mark_must_be_an_item_in_parentheses(self):
        for note in ('（境界値）UT/IT で実施', '（UT/IT で実施しない）'):
            st = ST_MOVED.replace('`ST-FR-001-01` | a', f'`ST-FR-001-01`{note} | a')
            self.assertNotIn('T4:IT-moved:ST-FR-001-01', self.it_keys(self.files(**{'docs/70_ST.md': st})))

    def test_moved_refs_resolve(self):
        it = IT.replace('| `ST-FR-002-01` | `IT-CMP1-EXT1-01` | r |',
                        '| `ST-FR-002-01` | `IT-CMP1-EXT1-02` | r |\n| `ST-FR-002-09` | ' + TO_UT + ' | r |')
        keys = self.it_keys(self.files(**{'docs/60_IT.md': it}))
        self.assertIn('T2:IT-moved:ST-FR-002-01->IT-CMP1-EXT1-02', keys)
        self.assertIn('T2:IT-moved:ST-FR-002-09', keys)

    def test_moved_destination_form(self):
        for ok in (TO_UT, '`IT-CMP1-EXT1-01`・`IT-CMP1-INT1-01`'):
            it = IT.replace('`IT-CMP1-EXT1-01` | r', ok + ' | r')
            self.assertEqual(self.check(self.files(**{'docs/60_IT.md': it})), [], ok)
        for bad in ('あとで', '`IT-CMP1-EXT1-01` と `IT-CMP1-EXT1-99', '`ST-FR-001-01`', ''):
            it = IT.replace('`IT-CMP1-EXT1-01` | r', bad + ' | r')
            self.assertIn('T1:IT-moved:ST-FR-002-01', self.it_keys(self.files(**{'docs/60_IT.md': it})), bad)

    def test_moved_source_cell_form(self):
        it = IT.replace('| `ST-FR-002-01` | `IT', '| `ST-FR-002-01` 補足 | `IT')
        self.assertIn('T1:IT-moved:`ST-FR-002-01` 補足', self.it_keys(self.files(**{'docs/60_IT.md': it})))

    def test_moved_duplicate_row(self):
        it = IT + '| `ST-FR-002-01` | ' + TO_UT + ' | r |\n'
        self.assertIn('T1:IT-moved:ST-FR-002-01:重複', self.it_keys(self.files(**{'docs/60_IT.md': it})))

    def test_seam_row_with_note_is_flagged(self):
        hld = HLD_SEAM.replace('| `CMP1-INT1` | a → b |', '| `CMP1-INT1`（補足） | a → b |')
        self.assertIn('T1:HLD-seam-row:`CMP1-INT1`（補足）', self.keys(self.files(**{'docs/30_HLD.md': hld})))

    def test_seam_row_outside_seam_section_is_flagged(self):
        hld = HLD_SEAM.replace('#### 3.1.5 結合のつなぎ目', '#### 3.1.4 共通部品\n\n| ID | 説明 |\n|---|---|\n'
                               '| `CMP1-INT8` | 別の小節 |\n\n#### 3.1.5 結合のつなぎ目')
        self.assertIn('T1:HLD-seam-outside:CMP1-INT8', self.keys(self.files(**{'docs/30_HLD.md': hld})))

    def test_no_seams_with_it_doc_is_flagged(self):
        self.assertIn('T1:HLD-seam:none', self.keys(self.files(**{'docs/30_HLD.md': HLD_PROGRAM})))
        self.assertNotIn('T1:HLD-seam:none', self.keys(dict(BASE, **{'docs/30_HLD.md': HLD_PROGRAM})))

    def test_moved_row_with_empty_source_is_flagged(self):
        it = IT + '|  | ' + TO_UT + ' | r |\n'
        self.assertIn('T1:IT-moved:', self.it_keys(self.files(**{'docs/60_IT.md': it})))

    def test_moved_separator_row_with_colons_is_skipped(self):
        head = '| ST のケース | 移した先 | 理由 |\n'
        it = IT.replace(head + '|---|---|---|', head + '|:--|:-:|--:|')
        self.assertEqual(self.check(self.files(**{'docs/60_IT.md': it})), [])

    def test_mark_in_nested_parentheses(self):
        st = ST.replace('`ST-FR-002-01`（異常系）', '`ST-FR-002-01`（境界値（N=4）。UT/IT で実施）')
        self.assertEqual(self.check(self.files(**{'docs/70_ST.md': st})), [])

    def test_nested_parentheses_do_not_hide_the_item_boundary(self):
        st = ST_MOVED.replace('`ST-FR-001-01` | a', '`ST-FR-001-01`（境界値（UT/IT で実施）） | a')
        self.assertNotIn('T4:IT-moved:ST-FR-001-01', self.it_keys(self.files(**{'docs/70_ST.md': st})))

    def st_ref(self, ref):
        row = '`ST-FR-002-01`（異常系。UT/IT で実施） | '
        return ST_MOVED.replace(row + 'b', row + f'IT の `{ref}` を参照')

    def test_it_case_ref_must_exist(self):
        st = self.st_ref('IT-CMP1-EXT1-02')
        self.assertIn('T2:IT-ref:IT-CMP1-EXT1-02', self.it_keys(self.files(**{'docs/70_ST.md': st})))
        it = IT.replace('| `IT-CMP1-EXT1-01` | a |', '| `IT-CMP1-EXT1-01` | `IT-CMP1-INT1-09` を実行した後 |')
        self.assertIn('T2:IT-ref:IT-CMP1-INT1-09', self.it_keys(self.files(**{'docs/60_IT.md': it})))

    def test_st_ref_to_it_must_be_a_moved_destination(self):
        st = self.st_ref('IT-CMP1-INT1-01')
        self.assertIn('T4:IT-ref:ST-FR-002-01->IT-CMP1-INT1-01', self.it_keys(self.files(**{'docs/70_ST.md': st})))
        st = self.st_ref('IT-CMP1-EXT1-01')
        self.assertEqual(self.check(self.files(**{'docs/70_ST.md': st})), [])

    def test_no_moved_check_without_it_doc(self):
        files = dict(BASE, **{'docs/30_HLD.md': HLD_SEAM, 'docs/70_ST.md': ST_MOVED})
        self.assertEqual([k for k in self.keys(files) if 'IT-moved' in k], [])



class LldTest(TraceTestCase):
    def files(self, **over):
        files = dict(BASE, **{
            'docs/30_HLD.md': HLD, 'docs/40_LLD.md': LLD_REF, 'docs/50_UT.md': UT,
            'src/one.cpp': '// trace: LLD-one\nint one() { return 1; }\n',
            'tests/src/test_one.cpp': '// trace: UT-one-001\n',
        })
        files.update(over)
        return files

    def moved_keys(self, lld, ut=UT):
        return [k for k in self.keys(self.files(**{'docs/40_LLD.md': lld, 'docs/50_UT.md': ut})) if ':UT-move:' in k]

    def test_ut_moved_clean(self):
        self.assertEqual(self.moved_keys(LLD_REF), [])

    def test_ut_moved_rows_and_cases(self):  # 規則 1
        lld = LLD_REF + '\n| ID | 確かめること |\n|---|---|\n| `UT-one-003` | c |\n'
        self.assertEqual(self.moved_keys(lld), ['T1:UT-move:LLD-one:二重'])

    def test_ut_moved_ref_without_cases(self):  # 規則 2（表もある小節に参照だけ足した）
        lld = LLD_UT + '\n[1.1](50_UT.md#11-一) も見る。\n'
        self.assertEqual(self.moved_keys(lld, ut='# UT\n\n### 1.1 一\n'), ['T2:UT-move:LLD-one->50_UT'])

    def test_ut_moved_cases_without_ref(self):  # 規則 3（小節が無い）
        self.assertEqual(self.moved_keys(LLD), ['T1:UT-move:LLD-one:参照'])

    def test_ut_moved_not_yet(self):  # 未移行（表だけ、50_UT.md にケースなし）
        self.assertEqual(self.moved_keys(LLD_UT, ut='# UT\n'), [])

    def test_ut_moved_deep_heading(self):  # 深い見出しの下の参照も小節の中
        lld = LLD + '\n#### 1.1.5 UT 候補\n\n##### 群（UT 候補）\n\n[1.1](50_UT.md#11-一) にある。\n'
        self.assertEqual(self.moved_keys(lld), [])

    def test_ut_moved_dot_slash(self):  # ./50_UT.md も ../docs/50_UT.md も参照（パスを正規化して解く）
        for target in ('./50_UT.md', '../docs/50_UT.md'):
            with self.subTest(target=target):
                self.assertEqual(self.moved_keys(LLD_REF.replace('(50_UT.md#', f'({target}#')), [])

    def test_ut_moved_other_number_not_ref(self):  # 番号の違う節へのリンクは参照でない
        ut = UT + '\n### 2.1 二\n'
        lld = LLD + '\n#### 1.1.5 UT 候補\n\n[2.1](50_UT.md#21-二) と同じ分け方。\n'
        self.assertEqual(self.moved_keys(lld, ut=ut), ['T1:UT-move:LLD-one:参照'])

    def test_ut_moved_link_in_table_or_code_not_ref(self):  # 表のセルとコード表記の中は参照でない
        lld = LLD + ('\n#### 1.1.5 UT 候補\n\n`[1.1](50_UT.md#11-一)` は書き方の例。\n\n'
                     '| 名 | 値 |\n|---|---|\n| a | [1.1](50_UT.md#11-一) |\n')
        self.assertIn('T1:UT-move:LLD-one:参照', self.moved_keys(lld))

    def test_ut_moved_link_outside_subsection_not_ref(self):  # 小節の外のリンクは参照でない
        lld = LLD + '\n#### 1.1.3 関数の細部\n\n[1.1](50_UT.md#11-一) を見る。\n'
        self.assertEqual(self.moved_keys(lld), ['T1:UT-move:LLD-one:参照'])

    def test_ut_moved_preparation_table_not_rows(self):  # 準備の表は表の行に数えない
        lld = LLD_REF + '\n- 準備:\n\n  | 名 | 値 |\n  |---|---|\n  | a | b |\n'
        self.assertEqual(self.moved_keys(lld), [])

    def test_ut_moved_hidden_link_not_ref(self):  # 表示されないリンク（コメント・エスケープ・画像）は参照でない
        ref = '[1.1](50_UT.md#11-一)'
        # `x` の後と、\ で逃がしたバッククォート（コード表記を始めない）の後の <!-- も、本物のコメントの始まり
        for hidden in (f'<!-- {ref} -->', f'<!--\n{ref}\n-->', f'\\{ref}', f'!{ref}',
                       f'`x` <!-- {ref} -->', f'\\` <!-- \\` {ref} -->', f'\\`\\` <!-- {ref} -->',
                       f'`x\n\n<!-- {ref} -->',  # 閉じないバッククォートは、空行（段落の切れ目）で終わる
                       # 段落の中で閉じないバッククォートは字のまま（同じ行の後のコメントも本物）。見出しも越えない
                       f'`x <!-- {ref} -->', f'x ` y <!-- c -->\n<!-- {ref} -->',
                       f'x ` y <!-- c -->\n##### 群\n<!-- {ref} -->',
                       f'`a {ref}\nb` の続き',  # 行をまたいで閉じるコード表記の中のリンクは表示されない
                       f'a | b\n---|---\nx ` y | z\n<!-- ` {ref} -->',  # 頭の | を省いた表の行も越えない
                       # 行頭の <!--（HTML のブロック）も段落を切る（前の行の閉じないバッククォートは字のまま）
                       f'x ` y\n<!-- ` {ref} -->', f'x ` y <!-- c -->\n<!-- ` {ref} -->'):
            with self.subTest(hidden=hidden):
                lld = LLD + f'\n#### 1.1.5 UT 候補\n\n{hidden} にある。\n'
                self.assertEqual(self.moved_keys(lld), ['T1:UT-move:LLD-one:参照'])

    def test_ut_moved_block_start_ends_code_span(self):  # 引用・区切り線も段落を切り、後ろの表示される参照を残す
        ref = '[1.1](50_UT.md#11-一)'
        for shown in (f'x ` y\n> {ref} `', f'x ` y\n***\n{ref} `', f'x ` y\n  > {ref} `', f'x ` y\n_ _ _\n{ref} `'):
            with self.subTest(shown=shown):
                lld = LLD + f'\n#### 1.1.5 UT 候補\n\n{shown} にある。\n'
                self.assertEqual(self.moved_keys(lld), [])

    def test_ut_moved_comment_opener_in_code_span_hides_nothing(self):  # コード表記の中の <!-- はコメントでない
        ref_part = LLD_REF[len(LLD):]
        for span in ('`<!--`', '``a `<!--` b``', '`<!--\nb`', '``a\n`<!--` b``'):  # 行をまたぐコード表記も
            with self.subTest(span=span):
                lld = LLD + f'\n中身に {span} を書かない。\n' + ref_part
                self.assertEqual(self.moved_keys(lld), [])

    def test_ut_moved_percent_encoded_anchor(self):  # %-符号化したアンカーも参照（unquote して照らす）
        lld = LLD_REF.replace('#11-一)', '#11-%E4%B8%80)')
        self.assertEqual(self.moved_keys(lld), [])

    def test_ut_moved_cases_outside_numbered_section(self):  # ケースが同じ番号の節の外にある
        ut = '# UT\n\n### 1.1 一\n\n前置き。\n\n### 3.1 三\n\n| ID | 手順 |\n|---|---|\n| `UT-one-001` | a |\n'
        self.assertEqual(self.moved_keys(LLD_REF, ut=ut), ['T2:UT-move:LLD-one:置き場'])

    def test_ut_moved_cases_in_deeper_heading(self):  # 同じ番号の節のより深い見出しの下は節の中
        ut = '# UT\n\n### 1.1 一\n\n#### 群\n\n| ID | 手順 |\n|---|---|\n| `UT-one-001` | a |\n'
        self.assertEqual(self.moved_keys(LLD_REF, ut=ut), [])

    def lld_keys(self, lld):
        return [k for k in self.keys(self.files(**{'docs/40_LLD.md': lld})) if ':LLD-UT:' in k]

    def test_lld_ut_candidates_clean(self):
        self.assertEqual(self.lld_keys(LLD_UT), [])

    def test_lld_ut_candidate_bad_format(self):
        keys = self.lld_keys(LLD_UT + '| `UT-one-04` | x |\n| `UT-one-1000` | x |\n| `UT-one-00５` | x |\n')
        for bad in ('UT-one-04', 'UT-one-1000', 'UT-one-00５'):
            self.assertIn(f'T1:LLD-UT:{bad}', keys)

    def test_lld_ut_candidate_other_module(self):
        self.assertIn('T2:LLD-UT:UT-two-004->LLD-one', self.lld_keys(LLD_UT + '| `UT-two-004` | x |\n'))

    def test_lld_ut_candidate_duplicate_across_modules(self):
        keys = self.lld_keys(LLD_UT + LLD_TWO + '| `UT-one-001` | x |\n')
        self.assertEqual(keys, ['T1:LLD-UT:UT-one-001:重複'])

    def test_lld_ut_candidate_duplicate_checked_before_format(self):
        keys = self.lld_keys(LLD_UT + '| `UT-one-04` | x |\n| `UT-one-04` | y |\n')
        self.assertCountEqual(keys, ['T1:LLD-UT:UT-one-04', 'T1:LLD-UT:UT-one-04:重複'])

    def test_lld_ut_candidate_bare(self):
        self.assertIn('T1:LLD-UT:UT-one-004:コード表記', self.lld_keys(LLD_UT + '| UT-one-004 | x |\n'))

    def test_lld_ut_candidate_bad_first_cell(self):
        rows = '| `UX-one-004` | x |\n|  | x |\n| `UT-one-004`・`UT-one-005` | x |\n| `UT-one-006` 追記 | x |\n'
        keys = self.lld_keys(LLD_UT + rows)
        self.assertEqual(len([k for k in keys if k.endswith(':1列目')]), 4)

    def test_lld_ut_candidate_table_without_id_header(self):
        lld = LLD_UT + '\n| 番号 | x |\n|---|---|\n| `UT-one-04` | e |\n'
        keys = self.lld_keys(lld)
        self.assertEqual(len([k for k in keys if k.endswith(':表')]), 1)
        self.assertNotIn('T1:LLD-UT:UT-one-04', keys)

    def test_lld_ut_candidate_missing_separator(self):
        keys = self.lld_keys(LLD_UT + '\n| ID | x |\n| `UT-one-04` | a |\n')
        self.assertEqual(len([k for k in keys if k.endswith(':表')]), 1)
        self.assertIn('T1:LLD-UT:UT-one-04', keys)

    def test_lld_ut_candidate_indented_table(self):
        inside = LLD_UT + '\n- 群 A:\n\n  | ID | x |\n  |---|---|\n  | `UT-one-04` | x |\n'
        self.assertIn('T1:LLD-UT:UT-one-04', self.lld_keys(inside))
        outside = LLD + '\n- 群 A:\n\n  | ID | x |\n  |---|---|\n  | `UT-one-001` | x |\n'
        self.assertIn('T1:LLD-UT:UT-one-001:小節の外', self.lld_keys(outside))

    def test_lld_ut_candidate_header_without_second_row(self):
        for tail in ('\n| ID | x |\n\n', '\n| ID | x |'):
            keys = self.lld_keys(LLD_UT + tail)
            self.assertEqual(len([k for k in keys if k.endswith(':表')]), 1, tail)

    def test_lld_ut_candidate_preparation_table_header_with_ut_id(self):
        lld = LLD_UT + '\n- 準備の値:\n\n  | `UT-one-004` | x |\n'
        self.assertEqual(len([k for k in self.lld_keys(lld) if k.endswith(':表')]), 1)

    def test_lld_ut_candidate_indented_preparation_table(self):
        prep = LLD_UT + '\n- 準備の値:\n\n  | 名 | 値 |\n  |---|---|\n  | `MD0` | x |\n'
        self.assertEqual(self.lld_keys(prep), [])
        stray = LLD_UT + '\n- 準備の値:\n\n  | 名 | 値 |\n  |---|---|\n  | `UT-one-004` | x |\n'
        self.assertEqual(len([k for k in self.lld_keys(stray) if k.endswith(':表')]), 1)

    def test_lld_ut_candidate_fence_between_tables(self):
        lld = (LLD_UT + '\n| ID | x |\n|---|---|\n| `UT-one-004` | a |\n```text\nx\n```\n'
               '| ID | x |\n|---|---|\n| `UT-one-005` | b |\n')
        self.assertEqual(self.lld_keys(lld), [])

    def test_lld_ut_candidate_numbered_deep_heading_keeps_subsection(self):
        lld = (LLD_UT + '\n###### 1.1.5.1 UT 候補\n\n| ID | x |\n|---|---|\n| `UT-one-004` | a |\n'
               '\n##### 群2\n\n| ID | x |\n|---|---|\n| `UT-one-05` | b |\n')
        keys = self.lld_keys(lld)
        self.assertIn('T1:LLD-UT:UT-one-05', keys)
        self.assertNotIn('T1:LLD-UT:UT-one-05:小節の外', keys)

    def test_lld_ut_candidate_module_ends_at_deep_heading(self):
        lld = (LLD_UT + '\n##### A\n\n- **ID**: LLD-two\n\n##### B\n\n'
               '| ID | x |\n|---|---|\n| `UT-two-004` | e |\n')
        keys = self.lld_keys(lld)
        self.assertIn('T2:LLD-UT:UT-two-004->なし', keys)
        self.assertNotIn('T2:LLD-UT:UT-two-004->LLD-two', keys)

    def test_lld_ut_candidate_outside_header_row(self):
        lld = LLD + '\n#### 1.1.5 UT候補\n\n| `UT-one-001` | x |\n|---|---|\n'
        self.assertIn('T1:LLD-UT:UT-one-001:小節の外', self.lld_keys(lld))

    def test_lld_ut_candidate_bare_outside_subsection(self):
        lld = LLD + '\n#### 1.1.6 その他\n\n| ID | x |\n|---|---|\n| UT-one-004 | e |\n'
        self.assertIn('T1:LLD-UT:UT-one-004:小節の外', self.lld_keys(lld))

    def test_lld_ut_candidate_first_id_declaration_wins(self):
        lld = LLD_UT.replace('- **ID**: LLD-one\n', '- **ID**: LLD-one\n- **ID**: LLD-two\n')
        self.assertEqual(self.lld_keys(lld), [])

    def test_lld_ut_candidate_declaration_before_first_heading(self):
        lld = ('- **ID**: LLD-one\n\n# LLD\n\n## 1. モジュール\n\n#### 1.9.5 UT 候補\n\n'
               '| ID | x |\n|---|---|\n| `UT-one-004` | a |\n')
        self.assertIn('T2:LLD-UT:UT-one-004->なし', self.lld_keys(lld))

    def test_lld_ut_candidate_declaration_value_stripped(self):
        self.assertEqual(self.lld_keys(LLD_UT.replace('- **ID**: LLD-one\n', '- **ID**: LLD-one  \n')), [])

    def test_lld_ut_candidate_outside_module(self):
        lld = LLD_UT + '\n### 1.3 横断\n\n#### 1.3.5 UT 候補\n\n| ID | x |\n|---|---|\n| `UT-one-005` | e |\n'
        self.assertIn('T2:LLD-UT:UT-one-005->なし', self.lld_keys(lld))

    def test_lld_ut_candidate_leaves_subsection(self):
        lld = LLD_UT + '\n#### 1.1.6 その他\n\n| ID | x |\n|---|---|\n| `UT-one-04` | e |\n'
        keys = self.lld_keys(lld)
        self.assertIn('T1:LLD-UT:UT-one-04:小節の外', keys)
        self.assertNotIn('T1:LLD-UT:UT-one-04', keys)

    def test_lld_ut_candidate_misspelled_heading(self):
        lld = LLD + '\n#### 1.1.5 UT候補\n\n| ID | x |\n|---|---|\n| `UT-one-001` | e |\n'
        self.assertIn('T1:LLD-UT:UT-one-001:小節の外', self.lld_keys(lld))

    def test_ut_id_three_digits(self):
        ut = UT + ''.join(f'| `{i}` | x |\n' for i in (
            'UT-one-010', 'UT-one-099', 'UT-one-100', 'UT-one-999', 'UT-one-01', 'UT-one-000', 'UT-one-1000',
            'UT-one-1', 'UT-one-10９'))
        keys = self.keys(self.files(**{'docs/50_UT.md': ut}))
        for ok in ('UT-one-010', 'UT-one-099', 'UT-one-100', 'UT-one-999'):
            self.assertNotIn(f'T1:{ok}', keys)
        for bad in ('UT-one-01', 'UT-one-000', 'UT-one-1000', 'UT-one-1', 'UT-one-10９'):
            self.assertIn(f'T1:{bad}', keys)

    def test_ut_id_fullwidth_digit_in_heading(self):
        # 見出しの ID を全角の数字の手前で切ると、誤記が別の有効なケースの宣言になる
        ut = UT + '\n### UT-one-100９: x\n'
        keys = self.keys(self.files(**{'docs/50_UT.md': ut}))
        self.assertIn('T1:UT-one-100９', keys)

    def test_ut_id_fullwidth_digit_in_trace(self):
        # trace: の ID を全角の数字の手前で切ると、誤記が別の有効なケースの実装になる
        files = self.files(**{'tests/src/test_one.cpp': '// trace: UT-one-001９\n'})
        self.assertIn('T2:tests/src/test_one.cpp->UT-one-001９', self.keys(files))

    def test_it_st_keep_two_digits(self):
        # IT・ST の連番は 2 桁のまま。ASCII の数字だけを通し、全角の数字は書式の誤り（T1）にする
        it = IT.replace('| `IT-CMP1-INT1-01` | a | b | c | d |\n', ''.join(
            f'| `{i}` | a | b | c | d |\n' for i in ('IT-CMP1-INT1-01', 'IT-CMP1-INT1-001', 'IT-CMP1-INT1-1０',
                                                     'IT-CMP1-INT1０-01')))
        st = ST_MOVED.replace('| `ST-FR-001-01` | a |', ''.join(
            f'| `{i}` | a |\n' for i in ('ST-FR-001-01', 'ST-FR-001-001', 'ST-FR-００１-01', 'ST-FR-001-0１'))[:-1])
        keys = self.keys(dict(BASE, **{'docs/30_HLD.md': HLD_SEAM, 'docs/60_IT.md': it, 'docs/70_ST.md': st}))
        for ok in ('IT-CMP1-INT1-01', 'ST-FR-001-01'):
            self.assertNotIn(f'T1:{ok}', keys)
        for bad in ('IT-CMP1-INT1-001', 'IT-CMP1-INT1-1０', 'IT-CMP1-INT1０-01',
                    'ST-FR-001-001', 'ST-FR-００１-01', 'ST-FR-001-0１'):
            self.assertIn(f'T1:{bad}', keys)

    def test_clean_when_confirmed(self):
        keys = self.keys(self.files(), confirmed={'LLD', 'UT'}, implemented={'UT'})
        self.assertEqual([k for k in keys if not k.startswith('T1:stage:')], [])

    def test_missing_file_field(self):
        lld = LLD.replace('- **ファイル**: `src/one.cpp`\n', '')
        self.assertIn('T1:LLD-one:ファイル', self.keys(self.files(**{'docs/40_LLD.md': lld})))

    def test_file_not_in_git_only_when_lld_implemented(self):
        # 製品のコードがそろう（LLD が IMPLEMENTED_STAGES に入る）までは、コードが HLD の名前にそろっていない
        # （ADR-LLD-001、ADR-OPS-011）
        lld = LLD.replace('`src/one.cpp`', '`src/one.cpp`・`src/two.cpp`')
        files = self.files(**{'docs/40_LLD.md': lld})
        key = 'T2:LLD-one->src/two.cpp'
        self.assertIn(key, self.keys(files, confirmed={'LLD'}, implemented={'LLD'}))
        self.assertNotIn(key, self.keys(files, confirmed={'LLD'}))
        # 無いファイルは T2 だけにする（対象の拡張子なのに「対象ではありません」と重ねて出さない）
        self.assertNotIn('T5:LLD-one->src/two.cpp', self.keys(files, confirmed={'LLD'}, implemented={'LLD'}))

    def test_unknown_hld_section(self):
        lld = LLD.replace('[4.1](30_HLD.md#41-fr-001-一)', '[4.9](30_HLD.md#41-fr-001-一)')
        self.assertIn('T2:LLD-one->4.9', self.keys(self.files(**{'docs/40_LLD.md': lld})))

    def test_untraced_product_file_only_when_lld_implemented(self):
        files = self.files(**{'scripts/tool.py': 'print(1)\n'})
        self.assertIn('T5:scripts/tool.py', self.keys(files, confirmed={'LLD'}, implemented={'LLD'}))
        self.assertNotIn('T5:scripts/tool.py', self.keys(files, confirmed={'LLD'}))

    def test_trace_not_in_file_field(self):
        files = self.files(**{'src/extra.cpp': '// trace: LLD-one\n'})
        self.assertIn('T5:src/extra.cpp->LLD-one', self.keys(files, confirmed={'LLD'}))

    def test_file_field_without_trace_only_when_lld_implemented(self):
        files = self.files(**{'src/one.cpp': 'int one() { return 1; }\n'})
        self.assertIn('T5:LLD-one->src/one.cpp', self.keys(files, confirmed={'LLD'}, implemented={'LLD'}))
        self.assertNotIn('T5:LLD-one->src/one.cpp', self.keys(files, confirmed={'LLD'}))

    def test_unknown_lld_in_code(self):
        files = self.files(**{'src/one.cpp': '// trace: LLD-one\n// trace: LLD-two\n'})
        self.assertIn('T2:src/one.cpp->LLD-two', self.keys(files, confirmed={'LLD'}))

    def test_hld_section_without_lld_when_confirmed(self):
        lld = LLD.replace('[4.1](30_HLD.md#41-fr-001-一)', '[2.1](30_HLD.md#21-全体)')
        self.assertIn('T3:LLD:4.1', self.keys(self.files(**{'docs/40_LLD.md': lld}), confirmed={'LLD'}))

    def test_lld_can_point_to_program_chapter(self):
        lld = LLD_REF.replace('[4.1](30_HLD.md#41-fr-001-一)',
                          '[4.1](30_HLD.md#41-fr-001-一)・[3.1](30_HLD.md#31-cmp1-一)')
        files = self.files(**{'docs/30_HLD.md': HLD_PROGRAM, 'docs/40_LLD.md': lld})
        keys = self.keys(files, confirmed={'LLD', 'UT'})
        self.assertEqual([k for k in keys if not k.startswith('T1:stage:')], [])

    def test_program_chapter_section_without_lld_when_confirmed(self):
        files = self.files(**{'docs/30_HLD.md': HLD_PROGRAM})
        self.assertIn('T3:LLD:3.1', self.keys(files, confirmed={'LLD'}))
        self.assertNotIn('T3:LLD:3.1', self.keys(files))

    def test_unimplemented_automated_case(self):
        files = self.files(**{'tests/src/test_one.cpp': '// 空\n'})
        keys = self.keys(files, confirmed={'UT'}, implemented={'UT'})
        self.assertIn('T5:UT-one-001', keys)
        self.assertNotIn('T5:UT-one-002', keys)

    def test_unknown_case_in_test_code(self):
        files = self.files(**{'tests/src/test_one.cpp': '// trace: UT-one-001\n// trace: UT-one-009\n'})
        self.assertIn('T2:tests/src/test_one.cpp->UT-one-009', self.keys(files))

    def test_ut_for_unknown_module(self):
        ut = UT + '| `UT-two-001` | c |\n'
        self.assertIn('T2:UT-two-001', self.keys(self.files(**{'docs/50_UT.md': ut})))

    def test_trace_in_string_literal_is_ignored(self):
        files = self.files(**{'tests/scripts/test_x.py': "X = '// trace: UT-one-009'\n"})
        self.assertNotIn('T2:tests/scripts/test_x.py->UT-one-009', self.keys(files))

    def test_trace_in_multiline_string_is_ignored(self):
        files = self.files(**{'tests/scripts/test_y.py': "X = '''\n# trace: UT-one-009\n'''\n",
                              'tests/scripts/test_z.py': "# trace: UT-one-008\n"})
        keys = self.keys(files)
        self.assertNotIn('T2:tests/scripts/test_y.py->UT-one-009', keys)
        self.assertIn('T2:tests/scripts/test_z.py->UT-one-008', keys)

    def test_missing_id_in_module_section(self):
        lld = LLD.replace('- **ID**: LLD-one\n', '')
        self.assertIn('T1:LLD:5:ID', self.keys(self.files(**{'docs/40_LLD.md': lld})))

    def test_file_outside_code_scope(self):
        lld = LLD.replace('`src/one.cpp`', '`src/one.cpp`・`src/table.json`')
        files = self.files(**{'docs/40_LLD.md': lld, 'src/table.json': '{}\n'})
        self.assertIn('T5:LLD-one->src/table.json', self.keys(files, confirmed={'LLD'}, implemented={'LLD'}))

    def html_keys(self, html):
        lld = LLD.replace('`src/one.cpp`', '`src/one.cpp`・`public/index.html`')
        files = self.files(**{'docs/40_LLD.md': lld, 'public/index.html': html})
        return self.keys(files, confirmed={'LLD'}, implemented={'LLD'})

    def test_html_script_traces_are_read(self):
        keys = self.html_keys('<script id="a">\n// trace: LLD-one\n</script>\n'
                              '<SCRIPT id="b">\n  // trace: LLD-two\n</SCRIPT>\n')
        self.assertNotIn('T5:LLD-one->public/index.html', keys)
        self.assertIn('T2:public/index.html->LLD-two', keys)

    def test_html_trace_outside_script_or_in_comment_is_ignored(self):
        for html in ('<p>\n// trace: LLD-one\n</p>\n',
                     '<!--\n<script>\n// trace: LLD-one\n</script>\n-->\n',
                     '<textarea>\n<script>\n// trace: LLD-one\n</script>\n</textarea>\n',
                     "<script>\nf();  // trace: LLD-one\n/* trace: LLD-one */\n/*\n * trace: LLD-one\n */\n"
                     "const s = '// trace: LLD-one';\n</script>\n",
                     '<script>\n/*\n// trace: LLD-one\n*/\n</script>\n',
                     '<script>\nconst t = `\n// trace: LLD-one\n`;\n</script>\n'):
            keys = self.html_keys(html)
            self.assertIn('T5:public/index.html', keys, html)
            self.assertIn('T5:LLD-one->public/index.html', keys, html)

    def test_html_comment_mark_in_script_string_does_not_hide_traces(self):
        keys = self.html_keys('<script>\nconst s = "<!--";\nconst u = "https://x/*";\n// trace: LLD-one\n</script>\n')
        self.assertNotIn('T5:LLD-one->public/index.html', keys)

    def test_js_test_code_is_read(self):
        files = self.files(**{'tests/public/test_one.js':
                              "test('a', () => {\n  // trace: UT-one-001\n});\nf();  // trace: UT-one-008\n"
                              "/*\n * trace: UT-one-007\n */\n// trace: UT-one-009\n"})
        keys = self.keys(files)
        self.assertIn('T2:tests/public/test_one.js->UT-one-009', keys)
        self.assertNotIn('T2:tests/public/test_one.js->UT-one-008', keys)
        self.assertNotIn('T2:tests/public/test_one.js->UT-one-007', keys)

    def test_js_regex_literal_does_not_confuse_the_trace_reader(self):
        # 正規表現リテラルの中のバッククォートや /* は、文字列やコメントの始まりではない（視点5 の指摘）
        for head in ("const tick = /`/;\n", "const r = /[/*]/;\n", "foo(/'/);\n", "x = a / b; y = /`/g;\n",
                     "return /`/.test(x);\n"):
            files = self.files(**{'tests/public/test_one.js':
                                  head + "const s = `\n// trace: UT-one-009\n`;\n// trace: UT-one-008\n"})
            keys = self.keys(files)
            self.assertNotIn('T2:tests/public/test_one.js->UT-one-009', keys, head)
            self.assertIn('T2:tests/public/test_one.js->UT-one-008', keys, head)

    def test_js_division_is_not_a_regex(self):
        files = self.files(**{'tests/public/test_one.js': "const h = (a) / 2 / b;\n// trace: UT-one-008\n"})
        self.assertIn('T2:tests/public/test_one.js->UT-one-008', self.keys(files))

    def test_empty_test_file_needs_no_trace(self):
        files = self.files(**{'tests/scripts/__init__.py': ' \n', 'tests/public/browser.js': '// 道具\n'})
        keys = self.keys(files, confirmed={'UT'}, implemented={'UT'})
        self.assertNotIn('T5:tests/scripts/__init__.py', keys)
        self.assertIn('T5:tests/public/browser.js', keys)

    def test_browser_tool_is_exempted_by_the_adr_only(self):
        # LLD 2.6 の試験の道具は、どのケースにも属さないので EXEMPTIONS で除く（ADR-OPS-011）。実際の EXEMPTIONS で見る
        key = 'T5:tests/public/browser.js'
        adr = lt.EXEMPTIONS.get(key, 'docs/decisions/ADR-OPS-011-separate-lld-confirmation-from-code-checks.md')
        files = self.files(**{'tests/public/browser.js': '// 道具\n', 'tests/public/other.js': '// 道具\n',
                              'tests/public/test_one.js': '// trace: UT-one-009\n'})
        kw = dict(confirmed={'UT'}, implemented={'UT'}, exemptions=lt.EXEMPTIONS)
        keys = self.keys(dict(files, **{adr: '# X\n'}), **kw)
        self.assertNotIn(key, keys)
        self.assertIn('T5:tests/public/other.js', keys)
        self.assertIn('T2:tests/public/test_one.js->UT-one-009', keys)
        self.assertIn(key, self.keys(files, **kw))

    def test_tool_tests_and_prototype_tests_are_not_test_code(self):
        files = self.files(**{'tests/tools/test_t.py': 'x = 1\n', 'tests/test_proto.c': 'int x;\n'})
        keys = self.keys(files, confirmed={'UT'}, implemented={'UT'})
        self.assertNotIn('T5:tests/tools/test_t.py', keys)
        self.assertNotIn('T5:tests/test_proto.c', keys)

    def test_untraced_test_file_only_when_tests_implemented(self):
        files = self.files(**{'tests/src/helper.cpp': 'int helper;\n'})
        self.assertIn('T5:tests/src/helper.cpp', self.keys(files, confirmed={'UT'}, implemented={'UT'}))
        self.assertNotIn('T5:tests/src/helper.cpp', self.keys(files, confirmed={'UT'}))
        files = self.files(**{'tests/scripts/test_it_helper.py': 'x = 1\n'})
        self.assertIn('T5:tests/scripts/test_it_helper.py', self.keys(files, confirmed={'UT'}, implemented={'UT'}))

    def test_module_without_ut_when_confirmed(self):
        ut = UT.replace('| `UT-one-001` | a |\n| `UT-one-002`（手動） | b |\n', '')
        files = self.files(**{'docs/50_UT.md': ut, 'tests/src/test_one.cpp': '// 空\n'})
        self.assertIn('T3:UT:LLD-one', self.keys(files, confirmed={'UT'}))


    def test_several_ids_in_one_trace_comment(self):
        files = self.files(**{'tests/src/test_one.cpp': '// trace: UT-one-001, UT-one-009\n'})
        keys = self.keys(files, confirmed={'UT'}, implemented={'UT'})
        self.assertIn('T2:tests/src/test_one.cpp->UT-one-009', keys)
        self.assertNotIn('T5:UT-one-001', keys)

    def test_trailing_comment_counts_except_in_bash(self):
        files = self.files(**{'tests/scripts/test_e.py': 'x = 1  # trace: UT-one-009\n',
                              'tests/scripts/t.sh': 'echo a  # trace: UT-one-008\n'})
        keys = self.keys(files)
        self.assertIn('T2:tests/scripts/test_e.py->UT-one-009', keys)
        self.assertNotIn('T2:tests/scripts/t.sh->UT-one-008', keys)

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
        self.assertIn('T1:HLD-4.1:対応 SRS', self.keys(self.hld_files(hld)))

    def test_hld_section_label_without_anchor_is_not_a_parent(self):
        hld = HLD.replace('[SRS §3.2](20_SRS.md#32-主要コンポーネント構成)', '[SRS §3.2](20_SRS.md)')
        self.assertIn('T1:HLD-2.1:対応 SRS', self.keys(self.hld_files(hld)))

    def test_lld_declaration_in_code_span_is_not_a_parent(self):
        lld = LLD.replace('[4.1](30_HLD.md#41-fr-001-一)', '`[4.1](30_HLD.md#41-fr-001-一)`')
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
        keys = self.keys(self.files_with_cpp('const char* s = R"(\n// trace: UT-one-009\n)";\n'))
        self.assertNotIn('T2:tests/src/test_raw.cpp->UT-one-009', keys)

    def test_trace_in_cpp_raw_string_with_delimiter_is_ignored(self):
        keys = self.keys(self.files_with_cpp('auto s = R"x(\n)"\n// trace: UT-one-009\n)x";\n'))
        self.assertNotIn('T2:tests/src/test_raw.cpp->UT-one-009', keys)

    def test_trace_in_cpp_string_and_block_comment(self):
        source = ('const char* u = "http://x"; // trace: UT-one-007\n'
                  '/* x\n * trace: UT-one-008\n */\n'
                  "int k = 1'000; // trace: UT-one-006\n")
        keys = self.keys(self.files_with_cpp(source))
        for case_id in ('UT-one-007', 'UT-one-008', 'UT-one-006'):
            self.assertIn(f'T2:tests/src/test_raw.cpp->{case_id}', keys)


if __name__ == '__main__':
    unittest.main()
