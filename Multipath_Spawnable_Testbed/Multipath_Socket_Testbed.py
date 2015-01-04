__author__ = 'Krish'

import os
import kodo
import numpy as np
from math import sqrt
import threading
import time
import socket
from matplotlib import pyplot as plt
from prettytable import PrettyTable


def threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper


def initialize():
    global DECODED
    global adr
    global relays
    global time_taken
    global encoded_packets
    global decoded_packets
    global lin_dep_pkts
    global relayed_pkts
    global lock
    global free_socket
    global start_socket
    global nxt_bufIndex
    global RECODE

    DECODED = False
    adr = [(1000, 1000) for _ in range(20)]
    time_taken = 0
    encoded_packets = 0
    decoded_packets = 0
    lin_dep_pkts = 0
    relayed_pkts = 0
    lock = threading.Lock()
    free_socket = 3000
    start_socket = 3000
    nxt_bufIndex = 0
    RECODE = True


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
            #print("Encoded Packets : " + str(encoded_packets))

            #delay()
            #time.sleep(sleep_time)                    # DELAY INTRODUCED to synchronise Encoding and decoding.
        s.close()


    @threaded
    def relay(self):
        global DECODED
        global RECODE
        global relayed_pkts

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', self.sockID))
        s.settimeout(0.0001)

        # print(".........Decoding..")

        decoder_factory = kodo.FullVectorDecoderFactoryBinary(self.symbols, self.symbol_size)
        recoder = decoder_factory.build()

        #print(adr[1])

        if RECODE:
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
                        #print("Recoder Rank : " + str(recoder.rank()))
                relayed_pkts += 1

                 #time.sleep(sleep_time)                    # DELAY INTRODUCED to synchronise Encoding and decoding.
        else:
            while not DECODED:
                # print("####Relay#### " + str(self.bufindex))
                try:
                    rcv = s.recvfrom(180)[0]
                    pkt = rcv
                    for i in range(relays+2):               # (relays+1) because encoder also produces packets
                        if np.random.randint(100) >= (self.dist(adr[i][0], adr[i][1])) * 5 and not adr[i] == (self.x, self.y):
                            s.sendto(pkt, ('', start_socket + i))
                            #print("Recoder Rank : " + str(recoder.rank()))
                    relayed_pkts += 1

                except socket.timeout:
                    pass

                #delay()
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
                decoded_packets += 1
                #print("Decoder Rank : " + str(decoder.rank()))
            except socket.timeout:
                pass

            # delay()
            #time.sleep(sleep_time)              # DELAY INTRODUCED to synchronise Encoding and decoding.
        s.close()

        if decoder.is_complete():
            DECODED = True
            #print("DECODED")
            time_taken = time.time() - start


"""------- Average Statistics (Text report) --------"""


def avg_statistics():
    avg_time_taken = 0
    avg_encoded_packets = 0
    avg_decoded_packets = 0
    avg_relayed_packets = 0
    global RECODE
    global relays

    iterations = 200

    for i in range(iterations):
        initialize()

        RECODE = True
        relays = 1

        src = Node(0, 0)
        snk = Node(0, 19)
        relay1 = Node(0, 16)
        #relay2 = Node(7, 10)
        #relay3 = Node(5, 15)
        #relay4 = Node(5, 5)

        src.source("")
        snk.sink()
        relay1.relay()
        #relay2.relay()
        #relay3.relay()
        #relay4.relay()

        while not DECODED: pass
        #print("==================------------------------- Encoded Pkts : " + str(encoded_packets))
        avg_time_taken += time_taken
        avg_encoded_packets += encoded_packets
        avg_decoded_packets += decoded_packets
        avg_relayed_packets += relayed_pkts

        delay()                     # To wait for OS to close the sockets , so that its available for next iteration


    delay()
    print("Source  : (" + str(src.x) + ", " + str(src.y) + ")")
    print("Sink    : (" + str(snk.x) + ", " + str(snk.y) + ")")
    print("Relays  : " + str(relays))

    # print("Relay 1 : (" + str(relay1.x) + ", " + str(relay1.y) + ")")
    # print("Relay 2 : (" + str(relay2.x) + ", " + str(relay2.y) + ")")
    # print("Relay 3 : (" + str(relay3.x) + ", " + str(relay3.y) + ")")

    print("\nAverage of " + str(iterations) + " iterations")
    print("Time Taken    : " + str(avg_time_taken/iterations))
    print("Min req packets : " + str(src.symbols))
    print("Encoded Pkts : " + str(avg_encoded_packets/iterations))
    print("Relayed Pkts : " + str(avg_relayed_packets/iterations))
    print("Decoded Pkts : " + str(avg_decoded_packets/iterations))


def OneRelay(x,y):
    """
    Give Avg statistics on system with one active relay.
    :param x: X coordinate
    :param y: Y coordinate
    :return: avg_time_taken, avg_encoded_packets, avg_relayed_packets, avg_decoded_packets
    """
    avg_time_taken = 0
    avg_encoded_packets = 0
    avg_decoded_packets = 0
    avg_relayed_packets = 0
    global RECODE
    global relays

    iterations = 200

    for i in range(iterations):
        initialize()

        RECODE = True
        relays = 1

        src = Node(0, 0)
        snk = Node(0, 19)
        relay1 = Node(x, y)
        #relay2 = Node(7, 10)
        #relay3 = Node(5, 15)
        #relay4 = Node(5, 5)

        src.source("")
        snk.sink()
        relay1.relay()
        #relay2.relay()
        #relay3.relay()
        #relay4.relay()

        while not DECODED: pass
        #print("==================------------------------- Encoded Pkts : " + str(encoded_packets))
        avg_time_taken += time_taken
        avg_encoded_packets += encoded_packets
        avg_decoded_packets += decoded_packets
        avg_relayed_packets += relayed_pkts

        delay()                     # To wait for OS to close the sockets , so that its available for next iteration

    delay()

    # print("Source  : (" + str(src.x) + ", " + str(src.y) + ")")
    # print("Sink    : (" + str(snk.x) + ", " + str(snk.y) + ")")
    # print("Relays  : " + str(relays))
    #
    # # print("Relay 1 : (" + str(relay1.x) + ", " + str(relay1.y) + ")")
    # # print("Relay 2 : (" + str(relay2.x) + ", " + str(relay2.y) + ")")
    # # print("Relay 3 : (" + str(relay3.x) + ", " + str(relay3.y) + ")")
    #
    # print("\nAverage of " + str(iterations) + " iterations")
    # print("Time Taken    : " + str(avg_time_taken/iterations))
    # print("Min req packets : " + str(src.symbols))
    # print("Encoded Pkts : " + str(avg_encoded_packets/iterations))
    # print("Relayed Pkts : " + str(avg_relayed_packets/iterations))
    # print("Decoded Pkts : " + str(avg_decoded_packets/iterations))

    return avg_time_taken/iterations, avg_encoded_packets/iterations, avg_relayed_packets/iterations, \
           avg_decoded_packets/iterations


"""  ###########--- Sweep One Relay from Source to destination and plot the Statistics ---#########  """
list_time = []
list_encoded_packets = []
list_relyed_packets = []
list_decoded_packets = []
index = []

for i in range(1, 25):
    timetaken, encoded_packets, relyed_packets, decoded_packets = OneRelay(1, i)
    list_time.append(timetaken)
    list_encoded_packets.append(encoded_packets)
    list_decoded_packets.append(decoded_packets)
    list_relyed_packets.append(relyed_packets)
    index.append(i)

plt.figure(1)
plt.subplot(221)
plt.plot(index, list_time, linestyle='--', marker='o', color='b', label='Time')
plt.ylabel("Time Taken")


plt.subplot(222)
plt.plot(index, list_encoded_packets, linestyle='--', marker='o', color='r', label='encoded')
plt.ylabel("Encoded Packets")

plt.subplot(223)
plt.plot(index, list_decoded_packets, linestyle='--', marker='o', color='g', label='decoded')
plt.ylabel("Decoded Packets")

plt.subplot(224)
plt.plot(index, list_relyed_packets, linestyle='--', marker='o', color='b', label='relayed')
plt.ylabel("Relayed Packets")
plt.show()

x = PrettyTable()
x.add_column('Index', index)
x.add_column('Time', list_time)
x.add_column('Encoded Pkts', list_encoded_packets)
x.add_column('Decoded Pkts', list_decoded_packets)
x.add_column('Relayed Pkts', list_relyed_packets)
print x

data = x.get_string()

with open('/Users/Krish/Office/FILES/Multipath-OneRelaySweep/Result.txt', 'wb') as f:
    f.write(data)


#avg_statistics()





