// #197 の書き込みの見本を、候補のライブラリで作る。
// 使い方: リポジトリのルートで node docs/decisions/research/library-file-scheme-probe/write_check.js <出力先>
// ライブラリは fetch_libs.sh が build/probe-libs/ に取ったものを読む（npm は使わない）。
// 出力: <出力先>/<候補>/application.xlsx・application-props.xlsx・list.xlsx と、
//       <出力先>/zip-raw.zip（時刻を補正しない）・zip-fixed.zip（時刻を補正する）。
// 読めない・作れない候補は <出力先>/<候補>/error.txt に理由を書く。
"use strict";

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const LIBS = path.resolve("build/probe-libs");
const expected = JSON.parse(fs.readFileSync(path.join(__dirname, "expected.json"), "utf8"));
const out = process.argv[2];
if (!out) {
  console.error("使い方: write_check.js <出力先>");
  process.exit(2);
}
fs.mkdirSync(out, { recursive: true });

function load(file, globalName) {
  // UMD を require で読み、だめなら vm の文脈でグローバルを取る
  try {
    const mod = require(path.join(LIBS, file));
    if (mod && Object.keys(mod).length) return mod;
  } catch (e) {
    // 続けて vm で試す
  }
  const ctx = { console, setTimeout, clearTimeout, setImmediate, Promise, Uint8Array, ArrayBuffer, TextEncoder, TextDecoder };
  ctx.window = ctx;
  ctx.self = ctx;
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(LIBS, file), "utf8"), ctx);
  if (!ctx[globalName]) throw new Error(`${file} から ${globalName} を取れない`);
  return ctx[globalName];
}

const created = new Date(expected.props_created);
const cellsOf = (spec) => Object.entries(spec.cells).filter(([, [, kind]]) => kind !== null);

// --- SheetJS 系（SheetJS CE と xlsx-js-style）の組み立て ---
function sheetjsSheet(XLSX, spec, opts) {
  const ws = {};
  for (const [ref, [value, kind]] of cellsOf(spec)) {
    const cell = { t: kind, v: value };
    if (spec.formats && spec.formats[ref]) cell.z = spec.formats[ref];
    if (opts.wrap && ref === spec.wrap) cell.s = { alignment: { wrapText: true } };
    ws[ref] = cell;
  }
  const refs = Object.keys(spec.cells).map((r) => XLSX.utils.decode_cell(r));
  const maxR = Math.max(...refs.map((c) => c.r));
  const maxC = Math.max(...refs.map((c) => c.c), 9);
  ws["!ref"] = XLSX.utils.encode_range({ s: { r: 0, c: 0 }, e: { r: maxR, c: maxC } });
  if (spec.merges) ws["!merges"] = spec.merges.map((m) => XLSX.utils.decode_range(m));
  return ws;
}

function sheetjsBook(XLSX, key, opts) {
  const wb = XLSX.utils.book_new();
  const spec = expected[key];
  XLSX.utils.book_append_sheet(wb, sheetjsSheet(XLSX, spec, opts), spec.sheets[0]);
  if (spec.second_a1) {
    XLSX.utils.book_append_sheet(wb, { A1: { t: "s", v: spec.second_a1 }, "!ref": "A1" }, spec.sheets[1]);
  }
  if (opts.props) wb.Props = { CreatedDate: created };
  return XLSX.write(wb, { type: "buffer", bookType: "xlsx", compression: true, cellStyles: !!opts.wrap });
}

// SheetJS で書いた XLSX の 1 枚目に、JSZip で固定の pane を書き足す（候補 b）
async function addPane(JSZip, buf) {
  const zip = await JSZip.loadAsync(buf);
  const name = "xl/worksheets/sheet1.xml";
  let xml = await zip.file(name).async("string");
  const pane = '<pane xSplit="0" ySplit="5" topLeftCell="A6" activePane="bottomLeft" state="frozen"/>';
  if (/<sheetView([^>]*)\/>/.test(xml)) {
    xml = xml.replace(/<sheetView([^>]*)\/>/, `<sheetView$1>${pane}</sheetView>`);
  } else if (/<sheetView([^>]*)>/.test(xml)) {
    xml = xml.replace(/<sheetView([^>]*)>/, `<sheetView$1>${pane}`);
  } else {
    throw new Error("sheetView が無い");
  }
  const date = zip.file(name).date;
  // createFolders: false にしないと、JSZip が xl/ などのフォルダのエントリを今の時刻で足し、決定性が崩れる
  zip.file(name, xml, { date, createFolders: false });
  return zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" });
}

// --- ExcelJS の組み立て ---
async function exceljsBook(ExcelJS, key, opts) {
  const spec = expected[key];
  const wb = new ExcelJS.Workbook();
  if (opts.props) {
    wb.created = created;
    wb.modified = created;
  }
  const ws = wb.addWorksheet(spec.sheets[0]);
  for (const [ref, [value]] of cellsOf(spec)) {
    const cell = ws.getCell(ref);
    cell.value = value;
    if (spec.formats && spec.formats[ref]) cell.numFmt = spec.formats[ref];
  }
  if (spec.merges) for (const m of spec.merges) ws.mergeCells(m);
  if (spec.wrap) ws.getCell(spec.wrap).alignment = { wrapText: true };
  if (spec.freeze) ws.views = [{ state: "frozen", xSplit: 0, ySplit: 5, topLeftCell: "A6" }];
  if (spec.second_a1) wb.addWorksheet(spec.sheets[1]).getCell("A1").value = spec.second_a1;
  return Buffer.from(await wb.xlsx.writeBuffer());
}

async function candidate(name, make) {
  const dir = path.join(out, name);
  fs.mkdirSync(dir, { recursive: true });
  try {
    fs.writeFileSync(path.join(dir, "application.xlsx"), await make("application", {}));
    fs.writeFileSync(path.join(dir, "application-props.xlsx"), await make("application", { props: true }));
    fs.writeFileSync(path.join(dir, "list.xlsx"), await make("list", {}));
  } catch (e) {
    fs.writeFileSync(path.join(dir, "error.txt"), `${e && e.stack ? e.stack : e}\n`);
  }
}

async function main() {
  const JSZip = load("jszip.min.js", "JSZip");

  let XLSX = null;
  try {
    XLSX = load("xlsx.full.min.js", "XLSX");
  } catch (e) {
    fs.mkdirSync(path.join(out, "a-sheetjs"), { recursive: true });
    fs.writeFileSync(path.join(out, "a-sheetjs", "error.txt"), `${e.stack}\n`);
  }
  if (XLSX) {
    await candidate("a-sheetjs", (key, o) => sheetjsBook(XLSX, key, { ...o, wrap: true }));
    await candidate("b-sheetjs-pane", async (key, o) => {
      const buf = sheetjsBook(XLSX, key, { ...o, wrap: true });
      return key === "application" ? addPane(JSZip, buf) : buf;
    });
  }
  try {
    const ExcelJS = load("exceljs.min.js", "ExcelJS");
    await candidate("c-exceljs", (key, o) => exceljsBook(ExcelJS, key, o));
  } catch (e) {
    fs.mkdirSync(path.join(out, "c-exceljs"), { recursive: true });
    fs.writeFileSync(path.join(out, "c-exceljs", "error.txt"), `${e.stack}\n`);
  }
  try {
    const XS = load("xlsx-js-style.bundle.js", "XLSX");
    await candidate("d-xlsx-js-style", (key, o) => sheetjsBook(XS, key, { ...o, wrap: true }));
  } catch (e) {
    fs.mkdirSync(path.join(out, "d-xlsx-js-style"), { recursive: true });
    fs.writeFileSync(path.join(out, "d-xlsx-js-style", "error.txt"), `${e.stack}\n`);
  }

  // ZIP: 現地時刻のコンストラクタで作った時刻を、補正なしと補正ありで書く（DEC124）
  const [y, mo, d, h, mi, s] = expected.zip.local_time;
  const t = new Date(y, mo, d, h, mi, s);
  for (const [file, date] of [["zip-raw.zip", t], ["zip-fixed.zip", new Date(t.getTime() - t.getTimezoneOffset() * 60000)]]) {
    const zip = new JSZip();
    zip.file("a.txt", "a", { date });
    zip.file("b.geojson", '{"type":"FeatureCollection","features":[]}', { date });
    fs.writeFileSync(path.join(out, file), await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
