from os import listdir
from os.path import isdir,join,abspath
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Audio_File_List(QScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        font = QFont('Segoe UI', 11)
        self.list_content = QLabel()
        self.list_content.showFullScreen()
        self.list_content.setAlignment(Qt.AlignTop)
        self.list_content.setFixedWidth(500)
        self.list_content.setWordWrap(True)
        self.list_content.setMargin(6)
        self.list_content.setFont(font)
        self.setWidget(self.list_content)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFixedSize(500,210)
        self.setWidgetResizable(True)
        self.dir = ""
        self.format = "m4a"
        self.filelist = []

    def setDir(self, dir:str):
        self.dir = dir

    def setAudioFormat(self, format: str):
        self.format = format

    def __get_file_list(self):
        if self.dir == "" or self.format == "":
            return False
        self.filelist=[]
        for file in listdir(self.dir):
            if not isdir(file):
                if str('.'+self.format.lower()) in file or str('.'+self.format.upper()) in file:
                    self.filelist.append(file)
        return True

    def refresh(self):
        if self.__get_file_list():
            # render list
            showcase = ""
            for i in range(len(self.filelist)):
                showcase = showcase+f'{i+1}. {self.filelist[i]}\n'
            self.list_content.setText(showcase)

    def getAudioFileList(self):
        abspathFileList=[]
        for f in self.filelist:
            abs = abspath(join(self.dir,f))
            abspathFileList.append(abs)
        return abspathFileList
