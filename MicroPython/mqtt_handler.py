import json
import machine
import network
import ubinascii
from umqttsimple import MQTTClient


class MQTTHandler:
    def __init__(self, broker_address=None, broker_port=None, keepalive=None, client_id=None):
        self.broker_address = broker_address or '192.192.192.192'
        self.broker_port = broker_port or 1883 # Default MQTT port
        self.keepalive = keepalive or 3600 # Defaults to 1 hour
        self.client_id = client_id or ubinascii.hexlify(machine.unique_id())
        self.client = None
        self.subscriptions = {}
        self.connected = False

    @staticmethod
    def _ensure_connection():
        wlan = network.WLAN(network.STA_IF)
        while not wlan.isconnected():
            pass

    def _message_callback(self, topic, payload):
        topic_str = topic.decode()

        try:
            try:
                message = json.loads(payload.decode())
            except Exception:
                try:
                    message = payload.decode()
                except Exception:
                    message = payload
        except UnicodeDecodeError:
            message = payload

        if topic_str in self.subscriptions:
            for callback in self.subscriptions[topic_str]:
                try:
                    callback(topic_str, message)
                except Exception as e:
                    print(f"Error in callback for topic {topic_str}: {e}")

        for pattern, callbacks in self.subscriptions.items():
            if self._topic_matches_pattern(topic_str, pattern):
                for callback in callbacks:
                    try:
                        callback(topic_str, message)
                    except Exception as e:
                        print(f"Error in wildcard callback for pattern {pattern}: {e}")

    @staticmethod
    def _topic_matches_pattern(topic, pattern):
        if pattern == topic:
            return True
        if '+' in pattern or '#' in pattern:
            pattern_parts = pattern.split('/')
            topic_parts = topic.split('/')
            if pattern.endswith('#'):
                return topic.startswith(pattern[:-1])
            if len(pattern_parts) != len(topic_parts):
                return False
            for p, t in zip(pattern_parts, topic_parts):
                if p != '+' and p != t:
                    return False
            return True
        return False

    def connect(self):
        if self.connected:
            return
        self._ensure_connection()
        self.client = MQTTClient(self.client_id, self.broker_address, broker_port=self.broker_port, keepalive=self.keepalive)
        self.client.set_callback(self._message_callback)
        self.client.connect()
        self.connected = True

    def disconnect(self):
        if self.client and self.connected:
            self.client.disconnect()
            self.connected = False

    def publish_message(self, topic, payload, retain=False, qos=0):
        self._ensure_connection()
        if isinstance(payload, (dict, list)):
            payload = json.dumps(payload)
        elif isinstance(payload, str):
            payload = payload
        else:
            payload = str(payload)
        if isinstance(topic, str):
            topic = topic.encode()
        self.connect()
        try:
            self.client.publish(topic, payload.encode(), retain=retain, qos=qos)
        finally:
            self.disconnect()

    def publish_to_channel(self, topic="testes", payload="Hello world!", retain=False, qos=0):
        self.publish_message(topic, payload, retain, qos)

    def publish_sensor_data(self, sensor_name, data, retain=False, qos=0):
        payload = {
            "sensor": sensor_name,
            "data": data,
            "timestamp": machine.RTC().datetime()
        }
        topic = f"sensors/{sensor_name}"
        self.publish_message(topic, payload, retain, qos)

    def publish_status(self, device_name, status, retain=True, qos=0):
        payload = {
            "device": device_name,
            "status": status,
            "timestamp": machine.RTC().datetime()
        }
        topic = f"status/{device_name}"
        self.publish_message(topic, payload, retain, qos)

    def subscribe(self, topic, callback, qos=0):
        self.connect()
        if topic not in self.subscriptions:
            self.subscriptions[topic] = []
        self.subscriptions[topic].append(callback)
        if isinstance(topic, str):
            topic_bytes = topic.encode()
        else:
            topic_bytes = topic
        self.client.subscribe(topic_bytes, qos)

    def subscribe_to_topic(self, topic, callback, qos=0):
        self.subscribe(topic, callback, qos)

    def subscribe_to_sensor(self, sensor_name, callback, qos=0):
        topic = f"sensors/{sensor_name}" if sensor_name else "sensors/+"
        self.subscribe(topic, callback, qos)

    def subscribe_to_status(self, device_name, callback, qos=0):
        topic = f"status/{device_name}" if device_name else "status/+"
        self.subscribe(topic, callback, qos)

    def unsubscribe(self, topic, callback=None):
        if topic in self.subscriptions:
            if callback:
                if callback in self.subscriptions[topic]:
                    self.subscriptions[topic].remove(callback)
                if not self.subscriptions[topic]:
                    del self.subscriptions[topic]
            else:
                del self.subscriptions[topic]

    def wait_for_messages(self):
        if not self.connected:
            raise Exception("Not connected to MQTT broker")
        try:
            while True:
                self.client.wait_msg()
        except KeyboardInterrupt:
            print("Stopping message listener...")

    def check_messages(self):
        if self.connected:
            self.client.check_msg()
