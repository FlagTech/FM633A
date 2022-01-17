# 從 machine 模組匯入 Pin 物件
from machine import Pin
# 從 neopixel 模組匯入控制條燈的 NeoPixel 物件
from neopixel import NeoPixel
# 匯入時間相關的 time 模組
import time

# 建立 NeoPixel 物件, 設定控制為 4 號腳位, 燈珠數量為 15, 命名為 led_strip
led_strip = NeoPixel(Pin(4), 15)

while True:                             # 一直不斷執行
    for i in range(led_strip.n):        # for 走訪整數串列, 範圍為燈珠數量
        led_strip[i] = (0, 48, 64)      # 依序設定每一顆燈珠
        led_strip.write()               # 依設定顯示
        time.sleep_ms(100)              # 暫停 100 毫秒
        led_strip[i] = (0, 0, 0)        # 再將當顆燈珠熄滅
