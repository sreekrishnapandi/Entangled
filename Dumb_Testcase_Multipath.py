__author__ = 'Krish'

import os
import kodo
import time
#import hashlib
import numpy as np
import matplotlib.pyplot as plt


def multipath_switch_recoding(FILE, recode, link1, link2, link3, link4, link5, linkx):

    start = time.time()
    con1_pkt_loss_rate = link1
    con2_pkt_loss_rate = link2
    con3_pkt_loss_rate = link3
    con4_pkt_loss_rate = link4
    con5_pkt_loss_rate = link5
    con6_pkt_loss_rate = linkx

    buf1 = buf2 = buf3 = buf4 = ''

    try:
        fsize = os.path.getsize(FILE)
    except os.error:
        print("ERROR : File Not found")

    f = open(FILE, 'rb')

    symbol_size = 32
    symbols = 60

    encoder_factory = kodo.FullVectorEncoderFactoryBinary(symbols, symbol_size)

    decoder_factory = kodo.FullVectorDecoderFactoryBinary(symbols, symbol_size)

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
    lin_dep_pkts = 0
    relayed_pkts = 0

    for gen in range(generations):

        prev_rank = 0
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
        buf3 = 0
        buf4 = 0

        while not decoder.is_complete():
            buf1 = encoder.encode()
            sentPackets += 1
            #print(str(decoder.rank()) + "    " + str(sentPackets))

            if np.random.randint(100) >= con1_pkt_loss_rate:
                if recode == 0:
                    buf3 = buf1
                    relayed_pkts += 1
                else:
                    recoder1.decode(buf1)
            if np.random.randint(100) >= con5_pkt_loss_rate and not buf4 == 0:
                if recode == 1:
                    recoder1.decode(buf4)
            if recode == 1:
                buf3 = recoder1.recode()
                relayed_pkts +=1

            # if np.random.randint(100) >= con3_pkt_loss_rate and not buf3 == 0:
            #     decoder.decode(buf3)
            #     #print(decoder.rank())
            #     if prev_rank == decoder.rank():
            #         lin_dep_pkts += 1
            #     prev_rank = decoder.rank()


            # if np.random.randint(100) >= con5_pkt_loss_rate and not buf4 == 0:
            #     if recode == 1:
            #         recoder1.decode(buf4)
            #         buf5 = recoder1.recode()


            # if np.random.randint(100) >= con3_pkt_loss_rate and not buf3 == 0:
            #     decoder.decode(buf3)
            #     #print(decoder.rank())
            #     if prev_rank == decoder.rank():
            #         lin_dep_pkts += 1
            #     prev_rank = decoder.rank()

            if np.random.randint(100) > con2_pkt_loss_rate:
                if recode == 0:
                    buf4 = buf1
                    relayed_pkts += 1
                else:
                    recoder2.decode(buf1)
            if np.random.randint(100) >= con5_pkt_loss_rate and not buf3 == 0:
                if recode == 1:
                    recoder2.decode(buf3)

            if recode == 1:
                buf4 = recoder2.recode()
                relayed_pkts += 1


            # if np.random.randint(100) > con4_pkt_loss_rate and not buf4 == 0:
            #     decoder.decode(buf4)
            #     if prev_rank == decoder.rank():
            #         lin_dep_pkts += 1
            #     prev_rank = decoder.rank()

            # if np.random.randint(100) >= con5_pkt_loss_rate and not buf3 == 0:
            #     if recode == 1:
            #         recoder2.decode(buf3)
            # buf4 = recoder2.recode()

            if np.random.randint(100) >= con3_pkt_loss_rate and not buf3 == 0:
                decoder.decode(buf3)
                #print(decoder.rank())
                if prev_rank == decoder.rank():
                    lin_dep_pkts += 1
                prev_rank = decoder.rank()

            if np.random.randint(100) >= con4_pkt_loss_rate and not buf4 == 0:
                decoder.decode(buf4)
                if prev_rank == decoder.rank():
                    lin_dep_pkts += 1
                prev_rank = decoder.rank()

            if np.random.randint(100) >= con6_pkt_loss_rate and not buf1 == 0:
                decoder.decode(buf1)
                if prev_rank == decoder.rank():
                    lin_dep_pkts += 1
                prev_rank = decoder.rank()

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
    print("Lin dependant pkts  = " + str(lin_dep_pkts))
    print("Relayed Packets     = " + str(relayed_pkts))
    print("Channel 1,2 Loss    = " + str(link1))
    print("Channel 3,4 Loss    = " + str(link3))
    print("Recoding            = " + str(recode))

    report = {'time': time_taken, 'sent_pkts': sentPackets, 'min_pkts': min_req_pkts,
              'overhead': pkt_overhead, 'redundancy': redundancy}

    return time_taken, sentPackets, lin_dep_pkts, relayed_pkts, redundancy, link1, link3, link5

#FILE = '/Users/Krish/Office/FILES/randomBinary_10MB.bin'
#FILE = '/Users/Krish/Office/FILES/randomBinary_1Gen_1480x60.bin'
#FILE = '/Users/Krish/Office/FILES/randomBinary_1480x60-1.bin'
#FILE = '/Users/Krish/Office/FILES/randomBinary_1MB.bin'
FILE = '/Users/Krish/Office/FILES/randomBinary_1Gen_120x60.bin'



#multipath_switch_recoding(FILE, 1, 10, 10, 20, 20)

report1 = []
report2 = []
report3 = []
report4 = []
map1 = []
index = []
spmap = [0]

"""simulate 2D matrix of sweeping both channel losses"""
# for i in range(10, 100, 10):
#     spmap.append([])
#     for j in range(10, 100, 10):
#         map1.append(multipath_switch_recoding(FILE, 1, i, j, 100-i, 100-j, 50))
#         spmap[i/10].append(map1[len(map1)-1][1])
# spmap.pop(0)
##################
""""""
# for i in range(10, 100, 10):
#     spmap.append([])
#     for j in range(10, 100, 10):
#         map1.append(multipath_switch_recoding(FILE, 1, i, j, 100-i, 100-j, 50))
#         spmap[i/10].append(map1[len(map1)-1][1])
# spmap.pop(0)

""""""

"""PLOT HEATMAP"""
# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib import cm
# from matplotlib.ticker import LinearLocator, FormatStrFormatter
#
# M1 = np.array(map1)
#
# print(len(spmap))
# print spmap
# print(M1[:, 5])
# print(len(M1[:, 5]))
#
# fig = plt.figure(1)
# plt.xlabel("Loss Rate in Channel 1")
# plt.ylabel("Loss Rate in Channel 3")
# ax = fig.gca(projection='3d')
# X = np.arange(10, 100, 10)
# Y = np.arange(10, 100, 10)
# #Y = Y[::-1]
# X, Y = np.meshgrid(X, Y)
# Z = spmap
# surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
# surf.set_clim(vmin=3500,vmax=11000)
# #ax.set_zlim(min(Z[0]), max(Z[-1]))
# ax.set_zlim(0, 7000)
#
# ax.zaxis.set_major_locator(LinearLocator(10))
# ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
# fig.colorbar(surf, shrink=0.5, aspect=5)
#
#
#
#
#
# plt.show()
#


""""""
# for i in range(0, 20):
#     report1.append(multipath_switch_recoding(FILE, 0, 20, 20, 20, 20, i))
#     report2.append(multipath_switch_recoding(FILE, 1, 20, 20, 20, 20, i))
#     # report3.append(multipath_switch_recoding(FILE, 0, 20, 20, i, i))
#     # report4.append(multipath_switch_recoding(FILE, 1, 20, 20, i, i))
#     index.append(i)

""""""
pak = 0
for _x in range(50):
    _,pa,_,_,_,_,_,_ = multipath_switch_recoding(FILE, 0, 100, 100, 100, 100, 100, 75)
    pak += pa
    print(pak)
avg_pak = pak/50
print("AVERAGE OF 100 runs : SENT PACKETS = " + str(avg_pak))
""""""
R1 = np.array(report1)
R2 = np.array(report2)
# R3 = np.array(report3)
# R4 = np.array(report4)

# plt.figure(1)
# plt.title("Sweep Loss rate of channel 1 and 2")
#
# plt.subplot(221)
# plt.plot(R1[:, 5], R1[:, 0], linestyle='--', marker='o', color='b', label='Without Recoding')
# plt.plot(R2[:, 5], R2[:, 0], linestyle='--', marker='o', color='r', label='With Recoding')
# plt.ylabel("Time Taken")
# plt.xlabel("Packet Loss Rate in channel 1,2")
# plt.legend()
#
# plt.subplot(222)
# plt.plot(R1[:, 5], R1[:, 1], linestyle='--', marker='o', color='b', label='Without Recoding')
# plt.plot(R2[:, 5], R2[:, 1], linestyle='--', marker='o', color='r', label='With Recoding')
# plt.ylabel("Sent Packets")
# plt.xlabel("Packet Loss Rate in channel 1,2")
# plt.legend()
#
# plt.subplot(223)
# plt.plot(R1[:, 5], R1[:, 3], linestyle='--', marker='o', color='b', label='Without Recoding')
# plt.plot(R2[:, 5], R2[:, 3], linestyle='--', marker='o', color='r', label='With Recoding')
# plt.ylabel("Data Overhead")
# plt.xlabel("Packet Loss Rate in channel 1,2")
# plt.legend()
#
# plt.subplot(224)
# plt.plot(R1[:, 5], R1[:, 4], linestyle='--', marker='o', color='b', label='Without Recoding')
# plt.plot(R2[:, 5], R2[:, 4], linestyle='--', marker='o', color='r', label='With Recoding')
# plt.ylabel("Redundancy")
# plt.xlabel("Packet Loss Rate in channel 1,2")
# plt.legend()
#
# #plt.show()
# ax = plt.gca()
# ax.ticklabel_format(useOffset=False)

#
# plt.figure(2)
# plt.title("Sweep Loss rate of channel 3 and 4")
#
# plt.subplot(221)
# plt.plot(R3[:, 6], R1[:, 0], linestyle='--', marker='o', color='b', label='Without Recoding')
# plt.plot(R4[:, 6], R2[:, 0], linestyle='--', marker='o', color='r', label='With Recoding')
# plt.ylabel("Time Taken")
# plt.xlabel("Packet Loss Rate in channel 3,4")
# plt.legend()
#
# plt.subplot(222)
# plt.plot(R3[:, 6], R1[:, 1], linestyle='--', marker='o', color='b', label='Without Recoding')
# plt.plot(R4[:, 6], R2[:, 1], linestyle='--', marker='o', color='r', label='With Recoding')
# plt.ylabel("Sent Packets")
# plt.xlabel("Packet Loss Rate in channel 3,4")
# plt.legend()
#
# plt.subplot(223)
# plt.plot(R3[:, 6], R1[:, 3], linestyle='--', marker='o', color='b', label='Without Recoding')
# plt.plot(R4[:, 6], R2[:, 3], linestyle='--', marker='o', color='r', label='With Recoding')
# plt.ylabel("Data Overhead")
# plt.xlabel("Packet Loss Rate in channel 3,4")
# plt.legend()
#
# plt.subplot(224)
# plt.plot(R3[:, 6], R1[:, 4], linestyle='--', marker='o', color='b', label='Without Recoding')
# plt.plot(R4[:, 6], R2[:, 4], linestyle='--', marker='o', color='r', label='With Recoding')
# plt.ylabel("Redundancy")
# plt.xlabel("Packet Loss Rate in channel 3,4")
# plt.legend()




# plt.figure(1)
# plt.title("Sweep Loss rate of channel 1 and 2")
#
# plt.subplot(221)
# plt.plot(R1[:, 7], R1[:, 0], linestyle='--', marker='o', color='b', label='Without Recoding')
# plt.plot(R2[:, 7], R2[:, 0], linestyle='--', marker='o', color='r', label='With Recoding')
# plt.ylabel("Time Taken")
# plt.xlabel("Packet Loss Rate in channel 1,2")
# plt.legend()
#
# plt.subplot(222)
# plt.plot(R1[:, 7], R1[:, 1], linestyle='--', marker='o', color='b', label='Without Recoding')
# plt.plot(R2[:, 7], R2[:, 1], linestyle='--', marker='o', color='r', label='With Recoding')
# plt.ylabel("Sent Packets")
# plt.xlabel("Packet Loss Rate in channel 1,2")
# plt.legend()
#
# plt.subplot(223)
# plt.plot(R1[:, 7], R1[:, 3], linestyle='--', marker='o', color='b', label='Without Recoding')
# plt.plot(R2[:, 7], R2[:, 3], linestyle='--', marker='o', color='r', label='With Recoding')
# plt.ylabel("Data Overhead")
# plt.xlabel("Packet Loss Rate in channel 1,2")
# plt.legend()
#
# plt.subplot(224)
# plt.plot(R1[:, 7], R1[:, 4], linestyle='--', marker='o', color='b', label='Without Recoding')
# plt.plot(R2[:, 7], R2[:, 4], linestyle='--', marker='o', color='r', label='With Recoding')
# plt.ylabel("Redundancy")
# plt.xlabel("Packet Loss Rate in channel 1,2")
# plt.legend()
#
# #plt.show()
# ax = plt.gca()
# ax.ticklabel_format(useOffset=False)
#
#
#
# plt.show()
# ax = plt.gca()
# ax.ticklabel_format(useOffset=False)


