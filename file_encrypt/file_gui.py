import socket
import os
from file_encrypt.FileCrypt import AES_128
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton,QListWidget,QFileDialog
import time
from file_encrypt.FileClient import *
def file_encrypt_gui(self):
    try:
        self.FileRecorder = []
        Download("127.0.0.1",23456,"FileRecord")
        f = open("FileRecord","r")
        while 1:
            a = f.readline().strip()
            if a != "":
                self.FileRecorder.append(a)
            else:
                break
        f.close()

        self.Encrpty = QPushButton('添加私密文件',self)
        self.right_layout4.addWidget(self.Encrpty,5,0,1,1)
        self.Encrpty.clicked.connect(lambda: FileToPrivate(self))

        self.Decrpty = QPushButton('解除私密文件',self)
        self.right_layout4.addWidget(self.Decrpty,6,0,1,1)
        self.Decrpty.clicked.connect(lambda: FileToPublic(self) )

        self.Filelist = QListWidget()  #实例化列表控件
        self.Filelist.doubleClicked.connect(lambda: UseFile(self))
        self.right_layout4.addWidget(self.Filelist,7,0)
        for i in self.FileRecorder:
            self.Filelist.addItem(i)
    except Exception as err:
        print(err)

def UseFile(self):
    try:
        item = self.Filelist.currentItem().text()
        DirPath,Filename = item.rsplit("/",1)
        self.AES.decrypt(DirPath,Filename)
        time.sleep(0.1)
        os.startfile(Filename)
        time.sleep(0.3)
        self.AES.encrypt(DirPath,Filename)
    except Exception:
        #raise
        QtWidgets.QMessageBox.warning(self, "错误", "出现未知错误：该文件无法被复原")

def FileToPrivate(self):
    try:
        CompleteFilePath = QFileDialog.getOpenFileName()[0]
        if CompleteFilePath not in self.FileRecorder:
            os.chdir(WorkPath)
            with open("FileRecord","a") as f:
                a = f.write(CompleteFilePath + "\n")
            Upload("127.0.0.1",23456,"FileRecord")
            f.close()
            DirPath,Filename = CompleteFilePath.rsplit("/",1)
            self.AES.encrypt(DirPath,Filename)
            self.Filelist.addItem(CompleteFilePath)
            self.FileRecorder.append(CompleteFilePath)
    except Exception:
        QtWidgets.QMessageBox.warning(self, "错误", "未选择文件或该文件的类型不支持加密")
        #raise

def FileToPublic(self):
    try:
        item = self.Filelist.currentItem()
        item_text = item.text()
    except:
        pass
    else:
        try:
            DirPath,Filename = item_text.rsplit("/",1)
            self.AES.decrypt(DirPath,Filename)
        except Exception:
            #raise
            QtWidgets.QMessageBox.warning(self, "错误", "出现未知错误：该文件可能已被修改，无法还原，自动从系统中删除")
        finally:
            self.FileRecorder.remove(item_text)
            self.Filelist.takeItem(self.Filelist.row(item))
            os.chdir(WorkPath)
            print(os.getcwd())
            with open("FileRecord","w") as f:
                for i in self.FileRecorder:
                    f.write(i + '\n')
            Upload("127.0.0.1",23456,"FileRecord")
            f.close()