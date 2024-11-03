import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from PIL import Image
from io import BytesIO
import os

# Definindo a arquitetura da CNN
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        # Ajustando o tamanho correto
        self.fc1 = nn.Linear(64 * 56 * 56, 128)  
        # 2 classes: com pneumonia e sem pneumonia
        self.fc2 = nn.Linear(128, 2)  

    def forward(self, x):
        x = nn.functional.relu(self.conv1(x))
        x = nn.functional.max_pool2d(x, 2)
        x = nn.functional.relu(self.conv2(x))
        x = nn.functional.max_pool2d(x, 2)
        # Ajustando o tamanho correto
        x = x.view(-1, 64 * 56 * 56)  
        x = nn.functional.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Verifica se o treinamento será feito em GPU ou CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Defina transformações para pré-processamento
transform = transforms.Compose([
    # Redimensiona as imagens para um tamanho fixo
    transforms.Resize((224, 224)),  
    # Converte as imagens para tensores
    transforms.ToTensor(),  
    # Normaliza as imagens
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  
])

# Verifique se há um modelo previamente treinado para carregar
if os.path.exists('model.pth'):
    model = torch.load('model.pth').to(device)
else:
    # Carrega as imagens usando ImageFolder
    train_data = datasets.ImageFolder('images', transform=transform)
    train_loader = torch.utils.data.DataLoader(train_data, batch_size=32, shuffle=True)

    # Definindo a função de perda e o otimizador
    model = CNN().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Treinando o modelo
    num_epochs = 10
    for epoch in range(num_epochs):
        # Garante que o modelo está em modo de treino
        model.train()  
        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

            # Calculando a acurácia durante o treinamento
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        accuracy = 100 * correct / total
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader):.4f}, Accuracy: {accuracy:.2f}%')

    # Salvando o modelo treinado
    torch.save(model, 'model.pth')

# Função para fazer o diagnostico em uma nova imagem
def diagnosis(image_bytes):
    # Coloca o modelo em modo de avaliação
    model.eval()  
    # Carrega a imagem de bytes e converte para RGB
    image = Image.open(BytesIO(image_bytes)).convert('RGB')  
    # Transforma e adiciona batch dimension
    image = transform(image).unsqueeze(0).to(device)  

    # Desativa o cálculo de gradientes para inferência
    with torch.no_grad():  
        output = model(image)
        _, predicted = torch.max(output, 1)

    if predicted.item() == 0:
        return 'Com pneumonia'
    else:
        return 'Sem pneumonia'