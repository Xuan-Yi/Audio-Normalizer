from signal import signal
from tkinter.ttk import Progressbar
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import pathlib
import time
from shutil import rmtree
from os import mkdir
from os.path import abspath, join, isfile, isdir
from pydub import AudioSegment


class Processing:
    def __init__(self):
        self.queue = []
        self.dBFS = 'N'
        self.format = ''

    def set_queue(self, audioList: list):
        self.queue = audioList

    def set_dBFS(self, dBFS):
        self.dBFS = dBFS

    def set_format(self, audio_format: str):
        if audio_format in ['mp4', 'mp3',  'wav',  'flac']:
            self.format = audio_format

    def setProgressBar(self, progressBar: QProgressBar):
        self.progressbar = progressBar

    def __normalize(self, sound):
        if self.dBFS == 'N':    # do not normalize
            return sound
        ratio = 0.99  # ratio of hard_normalization
        loudness_hard = sound.max_dBFS
        loudness_soft = sound.dBFS+3
        loudness = loudness_hard*ratio+loudness_soft*(1-ratio)
        change_in_dBFS = self.dBFS-loudness
        return sound.apply_gain(change_in_dBFS)

    '''def Progreebar_setValue(self, progress: int):
        print(f'{progress} %')
        if progress >= self.maxProgress:
            self.progressbar.setValue(progress)
            self.maxProgress = progress'''

    def process(self):
        if self.format == '' or len(self.queue) == 0:
            return False

        original_dir = pathlib.Path(self.queue[0]).parent
        new_dir = abspath(
            join(original_dir, '\..', f'{original_dir}_{self.dBFS} dB_{self.format}'))
        if isdir(new_dir):
            rmtree(new_dir)
        mkdir(new_dir)
        txt_path = abspath(
            join(new_dir, 'error message.txt'))
        self.maxProgress = 0

        for i in range(len(self.queue)):
            file = self.queue[i]
            sound = AudioSegment.from_file(file)
            new_sound = self.__normalize(sound)
            name = pathlib.Path(file).name
            new_path = abspath(
                join(new_dir, name))
            try:
                new_sound.export(new_path, self.format)
                # progress
                progress = int(float(i+1)/len(self.queue)*100)
                self.progressbar.setValue(progress)
            except Exception as e:
                if not isfile(txt_path):
                    msg = f'{file} is converted failed. \nSee error message: \t{e}\n'
                    with open(txt_path, 'a') as f:
                        f.write(msg)
        self.queue = []
