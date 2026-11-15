// Firefox をヘッドレスで起動し、probe.html を file:// で開いて 9 つの能力を確かめる（#299）。
// WebDriver BiDi（Firefox の --remote-debugging-port が待ち受ける ws://127.0.0.1:<port>/session）を、
// Node.js の組み込みの WebSocket で使う（npm も geckodriver も使わない）。
// 使い方: node bidi_probe.js <Firefox の実行ファイル> <空の作業ディレクトリ>
//   作業ディレクトリの下に、新しいプロファイル（prof/）とダウンロード先（dl/）を作る。空でなければ止まる（前回の結果を取り違えないため）。
//   --no-remote で、持ち主が開いている Firefox に渡さない。プロセスのグループで起動し、終わりにグループごと止める。
// 出力: 能力ごとの結果を 1 行の JSON で標準出力に出す。ホストのパスは出さない。
"use strict";
const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");

const [bin, work] = process.argv.slice(2);
if (!bin || !work) {
  console.error("使い方: bidi_probe.js <Firefox の実行ファイル> <空の作業ディレクトリ>");
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
const port = 9800 + Math.floor(Math.random() * 100);
const br = spawn(bin, ["--headless", "--no-remote", "--profile", path.resolve(prof), `--remote-debugging-port=${port}`, "about:blank"],
  { stdio: "ignore", detached: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const res = { browser: path.basename(bin) };

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
  let ws = null;
  for (let i = 0; i < 100 && !ws; i++) {
    try {
      ws = new WebSocket(`ws://127.0.0.1:${port}/session`);
      await new Promise((r, j) => { ws.onopen = r; ws.onerror = j; });
    } catch (e) { ws = null; await sleep(200); }
  }
  if (!ws) throw new Error("WebDriver BiDi に繋がらない");
  let id = 0;
  const pend = new Map();
  const handlers = [];
  ws.onmessage = (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); } else handlers.forEach((h) => h(m));
  };
  const send = (method, params = {}) => new Promise((r) => { const n = ++id; pend.set(n, r); ws.send(JSON.stringify({ id: n, method, params })); });
  const s = await send("session.new", { capabilities: {} });
  res.version = s.result && s.result.capabilities.browserVersion;
  const ctx = (await send("browsingContext.getTree", {})).result.contexts[0].context;
  // ページの中の値は JSON の文字列にして受け取る（BiDi の値の直列化の形に頼らない）。
  const ev = async (c, expr) => {
    const r = await send("script.evaluate", { expression: `(async () => JSON.stringify(await (${expr})))()`, target: { context: c }, awaitPromise: true });
    if (r.error || r.result.type === "exception") throw new Error("script.evaluate: " + JSON.stringify(r).slice(0, 300));
    const v = r.result.result.value;
    return v === undefined ? undefined : JSON.parse(v);
  };
  const dlr = await send("browser.setDownloadBehavior", { downloadBehavior: { type: "allowed", destinationFolder: path.resolve(dl) } });
  if (dlr.error) throw new Error("browser.setDownloadBehavior: " + dlr.error);
  // 2. 通信の記録と、応答・失敗の注入
  await send("session.subscribe", { events: ["network.beforeRequestSent"] });
  const seen = [];
  await send("network.addIntercept", { phases: ["beforeRequestSent"], urlPatterns: [{ type: "pattern", protocol: "https", hostname: "probe.invalid" }] });
  handlers.push(async (m) => {
    if (m.method !== "network.beforeRequestSent" || !m.params.isBlocked) return;
    const u = m.params.request.url;
    seen.push(u);
    if (u.endsWith("ok.txt")) {
      await send("network.provideResponse", { request: m.params.request.request, statusCode: 200, reasonPhrase: "OK",
        headers: [{ name: "Access-Control-Allow-Origin", value: { type: "string", value: "*" } }], body: { type: "string", value: "hello" } });
    } else {
      await send("network.failRequest", { request: m.params.request.request });
    }
  });
  await send("browsingContext.navigate", { context: ctx, url: page, wait: "complete" });
  // 1. file:// で開く
  res.file_url = String(await ev(ctx, "location.href")).startsWith("file://");
  res.net = await ev(ctx, "net()");
  res.net_seen = seen.slice();
  // 3. Canvas の画素
  res.pixel = await ev(ctx, "pixel()");
  // 4. ファイル選択
  const el = await send("script.evaluate", { expression: "document.getElementById('f')", target: { context: ctx }, awaitPromise: false, resultOwnership: "none" });
  const sf = await send("input.setFiles", { context: ctx, element: { sharedId: el.result.result.sharedId }, files: [upload] });
  if (sf.error) throw new Error("input.setFiles: " + sf.error);
  await sleep(300);
  res.file = await ev(ctx, "R.file");
  // 5. ダウンロード
  await ev(ctx, "document.getElementById('dl').click()");
  await sleep(1500);
  res.download = fs.readdirSync(dl).map((f) => [f, fs.readFileSync(path.join(dl, f), "utf8")]);
  // 7. 応答時間とフレーム時間（ページの中で測った値を読む）
  res.measure = await ev(ctx, "measure()");
  // 8. タブのメモリ（BiDi に JS ヒープを読む命令は無いので、プロセスのグループの RSS）
  res.memory = { js_heap_used: null, group_rss_kib: groupRssKiB(br.pid) };
  // 9. 実際の入力（押す・2 回動かす・離す）
  const c = await ev(ctx, "padCenter()");
  const pa = await send("input.performActions", { context: ctx, actions: [{ type: "pointer", id: "mouse", parameters: { pointerType: "mouse" }, actions: [
    { type: "pointerMove", x: c.x, y: c.y }, { type: "pointerDown", button: 0 },
    { type: "pointerMove", x: c.x + 10, y: c.y }, { type: "pointerMove", x: c.x + 20, y: c.y }, { type: "pointerUp", button: 0 }] }] });
  if (pa.error) throw new Error("input.performActions: " + pa.error);
  await sleep(200);
  res.pointer = await ev(ctx, "R.pointer");
  // 6. 2 つのタブの localStorage と storage イベント
  const c2 = (await send("browsingContext.create", { type: "tab" })).result.context;
  await send("browsingContext.navigate", { context: c2, url: page, wait: "complete" });
  await ev(c2, "localStorage.setItem('k', 'v2')");
  await sleep(500);
  res.storage_event = await ev(ctx, "R.storage");
  await send("session.end", {});
}

function stop() {
  try { process.kill(-br.pid, "SIGTERM"); } catch (e) { /* もう終わっている */ }
}
main().catch((e) => { res.error = String(e && e.message || e); })
  .finally(() => { console.log(JSON.stringify(res)); stop(); setTimeout(() => process.exit(0), 500); });
