#!/bin/bash
# RC Patrol - Stop All Services

PROJECT_DIR="/Users/davidgu/Documents/GenAI Projects/RC_Patrol"

echo "🛑 Stopping RC Patrol Services..."
echo ""

# Stop MediaMTX
"$PROJECT_DIR/stop_mediamtx.sh"

# Stop web server
if pgrep -f "start_web_server.py" > /dev/null; then
    pkill -f "start_web_server.py"
    echo "✅ Web server stopped"
else
    echo "ℹ️  Web server was not running"
fi

echo ""
echo "✅ All services stopped"
