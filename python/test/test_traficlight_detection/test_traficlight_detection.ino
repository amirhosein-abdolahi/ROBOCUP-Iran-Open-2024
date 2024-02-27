int r = 2;
int y = 3;
int g = 4;


void setup() {
  pinMode(r, OUTPUT);
  pinMode(y, OUTPUT);
  pinMode(g, OUTPUT);
}

void loop() {
  digitalWrite(r, 1);
  delay(3000);
  digitalWrite(r, 0);

  digitalWrite(y, 1);
  delay(3000);
  digitalWrite(y, 0);

  digitalWrite(g, 1);
  delay(3000);
  digitalWrite(g, 0);
}
