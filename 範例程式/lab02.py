# 從 machine 模組匯入 Pin 物件
from machine import Pin
# 從 neopixel 模組匯入控制條燈的 NeoPixel 物件
from neopixel import NeoPixel

# 建立 NeoPixel 物件, 設定控制為 4 號腳位, 燈珠數量為 15, 命名為 led_strip
led_strip = NeoPixel(Pin(4), 15)
# 設定第 1 顆燈珠數值
led_strip[0] = (0, 0, 255)
# 依設定顯示
led_strip.write()               

