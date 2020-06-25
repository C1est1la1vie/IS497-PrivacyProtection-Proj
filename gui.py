from file_encrypt.FileCrypt import AES_128
from pwbox import *
from base_gui import MainUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QLineEdit, QStackedLayout
from identity.cipher import *
from register.dataRecord import *
from register.dataManage import *
from register.set_user_password import *
import identity.global_vari

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
        self.left_button_6.clicked.connect(self.click_face_collect)
        self.left_button_7.clicked.connect(self.click_build_model)
        self.left_button_9.clicked.connect(self.click_set_user_password)
        self.left_close.clicked.connect(self.close_and_enc)

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
        # self.AES = AES_128()

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

    def click_find_device_location(self): # 4. visual crypto
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

    def close_and_enc(self):
        try:
            sno = identity.global_vari.login_sno
            key = identity.global_vari.login_password

            base_dir = r"./identity/datasets"
            img_dir = base_dir + "\\" + "stu_" + sno
            lists = os.listdir(img_dir)
            for img in lists:
                path = img_dir + "\\" + img
                enc_pic(key,path)

            self.close()
        except Exception as err:
            print(err)

    def click_face_collect(self):
        try:
            logging.config.fileConfig('./identity/config/logging.cfg')
            window = DataRecordUI()
            window.show()
        except Exception as err:
            print(err)

    def click_build_model(self):
        try:
            logging.config.fileConfig('./identity/config/logging.cfg')
            window = DataManageUI()
            window.show()
        except Exception as err:
            print(err)

    def click_password_book(self):
        self.controler=Controller()
        self.controler.show_login()

    def click_set_user_password(self):
        if self.stacked_layout.currentIndex() != 4:
            self.stacked_layout.setCurrentIndex(4)

        self.right_min_info = QtWidgets.QLabel("学号:")
        self.right_layout5.addWidget(self.right_min_info, 1, 1, 1, 1)

        self.lineedit = QLineEdit(self)
        self.right_layout5.addWidget(self.lineedit, 1, 2, 1, 1)
        self.lineedit.setPlaceholderText("输入新用户的学号")

        self.right_min_info2 = QtWidgets.QLabel("密码:")
        self.right_layout5.addWidget(self.right_min_info2, 2, 1, 1, 1)

        self.lineedit2 = QLineEdit(self)
        self.right_layout5.addWidget(self.lineedit2, 2, 2, 1, 1)
        self.lineedit2.setPlaceholderText("输入新用户的密码")

        self.bt = QPushButton('插入', self)
        self.right_layout5.addWidget(self.bt, 3, 1, 1, 1)
        self.bt.clicked.connect(self.insert)

    def insert(self):
        sno = self.lineedit.text()
        password = self.lineedit2.text()
        mysql_insert_data(sno,password)
        QMessageBox.about(self, "通知", "新用户密码插入数据库成功！")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
