#include <Servo.h>
Servo myservo;

String steering_state = "center";

int E = 10;
int M = 12;

int delay_go_right = 140;
int delay_back_right = 140;

int delay_go_left = 240;
int delay_back_left = 240;

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

      // control steering
      // go to center
      if (steering == "center") {
        if (steering_state == "right") {
          myservo.write(180);
          delay(delay_back_right);
          myservo.write(90);
          steering_state = "center";
        } 
        else if (steering_state == "left") {
          myservo.write(0);
          delay(delay_back_left);
          myservo.write(90);
          steering_state = "center";
        }
      }

      // go to right
      else if (steering == "right") {
        if (steering_state == "center") {
          myservo.write(0);
          delay(delay_go_right);
          myservo.write(90);
          steering_state = "right";
        } 
        else if (steering_state == "left") {
          myservo.write(0);
          delay(delay_back_left + delay_go_right);
          myservo.write(90);
          steering_state = "right";
        }
      }

      // go to left
      else if (steering == "left") {
        if (steering_state == "center") {
          myservo.write(180);
          delay(delay_go_left);
          myservo.write(90);
          steering_state = "left";
        } 
        else if (steering_state == "right") {
          myservo.write(180);
          delay(delay_back_right + delay_go_left);
          myservo.write(90);
          steering_state = "left";
        }
      }

      // control motor
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
