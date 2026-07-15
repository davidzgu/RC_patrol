#!/bin/bash
# RC Patrol - System Check
# Verifies all components are ready

echo "🔍 RC Patrol System Check"
echo "========================="
echo ""

# Check nginx installation
echo "1. Checking nginx-full installation..."
if command -v /opt/homebrew/opt/nginx-full/bin/nginx &> /dev/null; then
    echo "   ✅ nginx-full installed"
    /opt/homebrew/opt/nginx-full/bin/nginx -v 2>&1 | head -1
else
    echo "   ❌ nginx-full not found"
fi
echo ""

# Check ffmpeg installation
echo "2. Checking ffmpeg installation..."
if command -v ffmpeg &> /dev/null; then
    echo "   ✅ ffmpeg installed"
    ffmpeg -version | head -1
else
    echo "   ❌ ffmpeg not found"
fi
echo ""

# Check project files
echo "3. Checking project files..."
PROJECT_DIR="/Users/davidgu/Documents/GenAI Projects/RC_Patrol"
FILES=(
    "arduino_servo_motor_control.ino"
    "nginx_rtmp.conf"
    "start_rtmp_server.sh"
    "stop_rtmp_server.sh"
    "web/index.html"
)

for file in "${FILES[@]}"; do
    if [ -f "$PROJECT_DIR/$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file (missing)"
    fi
done
echo ""

# Check directories
echo "4. Checking project directories..."
DIRS=("logs" "hls" "web" "recordings")
for dir in "${DIRS[@]}"; do
    if [ -d "$PROJECT_DIR/$dir" ]; then
        echo "   ✅ $dir/"
    else
        echo "   ❌ $dir/ (missing)"
    fi
done
echo ""

# Get network info
echo "5. Network information..."
IP=$(ipconfig getifaddr en0 2>/dev/null)
if [ -n "$IP" ]; then
    echo "   📡 Mac IP (WiFi): $IP"
    echo "   🎥 GoPro RTMP URL: rtmp://$IP:1935/live"
    echo "   🎮 Control Interface: http://localhost:8080"
else
    echo "   ⚠️  No WiFi IP found (check en0 connection)"
fi
echo ""

# Check if nginx is running
echo "6. Checking nginx status..."
if pgrep -f "nginx.*rtmp" > /dev/null; then
    echo "   ✅ nginx RTMP server is running"
else
    echo "   ℹ️  nginx RTMP server is not running"
    echo "   Run: ./start_rtmp_server.sh to start"
fi
echo ""

echo "========================="
echo "💡 Next Steps:"
echo "   1. Upload arduino_servo_motor_control.ino to Arduino"
echo "   2. Run: ./start_rtmp_server.sh"
echo "   3. Configure GoPro with RTMP URL"
echo "   4. Open http://localhost:8080 to control"
echo ""
