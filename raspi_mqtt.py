import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

led_pin = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin,GPIO.OUT)


broker = "192.168.10.89"
port = 9001
sub_topic = "192.168.10.89/led"
pub_topic = "192.168.10.89/status"

def on_connect(client, userdata, flags, rc):
    print("connect.."+str(rc))
    if rc==0:
        client.subscribe(sub_topic,0)
    else:
        print("연결 실패..")

def on_message(client, userdata, message):
    myvalue = message.payload.decode("utf-8")
    print(message.topic+"---"+myvalue)
    if myvalue == "led_on":
        GPIO.output(led_pin, GPIO.HIGH)
        client.publish(pub_topic,"on")
        print(GPIO.input(led_pin))
    else:
        GPIO.output(led_pin, GPIO.LOW)
        client.publish(pub_topic,"off")
        print(GPIO.input(led_pin))

if __name__ == "__main__":
        try:
         

         mqttClient = mqtt.Client(transport='websockets')
         mqttClient.on_connect = on_connect
         mqttClient.on_message = on_message
         mqttClient.connect(broker ,port ,60)
         mqttClient.loop_forever()
         
         if GPIO.input(led_pin) == 1:
            print("led state: on")
         else:
           print("led state: off")
         
        except:
            GPIO.cleanup()
