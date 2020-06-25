from . import browser_history
import qtawesome
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton,QComboBox, QLineEdit, QTextBrowser
import time
import threading

def show_browser_history(self):
    try:
        self.search_icon = QtWidgets.QLabel(chr(0xf002) + ' ' + '搜索  ')
        self.search_icon.setFont(qtawesome.font('fa', 16))
        self.right_bar_widget_search_input = QtWidgets.QLineEdit()
        self.right_bar_widget_search_input.setPlaceholderText("输入浏览记录关键字，按回车进行搜索")
        self.right_bar_widget_search_input.returnPressed.connect(lambda: search(self))

        self.right_layout.addWidget(self.search_icon, 0, 0, 1, 1)
        self.right_layout.addWidget(self.right_bar_widget_search_input, 0, 1, 1, 8)

        self.right_op_label = QtWidgets.QLabel("操作面板")
        self.right_layout.addWidget(self.right_op_label, 1, 0, 1, 1)

        self.right_browser_label = QtWidgets.QLabel("浏览器:")
        self.right_layout.addWidget(self.right_browser_label, 2, 0, 1, 1)

        self.combobox = QComboBox(self)
        self.right_layout.addWidget(self.combobox, 2, 1, 1, 1)
        self.combobox.addItem('chrome')
        self.choice_list = ['firefox', 'safari', 'Edge', 'IE']
        self.combobox.addItems(self.choice_list)

        self.bt_look = QPushButton('查看记录', self)
        self.right_layout.addWidget(self.bt_look, 3, 0, 1, 1)
        self.bt_look.clicked.connect(lambda: look(self))

        self.bt_del = QPushButton('删除记录', self)
        self.right_layout.addWidget(self.bt_del, 3, 1, 1, 1)
        self.bt_del.clicked.connect(lambda: del_record(self))

        self.round_del_label = QtWidgets.QLabel("周期性删除模式:")
        self.right_layout.addWidget(self.round_del_label, 2, 3, 1, 1)

        self.combobox2 = QComboBox(self)
        self.right_layout.addWidget(self.combobox2, 2, 4, 1, 1)
        self.combobox2.addItem('--周期为天--')
        self.choice_list = ['1', '3', '7', '30']
        self.combobox2.addItems(self.choice_list)

        self.bt_on = QPushButton('开启', self)
        self.right_layout.addWidget(self.bt_on, 3, 3, 1, 1)
        self.bt_on.clicked.connect(lambda: period_mode_on(self))

        self.bt_off = QPushButton('关闭', self)
        self.right_layout.addWidget(self.bt_off, 3, 4, 1, 1)
        self.bt_off.clicked.connect(lambda: period_mode_off(self))

        self.right_min_label = QtWidgets.QLabel("删除敏感条目")
        self.right_layout.addWidget(self.right_min_label, 5, 0, 1, 1)

        self.bt_min_del = QPushButton('删除', self)
        self.right_layout.addWidget(self.bt_min_del, 5, 1, 1, 1)
        self.bt_min_del.clicked.connect(lambda: del_key_word(self))

        self.right_min_info = QtWidgets.QLabel("敏感词列表:")
        self.right_layout.addWidget(self.right_min_info, 6, 0, 1, 1)

        self.lineedit = QLineEdit(self)
        self.right_layout.addWidget(self.lineedit, 6, 1, 1, 8)
        self.lineedit.setPlaceholderText("输入敏感词，以顿号分隔")

        self.right_playlist_lable = QtWidgets.QLabel("显示面板")
        self.right_layout.addWidget(self.right_playlist_lable, 7, 0, 1, 1)

        self.text_browser = QTextBrowser(self)
        self.right_layout.addWidget(self.text_browser, 8, 0, 10, 10)
    except Exception as err:
        print(err)


def search(self):
    try:
        line = self.right_bar_widget_search_input.text()
        try:
            dict = browser_history.get_browserhistory()
            tmp_str = "搜索的条目为：\n"
            browser = self.combobox.currentText()

            for i in range(len(dict[browser])):
                if line in str(dict[browser][i][1]):
                    tmp_str += str(dict[browser][i][2]) + " " + str(dict[browser][i][1]) + "\n"
            self.text_browser.setText(tmp_str)
        except Exception as err:
            print(err)
            self.text_browser.setText(browser + "中没有浏览记录")
    except Exception as err:
        print(err)

def look(self):
    try:
        dict = browser_history.get_browserhistory()
        tmp_str = ""
        browser = self.combobox.currentText()

        if (len(dict[browser]) < 100):
            num = len(dict[browser])
        else:
            num = 100
        for i in range(num):
            if str(dict[browser][i][1]) != 'None':
                tmp_str += str(dict[browser][i][2]) + " " + str(dict[browser][i][1]) + "\n"
        self.text_browser.setText(tmp_str)
    except Exception as err:
        print(err)
        self.text_browser.setText(browser + "中没有浏览记录")


def del_record(self):
    choice = self.combobox.currentText()
    try:
        browser_history.del_browserhistory(choice)
        self.text_browser.setText(choice + "中的记录已经删除")
    except:
        self.text_browser.setText(choice + "中没有浏览记录")


def period_mode_on(self):
    self.flag_period_mode = 0  # 浏览记录-周期删除模式-标志位
    self.bt_on.setEnabled(False)
    period = self.combobox2.currentText()
    choice = self.combobox.currentText()
    self.t1 = threading.Thread(target=self.period_task, args=(period, choice))
    self.t1.start()

def period_mode_off(self):
    self.bt_on.setEnabled(True)
    self.flag_period_mode = 1

def period_task(self, period, choice):
    while (True):
        if self.flag_period_mode == 1:
            break
        else:
            time.sleep(int(period) * 86400)
            try:
                browser_history.del_browserhistory(choice)
                self.text_browser.setText(choice + "中的记录已经删除")
            except:
                self.text_browser.setText(choice + "中没有浏览记录")


def del_key_word(self):
    try:
        line = self.lineedit.text()
        word_list = line.split("、")
        try:
            dict = browser_history.get_browserhistory()
            tmp_str = "删除的条目为：\n"
            browser = self.combobox.currentText()

            for i in range(len(dict[browser])):
                for word in word_list:
                    if word in str(dict[browser][i][1]):
                        tmp_str += str(dict[browser][i][2]) + " " + str(dict[browser][i][1]) + "\n"
                        browser_history.del_key_record(browser, str(dict[browser][i][1]))
                        break
            self.text_browser.setText(tmp_str)

        except Exception as err:
            print(err)
            self.text_browser.setText(browser + "中没有浏览记录")

    except Exception as err:
        print(err)