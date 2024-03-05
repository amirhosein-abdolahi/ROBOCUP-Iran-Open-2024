const unsigned int TRIG_PIN1=23;
const unsigned int ECHO_PIN1=22;
const unsigned int TRIG_PIN2=25;
const unsigned int ECHO_PIN2=24;
const  unsigned int BAUD_RATE=9600;
const int LED = 2;

void setup() {
  pinMode(TRIG_PIN1, OUTPUT);
  pinMode(ECHO_PIN1, INPUT);
  pinMode(TRIG_PIN2, OUTPUT);
  pinMode(ECHO_PIN2, INPUT);
  pinMode(LED, OUTPUT);
  Serial.begin(BAUD_RATE);
}

void loop()  {
  digitalWrite(TRIG_PIN1, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN1,  HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN1, LOW);

  const unsigned long duration1= pulseIn(ECHO_PIN1, HIGH);

  digitalWrite(TRIG_PIN2, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN2,  HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN2, LOW);

  const unsigned long duration2= pulseIn(ECHO_PIN2, HIGH);

 int distance1= duration1/29/2;
 int distance2= duration2/29/2;
 
  if(duration1==0 and duration2==0){
   Serial.println("Warning: no pulse from sensor");
   }  
  else{
      Serial.print("distance1: ");
      Serial.print(distance1);
      Serial.println(" cm");

      Serial.print("distance2: ");
      Serial.print(distance2);
      Serial.println(" cm");

      if (distance1 < 30 or distance2 < 30) {
        digitalWrite(LED, HIGH);
      }
      else {
      digitalWrite(LED, LOW);
      }
  }
 delay(100);
 }