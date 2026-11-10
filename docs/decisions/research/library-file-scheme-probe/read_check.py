"""#197 の書き込みの可否を、openpyxl と zipfile で読み返して判定する。

使い方: venv/bin/python3 docs/decisions/research/library-file-scheme-probe/read_check.py <出力先>...
出力先は write_check.js が書いたディレクトリ。最初の出力先の中身を判定し、2 つ目からは
最初の出力先と同じファイルの sha256 を比べる（決定性）。期待は同じディレクトリの expected.json。
"""

import hashlib
import json
import os
import re
import sys
import zipfile
from xml.etree import ElementTree

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))


def _kind(value):
    if value is None:
        return None
    if isinstance(value, bool):
        return "b"
    if isinstance(value, (int, float)):
        return "n"
    return "s"


def check_sheet(path, expected):
    """1 つの XLSX を期待と比べ、項目ごとの判定の dict を返す。"""
    wb = openpyxl.load_workbook(path)
    result = {}
    names = wb.sheetnames
    result["シート"] = "一致" if names == expected["sheets"] else f"不一致 {names}"
    if "second_a1" in expected:
        got = wb[names[1]]["A1"].value if len(names) > 1 else None
        result["2 枚目の A1"] = "一致" if got == expected["second_a1"] else f"不一致 {got!r}"
    ws = wb[names[0]]
    merges = {str(r) for r in ws.merged_cells.ranges}
    if "merges" in expected:
        result["結合"] = "書ける" if merges == set(expected["merges"]) else f"書けない {sorted(merges)}"
    if "freeze" in expected:
        # topLeftCell だけでなく、枠が固定（frozen）で、分ける行の数が固定の行の上の行の数であることも見る
        pane = ws.sheet_view.pane
        want_rows = openpyxl.utils.cell.coordinate_to_tuple(expected["freeze"])[0] - 1
        frozen = (pane is not None and pane.state == "frozen" and pane.topLeftCell == expected["freeze"]
                  and int(pane.ySplit or 0) == want_rows)
        state = None if pane is None else f"{pane.topLeftCell} {pane.state} ySplit={pane.ySplit}"
        result["固定"] = "書ける" if frozen else f"書けない（{state}）"
    if "wrap" in expected:
        wrapped = bool(ws[expected["wrap"]].alignment.wrap_text)
        result["折り返し（参考）"] = "書ける" if wrapped else "書けない"

    # 期待が None のセルは、openpyxl では空文字のセルと見分けられないので、XML に要素が無いことを見る（DEC112）
    # 属性の順や名前空間の接頭辞によらないよう、XML を解析して c 要素の r 属性を集める
    with zipfile.ZipFile(path) as z:
        root = ElementTree.fromstring(z.read("xl/worksheets/sheet1.xml"))
    present = {el.get("r") for el in root.iter() if el.tag.rsplit("}", 1)[-1] == "c"}
    bad_values = []
    for ref, (value, kind) in expected["cells"].items():
        got = ws[ref].value
        if kind is None:
            if ref in present:
                bad_values.append(f"{ref}=セルがある")
        elif _kind(got) != kind or got != value:
            bad_values.append(f"{ref}={got!r}")
    result["値と型"] = "一致" if not bad_values else "不一致 " + " ".join(bad_values)

    formats = expected.get("formats", {})
    bad_formats = []
    for ref, (_value, kind) in expected["cells"].items():
        if kind != "n":
            continue
        want = formats.get(ref, "General")
        got = ws[ref].number_format
        if got != want:
            bad_formats.append(f"{ref}={got}")
    result["表示形式"] = "一致" if not bad_formats else "不一致 " + " ".join(bad_formats)
    return result


def core_dates(path):
    """docProps/core.xml の作成日時と更新日時の有無と値を返す。"""
    with zipfile.ZipFile(path) as z:
        try:
            text = z.read("docProps/core.xml").decode("utf-8")
        except KeyError:
            return {"created": "なし（core.xml が無い）", "modified": "なし（core.xml が無い）"}
    result = {}
    for key in ("created", "modified"):
        m = re.search(rf"<dcterms:{key}[^>]*>([^<]*)</dcterms:{key}>", text)
        result[key] = f"あり {m.group(1)}" if m else "なし"
    return result


def check_zip(path, date_time):
    """ZIP の各エントリの圧縮方式と時刻を判定する。"""
    result = {}
    with zipfile.ZipFile(path) as z:
        for info in z.infolist():
            method = "DEFLATE" if info.compress_type == zipfile.ZIP_DEFLATED else "DEFLATE でない"
            when = "時刻一致" if tuple(info.date_time) == tuple(date_time) else f"時刻不一致 {info.date_time}"
            result[info.filename] = f"{method} {when}"
    return result


def _sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def _zip_diff(a, b):
    """2 つの ZIP（XLSX）で中身か時刻が違うエントリの名前を返す。"""
    with zipfile.ZipFile(a) as za, zipfile.ZipFile(b) as zb:
        names = sorted(set(za.namelist()) | set(zb.namelist()))
        diff = []
        for n in names:
            try:
                ia, ib = za.getinfo(n), zb.getinfo(n)
            except KeyError:
                diff.append(f"{n}（片方に無い）")
                continue
            if za.read(n) != zb.read(n):
                diff.append(f"{n}（中身）")
            elif ia.date_time != ib.date_time:
                diff.append(f"{n}（時刻）")
        return diff


def main(dirs):
    with open(os.path.join(HERE, "expected.json"), encoding="utf-8") as f:
        expected = json.load(f)
    first = dirs[0]
    for cand in sorted(os.listdir(first)):
        cdir = os.path.join(first, cand)
        if not os.path.isdir(cdir):
            continue
        print(f"## {cand}")
        for name, key in (("application.xlsx", "application"), ("list.xlsx", "list")):
            path = os.path.join(cdir, name)
            if not os.path.exists(path):
                print(f"- {name}: 無い")
                continue
            try:
                items = check_sheet(path, expected[key])
            except Exception as e:  # 読めないことも結果として出す
                print(f"- {name}: openpyxl で読めない（{type(e).__name__}: {e}）")
                continue
            for item, value in items.items():
                print(f"- {name} {item}: {value}")
            for k, v in core_dates(path).items():
                print(f"- {name} {k}: {v}")
        props = os.path.join(cdir, "application-props.xlsx")
        if os.path.exists(props):
            print(f"- application-props.xlsx created: {core_dates(props)['created']}")
    for zname in ("zip-raw.zip", "zip-fixed.zip"):
        path = os.path.join(first, zname)
        if os.path.exists(path):
            for entry, value in check_zip(path, tuple(expected["zip"]["date_time"])).items():
                print(f"- {zname} {entry}: {value}")
    for other in dirs[1:]:
        print(f"## 決定性 {first} と {other}")
        for cand in sorted(os.listdir(first)):
            for name in ("application.xlsx", "list.xlsx"):
                a = os.path.join(first, cand, name)
                b = os.path.join(other, cand, name)
                if not (os.path.exists(a) and os.path.exists(b)):
                    continue
                if _sha256(a) == _sha256(b):
                    print(f"- {cand}/{name}: 一致")
                else:
                    print(f"- {cand}/{name}: 不一致 {', '.join(_zip_diff(a, b))}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("使い方: read_check.py <出力先>...")
    main(sys.argv[1:])
