''' 장비 준비 '''
import numpy as np
import os
from PIL import Image
import torch
from torchvision import transforms, datasets
from torch.utils.data import Subset, DataLoader
from torch.utils.data import Dataset
import torchvision.models as models\

PATH = './model/weight/'
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = models.resnet18()
optimizer = torch.optim.Adam(model.parameters(), lr=0.002)

#model = torch.load(PATH + 'model.pt')  # 전체 모델을 통째로 불러옴, 클래스 선언 필수
model = torch.load(PATH + 'model.pt', map_location='cpu') # cpu only

#model.load_state_dict(torch.load(PATH + 'model_state_dict.pt'))  # state_dict를 불러 온 후, 모델에 저장
#checkpoint = torch.load(PATH + 'all.tar')   # dict 불러오기
#model.load_state_dict(checkpoint['model'])
#optimizer.load_state_dict(checkpoint['optimizer'])

model.to(DEVICE)


image_list = []
prediction_list = []
output_list = []
    
def evaluate(model, test_loader):
    model.eval()
    num_of_mini_batch = len(test_loader)
    no_count = 0
    yes_count = 0
    
    with torch.no_grad():
        for image in test_loader :
            image_list.append(image)
            image = image.to(DEVICE)
            output = model(image)
            
            prediction = output.max(1, keepdim = True)[1]
            if prediction == 0:
                no_count +=1
            else:
                yes_count+=1
                
            prediction_list.append(prediction.detach().cpu().numpy())
            output_list.append(output.detach().cpu().numpy())
    
    return no_count, yes_count

''' 데이터셋 준비 '''
path = './dataset' # 불러올 데이터셋 경로 를 수정하여야 함.
file_names = os.listdir(path)

# 폴더 안의 이미지 데이터 불러오기
class custom_dataset(Dataset):
    def __init__(self, path, file_names, transform=None):
        self. root_dir = path
        self.transform = transform
    
    def __len__(self):
        return len(file_names)
    
    def __getitem__(self,idx):
        image_name = self.root_dir + '/' + file_names[idx]
        image = Image.open(image_name)
        
        if self.transform != None:
            image = self.transform(image)
        
        return image
    
dataset = custom_dataset(path, file_names,
                              transform = transforms.Compose([
                                  transforms.Resize((224,224)),
                                  transforms.RandomHorizontalFlip(p=0.3),
                                  transforms.RandomGrayscale(p=0.1),
                                  transforms.ToTensor(),
                                  transforms.Normalize([0.4, 0.4, 0.4], [0.2, 0.2, 0.2])
                              ]))

"""
dataset = datasets.ImageFolder(root = path,
                              transform = transforms.Compose([
                                  transforms.Resize((224,224)),
                                  transforms.RandomHorizontalFlip(p=0.3),
                                  transforms.RandomGrayscale(p=0.1),
                                  transforms.ToTensor(),
                                  transforms.Normalize([0.4, 0.4, 0.4], [0.2, 0.2, 0.2])
                              ]))
"""

test_idx = list(range(len(dataset)))
test_data = Subset(dataset, test_idx)

# 학습/평가용 데이터 생성 완료
test_loader = DataLoader(test_data, batch_size = 1, shuffle = False)

no_count, yes_count = evaluate(model, test_loader)

checklist = []

for i in range(len(output_list)):
    checklist.append((list(output_list[i])[0][0])-(list(output_list[i])[0][1]))

checklist = np.array(checklist)

ratio = (no_count / (no_count + yes_count)) * 100 # 정상 비율

comment = "./dataset/"+str(file_names[checklist.argmax()])+"!./dataset/"+str(file_names[checklist.argmin()])+"!" + str(ratio)

with open("turtle_result.txt", "w") as f:
    f.write(comment)
    f.close()

#print(file_names[checklist.argmax()], file_names[checklist.argmin()]) 
# 왼쪽이 정상 경향이 가장 큰 사진 인덱스, 오른쪽이 거북목 경향이 가장 큰 사진 인덱스

#print(no_count, yes_count) 
# 왼쪽이 정상 사진 갯수, 오른쪽이 거북목 사진 갯수.
