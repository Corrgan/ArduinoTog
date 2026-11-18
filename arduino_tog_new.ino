#define TOG_OUT 6
#define TOG_IN A1
#define IMMER_PIN 5

// Temperature levels (°C), only for reference: the dash reads the pulse timing below
const int TEMPS[] = {41, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 170};
// Analog input thresholds for each temperature level. IMPORTANT: Must be sorted in descending order.
// The last one is 0, so an unknown or missing sensor falls back to 170 °C.
const int ANALOG_VALUES[] = {983, 939, 915, 889, 863, 839, 815, 782, 755, 726, 700, 663, 645, 621, 583, 502, 473, 449, 414, 384, 359, 332, 0};
// Pulse timing (microseconds) for each level: LOW time after the 20 ms start pulse, then HIGH time
const unsigned int LOW_US[]  = {23000, 26250, 27000, 28000, 28500, 29250, 30250, 31000, 31750, 32500, 33250, 34000, 35000, 35750, 36750, 37500, 38250, 39250, 40000, 41000, 41750, 42750, 44500};
const unsigned int HIGH_US[] = {24000, 27000, 27750, 28250, 29250, 30000, 30750, 31500, 32500, 33250, 34000, 35000, 35750, 36750, 37500, 38250, 39250, 40000, 40750, 41750, 42750, 43500, 45250};
const int NUM_TEMP_LEVELS = sizeof(ANALOG_VALUES) / sizeof(ANALOG_VALUES[0]);
const int NUM_READINGS = 8; // averaged per loop against sensor noise

void setup() {
  pinMode(TOG_OUT, OUTPUT);
  pinMode(TOG_IN, INPUT);
  pinMode(IMMER_PIN, OUTPUT);
  // IMMER_PIN is set LOW (off). Use digitalWrite for clarity, since PWM is not used.
  digitalWrite(IMMER_PIN, LOW);
}

/*
  Reads the oil temperature sensor on TOG_IN (averaged), finds its level
  in ANALOG_VALUES and outputs the matching pulse pattern on TOG_OUT.
*/
void loop() {
  long sum = 0;
  for (int i = 0; i < NUM_READINGS; i++) sum += analogRead(TOG_IN);
  int tog_in = sum / NUM_READINGS;

  int temp_level = NUM_TEMP_LEVELS - 1;
  for (int i = 0; i < NUM_TEMP_LEVELS; i++) {
    if (tog_in >= ANALOG_VALUES[i]) {
      temp_level = i;
      break;
    }
  }
  pulsePattern(LOW_US[temp_level], HIGH_US[temp_level]);
  delay(250); // Loop timing delay
}

// delayMicroseconds() is only accurate up to ~16 ms, so wait the full milliseconds first
void waitMicros(unsigned int us) {
  delay(us / 1000);
  delayMicroseconds(us % 1000);
}

/*
  Outputs a pulse pattern to TOG_OUT:
  - 20ms HIGH pulse
  - 'low_us' LOW
  - 'high_us' HIGH pulse
*/
void pulsePattern(unsigned int low_us, unsigned int high_us) {
  digitalWrite(TOG_OUT, HIGH);
  delay(20);
  digitalWrite(TOG_OUT, LOW);
  waitMicros(low_us);
  digitalWrite(TOG_OUT, HIGH);
  waitMicros(high_us);
  digitalWrite(TOG_OUT, LOW);
}
