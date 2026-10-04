"""tools/lint_geojson.py のテスト（標準ライブラリの unittest）"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
import lint_geojson as lg  # noqa: E402


class CheckFileTest(unittest.TestCase):
    def check(self, text):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'x.geojson'
            path.write_text(text, encoding='utf-8')
            return lg.check_file(str(path))

    def test_valid_feature_collection_has_no_violation(self):
        self.assertEqual(self.check(
            '{"type": "FeatureCollection", "features": [{"type": "Feature", '
            '"geometry": {"type": "Point", "coordinates": [139.0, 35.0]}, '
            '"properties": {}}]}'), [])

    def test_unsupported_type_is_structure_violation(self):
        violations = self.check('{"type": "Nope"}')
        self.assertEqual(len(violations), 1)
        self.assertIn(': STRUCTURE: ', violations[0])
        self.assertIn('Nope', violations[0])

    def test_object_without_type_is_structure_violation(self):
        violations = self.check('{}')
        self.assertEqual(len(violations), 1)
        self.assertIn(': STRUCTURE: ', violations[0])

    def test_non_object_top_level_is_structure_violation(self):
        violations = self.check('[]')
        self.assertEqual(len(violations), 1)
        self.assertIn(': STRUCTURE: ', violations[0])

    def test_unsupported_geometry_type_in_feature_is_structure_violation(self):
        violations = self.check(
            '{"type": "FeatureCollection", "features": [{"type": "Feature", '
            '"geometry": {"type": "Nope", "coordinates": []}, "properties": {}}]}')
        self.assertTrue(violations)
        self.assertTrue(all(': STRUCTURE: ' in v for v in violations))

    def test_invalid_geometry_is_still_reported(self):
        violations = self.check(
            '{"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", '
            '"coordinates": [[[0, 0], [1, 1], [0, 0]]]}}')
        self.assertTrue(any(': INVALID-' in v for v in violations), violations)


if __name__ == '__main__':
    unittest.main()
