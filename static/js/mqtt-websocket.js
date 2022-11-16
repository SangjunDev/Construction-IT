$(document).ready(function(){
    MQTTConnect();
  });
  
var mqtt;
var reconnectTimeout = 2000;
var host = "192.168.10.89";
var port = 9001;

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
  mqtt.subscribe("192.168.10.89/status")
  mqtt.onMessageArrived = onMessageArrived;

}

function onFailure(){
  console.log("연결 실패");
}

function onMessageArrived(message) {
console.log("onMessageArrived: " + message.payloadString);
}

function Msg(msg){
  //alert(msg);
  message = new Paho.MQTT.Message(msg);
  message.destinationName = "192.168.10.89/led";

  mqtt.send(message);
}