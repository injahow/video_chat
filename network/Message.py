# -*- coding: utf-8 -*-

import socket
import sys

from PyQt5.QtCore import QThread, QMutex, pyqtSignal

from network.TCPSocket import Server, Client


class MessageServer(Server, QThread):  # 信息接收者

    #  定义信号
    _log = pyqtSignal(str)
    _msg = pyqtSignal(object)  # 连接消息处理
    _video = pyqtSignal(bytes)  # 显示接收的视频
    _audio = pyqtSignal(bytes)  # 播放接收的音频
    _file = pyqtSignal(bytes)  # 下载接收的文件
    _text = pyqtSignal(str)  # 显示接收的文字

    def __init__(self):
        Server.__init__(self)
        QThread.__init__(self)

    def emit(self, conn, addr, msg: dict):

        # 实现 Server 统一回调，处理客户端请求
        """ msg 统一格式:
        {
            'type':[message|video|audio|file|text]
            'data':[null]
        }
        """
        data_type = msg['type']
        data = msg['data']

        if data_type == 'message':
            self._msg.emit({
                'conn': conn,
                'addr': addr,
                'data': data
            })
        if data_type == 'video':
            self._video.emit(data)
        elif data_type == 'audio':
            self._audio.emit(data)
        elif data_type == 'file':
            self._file.emit(data)
        elif data_type == 'text':
            self._text.emit(
                addr[0] + '(' + str(addr[1]) + '): ' + data.decode())

    def _print(self, text: str):
        self._log.emit(text)
        return super()._print(text)

    def run(self):
        try:
            self.listen()
        except socket.error as error:
            print('MessageServer bind failed :', error)
            sys.exit(1)


class MessageClient(Client, QThread):  # 信息发送者
    # _msg = pyqtSignal(str)  # 连接消息处理
    _log = pyqtSignal(str)  # 显示线程提示

    def __init__(self, tar_ip):
        Client.__init__(self)
        QThread.__init__(self)
        self.mutex = QMutex()
        self.tar_ip = tar_ip

    def quit(self):
        self.close_connect()

    def _print(self, data: str):
        self._log.emit(data)

    def send_message(self, data: str):
        self.mutex.lock()
        self.sendall({
            'type': 'message',
            'data': data
        })
        self.mutex.unlock()

    def send_video(self, data: bytes):
        self.mutex.lock()
        self.sendall({
            'type': 'video',
            'data': data
        })
        self.mutex.unlock()

    def send_audio(self, data: bytes):
        self.mutex.lock()
        self.sendall({
            'type': 'audio',
            'data': data
        })
        self.mutex.unlock()

    def send_file(self, data: bytes):
        self.mutex.lock()
        self.sendall({
            'type': 'file',
            'data': data
        })
        self.mutex.unlock()

    def send_text(self, data: str):
        self.mutex.lock()
        self.sendall({
            'type': 'text',
            'data': data.encode()
        })
        self.mutex.unlock()

    def run(self):
        try:
            self.get_connect(self.tar_ip)
        except:
            pass
