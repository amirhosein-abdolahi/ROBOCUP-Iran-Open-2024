int i;

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
  delay(1000);
  digitalWrite(g, 0);

  for (i=0; i<255; i++){
    analogWrite(y, i);
    delay(10);
  }
  analogWrite(y, 0);

  digitalWrite(r, 1);
  delay(1000);
  digitalWrite(r, 0);
}
