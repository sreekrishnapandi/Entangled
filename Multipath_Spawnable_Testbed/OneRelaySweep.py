__author__ = 'Krish'
from Multipath_Socket_Testbed import *


def OneRelay(x, y):
    """
    Give Avg statistics on system with one active relay.
    :param x: X coordinate
    :param y: Y coordinate
    :return: avg_time_taken, avg_encoded_packets, avg_relayed_packets, avg_decoded_packets
    """
    Node.relayz = 1

    avg_time_taken = 0
    avg_encoded_packets = 0
    avg_decoded_packets = 0
    avg_relayed_packets = 0

    avg_contr_dec = [0 for _ in range(Node.relayz+2)]
    avg_contr_rel1 = [0 for _ in range(Node.relayz+2)]
    avg_innov_contr_dec = [0 for _ in range(Node.relayz+2)]
    avg_innov_contr_rel1 = [0 for _ in range(Node.relayz+2)]
    avg_redund_dec = [0 for _ in range(Node.relayz+2)]
    avg_redund_rel1 = [0 for _ in range(Node.relayz+2)]

    iterations = 20

    for i in range(iterations):
        initialize()

        Node.RECODE = False

        src = Node(0, 0)
        snk = Node(0, 19)
        relay1 = Node(x, y)
        #relay2 = Node(7, 10)
        #relay3 = Node(5, 15)
        #relay4 = Node(5, 5)

        src.source("")
        snk.sink()
        relay1.relay()
        #relay2.relay()
        #relay3.relay()
        #relay4.relay()

        while not Node.DECODED: pass
        #print("==================------------------------- Encoded Pkts : " + str(encoded_packets))
        avg_time_taken += Node.time_taken
        avg_encoded_packets += Node.encoded_packets
        avg_decoded_packets += Node.decoded_packets
        avg_relayed_packets += Node.relayed_pkts

        for i in range(Node.relayz+2):          # To average the Contribution values
            avg_contr_dec[i] += snk.contribution[i]
            avg_innov_contr_dec[i] += snk.innov_contribution[i]
            avg_redund_dec[i] += snk.redundant_pkts[i]

            avg_contr_rel1[i] += relay1.contribution[i]
            avg_innov_contr_rel1[i] += relay1.innov_contribution[i]
            avg_redund_rel1[i] += relay1.redundant_pkts[i]

        delay()                     # To wait for OS to close the sockets , so that its available for next iteration

    delay()

    for i in range(Node.relayz+2):
        avg_contr_dec[i] /= iterations
        avg_innov_contr_dec[i] /= iterations
        avg_redund_dec[i] /= iterations
        avg_contr_rel1[i] /= iterations
        avg_innov_contr_rel1[i] /= iterations
        avg_redund_rel1[i] /= iterations

    # print("Source  : (" + str(src.x) + ", " + str(src.y) + ")")
    # print("Sink    : (" + str(snk.x) + ", " + str(snk.y) + ")")
    # print("Relays  : " + str(Node.relayz))
    #
    # # print("Relay 1 : (" + str(relay1.x) + ", " + str(relay1.y) + ")")
    # # print("Relay 2 : (" + str(relay2.x) + ", " + str(relay2.y) + ")")
    # # print("Relay 3 : (" + str(relay3.x) + ", " + str(relay3.y) + ")")
    #
    # print("\nAverage of " + str(iterations) + " iterations")
    # print("Time Taken    : " + str(avg_time_taken/iterations))
    # print("Min req packets : " + str(src.symbols))
    # print("Encoded Pkts : " + str(avg_encoded_packets/iterations))
    # print("Relayed Pkts : " + str(avg_relayed_packets/iterations))
    # print("Decoded Pkts : " + str(avg_decoded_packets/iterations))

    return avg_time_taken/iterations, avg_encoded_packets/iterations, avg_relayed_packets/iterations, \
           avg_decoded_packets/iterations, avg_contr_dec, avg_innov_contr_dec, avg_redund_dec, avg_contr_rel1, \
           avg_innov_contr_rel1, avg_redund_rel1


"""  ###########--- Sweep One Relay from Source to destination and plot the Statistics ---#########  """
list_time = []
list_encoded_packets = []
list_relyed_packets = []
list_decoded_packets = []
list_cont_dec = []
list_innov_cont_dec = []
list_red_dec = []
list_cont_rel1 = []
list_innov_cont_rel1 = []
list_red_rel1 = []
index = []

for i in range(1, 25):
    timetaken, encoded_packets, relyed_packets, decoded_packets, cont_dec, innov_cont_dec, red_dec, cont_rel1, \
    innov_cont_rel1, red_rel1 = OneRelay(7, i)

    list_time.append(timetaken)
    list_encoded_packets.append(encoded_packets)
    list_decoded_packets.append(decoded_packets)
    list_relyed_packets.append(relyed_packets)
    list_cont_dec.append(cont_dec)
    list_innov_cont_dec.append(innov_cont_dec)
    list_red_dec.append(red_dec)
    list_cont_rel1.append(cont_rel1)
    list_innov_cont_rel1.append(innov_cont_rel1)
    list_red_rel1.append(red_rel1)
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

plt.figure(2)
plt.subplot(231)
plt.plot(index, list_cont_dec, linestyle='--', marker='o', color='b', label='')
plt.ylabel("Contribution - Decoder")

plt.subplot(232)
plt.plot(index, list_innov_cont_dec, linestyle='--', marker='o', color='g', label='')
plt.ylabel(" Innovative Contribution - Decoder")

plt.subplot(233)
plt.plot(index, list_red_dec, linestyle='--', marker='o', color='r', label='')
plt.ylabel("Redundant - Decoder")

plt.subplot(234)
plt.plot(index, list_cont_rel1, linestyle='--', marker='o', color='b', label='')
plt.ylabel("Contribution - Relay 1")

plt.subplot(235)
plt.plot(index, list_innov_cont_rel1, linestyle='--', marker='o', color='g', label='')
plt.ylabel("Innovative Contribution - Relay 1")

plt.subplot(236)
plt.plot(index, list_red_rel1, linestyle='--', marker='o', color='r', label='')
plt.ylabel("Redundant - Relay 1")


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
