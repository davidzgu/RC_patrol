# Arduino Nano ESP32 Servo & Motor Control

Control a servo and motor (via ESC) using WiFi from your laptop.

## Hardware Connections

### Servo
- Signal → Pin 9
- VCC → 5V
- GND → GND

### ESC (Electronic Speed Controller)
- Signal → Pin 10
- Red (5V) → Leave disconnected or connect to external power
- Black (GND) → GND (shared with Arduino)
- **Motor battery** → Connect to ESC power input

⚠️ **Important**: Power the motor through the ESC with an external battery (LiPo/NiMH). Do NOT power high-current motors from the Arduino 5V pin.

## Setup Instructions

1. **Install ESP32 board support** in Arduino IDE:
   - Go to File → Preferences
   - Add to "Additional Board Manager URLs":
     ```
     https://espressif.github.io/arduino-esp32/package_esp32_index.json
     ```
   - Tools → Board → Boards Manager → Search "ESP32" → Install

2. **Install ESP32Servo library**:
   - Tools → Manage Libraries → Search "ESP32Servo" → Install

3. **Edit WiFi credentials** in the code:
   ```cpp
   const char* ssid = "YOUR_WIFI_SSID";
   const char* password = "YOUR_WIFI_PASSWORD";
   ```

4. **Upload**:
   - Board: "Arduino Nano ESP32"
   - Port: Select your board's port
   - Click Upload

5. **Get IP address**:
   - Open Serial Monitor (115200 baud)
   - Copy the IP address shown (e.g., 192.168.1.42)

6. **Control from laptop**:
   - Make sure laptop is on the same WiFi network
   - Open browser and go to: `http://192.168.1.42` (use your IP)
   - Use sliders to control servo and motor

## ESC Calibration

If your ESC needs calibration:
1. Set `throttle = 2000` in setup
2. Power on Arduino (ESC will beep)
3. Connect ESC battery
4. Wait for beep, change to `throttle = 1000`
5. ESC should beep confirming calibration
6. Restore code to original and re-upload

## Safety Notes

- **Motor starts at 1000μs (stopped)**. Test carefully before increasing throttle.
- Keep fingers away from motor/propeller when powered.
- Use the emergency stop: reload the page or disconnect ESC battery.
