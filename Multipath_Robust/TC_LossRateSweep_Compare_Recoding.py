__author__ = 'Krish'
from Multipath_robust import np, plt, multipath_switch_recoding

#FILE = '/Users/Krish/Office/FILES/randomBinary_10MB.bin'
#FILE = '/Users/Krish/Office/FILES/randomBinary_1Gen_1480x60.bin'
#FILE = '/Users/Krish/Office/FILES/randomBinary_1480x60-1.bin'
#FILE = '/Users/Krish/Office/FILES/randomBinary_1MB.bin'
FILE = '/Users/Krish/Office/FILES/randomBinary_1Gen_120x60.bin'


report1 = []
report2 = []
report3 = []
report4 = []
map1 = []
index = []
spmap = [0]


for i in range(0, 100):
    report1.append(multipath_switch_recoding(FILE, 0, 20, 20, 20, 20, i, 100))
    report2.append(multipath_switch_recoding(FILE, 1, 20, 20, 20, 20, i, 100))
    # report3.append(multipath_switch_recoding(FILE, 0, 20, 20, i, i))
    # report4.append(multipath_switch_recoding(FILE, 1, 20, 20, i, i))
    index.append(i)

R1 = np.array(report1)
R2 = np.array(report2)

R3 = np.array(report3)
R4 = np.array(report4)

plt.figure(1)
plt.title("Sweep Loss rate of channel 1 and 2")

plt.subplot(221)
plt.plot(index, R1[:, 0], linestyle='--', marker='o', color='b', label='Without Recoding')
plt.plot(index, R2[:, 0], linestyle='--', marker='o', color='r', label='With Recoding')
plt.ylabel("Time Taken")
plt.xlabel("Packet Loss Rate in channel 1,2")
plt.legend()

plt.subplot(222)
plt.plot(index, R1[:, 1], linestyle='--', marker='o', color='b', label='Without Recoding')
plt.plot(index, R2[:, 1], linestyle='--', marker='o', color='r', label='With Recoding')
plt.ylabel("Sent Packets")
plt.xlabel("Packet Loss Rate in channel 1,2")
plt.legend()

plt.subplot(223)
plt.plot(index, R1[:, 3], linestyle='--', marker='o', color='b', label='Without Recoding')
plt.plot(index, R2[:, 3], linestyle='--', marker='o', color='r', label='With Recoding')
plt.ylabel("Relayed Packets")
plt.xlabel("Packet Loss Rate in channel 1,2")
plt.legend()

plt.subplot(224)
plt.plot(index, R1[:, 2], linestyle='--', marker='o', color='b', label='Without Recoding')
plt.plot(index, R2[:, 2], linestyle='--', marker='o', color='r', label='With Recoding')
plt.ylabel("Linear Dependant Packets")
plt.xlabel("Packet Loss Rate in channel 1,2")
plt.legend()

#plt.show()
ax = plt.gca()
ax.ticklabel_format(useOffset=False)

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

plt.show()
ax = plt.gca()
ax.ticklabel_format(useOffset=False)
