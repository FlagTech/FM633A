import network
from machine import Pin,PWM
from time import sleep_ms
from umqtt.robust import MQTTClient

buzzer = PWM(Pin(5))
# 設定蜂鳴器發聲頻率
buzzer.freq(400)
# 建立變數作為警報狀態
buzzer_on = 0
 
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
    global buzzer_on
    print(topic,msg)
    if msg == b"100":
        buzzer_on = 1
        print('Times up!') 
    else:
        buzzer_on = 0
        print('CLEAR.')

# 蜂鳴器發聲函式
def buzz():
    buzzer.duty(512)
    sleep_ms(200)
    buzzer.duty(0)
    sleep_ms(200)

client.connect()
client.set_callback(get_cmd)
client.subscribe(client.user.encode() + b"/feeds/timer");

while True:   
    client.check_msg()
    # 判斷狀態是否需要發聲
    if buzzer_on :
        buzz()
