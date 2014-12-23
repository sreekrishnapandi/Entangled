__author__ = 'Krish'

import os
import kodo
import numpy as np
from math import sqrt
import threading
import time
import socket


# global DECODED
# global buf
# global adr
# global relays
# global sleep_time
# global time_taken
# global encoded_packets
# global decoded_packets
# global lin_dep_pkts
# global relayed_pkts
# global free_socket
# global start_socket
#
#
# relays = 3
# sleep_time = 0.000001
#
# DECODED = False
# buf = [0 for _ in range(20)]
# adr = [(1000, 1000) for _ in range(20)]
# time_taken = 0
# encoded_packets = 0
# decoded_packets = 0
# lin_dep_pkts = 0
# relayed_pkts = 0
# free_socket = 3000
# start_socket = 3000


def threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper


def initialize():
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
    global sync_nodes
    global lock
    global token
    global free_socket
    global start_socket
    global nxt_bufIndex

    DECODED = False
    buf = [0 for _ in range(20)]
    adr = [(1000, 1000) for _ in range(20)]
    time_taken = 0
    encoded_packets = 0
    decoded_packets = 0
    lin_dep_pkts = 0
    relayed_pkts = 0
    sync_nodes = 0
    lock = threading.Lock()
    token = [1 for _ in range(20)]
    free_socket = 3000
    start_socket = 3000
    nxt_bufIndex = 0


def delay(): time.sleep(0.001)


class Node:
    def __init__(self, x, y):
        global free_socket
        global nxt_bufIndex
        lock.acquire()
        self.sockID = free_socket
        free_socket += 1
        self.bufindex = nxt_bufIndex
        nxt_bufIndex += 1
        lock.release()

        self.x = x
        self.y = y
        adr[self.bufindex] = (x, y)
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
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', self.sockID))

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
            pkt = encoder.encode()
            #print(pkt)
            for i in range(relays+2):
                if np.random.randint(100) >= (self.dist(adr[i][0], adr[i][1])) * 5 and not adr[i] == (self.x, self.y):
                    s.sendto(pkt, ('', start_socket + i))
            encoded_packets += 1
            # print("Encoded Packets : " + str(encoded_packets))
            #time.sleep(sleep_time)                    # DELAY INTRODUCED to synchronise Encoding and decoding.
        s.close()


    @threaded
    def relay(self):
        global DECODED

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', self.sockID))
        s.settimeout(0.0001)

        # print(".........Decoding..")

        decoder_factory = kodo.FullVectorDecoderFactoryBinary(self.symbols, self.symbol_size)
        recoder = decoder_factory.build()

        #print(adr[1])

        while not DECODED:
            # print("####Relay#### " + str(self.bufindex))
            try:
                rcv = s.recvfrom(180)[0]
                recoder.decode(rcv)
            except socket.timeout:
                pass
            pkt = recoder.recode()
            for i in range(relays+2):               # (relays+1) because encoder also produces packets
                if np.random.randint(100) >= (self.dist(adr[i][0], adr[i][1])) * 5 and not adr[i] == (self.x, self.y):
                    s.sendto(pkt, ('', start_socket + i))
                    #print("Decoder Rank : " + str(decoder.rank()))

            #time.sleep(sleep_time)                    # DELAY INTRODUCED to synchronise Encoding and decoding.
        s.close()

    @threaded
    def sink(self):
        start = time.time()
        global DECODED
        global time_taken
        global decoded_packets

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', self.sockID))
        s.settimeout(0.0001)

        # print(".........Decoding..")

        decoder_factory = kodo.FullVectorDecoderFactoryBinary(self.symbols, self.symbol_size)
        decoder = decoder_factory.build()

        while not decoder.is_complete():
            try:
                rcv = s.recvfrom(180)[0]
                #print(rcv)
                decoder.decode(rcv)
                # print("Decoder Rank : " + str(decoder.rank()))
            except socket.timeout:

                pass

            #time.sleep(sleep_time)              # DELAY INTRODUCED to synchronise Encoding and decoding.
        s.close()

        if decoder.is_complete():
            DECODED = True
            #print("DECODED")
            time_taken = time.time() - start

"""------- Average Statistics (Text report) --------"""

avg_time_taken = 0
avg_encoded_packets = 0
avg_decoded_packets = 0

iterations = 500

for i in range(iterations):
    initialize()
    relays = 3
    src = Node(0, 0)
    snk = Node(0, 19)
    relay1 = Node(5, 5)
    relay2 = Node(7, 10)
    relay3 = Node(5, 15)
    #relay4 = Node(5, 5)

    src.source("")
    snk.sink()
    relay1.relay()
    relay2.relay()
    relay3.relay()
    #relay4.relay()

    while not DECODED: pass
    print("==================------------------------- Encoded Pkts : " + str(encoded_packets))
    avg_time_taken += time_taken
    avg_encoded_packets += encoded_packets
    avg_decoded_packets += decoded_packets
    delay()                     # To wait for OS to close the sockets , so that its available for next iteration


delay()
print("\nAverage of " + str(iterations) + " iterations")
print("Time Taken    : " + str(avg_time_taken/iterations))
print("Min req packets : " + str(src.symbols))
print("Encoded Pkts : " + str(avg_encoded_packets/iterations))
print("Decoded Pkts : " + str(avg_decoded_packets/iterations))
