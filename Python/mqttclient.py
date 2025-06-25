# mqttclient.py

import paho.mqtt.client as mqtt
from gpiozero import Device, LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

broker_ip = "192.192.192.192" # What IP address is this broker running on?

Device.pin_factory = PiGPIOFactory()

led_pin = 21
led = LED(led_pin)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("doorbell")

def on_message(client, userdata, msg):
    print("Topic: " + msg.topic + " & " + "Payload: " + msg.payload.decode())
    led.toggle()

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_ip, 1883)

client.loop_forever()