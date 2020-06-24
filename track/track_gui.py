from PyQt5 import QtCore, QtWebEngineWidgets
import socket
import threading
import time
import io
import pyAesCrypt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QButtonGroup, QFrame, QToolButton, QStackedLayout,\
    QWidget, QStatusBar, QLineEdit, QLabel

import base64
from Crypto.Cipher import AES

def decrypt(data):
    key = 16 * 'a'
    try:
        aes = AES.new(str.encode(key), AES.MODE_ECB)  # 初始化加密器
        decrypted_text = aes.decrypt(base64.decodebytes(bytes(data, encoding='utf8'))).decode("utf8")  # 解密
        decrypted_text = decrypted_text[:-ord(decrypted_text[-1])]  # 去除多余补位
    except Exception as e:
        pass
    return decrypted_text
 
def encrypt(data):
    key = 16 * 'a'
    while len(data) % 16 != 0:     # 补足字符串长度为16的倍数
        data += (16 - len(data) % 16) * chr(16 - len(data) % 16)
    data = str.encode(data)
    aes = AES.new(str.encode(key), AES.MODE_ECB)  # 初始化加密器
    return str(base64.encodebytes(aes.encrypt(data)), encoding='utf8').replace('\n', '')  # 加密

def find(self):
    request = ('find+' + str(self.input1.text())).strip()
    self.input1.clear()
    s.sendall(encrypt(request).encode())
    data = decrypt(s.recv(1024).decode()) 
    self.output.setText(data)

# 更新当前设备的名称
def set_device_name(self):
    request = ('device+' + str(self.input2.text())).strip()
    self.input2.clear()
    s.sendall(encrypt(request).encode())
    data = decrypt(s.recv(1024).decode()) 
    self.output.setText(data)


# 负责与服务器连接，并实现断线重连
def tcp_connection(self):
    while True:
        try:
            ip_port = ('129.211.60.133', 12346)
            s.connect(ip_port)
            s.settimeout(3)
            set_device_name(self)
            while True:
                try:
                    request = 'test+'
                    s.sendall(encrypt(request).encode())
                    s.recv(1024).decode()
                    time.sleep(100)
                except socket.error as e:
                    print(e)
                    break

        except socket.error as e:
            print(e)
            continue


# 左侧按钮触发的函数，显示主面板
def find_device_location(self):

    self.hint1 = QLabel(self)
    self.hint1.setText('请输入查找设备名')
    self.hint1.setFixedHeight(30)
    self.right_layout6.addWidget(self.hint1, 0, 0, 1, 1)

    self.input1 = QLineEdit(self)
    self.input1.setFocus()
    self.input1.setFixedHeight(30)
    self.right_layout6.addWidget(self.input1, 0, 1, 1, 1)

    self.button1 = QPushButton('查找', self)
    self.button1.clicked.connect(lambda: find(self))
    self.button1.setFixedHeight(30)
    self.right_layout6.addWidget(self.button1, 0, 2, 1, 1)

    self.hint2 = QLabel(self)
    self.hint2.setText('请输入本机设备名')
    self.hint2.setFixedHeight(30)
    self.right_layout6.addWidget(self.hint2, 1, 0, 1, 1)

    self.input2 = QLineEdit(self)
    self.input2.setText('cx')
    self.input2.setFixedHeight(30)
    self.right_layout6.addWidget(self.input2, 1, 1, 1, 1)

    self.button2 = QPushButton('更新', self)
    self.button2.setFixedHeight(30)
    self.button2.clicked.connect(lambda: set_device_name(self))
    self.right_layout6.addWidget(self.button2, 1, 2, 1, 1)

    self.hint3 = QLabel(self)
    self.hint3.setText('服务器返回结果')
    self.hint3.setFixedHeight(30)
    self.right_layout6.addWidget(self.hint3, 2, 0, 1, 1)

    self.output = QLineEdit(self)
    self.output.setFixedHeight(30)
    self.right_layout6.addWidget(self.output, 2, 1, 1, 1)

    # 浏览器控件
    self.browser = QtWebEngineWidgets.QWebEngineView(self)
    self.right_layout6.addWidget(self.browser, 3, 0, 1, 3)
    self.browser.load(QtCore.QUrl('http://129.211.60.133:8080/display'))
    self.browser.show()

    # 连接到服务器,设置为守护线程,并支持断线重连
    global s
    s = socket.socket()
    tcp_client = threading.Thread(target=tcp_connection,args=(self,))
    tcp_client.setDaemon(True)
    tcp_client.start()
