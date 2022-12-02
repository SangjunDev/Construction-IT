import paho.mqtt.client as mqtt
import time
import json

broker = "cnditest.kro.kr"
port = 9001

LedControl_topic = "192.168.10.89/led"
CurrentStatus_topic = "192.168.10.89/status"
ChangeDetections_topic = "192.168.10.89/detection"

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.subscribe(LedControl_topic)
        client.subscribe(CurrentStatus_topic)
        print("연결 성공..")
        
    else:
        print("연결 실패..")
        
def on_disconnect(client, userdata, rc):
    client.loop_stop(force=False)
    if rc != 0:
        print("Unexpected disconnection.")
    else:
        print("Disconnected")        


def on_message(client, userdata, message):
    myvalue = message.payload.decode("utf-8")
    print(message.topic+"---"+myvalue)


mqttClient = mqtt.Client(transport='websockets')
mqttClient.on_connect = on_connect
mqttClient.on_disconnect = on_disconnect
mqttClient.on_message = on_message
mqttClient.username_pw_set("user","1234")
mqttClient.connect(broker ,port , 60)


