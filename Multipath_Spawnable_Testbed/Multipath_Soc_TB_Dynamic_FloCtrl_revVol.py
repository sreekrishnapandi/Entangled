__author__ = 'Krish'

import os
import kodo
import numpy as np
from math import sqrt
import threading
import time
import socket
from operator import mul

from matplotlib import pyplot as plt
from prettytable import PrettyTable


def threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper


def chunk_transpose(l, n):
    """ Yield successive n-sized chunks from l.
    """
    x = []
    for i in xrange(0, len(l), n):
        x.append(l[i:i+n])
        y = zip(*x)
    return y


def set_States(prev_rates):
    Node.R_relays = prev_rates
    Node.first_run = False


def initialize(cumil_ind_rel_pkt):
    global adr
    global sock_list
    global lin_dep_pkts
    global lock
    global free_socket
    global start_socket
    global nxt_bufIndex
    global RECODE

    Node.DECODED = False
    adr = [(1000, 1000) for _ in range(100)]
    Node.time_taken = 0
    Node.encoded_packets = 0
    Node.decoded_packets = 0
    lin_dep_pkts = 0
    Node.relayed_pkts = 0
    lock = threading.Lock()
    free_socket = 3000
    start_socket = 3000
    nxt_bufIndex = 0
    RECODE = True
    Node.Dec_LD_profile = [0 for _ in range(105)]
    Node.indiv_relayed_pkts = [0 for _ in range(Node.relayz+2)]
    Node.R_relays = [[0 for _ in range(Node.relayz+2)] for __ in range(Node.relayz+2)]
    Node.list_tx_prob = [0 for _ in range(Node.relayz+2)]
    #Node.history_innov_pkts = [[0 for _ in range(Node.relayz+2)] for __ in range(Node.relayz+2)]
    Node.cumilative_indiv_relayed_pkts = cumil_ind_rel_pkt


def delay(): time.sleep(0.01)


#def txdelay(): time.sleep(0.005)
def txdelay(): time.sleep(0.0005)


class Node:
    relayz = 0
    DECODED = False
    time_taken = 0
    encoded_packets = 0
    decoded_packets = 0
    relayed_pkts = 0
    indiv_relayed_pkts = [0 for _ in range(relayz+2)]
    RelayOnlyWhenRecieved = False
    Dec_LD_profile = [0 for _ in range(65)]
    staticPause = 0
    RECODE = True
    sock_list = [0 for _ in range(50)]
    R_dec = [0 for _ in range(relayz+2)]
    R_relays = [[0 for _ in range(relayz+2)] for __ in range(relayz+2)]
    list_tx_prob = [0 for _ in range(relayz+2)]
    first_run = True
    history_innov_pkts = []
    cumilative_indiv_relayed_pkts = []

    def __init__(self, x, y):
        global free_socket
        global nxt_bufIndex
        lock.acquire()
        self.sockID = free_socket
        free_socket += 1
        self.bufindex = nxt_bufIndex
        nxt_bufIndex += 1
        lock.release()
        self.txprob = 100

        self.contribution = [0 for _ in range(Node.relayz+2)]        # [encoder, decoder, relay1, relay2, ...]
        self.innov_contribution = [0 for _ in range(Node.relayz+2)]  # [encoder, decoder, relay1, relay2, ...]
        self.redundant_pkts = [0 for _ in range(Node.relayz+2)]      # [encoder, decoder, relay1, relay2, ...]
        self.pause_list = [0 for _ in range(Node.relayz+2)]
        self.doneList = [0 for _ in range(Node.relayz+2)]
        self.volume = [0 for _ in range(Node.relayz+2)]
        self.iq = [0 for _ in range(Node.relayz+2)]

        self.cumilative_innov_contrib = Node.history_innov_pkts[self.bufindex]
        #print "History :", Node.history_innov_pkts

        self.x = x
        self.y = y
        adr[self.bufindex] = (x, y)
        Node.sock_list[self.bufindex] = self.sockID

        self.symbol_size = 64
        self.symbols = 100

        # self.symbol_size = 128
        # self.symbols = 60



    def dist(self, x, y):
        # print(x)
        # print(y)
        # print(self.x)
        # print(self.y)
        distance = sqrt((self.x - x)**2 + (self.y - y)**2)
        #print("Distance = " + str(distance))
        return distance

    def pause(self, nodeID):
        self.pause_list[nodeID-3000] = Node.staticPause

    def shutup(self, s, nodeID):
        s.sendto("SHUTUP", ('', nodeID))

    def imDone(self, s, nodeID):
        s.sendto("IMDONE", ('', nodeID))

    def isPaused(self):
        prd = 0
        for i in range(1, Node.relayz+2):
            if not i == self.bufindex:
                prd += self.pause_list[i]
        return prd

    def isDone(self):
        done = 1
        for i in range(2, Node.relayz+2):
            done *= self.doneList[i]
            #print(self.doneList)
        return done

    @threaded
    def source(self, FILE):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', self.sockID))
        s.settimeout(0.0001)

        encoder_factory = kodo.FullVectorEncoderFactoryBinary8(self.symbols, self.symbol_size)
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
        while not Node.DECODED:
            try:
                rcv = s.recvfrom(180)
                # if rcv[0] == "SHUTUP":
                #     self.pause(rcv[1][1])
                if rcv[0] == "IMDONE":
                    self.doneList[rcv[1][1]-3000] = 1
                    if self.isDone():
                        break
            except socket.timeout:
                pass

            #print("---Encoding---")
            pkt = encoder.encode()
            #print(pkt)
            txdelay()

            """ Rank - evaluate """
            decoder = 1
            rate_pri = Node.R_relays[decoder][self.bufindex]
            rate_sec = 0

            # print Node.R_relays
            # print Node.list_tx_prob

            for i in range(Node.relayz+2):
                rate_sec += Node.R_relays[decoder][i] * Node.R_relays[i][self.bufindex]
            RATE = (rate_pri + rate_sec) * 100
            #print(RATE)

            if (Node.encoded_packets > 5) or not Node.first_run:
                self.txprob = RATE
                Node.list_tx_prob[self.bufindex] = round(RATE, 2)

            """------------------"""

            if np.random.randint(100) <= self.txprob:
                for i in range(Node.relayz+2):
                    if np.random.randint(100) >= (self.dist(adr[i][0], adr[i][1])) * 5 and not adr[i] == (self.x, self.y):
                        if not self.pause_list[i] > 0:      # To pause

                                s.sendto(pkt, ('', start_socket + i))
                        else:
                            self.pause_list[i] -= 1
                if not self.isPaused():
                    Node.encoded_packets += 1
                    Node.cumilative_indiv_relayed_pkts[self.bufindex] += 1
                    Node.indiv_relayed_pkts[self.bufindex] += 1
            #print("Encoded Packets : " + str(encoded_packets))

            #delay()
            #time.sleep(sleep_time)                    # DELAY INTRODUCED to synchronise Encoding and decoding.

        #print("Encoder Stopped")
        s.close()


    @threaded
    def relay(self):
        prev_rank = 0
        rank = 0

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', self.sockID))
        s.settimeout(0.0001)

        # print(".........Decoding..")

        decoder_factory = kodo.FullVectorDecoderFactoryBinary8(self.symbols, self.symbol_size)
        recoder = decoder_factory.build()

        #print(adr[1])
        if Node.RECODE:

            while not Node.DECODED:
                #print(self.pause_list)
                #print("####Relay#### " + str(self.bufindex))
                # if recoder.is_complete():
                #     print("IM DONEEEE")
                try:
                    rcv = s.recvfrom(180)
                    if rcv[0] == "SHUTUP":
                        self.pause(rcv[1][1])
                        #print(self.pause_list)
                        continue

                    sender = (rcv[1][1])-3000

                    self.contribution[sender] += 1
                    recoder.decode(rcv[0])
                    rank = recoder.rank()

                    if prev_rank < rank:
                        self.innov_contribution[sender] += 1
                        self.cumilative_innov_contrib[sender] += 1
                    else:
                        self.redundant_pkts[sender] += 1
                        #lin_dep_pkts += 1
                        i = sender

                        if np.random.randint(100) >= (self.dist(adr[i][0], adr[i][1])) * 5 and not adr[i] == (self.x, self.y):
                            self.shutup(s, rcv[1][1])

                        """IMPORTANT FUNCTION - SAYS IM DONE TO STOP ENCODER"""
                        # if (rcv[1][1]) == 3000 and recoder.is_complete():
                        #     self.imDone(s, rcv[1][1])
                    #print(Node.cumilative_indiv_relayed_pkts)
                    self.volume[sender] = self.contribution[sender] * 1.0 / Node.indiv_relayed_pkts[sender]
                    self.iq[sender] = self.innov_contribution[sender] *1.0 / self.contribution[sender]

                    Node.R_relays[self.bufindex][sender] = self.iq[sender]

                except socket.timeout:
                    pass
                except ZeroDivisionError:
                    pass

                """ Rank - evaluate """
                decoder = 1

                rate_pri = Node.R_relays[decoder][self.bufindex]
                rate_sec = 0
                for i in range(Node.relayz+2):
                    rate_sec += Node.R_relays[decoder][i] * Node.R_relays[i][self.bufindex]
                RATE = (rate_pri + rate_sec) * 100

                if (recoder.rank() > 5) or not Node.first_run:
                    self.txprob = RATE
                    Node.list_tx_prob[self.bufindex] = round(RATE, 2)

                """------------------"""

                if prev_rank < rank or recoder.is_complete():
                    pkt = recoder.recode()
                    #print("recoding.......")

                    txdelay()
                    if np.random.randint(100) <= self.txprob and recoder.rank() > 0:
                        for i in range(Node.relayz+2):               # (Node.relayz+1) because encoder also produces packets
                            if np.random.randint(100) >= (self.dist(adr[i][0], adr[i][1])) * 5 and not i == self.bufindex:
                                if not self.pause_list[i] > 0:      # To pause
                                    if not self.isPaused():
                                        s.sendto(pkt, ('', start_socket + i))
                                    #Node.relayed_pkts += 1
                                else:
                                    self.pause_list[i] -= 1
                                    #print(self.pause_list)

                                #print("Recoder Rank : " + str(recoder.rank()))
                        if not self.isPaused():
                            #print("BAAAAAA")
                            Node.relayed_pkts += 1
                            Node.indiv_relayed_pkts[self.bufindex] += 1
                            Node.cumilative_indiv_relayed_pkts[self.bufindex] += 1
                        # else:
                        #     print("BAAAAAA")

                prev_rank = rank

        if not Node.RECODE:
            while not Node.DECODED:
                # print("####Relay#### " + str(self.bufindex))
                try:
                    rcv = s.recvfrom(180)
                    self.contribution[(rcv[1][1])-3000] += 1
                    pkt = rcv[0]
                    txdelay()
                    for i in range(Node.relayz+2):               # (Node.relayz+1) because encoder also produces packets
                        if np.random.randint(100) >= (self.dist(adr[i][0], adr[i][1])) * 5 and not i == self.bufindex:
                            s.sendto(pkt, ('', start_socket + i))
                            #print("Recoder Rank : " + str(recoder.rank()))
                    Node.relayed_pkts += 1

                except socket.timeout:
                    pass

        Node.history_innov_pkts[self.bufindex] = self.cumilative_innov_contrib
        s.close()

    @threaded
    def sink(self):
        start = time.time()
        prev_rank = 0
        rank = 0

        # contribution = [0 for _ in range(Node.relayz+2)]        # [encoder, decoder, relay1, relay2, ...]
        # innov_contribution = [0 for _ in range(Node.relayz+2)]  # [encoder, decoder, relay1, relay2, ...]

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', self.sockID))
        s.settimeout(0.0001)

        # print(".........Decoding..")

        decoder_factory = kodo.FullVectorDecoderFactoryBinary8(self.symbols, self.symbol_size)
        decoder = decoder_factory.build()

        while not decoder.is_complete():
            #print(self.pause_list)
            try:
                rcv = s.recvfrom(180)

                if rcv[0] == "SHUTUP":
                    self.pause(rcv[1][1])
                    continue

                sender = (rcv[1][1])-3000
                # print(contribution)
                # print(innov_contribution)
                # print(sender)
                self.contribution[sender] += 1
                decoder.decode(rcv[0])
                rank = decoder.rank()

                if prev_rank < rank:
                    self.innov_contribution[sender] += 1
                    self.cumilative_innov_contrib[sender] += 1
                    # print Node.R_relays
                    #print Node.list_tx_prob
                else:
                    self.redundant_pkts[sender] += 1
                    #print(self.redundant_pkts)
                    i = sender
                    if np.random.randint(100) >= (self.dist(adr[i][0], adr[i][1])) * 5 and not adr[i] == (self.x, self.y):
                        self.shutup(s, rcv[1][1])
                    Node.Dec_LD_profile[rank] += 1
                    #lin_dep_pkts += 1

                self.volume[sender] = self.contribution[sender] * 1.0 / Node.indiv_relayed_pkts[sender]
                self.iq[sender] = self.innov_contribution[sender] *1.0 / self.contribution[sender]

                prev_rank = rank
                Node.decoded_packets += 1
                #print("Decoder Rank : " + str(decoder.rank()))

                """ Eval - Rate"""
                Node.R_relays[self.bufindex][sender] = self.iq[sender]

                print "Contrib       : ", self.contribution
                print "Innov Contrib : ", self.innov_contribution
                print "indiv rel pkt : ", Node.indiv_relayed_pkts
                print "Rank : ", rank, " Tx_Prob : ", Node.list_tx_prob

            except socket.timeout:
                pass
            except ZeroDivisionError:
                pass
        #delay()
        #time.sleep(sleep_time)              # DELAY INTRODUCED to synchronise Encoding and decoding.

        Node.history_innov_pkts[self.bufindex] = self.cumilative_innov_contrib
        s.close()

        if decoder.is_complete():
            Node.DECODED = True
            #print("DECODED")
            Node.time_taken = time.time() - start
