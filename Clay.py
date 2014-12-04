__author__ = 'Krish'

#
# import random
# x = random.randint(0,100)
# print(x)

##########################
import os

with open('/Users/Krish/Office/FILES/randomBinary_1480x60-1.bin', 'wb') as fout:
    #fout.write(os.urandom(1024*1024*1))
    fout.write(os.urandom((1480*60)-1))

#
# import hashlib
# def getHash(file):
#     hasher = hashlib.md5()
#     with open('/Users/Krish/Office/FILES/randomBinary.bin', 'rb') as afile:
#         buf = afile.read()
#         hasher.update(buf)
#     return (hasher.hexdigest())

import numpy as np

#
# import kodo
#
# symbols = 60
# symbol_size = 1480
#
# encoder_factory = kodo.full_rlnc_encoder_factory_binary(symbols, symbol_size)
# encoder = encoder_factory.build()
#
# decoder_factory = kodo.full_rlnc_decoder_factory_binary(symbols, symbol_size)
# decoder = decoder_factory.build()
# recoder1 = decoder_factory.build()
# recoder2 = decoder_factory.build()
#
#
# FILE = '/Users/Krish/Office/FILES/randomBinary_1Gen_1480*60-1.bin'
#
# f = open(FILE, 'rb')
#
# data_in = f.read()
# encoder.set_symbols(data_in)
#
# sentpkts = 0
#
#
#
#
# """
# #
# """
# # packet_number = 0
# # while not decoder.is_complete():
# #     packet = encoder.encode()
# #     sentpkts += 1
# #
# #     decoder.decode(packet)
# #     packet_number += 1
# #     print("rank: {}/{}".format(decoder.rank(), decoder.symbols()))
# #
# # print("Sent Packets : " + str(sentpkts))
# #
# # data_out = decoder.copy_symbols()
#
#
#
# """
# #
# """
#
# # sentPackets = 0
# #
# # con1_pkt_loss_rate = 40
# # con3_pkt_loss_rate = 0
# # recode = 0
# # lin_dep_pkts = 0
# # prev_rank = 0
# #
# # buf3 = 0
# # buf4 = 0
# #
# # print("Processing")
# # packet_number = 0
# # while not decoder.is_complete():
# #     buf1 = encoder.encode()
# #     sentPackets +=1
# #     #print(str(decoder.rank()) + "    " + str(sentPackets))
# #
# #     if np.random.randint(100) >= con1_pkt_loss_rate:
# #         if recode == 0:
# #             buf3 = buf1
# #         else:
# #             recoder1.decode(buf1)
# #             buf3 = recoder1.recode()
# #
# #     if np.random.randint(100) >= con3_pkt_loss_rate:
# #         decoder.decode(buf3)
# #         if prev_rank == decoder.rank():
# #             lin_dep_pkts += 1
# #         prev_rank = decoder.rank()
# #
# # print("Lin Dep Pkts : " + str(lin_dep_pkts))
# # print("sent Pkts    : " + str(sentPackets))
