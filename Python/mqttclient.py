import paho.mqtt.client as mqtt


class MQTTClient:
    def __init__(self, broker="localhost", port=1883, topic="#"):
        self._subscribers = []
        self.topic = topic

        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.connect(broker, port, 60)
        self.client.loop_start()

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("MQTT Connected")
            self.subscribe(self.topic)
        else:
            print(f"MQTT Connect failed: {rc}")

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def unsubscribe(self, topic):
        self.client.unsubscribe(topic)

    def publish(self, topic, payload, retain=False, qos=0):
        self.client.publish(topic, payload, retain=retain, qos=qos)
        print(f"📤 {topic}: {payload} (retain={retain}, qos={qos})")

    def _on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        print(f"MQTT Client received: {msg.topic}: {payload}")
        for callback in self._subscribers:
            callback(msg.topic, payload)

    def on_message(self, callback):
        self._subscribers.append(callback)

    def cleanup(self):
        self.unsubscribe(self.topic)
        self.client.disconnect()
