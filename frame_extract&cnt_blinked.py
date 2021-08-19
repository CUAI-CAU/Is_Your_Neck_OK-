# -*- coding: utf-8 -*-
import cv2
import time
import dlib   # version = 19.22.0
from scipy.spatial import distance as dist
import datetime
import numpy as np

'''
    - output
        : "./dataset/inputN.jpg" -> 60장
        : "./blink_count.txt" -> int, 3분 간 눈 깜박임 횟수
        
'''

JAWLINE_POINTS = list(range(0, 17))
RIGHT_EYEBROW_POINTS = list(range(17, 22))
LEFT_EYEBROW_POINTS = list(range(22, 27))
NOSE_POINTS = list(range(27, 36))
RIGHT_EYE_POINTS = list(range(36, 42))
LEFT_EYE_POINTS = list(range(42, 48))
MOUTH_OUTLINE_POINTS = list(range(48, 61))
MOUTH_INNER_POINTS = list(range(61, 68))

EYE_AR_THRESH = 0.26
EYE_AR_CONSEC_FRAMES = 2
EAR_AVG = 0
COUNTER = 0
TOTAL = 0


def eye_aspect_ratio(eye):
  # euclidean distance between the vertical eye landmarks
  A = dist.euclidean(eye[1], eye[5])
  B = dist.euclidean(eye[2], eye[4])

  # euclidean distance between the horizontal eye landmarks
  C = dist.euclidean(eye[0], eye[3])

  ear = (A + B) / (2 * C)
  return ear


def recording(cap, fps, codec, count, start_time, COUNTER, TOTAL, cnt, start_t):
    while(cap.isOpened()):

        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)  # 화면 반전 0: 상하, 1: 좌우

        if ret == True:
            cv2.imshow('Frame Save', frame)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rects = detector(gray, 0)

            for rect in rects:
                x = rect.left()
                y = rect.top()
                x1 = rect.right()
                y1 = rect.bottom()
                # get the facial landmarks
                landmarks = np.matrix([[p.x, p.y] for p in predictor(frame, rect).parts()])
                # get the left, right eye landmarks
                left_eye = landmarks[LEFT_EYE_POINTS]
                right_eye = landmarks[RIGHT_EYE_POINTS]
                # compute the EAR
                ear_left = eye_aspect_ratio(left_eye)
                ear_right = eye_aspect_ratio(right_eye)
                # compute the average EAR
                ear_avg = (ear_left + ear_right) / 2.0
                # detect the eye blink
                if ear_avg < EYE_AR_THRESH:
                    COUNTER += 1
                else:
                    if COUNTER >= EYE_AR_CONSEC_FRAMES:
                        TOTAL += 1
                    COUNTER = 0

            with open("blink_count.txt", "w") as f:
                f.write(str(TOTAL))
                f.close()

            end_time = datetime.datetime.now()
            diff = (end_time - start_time).seconds

            if time.time() - start_t >= 3:
                cv2.imwrite("./dataset/input%d.jpg" % cnt, frame)
                img = cv2.imread("./dataset/input%d.jpg" % cnt)
                # 중앙 기준으로 정사각형 모양으로 사진 자름
                res = img[0:img.shape[0], int((img.shape[1] / 2) - (img.shape[0] / 2)):int((img.shape[1] / 2) + (img.shape[0] / 2))].copy()
                cv2.imwrite("./dataset/input%d.jpg" % cnt, res)
                print("saved image%d.jpg" % cnt)
                cnt += 1
                start_t = time.time()

            if diff > 186:  # 3분 동안 웹캠에서 프레임 추출
                break
            #k = cv2.waitKey(1) & 0xFF
            #if k == 27:  # ESC 키 눌러졌을 경우 종료
            #    break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('./model/shape_predictor_68_face_landmarks.dat')
    fps = 11
    codec = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
    count = 99
    cnt = 1
    start_time = datetime.datetime.now()
    start_t = time.time()
    recording(cap, fps, codec, count, start_time, COUNTER, TOTAL, cnt, start_t)

