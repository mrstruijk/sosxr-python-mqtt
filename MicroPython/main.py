# main.py
import time

from led import LED
from mqtt_handler import MQTTHandler
from mac_address import FindMAC
from wifi_connect import WiFiConnect

mac_finder = FindMAC()
mac_address = mac_finder.get_mac()

wifi_connector = WiFiConnect("FatFreddy", "wifi@PSWMSW2h")
wifi_connector.connect_to_wifi()


led = LED()


def on_message(topic, payload):
    print(f"Received message on {topic}: {payload}")
    if topic == "testes":
        led.blink()
        
def on_other_message(topic, payload):
    print(f"Received other message on {topic}: {payload}")
    led.blink(10, 0.05, 0.05)
    
mqtt_handler = MQTTHandler('192.168.1.170')
mqtt_handler.connect()

# while mqtt_handler.connected == False:
#     print("Waiting for MQTT connection...")
#     time.sleep(1);

mqtt_handler.subscribe_to_topic("testes", on_message)
mqtt_handler.subscribe_to_topic("other_topic", on_other_message)

mqtt_handler.publish_message("testes", "Hello From MicroPython!", retain=False, qos=1)

mqtt_handler.wait_for_messages()
