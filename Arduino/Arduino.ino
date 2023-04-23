#include <SoftwareSerial.h>

SoftwareSerial mySerial(6,5);

#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN         9
#define SS_PIN          10

MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  mySerial.begin(9600);
	Serial.begin(9600);
	while (!Serial);
	SPI.begin();
	mfrc522.PCD_Init();
	delay(4);
	mfrc522.PCD_DumpVersionToSerial();
	Serial.println(F("Scan PICC to see UID, SAK, type, and data blocks..."));
}

void loop() {
	if ( ! mfrc522.PICC_IsNewCardPresent()) {
		return;
	}

	if ( ! mfrc522.PICC_ReadCardSerial()) {
		return;
	}

	mySerial.println("AT+CMGF=1");   // 
  delay(1000);                      
  mySerial.println("AT+CMGS=\"+91\"\r"); 
  delay(1000);
  mySerial.println("rfid id - 12041297");
  delay(100);
  mySerial.println((char)26);
  delay(1000);
}
