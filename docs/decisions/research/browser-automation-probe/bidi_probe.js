// Firefox をヘッドレスで起動し、probe.html を file:// で開いて 9 つの能力を確かめる（#299）。
// WebDriver BiDi を Node.js の組み込みの WebSocket で使う（npm も geckodriver も使わない）。
// 使い方: node bidi_probe.js <Firefox の実行ファイル> <空の作業ディレクトリ>
//   作業ディレクトリの下に、新しいプロファイル（prof/）とダウンロード先（dl/）を作る。空でなければ止まる（前回の結果を取り違えないため）。
//   --no-remote で、開いている Firefox に渡さない。ポート 0 で起動し、このブラウザが標準エラー出力に出す
//   「WebDriver BiDi listening on ws://…」の行から接続先を読む（ほかのブラウザにつながないため）。
//   ブラウザはプロセスのグループで起動し、終わり・例外・時間切れ（全体 90 秒、1 つの命令 15 秒）・SIGINT・SIGTERM のどれでも
//   グループごと止める。SIGTERM で止まらなければ SIGKILL。
// 出力: 能力ごとの値と合否（checks）を 1 行の JSON で標準出力に出す。ホストのパスは出さない。
//   version は BiDi の browserVersion で、ESR でも「esr」が付かない（153.5.1 ESR で「153.5.1」）。チャンネルは
//   `firefox --version` の出力（ESR なら「153.5.1esr」）で見分ける。
// 終了コード: 9 つとも期待どおりなら 0、そうでなければ 1、使い方の誤りは 2。
"use strict";
const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");

const [bin, work] = process.argv.slice(2);
if (!bin || !work) {
  console.error("使い方: bidi_probe.js <Firefox の実行ファイル> <空の作業ディレクトリ>");
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

const br = spawn(bin, ["--headless", "--no-remote", "--profile", prof, "--remote-debugging-port=0", "about:blank"],
  { stdio: ["ignore", "ignore", "pipe"], detached: true });
let wsUrl = null;
let stderrBuf = "";
br.stderr.on("data", (d) => {
  stderrBuf += d.toString();
  const m = /WebDriver BiDi listening on (ws:\/\/127\.0\.0\.1:[0-9]+)/.exec(stderrBuf);
  if (m && !wsUrl) wsUrl = m[1];
  if (stderrBuf.length > 65536) stderrBuf = stderrBuf.slice(-4096);
});
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
    "8_memory": mem.group_rss_kib > 0,
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
process.on("unhandledRejection", (e) => finish("受け手のない失敗: " + String(e && e.message || e)));

async function main() {
  for (let i = 0; i < 150 && !wsUrl; i++) await sleep(200);
  if (!wsUrl) throw new Error("WebDriver BiDi の待ち受けの行が出ない");
  ws = new WebSocket(`${wsUrl}/session`);
  await new Promise((r, j) => { ws.onopen = r; ws.onerror = () => j(new Error("WebSocket に繋がらない")); });
  let id = 0;
  const pend = new Map();
  const handlers = [];
  ws.onmessage = (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && pend.has(m.id)) { pend.get(m.id).resolve(m); pend.delete(m.id); } else handlers.forEach((h) => { Promise.resolve().then(() => h(m)).catch((e) => finish("受け手の失敗: " + String(e && e.message || e))); });
  };
  ws.onclose = () => { for (const p of pend.values()) p.reject(new Error("WebSocket が切れた")); pend.clear(); };
  const send = (method, params = {}) => new Promise((resolve, reject) => {
    const n = ++id;
    const t = setTimeout(() => { pend.delete(n); reject(new Error("応答が無い: " + method)); }, 15000);
    pend.set(n, { resolve: (m) => { clearTimeout(t); resolve(m); }, reject: (e) => { clearTimeout(t); reject(e); } });
    ws.send(JSON.stringify({ id: n, method, params }));
  });
  const must = async (method, params) => {
    const r = await send(method, params);
    if (r.error) throw new Error(method + ": " + r.error);
    return r.result;
  };
  const s = await must("session.new", { capabilities: {} });
  res.version = s.capabilities.browserVersion;
  const ctx = (await must("browsingContext.getTree", {})).contexts[0].context;
  // ページの中の値は JSON の文字列にして受け取る（BiDi の値の直列化の形に頼らない）。
  const ev = async (c, expr) => {
    const r = await must("script.evaluate", { expression: `(async () => JSON.stringify(await (${expr})))()`, target: { context: c }, awaitPromise: true });
    if (r.type === "exception") throw new Error("script.evaluate: " + expr);
    return r.result.value === undefined ? undefined : JSON.parse(r.result.value);
  };
  await must("browser.setDownloadBehavior", { downloadBehavior: { type: "allowed", destinationFolder: dl } });
  // 2. 通信の記録と、応答・失敗の注入
  await must("session.subscribe", { events: ["network.beforeRequestSent"] });
  const seen = [];
  await must("network.addIntercept", { phases: ["beforeRequestSent"], urlPatterns: [{ type: "pattern", protocol: "https", hostname: "probe.invalid" }] });
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
  await must("browsingContext.navigate", { context: ctx, url: page, wait: "complete" });
  // 1. file:// で開く
  res.file_url = String(await ev(ctx, "location.href")).startsWith("file://");
  res.net = await ev(ctx, "net()");
  res.net_seen = seen.slice();
  // 3. Canvas の画素
  res.pixel = await ev(ctx, "pixel()");
  // 4. ファイル選択
  const el = await must("script.evaluate", { expression: "document.getElementById('f')", target: { context: ctx }, awaitPromise: false, resultOwnership: "none" });
  await must("input.setFiles", { context: ctx, element: { sharedId: el.result.sharedId }, files: [upload] });
  await sleep(300);
  res.file = await ev(ctx, "R.file");
  // 5. ダウンロード
  await ev(ctx, "document.getElementById('dl').click()");
  await sleep(1500);
  res.download = fs.readdirSync(dl).map((f) => [f, fs.readFileSync(path.join(dl, f), "utf8")]);
  // 7. フレーム間隔（ページの中で測った、操作の無いときの値を読む）
  res.measure = await ev(ctx, "measure()");
  // 8. メモリの値（BiDi に JS ヒープを読む命令は無いので、プロセスのグループの RSS の和。補助の値）
  res.memory = { js_heap_used: null, group_rss_kib: groupRssKiB(br.pid) };
  // 9. 実際の入力（押す・2 回動かす・離す）
  const c = await ev(ctx, "padCenter()");
  await must("input.performActions", { context: ctx, actions: [{ type: "pointer", id: "mouse", parameters: { pointerType: "mouse" }, actions: [
    { type: "pointerMove", x: c.x, y: c.y }, { type: "pointerDown", button: 0 },
    { type: "pointerMove", x: c.x + 10, y: c.y }, { type: "pointerMove", x: c.x + 20, y: c.y }, { type: "pointerUp", button: 0 }] }] });
  await sleep(200);
  res.pointer = await ev(ctx, "R.pointer");
  // 6. 2 つのタブの localStorage と storage イベント
  const c2 = (await must("browsingContext.create", { type: "tab" })).context;
  await must("browsingContext.navigate", { context: c2, url: page, wait: "complete" });
  await ev(c2, "localStorage.setItem('k', 'v2')");
  await sleep(500);
  res.storage_event = await ev(ctx, "R.storage");
  await send("session.end", {});
}

main().then(() => finish(), (e) => finish(String(e && e.message || e)));
