// 本機測試伺服器（Node，無需安裝套件）。所有檔案加 Cache-Control: no-store。
// 用途：這台電腦的 Python 被防火牆擋住區網連入，Node 已有允許規則，手機測試用這個。
// 用法：node serve.js [埠號，預設 8766]
const http = require("http"), fs = require("fs"), path = require("path");
const root = __dirname, port = +process.argv[2] || 8766;
const types = { ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8", ".geojson": "application/geo+json; charset=utf-8", ".pbf": "application/x-protobuf",
  ".jpg": "image/jpeg", ".png": "image/png", ".txt": "text/plain; charset=utf-8", ".md": "text/plain; charset=utf-8" };
http.createServer((req, res) => {
  const p = decodeURIComponent(req.url.split("?")[0]);
  let f = path.join(root, p === "/" ? "index.html" : p);
  if (!f.startsWith(root)) { res.writeHead(403); return res.end(); }
  fs.readFile(f, (err, buf) => {
    if (err) { res.writeHead(404, { "Cache-Control": "no-store" }); return res.end("404"); }
    res.writeHead(200, { "Content-Type": types[path.extname(f).toLowerCase()] || "application/octet-stream", "Cache-Control": "no-store" });
    res.end(buf);
  });
}).listen(port, "0.0.0.0", () => console.log("serving " + root + " on " + port));
