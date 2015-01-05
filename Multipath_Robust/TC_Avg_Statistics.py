__author__ = 'Krish'

from Multipath_robust import np, plt, multipath_switch_recoding

#FILE = '/Users/Krish/Office/FILES/randomBinary_10MB.bin'
#FILE = '/Users/Krish/Office/FILES/randomBinary_1Gen_1480x60.bin'
#FILE = '/Users/Krish/Office/FILES/randomBinary_1480x60-1.bin'
#FILE = '/Users/Krish/Office/FILES/randomBinary_1MB.bin'
FILE = '/Users/Krish/Office/FILES/randomBinary_1Gen_120x60.bin'


pak = 0
ldpak = 0
rpak = 0

i =50

for _x in range(i):
    _,pa,ldp,rp,_,_,_,_ = multipath_switch_recoding(FILE, 1, 50, 100, 50, 100, 100, 100)
    pak += pa
    ldpak += ldp
    rpak += rp

    #print(pak)
avg_pak = pak/i
avg_ldpak = ldpak/i
avg_rpak = rpak/i

print("AVERAGE OF 100 runs : SENT PACKETS    = " + str(avg_pak))
print("AVERAGE OF 100 runs : RELAYED PACKETS = " + str(avg_rpak))
print("AVERAGE OF 100 runs : Lin Dep PACKETS = " + str(avg_ldpak))