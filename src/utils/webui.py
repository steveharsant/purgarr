from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import socket
import utils.config as config

LOG_FILE = "purgarr.log"


class LogHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(self.html_page().encode("utf-8"))

        elif self.path == "/logs":
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "r") as f:
                    logs = f.readlines()[-config.log_lines :]
                    log_data = "".join(logs)
            else:
                log_data = "Log file not found."

            self.send_response(200)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(log_data.encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()

    def html_page(self):
        hostname = socket.gethostname()
        return f"""
<html>
<head>
  <title>Purgarr Logs</title>
  <style>
    body {{
      background: #1e1e2f;
      color: #d0d0f0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, monospace;
      margin: 2rem;
    }}
    h1 {{
      color: #89b4fa;
      font-weight: 700;
      margin-bottom: 1rem;
      border-bottom: 2px solid #89b4fa;
      padding-bottom: 0.25rem;
      user-select: none;
    }}
    pre {{
      background: #2e2e4d;
      padding: 1rem;
      border-radius: 6px;
      overflow-y: auto;
      height: 80vh;
      box-shadow: 0 0 10px #0005;
      font-size: 0.9rem;
      line-height: 1.4;
      white-space: pre-wrap;
    }}
  </style>
  <script>
    function fetchLogs() {{
      fetch('/logs')
        .then(response => response.text())
        .then(data => {{
          const logContainer = document.getElementById('log');
          logContainer.textContent = data;
          logContainer.scrollTop = logContainer.scrollHeight;
        }});
    }}

    setInterval(fetchLogs, {config.log_refresh_interval}000);
    window.onload = fetchLogs;
  </script>
</head>
<body>
  <h1>Purgarr Logs ({hostname})</h1>
  <pre id="log">Loading...</pre>
</body>
</html>
"""
