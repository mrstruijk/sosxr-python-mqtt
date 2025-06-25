# mqtt_usage_examples.py

import time

from mqtt_handler import MQTTHandler


class MQTTUsageExamples:
    """
    Class containing MQTT usage examples that can be run as demonstrations.
    """

    def __init__(self, broker_ip=None):
        self.broker_ip = broker_ip or '192.192.192.192'  # Default broker IP if not provided

    def example_publisher(self):
        """Example of using MQTTPublisher"""
        mqtt_handler = MQTTHandler(broker_address=self.broker_ip)

        # Publish to doorbell channel (your original use case)
        mqtt_handler.publish_to_channel('doorbell', {'Message': 'Doorbell pressed!'})

        # Publish sensor data
        mqtt_handler.publish_sensor_data('humidity', {'value': 50, 'unit': '%'})

        # Publish device status
        mqtt_handler.publish_status('door_sensor', {'online': False, 'battery': 10})

        # Publish to custom topic
        mqtt_handler.publish_message('home/living_room/light', {'state': 'on', 'brightness': 75}, retain=True)

        return mqtt_handler

    def example_subscriber(self):
        """Example of using MQTTSubscriber"""
        # if we don't have a mqtt_handler, we create one. First we check to see if we already have one instantiated
        mqtt_handler = MQTTHandler(broker_address=self.broker_ip)

        # Define callback functions
        def doorbell_handler(topic, message):
            print(f"Doorbell message: {message}")  # Handle doorbell logic here

        def sensor_handler(topic, message):
            print(f"Sensor data from {topic}: {message}")  # Process sensor data here

        def status_handler(topic, message):
            print(f"Status update from {topic}: {message}")  # Handle status updates here

        # Subscribe to different topics
        mqtt_handler.subscribe_to_topic('doorbell', doorbell_handler)  # Doorbell channel
        mqtt_handler.subscribe_to_sensor(sensor_handler)  # Sensor data updates
        mqtt_handler.subscribe_to_status(status_handler)  # Status updates

        # Subscribe to specific sensor
        mqtt_handler.subscribe_to_sensor(sensor_handler, 'temperature')

        # Subscribe with wildcard
        def all_home_messages(topic, message):
            print(f"Home message from {topic}: {message}")

        mqtt_handler.subscribe_to_topic('home/+/+', all_home_messages)

        return mqtt_handler

    def run_demo(self):
        """
        Run a short demonstration showing publisher and subscriber working together.
        """
        print("🚀 Starting MQTT Demo...")
        print("-" * 40)

        # Setup subscriber first
        print("📡 Setting up subscriber...")
        subscriber = self.example_subscriber()

        # Small delay to ensure subscriber is ready
        time.sleep(1)

        # Setup and run publisher
        print("📤 Setting up publisher and sending messages...")
        publisher = self.example_publisher()

        # Give time for messages to be processed
        print("⏳ Processing messages...")
        for i in range(5):
            subscriber.check_messages()
            time.sleep(0.5)

        print("✅ Demo completed!")
        print("-" * 40)

        # Cleanup
        try:
            publisher.disconnect()
            subscriber.disconnect()
            print("🔌 Disconnected successfully")
        except:
            pass


if __name__ == "__main__":
    # Create demo instance and run it
    demo = MQTTUsageExamples()

    try:
        demo.run_demo()
    except KeyboardInterrupt:
        print("\n⚠️ Demo interrupted by user")
    except Exception as e:
        print(f"❌ Demo error: {e}")

    print("👋 Demo finished!")
