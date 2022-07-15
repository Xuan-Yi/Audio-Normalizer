import re
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class NormalizeInputBox(QGridLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font = QFont('Segoe UI', 11)
        self.setSpacing(12)
        self.addWidget(QLabel(text="Normalize to ",font=self.font),0,0,1,1)
        self.normalizeInput=QLineEdit(text='-0.1')
        self.normalizeInput.setFont(self.font)
        self.addWidget(self.normalizeInput,0,1,1,1)
        self.addWidget(QLabel(text=" dBFS",font=self.font),0,2,1,1)

    def normalize_validate(self):
        dBFS = self.normalizeInput.text()
        if dBFS in ['N', 'NaN', 'None']:    # do not normalize
            return True
        for c in dBFS:
            if c not in ['-', '.', ' ', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                self.normalizeInput.setText("-0.1")
                QMessageBox.warning(None,'Invalid dBFS', 'dBFS should be a number ≤0')
                return False
        if dBFS == '0':
            return True
        # quit invalid raw dBFS
        if len(re.findall('\.', dBFS)) > 1 or len(re.findall('-', dBFS)) > 1 or dBFS[0] != '-':
            self.normalizeInput.setText("-0.1")
            QMessageBox.warning(None,'Invalid dBFS', 'dBFS should be a number ≤0')
            return False
        # define raw dBFS to acceptable format
        if ' ' in dBFS:
            dBFS = dBFS.split()
            dBFS.join()
        while dBFS[1] == '0' and dBFS[2] != '.':
            dBFS = '-'+dBFS[2:]
        if dBFS[1] == '.':
            dBFS = '-0'+dBFS[1:]
        if len(re.findall('\.', dBFS)) == 0:
            dBFS = dBFS+'.0'
        self.normalizeInput.setText(str(dBFS))
        return True

    def get_dBFS(self): # return dBFS in double
        dBFS_str = self.normalizeInput.text()
        if dBFS_str in ['N', 'NaN', 'None']:    # do not normalize
            return 'N'
        if dBFS_str == '0':
            return 0
        dBFS_ = dBFS_str.split(sep='.')
        dBFS = int(dBFS_[0])-int(dBFS_[1])*pow(10, ((-1)*len(dBFS_[1])))
        return dBFS

    '''def clear(self):
        self.normalizeInput.setText("-0.1")'''