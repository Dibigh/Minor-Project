//import React from 'react'
import  React,{useState}  from 'react';
import axios from 'axios';
import './Disease.css'


function Disease() {
    const [selectedImage, setSelectedImage] = useState(null);
    const [message, setMessage] = useState('');

    // Handle file selection
    const handleImageChange = (e) => {
        setSelectedImage(e.target.files[0]);
    };

    // Handle form submission to upload image
    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!selectedImage) {
            setMessage('Please select an image.');
            return;
            Detection();
        }

        const formData = new FormData();
        formData.append('image', selectedImage);

        try {
            // Send the image to the Flask server
            const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',  // Important to send image correctly
                },
            });

            // Show success message or server response
            setMessage(response.data.message);
        } catch (error) {
            setMessage('Error uploading image.');
            console.error(error);
        }
    };
  return (
    <div id='disease'>
         <div id='navbar'>
       <div>
        <span><a id='anchor1' href="/home">Home</a></span>
       </div>
       <div>
       <span><a id='anchor2' href="disease">Disease</a></span>
       </div>
      </div>
      <div id='allcontents'>
    <h2>Upload an Image</h2>
    <div id='formdiv'>
    <form id='form' onSubmit={handleSubmit}>
        {/* Image input field */}
        <input type="file" accept="image/*" onChange={handleImageChange} />
        <button id='formbutton' type="submit">Upload</button>
    </form>
    </div>
    <div id='formmessage'>
    {message && <p>{message.message}{message.disease}</p>}

 </div>
 </div>
 </div>


  )
}

export default Disease