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

    def test_created_present_and_absent(self):
        _book(self.path("with.xlsx"))
        _strip_created(self.path("with.xlsx"), self.path("without.xlsx"))
        self.assertTrue(read_check.core_dates(self.path("with.xlsx"))["created"].startswith("あり"))
        self.assertEqual(read_check.core_dates(self.path("without.xlsx"))["created"], "なし")


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
