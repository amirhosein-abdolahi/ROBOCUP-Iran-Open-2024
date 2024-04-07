#include <Servo.h>
#include <LiquidCrystal.h>

// Debugger
#define DEBUG true

// LiquidCrystal lcd(2, 3, 4, 5, 6, 7);
// LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
// LiquidCrystal lcd(RS(D), E(PWM), D4(PWM), D5(PWM), D6(D), D7(D));

// Defining values
Servo myservo;
String command;
int stop_, tunnel_, park_, intersection_, motor_, steering_;

// UltraSonic Pins
#define ECHO_L 23
#define TRIG_L 22
#define ECHO_C 25
#define TRIG_C 24
#define ECHO_R 27
#define TRIG_R 26
#define ECHO_P_R 29
#define TRIG_P_R 28

// Motor Pins
// M => direction - E => intensity
#define E 11
#define M 13

// Steering
#define RR 70
#define R 90
#define C 105
#define L 130
#define LL 160

#define LED 40

void setup() {

  // Motor
  pinMode(M, OUTPUT);
  pinMode(E, OUTPUT);

  // UltraSonic
  pinMode(TRIG_L, OUTPUT);
  pinMode(ECHO_L, INPUT);
  pinMode(TRIG_C, OUTPUT);
  pinMode(ECHO_C, INPUT);
  pinMode(TRIG_R, OUTPUT);
  pinMode(ECHO_R, INPUT);
  pinMode(TRIG_P_R, INPUT);
  pinMode(ECHO_P_R, INPUT);

  pinMode(LED, OUTPUT);

  // Servo
  myservo.attach(9);
  myservo.write(C);

  // Serial
  Serial.begin(9600);

  // // LCD
  // lcd.begin(16, 2);
  // lcd.clear();
  // lcd.print("Hello World!");

  // digitalWrite(M, HIGH);
  // digitalWrite(E, HIGH);
  // myservo.write(135);

  if (DEBUG) Serial.println("Debug ON!");
}

void loop() {

  // Check for obstacle
  if (obstacle()) {
    motor(2);
  } else {
    motor(motor_);
  }

  // Commander
  while (Serial.available()) {
    if (DEBUG) Serial.println("Serial.available()");
    commander();
  }

  delay(1);
}



bool obstacle() {

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
    // digitalWrite(E, LOW);
    // tone(buzzer, 800);
    // delay(100);
    return true;
  }
  else { // Set motor's last status again
    return false;
  }
}


void commander() {

  // Read command
  // (motor)(tunnel)(park)(intersection)(steering)
  command = Serial.readStringUntil("\n");
  if (DEBUG) Serial.println("command: "+command);
  // lcd.clear();
  // lcd.print(command);

  // Parameters
  motor_ = command.substring(0, 1).toInt();
  tunnel_ = command.substring(1, 2).toInt();
  park_ = command.substring(2, 3).toInt();
  intersection_ = command.substring(3, 4).toInt();
  steering_ = command.substring(4, 5).toInt();

  if (DEBUG) Serial.println("motor: "+String(motor_)+" | tunnel: "+String(tunnel_)+" | park: "+String(park_)+" | intersection: "+String(intersection_)+" | steering: "+String(steering_));

  // Call the action
  if (motor_ != 0) motor(motor_);
  else if (tunnel_ != 0) tunnel(tunnel_);
  else if (park_ != 0) park(park_);
  else if (intersection_ != 0) intersection(intersection_);
  else if (steering_ != 0) steering(steering_);

  Serial.flush();
}

void motor(int c) {

  switch (c) {

    case 1: // forward
      digitalWrite(M, HIGH);
      digitalWrite(E, HIGH);
      break;

    case 2: // stop
      digitalWrite(M, HIGH);
      digitalWrite(E, LOW);
      break;

    case 3: // backward
      digitalWrite(M, LOW);
      digitalWrite(E, HIGH);
      break;
  }
}

void tunnel(int c) {

  switch (c) {
  
    case 1: // lighs ON
      digitalWrite(52, HIGH);
      digitalWrite(53, HIGH);
      break;

    case 2: // lights OFF
      digitalWrite(52, LOW);
      digitalWrite(53, LOW);
      break;
  }
}

void park(int c) {

  switch (c) {
  
    // right side
    case 1:

      for (int i = 0; i<3; i++) {
        motor(1);
        delay(3000);
        motor(2);
        
        if (park_check(1)) {
          digitalWrite(LED, HIGH);
          delay(200);
          digitalWrite(LED, LOW);
          delay(100);
          digitalWrite(LED, HIGH);
          delay(200);
          digitalWrite(LED, LOW);
          break;
        }
        digitalWrite(LED, HIGH);
        delay(200);
        digitalWrite(LED, LOW);
      }
      digitalWrite(LED, LOW);
      break;

    // left side
    case 2:

      break;
  }
}

void intersection(int c) {

  switch (c) {
    
    case 1: // turn Right

      myservo.write(RR);
      for (int i = 0; i < 300; i++) {
        if (obstacle()) {
        motor(2);
        i -= 1;
      } else {
        motor(1);
      }
        delay(10);
      }
      myservo.write(C);
      Serial.flush();
      break;

    case 2: // center
      myservo.write(C);
      break;

    case 3: // turn Left
      motor(1);
      myservo.write(C);
      delay(2000);
      myservo.write(L);
      delay(9000);
      myservo.write(LL);
      delay(9000);
      myservo.write(C);
      Serial.flush();
      break;
  }
}

void steering(int c) {

  switch (c) {

    case 1: // RR
      myservo.write(RR);
      break;

    case 2: // R
      myservo.write(R);
      break;

    case 3: // C
      myservo.write(C);
      break;

    case 4: // L
      myservo.write(L);
      break;

    case 5: // LL
      myservo.write(LL);
      break;
  }
}


bool park_check(int side) {

  switch (side) {
  
    case 1:

      digitalWrite(TRIG_C, LOW);
      delayMicroseconds(2);
      digitalWrite(TRIG_C,  HIGH);
      delayMicroseconds(10);
      digitalWrite(TRIG_C, LOW);
      const unsigned long duration_C = pulseIn(ECHO_C, HIGH);

      Serial.println(duration_C);

      if (duration_C < 400) {
        return false;
      } else {
        return true;
      }

      break;
  }
}