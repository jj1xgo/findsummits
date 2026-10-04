#!/usr/bin/env python3
"""要求の追跡と整合の検査（docs/03_development.md「6. 要求の追跡と整合」、ADR-URD-020）

T1: 宣言の欠落・書式違い・欠番
T2: 参照先（ID・見出しのアンカー・ファイル）の実在
T3: 被覆（下位の段が確定済みのときだけ）
T4: 追跡マトリクスと宣言の照合
T5: 製品のコード・テストのコードと文書の双方向（確定済みの段だけ）
"""
import os
import re
import subprocess
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import NamedTuple
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent

# フェーズゲートを通った段。ゲートの判定が Go / 条件付きGo なら段を足す（docs/03_development.md §4）。
# T3・T5 は下位の段の名前で効くので、最上位の URD は入れない。
CONFIRMED_STAGES = frozenset({'SRS'})

# 欠番と、削除の根拠の ADR
RETIRED_IDS = {
    'UR-009': 'docs/decisions/ADR-URD-020-requirement-traceability-and-consistency.md',
    'FR-010': 'docs/decisions/ADR-SRS-028-nationwide-batch-matching-fr010-removal.md',
}

# 構造上の例外。Finding.key → 根拠の ADR。ADR が git に無い項目は例外にならない。
EXEMPTIONS = {}

URD = 'docs/10_URD.md'
SRS = 'docs/20_SRS.md'
HLD = 'docs/30_HLD.md'
LLD = 'docs/40_LLD.md'
CASE_DOCS = {'UT': 'docs/50_UT.md', 'IT': 'docs/60_IT.md', 'ST': 'docs/70_ST.md'}

NO_PARENT = 'なし（横断の設計）'
ALL_COMPONENTS = '全体'
MANUAL_MARK = '（手動）'
PRODUCT_DIRS = ('src/', 'scripts/')
TEST_DIRS = ('tests/',)
CODE_SUFFIXES = ('.c', '.h', '.cpp', '.hpp', '.py', '.sh')

HEADING_RE = re.compile(r'^(#{1,6})\s+(.*?)\s*#*\s*$')
HTML_ANCHOR_RE = re.compile(r'<a\s+(?:id|name)=["\']?([^"\'\s>]+)')
LINK_RE = re.compile(r'\[([^\]]*)\]\(([^)\s#]*)(?:#([^)\s]+))?\)')
INLINE_CODE_RE = re.compile(r'`[^`\n]+`')
ID_LABEL_RE = re.compile(r'^(?:UR|FR|NFR)-\d+$')
SECTION_LABEL_RE = re.compile(r'^(?:SRS §(\d+(?:\.\d+)*)|(\d+(?:\.\d+)+))$')


class Finding(NamedTuple):
    key: str   # 例外の照合とテストに使う。'<検査>:<対象>'
    text: str  # 表示する文


def finding(check, subject, where, message):
    return Finding(f'{check}:{subject}', f'{where}: {check} {message}')


class Repo:
    """git 管理下のファイルだけを見る（CI と手元で結果をそろえるため）"""

    def __init__(self, root, files):
        self.root = Path(root)
        self.files = {os.path.normpath(f) for f in files}
        self.dirs = set()
        for f in self.files:
            parent = Path(f).parent
            while str(parent) != '.':
                self.dirs.add(str(parent))
                parent = parent.parent

    def has(self, rel):
        return os.path.normpath(rel) in self.files

    def exists(self, rel):
        rel = os.path.normpath(rel)
        return rel in self.files or rel in self.dirs

    def read(self, rel):
        return (self.root / rel).read_text(encoding='utf-8')

    def md_files(self):
        return sorted(f for f in self.files if f.endswith('.md'))


def iter_lines(text):
    """コードブロックの外の行を (行番号, 行) で返す"""
    in_code = False
    for no, line in enumerate(text.split('\n'), 1):
        if line.lstrip().startswith('```'):
            in_code = not in_code
            continue
        if not in_code:
            yield no, line


def github_slug(text):
    """GitHub が見出しに付けるアンカーと同じ文字列を作る"""
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('`', '').strip().lower()
    kept = ''.join(
        c for c in text
        if c in ' -' or unicodedata.category(c)[0] in 'LMN' or unicodedata.category(c) == 'Pc'
    )
    return kept.replace(' ', '-')


def anchors_of(text):
    found, seen = set(), Counter()
    for _, line in iter_lines(text):
        m = HEADING_RE.match(line)
        if m:
            base = github_slug(m.group(2))
            n = seen[base]
            seen[base] += 1
            found.add(base if n == 0 else f'{base}-{n}')
        found.update(HTML_ANCHOR_RE.findall(line))
    return found


def label_mismatch(label, anchor):
    """リンク文字列が ID（UR/FR/NFR）か節番号（点を含むか SRS §）なら、アンカーがその要素を指すかを見る"""
    if ID_LABEL_RE.match(label):
        prefix = label.lower()
        return not (anchor == prefix or anchor.startswith(prefix + '-'))
    m = SECTION_LABEL_RE.match(label)
    if m:
        prefix = (m.group(1) or m.group(2)).replace('.', '')
        return not anchor.startswith(prefix + '-')
    return False


def check_links(repo):
    out, cache = [], {}
    for path in repo.md_files():
        for no, line in iter_lines(repo.read(path)):
            for m in LINK_RE.finditer(INLINE_CODE_RE.sub('', line)):
                label, target, anchor = m.group(1), m.group(2), m.group(3)
                if target.startswith(('http://', 'https://', 'mailto:')):
                    continue
                where = f'{path}:{no}'
                dest = path
                if target:
                    dest = os.path.normpath(os.path.join(os.path.dirname(path), unquote(target)))
                if not repo.exists(dest):
                    out.append(finding('T2', f'{path}->{target}', where,
                                       f'リンク先のファイルがありません: {target}'))
                    continue
                if anchor and dest.endswith('.md'):
                    if dest not in cache:
                        cache[dest] = anchors_of(repo.read(dest))
                    if unquote(anchor) not in cache[dest]:
                        out.append(finding('T2', f'{path}->{target}#{anchor}', where,
                                           f'リンク先の見出し・アンカーがありません: {target}#{anchor}'))
                    elif label_mismatch(label, unquote(anchor)):
                        out.append(finding('T2', f'{path}->{target}#{anchor}:label', where,
                                           f'リンク文字列 {label} とリンク先 #{anchor} が違う要素を指しています'))
    return out


def run_checks(repo, confirmed=CONFIRMED_STAGES, retired=RETIRED_IDS, exemptions=EXEMPTIONS):
    return check_links(repo)


def git_files(root):
    res = subprocess.run(['git', '-C', str(root), 'ls-files', '-z'], check=True, capture_output=True)
    return [p for p in res.stdout.decode('utf-8').split('\0') if p]


def main():
    findings = run_checks(Repo(ROOT, git_files(ROOT)))
    for f in findings:
        print(f.text)
    sys.exit(1 if findings else 0)


if __name__ == '__main__':
    main()
