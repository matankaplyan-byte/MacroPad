
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define OLED_ADDRESS 0x3C

Adafruit_SSD1306 display(
  SCREEN_WIDTH,
  SCREEN_HEIGHT,
  &Wire,
  OLED_RESET
);

const int buttonPin = 6;

int lastReading = HIGH;
int stableButtonState = HIGH;

unsigned long lastDebounceTime = 0;
const unsigned long debounceDelay = 40;

String currentLayout = "Everyday";

void showLayout() {
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);

  display.setTextSize(1);
  display.setCursor(0, 0);
  display.println("MACROPAD");

  display.drawLine(0, 12, 127, 12, SSD1306_WHITE);

  display.setTextSize(1);
  display.setCursor(0, 28);
  display.println(currentLayout);

  display.display();
}

void setup() {
  pinMode(buttonPin, INPUT_PULLUP);

  Serial.begin(9600);
  Serial.setTimeout(50);

  Wire.begin();

  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDRESS)) {
    Serial.println("OLED ERROR");
    while (true) {
      delay(100);
    }
  }

  showLayout();
  Serial.println("READY");
}

void loop() {
  int reading = digitalRead(buttonPin);

  if (reading != lastReading) {
    lastDebounceTime = millis();
  }

  if (millis() - lastDebounceTime > debounceDelay) {
    if (reading != stableButtonState) {
      stableButtonState = reading;

      if (stableButtonState == LOW) {
        Serial.println("PRESSED");
      }
    }
  }

  lastReading = reading;

  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command.startsWith("LAYOUT:")) {
      currentLayout = command.substring(7);
      showLayout();
    }
  }
}
