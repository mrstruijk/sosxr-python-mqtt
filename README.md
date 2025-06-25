# General

# Todo

In the `wifi_connect.py` you need to fill out your WiFi SSID and password.

Setup the Mosquitto broker. A good explanation on how to set this up on the Pi can be found [here](http://www.steves-internet-guide.com/install-mosquitto-linux/). In both the `mqtthandler.py` (on the sender) and the `mqttclient.py` (on the receiver) you need to fill out the IP-address of your MQTT broker.

## Running as the mqttclient.py as a service on the receiver

To make sure the receiver always works, even after power failure, it needs to run as a service on the device, and start automatically on boot. 

On the receiver, copy the the `mqttclient.py` script to `/usr/bin/mqttclient.py`. 

Copy the systemd file `mqttclient.service` to: `/etc/systemd/system/mqttclient.service`

Reload, start, and enable systemctl and our new service:
- `sudo systemctl daemon-reload` 
- `sudo systemctl enable mqttclient.service` 
- `sudo systemctl start mqttclient.service`

## Known issues

Your sender will probably crash if the MQTT broker is not yet turned on. Make sure the broker is operational before turning on the sender. Turn the sender off and on if this got mixed up somehow. 

# Other

Any ideas and improvements are welcome!

Wherever applicable I noted in the scripts where I got the original code from that I based my work on. Thanks a million to the giants before me!

You are free to use and modify this project to your heart's content. 
