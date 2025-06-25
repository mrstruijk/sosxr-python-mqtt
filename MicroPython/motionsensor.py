# motionsensor.py

# Based on https://randomnerdtutorials.com/micropython-interrupts-esp32-esp8266/
# Based on https://electrocredible.com/raspberry-pi-pico-external-interrupts-button-micropython/

import machine
import time
from mqtthandler import MQTTHandler
from wifi_connect import WiFiConnect

class MotionSensor:
    def __init__(self, sensor_pin=11):
        self.wifi_connector = WiFiConnect()
        self.led = machine.Pin("LED", machine.Pin.OUT)
        self.sensor = machine.Pin(sensor_pin, machine.Pin.IN, machine.Pin.PULL_UP) 
        self.motion = False
        self.debounce_time_ms = 0
        self.MIN_DEBOUNCE_MS = 250
        self.REBOOT_TIME_S = 120
        self.messager = MQTTHandler()
        self.sensor.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.handle_interrupt)
        self.will_reset = False
        self.start_reset_time = 0
        self.current_time = 0
        
    def handle_interrupt(self, pin):
        if (time.ticks_ms() - self.debounce_time_ms) > self.MIN_DEBOUNCE_MS:
            self.motion = True
            self.debounce_time_ms = time.ticks_ms()
    
    def led_flash(self, times=2, on_delay=0.1, off_delay=0.1):
        for _ in range(times):
            self.led.on()
            time.sleep(on_delay)
            self.led.off()
            time.sleep(off_delay)
    
    def check_motion(self):
        if self.motion:
            self.wifi_connector.connect_to_wifi()
            self.messager.message_to_send("DING DONG")
            self.led_flash()
            self.will_reset = True
            self.start_reset_time = time.time()
            self.motion = False
            
    def check_reset(self):
        if self.will_reset:
            print('Will check to see when we are done')
            self.current_time = time.time()
            elapsed_time = self.current_time - self.start_reset_time
            if (elapsed_time > self.REBOOT_TIME_S):
                print('Enough is enough')
                self.led_flash(3,2,0.25)
                machine.reset()
