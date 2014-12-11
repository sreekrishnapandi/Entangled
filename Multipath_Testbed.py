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

relays = 3
sleep_time = 0.00001


DECODED = False
buf = [0 for _ in range(20)]
adr = [(1000, 1000) for _ in range(20)]


# def dist(self, x, y):
#     print(sqrt((self.x - x)**2 + (self.y - y)**2))
#     return sqrt((self.x - x)**2 + (self.y - y)**2)


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

    def dist(self, x, y):
        # print(x)
        # print(y)
        # print(self.x)
        # print(self.y)
        distance = sqrt((self.x - x)**2 + (self.y - y)**2)
        print("Distance = " + str(distance))
        return distance

    @threaded
    def source(self, FILE):
        # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # s.bind(('', 8500))


        symbol_size = 128
        symbols = 60

        encoder_factory = kodo.FullVectorEncoderFactoryBinary(symbols, symbol_size)
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
            print("Encoding...")
            buf[self.bufindex] = encoder.encode()
            time.sleep(sleep_time)                    # DELAY INTRODUCED to synchronise Encoding and decoding.

    @threaded
    def relay(self):
        global DECODED
        # print(".........Decoding..")
        symbol_size = 128
        symbols = 60

        decoder_factory = kodo.FullVectorDecoderFactoryBinary(symbols, symbol_size)
        recoder = decoder_factory.build()

        print(adr[1])

        while not DECODED:
            print("####Relay#### " + str(self.bufindex))
            for i in range(relays-1):
                #sqrt((self.x - adr[i][0])**2 + (self.y - adr[i][1]))**2)
                if np.random.randint(100) >= (self.dist(adr[i][0], adr[i][1])) * 5 and not adr[i] == (self.x, self.y):
#                if np.random.randint(100) >= (sqrt((self.x - adr[i][0])**2 + (self.y - adr[i][1])**2)) * 5 and not adr[i] == (self.x, self.y):
                    recoder.decode(buf[i])
                    buf[self.bufindex] = recoder.recode()
                    #print("Decoder Rank : " + str(decoder.rank()))
            time.sleep(sleep_time)              # DELAY INTRODUCED to synchronise Encoding and decoding.


    @threaded
    def sink(self):
        global DECODED
        # print(".........Decoding..")
        symbol_size = 128
        symbols = 60

        decoder_factory = kodo.FullVectorDecoderFactoryBinary(symbols, symbol_size)
        decoder = decoder_factory.build()

        print(adr[1])

        while not decoder.is_complete():
            for i in range(relays):
                print("##DECODER##")
                #sqrt((self.x - adr[i][0])**2 + (self.y - adr[i][1]))**2)
                if np.random.randint(100) >= (self.dist(adr[i][0], adr[i][1])) * 5 and not adr[i] == (self.x, self.y):
#                if np.random.randint(100) >= (sqrt((self.x - adr[i][0])**2 + (self.y - adr[i][1])**2)) * 5 and not adr[i] == (self.x, self.y):
                    decoder.decode(buf[i])
                    print("Decoder Rank : " + str(decoder.rank()))
            time.sleep(sleep_time)              # DELAY INTRODUCED to synchronise Encoding and decoding.

        if decoder.is_complete():
            DECODED = True
            print("DECODED")


src = Node(0, 0, 0)
relay = Node(0, 2, 1)
snk = Node(0, 5, 2)


src.source("")
time.sleep(0.001)
relay.relay()
time.sleep(0.001)
snk.sink()
