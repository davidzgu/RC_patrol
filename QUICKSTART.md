# 🚀 Quick Start Guide - RC Patrol WebRTC

## ✅ Setup Complete!

MediaMTX WebRTC server is installed and configured for **sub-second latency** (0.2-0.5s).

---

## 🎯 How to Use

### 1. Start the System
```bash
cd "/Users/davidgu/Documents/GenAI Projects/RC_Patrol"
./start_all.sh
```

### 2. Configure GoPro Hero 11
1. **Swipe down** → **Preferences** → **Connections** → **Live Stream**
2. **Set Up New Platform** → **RTMP**
3. Enter:
   - **RTMP URL**: `rtmp://192.168.12.40:1935/gopro`
   - **Stream Key**: (leave empty or any value)
4. **Start Streaming** on GoPro

### 3. Open Control Interface
- Browser: **http://localhost:8080**
- Expected latency: **0.2-0.5 seconds** (WebRTC)

### 4. Stop the System
```bash
./stop_all.sh
```

---

## 🎮 Controls

- **↑** (Up Arrow): Increase throttle +5%
- **↓** (Down Arrow): Decrease throttle -5%
- **←** (Left Arrow): Turn left -15°
- **→** (Right Arrow): Turn right +15°
- **Space**: Emergency stop (motor off, center steering)

---

## 🔧 Troubleshooting

### Video says "Connecting to GoPro WebRTC..."
- ✅ Check GoPro is streaming (display shows "LIVE")
- ✅ Verify RTMP URL: `rtmp://192.168.12.40:1935/gopro`
- ✅ Wait 5-10 seconds for WebRTC handshake
- ✅ Check MediaMTX logs: `cat logs/mediamtx.log`

### "Arduino disconnected" message
- ✅ Check Arduino IP in `web/index.html` (line with `ARDUINO_IP`)
- ✅ Verify Arduino is on same WiFi network
- ✅ Open Serial Monitor to confirm Arduino IP

### High latency / laggy video
- Check WiFi signal strength (GoPro to Mac)
- Reduce GoPro resolution (1080p better than 4K for latency)
- Close other apps using network

---

## 📊 System Architecture

```
GoPro Hero 11 Black
    ↓ (RTMP stream)
MediaMTX Server (Mac)
    ↓ (WebRTC)
Browser (http://localhost:8080)
    ↓ (HTTP commands)
Arduino Nano ESP32
    ↓ (PWM signals)
Servo + ESC → RC Car
```

---

## 📝 File Structure

- `start_all.sh` - **Start everything** (use this!)
- `stop_all.sh` - Stop all services
- `mediamtx.yml` - WebRTC server config
- `web/index.html` - Control interface
- `logs/` - Server and error logs

---

## 🆘 Need Help?

**View live logs:**
```bash
tail -f logs/mediamtx.log
```

**Check what's running:**
```bash
ps aux | grep mediamtx
ps aux | grep start_web_server
```

**Force kill everything:**
```bash
pkill -f mediamtx
pkill -f start_web_server
```

---

## 🎉 Expected Performance

- **Latency**: 0.2-0.5 seconds (near-instant)
- **Resolution**: Up to 4K (1080p recommended for lowest latency)
- **Range**: WiFi range (20-30 meters indoors)
- **Frame rate**: 30-60 fps depending on GoPro settings

---

**Last Updated**: July 14, 2026  
**Status**: ✅ WebRTC setup complete and verified
