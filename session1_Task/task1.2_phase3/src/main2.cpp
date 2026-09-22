#include <Arduino.h>
#include <avr/io.h>
#include <util/delay.h>

void delay_1ms() {
    TCNT0 = 0; 
    // Wait until the Compare Match flag (OCF0) is set
    while ((TIFR & (1 << OCF0)) == 0); 
    TIFR |= (1 << OCF0); // Clear the OCF0 flag
}

 int main(void) {
    DDRB |= (1 << PB3);
    PORTB &= ~(1 << PB3); // led off
    // fast pwm mode with prescaler 8 & frequency = 8MHz/(8*256) = 3906.25Hz
    TCCR0 = (1 << WGM01) | (1 << WGM00) | (1 << COM01) | (1 << CS01);

    OCR0 = 63; // Start with a 25% duty cycle

    while (1) {

        for (uint8_t duty = 63; duty < 255; duty++) {
            OCR0 = duty;
            _delay_ms(15); 
        }
        
        OCR0 = 63;
        _delay_ms(500); // Hold at 25% before repeating
    }
    return 0;
}