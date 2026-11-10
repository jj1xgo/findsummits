// 地理院の標高タイル（8 ビットの RGB、インターレースなしの PNG）を、Canvas を通さずに復号できるかの確かめ（#197）。
// DecompressionStream（ブラウザにも Node.js にもある）で IDAT を展開し、PNG のフィルタを戻して RGBA にし、
// probe.js と同じ「真ん中の画素」と「全画素の RGBA の値の合計」を出す。Chrome の Canvas の読み出しと比べるため。
// 使い方: node png_decode_check.js <PNG のファイル>...
"use strict";
const fs = require("fs");

async function inflate(bytes) {
  const stream = new Blob([bytes]).stream().pipeThrough(new DecompressionStream("deflate"));
  return new Uint8Array(await new Response(stream).arrayBuffer());
}

function paeth(a, b, c) {
  const p = a + b - c;
  const pa = Math.abs(p - a);
  const pb = Math.abs(p - b);
  const pc = Math.abs(p - c);
  return pa <= pb && pa <= pc ? a : pb <= pc ? b : c;
}

const SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

// HLD 4.19.2 の「標高タイルの復号」の確かめ: シグネチャ、IHDR（8 ビットの RGB、圧縮とフィルタの方式 0、インターレースなし）、
// 展開した長さ、行のフィルタの種類（0〜4）。外れたら例外にする（製品では fetch_tile の「失敗」に当たる）
async function decode(buf) {
  if (buf.length < 8 || SIGNATURE.some((b, i) => buf[i] !== b)) throw new Error("PNG のシグネチャでない");
  const view = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  let width = 0;
  let height = 0;
  const idat = [];
  for (let i = 8; i < buf.length;) {
    const len = view.getUint32(i);
    const type = String.fromCharCode(...buf.subarray(i + 4, i + 8));
    const data = buf.subarray(i + 8, i + 8 + len);
    if (type === "IHDR") {
      width = view.getUint32(i + 8);
      height = view.getUint32(i + 12);
      if (len !== 13 || data[8] !== 8 || data[9] !== 2 || data[10] !== 0 || data[11] !== 0 || data[12] !== 0) {
        throw new Error("8 ビットの RGB、圧縮とフィルタの方式 0、インターレースなしの PNG だけを扱う");
      }
    } else if (type === "IDAT") {
      idat.push(data);
    }
    i += 12 + len;
  }
  const raw = await inflate(Buffer.concat(idat));
  const bpp = 3;
  const stride = width * bpp;
  if (width === 0 || raw.length !== height * (stride + 1)) throw new Error("展開した長さが IHDR と合わない");
  const rgb = new Uint8Array(height * stride);
  for (let y = 0; y < height; y++) {
    const f = raw[y * (stride + 1)];
    if (f > 4) throw new Error(`行 ${y} のフィルタの種類 ${f} は無い`);
    for (let x = 0; x < stride; x++) {
      const v = raw[y * (stride + 1) + 1 + x];
      const a = x >= bpp ? rgb[y * stride + x - bpp] : 0;
      const b = y > 0 ? rgb[(y - 1) * stride + x] : 0;
      const c = x >= bpp && y > 0 ? rgb[(y - 1) * stride + x - bpp] : 0;
      const pred = f === 0 ? 0 : f === 1 ? a : f === 2 ? b : f === 3 ? (a + b) >> 1 : paeth(a, b, c);
      rgb[y * stride + x] = (v + pred) & 255;
    }
  }
  return { width, height, rgb };
}

(async () => {
  for (const file of process.argv.slice(2)) {
    const { width, height, rgb } = await decode(new Uint8Array(fs.readFileSync(file)));
    let sum = 0;
    for (let i = 0; i < rgb.length; i++) sum += rgb[i];
    sum += 255 * width * height;
    const m = (128 * width + 128) * 3;
    console.log(`${file}: 真ん中 ${rgb[m]},${rgb[m + 1]},${rgb[m + 2]},255、合計 ${sum}`);
  }
})();
