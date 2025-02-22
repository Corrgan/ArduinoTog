#define TOG_OUT 6
#define TOG_IN A1
#define IMMER_PIN 5

const int DELAY_TIMES[] = {41, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110};
const int ANALOG_VALUES[] = {983, 939, 915, 889, 863, 839, 815, 782, 755, 726, 700, 663};
const int NUM_TEMP_LEVELS = sizeof(ANALOG_VALUES) / sizeof(ANALOG_VALUES[0]);

void setup() {
  pinMode(TOG_OUT, OUTPUT);
  pinMode(TOG_IN, INPUT);
  pinMode(IMMER_PIN, OUTPUT);
  analogWrite(IMMER_PIN, 0);
}

void loop() {
  int tog_in = analogRead(TOG_IN);
  int temp_level = -1;
  for (int i = 0; i < NUM_TEMP_LEVELS; i++) {
    if (tog_in >= ANALOG_VALUES[i]) {
      temp_level = i;
      break;
    }
  }
  if (temp_level != -1) {
    pulsePattern(DELAY_TIMES[temp_level]);
  } else {
    digitalWrite(TOG_OUT, LOW);
  }
  delay(250); // Add a delay to match the original code's loop timing
}

void pulsePattern(int delay_time) {
  digitalWrite(TOG_OUT, HIGH);
  delay(20);
  digitalWrite(TOG_OUT, LOW);
  delay(delay_time);
  digitalWrite(TOG_OUT, HIGH);
  delay(delay_time + 1); // Assuming the second pulse is slightly longer
  digitalWrite(TOG_OUT, LOW);
}
