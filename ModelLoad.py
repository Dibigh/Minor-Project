from flask import Flask, request, jsonify
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import io
import requests as req  # For downloading the image

# Define the CNN model class
class SpinachDiseaseCNN(nn.Module):
    def __init__(self, num_classes):
        super(SpinachDiseaseCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.fc1 = nn.Linear(64 * 64 * 64, 512)
        self.fc2 = nn.Linear(512, num_classes)
        
    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = x.view(x.size(0), -1)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
num_classes = 3  # Update this to match the number of classes in your training data
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SpinachDiseaseCNN(num_classes).to(device)

# Load model state
model.load_state_dict(torch.load("spinach_disease_model.pth", map_location=device))
model.eval()

# Define the same transformation as used during training
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

# Define route for downloading and predicting the image
@app.route("/predict_from_url", methods=["POST"])
def predict_from_url():
    try:
        # Extract the image URL from the request
        data = request.json
        if "image_url" not in data:
            return jsonify({"error": "No image URL provided"}), 400
        
        image_url = data["image_url"]

        # Download the image
        response = req.get(image_url)
        if response.status_code != 200:
            return jsonify({"error": "Failed to download image"}), 400

        # Load the image into a PIL format
        image = Image.open(io.BytesIO(response.content)).convert("RGB")
        
        # Preprocess the image
        input_tensor = transform(image).unsqueeze(0).to(device)

        # Perform prediction
        with torch.no_grad():
            output = model(input_tensor)
            _, predicted_class = torch.max(output, 1)

        # Map class index to class label
        class_labels = ["Healthy", "Diseased_A", "Diseased_B"]  # Replace with your actual class names
        predicted_label = class_labels[predicted_class.item()]

        return jsonify({"predicted_class": predicted_label}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050) 
