var mqtt;
var reconnectTimeout = 2000;
var host = "192.168.10.89";
var port = 9001;

function onConnect(){
    console.log("연결 성공");
}

function onFailure(){
    console.log("연결 실패");
    //setTimeout(MQTTConnect, reconnectTimeout);
}

function sendMsg(msg){
    //alert(msg);

    message = new Paho.MQTT.Message(msg);
    message.destinationName = "192.168.10.89/led"; 
    mqtt.send(message);
}

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
