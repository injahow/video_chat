# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\1813010038\毕业设计\video_chat\ui\main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1020, 820)
        MainWindow.setMinimumSize(QtCore.QSize(1020, 820))
        MainWindow.setMaximumSize(QtCore.QSize(1020, 820))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_video_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_video_2.setGeometry(QtCore.QRect(760, 30, 231, 161))
        self.label_video_2.setFrameShape(QtWidgets.QFrame.Box)
        self.label_video_2.setText("")
        self.label_video_2.setObjectName("label_video_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 200, 121, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(760, 10, 131, 21))
        self.label_4.setObjectName("label_4")
        self.groupBox_video_type = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_video_type.setGeometry(QtCore.QRect(30, 10, 721, 181))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_video_type.setFont(font)
        self.groupBox_video_type.setObjectName("groupBox_video_type")
        self.lineEdit_ip = QtWidgets.QLineEdit(self.groupBox_video_type)
        self.lineEdit_ip.setGeometry(QtCore.QRect(70, 20, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_ip.setFont(font)
        self.lineEdit_ip.setObjectName("lineEdit_ip")
        self.lineEdit_broadcast = QtWidgets.QLineEdit(self.groupBox_video_type)
        self.lineEdit_broadcast.setGeometry(QtCore.QRect(70, 60, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_broadcast.setFont(font)
        self.lineEdit_broadcast.setClearButtonEnabled(False)
        self.lineEdit_broadcast.setObjectName("lineEdit_broadcast")
        self.label = QtWidgets.QLabel(self.groupBox_video_type)
        self.label.setGeometry(QtCore.QRect(10, 20, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox_video_type)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pushButton_start_vs = QtWidgets.QPushButton(self.groupBox_video_type)
        self.pushButton_start_vs.setGeometry(QtCore.QRect(220, 60, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_start_vs.setFont(font)
        self.pushButton_start_vs.setObjectName("pushButton_start_vs")
        self.pushButton_close = QtWidgets.QPushButton(self.groupBox_video_type)
        self.pushButton_close.setGeometry(QtCore.QRect(310, 20, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_close.setFont(font)
        self.pushButton_close.setObjectName("pushButton_close")
        self.pushButton_get_ip = QtWidgets.QPushButton(self.groupBox_video_type)
        self.pushButton_get_ip.setGeometry(QtCore.QRect(310, 100, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_get_ip.setFont(font)
        self.pushButton_get_ip.setObjectName("pushButton_get_ip")
        self.pushButton_start_as = QtWidgets.QPushButton(self.groupBox_video_type)
        self.pushButton_start_as.setGeometry(QtCore.QRect(280, 60, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_start_as.setFont(font)
        self.pushButton_start_as.setObjectName("pushButton_start_as")
        self.pushButton_start_fs = QtWidgets.QPushButton(self.groupBox_video_type)
        self.pushButton_start_fs.setGeometry(QtCore.QRect(340, 60, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_start_fs.setFont(font)
        self.pushButton_start_fs.setObjectName("pushButton_start_fs")
        self.pushButton_end = QtWidgets.QPushButton(self.groupBox_video_type)
        self.pushButton_end.setGeometry(QtCore.QRect(310, 140, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_end.setFont(font)
        self.pushButton_end.setObjectName("pushButton_end")
        self.pushButton_send_broadcast = QtWidgets.QPushButton(self.groupBox_video_type)
        self.pushButton_send_broadcast.setGeometry(QtCore.QRect(10, 140, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_send_broadcast.setFont(font)
        self.pushButton_send_broadcast.setObjectName("pushButton_send_broadcast")
        self.pushButton_connect = QtWidgets.QPushButton(self.groupBox_video_type)
        self.pushButton_connect.setGeometry(QtCore.QRect(220, 20, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_connect.setFont(font)
        self.pushButton_connect.setObjectName("pushButton_connect")
        self.lineEdit_text = QtWidgets.QLineEdit(self.groupBox_video_type)
        self.lineEdit_text.setGeometry(QtCore.QRect(410, 140, 301, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_text.setFont(font)
        self.lineEdit_text.setText("")
        self.lineEdit_text.setObjectName("lineEdit_text")
        self.textBrowser_text = QtWidgets.QTextBrowser(self.groupBox_video_type)
        self.textBrowser_text.setGeometry(QtCore.QRect(410, 20, 301, 111))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textBrowser_text.setFont(font)
        self.textBrowser_text.setObjectName("textBrowser_text")
        self.lineEdit_broadcast_sec = QtWidgets.QLineEdit(self.groupBox_video_type)
        self.lineEdit_broadcast_sec.setGeometry(QtCore.QRect(80, 100, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(10)
        self.lineEdit_broadcast_sec.setFont(font)
        self.lineEdit_broadcast_sec.setText("")
        self.lineEdit_broadcast_sec.setObjectName("lineEdit_broadcast_sec")
        self.label_5 = QtWidgets.QLabel(self.groupBox_video_type)
        self.label_5.setGeometry(QtCore.QRect(10, 100, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.pushButton_set_video_type = QtWidgets.QPushButton(self.groupBox_video_type)
        self.pushButton_set_video_type.setGeometry(QtCore.QRect(220, 100, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_set_video_type.setFont(font)
        self.pushButton_set_video_type.setObjectName("pushButton_set_video_type")
        self.pushButton_clean_text = QtWidgets.QPushButton(self.groupBox_video_type)
        self.pushButton_clean_text.setGeometry(QtCore.QRect(220, 140, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_clean_text.setFont(font)
        self.pushButton_clean_text.setObjectName("pushButton_clean_text")
        self.pushButton_get_broadcast = QtWidgets.QPushButton(self.groupBox_video_type)
        self.pushButton_get_broadcast.setGeometry(QtCore.QRect(110, 140, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_get_broadcast.setFont(font)
        self.pushButton_get_broadcast.setObjectName("pushButton_get_broadcast")
        self.label_video = QtWidgets.QLabel(self.centralwidget)
        self.label_video.setGeometry(QtCore.QRect(30, 220, 961, 541))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_video.setFont(font)
        self.label_video.setFrameShape(QtWidgets.QFrame.Box)
        self.label_video.setText("")
        self.label_video.setObjectName("label_video")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1020, 29))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action80 = QtWidgets.QAction(MainWindow)
        self.action80.setObjectName("action80")
        self.action60 = QtWidgets.QAction(MainWindow)
        self.action60.setObjectName("action60")
        self.action40 = QtWidgets.QAction(MainWindow)
        self.action40.setObjectName("action40")
        self.action20 = QtWidgets.QAction(MainWindow)
        self.action20.setObjectName("action20")
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action100 = QtWidgets.QAction(MainWindow)
        self.action100.setObjectName("action100")
        self.action_per1 = QtWidgets.QAction(MainWindow)
        self.action_per1.setObjectName("action_per1")
        self.action_per2 = QtWidgets.QAction(MainWindow)
        self.action_per2.setObjectName("action_per2")
        self.action_per3 = QtWidgets.QAction(MainWindow)
        self.action_per3.setObjectName("action_per3")
        self.action_per4 = QtWidgets.QAction(MainWindow)
        self.action_per4.setObjectName("action_per4")
        self.action_per5 = QtWidgets.QAction(MainWindow)
        self.action_per5.setObjectName("action_per5")
        self.action_audio_t1 = QtWidgets.QAction(MainWindow)
        self.action_audio_t1.setObjectName("action_audio_t1")
        self.action_audio_t2 = QtWidgets.QAction(MainWindow)
        self.action_audio_t2.setObjectName("action_audio_t2")
        self.menu.addAction(self.action100)
        self.menu.addAction(self.action80)
        self.menu.addAction(self.action60)
        self.menu.addAction(self.action40)
        self.menu.addAction(self.action20)
        self.menu_2.addAction(self.action_per1)
        self.menu_2.addAction(self.action_per2)
        self.menu_2.addAction(self.action_per3)
        self.menu_2.addAction(self.action_per4)
        self.menu_2.addAction(self.action_per5)
        self.menu_3.addAction(self.action_audio_t1)
        self.menu_3.addAction(self.action_audio_t2)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.pushButton_start_vs, self.pushButton_start_as)
        MainWindow.setTabOrder(self.pushButton_start_as, self.pushButton_start_fs)
        MainWindow.setTabOrder(self.pushButton_start_fs, self.pushButton_get_ip)
        MainWindow.setTabOrder(self.pushButton_get_ip, self.lineEdit_broadcast)
        MainWindow.setTabOrder(self.lineEdit_broadcast, self.lineEdit_ip)
        MainWindow.setTabOrder(self.lineEdit_ip, self.pushButton_end)
        MainWindow.setTabOrder(self.pushButton_end, self.pushButton_close)
        MainWindow.setTabOrder(self.pushButton_close, self.pushButton_send_broadcast)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "局域网视频通信程序"))
        self.label_3.setText(_translate("MainWindow", "接收视频/桌面"))
        self.label_4.setText(_translate("MainWindow", "本地视频/桌面"))
        self.groupBox_video_type.setTitle(_translate("MainWindow", "功能"))
        self.lineEdit_ip.setText(_translate("MainWindow", "127.0.0.1"))
        self.lineEdit_broadcast.setText(_translate("MainWindow", "192.168.31.255"))
        self.label.setText(_translate("MainWindow", "对方IP:"))
        self.label_2.setText(_translate("MainWindow", "广播IP:"))
        self.pushButton_start_vs.setText(_translate("MainWindow", "视频"))
        self.pushButton_close.setText(_translate("MainWindow", "断开"))
        self.pushButton_get_ip.setText(_translate("MainWindow", "广播设置"))
        self.pushButton_start_as.setText(_translate("MainWindow", "音频"))
        self.pushButton_start_fs.setText(_translate("MainWindow", "文件"))
        self.pushButton_end.setText(_translate("MainWindow", "退出程序"))
        self.pushButton_send_broadcast.setText(_translate("MainWindow", "视频广播"))
        self.pushButton_connect.setText(_translate("MainWindow", "连接"))
        self.lineEdit_text.setPlaceholderText(_translate("MainWindow", "在此处进行聊天~~~"))
        self.textBrowser_text.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.lineEdit_broadcast_sec.setPlaceholderText(_translate("MainWindow", "留空不加密"))
        self.label_5.setText(_translate("MainWindow", "广播密钥:"))
        self.pushButton_set_video_type.setText(_translate("MainWindow", "视频设置"))
        self.pushButton_clean_text.setText(_translate("MainWindow", "清除聊天"))
        self.pushButton_get_broadcast.setText(_translate("MainWindow", "接收广播"))
        self.menu.setTitle(_translate("MainWindow", "视频质量"))
        self.menu_2.setTitle(_translate("MainWindow", "视频尺寸"))
        self.menu_3.setTitle(_translate("MainWindow", "音频类型"))
        self.action80.setText(_translate("MainWindow", "80"))
        self.action60.setText(_translate("MainWindow", "60"))
        self.action40.setText(_translate("MainWindow", "40"))
        self.action20.setText(_translate("MainWindow", "20"))
        self.action.setText(_translate("MainWindow", "广播质量"))
        self.action100.setText(_translate("MainWindow", "100"))
        self.action_per1.setText(_translate("MainWindow", "100%"))
        self.action_per2.setText(_translate("MainWindow", "90%"))
        self.action_per3.setText(_translate("MainWindow", "80%"))
        self.action_per4.setText(_translate("MainWindow", "70%"))
        self.action_per5.setText(_translate("MainWindow", "60%"))
        self.action_audio_t1.setText(_translate("MainWindow", "录音"))
        self.action_audio_t2.setText(_translate("MainWindow", "系统"))
