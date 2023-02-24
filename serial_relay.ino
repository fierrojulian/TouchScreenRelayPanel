int relay1Pin = 13;
int relay2Pin = 12;
int relay3Pin = 11;
int relay4Pin = 10;
int relay5Pin = 9;
int relay6Pin = 8;
int relay7Pin = 7;
int relay8Pin = 6;
int relay9Pin = 5;
int relay10Pin = 4;
int relay11Pin = 3;
int relay12Pin = 2;
int relay13Pin = 1;
int relay14Pin = 0;

void setup() {
  
  Serial.begin(9600);
  pinMode(relay1Pin, OUTPUT);
  digitalWrite(relay1Pin, HIGH);
  pinMode(relay2Pin, OUTPUT);
  digitalWrite(relay2Pin, HIGH);
  pinMode(relay3Pin, OUTPUT);
  digitalWrite(relay3Pin, HIGH);
  pinMode(relay4Pin, OUTPUT);
  digitalWrite(relay4Pin, HIGH);
  pinMode(relay5Pin, OUTPUT);
  digitalWrite(relay5Pin, HIGH);
  pinMode(relay6Pin, OUTPUT);
  digitalWrite(relay6Pin, HIGH);
  pinMode(relay7Pin, OUTPUT);
  digitalWrite(relay7Pin, HIGH);
  pinMode(relay8Pin, OUTPUT);
  digitalWrite(relay8Pin, HIGH);
  pinMode(relay9Pin, OUTPUT);
  digitalWrite(relay9Pin, HIGH);
  pinMode(relay10Pin, OUTPUT);
  digitalWrite(relay10Pin, HIGH);
  pinMode(relay11Pin, OUTPUT);
  digitalWrite(relay11Pin, HIGH);
  pinMode(relay12Pin, OUTPUT);
  digitalWrite(relay12Pin, HIGH);
  pinMode(relay13Pin, OUTPUT);
  digitalWrite(relay13Pin, HIGH);
  pinMode(relay14Pin, OUTPUT);
  digitalWrite(relay14Pin, HIGH);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == '0') {
      digitalWrite(relay1Pin, LOW);
    }
    else if (command == '1') {
      digitalWrite(relay1Pin, HIGH);
    }
    else if (command == '2') {
      digitalWrite(relay2Pin, LOW);
    }
    else if (command == '3') {
      digitalWrite(relay2Pin, HIGH);
    }
    else if (command == '4') {
      digitalWrite(relay3Pin, LOW);
    }
    else if (command == '5') {
      digitalWrite(relay3Pin, HIGH);
    }
    else if (command == '6') {
      digitalWrite(relay4Pin, LOW);
    }
    else if (command == '7') {
      digitalWrite(relay4Pin, HIGH);
    }
    else if (command == '8') {
      digitalWrite(relay5Pin, LOW);
    }
    else if (command == '9') {
      digitalWrite(relay5Pin, HIGH);
    }
    else if (command == 'A') {
      digitalWrite(relay6Pin, LOW);
    }
    else if (command == 'B') {
      digitalWrite(relay6Pin, HIGH);
    }
    else if (command == 'C') {
      digitalWrite(relay7Pin, LOW);
    }
    else if (command == 'D') {
      digitalWrite(relay7Pin, HIGH);
    }
    else if (command == 'E') {
      digitalWrite(relay8Pin, LOW);
    }
    else if (command == 'F') {
      digitalWrite(relay8Pin, HIGH);
    }
    else if (command == 'G') {
      digitalWrite(relay9Pin, LOW);
    }
    else if (command == 'H') {
      digitalWrite(relay9Pin, HIGH);
    }
    else if (command == 'I') {
      digitalWrite(relay10Pin, LOW);
    }
    else if (command == 'J') {
      digitalWrite(relay10Pin, HIGH);
    }
    else if (command == 'K') {
      digitalWrite(relay11Pin, LOW);
    }
    else if (command == 'L') {
      digitalWrite(relay11Pin, HIGH);
    }
    else if (command == 'M') {
      digitalWrite(relay12Pin, LOW);
    }
    else if (command == 'N') {
      digitalWrite(relay12Pin, HIGH);
    }
    else if (command == 'O') {
      digitalWrite(relay13Pin, LOW);
    }
    else if (command == 'P') {
      digitalWrite(relay13Pin, HIGH);
    }
    else if (command == 'Q') {
      digitalWrite(relay14Pin, LOW);
    }
    else if (command == 'R') {
      digitalWrite(relay14Pin, HIGH);
	}
	else {
	}
  }
}
