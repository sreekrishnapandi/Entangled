#! /usr/bin/env python
# encoding: utf-8

# Copyright Steinwurf ApS 2011-2013.
# Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
# See accompanying file LICENSE.rst or
# http://www.steinwurf.com/licensing

import os
import sys

import kodo


def main():
    """Simple example showing how to encode and decode a block of memory."""
    # Set the number of symbols (i.e. the generation size in RLNC
    # terminology) and the size of a symbol in bytes
    symbols = 8
    symbol_size = 160

    # In the following we will make an encoder/decoder factory.
    # The factories are used to build actual encoders/decoders
    encoder_factory = kodo.FullVectorEncoderFactoryBinary(
        max_symbols=symbols,
        max_symbol_size=symbol_size)

    encoder = encoder_factory.build()

    decoder_factory = kodo.FullVectorDecoderFactoryBinary(
        max_symbols=symbols,
        max_symbol_size=symbol_size)

    decoder = decoder_factory.build()

    # Create some data to encode. In this case we make a buffer
    # with the same size as the encoder's block size (the max.
    # amount a single encoder can encode)
    # Just for fun - fill the input data with random data
    data_in = os.urandom(encoder.block_size())

    # Assign the data buffer to the encoder so that we can
    # produce encoded symbols
    encoder.set_symbols(data_in)

    print("Processing")
    packet_number = 0
    while not decoder.is_complete():
        # Generate an encoded packet
        packet = encoder.encode()
        print("Packet {} encoded!".format(packet_number))

        # Pass that packet to the decoder
        decoder.decode(packet)
        print("Packet {} decoded!".format(packet_number))
        packet_number += 1
        print("rank: {}/{}".format(decoder.rank(), decoder.symbols()))

    print("Processing finished")

    # The decoder is complete, now copy the symbols from the decoder
    data_out = decoder.copy_symbols()

    # Check if we properly decoded the data
    print("Checking results")
    if data_out == data_in:
        print("Data decoded correctly")
    else:
        print("Unable to decode please file a bug report :)")
        sys.exit(1)

if __name__ == "__main__":
    main()
