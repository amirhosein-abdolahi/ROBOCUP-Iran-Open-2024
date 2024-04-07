

void obstacle_check() {

  // Left Module
  digitalWrite(TRIG_L, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_L,  HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_L, LOW);
  const unsigned long duration_L = pulseIn(ECHO_L, HIGH);

  delay(10);

  // Center Module
  digitalWrite(TRIG_C, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_C,  HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_C, LOW);
  const unsigned long duration_C = pulseIn(ECHO_C, HIGH);

  delay(10);

  // Right Module
  digitalWrite(TRIG_R, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_R,  HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_R, LOW);
  const unsigned long duration_R = pulseIn(ECHO_R, HIGH);

  // Stop if obstacle found
  if (duration_L < 1000 || duration_C < 1000 || duration_R < 1000) {
    digitalWrite(E, LOW);
    // tone(buzzer, 800);
    delay(100);
  }
  else { // Set motor's last status again
    motor(motor_);
  }
}