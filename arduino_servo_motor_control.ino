#include <WiFi.h>
#include <ESP32Servo.h>

// WiFi credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Pin definitions
const int SERVO_PIN = 9;
const int ESC_PIN = 10;

// Objects
Servo servo;
Servo esc;
WiFiServer server(80);

// Control values
int servoAngle = 90;    // 0-180 degrees (90 = center)
int throttle = 1000;    // 1000-2000 microseconds (1000 = stopped, 2000 = full)

// Control constants
const int THROTTLE_STEP = 50;  // 5% of 1000 range = 50
const int SERVO_STEP = 27;     // 15% of 180 range = 27

void setup() {
  Serial.begin(115200);
  
  // Attach servo and ESC
  servo.attach(SERVO_PIN);
  esc.attach(ESC_PIN, 1000, 2000);
  
  // Initialize to safe positions
  servo.write(servoAngle);
  esc.writeMicroseconds(1000); // ESC stopped
  
  // Connect to WiFi
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  
  server.begin();
}

void stopAll() {
  throttle = 1000;
  servoAngle = 90;
  esc.writeMicroseconds(throttle);
  servo.write(servoAngle);
  Serial.println("STOP - All motors stopped, servo centered");
}

void loop() {
  WiFiClient client = server.available();
  
  if (client) {
    String request = "";
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        request += c;
        
        if (c == '\n') {
          // Parse HTTP request for keyboard commands
          if (request.indexOf("GET /key?code=") >= 0) {
            if (request.indexOf("code=ArrowUp") >= 0) {
              throttle += THROTTLE_STEP;
              throttle = constrain(throttle, 1000, 2000);
              esc.writeMicroseconds(throttle);
              Serial.println("Arrow Up - Throttle: " + String(throttle));
            }
            else if (request.indexOf("code=ArrowDown") >= 0) {
              throttle -= THROTTLE_STEP;
              throttle = constrain(throttle, 1000, 2000);
              esc.writeMicroseconds(throttle);
              Serial.println("Arrow Down - Throttle: " + String(throttle));
            }
            else if (request.indexOf("code=ArrowLeft") >= 0) {
              servoAngle -= SERVO_STEP;
              servoAngle = constrain(servoAngle, 0, 180);
              servo.write(servoAngle);
              Serial.println("Arrow Left - Servo: " + String(servoAngle));
            }
            else if (request.indexOf("code=ArrowRight") >= 0) {
              servoAngle += SERVO_STEP;
              servoAngle = constrain(servoAngle, 0, 180);
              servo.write(servoAngle);
              Serial.println("Arrow Right - Servo: " + String(servoAngle));
            }
            else if (request.indexOf("code=Space") >= 0) {
              stopAll();
            }
          }
          
          // Send HTML response
          client.println("HTTP/1.1 200 OK");
          client.println("Content-type:text/html");
          client.println();
          client.println("<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width'>");
          client.println("<title>RC Patrol Control</title>");
          client.println("<style>");
          client.println("body{font-family:Arial;text-align:center;margin:50px;background:#1a1a1a;color:#fff;}");
          client.println(".status{font-size:24px;margin:20px;padding:15px;background:#2a2a2a;border-radius:10px;}");
          client.println(".controls{margin:30px auto;max-width:400px;padding:20px;background:#2a2a2a;border-radius:10px;}");
          client.println(".btn{font-size:18px;padding:15px 30px;margin:10px;background:#4CAF50;color:#fff;border:none;border-radius:5px;cursor:pointer;}");
          client.println(".btn:active{background:#45a049;}");
          client.println(".stop-btn{background:#f44336;font-size:20px;padding:20px 40px;}");
          client.println(".key-hint{font-size:14px;color:#888;margin-top:30px;}");
          client.println("</style></head><body>");
          client.println("<h1>🚗 RC Patrol Control</h1>");
          client.println("<div class='status'>");
          client.println("Servo: <b>" + String(servoAngle) + "°</b> | ");
          client.println("Throttle: <b>" + String(throttle) + "μs</b>");
          client.println("</div>");
          client.println("<div class='controls'>");
          client.println("<h3>Keyboard Controls</h3>");
          client.println("<button class='btn stop-btn' onclick=\"sendKey('Space')\">⏹ STOP (Space)</button><br>");
          client.println("<button class='btn' onclick=\"sendKey('ArrowUp')\">▲ Faster</button><br>");
          client.println("<button class='btn' onclick=\"sendKey('ArrowLeft')\">◀ Left</button> ");
          client.println("<button class='btn' onclick=\"sendKey('ArrowDown')\">▼ Slower</button> ");
          client.println("<button class='btn' onclick=\"sendKey('ArrowRight')\">▶ Right</button>");
          client.println("</div>");
          client.println("<div class='key-hint'>");
          client.println("💡 Use arrow keys on keyboard or click buttons<br>");
          client.println("Up/Down: ±5% throttle | Left/Right: ±15° steering | Space: Emergency Stop");
          client.println("</div>");
          client.println("<script>");
          client.println("function sendKey(code){fetch('/key?code='+code).then(()=>location.reload());}");
          client.println("document.addEventListener('keydown',e=>{");
          client.println("if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Space'].includes(e.code)){");
          client.println("e.preventDefault();sendKey(e.code);}}");
          client.println(");");
          client.println("</script>");
          client.println("</body></html>");
          break;
        }
      }
    }
    client.stop();
  }
}