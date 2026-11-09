"""Local-only webhook receiver for this lesson."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os

root = Path(os.environ.get("HYDRA_LAB25_ROOT", "/root/lab/reversible-actions"))
port = int(os.environ.get("LAB25_PORT", "8790"))
events = {"/notify": "webhook_called", "/cancel": "webhook_undone"}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        event = events.get(self.path)
        if not event:
            self.send_error(404)
            return
        self.rfile.read(int(self.headers.get("Content-Length", "0")))
        with (root / "reports" / "events.log").open("a", encoding="utf-8") as log:
            log.write(event + "\n")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, fmt, *args):
        pass

server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
(root / "reports" / "webhook-ready").touch()
server.serve_forever()
