import time

import machine


class LED:

    def __init__(self, led_pin="LED"):
        self.led = machine.Pin(led_pin, machine.Pin.OUT)
        self.led.off()
        self.status = 0

    def on(self):
        self.led.on()
        self.status = 1

    def off(self):
        self.led.off()
        self.status = 0

    def toggle(self):
        if self.status == 0:
            self.on()
        else:
            self.off()


    def blink(self, times=2, on_delay=0.1, off_delay=0.1):
        for _ in range(times):
            self.on()
            time.sleep(on_delay)
            self.off()
            time.sleep(off_delay)


if __name__ == "__main__":
    led = LED()
    led.led = machine.Pin("LED", machine.Pin.OUT)

    # Flash the LED 3 times with specified delays
    led.blink(times=3, on_delay=0.2, off_delay=0.2)

    print("LED flash completed.")
