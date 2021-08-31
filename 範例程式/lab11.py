import network, time, neopixel
from machine import Pin, PWM
from umqtt.robust import MQTTClient

from rtttl import RTTTL

buzzer = PWM(Pin(5))
buzzer.duty(0)

def play_tone(freq, msec):
    if freq > 0:
        buzzer.freq(freq)   # Set frequency
        buzzer.duty(512)
        time.sleep(msec*0.001)  # Play for a number of msec
    buzzer.duty(0)          # Stop playing
    time.sleep(0.05)

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect("無線網路基地台", "無線網路密碼")

# Wait for connecting to Wi-Fi
while not sta_if.isconnected():    
    pass
print("控制板已連線")

client = MQTTClient(
    client_id="", 
    server="io.adafruit.com", 
    user="Rainnie", 
    password="aio_exaA21CEmjAUxEySVU0fC8q5kVYW",
    ssl=False)
    
def get_cmd(topic, msg):
    print(topic,msg)
    if msg == b"1":
        print('play music1')
        tune = RTTTL("Halloween:d=4,o=5,b=180:8d6,8g,8g,8d6,8g,8g,8d6,8g,8d#6,8g,8d6,8g,8g,8d6,8g,8g,8d6,8g,8d#6,8g,8c#6,8f#,8f#,8c#6,8f#,8f#,8c#6,8f#")
        buzzer.duty(512)
        for freq, msec in tune.notes():
            play_tone(freq, msec) 
        buzzer.duty(0)
    elif msg == b"2":
        print('play music2')
        tune2 = RTTTL("BobMarleyNowomannocry:d=8,o=5,b=180:4c.6,b.,c.6,b.,4b.,2a.,2p,4p,p,16p,4e.6,f.6,e.6,d.6,2c.6,1p,4p,p,4c.6,b.,d.6,c.6,2a.,1p,4p,p,4e.6,f.6,e.6,d.6,2c.6,1p,4p,p")
        buzzer.duty(512)
        for freq, msec in tune2.notes():
            play_tone(freq, msec) 
        buzzer.duty(0)  
    elif msg == b"3":
        print('play music3')
        tune3 = RTTTL("Fugees-KillingMeSoftly:d=4,o=5,b=90:p,8e,f.,8g,a.,8g,d,g.,p,8a,g.,8f,e.,8f,c.,2p,8e,f.,8g,a.,8g,a,b,8b,c6,8b,a,g,2a")
        buzzer.duty(512)
        for freq, msec in tune3.notes():
            play_tone(freq, msec) 
        buzzer.duty(0)  

client.connect()
client.set_callback(get_cmd)
client.subscribe(client.user.encode() + b"/feeds/voicemood");

while True:       
    client.check_msg()
