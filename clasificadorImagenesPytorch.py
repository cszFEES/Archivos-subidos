import os
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

class sacarImagenesDesdeCarpetas(Dataset):
    def __init__(self, carpeta_raiz, transform=None):
        self.carpeta_raiz = carpeta_raiz
        self.transform = transform
        self.imagenes = [x for sublist in os.listdir(carpeta_raiz) for x in os.listdir(os.path.join(carpeta_raiz,sublist))]
        self.classes = [sublist for sublist in os.listdir(carpeta_raiz) for x in os.listdir(os.path.join(carpeta_raiz,sublist))]
        self.class_to_idx = [i for i, sublist in enumerate(os.listdir(carpeta_raiz)) for x in os.listdir(os.path.join(carpeta_raiz,sublist))]
    def __len__(self):
        return len(self.imagenes)
    def __getitem__(self, idx):
        img_path = os.path.join(self.carpeta_raiz, self.classes[idx], self.imagenes[idx])
        image = Image.open(img_path).convert('L')  #single channel (luminance) image
        image = self.transform(image)
        label = self.class_to_idx[idx]
        return image, label

transformaciones = transforms.Compose([
    transforms.Resize((150, 150)),
    transforms.Grayscale(num_output_channels=1),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5], std=[0.2])
])
dataset = sacarImagenesDesdeCarpetas(carpeta_raiz='/home/USER/Escritorio/DP', transform=transformaciones)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)


from torch import nn
import torch.nn.functional as F

class modeloR(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=4, kernel_size=3, stride=1, padding=1)
        self.conv1_ = nn.Conv2d(in_channels=3, out_channels=4, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(in_channels=4, out_channels=16, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(in_channels=40, out_channels=88, kernel_size=3, stride=1, padding=1)
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(21904, 16)
        self.fc1_ = nn.Linear(916800, 16)
        self.fc2 = nn.Linear(16, 8)
        self.fc3 = nn.Linear(8, 2)

    def forward(self, x):
        try:
            x = self.pool(F.relu(self.conv1(x)))         
        except:
            x = self.pool(F.relu(self.conv1_(x)))         
        x = self.pool(F.relu(self.conv2(x)))       
        #x = self.pool(F.relu(self.conv3(x)))         
        x = self.flatten(x)
        try:
            x = F.relu(self.fc1(x))
        except:
            x = F.relu(self.fc1_(x))
        x = F.relu(self.fc2(x))                   
        x = self.fc3(x)
        return x

    
clasificador = modeloR()
loss_fn = nn.CrossEntropyLoss()
optimizar = torch.optim.SGD(clasificador.parameters())

if __name__ == "__main__":
    for epoch in range(10):
        for batch in dataloader:
            imgsEntrantes, labels = batch
            imgsConvolucionadas = clasificador(imgsEntrantes)
            loss = loss_fn(imgsConvolucionadas, labels)
            optimizar.zero_grad() # Backpropagation
            loss.backward()
            optimizar.step()
        print(f"Epoch:{epoch} loss is {loss.item()}")
    
    torch.save(clasificador.state_dict(), 'modeloManga.pt')

    img = Image.open('0.jpg')
    img_tensor = transforms.ToTensor()(img).unsqueeze(0)
    print(torch.argmax(clasificador(img_tensor)))
