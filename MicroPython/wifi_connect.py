# wifi_connect.py

import time
import network
import machine


class WiFiConnect:
    MAX_WAIT = 30
    SUCCESS_STATUS = 3

    def __init__(self):
        self.ssid = 'SSID_OF_YOUR_DESIRED_WIFI'
        self.password = 'YOUR_WIFI_SHOULD_PROBABLY_HAVE_A_PASSWORD'
        self.led = machine.Pin("LED", machine.Pin.OUT)
        self.wlan = network.WLAN(network.STA_IF)

    def connect_to_wifi(self):
        if self.wlan.status() == self.SUCCESS_STATUS: 
            print('We already have WiFi, no need to setup again')
            return
        
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)

        # Wait for connect or fail
        while self.MAX_WAIT > 0:
            if self.wlan.status() < 0 or self.wlan.status() >= self.SUCCESS_STATUS:
                break
            self.MAX_WAIT -= 2
            print('waiting for connection…')
            self.led.on()
            time.sleep(1)
            self.led.off()
            time.sleep(1)

        # Handle connection errors
        if self.wlan.status() != self.SUCCESS_STATUS:
            print('Network connection failed, will reset device')
            machine.reset()
        else:
            status = self.wlan.ifconfig()
            print( 'Connected! IP address is ' + status[0] )
            for _ in range(6):
                self.led.on()
                time.sleep(0.2)
                self.led.off()
                time.sleep(0.1)
    
    
if __name__ == "__main__":
    wifi_connector = WiFiConnect()
    wifi_connector.connect_to_wifi()