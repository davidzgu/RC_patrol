#!/usr/bin/env python3
"""
RC Patrol - YOLO Web Overlay Server
Streams YOLO detections to web interface via WebSocket
"""

import cv2
from ultralytics import YOLO
import asyncio
import websockets
import json
import base64
import threading
import time
from datetime import datetime

# Configuration
STREAM_URL = "rtmp://localhost:1935/gopro"
MODEL = "yolov8n.pt"
CONFIDENCE_THRESHOLD = 0.5
WEBSOCKET_PORT = 8765
OUTPUT_DIR = "/Users/davidgu/Documents/GenAI Projects/RC_Patrol/detections"

# Global state
latest_frame = None
latest_detections = []
frame_lock = threading.Lock()
clients = set()

# Colors for different object classes (BGR format)
COLORS = {
    'person': (0, 255, 0),
    'cat': (255, 0, 255),
    'dog': (0, 255, 255),
    'chair': (255, 255, 0),
    'couch': (128, 0, 128),
    'default': (0, 165, 255)
}

def capture_and_detect():
    """Background thread: capture frames and run YOLO detection"""
    global latest_frame, latest_detections
    
    print("🎥 Loading YOLO model...")
    model = YOLO(MODEL)
    print(f"✅ Model loaded: {MODEL}")
    
    while True:  # Outer loop for reconnection
        print(f"📡 Connecting to stream: {STREAM_URL}")
        cap = cv2.VideoCapture(STREAM_URL)
        
        if not cap.isOpened():
            print("❌ Failed to connect to stream, retrying in 3 seconds...")
            time.sleep(3)
            continue
        
        print("✅ Connected! Starting detection...")
        frame_count = 0
        fps_start = time.time()
        fps = 0
        consecutive_failures = 0
        
        while True:  # Inner loop for frame processing
            ret, frame = cap.read()
            if not ret:
                consecutive_failures += 1
                if consecutive_failures > 30:  # 30 failed reads in a row
                    print("⚠️  Lost connection, reconnecting...")
                    break
                time.sleep(0.1)
                continue
            
            consecutive_failures = 0  # Reset on successful read
            frame_count += 1
            
            # Calculate FPS
            if frame_count % 30 == 0:
                fps = 30 / (time.time() - fps_start)
                fps_start = time.time()
            
            # Run YOLO detection
            results = model(frame, conf=CONFIDENCE_THRESHOLD, verbose=False)
            detections = results[0].boxes
            
            # Draw detections on frame
            annotated_frame = frame.copy()
            detection_list = []
            
            for box in detections:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                
                color = COLORS.get(class_name, COLORS['default'])
                
                # Draw bounding box
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                
                # Draw label
                label = f"{class_name} {confidence:.2f}"
                label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                cv2.rectangle(annotated_frame,
                            (x1, y1 - label_size[1] - 10),
                            (x1 + label_size[0], y1),
                            color, -1)
                cv2.putText(annotated_frame, label, (x1, y1 - 5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                
                detection_list.append({
                    'class': class_name,
                    'confidence': round(confidence, 2),
                    'bbox': [x1, y1, x2, y2]
                })
            
            # Draw FPS and detection count
            info_text = f"FPS: {fps:.1f} | Objects: {len(detections)}"
            cv2.putText(annotated_frame, info_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Update global state
            with frame_lock:
                latest_frame = annotated_frame
                latest_detections = detection_list
            
            # Small delay to prevent maxing CPU
            time.sleep(0.005)
        
        cap.release()
        print("🔄 Reconnection attempt in 3 seconds...")
        time.sleep(3)

async def handle_client(websocket):
    """Handle WebSocket client connections"""
    global clients
    clients.add(websocket)
    print(f"✅ Client connected ({len(clients)} total)")
    
    try:
        # Send frames to client
        while True:
            if latest_frame is not None:
                with frame_lock:
                    frame = latest_frame.copy()
                    detections = latest_detections.copy()
                
                # Encode frame as JPEG
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
                jpg_base64 = base64.b64encode(buffer).decode('utf-8')
                
                # Send data
                data = {
                    'frame': jpg_base64,
                    'detections': detections,
                    'timestamp': datetime.now().isoformat()
                }
                
                try:
                    await websocket.send(json.dumps(data))
                except websockets.exceptions.ConnectionClosed:
                    break
            
            await asyncio.sleep(0.016)  # ~60 FPS
    
    except Exception as e:
        print(f"❌ Client error: {e}")
    
    finally:
        clients.remove(websocket)
        print(f"🔌 Client disconnected ({len(clients)} remaining)")

async def start_websocket_server():
    """Start WebSocket server"""
    print(f"🌐 Starting WebSocket server on port {WEBSOCKET_PORT}...")
    async with websockets.serve(handle_client, "localhost", WEBSOCKET_PORT):
        print(f"✅ WebSocket server running on ws://localhost:{WEBSOCKET_PORT}")
        await asyncio.Future()  # Run forever

def main():
    print("=" * 60)
    print("🚗 RC Patrol - YOLO Web Overlay Server")
    print("=" * 60)
    print(f"Stream: {STREAM_URL}")
    print(f"Model: {MODEL}")
    print(f"WebSocket: ws://localhost:{WEBSOCKET_PORT}")
    print(f"Web UI: http://localhost:8080")
    print("=" * 60)
    print()
    
    # Create output directory
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Start capture thread
    capture_thread = threading.Thread(target=capture_and_detect, daemon=True)
    capture_thread.start()
    
    # Start WebSocket server
    print("🚀 Starting services...\n")
    asyncio.run(start_websocket_server())

if __name__ == "__main__":
    main()
