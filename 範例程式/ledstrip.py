from machine import Pin
from neopixel import NeoPixel
import time

# LED strip configuration
# number of pixels
n = 15
# strip control gpio
p = 4

np = NeoPixel(Pin(p), n)

def setup(led_pin=4, led_num=15):
    global n, np
    n = led_num
    np = NeoPixel(Pin(led_pin), n)

# FUNCTIONS FOR LIGHTING EFFECTS
# bounce
def bounce(r, g, b, wait):
  for i in range(2 * n):
    for j in range(n):
      np[j] = (r, g, b)
    if (i // n) % 2 == 0:
      np[i % n] = (0, 0, 0)
    else:
      np[n - 1 - (i % n)] = (0, 0, 0)
    np.write()
    time.sleep_ms(wait)

# cycle
def cycle(r, g, b, wait):
  for i in range(n):
    for j in range(n):
      np[j] = (0, 0, 0)
    np[i % n] = (r, g, b)
    np.write()
    time.sleep_ms(wait)

# function to go through all colors 
def wheel(pos):
  # Input a value 0 to 255 to get a color value.
  # The colours are a transition r - g - b - back to r.
  if pos < 0 or pos > 255:
    return (0, 0, 0)
  if pos < 85:
    return (255 - pos * 3, pos * 3, 0)
  if pos < 170:
    pos -= 85
    return (0, 255 - pos * 3, pos * 3)
  pos -= 170
  return (pos * 3, 0, 255 - pos * 3)

# rainbow 
def rainbow_cycle(wait):
  for j in range(255):
    for i in range(n):
      rc_index = (i * 256 // n) + j
      np[i] = wheel(rc_index & 255)
    np.write()
    time.sleep_ms(wait)

# turn off all pixels
def clear():
  for i in range(n):
    np[i] = (0, 0, 0)
    np.write()
