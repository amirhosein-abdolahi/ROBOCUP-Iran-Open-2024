int i;

// Define CNC pins
// enable pin
const int en=8;
// X axis
const int stepX = 2; //X.STEP
const int dirX = 5; // X.DIR
// Turn wheel
const int stepY = 3; //Y.STEP
const int dirY = 6; // Y.DIR
// Go forward and backward
const int stepZ = 4; //Z.STEP
const int dirZ = 7; // Z.DIR

int dirPin = dirZ;
int stepPin = stepZ;

// defining speeds
int turnSpeed = 1200;
int goSpeed = 900;

// how much to go
int turn = 60;
int go = 300;

void setup() {

  // Enable CNC shield
 	pinMode(en, OUTPUT);
 	digitalWrite(en, LOW);

  // Set pin modes
 	for (int pin=2; pin<=7; pin++){
    pinMode(pin, OUTPUT);
  }
}

void loop() {

  // Go forward

  digitalWrite(dirPin, HIGH);

  for(i=0; i<go; i++){
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(goSpeed);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(goSpeed);
  }

  delay(500);

  // turn wheel
  digitalWrite(dirPin, HIGH);

  for(i = 0; i < turn; i++){
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(turnSpeed);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(turnSpeed);

  }

  delay(500);

  digitalWrite(dirPin, LOW);
  
  for(i = 0; i < turn; i++){
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(turnSpeed);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(turnSpeed);
  }

  delay(500);
}

