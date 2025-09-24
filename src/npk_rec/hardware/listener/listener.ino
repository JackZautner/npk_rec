#define LED_PIN    12   // Drives the LED
#define SENSE_PIN  13   // Reads the LED voltage

bool prevState = LOW;

void setup() {
  Serial.begin(115200);

  pinMode(LED_PIN, OUTPUT);
  pinMode(SENSE_PIN, INPUT);

  digitalWrite(LED_PIN, HIGH);  // turn LED on
}

void loop() {
  // Example: toggle LED every 2 seconds

  // Read LED state
  bool currentState = digitalRead(SENSE_PIN);

  // Figure out what the current and previous states are
  // and print accordingly.
  if (currentState == HIGH && prevState == LOW) {
    Serial.print("PING ");
    Serial.println(millis());
  }

  prevState = currentState;
  delay(2000);
}
