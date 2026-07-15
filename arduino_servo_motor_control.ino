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
int servoAngle = 90;    // 0-180 degrees
int throttle = 1000;    // 1000-2000 microseconds (1000 = stopped, 2000 = full)

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

void loop() {
  WiFiClient client = server.available();
  
  if (client) {
    String request = "";
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        request += c;
        
        if (c == '\n') {
          // Parse HTTP request
          if (request.indexOf("GET /servo?angle=") >= 0) {
            int idx = request.indexOf("angle=") + 6;
            servoAngle = request.substring(idx, idx + 3).toInt();
            servoAngle = constrain(servoAngle, 0, 180);
            servo.write(servoAngle);
          }
          else if (request.indexOf("GET /motor?throttle=") >= 0) {
            int idx = request.indexOf("throttle=") + 9;
            throttle = request.substring(idx, idx + 4).toInt();
            throttle = constrain(throttle, 1000, 2000);
            esc.writeMicroseconds(throttle);
          }
          
          // Send HTML response
          client.println("HTTP/1.1 200 OK");
          client.println("Content-type:text/html");
          client.println();
          client.println("<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width'>");
          client.println("<style>body{font-family:Arial;text-align:center;margin:50px;}");
          client.println("input[type=range]{width:80%;}</style></head><body>");
          client.println("<h1>Arduino Control</h1>");
          client.println("<h2>Servo: " + String(servoAngle) + "°</h2>");
          client.println("<input type='range' min='0' max='180' value='" + String(servoAngle) + "' ");
          client.println("oninput=\"fetch('/servo?angle='+this.value)\">");
          client.println("<h2>Motor: " + String(throttle) + "μs</h2>");
          client.println("<input type='range' min='1000' max='2000' value='" + String(throttle) + "' ");
          client.println("oninput=\"fetch('/motor?throttle='+this.value)\">");
          client.println("</body></html>");
          break;
        }
      }
    }
    client.stop();
  }
}
