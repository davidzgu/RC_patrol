# 🚗 RC Patrol - Indoor Pet Monitor & Security Camera

Transform an RC car into a WiFi-controlled pet monitor with **ultra-low latency WebRTC streaming** from GoPro Hero 11 Black.

## 🎯 Project Overview

- **Arduino Nano ESP32**: Controls servo (steering) and ESC (motor) via WiFi
- **GoPro Hero 11 Black**: Live RTMP → WebRTC video streaming
- **MediaMTX Server**: Sub-second latency WebRTC conversion (**0.2-0.5s lag**)
- **Web Control Interface**: Unified dashboard for driving and viewing
- **Keyboard Controls**: Arrow keys for intuitive control

## ⚡ Why WebRTC?

- **HLS (old)**: 2-10 seconds lag → Too slow for safe driving
- **WebRTC (current)**: 0.2-0.5 seconds lag → Near-instant feedback like FPV drones

## 📁 Project Structure

```
RC_Patrol/
├── arduino_servo_motor_control.ino  # Arduino firmware
├── mediamtx.yml                      # MediaMTX WebRTC config
├── start_all.sh                      # Start everything (recommended)
├── stop_all.sh                       # Stop everything
├── start_mediamtx.sh                 # Start MediaMTX only
├── stop_mediamtx.sh                  # Stop MediaMTX only
├── start_web_server.py               # Web interface server
├── web/
│   └── index.html                    # WebRTC control interface
├── hls/                              # HLS fallback (optional)
├── logs/                             # Server logs
└── recordings/                       # Optional stream recordings
```

## 🔧 Hardware Setup

### Arduino Connections

**Servo (Steering)**
- Signal → Pin 9
- VCC → 5V
- GND → GND

**ESC (Motor)**
- Signal → Pin 10
- Red (5V) → Leave disconnected
- Black (GND) → GND (shared with Arduino)
- **Motor battery** → Connect to ESC power input

⚠️ **Important**: Power the motor through the ESC with an external battery (LiPo/NiMH). Do NOT power from Arduino 5V.

### GoPro Mounting
- Securely mount GoPro Hero 11 Black on RC car
- Ensure clear forward view
- Balance weight distribution

## 🚀 Setup Instructions

### 1. Arduino Setup

1. Install **ESP32 board support** in Arduino IDE:
   - File → Preferences → Additional Board Manager URLs:
     ```
     https://espressif.github.io/arduino-esp32/package_esp32_index.json
     ```
   - Tools → Board → Boards Manager → Search "ESP32" → Install

2. Install **ESP32Servo library**:
   - Tools → Manage Libraries → Search "ESP32Servo" → Install

3. Edit WiFi credentials in `arduino_servo_motor_control.ino`:
   ```cpp
   const char* ssid = "YOUR_WIFI_SSID";
   const char* password = "YOUR_WIFI_PASSWORD";
   ```

4. Upload to Arduino Nano ESP32:
   - Board: "Arduino Nano ESP32"
   - Port: Select your board's port
   - Click Upload

5. Open Serial Monitor (115200 baud) and note the IP address (e.g., `192.168.1.42`)

### 2. MediaMTX WebRTC Server Setup

MediaMTX is already installed and configured.

1. **Start all services** (recommended):
   ```bash
   cd "/Users/davidgu/Documents/GenAI Projects/RC_Patrol"
   ./start_all.sh
   ```

2. Note your Mac's IP address from the output (e.g., `192.168.12.40`)

3. **Stop all services** when done:
   ```bash
   ./stop_all.sh
   ```

### 3. GoPro Hero 11 Setup

1. On GoPro: **Swipe down** → **Preferences** → **Connections** → **Live Stream**
2. Select **Set Up New Platform**
3. Choose **RTMP**
4. Enter:
   - **RTMP URL**: `rtmp://YOUR_MAC_IP:1935/gopro` (from start_all.sh output)
   - **Stream Key**: Leave empty (or use any value)
5. Save and start streaming

### 4. Control Interface Setup

1. Edit `web/index.html` and update Arduino IP:
   ```javascript
   const ARDUINO_IP = 'http://192.168.1.42'; // Your Arduino IP
   ```

2. Open in browser:
   ```
   http://localhost:8080
   ```

## 🎮 Controls

### Keyboard Controls
- **↑ (Up Arrow)**: Increase throttle by 5%
- **↓ (Down Arrow)**: Decrease throttle by 5%
- **← (Left Arrow)**: Turn left 15°
- **→ (Right Arrow)**: Turn right 15°
- **Space**: Emergency stop (motor stop, steering center)

### On-Screen Controls
- Click buttons for the same functionality
- Real-time status display shows current steering angle and throttle

## 📊 Features

✅ **Ultra-Low Latency**: 0.2-0.5s WebRTC streaming (sub-second!)  
✅ **WiFi Control**: No cables needed for operation  
✅ **Keyboard & Touch Controls**: Flexible input methods  
✅ **Emergency Stop**: Instant safety cutoff  
✅ **Status Monitoring**: Real-time connection and vehicle status  
✅ **Responsive Design**: Works on desktop and tablets  
✅ **Auto-reconnect**: Handles temporary disconnections  

## 🔍 Troubleshooting

### Arduino Not Connecting
- Check WiFi credentials
- Ensure laptop and Arduino on same network
- Verify IP address in Serial Monitor
- Check firewall settings

### GoPro Stream Not Showing
- Verify GoPro is streaming (check GoPro screen)
- Confirm RTMP URL: `rtmp://YOUR_MAC_IP:1935/gopro`
- Check MediaMTX is running: `ps aux | grep mediamtx`
- View logs: `cat logs/mediamtx.log`
- Wait 5-10 seconds for WebRTC connection to establish
- Try refreshing the browser

### ESC Not Responding
- Calibrate ESC (see below)
- Check signal wire connection
- Verify battery is connected and charged

### ESC Calibration (if needed)
1. Set `throttle = 2000` in Arduino `setup()`
2. Upload and power on Arduino
3. Connect ESC battery (listen for beep)
4. Change to `throttle = 1000` and re-upload
5. ESC should beep confirming calibration

## 📝 Technical Details

### Arduino Control
- **Throttle range**: 1000μs (stopped) to 2000μs (full speed)
- **Servo range**: 0° (full left) to 180° (full right), center at 90°
- **Step sizes**: 50μs (5%) throttle, 27° (15%) steering
- **WiFi protocol**: HTTP GET requests

### Video Streaming
- **Protocol**: RTMP (GoPro) → MediaMTX → WebRTC (Browser)
- **Latency**: 0.2-0.5 seconds (WebRTC low-latency)
- **Resolution**: GoPro default (1080p/4K depending on settings)
- **Ports**: 1935 (RTMP input), 8889 (WebRTC), 8080 (HTTP), 9997 (API)

## 🛡️ Safety Notes

⚠️ **Always test in a safe, open area**  
⚠️ **Keep fingers away from moving parts**  
⚠️ **Use Space key for emergency stop**  
⚠️ **Monitor battery levels**  
⚠️ **Start with low throttle to test**  

## 📋 TODO / Future Enhancements

- [ ] Add reverse functionality (H-bridge motor driver)
- [ ] Implement autonomous patrol routes
- [ ] Add distance sensors for obstacle avoidance
- [ ] Battery level monitoring
- [ ] Motion detection alerts
- [ ] Recording clips on demand
- [ ] Mobile app control
- [ ] Night vision mode

## 📄 License

Personal project - Educational use

---

**Last Updated**: July 14, 2026  
**Project by**: David Gu