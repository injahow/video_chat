# -*- coding: utf-8 -*-

import os

from PyQt5.QtCore import QThread, pyqtSignal

from network.Message import MessageClient


class FileSender(QThread):  # 文件发送者
    _print = pyqtSignal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.closed = False

    def set_sender(self, msg_client: MessageClient):
        self.msg_client = msg_client

    def sendall(self, data: bytes):
        if not self.msg_client:
            return
        self.msg_client.send_file(data)

    def run(self):
        file_name = os.path.basename(self.file_path)
        self._print.emit('[File]: ' + file_name + ' will send ...')
        with open(self.file_path, 'rb') as send_file:
            self.sendall(str('tag:' + file_name + ':open').encode())
            while not self.closed:
                send_data = send_file.read(102400)  # 100kb * 1000/s -> 10Mb/s
                if send_data:
                    self.sendall(send_data)
                else:
                    break
            self.msleep(1)
            self.sendall(str('tag:' + file_name + ':close').encode())
        self._print.emit('[File]: ' + file_name + ' send ok !')


class FileDownloader(QThread):  # 文件接收者

    _file_remind = pyqtSignal(str)

    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.buffer_list = []
        self.closed = False
        self.file = None

    def open_file(self):
        self.file = open(self.filename, 'wb')

    def quit(self):
        self.closed = True
        self.wait()

    def run(self):
        end = str(self.filename + ':end').encode()
        while not self.closed:
            if len(self.buffer_list) > 0:
                if self.buffer_list[0] == end:
                    self.buffer_list.clear()
                    break
                self.file.write(self.buffer_list.pop(0))
        self.file.flush()
        self.file.close()
        self._file_remind.emit(self.filename + '下载完成')
