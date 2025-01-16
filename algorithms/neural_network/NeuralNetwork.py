import os
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from PIL import Image
from algorithms.neural_network.CNN import CNN

def train():
    num_epochs = 10

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * images.size(0)
        
        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_dataset):.4f}")
    print("Finished Training")
    torch.save(model.state_dict(), "trained_model.pth")
    
def test():
    model.load_state_dict(torch.load("trained_model.pth"))
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    print(f"Accuracy: {100 * correct / total}%")

def predict(image_path):
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0).to(device)
    model.eval()
    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)
        class_index = predicted.item()
        class_name = train_dataset.classes[class_index]
        return class_name

transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

train_data_path = "data/train"
test_data_path = "data/test"

train_dataset = torchvision.datasets.ImageFolder(root=train_data_path, transform=transform)
test_dataset = torchvision.datasets.ImageFolder(root=test_data_path, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = CNN().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

model_path = "trained_model.pth"
num_epochs = 10

if os.path.exists(model_path):
    model.load_state_dict(torch.load(model_path))
    print("Model loaded from file.")
else:
    print("Training model...")
    model.train()
    print("Model saved to file.")


