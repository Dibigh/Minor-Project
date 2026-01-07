const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const Port=3000;
const app = express();
const userRoutes = require('./Routes/userRoutes.js');
const connectDB=require('./config/db.js'); 

const WebSocket = require('ws');

app.use(cors());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use('/',userRoutes);

connectDB();

const wsServerPort = 5500;
const wss = new WebSocket.Server({ port: wsServerPort });


console.log(`WebSocket server is running on ws://172.16.28.129:${wsServerPort}`);
let esp32Client = null;
let reactClient = null;
wss.on('connection', (ws) => {
  console.log('New client connected.');
  ws.on('message', (message) => {
    try {
      const data = JSON.parse(message);
       // Check if this is the ESP32 connection  && wss.clients.size<=2 && !esp32Client  && wss.clients.size<=2 && !reactClient
       console.log('Number of connected clients:', wss.clients.size);
       console.log(data);
       if (data?.type === 'esp32' ){
        if(esp32Client){
          esp32Client.close();
        }
        console.log('ESP32 identified and connected.');
        esp32Client = ws;
       }
       else if(data?.type === 'react' ){
        if(reactClient){
          reactClient.close();
        }
        console.log('react identified and connected.');
        reactClient = ws;
       }
       else if(esp32Client && data?.type === 'command'){
        esp32Client.send(JSON.stringify(data));
          console.log('Command forwarded to ESP32.');
       }
       else if(!esp32Client && data?.type === 'command'){
          console.log('ESP32 not found');
       }
       else if(reactClient && data?.type==='sensor_data'){
          reactClient.send(JSON.stringify(data?.message));
          console.log('data forwarded to react.');
        }
        else if(!reactClient && data?.type==='sensordata'){
          console.log('react not found');
        }
        ws.on('close', () => {
          if(ws===esp32Client){
          console.log('esp32 client disconnected.');
          }
          if(ws===reactClient){
            console.log('react client disconnected.');
            }
        });
       
    } catch (error) {
      console.error('Invalid JSON:', error.message);
    }
  });

  /*
  ws.on('close', () => {
   if(ws===esp32Client){
      esp32Client = null;
      console.log('WebSocket connection closed for esp32.')
   }
   else if(ws===reactClient){
    reactClient=null;
    console.log('WebSocket connection closed for react.')
   }
   else{
   console.log('WebSocket connection for previous closed.')
   }
    })
*/
  

  ws.on('error', (error) => {
    console.error('WebSocket error:', error.message);
  });

});



  app.listen(5000,'0.0.0.0', () => {
    console.log("Server running on http://192.168.18.2:5000");
  });
  


  /*
app.listen(Port, () => {
    console.log(`Server running at http://localhost:${Port}`);
});*/