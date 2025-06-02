from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import socket
import utils.config as config
import re

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
                    log_pattern = re.compile(
                        r"^(?P<time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(?P<level>[A-Z]+)\] (?P<message>.*)$"
                    )
                    html_lines = []

                    for log in logs:
                        match = log_pattern.match(log.strip())
                        if match:
                            time = (
                                f"<span class='log-time'>{match.group('time')}</span>"
                            )
                            level = f"<span class='log-level log-{match.group('level').lower()}'>{match.group('level')}</span>"
                            message = f"<span class='log-message'>{match.group('message')}</span>"
                            html_lines.append(
                                f"<div class='log-line'>{time} {level} {message}</div>"
                            )
                        else:
                            html_lines.append(
                                f"<div class='log-line'>{log.strip()}</div>"
                            )  # fallback for unmatched lines

                    log_data = "\n".join(html_lines)
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
    .log-container {{
      background: #2e2e4d;
      padding: 1rem;
      border-radius: 6px;
      overflow-y: auto;
      height: 80vh;
      box-shadow: 0 0 10px #0005;
      font-size: 0.9rem;
      line-height: 1.4;
      font-family: monospace;
      white-space: pre-wrap;
    }}
    .log-line {{ margin-bottom: -20px; }}
    .log-time {{ color: #aaa; }}
    .log-level {{ font-weight: bold; margin: 0 0.5rem; }}
    .log-info {{ color: #8ec07c; }}
    .log-error {{ color: #fb4934; }}
    .log-warning {{ color: #fabd2f; }}
    .log-debug {{ color: #83a598; }}
    .log-startup {{ color: #d3869b; }}
    .log-message {{ color: #ebdbb2; }}
  </style>
  <script>
    function fetchLogs() {{
      fetch('/logs')
        .then(response => response.text())
        .then(data => {{
          const logContainer = document.getElementById('log');
          logContainer.innerHTML = data;
          logContainer.scrollTop = logContainer.scrollHeight;
        }});
    }}

    setInterval(fetchLogs, {config.log_refresh_interval}000);
    window.onload = fetchLogs;
  </script>
</head>
<body>
  <h1>Purgarr Logs ({hostname})</h1>
  <div id="log" class="log-container">Loading...</div>
</body>
</html>
"""
