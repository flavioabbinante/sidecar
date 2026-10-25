"""HTTPS side of sidecar: serves the probe page and stores what the TV reports."""

import json
import re
import ssl
import subprocess
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib import resources

MAX_BODY = 1_000_000
SENSITIVE = re.compile(r"serial|uuid|deviceid|adsid|ipaddress|mac|email|token|account|password", re.I)


def redact(obj):
    """Blank out values whose key looks personal, at any depth."""
    if isinstance(obj, dict):
        return {k: "<redacted>" if SENSITIVE.search(k) else redact(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [redact(v) for v in obj]
    return obj


def ensure_cert(directory, domain):
    """Create a self-signed certificate once; the TV will ask you to accept it."""
    directory.mkdir(parents=True, exist_ok=True)
    crt, key = directory / "cert.pem", directory / "key.pem"
    if not (crt.exists() and key.exists()):
        subprocess.run(
            [
                "openssl",
                "req",
                "-x509",
                "-newkey",
                "rsa:2048",
                "-nodes",
                "-days",
                "365",
                "-keyout",
                str(key),
                "-out",
                str(crt),
                "-subj",
                f"/CN={domain}",
                "-addext",
                f"subjectAltName=DNS:{domain}",
            ],
            check=True,
            capture_output=True,
        )
        key.chmod(0o600)
    return crt, key


def make_handler(out_dir):
    page = resources.files("sidecar").joinpath("static/probe.html").read_bytes()

    class Handler(BaseHTTPRequestHandler):
        def _send(self, code, body=b"", ctype="text/plain"):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path in ("/", "/probe"):
                self._send(200, page, "text/html; charset=utf-8")
            else:
                self._send(404)

        def do_POST(self):
            if self.path != "/api/report":
                return self._send(404)
            length = int(self.headers.get("Content-Length", 0))
            if not 0 < length <= MAX_BODY:
                return self._send(413)
            try:
                report = redact(json.loads(self.rfile.read(length)))
            except ValueError:
                return self._send(400)
            out_dir.mkdir(parents=True, exist_ok=True)
            path = out_dir / f"report-{time.strftime('%Y%m%d-%H%M%S')}.json"
            path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
            print(f"saved {path}", flush=True)
            self._send(200, b"ok")

        def log_message(self, fmt, *args):
            print(f"{self.client_address[0]} {fmt % args}", flush=True)

    return Handler


def serve(bind_ip, port, domain, out_dir, cert_dir):
    crt, key = ensure_cert(cert_dir, domain)
    httpd = ThreadingHTTPServer((bind_ip, port), make_handler(out_dir))
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(crt, key)
    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
    print(f"https://{domain}/ on {bind_ip}:{port}, reports in {out_dir}", flush=True)
    httpd.serve_forever()
