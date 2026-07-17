#!/bin/bash
# RC Patrol - Stop YOLO Services

PROJECT_DIR="/Users/davidgu/Documents/GenAI Projects/RC_Patrol"

echo "🛑 Stopping RC Patrol YOLO Services..."
echo ""

# Stop YOLO web server
if pgrep -f "yolo_web_server.py" > /dev/null; then
    pkill -f "yolo_web_server.py"
    echo "✅ YOLO server stopped"
else
    echo "ℹ️  YOLO server not running"
fi

# Stop MediaMTX
"$PROJECT_DIR/stop_mediamtx.sh"

# Stop web server
if pgrep -f "start_web_server.py" > /dev/null; then
    pkill -f "start_web_server.py"
    echo "✅ Web server stopped"
else
    echo "ℹ️  Web server not running"
fi

echo ""
echo "✅ All services stopped"
