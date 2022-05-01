# -*- coding: utf-8 -*-

from abc import abstractmethod
import socket
import sys

from module.utils import DataHandler

BUFFER_SIZE = 61440


class Server:  # data 发送方
    def __init__(self, broadcast_ip) -> None:
        self.broadcast_ip = broadcast_ip
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def set_handler(self, sec_key):
        self.dataHandler = DataHandler(sec_key)

    def __sendto(self, data: bytes):
        data = self.dataHandler.encode(data)
        self.sock.sendto(data, (self.broadcast_ip, 9877))

    def sendto(self, data: bytes):
        len_data = sys.getsizeof(data)
        delta = BUFFER_SIZE
        if len_data > delta:  # udp数据包最大支持65507/4*10240=4096
            str_encode_arr = []
            i = 0
            while True:
                p = i * delta
                q = p + delta
                if p >= len_data:
                    end = (str(i)+':').encode()+data[p-delta:]+b'end'
                    str_encode_arr.append(end)
                    break
                str_encode_arr.append((str(i)+':').encode()+data[p:q])
                i += 1
            for str_encode in str_encode_arr:
                self.__sendto(str_encode)
        else:
            self.__sendto(b'0:'+data+b'end')


class Client:  # data 接收方
    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.closed = False

    def set_handler(self, sec_key):
        self.dataHandler = DataHandler(sec_key)

    @abstractmethod
    def emit(self):
        pass

    @abstractmethod
    def _print(self):
        pass

    def close_connect(self):
        if self.sock:
            self.sock.close()
        self.closed = True

    def bind(self):
        self.sock.bind(('', 9877))
        data_buffer = []
        while not self.closed:
            # 接收客户端信息，并解包
            try:
                data = self.sock.recv(BUFFER_SIZE)
                data = self.dataHandler.decode(data)
                data_id, data = data.split(b':', 1)
                if data[-3:] != b'end':
                    data_buffer.append((int(data_id), data))
                    continue
                data = data[:-3]
                data_buffer.append((int(data_id), data))
                # 排序 data_buffer
                data_buffer.sort(key=lambda x: x[0], reverse=False)
                jpg_data = b''.join([x[1] for x in data_buffer])
                self.emit(jpg_data)
            except:
                self._print('数据接收错误')
            data_buffer.clear()
