#ifndef DS1621_class_H
#define DS1621_class_H

#include <Arduino.h>
#include <Wire.h>

class DS1621 {
private:
    uint8_t deviceAddress;
    
    // Core I2C Wrappers that return transmission status codes
    uint8_t write_u8Command(uint8_t command);
    uint8_t write_u8Register(uint8_t reg, uint8_t data);

public:
    DS1621(uint8_t address);
    void begin();
    
    // Sensor operational functions
    uint8_t set_u8Config(bool oneShot);
    uint8_t start_u8Conversion();
    float Temperature_val();
};

#endif