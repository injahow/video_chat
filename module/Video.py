# -*- coding: utf-8 -*-

import sys

import cv2
from PyQt5.QtCore import QBuffer, QByteArray, QIODevice, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage

from module.Message import MessageClient


class VideoSender(QThread):

    _video_local = pyqtSignal(QImage)

    def __init__(self, video_type='camera'):
        super().__init__()
        self.msg_client = None

        self.video_type = video_type
        self.cap = None
        self.closed = True

    def qImg2bytes(self, qImg):
        # 获取空字节数组
        byte_array = QByteArray()
        # 字节数组绑定输出流
        qImg_buffer = QBuffer(byte_array)
        qImg_buffer.open(QIODevice.WriteOnly)
        if self.video_type == 'desktop':
            quality = 65
        else:
            quality = 50
        # 使用jpg格式保存数据
        qImg.save(qImg_buffer, 'jpg', quality)  # 1-100
        return byte_array.data()

    def set_sender(self, msg_client: MessageClient):
        self.msg_client = msg_client

    def quit(self):
        self.close_server()
        self.wait()

    def open_server(self):
        if self.video_type == 'camera':
            # 打开摄像头
            try:
                cap = self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            except:
                print('no camera')
                sys.exit(1)
        elif self.video_type == 'desktop':
            # 设置桌面对象
            self.screen = QApplication.primaryScreen()
            self.desktop_win_id = QApplication.desktop().winId()
        self.closed = False

    def close_server(self):
        self.closed = True
        if self.cap:
            self.cap.release()
            self.cap = None

    def sendall(self, data: bytes):
        if not self.msg_client:
            return
        self.msg_client.send_video(data)

    def run(self):
        # 1.获取本地video显示在主程序
        while not self.closed:
            if self.video_type == 'camera':
                ret, frame = self.cap.read()
                if not ret:
                    break
                height, width = frame.shape[:2]
                bytesPerLine = 3 * width
                q_img = QImage(frame.data, width, height, bytesPerLine,
                               QImage.Format_RGB888).rgbSwapped()

            elif self.video_type == 'desktop':
                q_img = self.screen.grabWindow(self.desktop_win_id).toImage()
                new_width, new_height = q_img.width()//1.5, q_img.height()//1.5
                q_img = q_img.scaled(new_width, new_height, transformMode=1)

            # 本地回调桌面图片QPixmap缩小 -> QImage格式
            self._video_local.emit(q_img)

            # 2.发送 video
            send_data = self.qImg2bytes(q_img)
            self.sendall(send_data)
            if self.video_type == 'desktop':
                self.msleep(100)
            else:
                self.msleep(50)
        pass
