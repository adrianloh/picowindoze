#include "pico/stdlib.h"

int main() {
    const uint LED_PIN = PICO_DEFAULT_LED_PIN;
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    uint i = 0;
    bool led_on = false;
    do {
        i++;
        if (i % 1000000 == 0) {
            i = 0;
            led_on = !led_on;
            gpio_put(LED_PIN, led_on);
        }
    } while (true);
    return 0;
}