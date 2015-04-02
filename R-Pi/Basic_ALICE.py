__author__ = 'Krish'

import socket

ALICE = ("192.168.2.38", 8055)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind(ALICE)

print "Alice.. Waiting for Bob's bird"

while True:
    msg = sock.recvfrom(1024)[0]
    print msg

