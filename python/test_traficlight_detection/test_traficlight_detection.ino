int r = 2;
int y = 3;
int g = 4;


void setup() {
  pinMode(r, OUTPUT);
  pinMode(y, OUTPUT);
  pinMode(g, OUTPUT);
}

void loop() {
  digitalWrite(g, 1);
  delay(5000);
  digitalWrite(g, 0);

  digitalWrite(y, 1);
  delay(1000);
  digitalWrite(y, 0);

  digitalWrite(r, 1);
  delay(5000);
  digitalWrite(r, 0);
}
