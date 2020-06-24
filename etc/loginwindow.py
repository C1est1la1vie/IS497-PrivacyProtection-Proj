from etc.mainwindow import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

sys.path.append("./etc/")

class Ui_loginmenu(object):       

    def retranslateUi(self, loginmenu):
        _translate = QtCore.QCoreApplication.translate
        loginmenu.setWindowTitle("登录")
        self.label.setText("用户名")
        self.label_2.setText("密码")
        self.pushButton_ok.setText("OK")
        
    def closeEvent(self, event):        
        try:            
            f = open(sessiontmp,"r")
            pass
        except:
            core.exit_now('','')

    def checkLogin(self, loginmenu):
        username = self.username.text()
        password = self.password.text()
        if not username:
            self.msgdialog.setText("用户名不能为空")
            self.repaint()
            return False
        if not password:
            self.msgdialog.setText("密码不能为空")
            self.repaint()
            return False
        try:

            keyfile = core.decrypt(password)
            pyAesCrypt.decryptFile(filename, filetemp, keyfile, bufferSize)
            df = pd.read_csv(filetemp, index_col=0, header=0, nrows=1)

            if username in df['用户名'][0]:
                if not password:

                    self.repaint()
                    return False

                check = core.verify_password(df['密码'][0], password)
                if check is True and username in df['用户名'][0]:

                    self.repaint()
                    session = core.session()
                    token = session[0]
                    timestamp = session[1]
                    self.switch_window.emit()
                else:
                    self.msgdialog.setText("错误的用户名或密码")
                    self.repaint()
                    return False
            else:
                self.msgdialog.setText("错误的用户名或密码")
                self.repaint()
                return False
        except:
            self.msgdialog.setText("错误的用户名或密码")
            self.repaint()
            return False
        return None

    def setupUi(self, loginmenu):
        loginmenu.setObjectName("loginmenu")
        loginmenu.resize(352, 178)
        loginmenu.setWindowModality(QtCore.Qt.ApplicationModal)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(loginmenu.sizePolicy().hasHeightForWidth())
        loginmenu.setSizePolicy(sizePolicy)
        loginmenu.setMaximumSize(QtCore.QSize(352, 179))
        loginmenu.setAcceptDrops(True)
        self.username = QtWidgets.QLineEdit(loginmenu)
        self.username.setGeometry(QtCore.QRect(140, 50, 141, 21))
        self.username.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.username.setObjectName("username")
        self.password = QtWidgets.QLineEdit(loginmenu)
        self.password.setGeometry(QtCore.QRect(140, 80, 141, 21))
        self.password.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setClearButtonEnabled(True)
        self.password.setObjectName("password")
        self.label = QtWidgets.QLabel(loginmenu)
        self.label.setGeometry(QtCore.QRect(60, 50, 71, 21))
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(loginmenu)
        self.label_2.setGeometry(QtCore.QRect(60, 80, 71, 21))
        self.label_2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.pushButton_ok = QtWidgets.QPushButton(loginmenu)
        self.pushButton_ok.setGeometry(QtCore.QRect(130, 110, 101, 41))
        self.pushButton_ok.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.msgdialog = QtWidgets.QLabel(loginmenu)
        self.msgdialog.setGeometry(QtCore.QRect(20, 150, 321, 16))
        self.msgdialog.setAlignment(QtCore.Qt.AlignCenter)
        self.msgdialog.setObjectName("msgdialog")
        self.msgdialog_2 = QtWidgets.QLabel(loginmenu)
        self.msgdialog_2.setGeometry(QtCore.QRect(25, 10, 321, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.msgdialog_2.setFont(font)
        self.msgdialog_2.setAlignment(QtCore.Qt.AlignCenter)
        self.msgdialog_2.setObjectName("msgdialog_2")
        self.retranslateUi(loginmenu)
        QtCore.QMetaObject.connectSlotsByName(loginmenu)


        self.pushButton_ok.clicked.connect(self.checkLogin)
