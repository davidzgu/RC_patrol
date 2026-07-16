#!/usr/bin/env python3
# Simple HTTP server for RC Patrol web interface

import http.server
import socketserver
import os

PORT = 8080
WEB_DIR = "/Users/davidgu/Documents/GenAI Projects/RC_Patrol/web"

os.chdir(WEB_DIR)

Handler = http.server.SimpleHTTPRequestHandler

# Enable CORS for Arduino requests
class CORSRequestHandler(Handler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
    print(f"🌐 Serving RC Patrol web interface at http://localhost:{PORT}")
    print(f"📂 Serving from: {WEB_DIR}")
    print("Press Ctrl+C to stop")
    httpd.serve_forever()
