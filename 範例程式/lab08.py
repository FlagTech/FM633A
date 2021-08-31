import network, time
from machine import Pin, PWM
from umqtt.robust import MQTTClient

from rtttl import RTTTL

buzzer = PWM(Pin(5))
buzzer.duty(0)

def play_tone(freq, msec):
    if freq > 0:        
        buzzer.freq(freq)
        buzzer.duty(512)
        time.sleep(msec*0.001)  
        buzzer.duty(0)          
    time.sleep(0.05)

# 連線到無線網路
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect("無線網路基地台", "無線網路密碼")


# 循環測試網路直到網路連線成功
while not sta_if.isconnected():  
    pass
print("控制板已連線")

# 建立 MQTT 客戶端物件
client = MQTTClient(
    client_id="", 
    server="io.adafruit.com", 
    user="AIO 帳號", 
    password="AIO 金鑰",
    ssl=False)
    
# 註冊收到訂閱資料時的處理函式   
def get_cmd(topic, msg):
    print(topic,msg)
    if msg == b"100":
        print('play music')
        tune = RTTTL("winner:d=4,o=5,b=140:16e6,16e6,32p,8e6,16c6,8e6,8g6,8p,8g,8p,8c6,16p,8g,16p,8e,16p,8a,8b,2e6")
        for freq, msec in tune.notes():
            play_tone(freq, msec) 
        buzzer.duty(0)
   
client.connect()
client.set_callback(get_cmd)
client.subscribe(client.user.encode() + b"/feeds/cardgame");

while True:       
    client.check_msg()

   

