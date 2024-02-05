#include <stdio.h>
#include "pico/stdlib.h"
#include "pico/time.h"

#define LED_PIN 22

bool repeating_timer_callback(struct repeating_timer *t) {
    gpio_xor_mask(1u << LED_PIN);
    return true;
}

int main() {

    stdio_init_all();

    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);

    struct repeating_timer timer;
    add_repeating_timer_us(-200000, repeating_timer_callback, NULL, &timer);

    while(1) {
    }
}