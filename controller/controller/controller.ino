#include <Servo.h>
Servo myservo;

int E = 10;
int M = 12;

void setup() {  
  Serial.begin(9600);

  pinMode(E, OUTPUT);
  pinMode(M, OUTPUT);

  myservo.attach(9);
  myservo.write(90);

  delay(1000);
}

void loop() {
  if (Serial.available() > 0) {
    String value = Serial.readStringUntil('\n');
    int comma_index = value.indexOf(',');

    if (comma_index != -1) {
      String steering = value.substring(0, comma_index);
      String motor = value.substring(comma_index + 1);

      // control steering ================
      // go to center
      if (steering == "center") {
        myservo.write(90);
      }

      // go to right
      else if (steering == "right") {
        myservo.write(110);
      }

      // go to left
      else if (steering == "left") {
        myservo.write(70);
      }

      // go more to right
      else if (steering == "right_right") {
        myservo.write(130);
      }

      // go more to left
      else if (steering == "left_left") {
        myservo.write(50);
      }

      // control motor ===================
      // stop motor
      if (motor == "stop") {
        analogWrite(E, 0);
        digitalWrite(M, LOW);
      }

      // forward
      else if (motor == "forward") {
        analogWrite(E, 255);
        digitalWrite(M, HIGH);
      }

      // backward
      else if (motor == "backward") {
        analogWrite(E, 255);
        digitalWrite(M, LOW);
      }
    }
  }
}
