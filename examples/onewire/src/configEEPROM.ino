#include <Tli4970.h>

// Tli4970 Object
Tli4970 Tli4970CurrentSensor = Tli4970();

// the setup function runs once when you press reset or power the board
void setup() {
  Serial.begin(9600);
  while(!Serial);
  
  // Use default SPI for communication with the Tli4970
  Tli4970CurrentSensor.begin();
  // Use custom SPI
  //Tli4970CurrentSensor.begin(SPI2, (uint8_t)96u, (uint8_t)71u, (uint8_t)97u);
}

// the loop function runs over and over again forever
void loop() {
	Tli4970CurrentSensor.abortConfiguration();
	Tli4970CurrentSensor.startConfiguration();
	
	Serial.print("original: ");
	Serial.println(Tli4970CurrentSensor.getEepromBits(Tli4970CurrentSensor.GAIN));
	Tli4970CurrentSensor.setEepromBits(Tli4970CurrentSensor.GAIN, 45);
	Serial.print("modified: ");
	Serial.println(Tli4970CurrentSensor.getEepromBits(Tli4970CurrentSensor.GAIN));

	delay(500);
}