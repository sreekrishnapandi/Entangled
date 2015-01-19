__author__ = 'Krish'

from Multipath_Socket_Testbed2 import *


def only_decoder(x, y):
    Node.relayz = 0

    avg_time_taken = 0
    avg_encoded_packets = 0
    avg_decoded_packets = 0
    avg_relayed_packets = 0

    avg_contr_dec = [0 for _ in range(Node.relayz+2)]
    avg_innov_contr_dec = [0 for _ in range(Node.relayz+2)]
    avg_redund_dec = [0 for _ in range(Node.relayz+2)]

    iterations = 100

    for i in range(iterations):
        initialize()

        Node.RECODE = False

        src = Node(0, 0)
        snk = Node(x, y)

        src.source("")
        snk.sink()

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

        delay()                     # To wait for OS to close the sockets , so that its available for next iteration

    delay()

    for i in range(Node.relayz+2):
        avg_contr_dec[i] /= iterations
        avg_innov_contr_dec[i] /= iterations
        avg_redund_dec[i] /= iterations

    return avg_time_taken/iterations, avg_encoded_packets/iterations, avg_relayed_packets/iterations, \
           avg_decoded_packets/iterations, avg_contr_dec, avg_innov_contr_dec, avg_redund_dec


"""  ###########--- Sweep Decoder from 0% to 100% loss and plot the Statistics ---#########  """

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

for i in range(1, 20):
    timetaken, encoded_packets, relyed_packets, decoded_packets, cont_dec, innov_cont_dec, red_dec = only_decoder(0, i)

    list_time.append(timetaken)
    list_encoded_packets.append(encoded_packets)
    list_decoded_packets.append(decoded_packets)
    list_relyed_packets.append(relyed_packets)
    list_cont_dec.append(cont_dec)
    list_innov_cont_dec.append(innov_cont_dec)
    list_red_dec.append(red_dec)
    index.append(i)


plt.figure(1)

plt.subplot(121)
plt.plot(index, list_encoded_packets, linestyle='--', marker='o', color='r', label='encoded')
plt.ylabel("Encoded Packets")
plt.xlabel("Decoder Position")

plt.subplot(122)
plt.plot(index, list_decoded_packets, linestyle='--', marker='o', color='g', label='decoded')
plt.ylabel("Decoded Packets")

plt.show()