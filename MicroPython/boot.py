# boot.py

from mac_address import FindMAC
from wifi_connect import WiFiConnect

mac_finder = FindMAC()
mac_address = mac_finder.get_mac()

wifi_connector = WiFiConnect("iotroam", "SoloVrOculus")
wifi_connector.connect_to_wifi()
