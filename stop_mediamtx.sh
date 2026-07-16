#!/bin/bash
# RC Patrol - Stop MediaMTX Server

echo "🛑 Stopping RC Patrol MediaMTX Server..."

if pgrep -f "mediamtx" > /dev/null; then
    pkill -f "mediamtx"
    sleep 1
    echo "✅ MediaMTX server stopped"
else
    echo "ℹ️  MediaMTX server is not running"
fi
