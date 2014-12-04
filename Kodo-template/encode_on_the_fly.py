#! /usr/bin/env python
# encoding: utf-8

# Copyright Steinwurf ApS 2011-2013.
# Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
# See accompanying file LICENSE.rst or
# http://www.steinwurf.com/licensing

import os
import random
import sys

import kodo


def main():
    """
    Encode on the fly example.

    This example shows how to use a storage aware encoder which will
    allow you to encode from a block before all symbols have been
    specified. This can be useful in cases where the symbols that
    should be encoded are produced on-the-fly.
    """
    # Set the number of symbols (i.e. the generation size in RLNC
    # terminology) and the size of a symbol in bytes
    symbols = 42
    symbol_size = 160

    # In the following we will make an encoder/decoder factory.
    # The factories are used to build actual encoders/decoders
    encoder_factory = kodo.OnTheFlyEncoderFactoryBinary(
        max_symbols=symbols,
        max_symbol_size=symbol_size)
    encoder = encoder_factory.build()

    decoder_factory = kodo.OnTheFlyDecoderFactoryBinary(
        max_symbols=symbols,
        max_symbol_size=symbol_size)

    decoder = decoder_factory.build()

    # Create some data to encode. In this case we make a buffer
    # with the same size as the encoder's block size (the max.
    # amount a single encoder can encode)
    # Just for fun - fill the input data with random data
    data_in = os.urandom(encoder.block_size())

    # Lets split the data into symbols and feed the encoder one symbol at a
    # time
    symbol_storage = [
        data_in[i:i+symbol_size] for i in range(0, len(data_in), symbol_size)
    ]

    print("Processing")
    while not decoder.is_complete():
        # Encode a packet into the payload buffer
        packet = encoder.encode()

        # Send the data to the decoders, here we just for fun
        # simulate that we are loosing 50% of the packets
        if random.choice([True, False]):
            continue

        # Packet got through - pass that packet to the decoder
        decoder.decode(packet)
        # Randomly choose to insert a symbol
        if random.choice([True, False]) and encoder.rank() < symbols:
            # For an encoder the rank specifies the number of symbols
            # it has available for encoding
            rank = encoder.rank()
            encoder.set_symbol(rank, symbol_storage[rank])

    print("Processing finished")
    # The decoder is complete, now copy the symbols from the decoder
    data_out = decoder.copy_symbols()

    # Check we properly decoded the data
    if data_out == data_in:
        print("Data decoded correctly")
    else:
        print("Unexpected failure to decode please file a bug report :)")
        sys.exit(1)

if __name__ == "__main__":
    main()
