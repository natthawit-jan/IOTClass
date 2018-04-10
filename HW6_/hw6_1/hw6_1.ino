
int c = 3;
int d  =4;
int e= 5;
int f = 6;

void setup() {
  pinMode(c, INPUT_PULLUP);
  pinMode(d, INPUT_PULLUP);
  pinMode(e, INPUT_PULLUP);
  pinMode(f, INPUT_PULLUP);
  Serial.begin(9600);
  
  
  // put your setup code here, to run once:
  

}

boolean getStatus(int switch_){
  if (digitalRead(switch_) == 0){
    return true;
  }
  else return false;
  
}

void loop() {
  boolean cIsPressed = getStatus(c);
  boolean dIsPressed = getStatus(d);
  boolean eIsPressed = getStatus(e);
  boolean fIsPressed = getStatus(f);

  if (cIsPressed) {
    Serial.println("0");
    delay(170);
  }
  else if(dIsPressed) {
    Serial.println("1");
    delay(170);
  }
  else if(eIsPressed) {
    Serial.println("2");
    delay(170);
  }
  else if(fIsPressed) {
    Serial.println("3"); 
    delay(170);
  }

  
  // put your main code here, to run repeatedly:

}
