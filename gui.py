import sys
import os
import requests
import json
from time import ctime, sleep
import qtawesome
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QButtonGroup, QFrame, QToolButton, QStackedLayout,\
    QWidget, QStatusBar, QComboBox, QLineEdit, QTextBrowser, QTextEdit

from base_gui import MainUi
from cipher import *
from clipboard_process import *
from url_record import *
from identity.dataRecord import *
from identity.dataManage import *


class GUI(MainUi):
    def __init__(self):
        super(GUI, self).__init__()
        # 左边面板按钮触发函数，可以是import进来的，也可以是类内的
        self.left_button_3.clicked.connect(self.click_url_record)
        self.left_button_5.clicked.connect(self.click_mar_word)
        self.left_button_6.clicked.connect(self.click_face_collect)
        self.left_button_7.clicked.connect(self.click_build_model)

        # 多个窗口切换
        self.stacked_layout = QStackedLayout(self.right_widget)

        self.main_frame1 = QWidget()
        self.right_layout = QtWidgets.QGridLayout()
        self.main_frame1.setLayout(self.right_layout)

        self.main_frame2 = QWidget()
        self.right_layout2 = QtWidgets.QGridLayout()
        self.main_frame2.setLayout(self.right_layout2)

        self.stacked_layout.addWidget(self.main_frame1)
        self.stacked_layout.addWidget(self.main_frame2)

    def click_mar_word(self):  # 火星文
        if self.stacked_layout.currentIndex() != 1:
            self.stacked_layout.setCurrentIndex(1)
        # 最好显示在主界面右边窗口，而不是单独跳一个窗口出来
        # 这是在右边面板添加一个按钮，并且connect相关函数的一个例子
        self.bt_on = QPushButton('开启', self)
        self.right_layout2.addWidget(self.bt_on, 1, 0, 1, 1)
        self.bt_on.clicked.connect(self.mar_mode_on)

    def click_url_record(self):  # 浏览记录
        if self.stacked_layout.currentIndex() != 0:
            self.stacked_layout.setCurrentIndex(0)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
