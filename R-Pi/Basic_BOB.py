__author__ = 'Krish'

import socket
import time


ALICE = ("192.168.3.36", 8053)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

for i in range(100):
    sock.sendto("tweet to alice4 " + str(i), ALICE)
    print "tweet-tweet ", i
    #time.sleep(0.05)



