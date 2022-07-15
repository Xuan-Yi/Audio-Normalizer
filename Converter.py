import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from containers.settingPage import settingPage

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Audio Converter")
        # layout
        self.settingPage = settingPage()
        self.setLayout(self.settingPage)


if __name__ == '__main__':
    app = QApplication(sys.argv)    # 系統視窗程式
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())   # 偵測視窗關閉後結束程式