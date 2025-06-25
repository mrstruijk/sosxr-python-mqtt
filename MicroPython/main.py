# main.py

from led import LED
from mqtt_handler import MQTTHandler

led = LED()


def on_message(topic, message):
    print(f"Received message on {topic}: {message}")
    if topic == "testes":
        led.blink()


mqtt_handler = MQTTHandler('145.118.220.163')
mqtt_handler.connect()
mqtt_handler.subscribe_to_topic("testes", on_message)
mqtt_handler.wait_for_messages()
