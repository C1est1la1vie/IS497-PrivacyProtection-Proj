from PyQt5 import QtCore, QtWebEngineWidgets
import socket
import threading
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QButtonGroup, QFrame, QToolButton, QStackedLayout,\
    QWidget, QStatusBar, QLineEdit, QLabel

# 向服务器请求设备位置
def find(self):
    request = ('find+' + str(self.input1.text())).strip()
    self.input1.clear()
    s.sendall(request.encode())
    data = s.recv(1024).decode()
    self.output.setText(data)

# 更新当前设备的名称
def set_device_name(self):
    request = ('device+' + str(self.input2.text())).strip()
    s.sendall(request.encode())
    data = s.recv(1024).decode()
    self.output.setText(data)


# 负责与服务器连接，并实现断线重连
def tcp_connection(self):
    while True:
        try:
            ip_port = ('129.211.60.133', 12345)
            s.connect(ip_port)
            s.settimeout(3)
            self.set_device_name()
            while True:
                try:
                    request = ('device+' + str(self.input2.text())).strip()
                    s.sendall(request.encode())
                    s.recv(1024).decode()
                    time.sleep(1)
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
    self.input1.setFixedHeight(20)
    self.right_layout6.addWidget(self.input1, 0, 1, 1, 1)

    self.button1 = QPushButton('查找', self)
    self.button1.clicked.connect(lambda: find(self))
    self.button1.setFixedHeight(20)
    self.right_layout6.addWidget(self.button1, 0, 2, 1, 1)

    self.hint2 = QLabel(self)
    self.hint2.setText('请输入本机设备名')
    self.hint2.setFixedHeight(20)
    self.right_layout6.addWidget(self.hint2, 1, 0, 1, 1)

    self.input2 = QLineEdit(self)
    self.input2.setText('cx')
    self.input2.setFixedHeight(20)
    self.right_layout6.addWidget(self.input2, 1, 1, 1, 1)

    self.button2 = QPushButton('更新', self)
    self.button2.setFixedHeight(20)
    self.button2.clicked.connect(lambda: set_device_name(self))
    self.right_layout6.addWidget(self.button2, 1, 2, 1, 1)

    self.hint3 = QLabel(self)
    self.hint3.setText('服务器返回结果')
    self.hint3.setFixedHeight(20)
    self.right_layout6.addWidget(self.hint3, 2, 0, 1, 1)

    self.output = QLineEdit(self)
    self.output.setFixedHeight(20)
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
