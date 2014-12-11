__author__ = 'Krish'

import os

with open('/Users/Krish/Office/FILES/randomBinary_1Byte', 'wb') as fout:
    #fout.write(os.urandom(1024*1024*1))
    fout.write(os.urandom(1))



# import hashlib
# def getHash(file):
#     hasher = hashlib.md5()
#     with open('/Users/Krish/Office/FILES/randomBinary.bin', 'rb') as afile:
#         buf = afile.read()
#         hasher.update(buf)
#     return (hasher.hexdigest())