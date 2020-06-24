from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton,QComboBox, QLineEdit, QTextBrowser,QTextEdit
import threading
from mar.clipboard_process import get_text,set_text
import requests
import json
from time import sleep

def show_mar_gui(self):
    try:
        self.round_del_label = QtWidgets.QLabel("火星文输入法")
        self.right_layout3.addWidget(self.round_del_label, 0, 0, 1, 1)

        self.bt_on = QPushButton('开启', self)
        self.right_layout3.addWidget(self.bt_on, 1, 0, 1, 1)
        self.bt_on.clicked.connect(lambda: mar_mode_on(self))

        self.bt_off = QPushButton('关闭', self)
        self.right_layout3.addWidget(self.bt_off, 1, 1, 1, 1)
        self.bt_off.clicked.connect(lambda: mar_mode_off(self))

        self.right_min_label = QtWidgets.QLabel("在线翻译")
        self.right_layout3.addWidget(self.right_min_label, 2, 0, 1, 1)

        self.bt_tran1 = QPushButton('汉字->火星文', self)
        self.right_layout3.addWidget(self.bt_tran1, 3, 0, 1, 1)
        self.bt_tran1.clicked.connect(lambda: to_mar(self))

        self.bt_tran2 = QPushButton('火星文->汉字', self)
        self.right_layout3.addWidget(self.bt_tran2, 3, 1, 1, 1)
        self.bt_tran2.clicked.connect(lambda: to_chinese(self))

        self.browser_label1 = QtWidgets.QLabel("输入窗口")
        self.right_layout3.addWidget(self.browser_label1, 7, 0, 1, 1)
        self.browser_label2 = QtWidgets.QLabel("输出窗口")
        self.right_layout3.addWidget(self.browser_label2, 7, 5, 1, 1)

        self.text_edit = QTextEdit(self)
        self.right_layout3.addWidget(self.text_edit, 8, 0, 10, 10)
        self.text_browser2 = QTextBrowser(self)
        self.right_layout3.addWidget(self.text_browser2, 8, 5, 10, 10)

    except Exception as err:
        print(err)

def to_mar(self):
    try:
        content = self.text_edit.toPlainText()
        payload = {'appkey': '74eafeb5266183f1', 'content': content, 'type': '2h'}
        r = requests.get('https://api.jisuapi.com/fontconvert/convert', params=payload)
        res = json.loads(r.text)
        self.text_browser2.setText(res['result']['rcontent'])
    except Exception as err:
        print(err)


def to_chinese(self):
    try:
        content = self.text_edit.toPlainText()
        payload = {'appkey': '74eafeb5266183f1', 'content': content, 'type': '2s'}
        r = requests.get('https://api.jisuapi.com/fontconvert/convert', params=payload)
        res = json.loads(r.text)
        self.text_browser2.setText(res['result']['rcontent'])
    except Exception as err:
        print(err)


def mar_mode_on(self):
    self.flag_mar_mode = 0  # 浏览记录-周期删除模式-标志位
    self.bt_on.setEnabled(False)
    self.origin_clip = get_text()
    self.t2 = threading.Thread(target=clipboard_task, args=())
    self.t2.start()

def mar_mode_off(self):
    self.bt_on.setEnabled(True)
    self.flag_mar_mode = 1

def clipboard_task(self):
    while (True):
        if self.flag_mar_mode == 1:
            break
        sleep(2)
        tmp = get_text()
        if tmp != self.origin_clip:
            if tmp[0] == '0':  # 第一个字符为0，则表示汉字转火星文，否则火星文转汉字
                payload = {'appkey': '74eafeb5266183f1', 'content': tmp, 'type': '2h'}
            else:
                payload = {'appkey': '74eafeb5266183f1', 'content': tmp, 'type': '2s'}

            r = requests.get('https://api.jisuapi.com/fontconvert/convert', params=payload)
            res = json.loads(r.text)
            set_text(res['result']['rcontent'])
            self.origin_clip = tmp