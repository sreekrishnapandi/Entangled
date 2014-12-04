#! /usr/bin/env python
# encoding: utf-8

# Copyright Steinwurf ApS 2011-2013.
# Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
# See accompanying file LICENSE.rst or
# http://www.steinwurf.com/licensing

import argparse
import kodo
import socket
import struct
import time

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007


def main():
    """
    Multicast example, reciever part.

    An example where data is received, decoded, and finally written to a file.
    """

    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument(
        '--output-file',
        type=str,
        help='Path to the file which should be received.',
        default='output_file')

    parser.add_argument(
        '--ip',
        type=str,
        help='The ip to send to.',
        default=MCAST_GRP)

    parser.add_argument(
        '--port',
        type=int,
        help='The port to send to.',
        default=MCAST_PORT)

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run without network use.')

    args = parser.parse_args()

    # Set the number of symbols (i.e. the generation size in RLNC
    # terminology) and the size of a symbol in bytes
    symbols = 64
    symbol_size = 1400

    # In the following we will make an decoder factory.
    # The factories are used to build actual decoder
    decoder_factory = kodo.FullVectorDecoderFactoryBinary(
        max_symbols=symbols,
        max_symbol_size=symbol_size)

    decoder = decoder_factory.build()

    sock = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_DGRAM,
        proto=socket.IPPROTO_UDP)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(('', args.port))
    mreq = struct.pack("4sl", socket.inet_aton(args.ip), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print("Processing")
    while not decoder.is_complete() and not args.dry_run:
        time.sleep(0.2)
        packet = sock.recv(10240)

        decoder.decode(packet)
        print("Packet decoded!")
        print("rank: {}/{}".format(decoder.rank(), decoder.symbols()))

        # Write data to file (it may not be valid until the very end though).
        f = open(args.output_file, 'wb')
        f.write(decoder.copy_symbols())
        f.close()

    print("Processing finished")

if __name__ == "__main__":
    main()
