// Chromium 系のブラウザ（Chrome・Brave）をヘッドレスで起動し、probe.html を file:// で開いて 9 つの能力を確かめる（#299）。
// Chrome DevTools Protocol を Node.js の組み込みの fetch と WebSocket で使う（npm は使わない）。
// 使い方: node cdp_probe.js <ブラウザのコマンド> <空の作業ディレクトリ>
//   作業ディレクトリの下に、新しいプロファイル（prof/）とダウンロード先（dl/）を作る。空でなければ止まる（前回の結果を取り違えないため）。
//   ポート 0 で起動し、そのプロファイルにブラウザが書く DevToolsActivePort から接続先を読む（ほかのブラウザにつながないため）。
//   ブラウザはプロセスのグループで起動し、終わり・例外・時間切れ（全体 90 秒、1 つの命令 15 秒）・SIGINT・SIGTERM のどれでも
//   グループごと止める（/usr/bin/brave-browser はラッパーで、子への kill が本体に届かない）。SIGTERM で止まらなければ SIGKILL。
// 出力: 能力ごとの値と合否（checks）を 1 行の JSON で標準出力に出す。ホストのパスは出さない。
// 終了コード: 9 つとも期待どおりなら 0、そうでなければ 1、使い方の誤りは 2。
"use strict";
const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");

const [bin, work] = process.argv.slice(2);
if (!bin || !work) {
  console.error("使い方: cdp_probe.js <ブラウザのコマンド> <空の作業ディレクトリ>");
  process.exit(2);
}
if (!fs.existsSync(work) || fs.readdirSync(work).length !== 0) {
  console.error("作業ディレクトリが無いか、空でない");
  process.exit(2);
}
const prof = path.resolve(work, "prof");
const dl = path.resolve(work, "dl");
fs.mkdirSync(prof);
fs.mkdirSync(dl);
const page = pathToFileURL(path.join(__dirname, "probe.html")).href;
const upload = path.join(__dirname, "upload.json");
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const res = { browser: path.basename(bin) };
let finished = false;
let ws = null;

const br = spawn(bin, ["--headless=new", "--no-first-run", "--no-default-browser-check", `--user-data-dir=${prof}`,
  "--remote-debugging-port=0", "about:blank"], { stdio: "ignore", detached: true });
br.on("error", (e) => finish("起動できない: " + e.code));
br.on("exit", (code) => { if (!finished) finish("ブラウザが途中で終わった: " + code); });

function groupAlive() {
  try { process.kill(-br.pid, 0); return true; } catch (e) { return false; }
}
async function stop() {
  if (!br.pid) return;
  try { process.kill(-br.pid, "SIGTERM"); } catch (e) { return; }
  for (let i = 0; i < 20 && groupAlive(); i++) await sleep(100);
  if (groupAlive()) { try { process.kill(-br.pid, "SIGKILL"); } catch (e) { /* もう終わっている */ } }
}

// 起動したプロセスのグループの VmRSS の和（KiB）。/proc/<pid>/stat の 5 つ目の欄がプロセスのグループ。
function groupRssKiB(pgid) {
  let sum = 0;
  for (const d of fs.readdirSync("/proc")) {
    if (!/^[0-9]+$/.test(d)) continue;
    try {
      const stat = fs.readFileSync(`/proc/${d}/stat`, "utf8");
      const fields = stat.slice(stat.lastIndexOf(")") + 2).split(" ");
      if (Number(fields[2]) !== pgid) continue;
      const m = /VmRSS:\s+([0-9]+) kB/.exec(fs.readFileSync(`/proc/${d}/status`, "utf8"));
      if (m) sum += Number(m[1]);
    } catch (e) { /* 途中で終わったプロセスは数えない */ }
  }
  return sum;
}

function checks() {
  const n = res.net || {};
  const m = res.measure || {};
  const mem = res.memory || {};
  const p = res.pointer || {};
  return {
    "1_file_url": res.file_url === true,
    "2_network": !!n.ok && n.ok.status === 200 && n.ok.body === "hello" && !!n.fail && n.fail.err === "TypeError" && (res.net_seen || []).length === 2,
    "3_canvas": JSON.stringify(res.pixel) === "[255,0,0,255]",
    "4_file_input": res.file === '{"in":"put"}\n',
    "5_download": JSON.stringify(res.download) === JSON.stringify([["probe-dl.json", '{"x":1}']]),
    "6_storage_event": !!res.storage_event && res.storage_event.key === "k" && res.storage_event.newValue === "v2",
    "7_frame_interval": m.frames >= 1 && Number.isFinite(m.max_ms) && m.max_ms > 0,
    "8_memory": mem.js_heap_used > 0 && mem.group_rss_kib > 0,
    "9_input": p.down === 1 && p.move >= 2 && p.up === 1,
  };
}

async function finish(err) {
  if (finished) return;
  finished = true;
  if (err) res.error = err;
  res.checks = checks();
  console.log(JSON.stringify(res));
  try { if (ws) ws.close(); } catch (e) { /* 閉じられなくてよい */ }
  await stop();
  process.exit(!res.error && Object.values(res.checks).every(Boolean) ? 0 : 1);
}
setTimeout(() => finish("時間切れ（90 秒）"), 90000);
process.on("SIGINT", () => finish("SIGINT"));
process.on("SIGTERM", () => finish("SIGTERM"));

async function main() {
  let port = null;
  let wsPath = null;
  for (let i = 0; i < 150 && !port; i++) {
    try {
      const lines = fs.readFileSync(path.join(prof, "DevToolsActivePort"), "utf8").split("\n");
      if (lines[0] && lines[1]) { port = lines[0].trim(); wsPath = lines[1].trim(); }
    } catch (e) { await sleep(200); }
  }
  if (!port) throw new Error("DevToolsActivePort が書かれない");
  res.version = (await (await fetch(`http://127.0.0.1:${port}/json/version`)).json()).Browser;
  ws = new WebSocket(`ws://127.0.0.1:${port}${wsPath}`);
  await new Promise((r, j) => { ws.onopen = r; ws.onerror = () => j(new Error("WebSocket に繋がらない")); });
  let id = 0;
  const pend = new Map();
  const handlers = [];
  ws.onmessage = (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && pend.has(m.id)) { pend.get(m.id).resolve(m); pend.delete(m.id); } else handlers.forEach((h) => h(m));
  };
  ws.onclose = () => { for (const p of pend.values()) p.reject(new Error("WebSocket が切れた")); pend.clear(); };
  const send = (method, params = {}, sessionId) => new Promise((resolve, reject) => {
    const n = ++id;
    const t = setTimeout(() => { pend.delete(n); reject(new Error("応答が無い: " + method)); }, 15000);
    pend.set(n, { resolve: (m) => { clearTimeout(t); resolve(m); }, reject: (e) => { clearTimeout(t); reject(e); } });
    ws.send(JSON.stringify({ id: n, method, params, sessionId }));
  });
  const waitEvent = (method, sessionId) => new Promise((r) => {
    const h = (m) => { if (m.method === method && m.sessionId === sessionId) { handlers.splice(handlers.indexOf(h), 1); r(m); } };
    handlers.push(h);
  });
  const open = async () => {
    const t = await send("Target.createTarget", { url: "about:blank" });
    const a = await send("Target.attachToTarget", { targetId: t.result.targetId, flatten: true });
    return a.result.sessionId;
  };
  const navigate = async (sid) => {
    await send("Page.enable", {}, sid);
    const loaded = waitEvent("Page.loadEventFired", sid);
    await send("Page.navigate", { url: page }, sid);
    await loaded;
  };
  const ev = async (sid, expr) => {
    const r = await send("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true }, sid);
    if (r.result.exceptionDetails) throw new Error("Runtime.evaluate: " + expr);
    return r.result.result.value;
  };

  const s1 = await open();
  await send("Browser.setDownloadBehavior", { behavior: "allow", downloadPath: dl });
  // 2. 通信の記録と、応答・失敗の注入
  const seen = [];
  await send("Fetch.enable", { patterns: [{ urlPattern: "https://probe.invalid/*" }] }, s1);
  handlers.push(async (m) => {
    if (m.method !== "Fetch.requestPaused") return;
    seen.push(m.params.request.url);
    if (m.params.request.url.endsWith("ok.txt")) {
      await send("Fetch.fulfillRequest", { requestId: m.params.requestId, responseCode: 200,
        responseHeaders: [{ name: "Access-Control-Allow-Origin", value: "*" }], body: Buffer.from("hello").toString("base64") }, m.sessionId);
    } else {
      await send("Fetch.failRequest", { requestId: m.params.requestId, errorReason: "Failed" }, m.sessionId);
    }
  });
  await navigate(s1);
  // 1. file:// で開く
  res.file_url = String(await ev(s1, "location.href")).startsWith("file://");
  res.net = await ev(s1, "net()");
  res.net_seen = seen.slice();
  // 3. Canvas の画素
  res.pixel = await ev(s1, "pixel()");
  // 4. ファイル選択
  await send("DOM.enable", {}, s1);
  const doc = await send("DOM.getDocument", {}, s1);
  const q = await send("DOM.querySelector", { nodeId: doc.result.root.nodeId, selector: "#f" }, s1);
  await send("DOM.setFileInputFiles", { nodeId: q.result.nodeId, files: [upload] }, s1);
  await sleep(300);
  res.file = await ev(s1, "R.file");
  // 5. ダウンロード
  await ev(s1, "document.getElementById('dl').click()");
  await sleep(1000);
  res.download = fs.readdirSync(dl).map((f) => [f, fs.readFileSync(path.join(dl, f), "utf8")]);
  // 7. フレーム間隔（ページの中で測った、操作の無いときの値を読む）
  res.measure = await ev(s1, "measure()");
  // 8. メモリの値（JS ヒープと、プロセスのグループの RSS の和。補助の値）
  await send("Performance.enable", {}, s1);
  const metrics = (await send("Performance.getMetrics", {}, s1)).result.metrics;
  const heap = metrics.find((x) => x.name === "JSHeapUsedSize");
  res.memory = { js_heap_used: heap ? heap.value : null, group_rss_kib: groupRssKiB(br.pid) };
  // 9. 実際の入力（押す・2 回動かす・離す）
  const c = await ev(s1, "padCenter()");
  await send("Input.dispatchMouseEvent", { type: "mouseMoved", x: c.x, y: c.y }, s1);
  await send("Input.dispatchMouseEvent", { type: "mousePressed", x: c.x, y: c.y, button: "left", buttons: 1, clickCount: 1 }, s1);
  await send("Input.dispatchMouseEvent", { type: "mouseMoved", x: c.x + 10, y: c.y, button: "left", buttons: 1 }, s1);
  await send("Input.dispatchMouseEvent", { type: "mouseMoved", x: c.x + 20, y: c.y, button: "left", buttons: 1 }, s1);
  await send("Input.dispatchMouseEvent", { type: "mouseReleased", x: c.x + 20, y: c.y, button: "left", buttons: 0, clickCount: 1 }, s1);
  await sleep(200);
  res.pointer = await ev(s1, "R.pointer");
  // 6. 2 つのタブの localStorage と storage イベント
  const s2 = await open();
  await navigate(s2);
  await ev(s2, "localStorage.setItem('k', 'v2')");
  await sleep(500);
  res.storage_event = await ev(s1, "R.storage");
}

main().then(() => finish(), (e) => finish(String(e && e.message || e)));
