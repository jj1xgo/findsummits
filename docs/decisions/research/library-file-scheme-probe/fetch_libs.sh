#!/bin/bash
# #197 の確かめに使うライブラリの配布用のファイルを build/probe-libs/ へ取り、ハッシュを出す。
# 使い方: リポジトリのルートで bash docs/decisions/research/library-file-scheme-probe/fetch_libs.sh
# 出力: 1 行 1 ファイルで「名前 HTTP の状態 バイト数 sha384 sha512」。公開の値と食い違えば終了状態 1。
set -euo pipefail

out=build/probe-libs
mkdir -p "$out"

# 名前 URL 照合する公開の値（無ければ -）
libs=(
  "leaflet.js https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.js sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
  "leaflet.css https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
  "jszip.min.js https://cdn.jsdelivr.net/npm/jszip@3.10.2/dist/jszip.min.js sha512-/ICos1xr6gGjsbC2d7Z6D0hmKAnNbkCv5Pp803Q75xgHowbEcgI4CVOHMHUux/ZorCuod6dzuJOjfNoCKV0tRw=="
  "jszip.js https://cdn.jsdelivr.net/npm/jszip@3.10.2/dist/jszip.js -"
  "xlsx.full.min.js https://cdn.sheetjs.com/xlsx-0.20.3/package/dist/xlsx.full.min.js -"
  "exceljs.min.js https://cdn.jsdelivr.net/npm/exceljs@4.4.0/dist/exceljs.min.js sha512-dlPw+ytv/6JyepmelABrgeYgHI0O+frEwgfnPdXDTOIZz+eDgfW07QXG02/O8COfivBdGNINy+Vex+lYmJ5rxw=="
  "xlsx-js-style.bundle.js https://cdn.jsdelivr.net/npm/xlsx-js-style@1.2.0/dist/xlsx.bundle.js -"
)

sri() {  # sri <アルゴリズム> <ファイル> → <アルゴリズム>-<Base64>
  printf '%s-%s' "$1" "$(openssl dgst "-$1" -binary "$2" | base64 -w0)"
}

bad=0
for row in "${libs[@]}"; do
  read -r name url want <<<"$row"
  code=$(curl -sS -L -o "$out/$name" -w '%{http_code}' "$url")
  size=$(wc -c <"$out/$name")
  h384=$(sri sha384 "$out/$name")
  h512=$(sri sha512 "$out/$name")
  note=""
  if [ "$code" != 200 ]; then note="HTTP-NG"; bad=1; fi
  if [ "$want" != - ]; then
    algo=${want%%-*}
    got=$(sri "$algo" "$out/$name")
    if [ "$got" = "$want" ]; then note="$note 公開の値と一致"; else note="$note 公開の値と不一致"; bad=1; fi
  fi
  printf '%s %s %s %s %s %s\n' "$name" "$code" "$size" "$h384" "$h512" "$note"
done
exit "$bad"
