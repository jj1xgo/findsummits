// #197 の確かめのページの処理。モジュールを使わない ES2020 の普通の script（DEC130）。
"use strict";

(function () {
  var GSI = "https://cyberjapandata.gsi.go.jp/xyz/";
  var LAND_DEM = ["dem_png/10/909/403.png", "dem5a_png/15/29105/12903.png", "dem1a_png/17/116421/51613.png"];
  var LAND_CP = "cp/12/3637/1612.geojson";
  var EMPTY = ["dem_png/10/930/420.png", "dem5a_png/15/29764/13566.png", "dem1a_png/17/119056/54266.png", "cp/12/3720/1680.geojson"];
  var JSZIP_URL = "https://cdn.jsdelivr.net/npm/jszip@3.10.2/dist/jszip.min.js";
  var JSZIP_SRI = "sha384-DdGlNq+wVXAn83gXqwyeFHB7iyXy6L0rLrNzgDmhKWPjiJLg9vj6qosYmZmkMfQ+";
  // 陰性の対照: Base64 の 11 文字目の X を Y に替えた（長さは同じ）
  var JSZIP_BAD = "sha384-DdGlNq+wVYAn83gXqwyeFHB7iyXy6L0rLrNzgDmhKWPjiJLg9vj6qosYmZmkMfQ+";
  var XLSX_URL = "https://cdn.sheetjs.com/xlsx-0.20.3/package/dist/xlsx.full.min.js";
  var XLSX_SRI = "sha384-EnyY0/GSHQGSxSgMwaIPzSESbqoOLSexfnSMN2AP+39Ckmn92stwABZynq1JyzdT";
  var EXCELJS_URL = "https://cdn.jsdelivr.net/npm/exceljs@4.4.0/dist/exceljs.min.js";
  var EXCELJS_SRI = "sha384-Pqp51FUN2/qzfxZxBCtF0stpc9ONI6MYZpVqmo8m20SoaQCzf+arZvACkLkirlPz";
  var KEY_NOW = "findsummits:probe-now";
  var KEY_PERSIST = "findsummits:probe-persist";
  var KEY_A = "findsummits:probe-a";

  var results = [];

  function add(id, what, status, detail) {
    results.push({ id: id, what: what, status: status, detail: detail || "" });
    render();  // 途中で止まっても、そこまでの結果が見えるように
  }

  function render() {
    var tbody = document.querySelector("#table tbody");
    tbody.textContent = "";
    results.forEach(function (r) {
      var tr = document.createElement("tr");
      [r.id, r.what, r.status, r.detail].forEach(function (text, i) {
        var td = document.createElement("td");
        td.textContent = text;
        if (i === 2) td.className = r.status === "通った" ? "ok" : r.status === "通らない" ? "ng" : "na";
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
    var out = {
      userAgent: navigator.userAgent,
      brave: typeof navigator.brave === "object",
      protocol: location.protocol,
      time: new Date().toString(),
      results: results
    };
    var ta = document.getElementById("json");
    ta.value = JSON.stringify(out, null, 1);
    ta.textContent = ta.value;  // ヘッドレスのブラウザの DOM の書き出しにも出すため
  }

  function withTimeout(promise, ms) {
    return Promise.race([promise, new Promise(function (resolve) { setTimeout(function () { resolve("timeout"); }, ms); })]);
  }

  function loadScript(url, integrity) {
    return withTimeout(new Promise(function (resolve) {
      var s = document.createElement("script");
      s.src = url;
      s.integrity = integrity;
      s.crossOrigin = "anonymous";
      s.onload = function () { resolve("load"); };
      s.onerror = function () { resolve("error"); };
      document.head.appendChild(s);
    }), 30000);
  }

  function storage() {
    try {
      return window.localStorage;
    } catch (e) {
      return null;
    }
  }

  async function checkFetchLocal() {
    try {
      var r = await fetch("probe_data.js");
      var text = await r.text();
      add("P2", "fetch でデータファイルを読む（file:// では通らない見込み）", "通った", "status " + r.status + "、" + text.length + " 文字");
    } catch (e) {
      add("P2", "fetch でデータファイルを読む（file:// では通らない見込み）", "通らない", String(e));
    }
  }

  function checkXhrLocal() {
    return withTimeout(new Promise(function (resolve) {
      var what = "XMLHttpRequest でデータファイルを読む";
      try {
        var x = new XMLHttpRequest();
        x.open("GET", "probe_data.js");
        x.onload = function () {
          var len = (x.responseText || "").length;
          add("P3", what, len > 0 ? "通った" : "通らない", "status " + x.status + "、" + len + " 文字");
          resolve();
        };
        x.onerror = function () { add("P3", what, "通らない", "error イベント"); resolve(); };
        x.send();
      } catch (e) {
        add("P3", what, "通らない", String(e));
        resolve();
      }
    }), 10000).then(function (v) { if (v === "timeout") add("P3", "XMLHttpRequest でデータファイルを読む", "判定不能", "10 秒で応答なし"); });
  }

  async function checkSri() {
    var bad = await loadScript(JSZIP_URL, JSZIP_BAD);
    var badGlobal = typeof window.JSZip;
    var good = await loadScript(JSZIP_URL, JSZIP_SRI);
    var goodOk = good === "load" && typeof window.JSZip === "function";
    if (!goodOk) {
      add("P8", "陰性の対照: 違えたハッシュの JSZip が読まれない", "判定不能", "正しいハッシュでも読めなかった（" + good + "）");
    } else {
      add("P8", "陰性の対照: 違えたハッシュの JSZip が読まれない", bad === "error" && badGlobal === "undefined" ? "通った" : "通らない",
        "違えたハッシュ: " + bad + "、そのときの JSZip: " + badGlobal);
    }
    add("P6", "JSZip を SRI 付きで足して読む", goodOk ? "通った" : "通らない", good + "、JSZip: " + typeof window.JSZip);
    var x = await loadScript(XLSX_URL, XLSX_SRI);
    var e = await loadScript(EXCELJS_URL, EXCELJS_SRI);
    add("P7", "XLSX の候補を SRI 付きで足して読む", x === "load" && window.XLSX && e === "load" && window.ExcelJS ? "通った" : "通らない",
      "SheetJS: " + x + "（XLSX " + typeof window.XLSX + "）、ExcelJS: " + e + "（ExcelJS " + typeof window.ExcelJS + "）");
  }

  function checkStorage() {
    var ls = storage();
    if (!ls) {
      add("P9a", "localStorage に書いて読み返す", "通らない", "localStorage を取れない");
      add("P9b", "閉じる前に保存した値（上書きせずに読む）", "通らない", "localStorage を取れない");
      add("P10", "a/index.html が書いた値が見えるか", "判定不能", "localStorage を取れない");
      return;
    }
    try {
      var v = "now " + Date.now();
      ls.setItem(KEY_NOW, v);
      add("P9a", "localStorage に書いて読み返す", ls.getItem(KEY_NOW) === v ? "通った" : "通らない", "");
    } catch (e) {
      add("P9a", "localStorage に書いて読み返す", "通らない", String(e));
    }
    try {
      var p = ls.getItem(KEY_PERSIST);
      add("P9b", "閉じる前に保存した値（上書きせずに読む）", p ? "通った" : "通らない", p ? "値: " + p : "値が無い");
    } catch (e) {
      add("P9b", "閉じる前に保存した値（上書きせずに読む）", "通らない", String(e));
    }
    try {
      var a = ls.getItem(KEY_A);
      add("P10", "a/index.html が書いた値が見えるか（良し悪しは判定しない）", "記録", a ? "見えた: " + a : "見えない");
    } catch (e) {
      add("P10", "a/index.html が書いた値が見えるか（良し悪しは判定しない）", "記録", String(e));
    }
  }

  // 真ん中の画素と、タイル全体の画素の値の合計。指紋対策で読み出しに雑音が入るブラウザでは、合計がほかのブラウザと違う
  function pixelSummary(ctx, w, h) {
    var all = ctx.getImageData(0, 0, w, h).data;
    var sum = 0;
    for (var i = 0; i < all.length; i++) sum += all[i];
    return "真ん中 " + Array.from(ctx.getImageData(128, 128, 1, 1).data).join(",") + "、合計 " + sum;
  }

  async function pixelFromBlob(blob) {
    var bmp = await createImageBitmap(blob);
    var c = document.createElement("canvas");
    c.width = bmp.width;
    c.height = bmp.height;
    var ctx = c.getContext("2d");
    ctx.drawImage(bmp, 0, 0);
    return pixelSummary(ctx, bmp.width, bmp.height);
  }

  function pixelFromImg(url) {
    return withTimeout(new Promise(function (resolve) {
      var img = new Image();
      img.crossOrigin = "anonymous";
      img.onload = function () {
        try {
          var c = document.createElement("canvas");
          c.width = img.naturalWidth;
          c.height = img.naturalHeight;
          var ctx = c.getContext("2d");
          ctx.drawImage(img, 0, 0);
          resolve({ ok: true, px: pixelSummary(ctx, img.naturalWidth, img.naturalHeight) });
        } catch (e) {
          resolve({ ok: false, px: String(e) });
        }
      };
      img.onerror = function () { resolve({ ok: false, px: "error イベント" }); };
      img.src = url + "?img=1";
    }), 30000);
  }

  async function checkTiles() {
    for (var i = 0; i < LAND_DEM.length; i++) {
      var url = GSI + LAND_DEM[i];
      try {
        var r = await fetch(url);
        if (!r.ok) {
          add("P11", "fetch でタイルの画素を読む " + LAND_DEM[i], "通らない", "status " + r.status);
        } else {
          add("P11", "fetch でタイルの画素を読む " + LAND_DEM[i], "通った", "画素 " + await pixelFromBlob(await r.blob()));
        }
      } catch (e) {
        add("P11", "fetch でタイルの画素を読む " + LAND_DEM[i], "通らない", String(e));
      }
      var res = await pixelFromImg(url);
      if (res === "timeout") res = { ok: false, px: "30 秒で応答なし" };
      add("P12", "img（crossOrigin）でタイルの画素を読む " + LAND_DEM[i], res.ok ? "通った" : "通らない", res.px);
    }
    try {
      var rc = await fetch(GSI + LAND_CP);
      var j = await rc.json();
      add("P13", "fetch で基準点のタイルを読む", rc.ok && Array.isArray(j.features) ? "通った" : "通らない", "status " + rc.status + "、" + (j.features ? j.features.length : "?") + " 点");
    } catch (e) {
      add("P13", "fetch で基準点のタイルを読む", "通らない", String(e));
    }
    for (var k = 0; k < EMPTY.length; k++) {
      try {
        var re = await fetch(GSI + EMPTY[k]);
        add("P14", "データの無い範囲が 404 か " + EMPTY[k], re.status === 404 ? "通った" : "通らない", "status " + re.status);
      } catch (e) {
        add("P14", "データの無い範囲が 404 か " + EMPTY[k], "通らない", String(e));
      }
    }
  }

  async function run() {
    results = [];
    add("P1", "データファイルを普通の script で読む", window.FINDSUMMITS_DATA && window.FINDSUMMITS_DATA.probe === 1 ? "通った" : "通らない", "");
    await checkFetchLocal();
    await checkXhrLocal();
    add("P4", "モジュールの script が実行される（file:// では通らない見込み）", window.FINDSUMMITS_PROBE_MODULE === 1 ? "通った" : "通らない", "");
    var css = document.getElementById("leaflet-css");
    add("P5", "Leaflet の CSS と JavaScript を SRI 付きで読む", css && css.sheet && typeof window.L === "object" ? "通った" : "通らない",
      "CSS の sheet: " + (css && css.sheet ? "ある" : "無い") + "、L: " + typeof window.L);
    render();
    if (typeof window.JSZip === "undefined") await checkSri();
    else add("P8", "陰性の対照", "判定不能", "2 回目の「確かめる」なので読み直さない（ページを開き直す）");
    checkStorage();
    render();
    await checkTiles();
    render();
  }

  // --- P15: 見本を作って落とす（write_check.js と同じ見本） ---
  function sheetjsSheet(spec) {
    var XLSX = window.XLSX;
    var ws = {};
    var refs = [];
    Object.keys(spec.cells).forEach(function (ref) {
      refs.push(XLSX.utils.decode_cell(ref));
      var vk = spec.cells[ref];
      if (vk[1] === null) return;
      var cell = { t: vk[1], v: vk[0] };
      if (spec.formats && spec.formats[ref]) cell.z = spec.formats[ref];
      ws[ref] = cell;
    });
    var maxR = Math.max.apply(null, refs.map(function (c) { return c.r; }));
    var maxC = Math.max.apply(null, refs.map(function (c) { return c.c; }).concat([9]));
    ws["!ref"] = XLSX.utils.encode_range({ s: { r: 0, c: 0 }, e: { r: maxR, c: maxC } });
    if (spec.merges) ws["!merges"] = spec.merges.map(function (m) { return XLSX.utils.decode_range(m); });
    return ws;
  }

  function sheetjsBook(key) {
    var XLSX = window.XLSX;
    var spec = window.FINDSUMMITS_PROBE_EXPECTED[key];
    var wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, sheetjsSheet(spec), spec.sheets[0]);
    if (spec.second_a1) XLSX.utils.book_append_sheet(wb, { A1: { t: "s", v: spec.second_a1 }, "!ref": "A1" }, spec.sheets[1]);
    return XLSX.write(wb, { type: "array", bookType: "xlsx", compression: true });
  }

  async function addPane(buf) {
    var zip = await window.JSZip.loadAsync(buf);
    var name = "xl/worksheets/sheet1.xml";
    var xml = await zip.file(name).async("string");
    var pane = '<pane xSplit="0" ySplit="5" topLeftCell="A6" activePane="bottomLeft" state="frozen"/>';
    xml = /<sheetView([^>]*)\/>/.test(xml)
      ? xml.replace(/<sheetView([^>]*)\/>/, "<sheetView$1>" + pane + "</sheetView>")
      : xml.replace(/<sheetView([^>]*)>/, "<sheetView$1>" + pane);
    zip.file(name, xml, { date: zip.file(name).date, createFolders: false });
    return zip.generateAsync({ type: "uint8array", compression: "DEFLATE" });
  }

  async function exceljsBook(key) {
    var spec = window.FINDSUMMITS_PROBE_EXPECTED[key];
    var wb = new window.ExcelJS.Workbook();
    var ws = wb.addWorksheet(spec.sheets[0]);
    Object.keys(spec.cells).forEach(function (ref) {
      var vk = spec.cells[ref];
      if (vk[1] === null) return;
      var cell = ws.getCell(ref);
      cell.value = vk[0];
      if (spec.formats && spec.formats[ref]) cell.numFmt = spec.formats[ref];
    });
    if (spec.merges) spec.merges.forEach(function (m) { ws.mergeCells(m); });
    if (spec.wrap) ws.getCell(spec.wrap).alignment = { wrapText: true };
    if (spec.freeze) ws.views = [{ state: "frozen", xSplit: 0, ySplit: 5, topLeftCell: "A6" }];
    if (spec.second_a1) wb.addWorksheet(spec.sheets[1]).getCell("A1").value = spec.second_a1;
    return new Uint8Array(await wb.xlsx.writeBuffer());
  }

  async function samples() {
    try {
      if (!window.JSZip || !window.XLSX || !window.ExcelJS) throw new Error("先に「確かめる」でライブラリを読んでください");
      var lt = window.FINDSUMMITS_PROBE_EXPECTED.zip.local_time;
      var t = new Date(lt[0], lt[1], lt[2], lt[3], lt[4], lt[5]);
      var date = new Date(t.getTime() - t.getTimezoneOffset() * 60000);
      var zip = new window.JSZip();
      zip.file("b-sheetjs-pane/application.xlsx", await addPane(sheetjsBook("application")), { date: date, createFolders: false });
      zip.file("b-sheetjs-pane/list.xlsx", sheetjsBook("list"), { date: date, createFolders: false });
      zip.file("c-exceljs/application.xlsx", await exceljsBook("application"), { date: date, createFolders: false });
      zip.file("c-exceljs/list.xlsx", await exceljsBook("list"), { date: date, createFolders: false });
      var bytes = await zip.generateAsync({ type: "uint8array", compression: "DEFLATE" });
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([bytes], { type: "application/zip" }));
      a.download = "probe-samples.zip";
      document.body.appendChild(a);
      a.click();
      a.remove();
      add("P15", "見本を作って落とす（落ちたかは目で見る）", "記録", "probe-samples.zip " + bytes.length + " バイトを作った");
    } catch (e) {
      add("P15", "見本を作って落とす", "通らない", String(e));
    }
    render();
  }

  function save() {
    var ls = storage();
    var el = document.getElementById("saved");
    try {
      var v = "保存した時刻 " + new Date().toString();
      ls.setItem(KEY_PERSIST, v);
      el.textContent = v;
    } catch (e) {
      el.textContent = "保存できない: " + e;
    }
  }

  document.getElementById("run").addEventListener("click", function () { run(); });
  // URL の末尾が #auto なら開いてすぐ走らせる（ヘッドレスのブラウザで確かめるため）
  if (location.hash === "#auto") run().then(function () { document.body.setAttribute("data-done", "1"); });
  document.getElementById("save").addEventListener("click", save);
  document.getElementById("samples").addEventListener("click", function () { samples(); });
  document.getElementById("copy").addEventListener("click", function () {
    var ta = document.getElementById("json");
    ta.select();
    try {
      navigator.clipboard.writeText(ta.value).catch(function () { document.execCommand("copy"); });
    } catch (e) {
      document.execCommand("copy");
    }
  });
})();
