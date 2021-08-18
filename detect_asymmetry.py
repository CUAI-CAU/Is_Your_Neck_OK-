import numpy as np
import math

import glob
from PIL import Image

import torch
import torchvision
from torchvision import models

'''
- input
    path : 이미지가 들어있는 폴더 경로
    
- output 
    most_asymmetric_image : 어깨 비대칭 정도가 가장 심한 이미지 경로(str).
    most_crooked_image : 어깨 중심을 기준으로 자세 삐뚤어짐(치우침) 정도가 가장 심한 이미지 경로(str).
    most_crooked_degree : 어깨 중심을 기준으로 치우짐 정도(numpy.float64).
    most_crooked_direction : 자세가 삐뚤어진 방향(str). 'right' or 'left'
'''

def detect_asymmetry(path):
    asymmetry_record = {} # {어깨 높이 차 : '이미지 경로'}
    crooked_record = {} # {삐뚤어진 정도 : ('이미지 경로', 삐뚤어진 방향)}

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = models.detection.keypointrcnn_resnet50_fpn(pretrained=True).to(device).eval()
    # Convert to tensor
    trf = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor()
    ])

    # Import all images contained in a folder with path
    all_imgs = []
    images = glob.glob(path)
    for fname in images:
        all_imgs.append(fname)
    
    # Travelling images in the list
    for fname in all_imgs:
        img = Image.open(fname)
        input_img = trf(img).to(device)  # CPU to GPU
        out = model([input_img])[0]
        THRESHOLD = 0.9  # use only 90% or more accuracy

        # Find key points of shoulders and nose
        for box, score, keypoints in zip(out['boxes'], out['scores'], out['keypoints']):
            score = score.detach().cpu().numpy()  # GPU to CPU
            if score < THRESHOLD:
                continue
            # box = box.detach().cpu().numpy()
            keypoints = keypoints.detach().cpu().numpy()[:, :2]  # GPU to CPU

            # Find coordinates of shoulders and nose
            for i, k in enumerate(keypoints):
                # Left shoulder
                if i == 5:
                    left_shoulder = k
                # Right shoulder
                elif i == 6:
                    right_shoulder = k
                # Nose
                elif i == 0:
                    nose = k

        # Shoulder asymmetry posture
        distance = round(abs(left_shoulder[1] - right_shoulder[1]),2) # height distance
        asymmetry_record[distance] = fname # add to dictionary

        # Crooked posture
        mid_Xpoint = (left_shoulder[0] + right_shoulder[0]) / 2 # shoulder midpoint
        nose_Xpoint = nose[0]
        crooked_direction = 'left' if ((nose_Xpoint - mid_Xpoint) < 0) else 'right'
        crooked_degree = round(100 * abs(mid_Xpoint - nose_Xpoint) / abs(mid_Xpoint - right_shoulder[0]),2)
        crooked_record[crooked_degree] = (fname, crooked_direction) # add to dictionary

    # Find most asymmetric image
    sorted_asymmetry_record = sorted(asymmetry_record.items(), reverse=True)
    most_asymmetric_image = sorted_asymmetry_record[0][1]

    # Find most crooked image, degree, direction
    sorted_crooked_record = sorted(crooked_record.items(), reverse=True)
    most_crooked_image = (sorted_crooked_record[0][1])[0]
    most_crooked_direction = (sorted_crooked_record[0][1])[1]
    most_crooked_degree = sorted_crooked_record[0][0]

    # Return most asymmetric image, most crooked image, crooked degree, crooked direction
    return most_asymmetric_image, most_crooked_image, most_crooked_degree, most_crooked_direction