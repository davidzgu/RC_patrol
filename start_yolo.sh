#!/bin/bash
# RC Patrol - Start All Services with YOLO Detection

PROJECT_DIR="/Users/davidgu/Documents/GenAI Projects/RC_Patrol"

echo "🚗 RC Patrol - Starting with YOLO Detection"
echo "=========================================="
echo ""

# Check and stop existing services
echo "0. Checking for existing services..."
if pgrep -f "start_web_server.py" > /dev/null; then
    echo "   ⚠️  Web server already running, stopping it..."
    pkill -f "start_web_server.py"
    sleep 1
fi
if pgrep -f "yolo_web_server.py" > /dev/null; then
    echo "   ⚠️  YOLO server already running, stopping it..."
    pkill -f "yolo_web_server.py"
    sleep 1
fi
echo "   ✅ Ready to start"
echo ""

# 1. Start MediaMTX (for GoPro RTMP input)
echo "1. Starting MediaMTX server..."
"$PROJECT_DIR/start_mediamtx.sh"
sleep 2

# 2. Start YOLO Web Server
echo ""
echo "2. Starting YOLO detection server..."
echo "   (This will process GoPro stream and send to browser)"
python3 "$PROJECT_DIR/yolo_web_server.py" &
YOLO_PID=$!
echo "   ✅ YOLO server started (PID: $YOLO_PID)"

# 3. Start web server
echo ""
echo "3. Starting web interface..."
python3 "$PROJECT_DIR/start_web_server.py" &
WEB_PID=$!
sleep 1
echo "   ✅ Web server started (PID: $WEB_PID)"

echo ""
echo "=========================================="
echo "✅ RC Patrol with YOLO is ready!"
echo "=========================================="
echo ""
echo "📋 Quick Start:"
echo "   1. GoPro: Stream to rtmp://192.168.12.40:1935/gopro"
echo "   2. Browser: Open http://localhost:8080"
echo "   3. You'll see LIVE OBJECT DETECTION with bounding boxes!"
echo ""
echo "🛑 To stop all services:"
echo "   Run: $PROJECT_DIR/stop_yolo.sh"
echo ""
