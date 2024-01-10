#include <Servo.h>

Servo servoMotor;

void setup() {
  Serial.begin(9600);
  servoMotor.attach(9);  // Attach the servo to pin 9
}

void loop() {
  if (Serial.available() > 0) {
    String angle = Serial.readStringUntil('\n');
    // angle = constrain(angle, 0, 180);  // Limit the angle between 0 and 180
    servoMotor.write(angle.toInt());
  }
}
