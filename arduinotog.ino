int togout = 6;              // tog ausgabe auf D6
int togin = analogRead(A1);              // tog eingang auf A1
int volt = 0;
int immerpin = 5;

void setup() {
  pinMode(togout, OUTPUT);    // digitalpin 6 als output
  pinMode(togin, INPUT);     // analogpin A1 als input
  pinMode(immerpin, OUTPUT);
  analogWrite(immerpin, volt);
}

void loop() {
  if   (togin >= 983){ // ist der analog wert größergleich 893 (4.8V) dann pulse für 41°C
  digitalWrite(togout, HIGH); // sets the tog on
  delay(20);
  digitalWrite(togout, LOW);
  delay(23);
  digitalWrite(togout, HIGH);
  delay(24);
  digitalWrite(togout, LOW);
  delay(250);}
  else if   (togin < 983 and togin >= 939){ // ist der analoge wert kleiner als 983 und größergleich 939 dann pulse für 60 °C
  digitalWrite(togout, HIGH); // sets the tog on
  delay(20);
  digitalWrite(togout, LOW);
  delay(26);
  delayMicroseconds(250);
  digitalWrite(togout, HIGH);
  delay(27);
  digitalWrite(togout, LOW);
  delay(250);}
  else if   (togin < 939 and togin >= 915){ // 65
  digitalWrite(togout, HIGH); // sets the tog on
  delay(20);
  digitalWrite(togout, LOW);
  delay(27);
  digitalWrite(togout, HIGH);
  delay(27);
  delayMicroseconds(750);
  digitalWrite(togout, LOW);
  delay(250);}
  else if   (togin < 915 and togin >= 889){ // 70
  digitalWrite(togout, HIGH); // sets the tog on
  delay(20);
  digitalWrite(togout, LOW);
  delay(28);
  digitalWrite(togout, HIGH);
  delay(28);
  delayMicroseconds(250);
  digitalWrite(togout, LOW);
  delay(250);}
  else if   (togin < 889 and togin >= 863){ // 75
  digitalWrite(togout, HIGH); // sets the tog on
  delay(20);
  digitalWrite(togout, LOW);
  delay(28);
  delayMicroseconds(500);
  digitalWrite(togout, HIGH);
  delay(29);
  delayMicroseconds(250);
  digitalWrite(togout, LOW);
  delay(250);}
  else if   (togin < 863 and togin >= 839){ // 80
  digitalWrite(togout, HIGH); // sets the tog on
  delay(20);
  digitalWrite(togout, LOW);
  delay(29.25);
  digitalWrite(togout, HIGH);
  delay(30);
  digitalWrite(togout, LOW);
  delay(250);}
  else if   (togin < 839 and togin >= 815){ // 85
  digitalWrite(togout, HIGH); // sets the tog on
  delay(20);
  digitalWrite(togout, LOW);
  delay(30);
  delayMicroseconds(250);
  digitalWrite(togout, HIGH);
  delay(30);
  delayMicroseconds(750);
  digitalWrite(togout, LOW);
  delay(250);}
  else if   (togin < 815 and togin >= 782){ // 90
  digitalWrite(togout, HIGH); // sets the tog on
  delay(20);
  digitalWrite(togout, LOW);
  delay(31);
  digitalWrite(togout, HIGH);
  delay(31);
  delayMicroseconds(500);
  digitalWrite(togout, LOW);
  delay(250);}
  else if   (togin < 782 and togin >= 755){ // 95
  digitalWrite(togout, HIGH); // sets the tog on
  delay(20);
  digitalWrite(togout, LOW);
  delay(31);
  delayMicroseconds(750);
  digitalWrite(togout, HIGH);
  delay(32);
  delayMicroseconds(500);
  digitalWrite(togout, LOW);
  delay(250);}
  else if   (togin < 755 and togin >= 726){ // 100
  digitalWrite(togout, HIGH); // sets the tog on
  delay(20);
  digitalWrite(togout, LOW);
  delay(32);
  delayMicroseconds(500);
  digitalWrite(togout, HIGH);
  delay(33);
  delayMicroseconds(250);
  digitalWrite(togout, LOW);
  delay(250);}
  else if   (togin < 726 and togin >= 700){ // 105
  digitalWrite(togout, HIGH); // sets the tog on
  delay(20);
  digitalWrite(togout, LOW);
  delay(33.25);
  digitalWrite(togout, HIGH);
  delay(34);
  digitalWrite(togout, LOW);
  delay(250);}
  else if   (togin < 700 and togin >= 663){ // 110
  digitalWrite(togout, HIGH); // sets the tog on
  delay(20);
  digitalWrite(togout, LOW);
  delay(34);
  digitalWrite(togout, HIGH);
  delay(35);
  digitalWrite(togout, LOW);
  delay(250);}
  else if   (togin < 663 and togin >= 645){ // 115
  digitalWrite(togout, HIGH); // sets the tog on
  delay(20);
  digitalWrite(togout, LOW);
  delay(35);
  digitalWrite(togout, HIGH);
  delay(35.75);
  digitalWrite(togout, LOW);
  delay(250);}
  else if   (togin < 645 and togin >= 621){ // 120
  digitalWrite(togout, HIGH); // sets the tog on
  delay(20);
  digitalWrite(togout, LOW);
  delay(35.75);
  digitalWrite(togout, HIGH);
  delay(36.75);
  digitalWrite(togout, LOW);
  delay(250);}
  else if   (togin < 621 and togin >= 583){ // 125
  digitalWrite(togout, HIGH); // sets the tog on
  delay(20);
  digitalWrite(togout, LOW);
  delay(36.75);
  digitalWrite(togout, HIGH);
  delay(37.5);
  digitalWrite(togout, LOW);
  delay(250);}
  else if   (togin < 583 and togin >= 502){ // 130
  digitalWrite(togout, HIGH); // sets the tog on
  delay(20);
  digitalWrite(togout, LOW);
  delay(37.5);
  digitalWrite(togout, HIGH);
  delay(38.25);
  digitalWrite(togout, LOW);
  delay(250);}
  else if   (togin < 502 and togin >= 473){ // 135
  digitalWrite(togout, HIGH); // sets the tog on
  delay(20);
  digitalWrite(togout, LOW);
  delay(38.25);
  digitalWrite(togout, HIGH);
  delay(39.25);
  digitalWrite(togout, LOW);
  delay(250);}
  else if   (togin < 473 and togin >= 449){ // 140
  digitalWrite(togout, HIGH); // sets the tog on
  delay(20);
  digitalWrite(togout, LOW);
  delay(39);
  delayMicroseconds(250);
  digitalWrite(togout, HIGH);
  delay(40);
  digitalWrite(togout, LOW);
  delay(250);}
  else if   (togin < 449 and togin >= 414){ // 145
  digitalWrite(togout, HIGH); // sets the tog on
  delay(20);
  digitalWrite(togout, LOW);
  delay(40);
  digitalWrite(togout, HIGH);
  delay(40);
  delayMicroseconds(750);
  digitalWrite(togout, LOW);
  delay(250);}
  else if   (togin < 414 and togin >= 384){ // 150
  digitalWrite(togout, HIGH); // sets the tog on
  delay(20);
  digitalWrite(togout, LOW);
  delay(41);
  digitalWrite(togout, HIGH);
  delay(41);
  delayMicroseconds(750);
  digitalWrite(togout, LOW);
  delay(250);}
  else if   (togin < 384 and togin >= 359){ // 155
  digitalWrite(togout, HIGH); // sets the tog on
  delay(20);
  digitalWrite(togout, LOW);
  delay(41);
  delayMicroseconds(750);
  digitalWrite(togout, HIGH);
  delay(42);
  delayMicroseconds(750);
  digitalWrite(togout, LOW);
  delay(250);}
  else if   (togin < 359 and togin >= 332){ // 160
  digitalWrite(togout, HIGH); // sets the tog on
  delay(20);
  digitalWrite(togout, LOW);
  delay(42);
  delayMicroseconds(750);
  digitalWrite(togout, HIGH);
  delay(43);
  delayMicroseconds(500);
  digitalWrite(togout, LOW);
  delay(250);}
  else if   (togin < 332 and togin >= 323){ // 170
  digitalWrite(togout, HIGH); // sets the tog on
  delay(20);
  digitalWrite(togout, LOW);
  delay(44);
  delayMicroseconds(500);
  digitalWrite(togout, HIGH);
  delay(45);
  delayMicroseconds(250);
  digitalWrite(togout, LOW);
  delay(250);}
  else if   (togin < 323){ // 170
  digitalWrite(togout, HIGH); // sets the tog on
  delay(20);
  digitalWrite(togout, LOW);
  delay(44);
  delayMicroseconds(500);
  digitalWrite(togout, HIGH);
  delay(45);
  delayMicroseconds(250);
  digitalWrite(togout, LOW);
  delay(250);}

}
