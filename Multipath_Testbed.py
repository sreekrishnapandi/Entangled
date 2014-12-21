__author__ = 'Krish'

import os
import kodo
import numpy as np
from math import sqrt
import threading
import time

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

relays = 1
sleep_time = 0.00001

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

"""
Problem : Python - thread scheduling =>
                            * multiple Encoding cycles and multiple decoding/ relay cycles done in bunches.
# Token is to ensure that each node iterates not more than once.
# Lock and Sync_nodes ensure that all nodes iterate atleast once.
"""

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


def delay(): time.sleep(0.001)


def threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper


class Node:
    def __init__(self, x, y, bufindex):
        self.x = x
        self.y = y
        self.bufindex = bufindex
        adr[bufindex] = (x, y)
        self.symbol_size = 128
        self.symbols = 60
        lock = threading.Lock()

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
        global sync_nodes
        global relays
        global token
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
            lock.acquire()
            if not sync_nodes < relays+1:
                token = [1 for _ in range(relays+3)]        # Give one token to each node.
                #print("---Encoding---")
                buf[self.bufindex] = encoder.encode()
                encoded_packets += 1
                print("Encoded Packets : " + str(encoded_packets))

                sync_nodes = 0
            try:
                lock.release()
            finally: pass
            time.sleep(sleep_time)                    # DELAY INTRODUCED to synchronise Encoding and decoding.

    @threaded
    def relay(self):
        global DECODED
        global sync_nodes
        global lock
        # print(".........Decoding..")

        decoder_factory = kodo.FullVectorDecoderFactoryBinary(self.symbols, self.symbol_size)
        recoder = decoder_factory.build()

        #print(adr[1])

        while not DECODED:
            lock.acquire()
            if token[self.bufindex] == 1 :
                sync_nodes += 1
                token[self.bufindex] = 0
            else:
                try:
                    lock.release()
                finally: pass
                continue
            print("####Relay#### " + str(self.bufindex))
            for i in range(relays+1):               # (relays+1) because encoder also produces packets
                #sqrt((self.x - adr[i][0])**2 + (self.y - adr[i][1]))**2)
                if np.random.randint(100) >= (self.dist(adr[i][0], adr[i][1])) * 5 and not adr[i] == (self.x, self.y) and not buf[i] == 0:
#                if np.random.randint(100) >= (sqrt((self.x - adr[i][0])**2 + (self.y - adr[i][1])**2)) * 5 and not adr[i] == (self.x, self.y):
                    recoder.decode(buf[i])
                    buf[self.bufindex] = recoder.recode()
                    #print("Decoder Rank : " + str(decoder.rank()))
            try:
                lock.release()
            finally: pass
            time.sleep(sleep_time)              # DELAY INTRODUCED to synchronise Encoding and decoding.

    @threaded
    def sink(self):
        start = time.time()
        global DECODED
        global time_taken
        global decoded_packets
        global sync_nodes
        global lock
        # print(".........Decoding..")

        decoder_factory = kodo.FullVectorDecoderFactoryBinary(self.symbols, self.symbol_size)
        decoder = decoder_factory.build()


        while not decoder.is_complete():
            lock.acquire()
            if token[self.bufindex] == 1 :
                sync_nodes += 1
                token[self.bufindex] = 0
                #print("###DECODER ###")
            else:
                try:
                    lock.release()
                finally: pass
                continue
            for i in range(relays):
                #print("##DECODER##")
                #sqrt((self.x - adr[i][0])**2 + (self.y - adr[i][1]))**2)
                if np.random.randint(100) >= (self.dist(adr[i][0], adr[i][1])) * 5 and not adr[i] == (self.x, self.y) and not buf[i] == 0:
#                if np.random.randint(100) >= (sqrt((self.x - adr[i][0])**2 + (self.y - adr[i][1])**2)) * 5 and not adr[i] == (self.x, self.y):
                    decoder.decode(buf[i])
                    decoded_packets += 1
                    print("Decoder Rank : " + str(decoder.rank()))
            try:
                lock.release()
            finally: pass
            time.sleep(sleep_time)              # DELAY INTRODUCED to synchronise Encoding and decoding.

        if decoder.is_complete():
            DECODED = True
            #print("DECODED")
            time_taken = time.time() - start


"""------- Average Statistics (Text report) --------"""

avg_time_taken = 0
avg_encoded_packets = 0
avg_decoded_packets = 0

iterations = 100

for i in range(iterations):
    initialize()
    src = Node(0, 0, 0)
    relay = Node(0, 21, 1)
    snk = Node(0, 0.00000001, 2)

    src.source("")
    #delay()
    relay.relay()
    #delay()
    snk.sink()
    while not DECODED: pass
    print("==================------------------------- Encoded Pkts : " + str(encoded_packets))
    avg_time_taken += time_taken
    avg_encoded_packets += encoded_packets
    avg_decoded_packets += decoded_packets


delay()
print("\nAverage of " + str(iterations) + " iterations")
print("Time Taken    : " + str(avg_time_taken/iterations))
print("Min req packets : " + str(src.symbols))
print("Encoded Pkts : " + str(avg_encoded_packets/iterations))
print("Decoded Pkts : " + str(avg_decoded_packets/iterations))