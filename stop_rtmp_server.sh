#!/bin/bash
# RC Patrol - Stop RTMP Server

NGINX_BIN="/opt/homebrew/opt/nginx-full/bin/nginx"

echo "🛑 Stopping RC Patrol RTMP Server..."

if pgrep -f "nginx.*rtmp" > /dev/null; then
    $NGINX_BIN -s stop
    echo "✅ RTMP server stopped"
else
    echo "ℹ️  RTMP server is not running"
fi
