#!/usr/bin/env python3
"""
Test YOLO installation and download model
"""

from ultralytics import YOLO
import sys

print("🔍 Testing YOLO installation...")
print("=" * 50)

try:
    print("\n1. Loading YOLOv8 nano model...")
    model = YOLO('yolov8n.pt')
    print("   ✅ Model loaded successfully!")
    
    print("\n2. Model information:")
    print(f"   - Classes: {len(model.names)}")
    print(f"   - Sample classes: {list(model.names.values())[:10]}")
    
    print("\n3. All 80 COCO classes:")
    classes_list = list(model.names.values())
    for i in range(0, len(classes_list), 5):
        print(f"   {', '.join(classes_list[i:i+5])}")
    
    print("\n" + "=" * 50)
    print("✅ YOLO is ready to use!")
    print("=" * 50)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)
