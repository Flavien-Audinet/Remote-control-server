from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import urllib

PORT = 0000
PASSWORD = "MDP"

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        action = parsed_path.path.strip("/").lower()
        params = urllib.parse.parse_qs(parsed_path.query)
        key = params.get("key", [""])[0]

        if key != PASSWORD:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"Unauthorized")
            return

        if action == "reboot":
            os.system("shutdown /r /t 5")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Rebooting")
        elif action == "shutdown":
            os.system("shutdown /s /t 5")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Shutting down")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Unknown action")

httpd = HTTPServer(("", PORT), RequestHandler)
print(f"[*] Listening on port {PORT}...")
httpd.serve_forever()
