__author__ = 'Krish'

import os
import kodo
import numpy as np
from math import sqrt
import threading
import time
import socket


global DECODED
global buf
global adr
global relays
global sleep_time
global time_taken
global encoded_packets
global decoded_packets
global lin_dep_pkts
global relayed_pkts
global free_socket


relays = 3
sleep_time = 0.000001

DECODED = False
buf = [0 for _ in range(20)]
adr = [(1000, 1000) for _ in range(20)]
time_taken = 0
encoded_packets = 0
decoded_packets = 0
lin_dep_pkts = 0
relayed_pkts = 0
free_socket = 9050


def threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper


class Node:
    def __init__(self, x, y, bufindex):
        self.x = x
        self.y = y
        self.bufindex = bufindex
        #adr[bufindex] = (x, y)
        self.symbol_size = 128
        self.symbols = 60

    def dist(self, x, y):
        # print(x)
        # print(y)
        # print(self.x)
        # print(self.y)
        distance = sqrt((self.x - x)**2 + (self.y - y)**2)
        #print("Distance = " + str(distance))
        return distance


    @threaded
    def source(self, FILE):
        global encoded_packets
        global free_socket
        # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # s.bind(('', 8500))

        encoder_factory = kodo.FullVectorEncoderFactoryBinary(self.symbols, self.symbol_size)
        encoder = encoder_factory.build()

        if not FILE == "":
            f = open(FILE, 'rb')
            data_in = f.read()
        else:
            data_in = os.urandom(encoder.block_size())

        encoder.set_symbols(data_in)

        """
        Assumption: "Decoded" message arrives in no delay to the encoder
        """
        #print(self.bufindex)
        while not DECODED:
            #print("---Encoding---")
            buf[self.bufindex] = encoder.encode()
            encoded_packets += 1
            time.sleep(sleep_time)                    # DELAY INTRODUCED to synchronise Encoding and decoding.


