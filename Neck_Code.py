''' 장비 준비 '''
import numpy as np
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms, datasets
import random
from torchsummary import summary
from sklearn.model_selection import train_test_split
from torch.utils.data import Subset, DataLoader
import torchvision.models as models
from efficientnet_pytorch import EfficientNet

PATH = './weight/'
DEVICE = torch.device("cuda")

model = models.resnet18()
optimizer = torch.optim.Adam(model.parameters(), lr=0.002)

model = torch.load(PATH + 'model.pt')  # 전체 모델을 통째로 불러옴, 클래스 선언 필수
model.to(DEVICE)

def evaluate(model, test_loader):
    model.eval()
    num_of_mini_batch = len(test_loader)
    #print(num_of_mini_batch)
    prediction_list = []
    no_count = 0
    yes_count = 0
    
    with torch.no_grad():
        for image, label in test_loader :
            image = image.to(DEVICE)
            #label = label - 1 # GPU 환경에서만 적용
            label = label.to(DEVICE)
            output = model(image)
            prediction = output.max(1, keepdim = True)[1]
            if prediction == 0:
                no_count +=1
            else:
                yes_count+=1
                
            prediction_list.append(prediction)    
    return prediction_list, no_count, yes_count

#seed = 777
#BATCH_SIZE = 32

''' 데이터셋 준비 '''
path = './dataset' # 불러올 데이터셋 경로 를 수정하여야 함.

# 폴더 안의 이미지 데이터 불러오기
dataset = datasets.ImageFolder(root = path,
                              transform = transforms.Compose([
                                  transforms.Resize((224,224)),
                                  transforms.RandomHorizontalFlip(p=0.3),
                                  transforms.RandomGrayscale(p=0.1),
                                  transforms.ToTensor(),
                                  transforms.Normalize([0.4, 0.4, 0.4], [0.2, 0.2, 0.2])
                              ])) 

# train/test data 분리. 사이킷런 train_test_split과 torch.utils.data의 Subset 활용
test_idx = list(range(len(dataset)))
test_data = Subset(dataset, test_idx)

# 학습/평가용 데이터 생성 완료
test_loader = DataLoader(test_data, batch_size = 1, shuffle = False)

prediction_list, no_count, yes_count = evaluate(model, test_loader)
print(no_count, yes_count)
