# Raspberry Pi Pico W MicroPython example
# Fill WIFI_SSID and WIFI_PASSWORD, then run on device.

import network
import urequests
import time

WIFI_SSID = "YOUR_WIFI"
WIFI_PASSWORD = "YOUR_PASSWORD"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

while not wlan.isconnected():
    time.sleep(1)

url = "https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&current=temperature_2m,relative_humidity_2m&timezone=Asia%2FSeoul"
r = urequests.get(url)
data = r.json()
r.close()

current = data["current"]
print("Seoul temperature:", current["temperature_2m"])
print("Humidity:", current["relative_humidity_2m"])
