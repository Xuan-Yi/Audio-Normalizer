from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import time
from components.lines import QHLine
from components.audio_file_list import Audio_File_List
from components.NormalizeInputBox import NormalizeInputBox

from core.processing import Processing

audio_formats = ['m4a','mp3','wav','flac']
audio_format_map = {'m4a': 'mp4', 'mp3': 'mp3', 'wav': 'wav', 'flac': 'flac'}


class settingPage(QGridLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font = QFont('Segoe UI', 11)
        self.setSpacing(12)
        self.sourceDir = ""
        self.sourceFormat = audio_format_map[audio_formats[0]]
        self.__initArea()

    def __initArea(self):
        self.openFolderBtn = QPushButton(text='Open Folder')    # choose folder
        self.openFolderBtn.setFont(self.font)
        self.openFolderBtn.setFixedSize(175, 32)
        self.openFolderBtn.clicked.connect(self.__open_folder_callback)
        self.addWidget(self.openFolderBtn, 0, 0, 1, 1)
        self.dirT = QLabel(text="C:/")  # folder name showcase
        self.dirT.setFont(self.font)
        self.dirT.setFixedHeight(32)
        self.dirT.setMinimumWidth(300)  #
        self.addWidget(self.dirT, 0, 1, 1, 3)
        # find audio files of some format
        splitter1 = QHLine()
        self.addWidget(splitter1, 1, 0, 1, 3)
        self.audio_format_combo = QComboBox()
        self.audio_format_combo.addItems(audio_formats)
        self.audio_format_combo.setFont(self.font)
        self.audio_format_combo.setCurrentText(audio_formats[0])
        self.audio_format_combo.currentIndexChanged.connect(
            self.__audio_format_combo_change_callback)
        self.addWidget(self.audio_format_combo,2,0,1,1)
        self.nInput = NormalizeInputBox()
        self.addItem(self.nInput,2,1,1,1)
        self.scrollArea = Audio_File_List()
        self.addWidget(self.scrollArea,3,0,1,2)
        self.startBtn = QPushButton(text="Start Convert",font=self.font)
        self.startBtn.clicked.connect(self.__start_convert_clicked_callback)
        self.addWidget(self.startBtn,4,0,1,2)# setup progressbar
        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        self.progressBar.setFont(self.font)
        self.addWidget(self.progressBar,5,0,1,2)

    def updateProgressbar(self,value:int):
        self.progressBar.setValue(value)

    def __open_folder_callback(self):
        dir = QFileDialog.getExistingDirectory(
            None, "Open source folder.", "C:/")   # 起始路徑
        if dir != "":
            self.sourceDir = dir
            self.dirT.setText(dir)
            self.scrollArea.setDir(dir)
            self.scrollArea.refresh()

    def __audio_format_combo_change_callback(self):
        self.sourceFormat =audio_format_map[self.audio_format_combo.currentText()]
        self.scrollArea.setAudioFormat(self.audio_format_combo.currentText())
        self.scrollArea.refresh()

    def __start_convert_clicked_callback(self):
        audioFileList = self.scrollArea.getAudioFileList()
        # validation
        if self.nInput.normalize_validate() and len(audioFileList)!=0:
            
            # disable inputs 
            self.openFolderBtn.setEnabled(False)
            self.audio_format_combo.setEnabled(False)
            self.nInput.setEnabled(False)
            self.startBtn.setEnabled(False)

            # process
            tool = Processing()
            dBFS = self.nInput.get_dBFS()
            tool.set_dBFS (dBFS)
            tool.set_format (self.sourceFormat)
            tool.set_queue (audioFileList)
            tool.setProgressBar(self.progressBar)
            tool.process()

            # resume
            self.openFolderBtn.setEnabled(True)
            self.audio_format_combo.setEnabled(True)
            self.nInput.setEnabled(True)
            self.startBtn.setEnabled(True)
            
            