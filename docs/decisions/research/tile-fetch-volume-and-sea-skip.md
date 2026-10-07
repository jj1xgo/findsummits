# タイル取得の要求数と海の位置の省略の調査（ADR-SRS-069）

- 調査日: 2026-10-07
- 目的: 処理範囲 175 メッシュの標高タイルの取得で、要求の件数と所要時間を見積もり、DEM5 の取り方と海の位置の省略を決める材料にする（[ADR-SRS-069](../ADR-SRS-069-conditional-dem5-fetch-and-sea-skip.md)）。
- データ: 動作確認環境のローカルキャッシュ（`$DATA_DIR/tiles`）と、国土地理院のタイルサーバーへの 60 件の要求（2026-10-07）。

## 測定の対象

- コンテナの `$DATA_DIR/tiles`。12 メッシュ（5237〜5240、5337〜5340、5437〜5440）、Z15 の位置が 82,125、Z14 のタイルが 20,679。
- 5539 は DEM10b が 4 枚しか無い（2026-04-22 の取得ですべて 404 になり、その後に取り直していない。[ADR-SRS-064](../ADR-SRS-064-stop-on-missing-dem10b-tiles.md) の調査と同じ件）ので外した。
- 取得ログ（`$DATA_DIR/logs/prefetch_*.log`）のエラーは 0 件で、ファイルが無い位置は 404 と見なした。キャッシュには読めないファイルが 20 個（S3 の `NoSuchKey` の XML と 0 バイト）あり、これも 404 と見なした。
- DEM5a の NODATA は画素値 `0x800000`（`src/elevation.c` と同じ判定）で数えた。

## 結果（Z15 の位置 82,125 に対する割合）

| 状態 | 位置の数 | 割合 |
|---|---|---|
| DEM5a が 404 | 19,540 | 23.8% |
| DEM5a はあるが NODATA の画素を含む | 36,661 | 44.6% |
| DEM5a に欠けが無い | 25,924 | 31.6% |
| DEM5a・5b とも 404 | 19,299 | 23.5% |
| 親の DEM10b（Z14）が 404 | 18,119 | 22.1% |

Z14 の DEM10b の 404 は 4,650／20,679（22.5%）。

## DEM5a の欠けの形

欠けのある DEM5a を、欠けの画素数の分位（20・40・50・60・70・80・90・97%）から 8 枚選び、陰影図に欠けを赤く塗って見た。欠けはほぼすべて、川筋・ため池・水路・港の水面の形だった。DEM10b との照合（欠けの画素に DEM10b の値があるか）は、DEM10b が湖や川の水面にも値を持つので、「海でない」ことしか示さない。この陰影図を作ったスクリプトは保存していない（手順の概要のみ）。

## DEM5b・5c で埋まるか

- 標本の母集団は、12 メッシュの欠けのある DEM5a 36,661 枚のうち、親の DEM10b のタイルがキャッシュにあり、欠けの画素の少なくとも 1 つに DEM10b の値がある 36,548 枚（差の 113 枚は、親の DEM10b が 404 か、欠けがすべて DEM10b の NODATA と重なるもの）。
- この母集団を `water.py` の出力の順に並べ、`random.seed(154)` の `random.sample` で 30 枚を選び（座標は下の一覧）、DEM5b・5c を 1 秒に 1 件で要求した（計 60 件、2026-10-07）。
- DEM5b は 200 が 2 枚・404 が 28 枚、DEM5c は 30 枚とも 404 だった。欠けの画素 28,390 のうち、DEM5b で埋まったのは 64（0.23%。欠け 16 画素と 48 画素の 2 枚）、DEM5c で埋まったのは 0 だった。
- DEM5a がある位置に DEM5b もある割合は 2/30（95% 信頼区間でおよそ 1〜22%）。

## 海の位置の余白

12 メッシュでの比較。範囲の外の Z14 のタイルは「無い」と数えたので、飛ばす位置の数は多めに出る。

| 海と見なす条件 | 飛ばす位置 | 落とすデータのある位置 | 全国の要求件数 | 毎秒 40 件 | 毎秒 80 件 |
|---|---|---|---|---|---|
| 親の DEM10b が 404 | 18,119 | 26 | 約 129 万 | 8.9 時間 | 4.5 時間 |
| 親と周りの 1 枚（3×3）がすべて 404 | 15,775 | 0 | 約 139 万 | 9.6 時間 | 4.8 時間 |
| 親と周りの 2 枚（5×5）がすべて 404 | 13,887 | 0 | 約 147 万 | 10.2 時間 | 5.1 時間 |

余白なしで落ちる 26 位置は、羽田沖・東京湾の埋立地や防波堤、千葉の湾岸、茨城の港、渥美の沿岸で、DEM10b に無い新しい埋立地や港湾施設だった。

## 取り方ごとの全国の見込み

Z15 が 1,209,629 枚、Z14 が 304,412 枚（`scripts/prefetch_tiles.py` の `enumerate_jobs` で数えた）に、上の割合を当てた。

| 取り方 | 要求件数 | 毎秒 10 件 | 毎秒 20 件 | 毎秒 40 件 | 毎秒 80 件 |
|---|---|---|---|---|---|
| 4 種別すべて | 3,933,299 | 109 時間 | 55 時間 | 27 時間 | 14 時間 |
| a→b→c を 404 のときだけ | 約 209 万 | 58 時間 | 29 時間 | 15 時間 | 7 時間 |
| 同上＋海の位置（3×3）を飛ばす | 約 139 万 | 39 時間 | 19 時間 | 9.6 時間 | 4.8 時間 |
| 5a に欠けがあれば 5b・5c も取る（採らなかった案） | 約 263〜317 万 | 73〜88 時間 | 36〜44 時間 | 18〜22 時間 | 9〜11 時間 |

## 並列数と毎秒の件数

応答時間は約 0.19 秒（DEM5a の 3 枚、2026-10-07）。並列 8・間隔なしで毎秒約 42 件、並列 12・ワーカーごとに 100ms で約 41 件、並列 8・ワーカーごとに 100ms で約 28 件。国土地理院はアクセスの上限を公開していない（地理院タイル仕様・地理院タイル一覧・コンテンツ利用規約。2026-10-07 に確認）。

## 限界

- 12 メッシュは東海・関東の一部（全国の約 7%）。DEM5a の整備状況と海の割合は地域で違う。
- DEM5b があるかどうかの割合は、標本 30 枚の幅でしか言えない。
- DEM5A の水部が -9999 という記述は二次資料（FIT2022 I-019 の抜粋）によるもので、国土地理院の仕様書の本文は確かめていない。

## 測定の手順

実行は本体ルートで `venv/bin/python3 <スクリプト> <引数>`。再現には測定時点（2026-10-07）と同じローカルキャッシュの状態が要る（キャッシュは取得のたびに変わりうる）。

`measure.py`（キャッシュの DEM5 の NODATA の画素を位置ごとに数える。13 メッシュ）:

```python
import os, sys, json
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from PIL import Image
sys.path.insert(0, "/workspace/scripts")
from prefetch_tiles import enumerate_jobs, tile_path
T = "/data/tiles"
MESHES = [5237,5238,5239,5240,5337,5338,5339,5340,5437,5438,5439,5440,5539]

def nodata_count(path):
    try:
        a = np.asarray(Image.open(path).convert("RGB")).astype(np.uint32)
    except Exception:
        return -1  # unreadable (error body / empty)
    v = (a[...,0] << 16) | (a[...,1] << 8) | a[...,2]
    return int((v == 0x800000).sum())

def per_tile(args):
    x, y = args
    r = {}
    for d in "abc":
        p = tile_path(T, 15, x, y, d)
        r[d] = nodata_count(p) if os.path.exists(p) else None
    return x, y, r

if __name__ == "__main__":
    jobs = enumerate_jobs(set(MESHES), T)
    z15 = [(x, y) for z, x, y, d, p in jobs if z == 15]
    z14 = [(x, y) for z, x, y, d, p in jobs if z == 14]
    with ProcessPoolExecutor(14) as ex:
        res = list(ex.map(per_tile, z15, chunksize=500))
    z14_exist = sum(os.path.exists(tile_path(T, 14, x, y, "b")) for x, y in z14)
    json.dump({"z15": res, "z14_total": len(z14), "z14_exist": z14_exist}, open(sys.argv[1], "w"))
```

`margin.py`（海の位置の余白の比較。12 メッシュ。範囲の外の Z14 は「無い」と数える）:

```python
import json, sys, os
sys.path.insert(0, "/workspace/scripts")
from prefetch_tiles import tile_path, enumerate_jobs
d = json.load(open(sys.argv[1])); T = "/data/tiles"   # sys.argv[1] は measure.py の出力
M12 = [5237,5238,5239,5240,5337,5338,5339,5340,5437,5438,5439,5440]
J = enumerate_jobs(set(M12), T)
keep = {(x, y) for z, x, y, _, _ in J if z == 15}
R = [(x, y, r) for x, y, r in d["z15"] if (x, y) in keep]; N = len(R)
ok = lambda v: v is not None and v >= 0
has = lambda r: any(ok(v) and v < 65536 for v in r.values())
def cost(r): return 1 + (0 if ok(r["a"]) else 1 + (0 if ok(r["b"]) else 1))  # a→b→c を 404 のときだけ
ex = {}
def z14ok(x, y):
    if (x, y) not in ex: ex[(x, y)] = os.path.exists(tile_path(T, 14, x, y, "b"))
    return ex[(x, y)]
Z15, Z14 = 1209629, 304412; base = sum(cost(r) for *_, r in R)
for m in (0, 1, 2):
    skip = [(x, y, r) for x, y, r in R
            if all(not z14ok(x//2+dx, y//2+dy) for dx in range(-m, m+1) for dy in range(-m, m+1))]
    lost = [(x, y) for x, y, r in skip if has(r)]
    v = (base - sum(cost(r) for *_, r in skip)) / N * Z15 + Z14
    print(f"margin {m}: skip {len(skip)}, lost-with-data {len(lost)}, total {v:,.0f}, 40/s {v/40/3600:.1f}h")
```

`water.py`（欠けが水面らしいかの集計と、標本の母集団 36,548 枚の出力）:

```python
import os, sys, json
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from PIL import Image
sys.path.insert(0, "/workspace/scripts")
from prefetch_tiles import tile_path, enumerate_jobs
T="/data/tiles"
def dec(path):
    a=np.asarray(Image.open(path).convert("RGB")).astype(np.int64)
    v=(a[...,0]<<16)|(a[...,1]<<8)|a[...,2]
    nd=v==0x800000
    e=np.where(v>0x800000, v-(1<<24), v)/100.0
    return np.where(nd,np.nan,e)
def f(xy):
    x,y=xy
    a=dec(tile_path(T,15,x,y,"a")); hole=np.isnan(a)
    p14=tile_path(T,14,x//2,y//2,"b")
    if not os.path.exists(p14): return None
    t=dec(p14)[(y%2)*128:(y%2)*128+128,(x%2)*128:(x%2)*128+128].repeat(2,0).repeat(2,1)
    h=hole & ~np.isnan(t)
    if h.sum()==0: return None
    th=t[h]
    # 水面らしさ: DEM10B が穴の中でほぼ平ら（範囲<=1m）か、穴の外の 5a の 5 パーセンタイル以下
    out=a[~hole]
    low=np.nanpercentile(out,5) if out.size else np.nan
    return dict(n=int(h.sum()), rng=float(th.max()-th.min()), med=float(np.median(th)),
                low_frac=float((th<=low+0.5).mean()) if out.size else None,
                tile_med=float(np.nanmedian(a)) if out.size else None)
if __name__=="__main__":
    M12=[5237,5238,5239,5240,5337,5338,5339,5340,5437,5438,5439,5440]
    d=json.load(open(sys.argv[1]))
    keep={(x,y) for z,x,y,_,_ in enumerate_jobs(set(M12),T) if z==15}
    xs=[(x,y) for x,y,r in d["z15"] if (x,y) in keep and r["a"] is not None and 0<r["a"]<65536]
    with ProcessPoolExecutor(14) as ex: out=list(ex.map(f,xs,chunksize=300))
    res=[(xy,o) for xy,o in zip(xs,out) if o]
    json.dump([[xy,o] for xy,o in res],open(sys.argv[2],"w"))
    n=np.array([o["n"] for _,o in res]); rng=np.array([o["rng"] for _,o in res]); lf=np.array([o["low_frac"] if o["low_frac"] is not None else np.nan for _,o in res])
    print("tiles",len(res),"hole px",n.sum())
    for r in (0.5,1,2,5,20): print(f" DEM10B range in hole <= {r}m: tiles {(rng<=r).mean()*100:5.1f}%  px {n[rng<=r].sum()/n.sum()*100:5.1f}%")
    print(f" hole px mostly at/below tile's 5th pct (low_frac>=0.8): tiles {(lf>=0.8).mean()*100:5.1f}%  px {n[lf>=0.8].sum()/n.sum()*100:5.1f}%")
```

`sample.py`（母集団から 30 枚を選び、DEM5b・5c を要求して欠けが埋まる画素を数える）:

```python
import sys, json, random, time, io, configparser
import numpy as np, requests
from PIL import Image
sys.path.insert(0, "/workspace/scripts")
from prefetch_tiles import tile_path, tile_url
T="/data/tiles"; S=sys.argv[2]
cfg=configparser.ConfigParser(); cfg.read("/workspace/params/fetch_config.ini")
ua=f"findsummits/1.0 (mailto:{cfg.get('fetch','user_agent_email',fallback='anonymous')})"
def dec_bytes(b):
    a=np.asarray(Image.open(io.BytesIO(b)).convert("RGB")).astype(np.int64)
    return ((a[...,0]<<16)|(a[...,1]<<8)|a[...,2])==0x800000
d=json.load(open(sys.argv[1])); random.seed(154)
picks=random.sample(d,30)
ses=requests.Session(); rows=[]; nreq=0
for (x,y),o in picks:
    hole=dec_bytes(open(tile_path(T,15,x,y,"a"),"rb").read())
    row={"xy":[x,y],"hole":int(hole.sum())}; rem=hole.copy()
    for dem in "bc":
        time.sleep(1.0); nreq+=1
        r=ses.get(tile_url(15,x,y,dem),headers={"User-Agent":ua},timeout=30)
        row[dem+"_status"]=r.status_code
        if r.status_code==200:
            open(f"{S}/fetched/{dem}_{x}_{y}.png","wb").write(r.content)
            nd=dec_bytes(r.content)
            row[dem+"_fills"]=int((rem & ~nd).sum()); rem=rem & nd
        else:
            row[dem+"_fills"]=0
    row["left"]=int(rem.sum()); rows.append(row); print(row, flush=True)
json.dump(rows,open(f"{S}/sample.json","w"))
H=sum(r["hole"] for r in rows); B=sum(r["b_fills"] for r in rows); C=sum(r["c_fills"] for r in rows)
print(f"requests={nreq} hole_px={H} filled_by_b={B} ({B/H*100:.2f}%) filled_by_c={C} ({C/H*100:.2f}%) left={H-B-C}")
print("tiles with any fill:", sum(1 for r in rows if r["b_fills"]+r["c_fills"]>0))
import collections; print("status b",collections.Counter(r["b_status"] for r in rows),"c",collections.Counter(r["c_status"] for r in rows))
```

標本 30 枚の Z15 の座標（x,y。選ばれた順）: 28963,12875 28915,12832 29048,12837 28978,12883 29021,12857 29099,12858 28917,12947 29100,12794 29060,12885 28918,12861 28994,12832 28929,12995 28972,12862 29175,12802 28884,13008 28882,12849 29171,12832 28995,12807 29105,12792 29093,12819 29026,12945 29102,12889 29093,12929 28923,12897 28862,12978 28897,12795 29039,12937 28966,13001 29102,12833 28858,12923
