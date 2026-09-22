#include <Arduino.h>
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

void delay_1ms() {
    TCNT0 = 0; 
    // Wait until the Compare Match flag (OCF0) is set
    while ((TIFR & (1 << OCF0)) == 0); 
    TIFR |= (1 << OCF0); // Clear the OCF0 flag
}

int main(void) {
    DDRB |= (1 << PB0); // led pin as output
    PORTB &= ~(1 << PB0);
    DDRD &= ~(1 << PD2);
    // Enable internal pull-up resistor on PD2 to ensure a stable HIGH when unpressed
    PORTD |= (1 << PD2);

    //  falling edge
    MCUCR |= (1 << ISC01);
    MCUCR &= ~(1 << ISC00);
    GICR |= (1 << INT0);

    // Enable the global interrupt 
    sei();

    while (1) {
        
    }
    return 0;
}

ISR(INT0_vect) {
    // Every time the button is pressed, toggle the LED[cite: 1]
    PORTB ^= (1 << PB0);
}