import network
import ubinascii

class FindMAC:
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

    def get_mac(self):
        mac = ubinascii.hexlify(self.wlan.config('mac'), ':').decode()
        print(f"MAC Address: %s" % mac)
        return mac

if __name__ == "__main__":
    wifi_mac = FindMAC()
    mac_address = wifi_mac.get_mac()