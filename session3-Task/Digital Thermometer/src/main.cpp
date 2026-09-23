#include <Arduino.h>
#include "DS1621_class.h"

// Instantiate the sensor object with the grounded A0-A2 address
DS1621 tempSensor(0x48); 

void setup() {
    Serial.begin(9600);
    Serial.println("Initializing DS1621...");
    
    tempSensor.begin();
    
    // Set to continuous conversion mode (oneShot = false)
    uint8_t configStatus = tempSensor.set_u8Config(false);
    if (configStatus != 0) {
        Serial.print("Failed to configure sensor. I2C Error Code: ");
        Serial.println(configStatus);
        while(1); // Halt execution on failure
    }
    
    // Initiate the continuous internal conversions
    uint8_t startStatus = tempSensor.start_u8Conversion();
    if (startStatus != 0) {
        Serial.print("Failed to start conversion. I2C Error Code: ");
        Serial.println(startStatus);
        while(1);
    }
    
    Serial.println("DS1621 Initialized Successfully.");
}

void loop() {
    float currentTemp = tempSensor.Temperature_val();
    
    if (currentTemp != -999.0) {
        Serial.print("Current Temperature: ");
        Serial.print(currentTemp);
        Serial.println(" C");
    } else {
        Serial.println("Failed to read temperature data.");
    }
    
    delay(1000); // Wait 1 second between reads
}