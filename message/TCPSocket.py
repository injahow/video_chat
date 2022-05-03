# -*- coding: utf-8 -*-

from abc import abstractmethod
import os
import socket
import ssl
import struct
import pickle
import threading

from message.utils import DataHandler, SSLTools

dataHandler = DataHandler()


class Server:  # data 接收者 - 只接收
    def __init__(self) -> None:
        self.address = ('', 9876)
        self.sock = None
        self.ssock = None
        self.conn_map: dict[tuple, ssl.SSLSocket] = {}
        # 生成SSL上下文
        ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ctx.load_default_certs(ssl.Purpose.CLIENT_AUTH)

        # 加载SSL文件
        if not (os.path.exists('ssl.cer') and os.path.exists('private_key.key')):
            SSLTools.makefile('ssl.cer', 'private_key.key')

        ctx.load_cert_chain(
            certfile='ssl.cer',
            keyfile='private_key.key')

        self.ctx = ctx

    @abstractmethod
    def emit(self, conn, addr: tuple, msg: dict):
        pass

    @abstractmethod
    def _print(self, text: str):
        pass

    def accept_connect(self, addr):
        self._print('Accept connection from %s:%s !' % addr)
        conn = self.conn_map[addr]
        link = threading.Thread(
            target=self.connect_thread, args=(conn, addr))
        link.setDaemon(True)
        link.start()

    def close_connect(self, addr):
        conn = self.conn_map.get(addr)
        if conn:
            self.conn_map.pop(addr)
            conn.close()

    def connect_thread(self, conn: ssl.SSLSocket, addr: tuple):
        """
        连接线程：用于接收客户端消息
        """
        conn_map = self.conn_map

        data_buffer = b''
        payload_size = struct.calcsize('L')  # 结果为4

        while conn_map.get(addr):
            # 接收客户端信息，并解包
            try:
                while len(data_buffer) < payload_size:
                    data_buffer += conn.recv(10240)
                packed_size = data_buffer[:payload_size]
                data_buffer = data_buffer[payload_size:]
                msg_size = struct.unpack('L', packed_size)[0]
                while len(data_buffer) < msg_size:
                    data_buffer += conn.recv(10240)
                zipframe_data = data_buffer[:msg_size]
                frame_data = dataHandler.decode(zipframe_data)
                frame = pickle.loads(frame_data)
                # emit 回调，执行接收消息后的业务
                self.emit(conn, addr, frame)
                # data 偏移
                data_buffer = data_buffer[msg_size:]
            except:
                break

        conn_map.pop(addr)
        self._print('%s:%s connect close !!!' % addr)
        conn.close()

    def listen(self):
        """
        TCP 绑定监听
        """
        # tcp sock
        sock = self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(self.address)
        sock.listen(3)
        print('MessageServer bind complete !')
        # 将socket 打包成 SSL socket
        ctx = self.ctx
        ssock = self.ssock = ctx.wrap_socket(sock, server_side=True)

        while True:
            # 接受新的连接
            conn, addr = ssock.accept()
            self.conn_map[addr] = conn
            self.emit(conn, addr, {
                'type': 'message',
                'data': 'connect'
            })


class Client:  # data 发送者 - 只发送
    def __init__(self) -> None:
        self.sock = None
        self.ssock = None
        # 生成不验证的 SSL 上下文
        self.ctx = ssl._create_unverified_context()
        self.is_connected = False
        self.wait_ip = ''
        self.closed = False

    @abstractmethod
    def _print(self, text: str):
        pass

    def get_connect(self, tar_ip: str):
        self._print('will connect to ' + tar_ip)
        try:
            # 与服务端建立socket连接
            self.sock = socket.create_connection(
                (tar_ip, 9876), timeout=3)
            # 将socket打包成 SSL socket
            # 注意 server_hostname 是指服务端证书中设置的CN
            self.ssock = self.ctx.wrap_socket(
                self.sock, server_hostname='127.0.0.1')
            self.is_connected = True
            self.closed = False
            self._print('connectioning, wait for confirmation ...')
            self.wait_ip = tar_ip
        except:
            self._print('create connection failed ?')
            self.close_connect()

    def close_connect(self):
        if self.ssock:
            self.ssock.close()
        if self.sock:
            self.sock.close()
        self.wait_ip = ''
        self.is_connected = False
        self.closed = True

    def sendall(self, obj):
        senddata = pickle.dumps(obj)
        senddata = dataHandler.encode(senddata)
        try:
            self.ssock.sendall(struct.pack('L', len(senddata)) + senddata)
        except:
            self._print('发送失败')
