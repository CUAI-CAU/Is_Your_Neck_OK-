'''
작동법
step1. 이미지에서 귀와 목(경추) 부분을 마우스로 클릭한다.
step2. 클릭이 끝나면 esc 버튼을 누른다.
step3. step1과 step2의 과정을 반복한다.
'''

import cv2 as cv
from PIL import Image
import os
import glob
import math
import numpy as np
import pandas as pd

from data import x_points, y_points

labels = [] # 최종 라벨값 모아둘 리스트
front_images = []  # 정면 이미지 파일을 모아둘 리스트
side_images = []  # 측면 이미지 파일을 모아둘 리스트
img_angle = [] # 전방머리자세각도 모아둘 리스트

# 좌표를 모아둘 리스트
x_points = []
y_points = []


def mouse_callback(event, x, y, flags, param):
    if (event == cv.EVENT_LBUTTONUP) :
        print("x :", x, "y :", y)
        x_points.append(x)
        y_points.append(y)


# 이미지 폴더 주소를 입력받아서 이미지 순회하기
def find_point(num, s_path):
    # 파일 열기
    print("num : ", num)
    # 이미지 탐색하며 좌표 찾기(수동으로)
    # 이미지 하나씩 받아오기
    img = cv.imread(s_path)
    cv.namedWindow('image')  # 마우스 이벤트 영역 윈도우 생성
    cv.setMouseCallback('image', mouse_callback)

    # 받아온 이미지 보여주고 마우스 클릭하여 좌표 찾기
    while(True):
        cv.imshow('image',img)
        k = cv.waitKey(1) & 0xFF
        if k == 27:    # ESC 키 눌러졌을 경우 종료
            break
    cv.destroyAllWindows()


def cal_turtle():
    # 거북목 판단 시작
    for i in range(0, len(x_points), 2):
        x1 = x_points[i]
        y1 = y_points[i]
        x2 = x_points[i+1]
        y2 = y_points[i+1]
        x = abs(x1 - x2)
        y = abs(y1 - y2)
        rad = np.arctan(y / x)  # 단위는 라디안
        CVangle = 180 * rad / math.pi  # 도 단위로 변경
        img_angle.append(CVangle)

        if CVangle <= 50:
            labels.append(1) # 거북목 자세
        else:
            labels.append(0) # 올바른 자세


if __name__ == '__main__':
    for i in range(100, 105):   # (a, b) : a부터 1씩 늘려가며 b가 될 때까지 반복
        s_path = './data/hy_data/HY' + str(i) + 'side.jpg'
        f_path = './HY' + str(i) + 'front.jpg'
        side_images.append(s_path)
        front_images.append(f_path)
        find_point(i, s_path=s_path)

    cal_turtle()
    # csv 파일로 저장
    df = pd.DataFrame()
    df['fname'] = front_images
    df['angle'] = img_angle
    df['labels'] = labels
    df.to_csv('./label1.csv')





