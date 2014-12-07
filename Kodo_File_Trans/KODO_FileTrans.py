__author__ = 'Krish'

import socket
import os
import kodo

def recvFileKODO(adr, file):
    print "in recv"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 8383))

    f = open(file, 'wb')

    symbol_size = 128
    symCount = s.recvfrom(64)
    symbols = int(symCount[0])

    decoder_factory = kodo.full_rlnc_decoder_factory_binary(symbols, symbol_size)
    decoder = decoder_factory.build()
    i = 0
    while not decoder.is_complete():
        rx = s.recvfrom(512)[0]
        i +=1
        print str(len(rx)) + rx[-1] + " " + str(i)
        decoder.decode(rx)
        print("rank: {}/{}".format(decoder.rank(), decoder.symbols()))

    print("DECODED")
    for i in range(10000):
        s.sendto("DECODED", adr)
    d_out = decoder.copy_symbols()
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
    symbols = (fsize/symbol_size) + 1
    blksize = symbol_size * symbols
    s.sendto(str(symbols), adr)

    encoder_factory = kodo.full_rlnc_encoder_factory_binary(symbols, symbol_size)   # Why two steps???
    encoder = encoder_factory.build()

    print "File Size : " + str(fsize)
    print "No of Symbols  : " + str(symbols)

    encoder.set_symbols('*' * (blksize - fsize) + f.read())

    while not rx == "DECODED":
        pkt = encoder.encode()
        try:
            print "sending.."
            print s.sendto(str(pkt), adr)
            rx = s.recvfrom(64)[0]
        except IOError as e:
            # print("Problem in Conn.")
            # print(e.strerror)
            continue
    print("Sent Successfully... I guess :P ")


