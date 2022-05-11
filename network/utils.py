# -*- coding: utf-8 -*-

import zlib
import hashlib
from Crypto.Cipher import AES


class SSLTools:
    def generate_adhoc_ssl_pair(cn=None):
        from datetime import datetime as dt
        from datetime import timedelta

        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import rsa

        p_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )

        # pretty damn sure that this is not actually accepted by anyone
        if cn is None:
            cn = u'*'

        # subject：使用者
        subject = x509.Name(
            [
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'myself'),
                x509.NameAttribute(NameOID.COMMON_NAME, '127.0.0.1'),
                x509.NameAttribute(NameOID.COUNTRY_NAME, 'cn')
            ]
        )

        # issuer：颁发机构
        issuer = x509.Name(
            [
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'myself'),
                x509.NameAttribute(NameOID.COMMON_NAME, '127.0.0.1'),
                x509.NameAttribute(NameOID.COUNTRY_NAME, 'cn')
            ]
        )

        # 生成证书，cert使用私钥签名
        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(p_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(dt.utcnow() + timedelta())
            .not_valid_after(dt.utcnow() + timedelta(days=365))
            # .sign(私钥，摘要生成算法，填充方式)
            .sign(p_key, hashes.SHA256(), default_backend())
        )

        return cert, p_key

    def makefile(cer_path='./ssl.cer', p_key_path='./private_key.key'):

        from cryptography.hazmat.primitives import serialization
        cert, p_key = SSLTools.generate_adhoc_ssl_pair()

        # ? print(cert)
        # 将证书类对象转换成PEM格式的字节串
        cert_bytes = cert.public_bytes(serialization.Encoding.PEM)
        # 保存证书
        with open(cer_path, mode='wb') as cert_file:
            cert_file.write(cert_bytes)

        # 将私钥类对象转换成PEM格式的字节串
        private_bytes = p_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()  # 私钥不加密
        )
        # 保存私钥
        with open(p_key_path, mode='wb') as p_key_file:
            p_key_file.write(private_bytes)


class AESHandler:
    def __init__(self, key: bytes):
        self.key = key
        self.mode = AES.MODE_ECB  # 操作模式选择ECB

    def encrypt(self, text: bytes) -> bytes:
        """AES加密"""
        aes = AES.new(self.key, self.mode)
        while len(text) % 16 != 0:  # 对字节型数据进行长度判断
            text += b'\x00'  # 如果字节型数据长度不是16倍整数就进行补充
        return aes.encrypt(text)

    def decrypt(self, text: bytes) -> bytes:
        """AES解密"""
        aes = AES.new(self.key, self.mode)
        return aes.decrypt(text)  # 密文进行解密，返回明文的bytes


def md5byte16(s: str) -> bytes:
    md5 = hashlib.md5()
    md5.update(s.encode('utf-8'))
    return md5.digest()  # hexdigest


class DataHandler:

    def __init__(self, key='') -> None:
        self.AES = None
        if key:
            self.AES = AESHandler(md5byte16(key))

    def decode(self, receive_data: bytes) -> bytes:
        try:
            if self.AES:
                receive_data = self.AES.decrypt(receive_data)
            receive_data = zlib.decompress(receive_data)
        except Exception as err:
            print('DataHandler decode error:', err)
            receive_data = b''
        return receive_data

    def encode(self, send_data: bytes) -> bytes:
        try:
            send_data = zlib.compress(send_data)
            if self.AES:
                send_data = self.AES.encrypt(send_data)
        except Exception as err:
            print('DataHandler encode error:', err)
            send_data = b''
        return send_data
