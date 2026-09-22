#include <Arduino.h>
#include <avr/io.h>

void delay_1ms() {
    TCNT0 = 0; 
    // Wait until the Compare Match flag (OCF0) is set
    while ((TIFR & (1 << OCF0)) == 0); 
    TIFR |= (1 << OCF0); // Clear the OCF0 flag
}

 int main(void) {
    DDRB |= (1 << PB0);
    PORTB &= ~(1 << PB0); // led off
    // Configure timer0 in CTC mode with Prescaler 64
    TCCR0 = (1 << WGM01) | (1 << CS01) | (1 << CS00);
    OCR0 = 124; 

    while (1) {
        for (int i = 0; i < 500; i++) {
            delay_1ms();
        }
        PORTB ^= (1 << PB0); // Toggle the LED on PB0
    }
    return 0;
}