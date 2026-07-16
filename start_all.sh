#!/bin/bash
# RC Patrol - Start All Services (WebRTC + Web Server)

PROJECT_DIR="/Users/davidgu/Documents/GenAI Projects/RC_Patrol"

echo "🚗 RC Patrol - Starting All Services"
echo "====================================="
echo ""

# Start MediaMTX
echo "1. Starting MediaMTX WebRTC server..."
"$PROJECT_DIR/start_mediamtx.sh"
echo ""

# Wait for MediaMTX to be ready
sleep 2

# Start web server in background
echo "2. Starting web interface server..."
python3 "$PROJECT_DIR/start_web_server.py" > "$PROJECT_DIR/logs/web_server.log" 2>&1 &
WEB_PID=$!
sleep 1

if ps -p $WEB_PID > /dev/null; then
    echo "✅ Web server started at http://localhost:8080"
else
    echo "❌ Web server failed to start"
fi

echo ""
echo "=============================================="
echo "✅ RC Patrol is ready!"
echo "=============================================="
echo ""
echo "📋 Quick Start:"
echo "   1. GoPro: Stream to rtmp://$(ipconfig getifaddr en0):1935/gopro"
echo "   2. Browser: Open http://localhost:8080"
echo "   3. Arduino: Make sure it's powered and connected to WiFi"
echo ""
echo "🛑 To stop all services:"
echo "   Run: $PROJECT_DIR/stop_all.sh"
echo ""
