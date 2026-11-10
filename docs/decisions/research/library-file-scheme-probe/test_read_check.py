"""read_check.py の判定の試験（#197）。

実行: venv/bin/python3 -m unittest discover -s docs/decisions/research/library-file-scheme-probe -p 'test_*.py'
"""

import os
import sys
import tempfile
import unittest
import zipfile

import openpyxl

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import read_check  # noqa: E402

EXPECTED = {
    "sheets": ["Sheet1"],
    "merges": ["A3:A4"],
    "freeze": "A6",
    "cells": {"A1": ["題", "s"], "E6": [12, "n"], "F6": [None, None], "G6": [35.1, "n"]},
    "formats": {"G6": "0.00000000"},
}


def _book(path, *, freeze="A6", e6=12, g6_format="0.00000000", f6=None):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    ws["A1"] = "題"
    ws["E6"] = e6
    if f6 is not None:
        ws["F6"] = f6
    ws["G6"] = 35.1
    ws["G6"].number_format = g6_format
    ws.merge_cells("A3:A4")
    if freeze:
        ws.freeze_panes = freeze
    wb.save(path)


def _strip_created(src, dst):
    """docProps/core.xml から dcterms:created を除いた写しを作る。"""
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "docProps/core.xml":
                text = data.decode("utf-8")
                start = text.find("<dcterms:created")
                end = text.find("</dcterms:created>") + len("</dcterms:created>")
                if start >= 0:
                    text = text[:start] + text[end:]
                data = text.encode("utf-8")
            zout.writestr(info, data)


def _rewrite_sheet(src, dst, change):
    """xl/worksheets/sheet1.xml を change で書き換えた写しを作る。"""
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "xl/worksheets/sheet1.xml":
                data = change(data.decode("utf-8")).encode("utf-8")
            zout.writestr(info, data)


class CheckSheetTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def path(self, name):
        return os.path.join(self.tmp.name, name)

    def test_good_book_passes_every_item(self):
        _book(self.path("good.xlsx"))
        result = read_check.check_sheet(self.path("good.xlsx"), EXPECTED)
        self.assertEqual(result["固定"], "書ける")
        self.assertEqual(result["結合"], "書ける")
        self.assertEqual(result["シート"], "一致")
        self.assertEqual(result["値と型"], "一致")
        self.assertEqual(result["表示形式"], "一致")

    def test_missing_freeze_is_reported(self):
        _book(self.path("nofreeze.xlsx"), freeze=None)
        result = read_check.check_sheet(self.path("nofreeze.xlsx"), EXPECTED)
        self.assertTrue(result["固定"].startswith("書けない"), result["固定"])

    def test_number_written_as_string_is_a_type_mismatch(self):
        _book(self.path("strnum.xlsx"), e6="12")
        result = read_check.check_sheet(self.path("strnum.xlsx"), EXPECTED)
        self.assertTrue(result["値と型"].startswith("不一致"), result["値と型"])
        self.assertIn("E6", result["値と型"])

    def test_empty_string_cell_is_a_mismatch(self):
        _book(self.path("emptystr.xlsx"), f6="")
        result = read_check.check_sheet(self.path("emptystr.xlsx"), EXPECTED)
        self.assertIn("F6", result["値と型"])

    def test_wrong_number_format_is_reported(self):
        _book(self.path("fmt.xlsx"), g6_format="0.00")
        result = read_check.check_sheet(self.path("fmt.xlsx"), EXPECTED)
        self.assertTrue(result["表示形式"].startswith("不一致"), result["表示形式"])
        self.assertIn("G6", result["表示形式"])

    def test_format_on_number_without_expected_format_is_reported(self):
        _book(self.path("fmt2.xlsx"))
        wb = openpyxl.load_workbook(self.path("fmt2.xlsx"))
        wb.active["E6"].number_format = "0.0"
        wb.save(self.path("fmt2.xlsx"))
        result = read_check.check_sheet(self.path("fmt2.xlsx"), EXPECTED)
        self.assertIn("E6", result["表示形式"])

    def test_second_sheet_a1_is_compared(self):
        wb = openpyxl.Workbook()
        wb.active.title = "一覧"
        wb.create_sheet("出典")["A1"] = "違う文"
        wb.save(self.path("two.xlsx"))
        expected = {"sheets": ["一覧", "出典"], "cells": {}, "second_a1": "出典の文"}
        result = read_check.check_sheet(self.path("two.xlsx"), expected)
        self.assertTrue(result["2 枚目の A1"].startswith("不一致"), result["2 枚目の A1"])

    def test_cell_with_r_not_first_attribute_is_found(self):
        # 期待が空のセルに値があり、XML の属性の順が t の後に r のときも見逃さない（Codex の push 前のレビュー I2）
        _book(self.path("order.xlsx"))
        cell = '<row r="7"><c t="inlineStr" r="F6"><is><t>x</t></is></c></row>'
        _rewrite_sheet(self.path("order.xlsx"), self.path("order2.xlsx"),
                       lambda xml: xml.replace("</sheetData>", cell + "</sheetData>"))
        result = read_check.check_sheet(self.path("order2.xlsx"), EXPECTED)
        self.assertIn("F6", result["値と型"])

    def test_split_pane_is_not_a_freeze(self):
        # topLeftCell が A6 でも、state が frozen でない分割の枠は固定でない（argon の push 前のレビュー 4）
        _book(self.path("split.xlsx"))
        _rewrite_sheet(self.path("split.xlsx"), self.path("split2.xlsx"),
                       lambda xml: xml.replace('state="frozen"', 'state="split"'))
        result = read_check.check_sheet(self.path("split2.xlsx"), EXPECTED)
        self.assertTrue(result["固定"].startswith("書けない"), result["固定"])

    def test_fractional_y_split_is_not_a_freeze(self):
        # ySplit は 5 ちょうどでなければ、A6 での固定でない（Codex の確認限定巡）
        _book(self.path("half.xlsx"))
        _rewrite_sheet(self.path("half.xlsx"), self.path("half2.xlsx"),
                       lambda xml: xml.replace('ySplit="5"', 'ySplit="5.5"'))
        result = read_check.check_sheet(self.path("half2.xlsx"), EXPECTED)
        self.assertTrue(result["固定"].startswith("書けない"), result["固定"])

    def test_missing_merge_is_reported(self):
        _book(self.path("nomerge.xlsx"))
        wb = openpyxl.load_workbook(self.path("nomerge.xlsx"))
        wb.active.unmerge_cells("A3:A4")
        wb.save(self.path("nomerge.xlsx"))
        result = read_check.check_sheet(self.path("nomerge.xlsx"), EXPECTED)
        self.assertTrue(result["結合"].startswith("書けない"), result["結合"])

    def test_wrong_sheet_name_is_reported(self):
        _book(self.path("name.xlsx"))
        wb = openpyxl.load_workbook(self.path("name.xlsx"))
        wb.active.title = "シート1"
        wb.save(self.path("name.xlsx"))
        result = read_check.check_sheet(self.path("name.xlsx"), EXPECTED)
        self.assertTrue(result["シート"].startswith("不一致"), result["シート"])

    def test_same_type_different_value_is_reported(self):
        _book(self.path("val.xlsx"), e6=13)
        result = read_check.check_sheet(self.path("val.xlsx"), EXPECTED)
        self.assertIn("E6", result["値と型"])

    def test_created_present_and_absent(self):
        _book(self.path("with.xlsx"))
        _strip_created(self.path("with.xlsx"), self.path("without.xlsx"))
        self.assertTrue(read_check.core_dates(self.path("with.xlsx"))["created"].startswith("あり"))
        self.assertEqual(read_check.core_dates(self.path("without.xlsx"))["created"], "なし")


class DeterminismTest(unittest.TestCase):
    def test_missing_file_in_other_dir_is_reported(self):
        # 比べる先にファイルが無いとき、黙って飛ばさない（argon の push 前のレビュー 4 の 1 つ目）
        import contextlib
        import io
        with tempfile.TemporaryDirectory() as tmp:
            first = os.path.join(tmp, "first", "b")
            os.makedirs(first)
            _book(os.path.join(first, "application.xlsx"))
            os.makedirs(os.path.join(tmp, "other"))
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                read_check.main([os.path.join(tmp, "first"), os.path.join(tmp, "other")])
            self.assertIn("b/application.xlsx: 比べる先に無い", out.getvalue())


class CheckZipTest(unittest.TestCase):
    def test_deflate_and_date_time(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "a.zip")
            with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
                z.writestr(zipfile.ZipInfo("x.txt", (2026, 11, 8, 12, 34, 56)), "x",
                           compress_type=zipfile.ZIP_DEFLATED)
                z.writestr(zipfile.ZipInfo("y.txt", (2026, 11, 8, 3, 34, 56)), "y",
                           compress_type=zipfile.ZIP_STORED)
            result = read_check.check_zip(path, (2026, 11, 8, 12, 34, 56))
            self.assertEqual(result["x.txt"], "DEFLATE 時刻一致")
            self.assertEqual(result["y.txt"], "DEFLATE でない 時刻不一致 (2026, 11, 8, 3, 34, 56)")


if __name__ == "__main__":
    unittest.main()
