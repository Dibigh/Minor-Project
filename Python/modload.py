import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
from torchvision import datasets
import os
import torchvision.models as models

import matplotlib.pyplot as plt

# Define the model architecture
class SpinachDiseaseDetection(nn.Module):
    def __init__(self, num_classes):
        super(SpinachDiseaseDetection, self).__init__()
        # Load the pretrained ResNet50 model
        self.model = models.resnet50(weights='IMAGENET1K_V1')  # Pre-trained weights
        num_ftrs = self.model.fc.in_features  # Get the number of input features for the final FC layer
        self.model.fc = nn.Linear(num_ftrs, num_classes)  # Modify final layer for your specific task

    def forward(self, x):
        return self.model(x)

# Load model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SpinachDiseaseDetection(num_classes=3)  # Initialize the model for 3 classes
model = model.to(device)  # Move model to GPU/CPU

# Load the model weights (make sure that the weights are compatible)
model.load_state_dict(torch.load('spinach_disease_detection_resnet50.pth', map_location=device), strict=False)
# strict=False allows loading weights without enforcing exact layer matching

# Define the same transformations that were used during training
transform = transforms.Compose([
    transforms.Resize((128, 128)),  # Resize to 128x128
    transforms.ToTensor(),  # Convert image to tensor
    transforms.Normalize(mean=[0.4912, 0.5459, 0.3178], std=[0.1811, 0.1581, 0.2519])  # Normalize image
])

# Load the test dataset
test_dir = r"test"  # Your test dataset directory
test_dataset = datasets.ImageFolder(root=test_dir, transform=transform)

# Function to predict the class of an image
def predict_image(image_path):
    # Check if the image path exists
    if not os.path.exists(image_path):
        print(f"Image file not found: {image_path}")
        return

    # Open and preprocess the image
    img = Image.open(image_path).convert('RGB')  # Ensure the image is in RGB format
    img_tensor = transform(img).unsqueeze(0).to(device)  # Add batch dimension and move to device (GPU/CPU)

    # Set the model to evaluation mode
    model.eval()

    # Make prediction
    with torch.no_grad():  # No need to track gradients for prediction
        output = model(img_tensor)
        _, predicted_class = torch.max(output, 1)

    # Map the predicted class index to your class labels
    class_names = ["augmented-anthracnose_leaf_spot", "augmented-healthy", "augmented-straw_mite"]  # Replace with actual class names
    predicted_label = class_names[predicted_class.item()]

    print(f"Predicted class: {predicted_label}")
    plt.imshow(img)
    plt.title(f"Predicted: {predicted_label}")
    plt.axis('off')  # Turn off axis
    plt.show()

    return predicted_label
        
# Test the prediction with an image
image_path = r"test\augmented-anthracnose_leaf_spot\augmented-anthracnose_leaf_spot (18).jpg"  # Replace with your image path
predicted_class = predict_image(image_path)
