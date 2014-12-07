__author__ = 'Krish'

import socket

from TCP_File_Trans.TCP_FileTrans import *


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 8090))
s.listen(5)

while 1:                        # Why is 'While 1' Mandatory???
    (cs, addr) = s.accept()
    print(addr)

    getFileTCP(cs)

