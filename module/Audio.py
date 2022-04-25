# -*- coding: utf-8 -*-

from pyaudio import paInt16, PyAudio
from PyQt5.QtCore import QThread, pyqtSignal


CHUNK = 1024
FORMAT = paInt16    # 格式
CHANNELS = 2    # 输入/输出通道数
RATE = 44100    # 音频数据的采样频率


class AudioSender(QThread):  # 发送方，服务器

    _audio_sender = pyqtSignal(bytes)

    def __init__(self):
        super().__init__()
        self.pyaudio = PyAudio()
        self.stream = None
        self.closed = False

    def quit(self):
        self.closed = True

    def open_server(self):
        try:
            self.stream = self.pyaudio.open(
                format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        except:
            print('Audio open error !')

    def close_server(self):

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        if self.pyaudio:
            self.pyaudio.terminate()

    def run(self):
        
        while not self.closed:
            try:
                data = self.stream.read(CHUNK*10)
                self._audio_sender.emit(data)
                self.msleep(10)
            except:
                pass


class AudioPlayer(QThread):  # 接收方-播放

    def __init__(self):
        super().__init__()
        self.buffer_list = []
        self.closed = False
        self.pyaudio = PyAudio()
        try:
            self.stream = self.pyaudio.open(
                format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
            self.stream.start_stream()
        except:
            print('Audio open error !')

    def quit(self):
        self.closed = True

    def run(self):

        end = str('audio:end').encode()
        while not self.closed:
            if len(self.buffer_list) > 0:
                if self.buffer_list[0] == end:
                    self.buffer_list.clear()
                    break
                try:
                    self.stream.write(self.buffer_list.pop(0), CHUNK*10)
                except:
                    pass

        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio.terminate()
