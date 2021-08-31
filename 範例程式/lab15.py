import network, time
from machine import Pin, PWM
from umqtt.robust import MQTTClient

from rtttl import RTTTL

buzzer = PWM(Pin(5))
buzzer.duty(0)

tune = RTTTL("maryhadlamb:d=4,o=6,b=140:2a5,8g5,4f5,4g5,4a5,4a5,4a5,p,4g5,4g5,4g5,p,4a5,4a5,4a5,p,2a5,8g5,4f5,g5,a5,a5,a5,p,g5,g5,a5,g5,2f5")

# 將音符資訊放入變數
tune_list = []
for freq, msec in tune.notes():
    tune_list.append((freq, msec))

# 計算音符數量
tune_lenth = len(tune_list)

# 建立播放索引變數和鬧鐘狀態變數
tune_index = 0
buzzer_on = False

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
        buzzer_on = True
        print('Times up!') 
    else:
        buzzer_on = False
        print('CLEAR.')
   
client.connect()
client.set_callback(get_cmd)
client.subscribe(client.user.encode() + b"/feeds/timer");

while True:       
    client.check_msg()
    if buzzer_on :
        # 分別從音符資料中取值
        freq = tune_list[tune_index][0]
        msec = tune_list[tune_index][1]
        if freq > 0:
            buzzer.freq(freq)   
            buzzer.duty(512)
            time.sleep(msec*0.001)  
        buzzer.duty(0)          
        time.sleep(0.05)
        # 準備播放下一個音符
        tune_index += 1
        if tune_index >= tune_lenth:
            tune_index = 0
    else:
        buzzer.duty(0) 
        # 重置播放順序索引
        tune_index = 0