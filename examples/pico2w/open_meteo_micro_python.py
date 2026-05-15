# Raspberry Pi Pico 2 WH + Grove Shield MicroPython example
# 기본 출력은 USB 시리얼입니다. Grove I2C OLED/LCD가 있으면 아래 표시 함수 부분을 확장하세요.

import network
import urequests
import time
from machine import Pin

WIFI_SSID = "YOUR_WIFI"
WIFI_PASSWORD = "YOUR_PASSWORD"

# Pico 2 WH 온보드 LED. Grove Shield 사용 시에도 연결 확인용으로 씁니다.
led = Pin("LED", Pin.OUT)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

while not wlan.isconnected():
    led.toggle()
    time.sleep(0.5)

led.on()

url = "https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&current=temperature_2m,relative_humidity_2m&timezone=Asia%2FSeoul"
r = urequests.get(url)
data = r.json()
r.close()

current = data["current"]
line1 = "Seoul temp: {} C".format(current["temperature_2m"])
line2 = "Humidity: {} %".format(current["relative_humidity_2m"])

print(line1)
print(line2)

# 선택: Grove I2C OLED/LCD 사용 시
# - Grove Shield의 I2C 포트에 디스플레이를 연결합니다.
# - 보통 SDA=GP4, SCL=GP5 조합을 사용하지만, 실물 Shield 표기를 우선 확인하세요.
# - 사용하는 OLED/LCD 드라이버(ssd1306 등)를 보드에 복사한 뒤 아래처럼 표시 코드를 추가합니다.
#
# from machine import I2C
# import ssd1306
# i2c = I2C(0, scl=Pin(5), sda=Pin(4))
# oled = ssd1306.SSD1306_I2C(128, 64, i2c)
# oled.text(line1[:16], 0, 0)
# oled.text(line2[:16], 0, 12)
# oled.show()
