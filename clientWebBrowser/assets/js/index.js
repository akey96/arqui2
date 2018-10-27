
let callbackTopics = {}

let addMqtt = (callback, topic) => {
  callbackTopics[topic] = callback
}

function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:", responseObject.errorMessage);
  }
}

// called when a message arrives
function onMessageArrived(message) {
  // console.log("topic:", message.destinationName, ", message:",message.payloadString );
  callbackTopics[message.destinationName](message.destinationName, message.payloadString)
}

function callbackDHT11(topic, message) {
  let body_content = document.querySelector('#body-contents')
  body_content.textContent = ""
  let payload = JSON.parse(message)
  
  for(let data of payload.data) {
    
    let tr = document.createElement('tr')

    let id = document.createElement('td')
    let date = document.createElement('td')
    let temperature = document.createElement('td')
    let humudity = document.createElement('td')

    id.textContent = data['id']
    date.textContent = data['date']
    temperature.textContent = data['temperature']
    humudity.textContent = data['humidity']

    tr.appendChild(id)
    tr.appendChild(date)
    tr.appendChild(temperature)
    tr.appendChild(humudity)
    body_content.appendChild(tr)
  }
  
}

function onConnect() {
  console.log("onConnect")
  client.subscribe('sensorDHT11')
  addMqtt(callbackDHT11, 'sensorDHT11')
}

client = new Paho.MQTT.Client('pepito', 9001, "/ws", Math.floor(Math.random()*100)+new Date().getSeconds().toString());
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;
client.connect({onSuccess:onConnect});





