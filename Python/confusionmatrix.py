import torch
import torchvision.transforms as transforms
import torchvision.datasets as datasets
from torch.utils.data import DataLoader
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Check if CUDA (GPU) is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load the saved model
import torchvision.models as models
model = models.resnet50(pretrained=False)  # Do not load pretrained weights

# Modify the final layer to match the number of classes in your dataset (3 classes)
model.fc = torch.nn.Linear(model.fc.in_features, 3)

# Load the saved model's state_dict
model.load_state_dict(torch.load('spinach_disease_detection_resnet50.pth'))
model = model.to(device)

# Set model to evaluation mode
model.eval()

# Data transformations for test data (must be the same as during training)
transform_test = transforms.Compose([
    transforms.Resize((128, 128)),  # Resize to 128x128
    transforms.ToTensor(),  # Convert images to tensors
    transforms.Normalize(mean=[0.4912, 0.5459, 0.3178], std=[0.1811, 0.1581, 0.2519])  # Normalize images
])

# Load test dataset
test_dir = r"test"  # Update with your test directory
test_dataset = datasets.ImageFolder(root=test_dir, transform=transform_test)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

# Collect predictions and true labels
true_labels = []
predictions = []

with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)
        
        true_labels.extend(labels.cpu().numpy())
        predictions.extend(predicted.cpu().numpy())

# Compute confusion matrix
cm = confusion_matrix(true_labels, predictions)

# Plot confusion matrix
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=test_dataset.classes, yticklabels=test_dataset.classes)
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()

# Print the confusion matrix values
print("Confusion Matrix:")
print(cm)

# Print the classification report in the desired format
print("\nClassification Report:")
report = classification_report(true_labels, predictions, target_names=test_dataset.classes)
print(report)
