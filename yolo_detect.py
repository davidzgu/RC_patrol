#!/usr/bin/env python3
"""
RC Patrol - YOLO Object Detection
Captures frames from MediaMTX WebRTC/RTMP stream and detects objects
"""

import cv2
from ultralytics import YOLO
import time
from datetime import datetime

# Configuration
STREAM_URL = "rtmp://localhost:1935/gopro"  # MediaMTX RTMP stream
MODEL = "yolov8n.pt"  # YOLOv8 nano (fastest), alternatives: yolov8s.pt, yolov8m.pt
CONFIDENCE_THRESHOLD = 0.5  # Only show detections above 50% confidence
OUTPUT_DIR = "/Users/davidgu/Documents/GenAI Projects/RC_Patrol/detections"

# Colors for different object classes (BGR format for OpenCV)
COLORS = {
    'person': (0, 255, 0),      # Green
    'cat': (255, 0, 255),        # Magenta
    'dog': (0, 255, 255),        # Yellow
    'chair': (255, 255, 0),      # Cyan
    'couch': (128, 0, 128),      # Purple
    'default': (0, 165, 255)     # Orange
}

def main():
    print("🚗 RC Patrol - YOLO Object Detection")
    print("=" * 50)
    print(f"Stream URL: {STREAM_URL}")
    print(f"Model: {MODEL}")
    print(f"Confidence: {CONFIDENCE_THRESHOLD}")
    print("=" * 50)
    print("\nInitializing YOLO model...")
    
    # Load YOLO model (downloads automatically on first run)
    try:
        model = YOLO(MODEL)
        print(f"✅ Model loaded: {MODEL}")
        print(f"📦 Classes: {len(model.names)} objects (person, cat, dog, chair, etc.)")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return
    
    print("\nConnecting to GoPro stream...")
    print("(Make sure GoPro is streaming to MediaMTX)")
    
    # Open video stream
    cap = cv2.VideoCapture(STREAM_URL)
    
    if not cap.isOpened():
        print("❌ Failed to connect to stream")
        print("💡 Make sure:")
        print("   1. MediaMTX is running (./start_all.sh)")
        print("   2. GoPro is streaming to rtmp://YOUR_IP:1935/gopro")
        return
    
    print("✅ Connected to stream!")
    print("\n" + "=" * 50)
    print("🎥 DETECTION STARTED")
    print("=" * 50)
    print("Press 'q' to quit")
    print("Press 's' to save current frame with detections")
    print("=" * 50 + "\n")
    
    frame_count = 0
    fps_start_time = time.time()
    fps = 0
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("⚠️  Lost connection to stream, retrying...")
                time.sleep(1)
                continue
            
            frame_count += 1
            
            # Calculate FPS every 30 frames
            if frame_count % 30 == 0:
                fps = 30 / (time.time() - fps_start_time)
                fps_start_time = time.time()
            
            # Run YOLO detection
            results = model(frame, conf=CONFIDENCE_THRESHOLD, verbose=False)
            
            # Get detections
            detections = results[0].boxes
            
            # Draw detections on frame
            annotated_frame = frame.copy()
            detection_text = []
            
            for box in detections:
                # Get box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                
                # Get color for this class
                color = COLORS.get(class_name, COLORS['default'])
                
                # Draw bounding box
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                
                # Draw label with background
                label = f"{class_name} {confidence:.2f}"
                label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                cv2.rectangle(annotated_frame, 
                            (x1, y1 - label_size[1] - 10), 
                            (x1 + label_size[0], y1), 
                            color, -1)
                cv2.putText(annotated_frame, label, (x1, y1 - 5),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                
                detection_text.append(f"{class_name} ({confidence:.2%})")
            
            # Draw FPS and detection count
            info_text = f"FPS: {fps:.1f} | Detections: {len(detections)}"
            cv2.putText(annotated_frame, info_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Print detections to console (every 30 frames to avoid spam)
            if frame_count % 30 == 0 and len(detections) > 0:
                print(f"[Frame {frame_count}] Detected: {', '.join(detection_text)}")
            
            # Display annotated frame
            cv2.imshow('RC Patrol - YOLO Detection', annotated_frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\n🛑 Stopping detection...")
                break
            elif key == ord('s'):
                # Save frame
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{OUTPUT_DIR}/detection_{timestamp}.jpg"
                cv2.imwrite(filename, annotated_frame)
                print(f"📸 Saved: {filename}")
    
    except KeyboardInterrupt:
        print("\n\n🛑 Detection stopped by user")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print(f"\n✅ Processed {frame_count} frames")
        print("👋 Goodbye!")

if __name__ == "__main__":
    import os
    # Create detections directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    main()
