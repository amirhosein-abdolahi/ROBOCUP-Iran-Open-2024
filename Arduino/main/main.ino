#include <Servo.h>

Servo myservo;

// unsigned long duration_L, duration_R;

const unsigned int ECHO_L=22;
const unsigned int TRIG_L=23;
const unsigned int ECHO_R=26;
const unsigned int TRIG_R=27;

// M => direction - E => intensity
int E1 = 10;  
int M1 = 12;
int E2 =11;
int M2 = 13;

void setup() {

  pinMode(M1, OUTPUT);
  pinMode(M2, OUTPUT);
  pinMode(E1, OUTPUT);
  pinMode(E2, OUTPUT);

  pinMode(TRIG_L, OUTPUT);
  pinMode(ECHO_L, INPUT);
  pinMode(TRIG_R, OUTPUT);
  pinMode(ECHO_R, INPUT);

  myservo.attach(9);

  digitalWrite(M1, HIGH);
  digitalWrite(E1, HIGH);

  Serial.begin(9600);
}

void loop() {

  digitalWrite(TRIG_L, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_L,  HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_L, LOW);
  const unsigned long duration_L = pulseIn(ECHO_L, HIGH);

  delay(10);

  digitalWrite(TRIG_R, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_R,  HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_R, LOW);
  const unsigned long duration_R = pulseIn(ECHO_R, HIGH);

  Serial.println("duration_L: "+String(duration_L)+"  duration_R: "+String(duration_R));

  // myservo.write(90);
  // delay(500);
  // myservo.write(135);
  // delay(500);
  // myservo.write(90);
  // delay(500);
  // myservo.write(45);
  // delay(500);

  delay(100);
}
