
const int buttonPin = 2;
int lastButtonState = HIGH;

void setup() {
  pinMode(buttonPin, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  int buttonState = digitalRead(buttonPin);

  if (buttonState == LOW && lastButtonState == HIGH) {
    Serial.println("PRESSED");
    delay(30);
  }

  lastButtonState = buttonState;
}
