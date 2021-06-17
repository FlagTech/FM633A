import network, time, neopixel
from machine import Pin, PWM
from umqtt.robust import MQTTClient

# C4  = 261
# D4  = 294
# E4  = 330
# F4  = 349
# G4  = 392
# A4  = 440
# B4  = 494

# 對應頻率
rhythm = (261, 294, 330, 349, 392, 440, 494)

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
    client_id="D1mini", 
    server="io.adafruit.com", 
    user="AIO 帳號", 
    password="AIO 金鑰",
    ssl=False)

# 註冊收到訂閱資料時的處理函式    
def get_cmd(topic, msg):
    msgs = msg.decode()
    for i in msgs:
        print(rhythm[int(i)])
        buzzer.duty(2)
        play_tone(rhythm[int(i)], 500)
        buzzer.duty(0)
        time.sleep(0.1)

client.connect()
client.set_callback(get_cmd)
client.subscribe(client.user.encode() + b"/feeds/music");

while True:       
    client.check_msg()


   

