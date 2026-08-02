"""
Local dev server that understands _redirects (200 rewrite / 301 redirect),
so clean URLs like /brick-repointing work the same as they will on Netlify.
Plain `python -m http.server` does NOT read _redirects at all — every clean
URL 404s there, which is not a bug in the site, just a gap in that server.

Usage:
    python scripts/dev_server.py [port]   (default port 8000)
"""
import http.server
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

RULES = []  # list of (path, target, code)


def load_redirects():
    RULES.clear()
    with open("_redirects", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) != 3:
                continue
            path, target, code = parts
            RULES.append((path, target, int(code)))


class RedirectingHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        load_redirects()  # pick up _redirects edits without restarting
        url_path = self.path.split("?", 1)[0].split("#", 1)[0]

        # Exact-match rules first (most of _redirects), then the /* catch-all.
        for path, target, code in RULES:
            if path == url_path:
                if code == 200:
                    self.path = target
                    return super().send_head()
                else:
                    self.send_response(code)
                    self.send_header("Location", target)
                    self.end_headers()
                    return None

        for path, target, code in RULES:
            if path == "/*":
                if os.path.exists("." + url_path) or url_path in ("", "/"):
                    return super().send_head()
                self.send_response(code)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                with open(target, "rb") as fh:
                    self.wfile.write(fh.read())
                return None

        return super().send_head()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    load_redirects()
    print(f"Serving {ROOT} at http://localhost:{port}/ (honouring _redirects, {len(RULES)} rules loaded)")
    http.server.HTTPServer(("", port), RedirectingHandler).serve_forever()
