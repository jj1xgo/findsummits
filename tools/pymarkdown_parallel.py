#!/usr/bin/env python3
"""pymarkdown を対象（ファイルかディレクトリ）ごとに並列で走らせる。

pymarkdown は 1 回の起動で全ファイルを順に走査し、大きいファイルほど急に遅くなる
（2MB の `docs/40_LLD.md` 1 本で十数秒。全体は約 27 秒。マシンの負荷が高いと数倍になる）。
対象ごとに別のプロセスで走らせれば、合計の所要は最も遅い 1 本に近づく（全体で約 16 秒）。

- 出力はファイルごとに溜め、入力の順に出す（並列でも行が混ざらず、毎回同じ順になる）。
- 終了コードは、1 つでも 0 以外で終わった対象があれば 0 以外（シグナルで落ちた場合も 0 以外）。
- 大きい対象から先に起動する（小さいものが先だと、最も遅い 1 本の開始が後ろに回る）。
- 並列数は `-j`、無ければ環境変数 `LINT_JOBS`、無ければ CPU 数。
"""
import argparse
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor


def tree_size(path):
    """ファイルの大きさ、ディレクトリなら下のファイルの大きさの和（起動の順を決めるためだけに使う）。"""
    if os.path.isfile(path):
        return os.path.getsize(path)
    total = 0
    for root, _dirs, files in os.walk(path):
        for name in files:
            try:
                total += os.path.getsize(os.path.join(root, name))
            except OSError:
                pass
    return total


def scan(config, recursive, target):
    cmd = [sys.executable, '-m', 'pymarkdown', '-c', config, 'scan']
    if recursive:
        cmd.append('-r')
    if target is not None:
        cmd.append(target)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def default_jobs():
    env = os.environ.get('LINT_JOBS')
    if env:
        return max(1, int(env))
    return os.cpu_count() or 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('-c', '--config', default='.pymarkdown')
    parser.add_argument('-j', '--jobs', type=int, default=None)
    parser.add_argument('-r', '--recursive', action='store_true')
    parser.add_argument('targets', nargs='*')
    args = parser.parse_args(argv)

    # 対象が無いときは、1 回の起動と同じ振る舞い（pymarkdown 自身の判断）にする
    targets = args.targets or [None]
    jobs = max(1, args.jobs if args.jobs is not None else default_jobs())

    order = sorted(range(len(targets)),
                   key=lambda i: -(tree_size(targets[i]) if targets[i] is not None else 0))
    results = [None] * len(targets)
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        futures = {i: pool.submit(scan, args.config, args.recursive, targets[i]) for i in order}
        for i, future in futures.items():
            results[i] = future.result()

    worst = 0
    for code, out, err in results:
        sys.stdout.write(out)
        sys.stderr.write(err)
        if code != 0:
            worst = max(worst, code if code > 0 else 1)
    sys.stdout.flush()
    sys.stderr.flush()
    return worst


if __name__ == '__main__':
    sys.exit(main())
