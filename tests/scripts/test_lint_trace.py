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


if __name__ == '__main__':
    unittest.main()
