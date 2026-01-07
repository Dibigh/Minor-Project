import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
import torchvision.datasets as datasets
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

# Check if CUDA (GPU) is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load pre-trained ResNet-50 model
import torchvision.models as models
model = models.resnet50(pretrained=True)

# Modify the final layer (fully connected layer) to match the number of classes in your dataset
model.fc = nn.Linear(model.fc.in_features, 3)  # Assuming you have 3 classes (spinach diseases)

# Move the model to the GPU if available
model = model.to(device)

# Define the loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Tracking lists for loss and accuracy
train_losses = []
train_accuracies = []
val_losses = []
val_accuracies = []

# Data transformations
transform_train = transforms.Compose([
    transforms.Resize((128, 128)),  # Resize to 128x128
    transforms.ToTensor(),  # Convert images to tensors
    transforms.Normalize(mean=[0.4912, 0.5459, 0.3178], std=[0.1811, 0.1581, 0.2519])  # Normalize images
])

transform_val_test = transforms.Compose([
    transforms.Resize((128, 128)),  # Resize to 128x128
    transforms.ToTensor(),  # Convert images to tensors
    transforms.Normalize(mean=[0.4912, 0.5459, 0.3178], std=[0.1811, 0.1581, 0.2519])  # Normalize images
])

# Load datasets
train_dir = r"train"  # Update with your train directory
val_dir = r"val"  # Update with your validation directory
test_dir = r"test"  # Update with your test directory

train_dataset = datasets.ImageFolder(root=train_dir, transform=transform_train)
val_dataset = datasets.ImageFolder(root=val_dir, transform=transform_val_test)
test_dataset = datasets.ImageFolder(root=test_dir, transform=transform_val_test)

# DataLoaders for training, validation, and testing
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

# Training loop
num_epochs = 10
for epoch in range(num_epochs):
    model.train()  # Set the model to training mode
    running_train_loss = 0.0
    correct_train = 0
    total_train = 0

    # Training phase
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)  # Move to device (GPU/CPU)
        optimizer.zero_grad()  # Clear previous gradients
        outputs = model(images)  # Forward pass
        loss = criterion(outputs, labels)  # Compute loss
        loss.backward()  # Backward pass
        optimizer.step()  # Update weights

        running_train_loss += loss.item()
        _, predicted = torch.max(outputs, 1)
        total_train += labels.size(0)
        correct_train += (predicted == labels).sum().item()

    # Calculate average training loss and accuracy
    avg_train_loss = running_train_loss / len(train_loader)
    train_accuracy = 100 * correct_train / total_train
    train_losses.append(avg_train_loss)
    train_accuracies.append(train_accuracy)

    # Validation phase
    model.eval()  # Set the model to evaluation mode
    running_val_loss = 0.0
    correct_val = 0
    total_val = 0
    with torch.no_grad():  # No gradients needed during evaluation
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            running_val_loss += loss.item()

            _, predicted = torch.max(outputs, 1)
            total_val += labels.size(0)
            correct_val += (predicted == labels).sum().item()

    # Calculate average validation loss and accuracy
    avg_val_loss = running_val_loss / len(val_loader)
    val_accuracy = 100 * correct_val / total_val
    val_losses.append(avg_val_loss)
    val_accuracies.append(val_accuracy)

    # Print epoch results
    print(f"Epoch [{epoch+1}/{num_epochs}], Train Loss: {avg_train_loss:.4f}, Train Accuracy: {train_accuracy:.2f}%, Val Loss: {avg_val_loss:.4f}, Val Accuracy: {val_accuracy:.2f}%")

# Step 1: Plot training and validation loss curve after training
plt.figure(figsize=(10, 5))
plt.plot(range(1, num_epochs + 1), train_losses, label='Training Loss')
plt.plot(range(1, num_epochs + 1), val_losses, label='Validation Loss')
plt.title("Training and Validation Loss Curve")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()

# Step 2: Plot training and validation accuracy curve after training
plt.figure(figsize=(10, 5))
plt.plot(range(1, num_epochs + 1), train_accuracies, label='Training Accuracy')
plt.plot(range(1, num_epochs + 1), val_accuracies, label='Validation Accuracy')
plt.title("Training and Validation Accuracy Curve")
plt.xlabel("Epochs")
plt.ylabel("Accuracy (%)")
plt.legend()
plt.show()

# Save the model's state_dict after training
torch.save(model.state_dict(), 'spinach_disease_detection_resnet50.pth')
print("Model saved as 'spinach_disease_detection_resnet50.pth'")

# Optionally, you can also save the accuracy and loss data to a file (e.g., pickle or CSV)
import pickle
with open('accuracy_data_resnet50.pkl', 'wb') as f:
    pickle.dump({
        'train_accuracies': train_accuracies,
        'val_accuracies': val_accuracies,
        'train_losses': train_losses,
        'val_losses': val_losses
    }, f)

print("Accuracy and loss data saved to 'accuracy_data_resnet50.pkl'")
