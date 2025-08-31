#define TOG_OUT 6
#define TOG_IN A1
#define IMMER_PIN 5

// Map of delay times (ms) for each temperature level
const int DELAY_TIMES[] = {41, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110};
// Analog input thresholds for each temperature level. IMPORTANT: Must be sorted in descending order.
const int ANALOG_VALUES[] = {983, 939, 915, 889, 863, 839, 815, 782, 755, 726, 700, 663};
const int NUM_TEMP_LEVELS = sizeof(ANALOG_VALUES) / sizeof(ANALOG_VALUES[0]);

void setup() {
  pinMode(TOG_OUT, OUTPUT);
  pinMode(TOG_IN, INPUT);
  pinMode(IMMER_PIN, OUTPUT);
  // IMMER_PIN is set LOW (off). Use digitalWrite for clarity, since PWM is not used.
  digitalWrite(IMMER_PIN, LOW);
}

/*
  Reads the analog value from TOG_IN, which is assumed to be a temperature sensor or similar analog input.
  Determines the temperature level by comparing against ANALOG_VALUES.
  If a valid temperature level is found, outputs a specific pulse pattern to TOG_OUT.
*/
void loop() {
  int tog_in = analogRead(TOG_IN);

  // (Optional improvement) For noisy sensors, consider averaging several readings:
  // int tog_in = 0;
  // for (int i = 0; i < 8; i++) tog_in += analogRead(TOG_IN);
  // tog_in /= 8;

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
  delay(250); // Loop timing delay
}

/*
  Outputs a pulse pattern to TOG_OUT:
  - 20ms HIGH pulse
  - 'delay_time' ms LOW
  - ('delay_time'+1) ms HIGH pulse
*/
void pulsePattern(int delay_time) {
  digitalWrite(TOG_OUT, HIGH);
  delay(20);
  digitalWrite(TOG_OUT, LOW);
  delay(delay_time);
  digitalWrite(TOG_OUT, HIGH);
  delay(delay_time + 1); // Second pulse slightly longer
  digitalWrite(TOG_OUT, LOW);
}