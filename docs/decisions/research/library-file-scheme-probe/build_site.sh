#!/bin/bash
# #197 の確かめ用のページ一式を build/probe-site/ に組み立てる。
# 使い方: リポジトリのルートで bash docs/decisions/research/library-file-scheme-probe/build_site.sh
# build/probe-site/ に site/ の中身と probe_expected.js（expected.json から作る）を並べ、同じ中身を
# findsummits-probe-197/ のフォルダに入れた probe.zip も置く（file:// で開くときに落として展開する）。
set -euo pipefail

here=docs/decisions/research/library-file-scheme-probe
stage=build/probe-stage/findsummits-probe-197
site=build/probe-site

rm -rf build/probe-stage "$site"
mkdir -p "$stage" "$site"
cp -R "$here/site/." "$stage/"
{ printf 'window.FINDSUMMITS_PROBE_EXPECTED = '; cat "$here/expected.json"; printf ';\n'; } >"$stage/probe_expected.js"

(cd build/probe-stage && zip -q -r -X ../probe.zip findsummits-probe-197)
cp -R "$stage/." "$site/"
mv build/probe.zip "$site/probe.zip"
find "$site" -type f | sort
