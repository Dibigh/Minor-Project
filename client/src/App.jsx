//import { useState } from 'react'
import './App.css'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Register_login from './Pages/Register_login/Register_login'
import Home from './Pages/Home/Home'
import Disease from './Pages/Disease/Disease';
function App() {
  return (
    <>
     <Router>
      <Routes>
        <Route path="/" element={<Register_login/>} />
        <Route path="/home" element={<Home/>} />
        <Route path="/disease" element={<Disease/>} />
      </Routes>
    </Router>
    </>
  )
}

export default App
