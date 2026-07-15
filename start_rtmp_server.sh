#!/bin/bash
# RC Patrol - Start RTMP Server
# This script starts the nginx RTMP server for receiving GoPro stream

PROJECT_DIR="/Users/davidgu/Documents/GenAI Projects/RC_Patrol"
NGINX_CONF="$PROJECT_DIR/nginx_rtmp.conf"
NGINX_BIN="/opt/homebrew/opt/nginx-full/bin/nginx"

echo "🚗 RC Patrol - Starting RTMP Server"
echo "===================================="

# Check if nginx is already running
if pgrep -f "nginx.*rtmp" > /dev/null; then
    echo "⚠️  nginx is already running. Stopping it first..."
    $NGINX_BIN -s stop 2>/dev/null
    sleep 2
fi

# Start nginx with our config
echo "Starting nginx RTMP server..."
$NGINX_BIN -c "$NGINX_CONF"

if [ $? -eq 0 ]; then
    echo "✅ RTMP server started successfully!"
    echo ""
    echo "📡 Server Information:"
    echo "   RTMP URL: rtmp://$(ipconfig getifaddr en0):1935/live"
    echo "   Stream Key: stream"
    echo "   Web Interface: http://localhost:8080"
    echo "   Statistics: http://localhost:8080/stat"
    echo ""
    echo "🎥 GoPro Setup:"
    echo "   1. On GoPro Hero 11: Swipe down → Preferences → Connections"
    echo "   2. Select 'Live Stream'"
    echo "   3. Choose 'Set Up New Platform' → RTMP"
    echo "   4. Enter RTMP URL: rtmp://$(ipconfig getifaddr en0):1935/live"
    echo "   5. Enter Stream Key: stream"
    echo "   6. Start streaming on GoPro"
    echo ""
    echo "🎮 Control Interface:"
    echo "   Open http://localhost:8080 in your browser"
    echo "   Update Arduino IP in the HTML file if needed"
    echo ""
    echo "📝 Logs: $PROJECT_DIR/logs/error.log"
else
    echo "❌ Failed to start nginx. Check the logs:"
    echo "   $PROJECT_DIR/logs/error.log"
    exit 1
fi
