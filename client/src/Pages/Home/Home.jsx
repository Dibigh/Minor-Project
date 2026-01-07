import React from 'react'
import { useEffect, useState } from 'react';
import './Home.css'
function Home() {

  const [sensorData, setSensorData] = useState(null);
  const [inputValue, setInputValue] = useState('');
  const [cropdatavalue, setCropDataValue] = useState('');
  const [webs, setWebs] = useState(null);
  const [buttonstate1, setButtonstate1] = useState(false);
  const [buttonstate2, setButtonstate2] = useState(false);
  const [buttonstate3, setButtonstate3] = useState(false);
  const [intervalid1, setIntervalId1] = useState(null);
  const [intervalid2, setIntervalId2] = useState(null);
  const [intervalid3, setIntervalId3] = useState(null);
  const [fanstatus, setFanStatus] = useState('OFF');
  const [waterpumpstatus, setWaterPumpStatus] = useState('OFF');
  const [humidifierstatus, setHumidifierStatus] = useState('OFF');

  const handleCropName=async(e)=>{
    if (e.key === 'Enter') {
      console.log('enter hit')
    try {
      const response = await fetch('http://localhost:5000/cropsdata', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({"cropName":inputValue}),
      });

      const data = await response.json();
      console.log(data);
      if(data.success==true){
        console.log(data.data[0])
       setCropDataValue(data.data[0])
      }
      else{
        window.alert('crop data not found')
      }
    } catch (error) {
      setError('An error occurred while connecting to the server.');
    }
  }
  }


  useEffect(() => {

    console.log('automatic or manual')
    if(cropdatavalue&&'soilMoisture' in sensorData && 'temperature' in sensorData && 'humidity' in sensorData){

    if(buttonstate1==true||buttonstate2==true||buttonstate3==true){

const checkValueInRange = (value,min,max,identifier) => {

      if (value >= min && value <= max) {
        if(identifier=='soilMoisture'){
          sendCommand('WATERPUMP_OFF')
        }
        if(identifier=='temperature'){
          sendCommand('FAN_OFF')
        }
        if(identifier=='humidity'){
          sendCommand('HUMIDIFIER_OFF')
        }
        console.log('Value is within the range');
      }
     else {
        if(identifier=='soilMoisture'){
          if(value<min){
          sendCommand('WATERPUMP_ON')
          }
          else{
            sendCommand('WATERPUMP_OFF')
            }
        }
        if(identifier=='temperature'){
          if(value<min){
            sendCommand('FAN_OFF')
            }
            else{
              sendCommand('FAN_ON')
              }
        }
        if(identifier=='humidity'){
          if(value<min){
            sendCommand('HUMIDIFIER_ON')
            }
            else{
              sendCommand('HUMIDIFIER_OFF')
              }
        }
        console.log('Value is out of the range');
      }
    }

     
        if(buttonstate1==true){
          if(intervalid1){
            clearInterval(intervalid1);
          }
          console.log('interval1')
          const intervalId1 = setInterval(() => {
    checkValueInRange(sensorData.soilMoisture,cropdatavalue.optimalSoilMoisture.min, cropdatavalue.optimalSoilMoisture.max,'soilMoisture')
  }, 10000);  
  setIntervalId1(intervalId1)
  }
        if(buttonstate2==true){
          if(intervalid2){
            clearInterval(intervalid2);
          }
          console.log('interval2')
          const intervalId2 = setInterval(() => {
    checkValueInRange(sensorData.temperature,cropdatavalue.optimalTemperature.min, cropdatavalue.optimalTemperature.max,'temperature')
  }, 10000);   
  setIntervalId2(intervalId2)    
  }
        if(buttonstate3==true){
          if(intervalid3){
            clearInterval(intervalid3);
          }
          console.log('interval3')
          const intervalId3 = setInterval(() => {
    checkValueInRange(sensorData.humidity,cropdatavalue.optimalHumidity.min, cropdatavalue.optimalHumidity.max,'humidity')
  }, 10000);  
  setIntervalId3(intervalId3)
  }
 

}
if(buttonstate1==false && intervalid1){
  console.log('previous interval1 clear')
  clearInterval(intervalid1);
  sendCommand('WATERPUMP_OFF')
}
if (buttonstate2==false && intervalid2){
  console.log('previous interval2 clear')
  clearInterval(intervalid2);
  sendCommand('FAN_OFF')
}
if(buttonstate3==false && intervalid3){
  console.log('previous interval3 clear')
  clearInterval(intervalid3);
  sendCommand('HUMIDIFIER_OFF')
}
//return () => clearInterval(intervalId);
}
  },[buttonstate1,buttonstate2,buttonstate3])

  useEffect(() => {
  const connectWebSocket=()=> {
    const ws = new WebSocket('ws://172.16.28.129:5500');
      setWebs(ws)
    ws.onopen = () => {
      console.log('Connected to WebSocket server.');
      const message = JSON.stringify({ type: 'react'});
      ws.send(message);
    };

    ws.onmessage = (event) => {
      
      const data = JSON.parse(event?.data);
      if ('soilMoisture' in data && 'temperature' in data && 'humidity' in data) {
        setSensorData(data);
      }
      
      if(data?.status=='Fan turned ON'){
        setFanStatus('ON')
      }
      if(data?.status=='Fan turned OFF')
        {
        setFanStatus('OFF')
      }
      if(data?.status=='WATWERPUMP turned ON')
        {
        setWaterPumpStatus('ON')
      }
      if(data?.status=='WATERPUMP turned OFF')
        {
          setWaterPumpStatus('OFF')
      }
      if(data?.status=='HUMIDIFIER turned ON')
        {
        setHumidifierStatus('ON')
      }
      if(data?.status=='HUMIDIFIER turned OFF')
        {
          setHumidifierStatus('OFF')
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.onclose = () => {
      console.log('WebSocket connection closed.retrying...');
      setTimeout(connectWebSocket,2000);
    };
  }
  connectWebSocket();
   return () => {
      ws.close();
    };
  }, []);

  const sendCommand = (command) => {
    const commandObj = { type: 'command', action: command };
    webs.send(JSON.stringify(commandObj));
    console.log('Sending command:', commandObj);
  };


 /*const handleTemperature=()=>{
  setButtonstate2(!buttonstate2)
  if(buttonstate2==true){
    sendCommand('FAN_ON');
  }
  else
  {
    sendCommand('FAN_OFF');
  }
 }*/

  /*
  useEffect(() => {
    const fetchData = async () => {
        try {
            const response = await fetch('http://localhost:5000/sensor-data');
            const data = await response.json();
            setSensorData(data);
            console.log(data);
        } catch (error) {
            console.error('Error fetching sensor data:', error);
        }
    };

    const interval = setInterval(fetchData, 1000); // Poll every 2 seconds
    return () => clearInterval(interval); // Cleanup on unmount
}, []);

*/
  return (
    <div id='home'>
      <div id='navbar'>
       <div>
        <span><a id='anchor1' href="/home">Home</a></span>
       </div>
       <div>
       <span><a id='anchor2' href="disease">Disease</a></span>
       </div>
      </div>
      <div id='body'>
      <div id='cropName'>
       <label>Enter crop Name</label> <input type="text"  value={inputValue} onChange={(e) => setInputValue(e.target.value)}  onKeyDown={handleCropName} placeholder='Enter crop name' />
      </div>
        <div id='sensordata'>
        <div id='soil'>
        <div id='sensorname'>Soil moisture</div>
           <div id='value'>Soil moisture Value:  {sensorData?.soilMoisture}%</div>
        {cropdatavalue &&(<div id='required_value'>Optimal Soil moisture value:{cropdatavalue.optimalSoilMoisture.min}-{cropdatavalue.optimalSoilMoisture.max}%</div>)}
            <div id='manualcontrol'>Manual Control   <button onClick={()=>setButtonstate1(!buttonstate1)}>{!buttonstate1?'ON':'OFF'}</button>
            
           {!buttonstate1 &&( <div>Water Pump <button onClick={()=>sendCommand('WATERPUMP_ON')}>ON</button> <button onClick={()=>sendCommand('WATERPUMP_OFF')}>OFF</button></div>)}
            </div>
            <div id='automaticcontrol'>Automatic Control   <button onClick={()=>setButtonstate1(!buttonstate1)}>{buttonstate1?'ON':'OFF'}</button></div>
              <div id='status'>WaterPump staus:{waterpumpstatus}</div>
              </div>
        <div id='temperature'>
        <div id='sensorname'>Temperature</div>
          <div id='value'>Temperature Value:  {sensorData?.temperature}°C</div>
        {cropdatavalue &&(<div id='required_value'>Optimal temperature value:{cropdatavalue.optimalTemperature.min}-{cropdatavalue.optimalTemperature.max}°C</div>)}
          <div id='manualcontrol'>Manual Control   <button onClick={()=>setButtonstate2(!buttonstate2)}>{!buttonstate2?'ON':'OFF'}</button>
          
          {!buttonstate2 &&( <div>Cooling Fan <button onClick={()=>sendCommand('FAN_ON')}>ON</button> <button onClick={()=>sendCommand('FAN_OFF')}>OFF</button></div>)}
          </div>
          <div id='automaticcontrol'>Automatic Control   <button onClick={()=>setButtonstate2(!buttonstate2)}>{buttonstate2?'ON':'OFF'}</button></div>
          <div id='status'>Fan staus:{fanstatus} </div>
        </div>
        <div id='humidity'>
        <div id='sensorname'>Humidity</div>
           <div id='value'>Humidity Value:  {sensorData?.humidity}%</div>
        {cropdatavalue &&(<div id='required_value'>Optimal Humidity value:{cropdatavalue.optimalHumidity.min}-{cropdatavalue.optimalHumidity.max}%</div>)}
           <div id='manualcontrol'>Manual Control   <button onClick={()=>setButtonstate3(!buttonstate3)}>{!buttonstate3?'ON':'OFF'}</button>
           
           {!buttonstate3 &&( <div>Humidifier <button onClick={()=>sendCommand('HUMIDIFIER_ON')}>ON</button> <button onClick={()=>sendCommand('HUMIDIFIER_OFF')}>OFF</button></div>)}
           </div>
           <div id='automaticcontrol'>Automatic Control   <button onClick={()=>setButtonstate3(!buttonstate3)}>{buttonstate3?'ON':'OFF'}</button></div>
           <div id='status'>Humidifier status:{humidifierstatus}</div>
       
        </div>
        </div>
      </div>
    </div>
  )
}

export default Home