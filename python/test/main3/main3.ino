// Include lib
#include <TM1637Display.h>
#include <Servo.h>
Servo myservo;

// Debuging functions
#define DEBUG_ARRAY(a) {for (int index = 0; index < sizeof(a) / sizeof(a[0]); index++)   {Serial.print(a[index]); Serial.print('\t');} Serial.println();};
#define DEBUG_COMMAND(a, index) {display.showNumberDec(a, false, 1, index);};

// Declared some variables
String command = "";
const int dataLength = 5;
int data[dataLength];
int motor, tunnel, park, intersection, steering;

// Motor pins
#define E 11
#define M 13

// Steering pins
#define RR 70
#define R 90
#define C 110
#define L 130
#define LL 160

// UltraSonic Pins
#define ECHO_L 23
#define TRIG_L 22
#define ECHO_C 25
#define TRIG_C 24
#define ECHO_R 27
#define TRIG_R 26
#define ECHO_P_R 29
#define TRIG_P_R 28

// Seven segment pins
#define CLK 3
#define DIO 2

// LED pins
#define LED1 20
#define LED2 21

// test
#define LED 40

// Create a display object of type TM1637Display
TM1637Display display = TM1637Display(CLK, DIO);

// Setup
void setup() {
  // Serial config
  Serial.begin(9600);
  Serial.setTimeout(5);

  // Motor pinmod
  pinMode(M, OUTPUT);
  pinMode(E, OUTPUT);

  // Servo attach
  myservo.attach(9);
  myservo.write(C);

  // UltraSonic
  pinMode(TRIG_L, OUTPUT);
  pinMode(ECHO_L, INPUT);
  pinMode(TRIG_C, OUTPUT);
  pinMode(ECHO_C, INPUT);
  pinMode(TRIG_R, OUTPUT);
  pinMode(ECHO_R, INPUT);
  pinMode(TRIG_P_R, INPUT);
  pinMode(ECHO_P_R, INPUT);

  // LEDs
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  digitalWrite(LED1, HIGH);
  digitalWrite(LED2, HIGH);

  // Set the seven segment brightness to 5 (0=dimmest 7=brightest)
  display.setBrightness(5);
  display.clear();
}

// Main loop
void loop() {
  
  // Get start time
  unsigned long start = millis(); // ==================================================

  // Check for obstacle
  if (obstacle()) {
    motion_fun(2, steering);
  } else {motion_fun(motor, steering);}

  // Check the serial
  if (Serial.available()) {
    // Read serial and split them
    command = Serial.readStringUntil('\n');
    for (int i = 0; i < dataLength ; i++) {
      data[i] = command.substring(i, i + 1).toInt();
    }
    // DEBUG_ARRAY(data);

    // Split data to {motor},{tunnel},{park},{intersection},{steering}
    motor = data[0];
    tunnel = data[1];
    park = data[2];
    intersection = data[3];
    steering = data[4];

    // Show command
    DEBUG_COMMAND(motor, 0);
    DEBUG_COMMAND(park, 1);
    DEBUG_COMMAND(intersection, 2);
    DEBUG_COMMAND(steering, 3);

    // Execute the commands
    if (tunnel != 0) lights_fun(tunnel);
    else if (intersection != 0) intersection_fun(intersection);
    else if (park != 0) parking_fun(park);
    else if ((motor != 0) || (steering != 0)) motion_fun(motor, steering);

    // Clean serial buffer
    Serial.flush();
  }

  // Get end time and show delay
  unsigned long end = millis(); // ==================================================
  int delay = end - start;
  // display.showNumberDec(delay);
}

// Function for ultrasonics
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

// Function for turn on/off lights
void lights_fun(int command) {
  switch (command) {
    case 1: // lighs ON
      digitalWrite(LED1, LOW);
      digitalWrite(LED2, LOW);
      break;

    case 2: // lights OFF
      digitalWrite(LED1, HIGH);
      digitalWrite(LED2, HIGH);
      break;
  }
}

// Function for parking
void parking_fun(int command) {
  switch (command) {
    // right side
    case 1:
      for (int i = 0; i<3; i++) {
        motion_fun(1, steering);
        delay(3000);
        motion_fun(2, steering);
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

// Function for turn left/right or go forward
void intersection_fun(int command) {
  switch (command) {
    case 1: // turn Right
      for (int i = 0; i < 150; i++) {
        if (obstacle()) {
        motion_fun(2, 1);
        i -= 1;
        } else {
          motion_fun(1, 1);
        }
          delay(10);
      }
      motion_fun(2, 3);
      Serial.flush();
      break;

    case 2: // center
      motion_fun(1, 3);
      delay(10000);
      motion_fun(2, 3);
      Serial.flush();
      break;

    case 3: // turn Left
      motion_fun(1, 3);
      delay(2000);
      motion_fun(1, 4);
      delay(9000);
      motion_fun(1, 5);
      delay(9000);
      motion_fun(2, 3);
      Serial.flush();
      break;
  }
}

// Function for controling motor and steering
void motion_fun(int motor_command, int steering_command) {
  // Execute motor command
  switch (motor_command) {
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

  // Execute steering command
  switch (steering_command) {
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

// Function for finding parking area
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