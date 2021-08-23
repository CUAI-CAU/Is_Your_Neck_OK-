# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPdfWriter, QPagedPaintDevice, QPainter, QScreen, QPixmap
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtCore import QDate, QDateTime, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import sys
from datetime import datetime


QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)


class MyWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.date = datetime.today().strftime("%Y/%m/%d %H:%M")      # 현재 날짜
        self.setStyleSheet("background-color: white;")  # 배경색 설정


        self.name = str(input("이름을 입력하세요. : "))
        self.birth = str(input("생년월일을 입력하세요. (2000.01.01) : "))
        # 인적사항
        temp = "이름 :   " + self.name + "\n\n생년월일 :   " + self.birth
        self.information = QLabel(temp, self)
        font1 = self.information.font()
        font1.setPointSize(15)
        #font1.setFamily('함초롬돋움')    # 폰트 설정
        self.information.setFont(font1)

        asymmetry = open('./detect_asymmetry_result.txt', 'r').read().split('\n')
        blinked = open('./blink_count.txt', 'r').read()
        temp = open('./turtle_result.txt', 'r').read().split('!')
        mormal_img = temp[0]
        turtle_img = temp[1]
        turtle_ratio = temp[2]
        asymmetry_comment = str(asymmetry[0])
        most_asymmetric_imge = str(asymmetry[1])
        most_crooked_image = str(asymmetry[2])

        analysis = self.name + "님의 3분간 자세 분석 결과입니다. " + self.name + "님의 가장 올바랐던 자세는 <Result 1> 이며 가장 거북이에 " + \
                   "가까웠던 자세는 <Result 2> 입니다.  바른 자세의 비율은 " + turtle_ratio + "%입니다. " + \
                   self.name + "님은 3분 동안 눈을 " + str(blinked) + "번 깜박이셨습니다. " + asymmetry_comment

        self.pixmap = QPixmap('./outbody_logo.png') # 로고
        self.turtle_best = QPixmap(mormal_img)      # 가장 바른 자세
        self.turtle_best = self.turtle_best.scaledToHeight(244)
        self.turtle_worst = QPixmap(turtle_img)     # 거북목 제일 안좋은 자세
        self.turtle_worst = self.turtle_worst.scaledToHeight(244)
        self.asymmetric_image = QPixmap(most_asymmetric_imge)   # 어깨 삐뚤어진 정도가 제일 안좋은 자세
        self.asymmetric_image = self.asymmetric_image.scaledToHeight(244)
        self.crooked_image = QPixmap(most_crooked_image)        # 어깨 가장 기울어진 자세
        self.crooked_image = self.crooked_image.scaledToHeight(244)

        temp = "\n"+self.name+"님의 " + str(self.date) + " OUTBODY 분석 결과"
        self.sub_title = QLabel(temp, self)
        font = self.sub_title.font()
        font.setPointSize(18)
        self.sub_title.setFont(font)

        self.result1 = QLabel("<Result 1>", self)
        self.result2 = QLabel("<Result 2>", self)
        self.result3 = QLabel("<Result 3>", self)
        self.result4 = QLabel("<Result 4>", self)
        self.result1.setAlignment(Qt.AlignHCenter)
        self.result2.setAlignment(Qt.AlignHCenter)
        self.result3.setAlignment(Qt.AlignHCenter)
        self.result4.setAlignment(Qt.AlignHCenter)

        self.comment = QTextBrowser(self)
        self.comment.append(analysis)
        self.comment.setFont(font1)

        self.big_box = QVBoxLayout()

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        # 로고 추가
        self.label = QLabel(self)
        self.label.setPixmap(self.pixmap)  # 이미지 세팅

        # 자세 이미지
        self.normal = QLabel(self)
        self.turtle = QLabel(self)
        self.shoulder = QLabel(self)
        self.crooked = QLabel(self)
        self.normal.setPixmap(self.turtle_best)
        self.turtle.setPixmap(self.turtle_worst)
        self.shoulder.setPixmap(self.asymmetric_image)
        self.crooked.setPixmap(self.crooked_image)

        # 컨트롤 박스 레이아웃 배치
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.information)

        middle_picture = QGridLayout()

        middle_picture.addWidget(self.normal, 0, 0)
        middle_picture.addWidget(self.turtle, 0, 1)
        middle_picture.addWidget(self.result1, 1, 0)
        middle_picture.addWidget(self.result2, 1, 1)
        middle_picture.addWidget(self.shoulder, 2, 0)
        middle_picture.addWidget(self.crooked, 2, 1)
        middle_picture.addWidget(self.result3, 3, 0)
        middle_picture.addWidget(self.result4, 3, 1)
        # middle_picture.addWidget("결과", 2,0)

        vbox.addWidget(self.sub_title)
        vbox.addWidget(self.comment)


        self.big_box.addLayout(layout)
        #big_box.addLayout(picture_comment)
        self.big_box.addLayout(middle_picture)
        self.big_box.addLayout(vbox)
        self.setLayout(self.big_box)
        self.resize(500, 880)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec_())


