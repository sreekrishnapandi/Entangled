__author__ = 'Krish'

import os

def getFileTCP(s):
    fsize = int(s.recv(1024))
    recvSize = 0
    f = open('/Users/Krish/Desktop/Bla.pdf', mode='w+b')
    while recvSize < fsize:
        rx = s.recv(512)
        f.write(rx)
        recvSize += len(rx)
    f.close()


def sendFileTCP(s,file):
    fsize = os.path.getsize(file)
    s.send(str(fsize))
    f = open(file, 'rb')
    sentCount = 0
    while sentCount < fsize:
        buf = f.read(min(512, fsize - sentCount))
        s.send(buf)
        sentCount += len(buf)