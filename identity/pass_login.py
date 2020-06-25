from PyQt5 import QtCore
from gui import *
import pymysql
import hashlib
import os
import identity.global_vari

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow,self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.gui = GUI()
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 130)
        MainWindow.setWindowIcon(QIcon('./identity/logo.png'))
        MainWindow.setStyleSheet("background-image:url(Background.jpg)")
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit.setGeometry(QtCore.QRect(250, 20, 150, 20))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(250, 50, 150, 20))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(180, 24, 30, 14))
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(180, 54, 30, 14))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(190, 90, 75, 23))

        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_2.setGeometry(QtCore.QRect(290, 90, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralWidget)

        self.pushButton.clicked.connect(self.word_get)
        self.pushButton_2.clicked.connect(MainWindow.close)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "密码认证"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "请输入学号"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "请输入密码"))
        self.label.setText(_translate("MainWindow", "学号"))
        self.label_2.setText(_translate("MainWindow", "密码"))
        self.pushButton.setText(_translate("MainWindow", "确定"))
        self.pushButton_2.setText(_translate("MainWindow", "取消"))

    def word_get(self):
        try:
            identity.global_vari.login_sno = self.lineEdit.text()
            identity.global_vari.login_password = self.lineEdit_2.text()

            db = pymysql.connect("localhost", "root", "123", "clients", charset='utf8')
            cursor = db.cursor()
            sql = "select password from user where sno = %s"
            cursor.execute(sql, identity.global_vari.login_sno)
            result = cursor.fetchall()

            m = hashlib.md5()
            m.update(identity.global_vari.login_password.encode('utf-8'))
            password_hash = m.hexdigest()

            if len(result)==0:
                QMessageBox.warning(self,
                                                "警告",
                                                "用户名不存在！",
                                                QMessageBox.Yes)
            elif result[0][0]!=password_hash:
                QMessageBox.warning(self,
                                    "警告",
                                    "用户名或密码错误！",
                                    QMessageBox.Yes)
            else:

                self.close()
                sno = identity.global_vari.login_sno
                key = identity.global_vari.login_password

                base_dir = r"./identity/datasets"
                img_dir = base_dir + "/" + "stu_" + sno
                lists = os.listdir(img_dir)
                for img in lists:
                    path = img_dir + "/" + img
                    dec_pic(key, path)

                self.gui.show()

        except Exception as err:
            print(err)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    gui = GUI()
    ui.show()
    sys.exit(app.exec_())