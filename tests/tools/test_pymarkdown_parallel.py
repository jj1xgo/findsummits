"""tools/pymarkdown_parallel.py のテスト（標準ライブラリの unittest）。実物の pymarkdown を起動する。"""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / 'tools' / 'pymarkdown_parallel.py'

CLEAN = '# Title\n\nbody\n'
# MD012（連続する空行）と MD041（先頭が見出しでない）に当たる
BAD = 'text\n\n\n# H\n'


class PymarkdownParallelTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.dir = Path(self._tmp.name)
        self.config = self.dir / 'config.json'
        self.config.write_text('{}', encoding='utf-8')

    def write(self, name, text):
        path = self.dir / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        return str(path)

    def run_script(self, *args, env=None, config=None):
        cmd = [sys.executable, str(SCRIPT), '-c', str(config or self.config), *args]
        return subprocess.run(cmd, capture_output=True, text=True, env=env)

    def test_clean_files_pass_without_output(self):
        a = self.write('a.md', CLEAN)
        b = self.write('b.md', CLEAN)
        result = self.run_script(a, b)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout, '')

    def test_one_violating_file_among_clean_files_fails_and_is_named(self):
        a = self.write('a.md', CLEAN)
        bad = self.write('bad.md', BAD)
        c = self.write('c.md', CLEAN)
        result = self.run_script(a, bad, c)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(bad, result.stdout)
        self.assertIn('MD012', result.stdout)
        self.assertNotIn(a, result.stdout)
        self.assertNotIn(c, result.stdout)

    def test_output_follows_input_order_even_when_sizes_differ(self):
        small = self.write('small.md', BAD)
        big = self.write('big.md', BAD + 'filler line\n\n' * 200)
        result = self.run_script(small, big)
        self.assertNotEqual(result.returncode, 0)
        self.assertLess(result.stdout.index(small), result.stdout.index(big))
        # 逆の順で渡せば逆の順で出る
        result = self.run_script(big, small)
        self.assertLess(result.stdout.index(big), result.stdout.index(small))

    def test_failure_of_pymarkdown_itself_is_propagated(self):
        a = self.write('a.md', CLEAN)
        result = self.run_script(a, config=self.dir / 'no_such_config.json')
        self.assertNotEqual(result.returncode, 0)
        # pymarkdown の「設定ファイルが無い」旨の出力が捨てられずに届く
        self.assertIn('does not exist', result.stdout + result.stderr)

    def test_recursive_scans_a_directory(self):
        self.write('docs/ok.md', CLEAN)
        bad = self.write('docs/sub/bad.md', BAD)
        result = self.run_script('-r', str(self.dir / 'docs'))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(bad, result.stdout)

    def test_violation_lines_equal_one_process_scan(self):
        files = [self.write(f'f{i}.md', BAD if i % 2 else CLEAN) for i in range(6)]
        single = subprocess.run(
            [sys.executable, '-m', 'pymarkdown', '-c', str(self.config), 'scan', *files],
            capture_output=True, text=True)
        parallel = self.run_script(*files)
        self.assertEqual(single.returncode, 1)
        self.assertEqual(sorted(parallel.stdout.splitlines()),
                         sorted(single.stdout.splitlines()))

    def test_single_job_gives_the_same_result(self):
        bad = self.write('bad.md', BAD)
        a = self.write('a.md', CLEAN)
        env = dict(os.environ, LINT_JOBS='1')
        result = self.run_script(a, bad, env=env)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(bad, result.stdout)


if __name__ == '__main__':
    unittest.main()
