from PyQt5.QtWidgets import QStackedLayout,QWidget
from PyQt5 import QtCore, QtWebEngineWidgets
from base_gui import MainUi
from file_encrypt.FileCrypt import AES_128
from pwbox import *

class GUI(MainUi):
    def __init__(self):
        super(GUI, self).__init__()
        # 左边面板按钮触发函数，可以是import进来的，也可以是类内的
        self.left_button_1.clicked.connect(self.click_password_book)
        self.left_button_2.clicked.connect(self.click_PrivateFiles)
        self.left_button_3.clicked.connect(self.click_browser_history)
        self.left_button_4.clicked.connect(self.click_visual_crypt)
        self.left_button_5.clicked.connect(self.click_mar_word)
        self.left_button_8.clicked.connect(self.click_find_device_location)

        # 多个窗口切换
        self.stacked_layout = QStackedLayout(self.right_widget)

        self.main_frame1 = QWidget()
        self.right_layout = QtWidgets.QGridLayout()
        self.main_frame1.setLayout(self.right_layout)

        self.main_frame2 = QWidget()
        self.right_layout2 = QtWidgets.QGridLayout()
        self.main_frame2.setLayout(self.right_layout2)

        self.main_frame3 = QWidget()
        self.right_layout3 = QtWidgets.QGridLayout()
        self.main_frame3.setLayout(self.right_layout3)

        self.main_frame4 = QWidget()
        self.right_layout4 = QtWidgets.QGridLayout()
        self.main_frame4.setLayout(self.right_layout4)
        self.FileRecorder = []
        self.AES = AES_128()

        self.main_frame5 = QWidget()
        self.right_layout5 = QtWidgets.QGridLayout()
        self.main_frame5.setLayout(self.right_layout5)

        self.main_frame6 = QWidget()
        self.right_layout6 = QtWidgets.QGridLayout()
        self.main_frame6.setLayout(self.right_layout6)

        self.stacked_layout.addWidget(self.main_frame1)
        self.stacked_layout.addWidget(self.main_frame2)
        self.stacked_layout.addWidget(self.main_frame3)
        self.stacked_layout.addWidget(self.main_frame4)
        self.stacked_layout.addWidget(self.main_frame5)
        self.stacked_layout.addWidget(self.main_frame6)

    def click_find_device_location(self):
        try:
            from track import track_gui
            if self.stacked_layout.currentIndex() != 5:
                self.stacked_layout.setCurrentIndex(5)
            track_gui.find_device_location(self)
        except Exception as err:
            print(err)

    def click_visual_crypt(self):       # 4. visual crypto
        from vc import vc_gui
        if self.stacked_layout.currentIndex() != 1:
            self.stacked_layout.setCurrentIndex(1)
        vc_gui.show_visual_crypt(self)

    def click_browser_history(self):  # 3. browser_history
        from browser import browser_gui
        if self.stacked_layout.currentIndex() != 0:
            self.stacked_layout.setCurrentIndex(0)
        browser_gui.show_browser_history(self)

    def click_mar_word(self):  # 5. mar_word_talk
        from mar import mar_gui
        if self.stacked_layout.currentIndex() != 2:
            self.stacked_layout.setCurrentIndex(2)
        mar_gui.show_mar_gui(self)

    def click_PrivateFiles(self):  # 2. private_files
        try:
            from file_encrypt import file_gui
            if self.stacked_layout.currentIndex() != 3:
                self.stacked_layout.setCurrentIndex(3)
            file_gui.file_encrypt_gui(self)
        except Exception as err:
            print(err)

    def click_password_book(self):
        if self.stacked_layout.currentIndex() != 4:
            self.stacked_layout.setCurrentIndex(4)
        self.controler=Controller()
        self.controler.show_login()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
