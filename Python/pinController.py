import lgpio


class PinController:
    def __init__(self, gpio_pin=14, topic="pin"):
        self.topic = topic
        self.state = 0
        self.gpio_pin = gpio_pin
        self.h = lgpio.gpiochip_open(0)  # Open the GPIO chip
        lgpio.gpio_claim_output(self.h, self.gpio_pin)

    def handle_message(self, topic, payload):
        if topic != self.topic:
            return

        print(f"PinController received: {topic}: {payload}")
        if payload.lower() == "on":
            self.state = 1
        elif payload.lower() == "off":
            self.state = 0
        elif payload.lower() == "toggle":
            self.state = 1 - self.state
        else:
            print(f"PinController received an invalid payload: {payload} for topic: {topic}. Expected 'on', 'off' or 'toggle'.")
            return
        lgpio.gpio_write(self.h, self.gpio_pin, self.state)

    def cleanup(self):
        lgpio.gpio_write(self.h, self.gpio_pin, 0)
        lgpio.gpiochip_close(self.h)
