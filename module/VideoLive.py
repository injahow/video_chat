# -*- coding: utf-8 -*-

from message.UDPSocket import Client, Server
from module.Video import VideoSender

from PyQt5.QtCore import QThread, pyqtSignal, QBuffer, QByteArray, QIODevice


class LiveServer(Server, VideoSender):  # 直播发送方

    def __init__(self, broadcast_ip: str, key: str, video_type: str):
        Server.__init__(self, broadcast_ip)
        self.set_handler(key)
        VideoSender.__init__(self, video_type)
        self.quality = 20

    def set_quality(self, quality):
        self.quality = quality

    def qImg2bytes(self, qImg):
        byte_array = QByteArray()
        qImg_buffer = QBuffer(byte_array)
        qImg_buffer.open(QIODevice.WriteOnly)
        qImg.save(qImg_buffer, 'jpg', self.quality)
        return byte_array.data()

    def sendall(self, data: bytes):
        self.sendto(data)


class LiveClient(Client, QThread):  # 直播接收方
    #  定义信号
    _log = pyqtSignal(str)
    _video = pyqtSignal(bytes)

    def __init__(self, key: str):
        self.key = key
        Client.__init__(self)
        QThread.__init__(self)

    def emit(self, data: bytes):
        self._video.emit(data)

    def _print(self, text: str):
        self._log.emit(text)

    def quit(self):
        self.close_connect()

    def run(self):
        self.set_handler(self.key)
        self.bind()
