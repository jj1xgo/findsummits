"""headless_probe.js の出力（JSON の行）や、持ち主が貼った JSON を、1 行 1 項目に並べる（#197）。

使い方: venv/bin/python3 docs/decisions/research/library-file-scheme-probe/summarize.py <ファイル>...
ファイルは 1 行 1 つの JSON（headless_probe.js の出力）か、ページの JSON 1 つ。
"""

import json
import sys


def _rows(obj):
    step = obj.get("step", "")
    page = obj.get("json", obj)
    if not isinstance(page, dict):
        return [f"{step}: 結果なし"]
    if "answer" in obj:
        return [f"{step}: {obj['answer']}"]
    if "saved" in obj:
        return [f"{step}: {obj['saved']}"]
    head = f"{step} {page.get('protocol', '')} brave={page.get('brave', '?')} {page.get('userAgent', '')}"
    lines = [head.strip()]
    for r in page.get("results", []):
        lines.append(f"  {r['id']} {r['status']} {r['detail']}")
    return lines


def main(paths):
    for p in paths:
        print(f"## {p}")
        with open(p, encoding="utf-8") as f:
            text = f.read().strip()
        try:
            objs = [json.loads(text)]
        except json.JSONDecodeError:
            objs = [json.loads(line) for line in text.splitlines() if line.strip()]
        for obj in objs:
            for line in _rows(obj):
                print(line)


if __name__ == "__main__":
    main(sys.argv[1:])
