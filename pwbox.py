import sys
sys.path.append("./etc/")
from etc.loginwindow import *

class Login(QtWidgets.QWidget, Ui_loginmenu):    
    switch_window = QtCore.pyqtSignal()    
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        return None

class MainWindow(QtWidgets.QWidget, Ui_MainMenu):
    switch_window = QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        return None

class Controller:
    def __init__(self):
        pass
    
    def show_login(self):
        self.login = Login()
        self.login.switch_window.connect(self.show_main)
        self.login.show()
        return None
            
    def show_main(self):
        self.window = MainWindow()
        self.login.close()
        session = core.session()      
        self.window.show()
        return None

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_login()
    sys.exit(app.exec_())
    core.exit_now('', '')