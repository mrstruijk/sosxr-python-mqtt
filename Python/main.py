import signal
import sys
import time

from mqttclient import MQTTClient
from pinController import PinController

pin = PinController()
mqtt = MQTTClient()

mqtt.subscribe("pin")
mqtt.on_message(pin.handle_message)


def cleanup(sig, frame):
    print("\n🛑 Exiting...")
    mqtt.cleanup()
    pin.cleanup()
    sys.exit(0)


signal.signal(signal.SIGINT, cleanup)

print("🚀 Running. Press Ctrl+C to quit.")
while True:
    time.sleep(1)
