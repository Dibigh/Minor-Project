import requests

# Server URL (update with your Flask server's IP or hostname)
SERVER_URL = "http://192.168.1.6:5050/predict_from_url"

# Path to the image file you want to send
IMAGE_PATH = r"E:\Pytorch\pretrained\DV.jpeg"

# Send the image as a file
with open(IMAGE_PATH, "rb") as image_file:
    files = {"file": image_file}  # Match the key expected by your server
    response = requests.post(SERVER_URL, files=files)  # Use 'files' instead of 'data'

    if response.status_code == 200:
        print("Image uploaded successfully:", response.json())
    else:
        print("Failed to upload image:", response.status_code, response.text)
