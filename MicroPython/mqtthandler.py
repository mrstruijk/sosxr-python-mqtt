# mqtthandler.py

import json
import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import network

class MQTTHandler:

    def __init__(self):
        server_ip = '192.192.192.192' # Which IP address is the MQTT broker using?

    def message_to_send(self, message): # Messages can be anything: string, bool, int, etc.
        
        # Checking that we already have established a network connection
        wlan = network.WLAN(network.STA_IF)
        while not wlan.isconnected():
            pass

        payload = {
            "Message": message,
        }

        client_id = ubinascii.hexlify(machine.unique_id())

        qt = MQTTClient(client_id, self.server_ip, keepalive=3600)
        qt.connect()
        qt.publish(b"doorbell", json.dumps(payload))
        qt.disconnect()
