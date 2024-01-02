int r = 3;
int y = 5;
int g = 6;


void setup() {
  pinMode(r, OUTPUT);
  pinMode(y, OUTPUT);
  pinMode(g, OUTPUT);
}

void loop() {
  analogWrite(g, 5);
  delay(1000);
  analogWrite(g, 0);

  analogWrite(y, 20);
  delay(1000);
  analogWrite(y, 0);

  analogWrite(r, 20);
  delay(1000);
  analogWrite(r, 0);
}
