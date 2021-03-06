# -*- coding: utf-8 -*-
from ssl import SSLSocket
import sys
import time

import netifaces
from PyQt5.QtCore import Qt, QBuffer, QByteArray, QIODevice
from PyQt5.QtGui import QPixmap, QCursor, QImageReader
from PyQt5.QtWidgets import QApplication, QInputDialog, QMainWindow, QMessageBox, QMenu, QAction, QFileDialog

from ui.Ui_main import Ui_MainWindow
from network.Message import MessageServer, MessageClient
from service.Video import VideoSender
from service.Audio import AudioSender, AudioPlayer
from service.File import FileSender, FileDownloader
from service.VideoLive import LiveServer, LiveClient


class MyMainForm(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        Ui_MainWindow.__init__(self)
        QMainWindow.__init__(self, parent)

        self.video_type = 'camera'  # camera or desktop
        self.audio_type = 'record'  # record or system
        self.is_full_video = False
        self.to_ip = '127.0.0.1'
        self.broadcast_ip = '192.168.31.255'
        self.video_quality = 60
        self.video_percent = 2/3

        self.video_sender = None
        self.audio_sender = None
        self.audio_player = None
        self.file_sender = None
        self.file_downloader = None
        self.live_client = None
        self.live_server = None

        self.msg_server = MessageServer()
        self.msg_server._msg.connect(self.show_msg)
        self.msg_server._video.connect(self.show_video)
        self.msg_server._audio.connect(self.show_audio)
        self.msg_server._file.connect(self.show_file)
        self.msg_server._text.connect(self.show_text)
        self.msg_server._log.connect(self.show_log)
        self.msg_server.start()
        self.msg_client = None

        self._setupUi(True)

    def _setupUi(self, is_first=False):

        if is_first:
            self.setupUi(self)

        # 处理UI文字
        to_ip = self.lineEdit_ip.text()
        broadcast_ip = self.lineEdit_broadcast.text()
        browser_text = self.textBrowser_text.toHtml()
        text = self.lineEdit_text.text()

        pushButton_connect_text = self.pushButton_connect.text()
        pushButton_start_vs_text = self.pushButton_start_vs.text()
        pushButton_start_as_text = self.pushButton_start_as.text()
        pushButton_send_broadcast_text = self.pushButton_send_broadcast.text()
        pushButton_get_broadcast_text = self.pushButton_get_broadcast.text()

        if not is_first:
            self.setupUi(self)

        def quality_action(quality):
            def action():
                self.video_quality = quality
                if self.live_client:
                    self.live_client.set_quality(quality)
                if self.video_sender:
                    self.video_sender.set_quality(quality)
            return action
        self.action20.triggered.connect(quality_action(22))
        self.action40.triggered.connect(quality_action(40))
        self.action60.triggered.connect(quality_action(60))
        self.action80.triggered.connect(quality_action(80))
        self.action100.triggered.connect(quality_action(98))

        def percent_action(percent):
            def action():
                self.video_percent = percent
                if self.live_client:
                    self.live_client.set_percent(percent)
                if self.video_sender:
                    self.video_sender.set_percent(percent)
            return action
        self.action_per1.triggered.connect(percent_action(1))
        self.action_per2.triggered.connect(percent_action(9/10))
        self.action_per3.triggered.connect(percent_action(4/5))
        self.action_per4.triggered.connect(percent_action(7/10))
        self.action_per5.triggered.connect(percent_action(3/5))

        def audio_action(audio_type):
            def action():
                self.audio_type = audio_type
            return action
        self.action_audio_t1.triggered.connect(audio_action('record'))
        self.action_audio_t2.triggered.connect(audio_action('system'))

        self.pushButton_connect.clicked.connect(self.con_connect_btn)  # 开启连接
        self.pushButton_close.clicked.connect(self.close_all_threads)  # 关闭连接
        self.pushButton_start_vs.clicked.connect(self.con_video_btn)  # 视频
        self.pushButton_start_as.clicked.connect(self.con_audio_btn)  # 音频
        self.pushButton_start_fs.clicked.connect(self.con_file_btn)  # 文件

        self.pushButton_set_video_type.clicked.connect(
            self.set_video_type)  # 视频设置
        self.pushButton_get_ip.clicked.connect(self.get_ips)  # 广播设置
        self.pushButton_send_broadcast.clicked.connect(
            self.con_live_client_btn)  # 视频广播
        self.pushButton_get_broadcast.clicked.connect(
            self.con_live_server_btn)  # 接收广播

        self.pushButton_clean_text.clicked.connect(self.clean_text_btn)  # 清除聊天
        self.pushButton_end.clicked.connect(self.close)  # 退出程序

        self.lineEdit_text.returnPressed.connect(self.send_text)  # 文本框-发送消息

        self.label_video.setContextMenuPolicy(Qt.CustomContextMenu)  # 视频框-右键菜单
        self.label_video.customContextMenuRequested.connect(
            self.create_rightmenu)

        # 处理UI文字
        self.lineEdit_ip.setText(to_ip)
        self.lineEdit_broadcast.setText(broadcast_ip)
        self.textBrowser_text.append(browser_text)
        self.lineEdit_text.setText(text)

        self.pushButton_connect.setText(pushButton_connect_text)
        self.pushButton_start_vs.setText(pushButton_start_vs_text)
        self.pushButton_start_as.setText(pushButton_start_as_text)
        self.pushButton_send_broadcast.setText(pushButton_send_broadcast_text)
        self.pushButton_get_broadcast.setText(pushButton_get_broadcast_text)

    def create_rightmenu(self):
        # 菜单对象
        self.groupBox_menu = QMenu(self)
        self.actionA = QAction(u'全屏播放', self)  # 创建菜单选项对象
        self.groupBox_menu.addAction(self.actionA)
        self.actionA.triggered.connect(self.video_full)
        self.groupBox_menu.popup(QCursor.pos())

    def set_video_type(self):
        video_type_list = ['desktop', 'camera']
        item, ok = QInputDialog.getItem(
            self, '选择视频类型', '类型列表：', video_type_list, 0, False)
        if ok and item:
            self.video_type = item

    def clean_text_btn(self):
        self.textBrowser_text.clear()

    def close_all_threads(self):
        self.close_video_sender()
        self.close_audio_sender()
        self.close_audio_player()
        self.close_file_sender()
        self.close_file_downloader()
        self.close_live_client()
        self.close_live_server()
        self.close_msg_client()
        # ...
        self.label_video.clear()
        self.label_video.repaint()

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

    def con_connect_btn(self):
        text = self.pushButton_connect.text()
        if text == '连接':
            self.run_msg_client()
            self.pushButton_connect.setText('关闭')
        else:
            if self.msg_client.is_connected:
                self.close_msg_client()
            else:
                self.pushButton_connect.setText('连接')

    def con_live_client_btn(self):
        text = self.pushButton_send_broadcast.text()
        if text == '视频广播':
            self.run_live_client()
            self.pushButton_send_broadcast.setText('关闭广播')
        else:
            self.close_live_client()

    def con_live_server_btn(self):
        text = self.pushButton_get_broadcast.text()
        if text == '接收广播':
            self.run_live_server()
            self.pushButton_get_broadcast.setText('关闭接收')
        else:
            self.close_live_server()

    def con_video_btn(self):
        text = self.pushButton_start_vs.text()
        if text == '视频':
            if not self.video_sender:
                if not self.client_connected():
                    self.show_log('video sender: no connect')
                    return
                self.run_video_sender()
                self.pushButton_start_vs.setText('关闭')
        else:
            self.close_video_sender()

    def con_audio_btn(self):
        text = self.pushButton_start_as.text()
        if text == '音频':
            if not self.audio_sender:
                if not self.client_connected():
                    self.show_log('audio sender: no connect')
                    return
                self.run_audio_sender()
                self.pushButton_start_as.setText('关闭')
        else:
            self.close_audio_sender()

    def con_file_btn(self):
        if not self.file_sender:
            if not self.client_connected():
                self.show_log('file sender: no connect')
                return
            self.run_file_sender()
        else:
            self.close_file_sender()

    def run_msg_client(self):
        if self.msg_client:
            return
        self.to_ip = self.lineEdit_ip.text()
        self.msg_client = MessageClient(self.to_ip)
        self.msg_client._log.connect(self.show_log)
        self.msg_client.start()

    def close_msg_client(self):
        if self.msg_client:
            self.msg_client.send_message('close')
            self.msg_client.quit()
            self.msg_client = None
        self.pushButton_connect.setText('连接')

    def run_video_sender(self):
        if self.video_sender:
            return
            # 创建视频发送线程
        self.video_sender = VideoSender(self.video_type)
        self.video_sender.open_server()
        self.video_sender.set_sender(self.msg_client)
        # 连接信号，绑定回调事件
        self.video_sender._video_local.connect(self.show_video_src)
        self.video_sender.start()

    def close_video_sender(self):
        if self.video_sender:
            self.video_sender.quit()
            self.video_sender = None
        self.pushButton_start_vs.setText('视频')
        self.label_video_2.clear()
        self.label_video_2.repaint()

    def run_live_client(self):
        if self.live_client:
            return
        # 创建视频广播线程
        broadcast_ip = self.lineEdit_broadcast.text()
        key = str(self.lineEdit_broadcast_sec.text())
        self.live_client = LiveClient(broadcast_ip, key, self.video_type)
        self.live_client.set_quality(self.video_quality)
        self.live_client.set_percent(self.video_percent)
        self.live_client.open_server()
        self.live_client._video_local.connect(self.show_video_src)
        self.live_client.start()

    def close_live_client(self):
        if self.live_client:
            self.live_client.quit()
            self.live_client = None
        self.pushButton_send_broadcast.setText('视频广播')

    def run_live_server(self):
        if self.live_server:
            return
        # 创建广播接收线程
        key = str(self.lineEdit_broadcast_sec.text())
        self.live_server = LiveServer(key)
        self.live_server._video.connect(self.show_video)
        self.live_server._log.connect(self.show_log)
        self.live_server.start()

    def close_live_server(self):
        if self.live_server:
            self.live_server.quit()
            self.live_server = None
        self.pushButton_get_broadcast.setText('接收广播')

    def run_audio_sender(self):
        if self.audio_sender:
            return
        self.audio_sender = AudioSender()
        self.audio_sender.set_sender(self.msg_client)
        self.audio_sender.open_server(self.audio_type)
        self.audio_sender.start()

    def close_audio_sender(self):
        if self.audio_sender:
            self.audio_sender.quit()
            self.audio_sender = None
        self.pushButton_start_as.setText('音频')

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

    def send_text(self):  # 绑定回车事件
        text = str(self.lineEdit_text.text())
        if not text:
            return
        if not self.client_connected():
            self.show_log('text sender: no connect')
            return
        self.textBrowser_text.append(
            '<span style="color:blue">我: ' + text + '</span>')
        self.lineEdit_text.setText('')

        self.msg_client.send_text(text)

    """
    线程回调
    处理接收的各种信息
    message, video, audio, file, text
    """

    def show_msg(self, data):  # 对接 Message 的 TCP 线程
        # data 格式 ip:port:msg
        """
        data 格式
        {
            'conn': conn,
            'addr': addr,
            'data': data
        }
        """
        conn: SSLSocket = data['conn']
        addr: tuple = data['addr']
        data: str = data['data']

        if data == 'connect':
            if self.msg_client:  # 对方接受连接后的自动连接请求
                if self.msg_client.wait_ip == addr[0]:
                    # 自动连接
                    self.msg_server.accept_connect(addr)
                    self.msg_client.send_text('连接成功！')
                else:
                    # 自动拒绝
                    self.msg_server.close_connect(addr)
                return

            question_msg = ('是否接受来至%s:%s的' % addr) + '连接？'
            reply = QMessageBox.question(
                self, '提示', question_msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                # 接受连接
                self.msg_server.accept_connect(addr)
                # 同时发起对方连接的请求
                self.lineEdit_ip.setText(addr[0])
                self.con_connect_btn()
            else:
                # 拒绝连接
                self.msg_server.close_connect(addr)
        elif data == 'close':
            try:
                self.msg_client.send_message('close')
            except:
                pass
            self.close_all_threads()

    def show_video_src(self, q_image):  # 线程回调-显示视频发送源
        if not q_image:
            return
        pixmap = QPixmap.fromImage(q_image).scaled(
            self.label_video_2.size(), transformMode=1)  # 平滑缩放
        self.label_video_2.setPixmap(pixmap)
        self.label_video_2.repaint()

    def show_video(self, receive_data: bytes):  # 线程回调-显示视频接收源
        if not receive_data:
            self.label_video.clear()
            self.label_video.repaint()
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

    def show_audio(self, data: bytes):  # 显示视频接收源
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

    def show_file(self, data: bytes):  # 下载接收的文件
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
