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
from collections import Counter, defaultdict
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



UR_ANCHOR_RE = re.compile(r'<a\s+id="ur-(\d+)"')
SRS_REQ_RE = re.compile(r'^#{3,4}\s+((?:FR|NFR)-\d+)')
DECL_RE = re.compile(r'^- \*\*([^*]+)\*\*:\s*(.*)$')
UR_LINK_RE = re.compile(r'\[(UR-\d+)\]\(')
REQ_LINK_RE = re.compile(r'\[((?:FR|NFR)-\d+)\]\(')
COMPONENT_ROW_RE = re.compile(r'^\|\s*(C\d+)\s*\|')
ID_NUM_RE = re.compile(r'^(UR|FR|NFR)-(\d+)$')
SRS_MATRIX_HEAD_RE = re.compile(r'^## \d+\. 要求追跡マトリクス')


def section_decls(text, start_re):
    """start_re に合う見出しごとに、次の見出しまでの宣言（太字ラベルの箇条書き）を集める"""
    out, cur = [], None
    for no, line in iter_lines(text):
        if HEADING_RE.match(line):
            m = start_re.match(line)
            cur = {'key': m.group(1), 'line': no, 'decl': {}} if m else None
            if cur:
                out.append(cur)
            continue
        d = DECL_RE.match(line)
        if cur is not None and d:
            cur['decl'].setdefault(d.group(1), (no, d.group(2).strip()))
    return out


def table_rows(text, heading_re):
    """heading_re に合う見出しの節にある表の行を (行番号, セルの list) で返す"""
    rows, inside = [], False
    for no, line in iter_lines(text):
        if HEADING_RE.match(line):
            if inside:
                break
            inside = bool(heading_re.match(line))
            continue
        if inside and line.startswith('|'):
            rows.append((no, [c.strip() for c in line.strip().strip('|').split('|')]))
    return rows


def load_requirements(repo):
    urs = {f'UR-{n}' for n in UR_ANCHOR_RE.findall(repo.read(URD))}
    srs_text = repo.read(SRS)
    reqs = section_decls(srs_text, SRS_REQ_RE)
    comps = set()
    for _, line in iter_lines(srs_text):
        m = COMPONENT_ROW_RE.match(line)
        if m:
            comps.add(m.group(1))
    return urs, reqs, comps


def check_numbering(ids, retired, repo):
    out, nums = [], defaultdict(set)
    for i in ids:
        m = ID_NUM_RE.match(i)
        if m:
            nums[m.group(1)].add(int(m.group(2)))
    for prefix, present in sorted(nums.items()):
        for n in range(1, max(present) + 1):
            rid = f'{prefix}-{n:03d}'
            if n not in present and rid not in retired:
                out.append(finding('T1', rid, 'scripts/lint_trace.py',
                                   f'{rid} が欠番ですが、欠番の一覧（RETIRED_IDS）にありません'))
    for rid, adr in sorted(retired.items()):
        if rid in ids:
            out.append(finding('T1', f'{rid}:retired', 'scripts/lint_trace.py',
                               f'{rid} は欠番の一覧にありますが、文書に残っています'))
        if not repo.has(adr):
            out.append(finding('T2', f'{rid}->{adr}', 'scripts/lint_trace.py',
                               f'{rid} の根拠の ADR がありません: {adr}'))
    return out


def check_srs(urs, reqs, confirmed):
    out, declared = [], {}
    for r in reqs:
        rid = r['key']
        if '対応 UR' not in r['decl']:
            out.append(finding('T1', rid, f'{SRS}:{r["line"]}', f'{rid} に「対応 UR」の宣言がありません'))
            continue
        no, value = r['decl']['対応 UR']
        parents = set(UR_LINK_RE.findall(value))
        if not parents:
            out.append(finding('T1', rid, f'{SRS}:{no}', f'{rid} の「対応 UR」に UR へのリンクがありません'))
        for p in sorted(parents - urs):
            out.append(finding('T2', f'{rid}->{p}', f'{SRS}:{no}', f'{rid} の対応 UR {p} は URD にありません'))
        declared[rid] = parents & urs
    if 'SRS' in confirmed:
        covered = set().union(*declared.values())
        for u in sorted(urs - covered):
            out.append(finding('T3', f'SRS:{u}', URD, f'{u} を対応 UR に持つ FR/NFR がありません'))
    return out, declared


def check_srs_matrix(repo, urs, declared):
    rows = table_rows(repo.read(SRS), SRS_MATRIX_HEAD_RE)
    if not rows:
        return [finding('T4', 'SRS-matrix:table', SRS, '要求追跡マトリクスの表がありません')]
    out = []
    head_no, head = rows[0]
    cols = []
    for cell in head[2:]:
        m = UR_LINK_RE.search(cell)
        cols.append(m.group(1) if m else None)
    col_set = {c for c in cols if c}
    if col_set != urs:
        out.append(finding('T4', 'SRS-matrix:columns', f'{SRS}:{head_no}',
                           f'列の UR が URD と違います（足りない {sorted(urs - col_set)}、'
                           f'余分 {sorted(col_set - urs)}）'))
    seen = set()
    for no, cells in rows[1:]:
        m = REQ_LINK_RE.search(cells[0]) if cells else None
        if not m:
            continue
        rid = m.group(1)
        seen.add(rid)
        marks = {cols[j] for j, c in enumerate(cells[2:]) if j < len(cols) and cols[j] and '✅' in c}
        if rid not in declared:
            out.append(finding('T4', f'SRS-matrix:{rid}', f'{SRS}:{no}', f'{rid} の行がありますが、宣言がありません'))
        elif marks != declared[rid]:
            out.append(finding('T4', f'SRS-matrix:{rid}', f'{SRS}:{no}',
                               f'{rid} の行 {sorted(marks)} が対応 UR の宣言 {sorted(declared[rid])} と違います'))
    for rid in sorted(set(declared) - seen):
        out.append(finding('T4', f'SRS-matrix:{rid}', SRS, f'要求追跡マトリクスに {rid} の行がありません'))
    return out


def apply_exemptions(findings, exemptions, repo):
    out = [f for f in findings if not (f.key in exemptions and repo.has(exemptions[f.key]))]
    for key, adr in sorted(exemptions.items()):
        if not repo.has(adr):
            out.append(finding('T2', f'exemption->{adr}', 'scripts/lint_trace.py',
                               f'{key} の根拠の ADR がありません: {adr}'))
    return out



def run_checks(repo, confirmed=CONFIRMED_STAGES, retired=RETIRED_IDS, exemptions=EXEMPTIONS):
    out = check_links(repo)
    urs, reqs, comps = load_requirements(repo)
    req_ids = {r['key'] for r in reqs}
    out += check_numbering(urs | req_ids, retired, repo)
    srs_out, declared = check_srs(urs, reqs, confirmed)
    out += srs_out
    out += check_srs_matrix(repo, urs, declared)
    return apply_exemptions(out, exemptions, repo)


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
