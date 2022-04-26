# -*- coding: utf-8 -*-

import ipaddress
from pyclbr import Function
import sys
import time

import netifaces
from PyQt5.QtCore import Qt, QBuffer, QByteArray, QIODevice
from PyQt5.QtGui import QPixmap, QCursor, QImageReader
from PyQt5.QtWidgets import QApplication, QInputDialog, QMainWindow, QMessageBox, QMenu, QAction, QFileDialog
from numpy import False_

from ui.Ui_main import Ui_MainWindow
from module.Message import MessageServer, MessageClient
from module.Video import VideoSender
from module.Audio import AudioSender, AudioPlayer
from module.File import FileSender, FileDownloader


class MyMainForm(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        Ui_MainWindow.__init__(self)
        QMainWindow.__init__(self, parent)

        self.video_type = 'camera'  # camera or desktop
        self.is_full_video = False

        self.video_sender = None

        self.audio_sender = None
        self.audio_player = None

        self.file_sender = None
        self.file_downloader = None

        self.live_server = None
        self.live_client = None

        self.to_ip = '127.0.0.1'
        self.broadcast_ip = '192.168.31.255'

        self.msg_server = MessageServer()
        self.msg_server._msg.connect(self.show_msg)
        self.msg_server._video.connect(self.show_video)
        self.msg_server._audio.connect(self.play_audio)
        self.msg_server._file.connect(self.download_file)
        self.msg_server._text.connect(self.show_text)
        self.msg_server._log.connect(self.show_log)
        self.msg_server.start()

        self.msg_client = None

        self._setupUi(True)

    def _setupUi(self, is_first=False):
        # 处理文本框
        if is_first:
            self.setupUi(self)

        to_ip = self.lineEdit_ip.text()
        broadcast_ip = self.lineEdit_broadcast.text()
        browser_text = self.textBrowser_text.toHtml()
        text = self.lineEdit_text.text()

        if not is_first:
            self.setupUi(self)

        self.pushButton_connect.clicked.connect(self.run_connect_btn)  # 开启连接
        self.pushButton_close.clicked.connect(self.close_all_threads)  # 关闭连接

        self.pushButton_start_vs.clicked.connect(self.run_video_btn)  # 视频
        self.pushButton_start_as.clicked.connect(self.run_audio_btn)  # 音频
        self.pushButton_start_fs.clicked.connect(self.run_file_btn)  # 文件

        self.pushButton_set_video_type.clicked.connect(
            self.set_video_type)  # 设置视频类型

        self.pushButton_get_ip.clicked.connect(self.get_ips)  # 广播设置 - 获取地址

        self.pushButton_start_scan.clicked.connect(self.scan_ip_btn)  # 获取在线名单

        self.pushButton_end.clicked.connect(self.close)  # 退出程序

        self.label_video.setContextMenuPolicy(Qt.CustomContextMenu)
        self.label_video.customContextMenuRequested.connect(
            self.create_rightmenu)

        self.lineEdit_text.returnPressed.connect(self.send_text)  # 发送消息

        # 处理文本框
        self.lineEdit_ip.setText(to_ip)
        self.lineEdit_broadcast.setText(broadcast_ip)
        self.textBrowser_text.append(browser_text)
        self.lineEdit_text.setText(text)

    def create_rightmenu(self):
        # 菜单对象
        self.groupBox_menu = QMenu(self)
        self.actionA = QAction(u'全屏播放', self)  # 创建菜单选项对象
        # self.actionA.setShortcut('Ctrl+S')#设置动作A的快捷键
        # 把动作A选项对象添加到菜单self.groupBox_menu上
        self.groupBox_menu.addAction(self.actionA)
        self.actionA.triggered.connect(self.video_full)
        self.groupBox_menu.popup(QCursor.pos())

    def set_video_type(self):
        if self.radioButton_camera.isChecked():
            self.video_type = 'camera'
        elif self.radioButton_desktop.isChecked():
            self.video_type = 'desktop'

    def close_all_threads(self):

        if self.msg_client:
            self.msg_client.quit()
            self.msg_client = None

        fun_list: list[Function] = [
            self.close_video_sender,
            self.close_audio_sender,
            self.close_file_sender
        ]

        for fun in fun_list:
            fun()

        self.label_video.clear()
        self.label_video.repaint()

    def scan_ip_btn(self):
        # if self.scan:
        #     return
        intfs = netifaces.interfaces()
        data_list = []
        for intf in intfs:
            res = netifaces.ifaddresses(intf)
            if netifaces.AF_INET in res:  # ipv4
                ipv4 = res[netifaces.AF_INET][0]
                data_list.append('addr:' + ipv4['addr'] +
                                 ',netmask:' + ipv4['netmask'])
        item, ok = QInputDialog.getItem(
            self, '选择IP', '本地IP列表：', data_list, 0, False)

        ips = []
        if ok and item:
            text = item.split(',')
            # self.lineEdit_ip.setText(text[0].split(':')[1])
            ip = text[0].split(':')[1]
            netmask = text[1].split(':')[1]
            netmask_num = sum([bin(int(i)).count('1')
                              for i in netmask.split('.')])

            net = ipaddress.ip_network(f'{ip}/{netmask_num}', strict=False)
            for x in net.hosts():
                if str(x) == ip:
                    continue
                ips.append(str(x))

    def video_full(self):
        self.to_ip = self.lineEdit_ip.text()
        self.broadcast_ip = self.lineEdit_broadcast.text()

        if not self.is_full_video:
            self.label_video.setWindowFlags(Qt.Window)  # 使得label位于最高级别的窗口
            self.label_video.showFullScreen()  # 全屏显示
            self.is_full_video = True
        else:
            self._setupUi()
            self.is_full_video = False

    def run_connect_btn(self):
        if not self.msg_client:
            self.run_msg_client()
            self.pushButton_connect.setText('关闭')
        elif self.msg_client.is_connected:
            self.close_msg_client()
            self.pushButton_connect.setText('连接')

    def run_video_btn(self):
        if not self.video_sender:
            if not self.client_connected():
                self.show_log('video sender: no connect')
                return
            self.pushButton_start_vs.setText('关闭')
            self.run_video_sender()
        else:
            self.pushButton_start_vs.setText('视频')
            self.close_video_sender()

    def run_audio_btn(self):
        if not self.audio_sender:
            if not self.client_connected():
                self.show_log('audio sender: no connect')
                return
            self.pushButton_start_as.setText('关闭')
            self.run_audio_sender()
        else:
            self.pushButton_start_as.setText('音频')
            self.close_audio_sender()

    def run_file_btn(self):
        if not self.file_sender:
            if not self.client_connected():
                self.show_log('file sender: no connect')
                return
            self.run_file_sender()
        else:
            self.close_file_sender()

    def run_msg_client(self):
        self.to_ip = self.lineEdit_ip.text()
        self.msg_client = MessageClient(self.to_ip)
        # self.msg_client._msg.connect(self.show_msg)
        self.msg_client._log.connect(self.show_log)
        self.msg_client.start()

    def close_msg_client(self):
        if self.msg_client:
            self.msg_client.quit()
            self.msg_client = None

    def run_video_sender(self):
        if not self.video_sender:
            # 创建视频发送线程
            self.video_sender = VideoSender(self.video_type)
            self.video_sender.open_server()
            self.video_sender.set_sender(self.msg_client)
            # 连接信号，绑定回调事件
            self.video_sender._video_local.connect(self.show_video_src)
            # self.video_sender._video_sender.connect(self.get_video_sender)
            self.video_sender.start()

    def close_video_sender(self):
        if self.video_sender:
            self.video_sender.quit()
            self.video_sender = None
        self.label_video_2.clear()
        self.label_video_2.repaint()

    def run_audio_sender(self):
        if not self.audio_sender:
            self.audio_sender = AudioSender()
            self.audio_sender.set_sender(self.msg_client)
            # self.audio_sender._audio_sender.connect(self.get_audio_sender)
            self.audio_sender.open_server()
            self.audio_sender.start()

    def close_audio_sender(self):
        if self.audio_sender:
            self.audio_sender.quit()
            self.audio_sender = None

    def run_audio_player(self):
        self.audio_player = AudioPlayer()
        self.audio_player.start()

    def close_audio_player(self):
        if self.audio_player:
            self.audio_player.quit()
            self.audio_player = None

    def run_file_sender(self):
        filepath = QFileDialog.getOpenFileName()[0]
        # ([filepath], 'All Files (*)')
        if not filepath:
            return
        self.file_sender = FileSender(filepath)
        self.file_sender.set_sender(self.msg_client)
        self.file_sender._print.connect(self.show_text)
        # self.file_sender._file_sender.connect(self.get_file_sender)
        self.file_sender.start()

    def close_file_sender(self):
        if self.file_sender:
            self.file_sender.quit()
            self.file_sender = None

    def run_file_downloader(self, filename):
        self.file_downloader = FileDownloader(filename)
        self.file_downloader._file_remind.connect(self.downloader_remind)
        self.file_downloader.open_file()
        self.file_downloader.start()

    def close_file_downloader(self):
        if self.file_downloader:
            self.file_downloader.quit()

    def client_connected(self):
        return self.msg_client and self.msg_client.is_connected

    def get_ips(self):
        intfs = netifaces.interfaces()
        data_list = []
        for intf in intfs:
            res = netifaces.ifaddresses(intf)
            if netifaces.AF_INET in res:  # ipv4
                ipv4 = res[netifaces.AF_INET][0]
                data_list.append('addr:' + ipv4['addr'] +
                                 ',broadcast:' + ipv4['broadcast'])

        item, ok = QInputDialog.getItem(
            self, '选择广播IP', '本地IP列表：', data_list, 0, False)

        if ok and item:
            text = item.split(',')
            # self.lineEdit_ip.setText(text[0].split(':')[1])
            self.lineEdit_broadcast.setText(text[1].split(':')[1])

    """
    线程回调
    用于发送各种信息
    message, video, audio, file, text
    """

    # def get_video_sender(self, data: bytes):  # 用于发送视频
    #     if not self.video_sender:
    #         return
    #     if not self.client_connected():
    #         return
    #     self.msg_client.sendall(b'video:::' + data)

    def get_audio_sender(self, data: bytes):  # 用于发送音频
        if not self.audio_sender:
            return
        if not self.client_connected():
            return
        self.msg_client.sendall(b'audio:::' + data)

    # def get_file_sender(self, data: bytes):  # 用于发送文件
    #     if not self.file_sender:
    #         return
    #     if not self.client_connected():
    #         return
    #     self.msg_client.sendall(b'file:::' + data)

    def send_text(self):  # 绑定回车事件
        text = str(self.lineEdit_text.text())
        if not self.client_connected():
            self.show_log('text sender: no connect')
            return

        self.textBrowser_text.append(
            '<span style="color:blue">我: ' + text + '</span>')
        self.lineEdit_text.setText('')

        self.msg_client.sendall(b'text:::' + text.encode())

    """
    线程回调
    处理接收的各种信息
    message, video, audio, file, text
    """

    def show_msg(self, data: str):  # 对接 Message 的 TCP 线程
        # data 格式 ip:port:msg
        data = data.split(':', 2)
        addr = (data[0], int(data[1]))
        data = data[2]

        if data == 'connect':
            if self.msg_client:
                if self.msg_client.wait_ip == addr[0]:
                    self.msg_server.accept_connect(addr)
                    self.msg_client.send_text('连接成功！')
                else:
                    self.msg_server.close_connect(addr)
                    self.msg_client.send_text('对方正处于连接状态！')
                return

            question_msg = ('是否接受来至%s:%s的' % addr) + '连接？'
            reply = QMessageBox.question(
                self, '提示', question_msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                # 可以连接
                self.msg_server.accept_connect(addr)
                # 同时发起对方连接的请求
                self.lineEdit_ip.setText(addr[0])
                self.run_connect_btn()
                # self.msg_client.send_text('连接成功！')
            else:
                # 拒绝连接
                self.msg_server.close_connect(addr)
                # self.msg_client.send_text('连接被拒绝！')
        else:
            pass

    def show_video_src(self, q_image):  # 显示视频发送源
        if not self.client_connected():
            return
        pixmap = QPixmap.fromImage(q_image).scaled(
            self.label_video_2.size(), transformMode=1)  # 平滑缩放
        self.label_video_2.setPixmap(pixmap)
        self.label_video_2.repaint()

    def show_video(self, receive_data: bytes):  # 线程回调-显示视频接收源
        if not self.client_connected():
            return
        byte_array = QByteArray(receive_data)
        buffer = QBuffer(byte_array)
        buffer.open(QIODevice.ReadOnly)
        # 读取图片
        reader = QImageReader(buffer)
        q_image = reader.read()

        pixmap = QPixmap.fromImage(q_image).scaled(
            self.label_video.size(), transformMode=1)  # 平滑缩放
        self.label_video.setPixmap(pixmap)
        self.label_video.repaint()

    def play_audio(self, data: bytes):  # 显示视频接收源
        # data 格式 'tag':'audio':['open'|'close'] or audio_buffer
        if not self.client_connected():
            return

        if not self.audio_player:
            self.run_audio_player()

        if self.audio_player:
            if not self.audio_player.stream:  # 没有声卡无法播放
                print('no audio player !!!')
                return
            self.audio_player.buffer_list.append(data)

    def download_file(self, data: bytes):  # 下载接收的文件
        if not self.client_connected():
            return
        # data 格式 'tag':[filename]:['open'|'close'] or file_buffer
        if data[:3] == b'tag':
            data = data.split(b':', 2)
            filename = data[1].decode()
            tag = data[2]
            if tag == b'open':
                self.run_file_downloader(filename)
                self.show_log(f'收到文件:{filename}，准备下载...')
            elif tag == b'close':
                # 通知下载线程结束
                self.file_downloader.buffer_list.append(
                    str(filename + ':end').encode())
        elif self.file_downloader:
            self.file_downloader.buffer_list.append(data)
        else:
            print('no file downloader !!!')

    def show_text(self, text: str):
        if not text:
            return
        self.textBrowser_text.append(text)

    def show_log(self, text: str):  # 显示情况
        if not text:
            return
        self.show_text(f'<span style="color:grey">[info]:{text}</span>')

    def downloader_remind(self, msg: str):
        # downloaded
        self.close_file_downloader()
        self.show_log(msg)

    def closeEvent(self, event):
        # 重构closeEvent函数，关闭所有线程
        reply = QMessageBox.question(
            self, '提示', '是否要退出程序？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            self.close_all_threads()
            time.sleep(1)
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())
