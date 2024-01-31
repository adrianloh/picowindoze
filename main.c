#include "pico/stdlib.h"

#define LED_PIN 25

int main() {
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    uint i = 0;
    do {
        i++;
        if (i % 1000000 == 0) {
            i = 0;
            gpio_xor_mask(1u << LED_PIN);
        }
    } while (1);
    return 0;
}