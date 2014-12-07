__author__ = 'Krish'

import time

from Kodo_File_Trans.KODO_FileTrans import *


start = time.time()

adr = ('127.0.0.1', 8383)
sendFileKODO(adr, '/Users/Krish/Desktop/sorc.txt')

print "TIME TO TRANSFER : " + str(time.time()-start)