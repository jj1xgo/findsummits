#!/usr/bin/env python3
"""要求の追跡と整合の検査（docs/03_development.md「6. 要求の追跡と整合」、ADR-URD-020）

T1: 宣言の欠落・書式違い・欠番
T2: 参照先（ID・見出しのアンカー・ファイル）の実在
T3: 被覆（下位の段が確定済みのときだけ）
T4: 追跡マトリクスと宣言の照合
T5: 製品のコード・テストのコードと文書の双方向（確定済みの段だけ）
"""
import io
import os
import re
import subprocess
import sys
import tokenize
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
UR_ID_RE = re.compile(r'^UR-\d+$')
REQ_ID_RE = re.compile(r'^(?:FR|NFR)-\d+$')
SRS_SECTION_LABEL_RE = re.compile(r'^SRS §\d+(?:\.\d+)*$')
HLD_SECTION_LABEL_RE = re.compile(r'^\d+\.\d+(?:\.\d+)*$')


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


FENCE_RE = re.compile(r'^\s*(`{3,}|~{3,})(.*)$')


def iter_lines(text):
    """コードブロックの外の行を (行番号, 行) で返す。

    フェンスは ``` と ~~~。閉じるには、開いたのと同じ文字で、同じ長さ以上で、説明の無い行が要る
    （4 個のフェンスの中に 3 個のフェンスの例を書ける）。
    """
    fence = None
    for no, line in enumerate(text.split('\n'), 1):
        m = FENCE_RE.match(line)
        if fence is None:
            if m and not (m.group(1)[0] == '`' and '`' in m.group(2)):
                fence = m.group(1)
                continue
            yield no, line
        elif m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not m.group(2).strip():
            fence = None


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


def decl_ids(value, label_re, doc=None):
    """宣言や表のセルの値から、コード表記の外にある、アンカー付きの完全なリンクのリンク文字列を取り出す。

    doc を渡すと、リンク先が（宣言のある文書と同じ docs/ の）その文書そのものでなければ数えない。
    外部 URL・別のディレクトリのパスは数えない。
    """
    ids = set()
    for m in LINK_RE.finditer(INLINE_CODE_RE.sub('', value)):
        label, target, anchor = m.group(1), m.group(2), m.group(3)
        if anchor and label_re.match(label) and (doc is None or os.path.normpath(unquote(target)) == doc):
            ids.add(label)
    return ids


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
        parents = decl_ids(value, UR_ID_RE, '10_URD.md')
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
        cols.append(next(iter(decl_ids(cell, UR_ID_RE)), None))
    col_set = {c for c in cols if c}
    if col_set != urs:
        out.append(finding('T4', 'SRS-matrix:columns', f'{SRS}:{head_no}',
                           f'列の UR が URD と違います（足りない {sorted(urs - col_set)}、'
                           f'余分 {sorted(col_set - urs)}）'))
    seen = set()
    for no, cells in rows[1:]:
        ids = decl_ids(cells[0], REQ_ID_RE) if cells else set()
        if not ids:
            continue
        rid = next(iter(ids))
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



CASE_ROW_RE = re.compile(r'^\|\s*`((?:UT|IT|ST)-[^`]+)`([^|]*)\|')
CASE_HEAD_RE = re.compile(r'^#{2,6}\s+((?:UT|IT|ST)-[A-Za-z0-9_-]+)(.*)$')
CASE_FORMAT = {
    'UT': re.compile(r'^UT-([A-Za-z0-9_]+)-\d{2}$'),
    'IT': re.compile(r'^IT-([A-Za-z0-9_-]+)-\d{2}$'),
    'ST': re.compile(r'^ST-((?:FR|NFR|UR)-\d{3})-\d{2}$'),
}
ST_COVERAGE_HEAD_RE = re.compile(r'^## \d+\. URカバレッジ表')
CASE_REF_RE = re.compile(r'`(ST-(?:FR|NFR|UR)-\d{3}-)(\d{2}|\*)`(?:〜`(\d{2})`)?')


def load_cases(repo):
    cases, out = {}, []
    for level, path in CASE_DOCS.items():
        if not repo.has(path):
            continue
        for no, line in iter_lines(repo.read(path)):
            m = CASE_ROW_RE.match(line) or CASE_HEAD_RE.match(line)
            if not m or not m.group(1).startswith(level + '-'):
                continue
            cid = m.group(1)
            if cid in cases:
                out.append(finding('T1', f'{cid}:重複', f'{path}:{no}', f'テストケース ID {cid} が重複しています'))
                continue
            cases[cid] = {'level': level, 'path': path, 'line': no, 'manual': MANUAL_MARK in m.group(2)}
    return cases, out


def check_cases(cases, req_ids, urs, modules, confirmed):
    out, st_parents, ut_modules = [], set(), set()
    for cid, c in sorted(cases.items()):
        where = f'{c["path"]}:{c["line"]}'
        m = CASE_FORMAT[c['level']].match(cid)
        if not m:
            out.append(finding('T1', cid, where,
                               f'テストケース ID {cid} の書式が規則（02_test_policy.md §6）と違います'))
            continue
        if c['level'] == 'ST':
            st_parents.add(m.group(1))
            if m.group(1) not in req_ids | urs:
                out.append(finding('T2', cid, where, f'{cid} の対象 {m.group(1)} は URD・SRS にありません'))
        elif c['level'] == 'UT':
            ut_modules.add(f'LLD-{m.group(1)}')
            if modules is not None and f'LLD-{m.group(1)}' not in modules:
                out.append(finding('T2', cid, where, f'{cid} の対象 LLD-{m.group(1)} は LLD にありません'))
    if 'ST' in confirmed:
        for rid in sorted(req_ids - st_parents):
            out.append(finding('T3', f'ST:{rid}', CASE_DOCS['ST'], f'{rid} の ST がありません'))
    if 'UT' in confirmed and modules is not None:
        for mid in sorted(set(modules) - ut_modules):
            out.append(finding('T3', f'UT:{mid}', CASE_DOCS['UT'], f'{mid} の UT がありません'))
    return out


def unresolved_case_refs(cell, cases):
    """`ST-FR-001-02`・`ST-FR-006-*`・`ST-NFR-001-02`〜`05` の形の参照のうち、実在するケースに解決しないもの"""
    out = []
    for prefix, start, end in CASE_REF_RE.findall(cell):
        if start == '*':
            if not any(c.startswith(prefix) for c in cases):
                out.append(prefix + '*')
            continue
        numbers = [start] if not end else [f'{n:02d}' for n in range(int(start), int(end) + 1)]
        out += [prefix + n for n in numbers if prefix + n not in cases]
    return out


def check_st_matrix(repo, urs, declared, cases):
    path = CASE_DOCS['ST']
    if not repo.has(path):
        return []
    inverse = defaultdict(set)
    for rid, parents in declared.items():
        for u in parents:
            inverse[u].add(rid)
    out, seen = [], set()
    for no, cells in table_rows(repo.read(path), ST_COVERAGE_HEAD_RE):
        ur_ids = decl_ids(cells[0], UR_ID_RE) if cells else set()
        if not ur_ids or len(cells) < 3:
            continue
        u = next(iter(ur_ids))
        seen.add(u)
        got = decl_ids(cells[2], REQ_ID_RE)
        if got != inverse[u]:
            out.append(finding('T4', f'ST-coverage:{u}', f'{path}:{no}',
                               f'{u} の行 {sorted(got)} が SRS の対応 UR の宣言 {sorted(inverse[u])} と違います'))
        for ref in unresolved_case_refs(cells[3] if len(cells) > 3 else '', cases):
            out.append(finding('T2', f'ST-coverage:{u}->{ref}', f'{path}:{no}',
                               f'{u} の行のテストケース {ref} は ST にありません'))
    for u in sorted(urs - seen):
        out.append(finding('T4', f'ST-coverage:{u}', path, f'URカバレッジ表に {u} の行がありません'))
    return out


HLD_SEC_RE = re.compile(r'^### ([234]\.\d+) ')


def check_hld(repo, req_ids, comps, confirmed):
    if not repo.has(HLD):
        return [], set()
    out, covered, sections = [], set(), set()
    for s in section_decls(repo.read(HLD), HLD_SEC_RE):
        sec, d = s['key'], s['decl']
        sections.add(sec)
        where = f'{HLD}:{s["line"]}'
        if '対応 SRS' not in d:
            out.append(finding('T1', f'HLD-{sec}:対応 SRS', where, f'{sec} に「対応 SRS」の宣言がありません'))
        else:
            no, value = d['対応 SRS']
            ids = decl_ids(value, REQ_ID_RE, '20_SRS.md')
            has_section = bool(decl_ids(value, SRS_SECTION_LABEL_RE, '20_SRS.md'))
            if value != NO_PARENT and not ids and not has_section:
                out.append(finding('T1', f'HLD-{sec}:対応 SRS', f'{HLD}:{no}',
                                   f'{sec} の「対応 SRS」に FR/NFR か SRS の節へのリンクがありません'
                                   f'（上位が無い節は「{NO_PARENT}」）'))
            for rid in sorted(ids - req_ids):
                out.append(finding('T2', f'HLD-{sec}->{rid}', f'{HLD}:{no}',
                                   f'{sec} の対応 SRS {rid} は SRS にありません'))
            covered |= ids & req_ids
        if '担当コンポーネント' not in d:
            out.append(finding('T1', f'HLD-{sec}:担当コンポーネント', where,
                               f'{sec} に「担当コンポーネント」の宣言がありません'))
        else:
            no, value = d['担当コンポーネント']
            if value != ALL_COMPONENTS:
                names = [v.strip() for v in value.split('・') if v.strip()]
                if not names:
                    out.append(finding('T1', f'HLD-{sec}:担当コンポーネント', f'{HLD}:{no}',
                                       f'{sec} の「担当コンポーネント」が空です'))
                for n in names:
                    if n not in comps:
                        out.append(finding('T2', f'HLD-{sec}->{n}', f'{HLD}:{no}',
                                           f'{sec} の担当コンポーネント {n} は SRS §3.2 にありません'))
    if 'HLD' in confirmed:
        for rid in sorted(req_ids - covered):
            out.append(finding('T3', f'HLD:{rid}', HLD, f'{rid} を対応 SRS に持つ HLD の節がありません'))
    return out, sections


LLD_ID_RE = re.compile(r'^LLD-[A-Za-z0-9_]+$')
ANY_HEADING_RE = re.compile(r'^#{1,6}\s+(.+?)\s*$')
CODE_SPAN_RE = re.compile(r'`([^`]+)`')
# コメント行（//、#、/* や * で始まる行）の trace: だけを拾う。文字列リテラルの中の trace: は拾わない
TRACE_RE = re.compile(r'^\s*(?://+|#+|/?\*+)\s*trace:\s*((?:LLD|UT|IT|ST)-[A-Za-z0-9_-]+)', re.M)
MODULE_LABELS = {'ID', '対応 HLD', 'ファイル'}


def check_lld(repo, hld_sections, confirmed):
    if not repo.has(LLD):
        return [], None
    out, modules = [], {}
    for s in section_decls(repo.read(LLD), ANY_HEADING_RE):
        d = s['decl']
        if not MODULE_LABELS & set(d):
            continue
        if 'ID' not in d:
            out.append(finding('T1', f'LLD:{s["line"]}:ID', f'{LLD}:{s["line"]}',
                               'モジュールの節に「ID」の宣言がありません'))
            continue
        no, mid = d['ID']
        where = f'{LLD}:{no}'
        if not LLD_ID_RE.match(mid):
            out.append(finding('T1', f'LLD:{no}:ID', where,
                               f'LLD の ID「{mid}」の書式が LLD-<モジュール名> と違います'))
            continue
        if mid in modules:
            out.append(finding('T1', f'{mid}:重複', where, f'LLD の ID {mid} が重複しています'))
            continue
        secs, files = set(), set()
        if '対応 HLD' not in d:
            out.append(finding('T1', f'{mid}:対応 HLD', where, f'{mid} に「対応 HLD」の宣言がありません'))
        else:
            hno, value = d['対応 HLD']
            secs = {'.'.join(label.split('.')[:2])
                    for label in decl_ids(value, HLD_SECTION_LABEL_RE, '30_HLD.md')}
            if not secs:
                out.append(finding('T1', f'{mid}:対応 HLD', f'{LLD}:{hno}',
                                   f'{mid} の「対応 HLD」に HLD の節へのリンクがありません'))
            for sec in sorted(secs - hld_sections):
                out.append(finding('T2', f'{mid}->{sec}', f'{LLD}:{hno}',
                                   f'{mid} の対応 HLD {sec} は HLD にありません'))
        if 'ファイル' not in d:
            out.append(finding('T1', f'{mid}:ファイル', where, f'{mid} に「ファイル」の宣言がありません'))
        else:
            fno, value = d['ファイル']
            files = set(CODE_SPAN_RE.findall(value))
            if not files:
                out.append(finding('T1', f'{mid}:ファイル', f'{LLD}:{fno}',
                                   f'{mid} の「ファイル」にコード表記のパスがありません'))
            for f in sorted(files):
                if not repo.has(f):
                    out.append(finding('T2', f'{mid}->{f}', f'{LLD}:{fno}',
                                       f'{mid} のファイル {f} は git にありません'))
        modules[mid] = {'files': files, 'hld': secs, 'where': where}
    if 'LLD' in confirmed:
        covered = set().union(*(m['hld'] for m in modules.values()))
        for sec in sorted(x for x in hld_sections if x.startswith(('3.', '4.')) and x not in covered):
            out.append(finding('T3', f'LLD:{sec}', LLD, f'HLD {sec} を対応 HLD に持つ LLD のモジュールがありません'))
    return out, modules


C_SUFFIXES = ('.c', '.h', '.cpp', '.hpp')
RAW_OPEN_RE = re.compile(r'"([^ ()\\\t\n]{0,16})\(')


def skip_quoted(text, i):
    """i の引用符（" か '）で始まる文字列・文字の、閉じの次の位置を返す（改行で打ち切る）"""
    quote = text[i]
    j = i + 1
    while j < len(text) and text[j] not in (quote, '\n'):
        j += 2 if text[j] == '\\' else 1
    return j + 1


def c_comments(text):
    """C/C++ のコメントだけを返す。文字列・文字・raw 文字列（R"x( … )x"）の中は含めない"""
    out, i, n = [], 0, len(text)
    while i < n:
        c, two = text[i], text[i:i + 2]
        if two == '//':
            j = text.find('\n', i)
            j = n if j < 0 else j
            out.append(text[i:j])
            i = j
        elif two == '/*':
            j = text.find('*/', i + 2)
            j = n if j < 0 else j + 2
            out.append(text[i:j])
            i = j
        elif c == '"' and i > 0 and text[i - 1] == 'R' and RAW_OPEN_RE.match(text, i):
            delim = RAW_OPEN_RE.match(text, i).group(1)
            end = text.find(')' + delim + '"', i)
            i = n if end < 0 else end + len(delim) + 2
        elif c == '"' or (c == "'" and not (i > 0 and text[i - 1].isalnum())):
            i = skip_quoted(text, i)
        else:
            i += 1
    return out


def comment_texts(path, text):
    """本物のコメントだけを取り出す。文字列リテラルの中の trace: を数えないため。

    Python は tokenize（三重引用符の中も除く）、C/C++ は c_comments。それ以外（bash）は行ごとに見るので、
    heredoc の中で # から始まる行はコメントとして数えてしまう（既知の制限。テストのコードに heredoc で
    trace: を書かない）。
    """
    if path.endswith(C_SUFFIXES):
        return c_comments(text)
    if not path.endswith('.py'):
        return text.split('\n')
    try:
        return [tok.string for tok in tokenize.generate_tokens(io.StringIO(text).readline)
                if tok.type == tokenize.COMMENT]
    except (tokenize.TokenError, SyntaxError):
        return text.split('\n')


def code_traces(repo, dirs):
    out = {}
    for f in sorted(repo.files):
        if f.startswith(dirs) and f.endswith(CODE_SUFFIXES):
            out[f] = {i for c in comment_texts(f, repo.read(f)) for i in TRACE_RE.findall(c)}
    return out


def check_code(repo, modules, cases, confirmed):
    out = []
    if modules is not None and 'LLD' in confirmed:
        traces = code_traces(repo, PRODUCT_DIRS)
        for f, ids in traces.items():
            lld_ids = {i for i in ids if i.startswith('LLD-')}
            if not lld_ids:
                out.append(finding('T5', f, f, 'どの LLD モジュールも名乗っていません（trace: LLD-…）'))
            for i in sorted(lld_ids):
                if i not in modules:
                    out.append(finding('T2', f'{f}->{i}', f, f'{i} は LLD にありません'))
                elif f not in modules[i]['files']:
                    out.append(finding('T5', f'{f}->{i}', f, f'{i} の「ファイル」欄に {f} がありません'))
        for mid, m in sorted(modules.items()):
            for f in sorted(m['files']):
                if f not in traces:
                    out.append(finding('T5', f'{mid}->{f}', m['where'],
                                       f'{f} は製品のコードの対象（src/・scripts/ の .c・.h・.cpp・.hpp・.py・.sh）'
                                       'ではありません'))
                elif mid not in traces[f]:
                    out.append(finding('T5', f'{mid}->{f}', m['where'], f'{f} に trace: {mid} がありません'))
    implemented = set()
    tests_confirmed = bool(confirmed & {'UT', 'IT', 'ST'})
    for f, ids in code_traces(repo, TEST_DIRS).items():
        case_ids = {i for i in ids if not i.startswith('LLD-')}
        if tests_confirmed and not case_ids:
            out.append(finding('T5', f, f, 'どのテストケースも名乗っていません（trace: <テストケース ID>）'))
        for i in sorted(case_ids):
            implemented.add(i)
            if i not in cases:
                out.append(finding('T2', f'{f}->{i}', f, f'テストケース {i} はテスト文書にありません'))
    for cid, c in sorted(cases.items()):
        if c['level'] in confirmed and not c['manual'] and cid not in implemented:
            out.append(finding('T5', cid, f'{c["path"]}:{c["line"]}',
                               f'{cid} を実装したテストのコードがありません（trace: {cid}）'))
    return out


def run_checks(repo, confirmed=CONFIRMED_STAGES, retired=RETIRED_IDS, exemptions=EXEMPTIONS):
    out = check_links(repo)
    urs, reqs, comps = load_requirements(repo)
    req_ids = {r['key'] for r in reqs}
    out += check_numbering(urs | req_ids, retired, repo)
    srs_out, declared = check_srs(urs, reqs, confirmed)
    out += srs_out
    out += check_srs_matrix(repo, urs, declared)
    hld_out, hld_sections = check_hld(repo, req_ids, comps, confirmed)
    out += hld_out
    lld_out, modules = check_lld(repo, hld_sections, confirmed)
    out += lld_out
    cases, case_out = load_cases(repo)
    out += case_out + check_cases(cases, req_ids, urs, modules, confirmed)
    out += check_st_matrix(repo, urs, declared, cases)
    out += check_code(repo, modules, cases, confirmed)
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
