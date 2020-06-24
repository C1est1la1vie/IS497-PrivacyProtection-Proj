import sys
from etc.cryp import *
from etc.mainwindow import *
from PyQt5 import QtWidgets
sys.path.append("./etc/")

class Ui_DialogDelete(object):

    def retranslateUi(self, DialogDelete):
        _translate = QtCore.QCoreApplication.translate
        DialogDelete.setWindowTitle("删除密码")
        self.label.setText("确认是否删除")
        self.pushButtonOk.setText("OK")
        self.pushButtonCancel.setText("取消")


    def reject(self):
        self.close()
        return False      
    

    def accept(self):
        delete = self.label_id.text()
        delete = int(delete)

        if delete == '0':
            self.tablemsg.setText("删除失败")
            self.repaint()
            self.close()
            core.sessioncheck()
            return False
        else:
            df = pd.read_csv(filetemp)
            df.drop(df.loc[df['序号']==delete].index, inplace=True)
            with open(filetemp, 'w') as f:
                df.to_csv(f,sep=',', encoding=encoding,index=False, mode='a')
                f.close()
                df = pd.read_csv(filetemp,index_col='序号')

                admpwd = df['密码'][0]
                password = core.detemppwd(admpwd)
                keyfile = core.decrypt(password)        
                pyAesCrypt.encryptFile(filetemp, filename, keyfile, bufferSize) 
                #self.pushButtonOk.hide()
                self.pushButtonCancel.setText("退出")
                self.label.setText("删除记录")
                self.repaint()
                core.sessioncheck()
                self.close()
            return True

        return None

    def setupUi(self, DialogDelete):
        DialogDelete.setObjectName("DialogDelete")
        DialogDelete.resize(391, 120)
        DialogDelete.setWindowModality(QtCore.Qt.ApplicationModal)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogDelete.sizePolicy().hasHeightForWidth())
        DialogDelete.setSizePolicy(sizePolicy)
        DialogDelete.setMinimumSize(QtCore.QSize(391, 120))
        DialogDelete.setMaximumSize(QtCore.QSize(391, 120))
        self.label = QtWidgets.QLabel(DialogDelete)
        self.label.setGeometry(QtCore.QRect(10, 0, 371, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.tablemsg = QtWidgets.QLabel(DialogDelete)
        self.tablemsg.setGeometry(QtCore.QRect(10, 20, 370, 71))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.tablemsg.setFont(font)
        self.tablemsg.setText("")
        self.tablemsg.setObjectName("tablemsg")

        self.label_id = QtWidgets.QLabel(DialogDelete)
        self.label_id.setGeometry(QtCore.QRect(310, 40, 61, 31))
        self.label_id.setText("")
        self.label_id.setObjectName("label_id")

        self.pushButtonOk = QtWidgets.QPushButton(DialogDelete)
        self.pushButtonOk.setGeometry(QtCore.QRect(100, 80, 81, 32))
        self.pushButtonOk.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.pushButtonOk.setObjectName("pushButtonOk")

        self.pushButtonCancel = QtWidgets.QPushButton(DialogDelete)
        self.pushButtonCancel.setGeometry(QtCore.QRect(200, 80, 81, 32))
        self.pushButtonCancel.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.pushButtonCancel.setObjectName("pushButtonCancel")

        self.label_id.raise_()
        self.label.raise_()
        self.tablemsg.raise_()
        # self.label_2.raise_()
        self.pushButtonOk.raise_()
        self.pushButtonCancel.raise_()

        self.retranslateUi(DialogDelete)
        QtCore.QMetaObject.connectSlotsByName(DialogDelete)

        self.pushButtonOk.clicked.connect(self.accept)
        self.pushButtonCancel.clicked.connect(self.reject)

        core.sessioncheck()
