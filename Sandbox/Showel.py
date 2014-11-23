__author__ = 'Krish'

from KODO_FileTrans import *
import time

start = time.time()

adr = ('127.0.0.1', 8383)
sendFileKODO(adr, '/Users/Krish/Desktop/sorc.txt')

print "TIME TO TRANSFER : " + str(time.time()-start)