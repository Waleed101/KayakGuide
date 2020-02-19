#include <SPI.h>
#include <RF24.h>

RF24 radio(9, 10);
int right = 6, left = 5;

void setup() {
  pinMode(right, OUTPUT);
  pinMode(left, OUTPUT);
  while(!Serial);
  Serial.begin(9600);
  
  radio.begin();
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(0x76);
  const uint64_t pipe = 0xE8E8F0F0E1LL;
  radio.openReadingPipe(1, pipe);
  
  radio.enableDynamicPayloads();
  radio.powerUp();
}

void loop() {
  radio.startListening();
  Serial.println("Starting loop...");
  Serial.println("Radio On...");
  char recievedMessage[32] = {0};
  if(radio.available()) {
    radio.read(recievedMessage, sizeof(recievedMessage));
    Serial.println(recievedMessage);
    
    String stringMessage(recievedMessage);
    Serial.println(stringMessage);
    if(stringMessage == "RIGHT") {
      digitalWrite(right, HIGH);
      digitalWrite(left, LOW);
    }
    else if(stringMessage == "LEFT") {
      digitalWrite(right, LOW);
      digitalWrite(left, HIGH);
    }
    else if(stringMessage == "CENTERED") {
      digitalWrite(right, LOW);
      digitalWrite(left, LOW);
    }
  }
  
  delay(100);
}
