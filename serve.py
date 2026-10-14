"""本機測試伺服器：所有檔案都加 Cache-Control: no-store，避免改版後瀏覽器還拿舊檔。
用法：python serve.py [埠號，預設 8765]"""
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

class NoCache(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    ThreadingHTTPServer(("", port), NoCache).serve_forever()
