// Chromium 系のブラウザ（Chrome・Brave）をヘッドレスで起動し、確かめ用のページを手順どおりに開いて結果の JSON を集める。
// DevTools Protocol を Node.js の組み込みの fetch と WebSocket で使う（npm は使わない）。
// 使い方: node headless_probe.js <ブラウザのコマンド> <プロファイルのディレクトリ> <ページの根の URL> <手順>...
//   手順: save（index.html を開いて「保存する」を押す）・run（index.html#auto を開いて終わるまで待つ）・
//         a・b（a/index.html・b/index.html を開く）・samples:<保存先>（run の後に「見本を落とす」を押し、落ちたものを保存先に置く）
//   同じプロファイルのディレクトリで 2 回起動すると、閉じた後の localStorage を確かめられる。
// 出力: 手順ごとの JSON（1 行に 1 つ）。
"use strict";
const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");

const [bin, profile, root, ...steps] = process.argv.slice(2);
if (!bin || !profile || !root || steps.length === 0) {
  console.error("使い方: headless_probe.js <ブラウザ> <プロファイル> <根の URL> <手順>...");
  process.exit(2);
}
fs.mkdirSync(profile, { recursive: true });
const port = 9300 + Math.floor(Math.random() * 500);
const browser = spawn(bin, ["--headless=new", "--no-first-run", "--no-default-browser-check", `--user-data-dir=${path.resolve(profile)}`,
  `--remote-debugging-port=${port}`, "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function main() {
  let targets = null;
  for (let i = 0; i < 100 && !targets; i++) {
    try { targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); } catch (e) { await sleep(200); }
  }
  if (!targets) throw new Error("ブラウザの DevTools に繋がらない");
  const page = targets.find((t) => t.type === "page");
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  let id = 0;
  const pending = new Map();
  ws.onmessage = (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
  };
  await new Promise((r) => { ws.onopen = r; });
  const send = (method, params = {}) => new Promise((r) => { const n = ++id; pending.set(n, r); ws.send(JSON.stringify({ id: n, method, params })); });
  const evalJs = async (expr) => {
    const res = await send("Runtime.evaluate", { expression: expr, returnByValue: true, awaitPromise: true });
    return res.result && res.result.result ? res.result.result.value : undefined;
  };
  const open = async (rel) => { await send("Page.navigate", { url: root.replace(/\/$/, "") + "/" + rel }); await sleep(1500); };
  const readJson = async () => {
    const text = await evalJs("(document.getElementById('json') || {}).value || ''");
    return text ? JSON.parse(text) : null;
  };

  for (const step of steps) {
    if (step === "save") {
      await open("index.html");
      const saved = await evalJs("document.getElementById('save').click(); document.getElementById('saved').textContent");
      console.log(JSON.stringify({ step, saved }));
    } else if (step === "run" || step.startsWith("samples:")) {
      await open("index.html#auto");
      const start = Date.now();
      while (Date.now() - start < 180000) {
        if (await evalJs("document.body && document.body.getAttribute('data-done') === '1'")) break;
        await sleep(1000);
      }
      if (step.startsWith("samples:")) {
        const dest = path.resolve(step.slice("samples:".length));
        fs.mkdirSync(dest, { recursive: true });
        await send("Browser.setDownloadBehavior", { behavior: "allow", downloadPath: dest });
        await evalJs("document.getElementById('samples').click()");
        for (let i = 0; i < 60 && !fs.existsSync(path.join(dest, "probe-samples.zip")); i++) await sleep(500);
      }
      console.log(JSON.stringify({ step, seconds: Math.round((Date.now() - start) / 1000), json: await readJson() }));
    } else if (step === "a" || step === "b") {
      await open(`${step}/index.html`);
      console.log(JSON.stringify({ step, answer: await evalJs("document.getElementById('answer').textContent"), json: await readJson() }));
    } else {
      throw new Error(`知らない手順 ${step}`);
    }
  }
  // brave-browser などはシェルの包みで、包みを kill しても本体が残るので、DevTools で閉じる
  await send("Browser.close");
  ws.close();
}

main().catch((e) => { console.error(e); process.exitCode = 1; }).finally(async () => {
  browser.kill();
  await sleep(1000);
});
