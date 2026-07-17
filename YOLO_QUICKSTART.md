# 🎯 YOLO Object Detection - Quick Start

## ✅ Setup Complete!

YOLOv8 is installed and ready to detect 80 different objects in your GoPro stream.

---

## 🚀 How to Run

### 1. Start RC Patrol System
```bash
cd "/Users/davidgu/Documents/GenAI Projects/RC_Patrol"
./start_all.sh
```

### 2. Start GoPro Streaming
- GoPro: Stream to `rtmp://192.168.12.40:1935/gopro`

### 3. Run YOLO Detection
```bash
python3 yolo_detect.py
```

A window will open showing your GoPro feed with **bounding boxes** around detected objects!

---

## 🎮 Controls

- **q** - Quit detection
- **s** - Save current frame with detections
- Window shows live FPS and detection count

---

## 📦 What Can YOLO Detect?

**80 object classes including:**

### 🐾 Pets & Animals
- person, cat, dog, bird, horse, sheep, cow, bear

### 🪑 Furniture & Indoor
- chair, couch, bed, dining table, potted plant, tv, laptop

### 🚪 Navigation Obstacles
- door, stairs, bicycle, backpack, suitcase, bottle

### 🍕 Kitchen & Food
- refrigerator, oven, microwave, sink, bowl, cup, fork, knife

### And 52 more classes!

---

## 📊 Performance

- **Model**: YOLOv8 Nano (yolov8n.pt) - fastest version
- **Speed**: 20-40 FPS on Mac (depends on GoPro resolution)
- **Accuracy**: ~50-90% depending on object and lighting

### Want Better Accuracy?

Edit `yolo_detect.py` and change the model:
```python
MODEL = "yolov8s.pt"  # Small (slower but more accurate)
# or
MODEL = "yolov8m.pt"  # Medium (best balance)
```

---

## 📸 Saved Detections

Press **'s'** while detection is running to save frames.

Saved to: `/Users/davidgu/Documents/GenAI Projects/RC_Patrol/detections/`

---

## 🔧 Configuration

Edit `yolo_detect.py` to customize:

```python
CONFIDENCE_THRESHOLD = 0.5  # Lower = more detections (may include false positives)
MODEL = "yolov8n.pt"        # yolov8s.pt or yolov8m.pt for better accuracy
```

---

## 🐛 Troubleshooting

### "Failed to connect to stream"
- Make sure `./start_all.sh` is running
- Verify GoPro is streaming (check GoPro display shows "LIVE")
- Check MediaMTX logs: `tail -f logs/mediamtx.log`

### Low FPS / Laggy
- Use yolov8n.pt (fastest model)
- Reduce GoPro resolution to 1080p
- Close other heavy apps

### No detections showing
- Increase lighting (YOLO needs good visibility)
- Lower `CONFIDENCE_THRESHOLD` to 0.3
- Make sure objects are in frame and not too far away

---

## 🎯 Next Steps

Once basic detection works, you can:

1. **Web Overlay** - Show detections in browser interface
2. **Object Tracking** - Follow specific objects (e.g., "follow person")
3. **Obstacle Avoidance** - Auto-stop before hitting furniture
4. **Alerts** - Notify when specific objects detected (e.g., "cat entered room")

Let me know what you want to add next!

---

**Last Updated**: July 15, 2026  
**Status**: ✅ YOLO basic detection ready
