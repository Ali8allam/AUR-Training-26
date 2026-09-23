#include "DS1621_class.h"

// I2C Commands
#define CMD_READ_TEMP  0xAA
#define CMD_START_CONVERSION 0xEE
#define CMD_ACCESS_CFG 0xAC

DS1621::DS1621(uint8_t address) {
    deviceAddress = address;
}

void DS1621::begin() {
    Wire.begin();
}

uint8_t DS1621::write_u8Command(uint8_t command) {
    //begin
    Wire.beginTransmission(deviceAddress);
    //send command
    Wire.write(command);
    return Wire.endTransmission(); // return 0 if success, >0 for NACK errors
}

// Wrapper for writing data to a specific register
uint8_t DS1621::write_u8Register(uint8_t reg, uint8_t data) {
    Wire.beginTransmission(deviceAddress);
    Wire.write(reg);
    Wire.write(data);
    return Wire.endTransmission();
}




uint8_t DS1621::set_u8Config(bool oneShot) {
    // DS1621 Config: LSB (bit 0) is the 1SHOT bit. 
    // 1 = One-Shot mode, 0 = Continuous mode.
    uint8_t configValue = oneShot ? 0x01 : 0x00;
    return write_u8Register(CMD_ACCESS_CFG, configValue);
}

uint8_t DS1621::start_u8Conversion() {
    return write_u8Command(CMD_START_CONVERSION);
}

float DS1621::Temperature_val() {
    // 1. Set the register pointer to the Temperature register
    Wire.beginTransmission(deviceAddress);
    Wire.write(CMD_READ_TEMP);
    
    // 2. End transmission with Repeated Start (false prevents STOP condition)
    uint8_t status = Wire.endTransmission(false);
    
    if (status != 0) {
        Serial.println("Error: I2C NACK during Read Setup");
        return -999.0; // Error indicator
    }

    // 3. Request the 2-byte payload
    Wire.requestFrom((int)deviceAddress, 2);
    
    if (Wire.available() == 2) {
        // Parse the MSB (Integer portion) as a signed 8-bit integer
        int8_t msb = Wire.read(); // first call for firstbyte
        
        // Parse the LSB (Fractional portion). 
        // Bit 7 indicates 0.5 degrees.
        uint8_t lsb = Wire.read(); 
        
        float temperature = (float)msb;
        if (lsb & 0x80) { // Check if the Most Significant Bit of LSB is 1
            temperature += 0.5;
        }
        return temperature;
    }
    
    return -999.0; // Return error if 2 bytes weren't received
}