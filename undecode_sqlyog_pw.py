#!/usr/bin/env python

# 解密sqlyog保存的db密码

import sys
import socket
from base64 import b64decode


def usage():
    print("usage: {0} encrypted_password".format(sys.argv[0]))
    sys.exit(1)


def decode_password(encoded):
    tmp = bytearray(b64decode(encoded))

    for i in range(len(tmp)):
        tmp[i] = rotate_left(tmp[i], 8)

    return tmp.decode('utf-8')


def rotate_left(num, bits):
    bit = num & (1 << (bits - 1))
    num <<= 1
    if (bit):
        num |= 1
    num &= (2 ** bits - 1)

    return num


if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     usage()

    # print(decode_password(sys.argv[1]))
    #print(decode_password('mBmZGpob'))
    print(socket.gethostbyname_ex("baidu.com"))
    sys.exit(0)
