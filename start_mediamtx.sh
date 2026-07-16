#!/bin/bash
# RC Patrol - Start MediaMTX WebRTC Server
# Low-latency streaming server for GoPro Hero 11

PROJECT_DIR="/Users/davidgu/Documents/GenAI Projects/RC_Patrol"
CONFIG_FILE="$PROJECT_DIR/mediamtx.yml"
MEDIAMTX_BIN="/opt/homebrew/opt/mediamtx/bin/mediamtx"

echo "🚗 RC Patrol - Starting MediaMTX WebRTC Server"
echo "=============================================="

# Check if MediaMTX is already running
if pgrep -f "mediamtx" > /dev/null; then
    echo "⚠️  MediaMTX is already running. Stopping it first..."
    pkill -f "mediamtx"
    sleep 2
fi

# Start MediaMTX in background
echo "Starting MediaMTX server..."
$MEDIAMTX_BIN "$CONFIG_FILE" > "$PROJECT_DIR/logs/mediamtx_console.log" 2>&1 &
MEDIAMTX_PID=$!

sleep 2

# Check if it started successfully
if pgrep -f "mediamtx" > /dev/null; then
    echo "✅ MediaMTX server started successfully!"
    echo ""
    echo "📡 Server Information:"
    echo "   Local IP: $(ipconfig getifaddr en0)"
    echo "   RTMP Input: rtmp://$(ipconfig getifaddr en0):1935/gopro"
    echo "   WebRTC Stream: http://localhost:8888/gopro"
    echo "   Web Interface: http://localhost:8080"
    echo "   API/Stats: http://localhost:9997"
    echo ""
    echo "🎥 GoPro Setup:"
    echo "   1. On GoPro Hero 11: Swipe down → Preferences → Connections"
    echo "   2. Select 'Live Stream'"
    echo "   3. Choose 'Set Up New Platform' → RTMP"
    echo "   4. Enter RTMP URL: rtmp://$(ipconfig getifaddr en0):1935/gopro"
    echo "   5. Leave Stream Key empty (or use any value)"
    echo "   6. Start streaming on GoPro"
    echo ""
    echo "🎮 Control Interface:"
    echo "   Open http://localhost:8080 in your browser"
    echo ""
    echo "📝 Logs:"
    echo "   MediaMTX: $PROJECT_DIR/logs/mediamtx.log"
    echo "   Console: $PROJECT_DIR/logs/mediamtx_console.log"
    echo ""
    echo "💡 Expected Latency: 0.2-0.5 seconds (WebRTC)"
else
    echo "❌ Failed to start MediaMTX. Check the logs:"
    echo "   $PROJECT_DIR/logs/mediamtx_console.log"
    exit 1
fi
