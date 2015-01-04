__author__ = 'Krish'
from Multipath_Socket_Testbed import *

"""  ###########--- Sweep One Relay from Source to destination and plot the Statistics ---#########  """
list_time = []
list_encoded_packets = []
list_relyed_packets = []
list_decoded_packets = []
index = []

for i in range(1, 25):
    timetaken, encoded_packets, relyed_packets, decoded_packets = OneRelay(1, i)
    list_time.append(timetaken)
    list_encoded_packets.append(encoded_packets)
    list_decoded_packets.append(decoded_packets)
    list_relyed_packets.append(relyed_packets)
    index.append(i)

plt.figure(1)
plt.subplot(221)
plt.plot(index, list_time, linestyle='--', marker='o', color='b', label='Time')
plt.ylabel("Time Taken")


plt.subplot(222)
plt.plot(index, list_encoded_packets, linestyle='--', marker='o', color='r', label='encoded')
plt.ylabel("Encoded Packets")

plt.subplot(223)
plt.plot(index, list_decoded_packets, linestyle='--', marker='o', color='g', label='decoded')
plt.ylabel("Decoded Packets")

plt.subplot(224)
plt.plot(index, list_relyed_packets, linestyle='--', marker='o', color='b', label='relayed')
plt.ylabel("Relayed Packets")
plt.show()

x = PrettyTable()
x.add_column('Index', index)
x.add_column('Time', list_time)
x.add_column('Encoded Pkts', list_encoded_packets)
x.add_column('Decoded Pkts', list_decoded_packets)
x.add_column('Relayed Pkts', list_relyed_packets)
print x

data = x.get_string()

with open('/Users/Krish/Office/FILES/Multipath-OneRelaySweep/Result.txt', 'wb') as f:
    f.write(data)
