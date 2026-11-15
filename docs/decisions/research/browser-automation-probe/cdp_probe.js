// Chromium 系のブラウザ（Chrome・Brave）をヘッドレスで起動し、probe.html を file:// で開いて 9 つの能力を確かめる（#299）。
// Chrome DevTools Protocol を Node.js の組み込みの fetch と WebSocket で使う（npm は使わない）。
// 使い方: node cdp_probe.js <ブラウザのコマンド> <空の作業ディレクトリ>
//   作業ディレクトリの下に、新しいプロファイル（prof/）とダウンロード先（dl/）を作る。空でなければ止まる（前回の結果を取り違えないため）。
//   ブラウザはプロセスのグループで起動し、終わりにグループごと止める（/usr/bin/brave-browser はラッパーで、子への kill が本体に届かない）。
// 出力: 能力ごとの結果を 1 行の JSON で標準出力に出す。ホストのパスは出さない。
"use strict";
const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");

const [bin, work] = process.argv.slice(2);
if (!bin || !work) {
  console.error("使い方: cdp_probe.js <ブラウザのコマンド> <空の作業ディレクトリ>");
  process.exit(2);
}
if (!fs.existsSync(work) || fs.readdirSync(work).length !== 0) {
  console.error("作業ディレクトリが無いか、空でない: " + work);
  process.exit(2);
}
const prof = path.join(work, "prof");
const dl = path.join(work, "dl");
fs.mkdirSync(prof);
fs.mkdirSync(dl);
const page = "file://" + path.join(__dirname, "probe.html");
const upload = path.join(__dirname, "upload.json");
const port = 9300 + Math.floor(Math.random() * 500);
const br = spawn(bin, ["--headless=new", "--no-first-run", "--no-default-browser-check", `--user-data-dir=${path.resolve(prof)}`,
  `--remote-debugging-port=${port}`, "about:blank"], { stdio: "ignore", detached: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const res = { browser: bin };

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

async function main() {
  let ver = null;
  for (let i = 0; i < 100 && !ver; i++) {
    try { ver = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json(); } catch (e) { await sleep(200); }
  }
  if (!ver) throw new Error("ブラウザの DevTools に繋がらない");
  res.version = ver.Browser;
  const ws = new WebSocket(ver.webSocketDebuggerUrl);
  await new Promise((r) => { ws.onopen = r; });
  let id = 0;
  const pend = new Map();
  const handlers = [];
  ws.onmessage = (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); } else handlers.forEach((h) => h(m));
  };
  const send = (method, params = {}, sessionId) => new Promise((r) => {
    const n = ++id; pend.set(n, r); ws.send(JSON.stringify({ id: n, method, params, sessionId }));
  });
  const open = async () => {
    const t = await send("Target.createTarget", { url: "about:blank" });
    const a = await send("Target.attachToTarget", { targetId: t.result.targetId, flatten: true });
    return a.result.sessionId;
  };
  const ev = async (sid, expr) => (await send("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true }, sid)).result.result.value;

  const s1 = await open();
  await send("Browser.setDownloadBehavior", { behavior: "allow", downloadPath: path.resolve(dl) });
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
  await send("Page.enable", {}, s1);
  await send("Page.navigate", { url: page }, s1);
  await sleep(800);
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
  // 7. 応答時間とフレーム時間（ページの中で測った値を読む）
  res.measure = await ev(s1, "measure()");
  // 8. タブのメモリ
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
  await send("Page.navigate", { url: page }, s2);
  await sleep(800);
  await ev(s2, "localStorage.setItem('k', 'v2')");
  await sleep(500);
  res.storage_event = await ev(s1, "R.storage");
}

function stop() {
  try { process.kill(-br.pid, "SIGTERM"); } catch (e) { /* もう終わっている */ }
}
main().catch((e) => { res.error = String(e && e.message || e); })
  .finally(() => { console.log(JSON.stringify(res)); stop(); setTimeout(() => process.exit(0), 500); });
