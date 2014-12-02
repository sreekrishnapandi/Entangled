__author__ = 'Krish'

import os
import kodo
import time
#import hashlib
import numpy as np
import matplotlib.pyplot as plt


def multipath_switch_recoding(FILE, recode, link1, link2, link3, link4):

    start = time.time()

    con1_pkt_loss_rate = link1
    con2_pkt_loss_rate = link2
    con3_pkt_loss_rate = link3
    con4_pkt_loss_rate = link4

    buf1 = buf2 = buf3 = buf4 = ''

    try:
        fsize = os.path.getsize(FILE)
    except os.error:
        print("ERROR : File Not found")

    f = open(FILE, 'rb')

    symbol_size = 128
    symbols = 60

    encoder_factory = kodo.full_rlnc_encoder_factory_binary(symbols, symbol_size)

    decoder_factory = kodo.full_rlnc_decoder_factory_binary(symbols, symbol_size)

    generations = (fsize/(symbol_size * symbols)) + 1
    gensize = symbol_size * symbols
    blksize = symbol_size * symbols * generations

    print "File Size : " + str(fsize)
    #print"Bulk Size : " + str(blksize)
    #print "No of Symbols  : " + str(symbols)
    print "Generations : " + str(generations)

    """Cos encoder must be full for correct functionong. BAD"""
    bulkfile = '*' * (blksize - fsize) + f.read()

    i = 0
    sentPackets = 0
    d_out = ""

    for gen in range(generations):

        encoder = encoder_factory.build()
        recoder1 = decoder_factory.build()
        recoder2 = decoder_factory.build()
        decoder = decoder_factory.build()

        symb = bulkfile[i:i+gensize]
        encoder.set_symbols(symb)
        i += gensize

        """
        To Initialize the buffers.. cos decoder throws error if it tries to decode empty buf
        """
        buf3 = encoder.encode()
        buf4 = encoder.encode()

        while not decoder.is_complete():
            buf1 = encoder.encode()
            #buf2 = encoder.encode()        # IF 2 different pkts sent in multiple paths
            buf2 = buf1                     # IF SAME PKT SENT IN BOTH PATHS
            sentPackets +=2

            if np.random.randint(100) > con1_pkt_loss_rate:
                if recode == 0:
                    buf3 = buf1
                else:
                    recoder1.decode(buf1)
                    buf3 = recoder1.recode()

            if np.random.randint(100) > con3_pkt_loss_rate:
                decoder.decode(buf3)

            if np.random.randint(100) > con2_pkt_loss_rate:
                if recode == 0:
                    buf4 = buf2
                else:
                    recoder2.decode(buf2)
                    buf4 = recoder2.recode()

            if np.random.randint(100) > con4_pkt_loss_rate:
                decoder.decode(buf4)

            #print("rank: {}/{}".format(decoder.rank(), decoder.symbols()))

        d_out += (decoder.copy_symbols())

        #print("Sent Generation : " + str(gen))
        rx = ''



    f2 = open('/Users/Krish/Office/FILES/RX_randomBinary_10MB.bin', 'wb')
    i = 0
    while d_out[i] == '*': i += 1
    f2.write(d_out[i:])

    if recode:
        print "\nWITH RECODING"
    else:
        print "\nWITHOUT RECODING"


    if d_out == bulkfile:
        print("Sent Successfully ")

    min_req_pkts = blksize/symbol_size
    pkt_overhead = sentPackets*1.0/min_req_pkts
    time_taken = time.time() - start
    redundancy = (sentPackets - min_req_pkts)*1.0/sentPackets

    print "Time to Transfer    = " + str(time_taken) + " seconds"
    print("Total Sent Packets  = " + str(sentPackets))
    print("Minimum Req Packets = " + str(min_req_pkts))
    print("Overhead            = " + str(pkt_overhead))
    print("Redundancy          = " + str(redundancy))

    report = {'time': time_taken, 'sent_pkts': sentPackets, 'min_pkts': min_req_pkts,
              'overhead': pkt_overhead, 'redundancy': redundancy}

    return time_taken, sentPackets, min_req_pkts, pkt_overhead, redundancy, link1, link3

FILE = '/Users/Krish/Office/FILES/randomBinary_10MB.bin'

#multipath_switch_recoding(FILE, 1, 10, 10, 20, 20)

report1 = []
report2 = []
report3 = []
report4 = []
index = []

for i in range(0, 10):
    report1.append(multipath_switch_recoding(FILE, 0, i, i, 20, 20))
    report2.append(multipath_switch_recoding(FILE, 1, i, i, 20, 20))
    report3.append(multipath_switch_recoding(FILE, 0, 20, 20, i, i))
    report4.append(multipath_switch_recoding(FILE, 1, 20, 20, i, i))

    index.append(i)

R1 = np.array(report1)
R2 = np.array(report2)
R3 = np.array(report3)
R4 = np.array(report4)


plt.figure(1)
plt.title("Sweep Loss rate of channel 1 and 2")

plt.subplot(221)
plt.plot(R1[:, 5], R1[:, 0], linestyle='--', marker='o', color='b', label='Without Recoding')
plt.plot(R2[:, 5], R2[:, 0], linestyle='--', marker='o', color='r', label='With Recoding')
plt.ylabel("Time Taken")
plt.xlabel("Packet Loss Rate in channel 1,2")
plt.legend()

plt.subplot(222)
plt.plot(R1[:, 5], R1[:, 1], linestyle='--', marker='o', color='b', label='Without Recoding')
plt.plot(R2[:, 5], R2[:, 1], linestyle='--', marker='o', color='r', label='With Recoding')
plt.ylabel("Sent Packets")
plt.xlabel("Packet Loss Rate in channel 1,2")
plt.legend()

plt.subplot(223)
plt.plot(R1[:, 5], R1[:, 3], linestyle='--', marker='o', color='b', label='Without Recoding')
plt.plot(R2[:, 5], R2[:, 3], linestyle='--', marker='o', color='r', label='With Recoding')
plt.ylabel("Data Overhead")
plt.xlabel("Packet Loss Rate in channel 1,2")
plt.legend()

plt.subplot(224)
plt.plot(R1[:, 5], R1[:, 4], linestyle='--', marker='o', color='b', label='Without Recoding')
plt.plot(R2[:, 5], R2[:, 4], linestyle='--', marker='o', color='r', label='With Recoding')
plt.ylabel("Redundancy")
plt.xlabel("Packet Loss Rate in channel 1,2")
plt.legend()

#plt.show()
ax = plt.gca()
ax.ticklabel_format(useOffset=False)


plt.figure(2)
plt.title("Sweep Loss rate of channel 3 and 4")

plt.subplot(221)
plt.plot(R3[:, 6], R1[:, 0], linestyle='--', marker='o', color='b', label='Without Recoding')
plt.plot(R4[:, 6], R2[:, 0], linestyle='--', marker='o', color='r', label='With Recoding')
plt.ylabel("Time Taken")
plt.xlabel("Packet Loss Rate in channel 3,4")
plt.legend()

plt.subplot(222)
plt.plot(R3[:, 6], R1[:, 1], linestyle='--', marker='o', color='b', label='Without Recoding')
plt.plot(R4[:, 6], R2[:, 1], linestyle='--', marker='o', color='r', label='With Recoding')
plt.ylabel("Sent Packets")
plt.xlabel("Packet Loss Rate in channel 3,4")
plt.legend()

plt.subplot(223)
plt.plot(R3[:, 6], R1[:, 3], linestyle='--', marker='o', color='b', label='Without Recoding')
plt.plot(R4[:, 6], R2[:, 3], linestyle='--', marker='o', color='r', label='With Recoding')
plt.ylabel("Data Overhead")
plt.xlabel("Packet Loss Rate in channel 3,4")
plt.legend()

plt.subplot(224)
plt.plot(R3[:, 6], R1[:, 4], linestyle='--', marker='o', color='b', label='Without Recoding')
plt.plot(R4[:, 6], R2[:, 4], linestyle='--', marker='o', color='r', label='With Recoding')
plt.ylabel("Redundancy")
plt.xlabel("Packet Loss Rate in channel 3,4")
plt.legend()

plt.show()
ax = plt.gca()
ax.ticklabel_format(useOffset=False)


