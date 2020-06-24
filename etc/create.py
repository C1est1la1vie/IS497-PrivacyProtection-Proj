import sys
from etc.cryp import *
from etc.mainwindow import *
from PyQt5 import QtCore, QtGui, QtWidgets
sys.path.append("./etc/")

class Ui_createpwd(object):

    def retranslateUi(self, createpwd):
        _translate = QtCore.QCoreApplication.translate
        createpwd.setWindowTitle("添加新密码")
        self.label.setText("添加新密码")
        self.label_2.setText("网址")
        self.label_3.setText("用户名")
        self.label_4.setText("密码")
        self.label_5.setText("备注")
        self.pushSave.setText("保存")


    def reject(self):
        core.sessioncheck()
        self.close()
        return False
        

    def newpassword(self):
        core.sessioncheck()        
        project = self.lineProject.text()        
        username = self.lineUsername.text()
        password = self.linePassword.text()
        notes = self.lineNotes.text()
        if project == '':
            self.label_Msg.setText("网址为空")
            self.repaint()
            return None
        if username == '':
            self.label_Msg.setText("用户名为空")
            self.repaint()
            return None
        if password == '':
            self.label_Msg.setText("密码为空")
            self.repaint()
            return None


        p = core.hash_password(password)
        

        date = core.now()
        df = pd.read_csv(filetemp, header=0)
        did = df['序号']
        nid = len(df)              
        for idd in did:
            if idd == nid:
                nid = 1+nid
            else:
                nid = nid


        ndate = "{}/{}/{}".format(date[1],date[2], date[3])
        df.loc[nid] = [nid, project, username, p, notes, ndate]

        try:
            with open(filetemp, 'w') as f:
                df.to_csv(f,sep=',', encoding=encoding,index=False, mode='a')
                f.close()

                admpwd = df['密码'][0]
                password = core.detemppwd(admpwd)
                keyfile = core.decrypt(password)        
                pyAesCrypt.encryptFile(filetemp, filename, keyfile, bufferSize) 
                
                self.label_Msg.setText("")
                self.lineProject.setText("")
                self.lineUsername.setText("")
                self.linePassword.setText("")
                self.lineNotes.setText("")
                core.sessioncheck()
                self.repaint()
        except:            
            self.label_Msg.setText("")
            self.repaint()
            core.sessioncheck()
        self.close()
        return None

    def setupUi(self, createpwd):
        createpwd.setObjectName("createpwd")
        createpwd.resize(354, 290)
        createpwd.setWindowModality(QtCore.Qt.ApplicationModal)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(createpwd.sizePolicy().hasHeightForWidth())
        createpwd.setSizePolicy(sizePolicy)
        createpwd.setMaximumSize(QtCore.QSize(354, 290))
        self.label = QtWidgets.QLabel(createpwd)
        self.label.setGeometry(QtCore.QRect(50, 0, 251, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(createpwd)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 81, 30))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(createpwd)
        self.label_3.setGeometry(QtCore.QRect(20, 90, 81, 30))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(createpwd)
        self.label_4.setGeometry(QtCore.QRect(20, 130, 81, 30))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(createpwd)
        self.label_5.setGeometry(QtCore.QRect(20, 170, 81, 30))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.lineProject = QtWidgets.QLineEdit(createpwd)
        self.lineProject.setGeometry(QtCore.QRect(110, 50, 201, 30))
        self.lineProject.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.lineProject.setObjectName("lineProject")
        self.lineUsername = QtWidgets.QLineEdit(createpwd)
        self.lineUsername.setGeometry(QtCore.QRect(110, 90, 201, 30))
        self.lineUsername.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.lineUsername.setObjectName("lineUsername")

        self.linePassword = QtWidgets.QLineEdit(createpwd)
        self.linePassword.setGeometry(QtCore.QRect(110, 130, 201, 30))
        self.linePassword.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.linePassword.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.linePassword.setObjectName("linePassword")

        self.lineNotes = QtWidgets.QLineEdit(createpwd)
        self.lineNotes.setGeometry(QtCore.QRect(110, 170, 201, 30))
        self.lineNotes.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.lineNotes.setObjectName("lineNotes")
        self.pushSave = QtWidgets.QPushButton(createpwd)
        self.pushSave.setGeometry(QtCore.QRect(120, 230, 110, 41))
        self.pushSave.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.pushSave.setObjectName("pushSave")

        self.label_Msg = QtWidgets.QLabel(createpwd)
        self.label_Msg.setGeometry(QtCore.QRect(0, 210, 351, 41))

        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_Msg.setFont(font)
        self.label_Msg.setText("")
        self.label_Msg.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Msg.setObjectName("label_Msg")

        self.retranslateUi(createpwd)
        QtCore.QMetaObject.connectSlotsByName(createpwd)
        self.pushSave.clicked.connect(self.newpassword)
