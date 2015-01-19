__author__ = 'Krish'
from Multipath_Socket_Testbed2 import *
import scipy as sp
from scipy import interpolate
import plotly.plotly as py
from plotly.graph_objs import *
import pylab


def TwoRelay(x1, y1, x2, y2):
    """
    Give Avg statistics on system with one active relay.
    :param x1: X coordinate
    :param y1: Y coordinate
    :return: avg_time_taken, avg_encoded_packets, avg_relayed_packets, avg_decoded_packets
    """
    Node.relayz = 2

    avg_time_taken = 0
    avg_encoded_packets = 0
    avg_decoded_packets = 0
    avg_relayed_packets = 0

    avg_contr_dec = [0 for _ in range(Node.relayz+2)]
    avg_contr_rel1 = [0 for _ in range(Node.relayz+2)]
    avg_contr_rel2 = [0 for _ in range(Node.relayz+2)]
    avg_innov_contr_dec = [0 for _ in range(Node.relayz+2)]
    avg_innov_contr_rel1 = [0 for _ in range(Node.relayz+2)]
    avg_innov_contr_rel2 = [0 for _ in range(Node.relayz+2)]
    avg_redund_dec = [0 for _ in range(Node.relayz+2)]
    avg_redund_rel1 = [0 for _ in range(Node.relayz+2)]
    avg_redund_rel2 = [0 for _ in range(Node.relayz+2)]

    iterations = 10

    for i in range(iterations):
        initialize()

        #Node.RECODE = False

        src = Node(0, 0)
        snk = Node(0, 19)
        relay1 = Node(x1, y1)
        relay2 = Node(x2, y2)
        #relay3 = Node(5, 15)
        #relay4 = Node(5, 5)

        src.source("")
        snk.sink()
        relay1.relay()
        relay2.relay()
        #relay3.relay()
        #relay4.relay()

        while not Node.DECODED: pass
        print("==================------------------------- Encoded Pkts : " + str(Node.encoded_packets))
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

            avg_contr_rel2[i] += relay2.contribution[i]
            avg_innov_contr_rel2[i] += relay2.innov_contribution[i]
            avg_redund_rel2[i] += relay2.redundant_pkts[i]

        delay()                     # To wait for OS to close the sockets , so that its available for next iteration

    delay()

    for i in range(Node.relayz+2):
        avg_contr_dec[i] /= iterations
        avg_innov_contr_dec[i] /= iterations
        avg_redund_dec[i] /= iterations
        avg_contr_rel1[i] /= iterations
        avg_innov_contr_rel1[i] /= iterations
        avg_redund_rel1[i] /= iterations
        avg_contr_rel2[i] /= iterations
        avg_innov_contr_rel2[i] /= iterations
        avg_redund_rel2[i] /= iterations

    avg_total_packets = avg_encoded_packets + avg_relayed_packets

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
           avg_decoded_packets/iterations, \
           avg_contr_dec, avg_innov_contr_dec, avg_redund_dec,\
           avg_contr_rel1, avg_innov_contr_rel1, avg_redund_rel1, \
           avg_contr_rel2, avg_innov_contr_rel2, avg_redund_rel2, avg_total_packets/iterations



"""  ###########--- Sweep One Relay from Source to destination and plot the Statistics ---#########  """
list_time = []
list_encoded_packets = []
list_relayed_packets = []
list_decoded_packets = []
list_cont_dec = []
list_innov_cont_dec = []
list_red_dec = []
list_cont_rel1 = []
list_innov_cont_rel1 = []
list_red_rel1 = []
list_cont_rel2 = []
list_innov_cont_rel2 = []
list_red_rel2 = []

list_total_packets = []

list_time2 = []
list_encoded_packets2 = []
list_relayed_packets2= []
list_decoded_packets2 = []
list_cont_dec2 = []
list_innov_cont_dec2 = []
list_red_dec2 = []
list_cont_rel12 = []
list_innov_cont_rel12 = []
list_red_rel12 = []
list_total_packets2 = []

index = []

map_total_pkt = []

for y1 in range(1, 19):
    map_total_pkt.append([])
    for y2 in range(1, 19):

        Node.RECODE = True
        timetaken, encoded_packets, relayed_packets, decoded_packets, cont_dec, innov_cont_dec, red_dec, cont_rel1, \
        innov_cont_rel1, red_rel1, cont_rel2, innov_cont_rel2, red_rel2, total_pkt = TwoRelay(0, y1, 0, y2)

        map_total_pkt[y1 - 1].append(total_pkt)

        list_time.append(timetaken)
        list_encoded_packets.append(encoded_packets)
        list_decoded_packets.append(decoded_packets)
        list_relayed_packets.append(relayed_packets)
        list_cont_dec.append(cont_dec)
        list_innov_cont_dec.append(innov_cont_dec)
        list_red_dec.append(red_dec)

        list_cont_rel1.append(cont_rel1)
        list_innov_cont_rel1.append(innov_cont_rel1)
        list_red_rel1.append(red_rel1)

        list_cont_rel2.append(cont_rel2)
        list_innov_cont_rel2.append(innov_cont_rel2)
        list_red_rel2.append(red_rel2)

        list_total_packets.append(encoded_packets + relayed_packets)
        #index.append(i)

        Node.RECODE = False

        # timetaken, encoded_packets, relayed_packets, decoded_packets, cont_dec, innov_cont_dec, red_dec, cont_rel1, \
        # innov_cont_rel1, red_rel1 = OneRelay(0, i)

        list_time2.append(timetaken)
        list_encoded_packets2.append(encoded_packets)
        list_decoded_packets2.append(decoded_packets)
        list_relayed_packets2.append(relayed_packets)
        list_cont_dec2.append(cont_dec)
        list_innov_cont_dec2.append(innov_cont_dec)
        list_red_dec2.append(red_dec)
        list_cont_rel12.append(cont_rel1)
        list_innov_cont_rel12.append(innov_cont_rel1)
        list_red_rel12.append(red_rel1)
        list_total_packets2.append(encoded_packets + relayed_packets)

print map_total_pkt
index = [_ for _ in range(1, 19)]
print index
z = np.array(map_total_pkt)

intrp_data = interpolate.interp2d(index, index, z, kind='cubic')

pylab.figure(1)
pylab.clf()
pylab.imshow(map_total_pkt, cmap=plt.cm.jet)
pylab.colorbar()
plt.clim(160, 450)
pylab.gca().invert_yaxis()
#pylab.show()

newindex = np.arange(0, 18, 0.1)
print(newindex)
MAP = intrp_data(newindex, newindex)
#data.ev(newindex, newindex)
print(MAP)
np.save('/Users/Krish/Google Drive/Notes/Project - Network Coding/Terminal_op/2dmap.npy', z)

pylab.figure(2)
pylab.clf()
pylab.imshow(MAP, cmap=plt.cm.jet)
pylab.colorbar()
plt.clim(160, 450)
pylab.gca().invert_yaxis()
pylab.show()

print("Minimum at: ", np.argmin(z), " is : ", z.min())


# data = Data([Heatmap(z=map_total_pkt)])
# plot_url = py.plot(data)


# plt.figure(3)
#
# plt.subplot(131)
# plt.plot(index, list_encoded_packets, linestyle='--', marker='o', color='r', label='Encoded Packets')
# # plt.plot(index, list_encoded_packets2, linestyle='--', marker='o', color='b', label='encoded')
# # plt.legend()
# plt.ylabel("Encoded Packets")
# plt.xlabel("Relay Position")
#
#
# plt.subplot(133)
# plt.plot(index, list_total_packets, linestyle='--', marker='o', color='r', label='Total Packets')
# # plt.plot(index, list_total_packets2, linestyle='--', marker='o', color='b', label='total')
# # plt.legend()
# plt.ylabel("Total Packets")
# plt.xlabel("Relay Position")
#
# plt.subplot(132)
# plt.plot(index, list_relayed_packets, linestyle='--', marker='o', color='r', label='Relayed Packets')
# # plt.plot(index, list_relayed_packets2, linestyle='--', marker='o', color='b', label='relayed')
# # plt.legend()
# plt.ylabel("Relayed Packets")
# plt.xlabel("Relay Position")
#
# plt.figure(1)
# plt.subplot(221)
# plt.plot(index, list_time, linestyle='--', marker='o', color='r', label='Time')
# # plt.plot(index, list_time2, linestyle='--', marker='o', color='b', label='Time')
# # plt.legend()
# plt.ylabel("Time Taken")
#
# plt.subplot(222)
# plt.plot(index, list_encoded_packets, linestyle='--', marker='o', color='r', label='Encoded Packets')
# # plt.plot(index, list_encoded_packets2, linestyle='--', marker='o', color='b', label='encoded')
# # plt.legend()
# plt.ylabel("Encoded Packets")
#
# plt.subplot(223)
# plt.plot(index, list_total_packets, linestyle='--', marker='o', color='r', label='Total Packets')
# # plt.plot(index, list_total_packets2, linestyle='--', marker='o', color='b', label='total')
# # plt.legend()
# plt.ylabel("Total Packets")
#
# plt.subplot(224)
# plt.plot(index, list_relayed_packets, linestyle='--', marker='o', color='r', label='Relayed Packets')
# # plt.plot(index, list_relayed_packets2, linestyle='--', marker='o', color='b', label='relayed')
# # plt.legend()
# plt.ylabel("Relayed Packets")
#
# plt.figure(2)
# plt.subplot(231)
# plt.plot(index, list_cont_dec, linestyle='--', marker='o', color='b', label='')
# plt.ylabel("Contribution - Decoder")
#
# plt.subplot(232)
# plt.plot(index, list_innov_cont_dec, linestyle='--', marker='o', color='g', label='')
# plt.ylabel(" Innovative Contribution - Decoder")
#
# plt.subplot(233)
# plt.plot(index, list_red_dec, linestyle='--', marker='o', color='r', label='')
# plt.ylabel("Redundant - Decoder")
#
# plt.subplot(234)
# plt.plot(index, list_cont_rel1, linestyle='--', marker='o', color='b', label='')
# plt.ylabel("Contribution - Relay 1")
#
# plt.subplot(235)
# plt.plot(index, list_innov_cont_rel1, linestyle='--', marker='o', color='g', label='')
# plt.ylabel("Innovative Contribution - Relay 1")
#
# plt.subplot(236)
# plt.plot(index, list_red_rel1, linestyle='--', marker='o', color='r', label='')
# plt.ylabel("Redundant - Relay 1")
# plt.show()

# x = PrettyTable()
# x.add_column('Index', index)
# x.add_column('Time', list_time)
# x.add_column('Encoded Pkts', list_encoded_packets)
# x.add_column('Decoded Pkts', list_decoded_packets)
# x.add_column('Relayed Pkts', list_relayed_packets)
# print x
#
# data = x.get_string()
#
# with open('/Users/Krish/Office/FILES/Multipath-OneRelaySweep/Result.txt', 'wb') as f:
#     f.write(data)
