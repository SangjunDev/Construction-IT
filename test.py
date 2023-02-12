
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import socket

led1_pin = 26
led2_pin = 13
led3_pin = 5
GPIO.setmode(GPIO.BCM)
GPIO.setup(led1_pin,GPIO.OUT)
GPIO.setup(led2_pin,GPIO.OUT)
GPIO.setup(led3_pin,GPIO.OUT)

broker = "cnditest.kro.kr"
port = 9001

def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
     st.connect(('10.255.255.255',1))
     IP = st.getsockname()[0]
    except Exception:
     IP = '127.0.0.1'
    finally:
     st.close()

    return IP

LedControl1_topic = extract_ip() + "/"+ "led_1"
LedControl2_topic = extract_ip() + "/"+ "led_2"
LedControl3_topic = extract_ip() + "/"+ "led_3"

CurrentStatus_topic = extract_ip() + "/" + "status"
ChangeDetection_topic = extract_ip() + "/" + "detection"

def on_connect(client, userdata, flags, rc):
    print("connect.."+str(rc))
    if rc==0:
        client.subscribe(LedControl1_topic)
        client.subscribe(LedControl2_topic)
        client.subscribe(LedControl3_topic)
    else:
        print("연결 실패..")

def on_message(client, userdata, message):
    myvalue = message.payload.decode("utf-8")
    print(message.topic+"---"+myvalue)

    if message.topic == LedControl1_topic:
      if myvalue == "led_on":
        GPIO.output(led1_pin, GPIO.HIGH)
        client.publish(ChangeDetection_topic,"on")

      elif myvalue == "led_off":
        GPIO.output(led1_pin, GPIO.LOW)
        client.publish(ChangeDetection_topic,"off")


    elif message.topic == LedControl2_topic:
      if myvalue == "led_on":
        GPIO.output(led2_pin, GPIO.HIGH)
        client.publish(ChangeDetection_topic,"on")

      elif myvalue == "led_off":
        GPIO.output(led2_pin, GPIO.LOW)
        client.publish(ChangeDetection_topic,"off")
      
    elif message.topic == LedControl3_topic:
      if myvalue == "led_on":
        GPIO.output(led3_pin, GPIO.HIGH)
        client.publish(ChangeDetection_topic,"on")

      elif myvalue == "led_off":
        GPIO.output(led3_pin, GPIO.LOW)
        client.publish(ChangeDetection_topic,"off")
        
    else:
       if GPIO.input(led1_pin) == 1:
        client.publish(CurrentStatus_topic,"on")

       else:
        client.publish(CurrentStatus_topic,"off")

if __name__ == "__main__":
        try:

         mqttClient = mqtt.Client(transport='websockets')
         mqttClient.on_connect = on_connect
         mqttClient.on_message = on_message
         mqttClient.username_pw_set("user","1234")
         mqttClient.connect(broker ,port , 60)
         mqttClient.loop_forever()

        except:
           GPIO.cleanup()
