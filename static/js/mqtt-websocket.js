$(document).ready(function(){
    MQTTConnect();

  });
  
var mqtt;
var reconnectTimeout = 2000;
var host = "192.168.10.89";
var port = 9001;
var LedControl_topic = "192.168.10.89/led"


function MQTTConnect(){
console.log("mqtt 연결");

mqtt = new Paho.MQTT.Client(host,port,"javascript_client"); 

var options = {
    timeout:3,
    onSuccess:onConnect, 
    onFailure:onFailure,
}
mqtt.connect(options);
}

function onConnect(){
  console.log("연결 성공");
  FistAction();
}

function onFailure(){
    console.log("연결 실패");
    mqtt.disconnect();
  }

function FistAction(){

sub_topic = "192.168.10.89/status"    
message = new Paho.MQTT.Message("status");
message.destinationName = LedControl_topic;
mqtt.send(message);

mqtt.subscribe(sub_topic)
mqtt.onMessageArrived = onMessageCS;
}

function onMessageCS(message) {
    console.log("Current Status: " + message.payloadString);
}

function onMessageCD(message) {
    console.log("Change Detection: " + message.payloadString);
}

function SendMsg(msg){
  //alert(msg);
  sub_topic = "192.168.10.89/detection"
  message = new Paho.MQTT.Message(msg);
  message.destinationName = LedControl_topic ;
  mqtt.send(message);
  mqtt.subscribe(sub_topic)
  mqtt.onMessageArrived = onMessageCD;
}
