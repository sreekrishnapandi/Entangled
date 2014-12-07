__author__ = 'Krish'
import os
import kodo
import time
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
        prev_buf3 = 0
        prev_buf4 = 0


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
            if np.random.randint(100) >= con5_pkt_loss_rate and not prev_buf4 == buf4:
                if recode == 1:
                    recoder1.decode(buf4)
            if recode == 1:
                buf3 = recoder1.recode()
                relayed_pkts +=1

            if np.random.randint(100) > con2_pkt_loss_rate:
                if recode == 0:
                    buf4 = buf1
                    relayed_pkts += 1
                else:
                    recoder2.decode(buf1)
            if np.random.randint(100) >= con5_pkt_loss_rate and not buf3 == prev_buf3:
                if recode == 1:
                    recoder2.decode(buf3)

            if recode == 1:
                buf4 = recoder2.recode()
                relayed_pkts += 1

            if np.random.randint(100) >= con3_pkt_loss_rate and not prev_buf3 == buf3:
                decoder.decode(buf3)
                #print(decoder.rank())
                if prev_rank == decoder.rank():
                    lin_dep_pkts += 1
                prev_rank = decoder.rank()
                prev_buf3 = buf3

            if np.random.randint(100) >= con4_pkt_loss_rate and not prev_buf4 == buf4:
                decoder.decode(buf4)
                if prev_rank == decoder.rank():
                    lin_dep_pkts += 1
                prev_rank = decoder.rank()
                prev_buf4 = buf4

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
    #print("Overhead            = " + str(pkt_overhead))
    print("Redundancy          = " + str(redundancy))
    print("Lin dependant pkts  = " + str(lin_dep_pkts))
    print("Relayed Packets     = " + str(relayed_pkts))
    print("Channel 1,2 Loss    = " + str(link1))
    print("Channel 3,4 Loss    = " + str(link3))
    print("Recoding            = " + str(recode))

    report = {'time': time_taken, 'sent_pkts': sentPackets, 'min_pkts': min_req_pkts,
              'overhead': pkt_overhead, 'redundancy': redundancy}

    return time_taken, sentPackets, lin_dep_pkts, relayed_pkts, redundancy, link1, link3, link5
