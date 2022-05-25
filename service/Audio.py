# -*- coding: utf-8 -*-

from pyaudio import paInt16, PyAudio
from PyQt5.QtCore import QThread, pyqtSignal

from network.Message import MessageClient


CHUNK = 1024
FORMAT = paInt16    # 格式
CHANNELS = 2    # 输入/输出通道数
RATE = 44100    # 音频数据的采样频率


class AudioSender(QThread):  # 发送
    _print = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.msg_client = None
        self.pyaudio = PyAudio()
        self.stream = None
        self.closed = False

    def quit(self):
        self.closed = True

    def open_server(self, audio_type):
        try:
            if audio_type == 'system':
                self.stream = self.pyaudio.open(
                    format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                    input_device_index=self.find_internal_recording_device(),
                    frames_per_buffer=CHUNK)
            else:
                self.stream = self.pyaudio.open(
                    format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        except:
            self._print.emit('[audio]: open error !')

    def find_internal_recording_device(self):
        p = self.pyaudio
        target = '立体声混音'  # 需要系统打开立体声混音声卡
        for i in range(p.get_device_count()):
            devInfo = p.get_device_info_by_index(i)
            # print(devInfo)
            if devInfo['name'].find(target) >= 0 and devInfo['hostApi'] == 0:
                return i
        print('无法找到内录设备!')
        return None

    def close_server(self):

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        if self.pyaudio:
            self.pyaudio.terminate()

    def set_sender(self, msg_client: MessageClient):
        self.msg_client = msg_client

    def sendall(self, data: bytes):
        if not self.msg_client:
            return
        self.msg_client.send_audio(data)

    def run(self):

        while not self.closed:
            try:
                data = self.stream.read(CHUNK*10)
                self.sendall(data)
                self.msleep(10)
            except:
                pass


class AudioPlayer(QThread):  # 接收

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
