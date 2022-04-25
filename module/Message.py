# -*- coding: utf-8 -*-

import socket
import sys

from PyQt5.QtCore import QThread, pyqtSignal

from .utils import DataHandler
from .MyTCPSocket import Server, Client


dataHandler = DataHandler()


class MessageServer(Server, QThread):  # 信息接收者

    #  定义信号
    _log = pyqtSignal(str)
    _msg = pyqtSignal(str)  # 连接消息处理
    _video = pyqtSignal(bytes)  # 显示接收的视频
    _audio = pyqtSignal(bytes)  # 播放接收的音频
    _file = pyqtSignal(bytes)  # 下载接收的文件
    _text = pyqtSignal(str)  # 显示接收的文字

    def __init__(self):
        Server.__init__(self)
        QThread.__init__(self)

    def emit(self, conn, addr, msg: bytes):

        # 实现 Server 统一回调，处理客户端请求
        """ msg 统一格式:
        video:::ctx
        audio:::ctx
        file:::ctx
        text:::ctx
        """
        data_type, data = msg.split(b':::', 1)
        data_type = data_type.decode()

        if data_type == 'video':
            self._video.emit(data)
        elif data_type == 'audio':
            self._audio.emit(data)
        elif data_type == 'file':
            self._file.emit(data)
        elif data_type == 'text':
            self._text.emit(
                addr[0] + '(' + str(addr[1]) + '): ' + data.decode())
        else:
            return super().emit(conn, addr, msg)

    def connect_remind(self, addr):
        self._msg.emit(addr[0] + ':' + str(addr[1]) + ':connect')
        # return super().connect_remind(addr)

    def _print(self, text: str):
        self._log.emit(text)
        # return super()._print(text)

    def run(self):
        try:
            self.listen()
        except socket.error as error:
            print('MessageServer bind failed :', error)
            sys.exit(1)


class MessageClient(Client, QThread):  # 信息发起者
    _msg = pyqtSignal(str)  # 连接消息处理
    _log = pyqtSignal(str)  # 显示接收的文字

    def __init__(self, tar_ip):
        Client.__init__(self)
        QThread.__init__(self)
        self.tar_ip = tar_ip

    def quit(self):
        self.close_connect()

    def _print(self, msg: str):
        self._log.emit(msg)

    def send_video(self, msg: bytes):
        self.sendall(b'video:::' + msg)

    def send_audio(self, msg: bytes):
        self.sendall(b'audio:::' + msg)

    def send_file(self, msg: bytes):
        self.sendall(b'file:::' + msg)

    def send_text(self, msg: str):
        self.sendall(b'text:::' + msg.encode())

    def run(self):
        try:
            self.get_connect(self.tar_ip)
        except:
            pass
