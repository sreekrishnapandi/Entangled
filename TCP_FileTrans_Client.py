__author__ = 'Krish'

import socket
from TCP_FileTrans import *


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 8090))

sendFileTCP(s, '/Users/Krish/Desktop/fund.pdf')