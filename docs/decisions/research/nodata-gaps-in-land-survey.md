# 陸地の中の NODATA の調査（HLD 3.6・ADR-SRS-064）

- 調査日: 2026-10-03
- 目的: [HLD 3.5](../../30_HLD.md#35-fr-005-ピーク候補検出) の D57 が受け入れたリスク（NODATA に囲まれて人工ボーダーに届かない陸地が、海面確定規則で確定する）が実データでどれだけ起きるかを測る
- データ: 動作確認環境のローカルキャッシュ（`$DATA_DIR/tiles`。DEM5a・5b・5c は Z15、DEM10b は Z14）と、N03 の都道府県界（`$DATA_DIR/ref/N03-20260101_prefecture.geojson`）。キャッシュがある 1次メッシュは 13 件（5237〜5240・5337〜5340・5437〜5440・5539）。`DATA_DIR=/data` の環境で実行したので、スクリプトにはそのパスを直に書いた

## 測り方

1. 1次メッシュごとに、メッシュを覆う Z15 のタイルを並べ、画素ごとに DEM5a → 5b → 5c → 10b の順に最初の有効な値を採る（[FR-002](../../20_SRS.md#fr-002-dem-階層フォールバック) と同じ）。4 つとも NODATA の画素を「NODATA」、有効で 0 より大きい画素を「陸地」とする。画素の中心がメッシュの中にある画素だけを見る。
2. N03 の陸地のポリゴンを Z15 の画素に塗り、その中の NODATA を「陸地の欠け」とする（N03 の陸地には川・運河・湖も入る）。
3. 陸地（8 近傍）の連結成分と、陸地と陸地の欠けを合わせた連結成分を求め、欠けを埋めると 1 つになる陸地の成分の組を「欠けで分かれた組」とする。組の中でいちばん大きい成分を除いた成分（小片）ごとに、最高点と、欠けに接する画素の最高の標高を求める。欠けに接する標高は、欠けの下に隠れたコルの高さの目安である。
4. 別に、メッシュの範囲の Z15 のタイルの位置ごとに、DEM5a・5b・5c のどれかのファイルがあるかと、DEM10b の Z14 のタイル (x // 2, y // 2) のファイルがあるかを数える。

画像として読めないタイルが、5338 に 2 枚（`dem5b_png`・`dem5c_png` の `15/29011/12939.png`）、5437 に 12 枚（`dem5a_png`・`dem5b_png`・`dem5c_png` の `15/28912/12827.png`・`15/28913/12827.png`・`15/28914/12827.png`・`15/28914/12828.png`）あった（開いた 1 枚は、中身が XML のエラー応答 `NoSuchKey` だった）。スクリプトは、読めないタイルを無いタイルと同じく全画素 NODATA として扱い、出力の `unreadable` に挙げる（調査だけの扱いで、製品の C4 は D49 で止まる）。13 メッシュとも、下のスクリプトの版で測った。

## 結果: 陸地の欠け

| メッシュ | どの DEM も無いタイルの位置 | 陸地の欠けの画素 | 欠けで分かれた小片 | 欠けに接する標高の最大（m） | 小片の最高点の最大（m） | 最高点が 100m 以上の小片 | 読めないタイル |
|---|---|---|---|---|---|---|---|
| 5237 | 252 | 72,465 | 162 | 4.66 | 17.50 | 0 | 0 |
| 5238 | 1,669 | 21,825 | 148 | 5.77 | 5.77 | 0 | 0 |
| 5239 | 4,581 | 90,887 | 409 | 6.73 | 6.78 | 0 | 0 |
| 5240 | 5,904 | 30,201 | 51 | 12.20 | 18.77 | 0 | 0 |
| 5337 | 0 | 0 | 0 | — | — | 0 | 0 |
| 5338 | 0 | 0 | 0 | — | — | 0 | 2 |
| 5339 | 527 | 177,322 | 84 | 5.03 | 6.83 | 0 | 0 |
| 5340 | 2,731 | 73,995 | 61 | 6.80 | 6.80 | 0 | 0 |
| 5437 | 0 | 0 | 0 | — | — | 0 | 12 |
| 5438 | 0 | 0 | 0 | — | — | 0 | 0 |
| 5439 | 0 | 0 | 0 | — | — | 0 | 0 |
| 5440 | 2,587 | 117,273 | 24 | 4.77 | 4.77 | 0 | 0 |
| 5539 | 12 | 11,031,390 | 854 | 1,660.91 | 1,660.93 | 854 | 0 |

「小片」は、欠けで分かれた組ごとに最も大きい陸地の成分を除いた成分である（最も大きい成分は、メッシュの陸地の本体か、組の中で最も広い陸地）。5539 を除くと、小片は運河・河口の水面で隔てられた埋立地や中州で、欠けに接する標高は最大 12.2m、小片の最高点は最大 18.77m だった。プロミネンス一次フィルタ閾値の下限（100m）より十分低く、海面確定規則で確定してもピークの判定には効かない。最も大きい成分の側は、この集計では見ていない。

5539 は、DEM10b のタイルがキャッシュにほぼ無かった（下の表）。2026-04-22 の取得の記録では DEM10b の 1,794 枚すべてが「存在なし」だったが、提供元には実在した（`dem_png/14/14524/6412.png` が HTTP 200。2026-10-03）。DEM5a は航空レーザ測量の範囲だけで山地に NODATA が多く、DEM10b が無いとそれが穴になる。最高点 1,660.93m の陸地を含む 854 片が穴で分かれ、どれも人工ボーダーに届かなければ海面確定規則で確定する。

## 結果: DEM5 のタイルがある位置の DEM10b

| メッシュ | DEM5 のどれかがある位置 | そのうち DEM10b が無い位置 | 割合 |
|---|---|---|---|
| 5237 | 6,567 | 2 | 0.030% |
| 5238 | 5,131 | 0 | 0.000% |
| 5239 | 2,086 | 3 | 0.144% |
| 5240 | 943 | 0 | 0.000% |
| 5337 | 6,992 | 0 | 0.000% |
| 5338 | 6,987 | 0 | 0.000% |
| 5339 | 6,385 | 13 | 0.204% |
| 5340 | 4,152 | 3 | 0.072% |
| 5437 | 6,744 | 0 | 0.000% |
| 5438 | 6,986 | 0 | 0.000% |
| 5439 | 6,992 | 0 | 0.000% |
| 5440 | 4,242 | 5 | 0.118% |
| 5539 | 7,071 | 6,964 | 98.487% |

5339 と 5440 の 0 でない位置の DEM5 には陸地の画素があった（東京湾の埋立地など。最高 40.35m）。DEM10b より新しい陸地と見た。

## 結論

- 調査した 13 メッシュでは、存在メッシュの中の部分的な欠け（地理院の未整備）で切り離された小片は、水面で隔てられた低い陸地（最高点 18.77m 以下）に限られた。この範囲では D57 の扱いのままでよい。
- DEM10b のタイルの取得の漏れは、山地の陸地を大きく分け、プロミネンスを黙って誤らせる。DEM5 のタイルがある位置のうち DEM10b のタイルが無い位置の割合は、漏れたメッシュで 98.487%、ほかで 0.204% 以下と大きく離れるので、1% を超えれば止める（[ADR-SRS-064](../ADR-SRS-064-stop-on-missing-dem10b-tiles.md)、[HLD 3.4](../../30_HLD.md#34-fr-004-33メッシュ結合解析オーケストレーション) の D64）。
- 測れたのは関東・中部・南東北の 13 メッシュだけである。全国の取得の後に、割合を全メッシュで確かめる（[HLD 3.4.5](../../30_HLD.md#345-未決事項と後続) の 11）。

## スクリプト

Python 3.14、numpy 2.5、scipy 1.18、Pillow 12.3 で実行した。

陸地の欠け（`nodata_gap.py <メッシュ> ...`）:

```python
# HLD 3.5.5 の 5 の実測: 陸地の中の NODATA（4 DEM とも値が無い画素）が陸地を分けるか
# 使い方: python nodata_gap.py <mesh> [<mesh> ...]
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, UnidentifiedImageError
from scipy import ndimage

TILES = '/data/tiles'
N03 = '/data/ref/N03-20260101_prefecture.geojson'
Z = 15
N = 2 ** Z


def tile_xy(lon, lat):
    x = (lon + 180.0) / 360.0 * N
    r = math.radians(lat)
    y = (1.0 - math.log(math.tan(r) + 1.0 / math.cos(r)) / math.pi) / 2.0 * N
    return x, y


def gpix(lon, lat):
    x, y = tile_xy(lon, lat)
    return x * 256.0, y * 256.0


UNREADABLE = []


def decode(path):
    # 調査だけの扱い: 画像として読めないタイルは、無いタイルと同じく全画素 NODATA にする
    # （製品の C4 は D49 で止まる）
    try:
        a = np.asarray(Image.open(path).convert('RGB'), dtype=np.int64)
    except UnidentifiedImageError:
        UNREADABLE.append(path)
        return np.ones((256, 256), dtype=bool), np.zeros((256, 256))
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    nd = (r == 128) & (g == 0) & (b == 0)
    x = r * 65536 + g * 256 + b
    h = np.where(x < 2 ** 23, x, x - 2 ** 24).astype(np.float64) * 0.01
    return nd, h


def tile_layers(tx, ty):
    for d in ('dem5a_png', 'dem5b_png', 'dem5c_png'):
        p = f'{TILES}/{d}/15/{tx}/{ty}.png'
        if os.path.exists(p):
            yield decode(p)
    p = f'{TILES}/dem_png/14/{tx // 2}/{ty // 2}.png'
    if os.path.exists(p):
        nd, h = decode(p)
        ox, oy = (tx % 2) * 128, (ty % 2) * 128
        nd = nd[oy:oy + 128, ox:ox + 128].repeat(2, 0).repeat(2, 1)
        h = h[oy:oy + 128, ox:ox + 128].repeat(2, 0).repeat(2, 1)
        yield nd, h


def load_n03():
    with open(N03, encoding='utf-8') as f:
        return json.load(f)['features']


def polys(features, lon0, lat0, lon1, lat1):
    for ft in features:
        g = ft['geometry']
        parts = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        for poly in parts:
            ring = poly[0]
            xs = [p[0] for p in ring]
            ys = [p[1] for p in ring]
            if max(xs) < lon0 or min(xs) > lon1 or max(ys) < lat0 or min(ys) > lat1:
                continue
            yield poly


def run(mesh, features):
    UNREADABLE.clear()
    lat0 = (mesh // 100) / 1.5
    lat1 = lat0 + 2.0 / 3.0
    lon0 = mesh % 100 + 100.0
    lon1 = lon0 + 1.0
    x0, y1 = tile_xy(lon0, lat0)
    x1, y0 = tile_xy(lon1, lat1)
    tx0, tx1, ty0, ty1 = int(x0), int(x1), int(y0), int(y1)
    W, H = (tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256
    nodata = np.ones((H, W), dtype=bool)
    land = np.zeros((H, W), dtype=bool)
    elev_m = np.zeros((H, W), dtype=np.float32)
    missing = 0
    for ty in range(ty0, ty1 + 1):
        for tx in range(tx0, tx1 + 1):
            nd_all = np.ones((256, 256), dtype=bool)
            elev = np.zeros((256, 256))
            any_tile = False
            for nd, h in tile_layers(tx, ty):
                any_tile = True
                take = nd_all & ~nd
                elev[take] = h[take]
                nd_all &= nd
            if not any_tile:
                missing += 1
            oy, ox = (ty - ty0) * 256, (tx - tx0) * 256
            nodata[oy:oy + 256, ox:ox + 256] = nd_all
            land[oy:oy + 256, ox:ox + 256] = ~nd_all & (elev > 0)
            elev_m[oy:oy + 256, ox:ox + 256] = elev
    # 画素の中心がメッシュの中にある画素
    gx0, gy0 = tx0 * 256, ty0 * 256
    cx = np.arange(W) + gx0 + 0.5
    cy = np.arange(H) + gy0 + 0.5
    lon = cx / (256 * N) * 360.0 - 180.0
    lat = np.degrees(np.arctan(np.sinh(np.pi * (1 - 2 * cy / (256 * N)))))
    inmesh = ((lat >= lat0) & (lat < lat1))[:, None] & ((lon >= lon0) & (lon < lon1))[None, :]
    # N03 の陸地
    img = Image.new('1', (W, H), 0)
    dr = ImageDraw.Draw(img)
    for poly in polys(features, lon0, lat0, lon1, lat1):
        for k, ring in enumerate(poly):
            pts = [(gpix(p[0], p[1])[0] - gx0, gpix(p[0], p[1])[1] - gy0) for p in ring]
            dr.polygon(pts, fill=1 if k == 0 else 0)
    n03 = np.asarray(img, dtype=bool)
    del img
    nodata &= inmesh
    land &= inmesh
    gap = nodata & n03 & inmesh
    s8 = np.ones((3, 3), dtype=int)
    lab_land, n_land = ndimage.label(land, structure=s8)
    lab_fill, n_fill = ndimage.label(land | gap, structure=s8)
    # 欠けを埋めると合流する陸地の成分: 埋めた後の成分ごとに、中の陸地の成分の数
    pairs = np.unique(np.stack([lab_fill[land], lab_land[land]]), axis=1)
    fill_ids, counts = np.unique(pairs[0], return_counts=True)
    split = fill_ids[counts >= 2]
    rows = []
    if len(split):
        sizes = np.bincount(lab_land.ravel())
        adj = land & ndimage.binary_dilation(gap, structure=s8)
        small = []
        for f in split:
            ls = pairs[1][pairs[0] == f]
            ls = sorted(ls, key=lambda i: -sizes[i])
            small.extend(int(i) for i in ls[1:])
        small = np.array(small)
        peak = ndimage.maximum(elev_m, lab_land, index=small)
        lab_adj = np.where(adj, lab_land, 0)
        bnd = ndimage.maximum(elev_m, lab_adj, index=small)
        for c, pk, bd in zip(small, peak, bnd):
            rows.append((int(c), int(sizes[c]), round(float(pk), 2), round(float(bd), 2)))
        rows.sort(key=lambda r: -r[3])
    lab_gap, n_gap = ndimage.label(gap, structure=s8)
    gsz = np.bincount(lab_gap.ravel())[1:] if n_gap else np.array([0])
    print(json.dumps({
        'mesh': mesh, 'tiles': (tx1 - tx0 + 1) * (ty1 - ty0 + 1), 'tiles_without_any_dem': missing,
        'pixels_in_mesh': int(inmesh.sum()), 'land_pixels': int(land.sum()),
        'nodata_pixels': int(nodata.sum()), 'gap_pixels_in_n03': int(gap.sum()),
        'gap_components': int(n_gap), 'gap_largest': int(gsz.max()),
        'land_components': int(n_land), 'filled_components': int(n_fill),
        'split_groups': len(split), 'separated_components': len(rows),
        'sep_over_10m_boundary': sum(1 for r in rows if r[3] >= 10.0),
        'max_peak_of_separated': max((r[2] for r in rows), default=None),
        'separated_peak_over_100m': sum(1 for r in rows if r[2] >= 100.0),
        'unreadable': sorted(UNREADABLE),
        'worst_by_boundary_elev(comp,px,peak,boundary)': rows[:8],
    }, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    feats = load_n03()
    for m in sys.argv[1:]:
        run(int(m), feats)
```

DEM10b の割合（`ratio.py`）:

```python
import math, os
N = 2 ** 15
def txy(lon, lat):
    r = math.radians(lat)
    return (lon + 180) / 360 * N, (1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * N
for m in (5237, 5238, 5239, 5240, 5337, 5338, 5339, 5340, 5437, 5438, 5439, 5440, 5539):
    lat0 = (m // 100) / 1.5; lon0 = m % 100 + 100
    x0, y1 = txy(lon0, lat0); x1, y0 = txy(lon0 + 1, lat0 + 2 / 3)
    d5 = bad = 0
    for ty in range(int(y0), int(y1) + 1):
        for tx in range(int(x0), int(x1) + 1):
            if any(os.path.exists(f'/data/tiles/{d}/15/{tx}/{ty}.png') for d in ('dem5a_png', 'dem5b_png', 'dem5c_png')):
                d5 += 1
                if not os.path.exists(f'/data/tiles/dem_png/14/{tx//2}/{ty//2}.png'):
                    bad += 1
    print(m, d5, bad, f'{100*bad/d5:.3f}%' if d5 else '-')
```
