int r = 2;
int y = 3;
int g = 4;


void setup() {
  Serial.begin(9600);
  pinMode(r, OUTPUT);
  pinMode(y, OUTPUT);
  pinMode(g, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');

    if (data == "Turn left") {
      digitalWrite(y, 0);
      digitalWrite(r, 0);
      digitalWrite(g, 1);
    }
      
    else if (data == "Go forward") {
      digitalWrite(g, 0);
      digitalWrite(r, 0);
      digitalWrite(y, 1);
    }

    else if (data == "Turn right") {
      digitalWrite(g, 0);
      digitalWrite(y, 0);
      digitalWrite(r, 1);
    }
    
    else {
      digitalWrite(g, 0);
      digitalWrite(y, 0);
      digitalWrite(r, 0);
    }
  }
}
