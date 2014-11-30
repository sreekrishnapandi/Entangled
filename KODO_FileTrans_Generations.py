__author__ = 'Krish'

import socket
import os
import kodo
import time
import hashlib


def getHash(FILE):
    hasher = hashlib.md5()
    with open(FILE, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    return (hasher.hexdigest())


def recvFileKODO(adr, file):
    print "in recv"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 8383))

    f = open(file, 'wb')

    symbol_size = 128
    symbols = 60
    genCount = s.recvfrom(64)[0]

    decoder_factory = kodo.full_rlnc_decoder_factory_binary(symbols, symbol_size)
    decoder = decoder_factory.build()
    i = 0
    d_out = ""

    for gen in range(int(genCount)):
        while not decoder.is_complete():
            rx = s.recvfrom(512)[0]
            i += 1
            #print str(len(rx)) + " " + str(i)
            decoder.decode(rx)
            #print("rank: {}/{}".format(decoder.rank(), decoder.symbols()))

        #print("DECODED")
        #for i in range(100):
        s.sendto("DECODED", adr)

        ##Drop packets delibrately##
        if gen < int(genCount)-1:
            for xx in range(500):
                dump = s.recvfrom(512)[0]
        ###########

        d_out += (decoder.copy_symbols())
        #print("Decoded Gen " + str(gen))

        decoder = decoder_factory.build()

    i = 0
    while d_out[i] == '*': i += 1
    f.write(d_out[i:])

    print("File Written!")


def sendFileKODO(adr, file):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 8282))
    s.settimeout(0)

    try:
        fsize = os.path.getsize(file)
    except os.error:
        print("ERROR : File Not found")

    f = open(file, 'rb')
    rx = ""

    symbol_size = 128
    symbols = 60
    generations = (fsize/(symbol_size * symbols)) + 1
    gensize = symbol_size * symbols
    blksize = symbol_size * symbols * generations
    s.sendto(str(generations), adr)

    encoder_factory = kodo.full_rlnc_encoder_factory_binary(symbols, symbol_size)   # Why two steps???
    encoder = encoder_factory.build()

    print "File Size : " + str(fsize)
    print"Bulk Size : " + str(blksize)
    print "No of Symbols  : " + str(symbols)
    print "Generations : " + str(generations)

    bulkfile = '*' * (blksize - fsize) + f.read()
    print len(bulkfile)

    i = 0
    sentPackets = 0
    for gen in range(generations):
        encoder_factory = kodo.full_rlnc_encoder_factory_binary(symbols, symbol_size)
        encoder = encoder_factory.build()

        symb = bulkfile[i:i+gensize]
        encoder.set_symbols(symb)
        i += gensize

        while not rx == "DECODED":
            pkt = encoder.encode()

            try:
                #print "sending.."
                s.sendto(str(pkt), adr)
                sentPackets +=1
                rx = s.recvfrom(64)[0]
            except IOError as e:
                # print("Problem in Conn.")
                # print(e.strerror)
                continue
        #print("Sent Generation : " + str(gen))
        rx = ''
    print(sentPackets)
    print("Sent Successfully... I guess :P ")


