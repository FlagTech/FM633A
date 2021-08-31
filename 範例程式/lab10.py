import network
import ledstrip
from umqtt.robust import MQTTClient

#建立變數來存放條燈特效類別
led_strip_effect = 0
#設定條燈腳位為 4, 燈珠數量為 15
ledstrip.setup(4,15)

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
    # 宣告使用全域變數 led_strip_effect
    global led_strip_effect
    print(topic,msg)
    # 設定條燈特效項目
    led_strip_effect = msg
     
client.connect()
client.set_callback(get_cmd)
client.subscribe(client.user.encode() + b"/feeds/effect");

# 不斷重複執行
while True:       
    client.check_msg()
    if led_strip_effect == b'0':
        ledstrip.clear()
    elif led_strip_effect == b'1':   
        #rainbow_cycle(間隔毫秒時間) 
        ledstrip.rainbow_cycle(5)
    elif led_strip_effect == b'2':
        #cycle(r, g, b, 間隔毫秒時間)
        ledstrip.cycle(123, 0, 20, 100)
    elif led_strip_effect == b'3':
        #bounce(r, g, b, 間隔毫秒時間)
        ledstrip.bounce(23, 20, 128, 50)