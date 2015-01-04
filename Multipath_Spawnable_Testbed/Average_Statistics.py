__author__ = 'Krish'

from Multipath_Socket_Testbed import *

"""------- Average Statistics (Text report) --------"""


def avg_statistics():
    global RECODE
    RECODE = True
    Node.relayz = 3

    avg_time_taken = 0
    avg_encoded_packets = 0
    avg_decoded_packets = 0
    avg_relayed_packets = 0

    avg_contr_dec = [0 for _ in range(Node.relayz+2)]
    avg_innov_contr_dec = [0 for _ in range(Node.relayz+2)]
    avg_redund_dec = [0 for _ in range(Node.relayz+2)]

    avg_contr_rel1 = [0 for _ in range(Node.relayz+2)]
    avg_innov_contr_rel1 = [0 for _ in range(Node.relayz+2)]
    avg_redund_rel1 = [0 for _ in range(Node.relayz+2)]

    avg_contr_rel2 = [0 for _ in range(Node.relayz+2)]
    avg_innov_contr_rel2 = [0 for _ in range(Node.relayz+2)]
    avg_redund_rel2 = [0 for _ in range(Node.relayz+2)]

    avg_contr_rel3 = [0 for _ in range(Node.relayz+2)]
    avg_innov_contr_rel3 = [0 for _ in range(Node.relayz+2)]
    avg_redund_rel3 = [0 for _ in range(Node.relayz+2)]

    iterations = 20

    for i in range(iterations):
        initialize()

        src = Node(10, 0)
        snk = Node(10, 19)
        relay1 = Node(5, 5)
        relay2 = Node(10, 10)
        relay3 = Node(15, 15)

        src.source("")
        snk.sink()
        relay1.relay()
        relay2.relay()
        relay3.relay()

        while not Node.DECODED: pass
        #print("==================------------------------- Encoded Pkts : " + str(encoded_packets))
        avg_time_taken += Node.time_taken
        avg_encoded_packets += Node.encoded_packets
        avg_decoded_packets += Node.decoded_packets
        avg_relayed_packets += Node.relayed_pkts

        # print(snk.contribution)
        # print(snk.innov_contribution)
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

            avg_contr_rel3[i] += relay3.contribution[i]
            avg_innov_contr_rel3[i] += relay3.innov_contribution[i]
            avg_redund_rel3[i] += relay3.redundant_pkts[i]


        delay()                     # To wait for OS to close the sockets , so that its available for next iteration

    delay()
    print("Source  : (" + str(src.x) + ", " + str(src.y) + ")")
    print("Sink    : (" + str(snk.x) + ", " + str(snk.y) + ")")
    print("Relays  : " + str(Node.relayz))

    print("Relay 1 : (" + str(relay1.x) + ", " + str(relay1.y) + ")")
    print("Relay 2 : (" + str(relay2.x) + ", " + str(relay2.y) + ")")
    print("Relay 3 : (" + str(relay3.x) + ", " + str(relay3.y) + ")")

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

        avg_contr_rel3[i] /= iterations
        avg_innov_contr_rel3[i] /= iterations
        avg_redund_rel3[i] /= iterations

    print("\nAverage of " + str(iterations) + " iterations")
    print("Time Taken    : " + str(avg_time_taken/iterations))
    print("Min req packets : " + str(src.symbols))
    print("Encoded Pkts : " + str(avg_encoded_packets/iterations))
    print("Relayed Pkts : " + str(avg_relayed_packets/iterations))
    print("Decoded Pkts : " + str(avg_decoded_packets/iterations))

    print("\nContribution in Decoder : " + str(avg_contr_dec))
    print("Innov Contr. in Decoder : " + str(avg_innov_contr_dec))
    print("Redund. Pkts in Decoder : " + str(avg_redund_dec))

    print("\nContribution in Relay 1 : " + str(avg_contr_rel1))
    print("Innov Contr. in Relay 1 : " + str(avg_innov_contr_rel1))
    print("Redund. Pkts in Relay 1 : " + str(avg_redund_rel1))

    print("\nContribution in Relay 2 : " + str(avg_contr_rel2))
    print("Innov Contr. in Relay 2 : " + str(avg_innov_contr_rel2))
    print("Redund. Pkts in Relay 2 : " + str(avg_redund_rel2))

    print("\nContribution in Relay 3 : " + str(avg_contr_rel3))
    print("Innov Contr. in Relay 3 : " + str(avg_innov_contr_rel3))
    print("Redund. Pkts in Relay 3 : " + str(avg_redund_rel3))

    plt.figure(1)
    plt.subplot(141)
    plt.bar([0, 1, 2, 3, 4], avg_innov_contr_dec, color='#2166AC', label='Innovative Pkts')
    plt.bar([0, 1, 2, 3, 4], avg_redund_dec, bottom=avg_innov_contr_dec, color='#B2182B', label='Redundant Pkts')
    plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5], ['Enc', 'Dec', 'R1', 'R2', 'R3'])
    plt.ylabel("Packets")
    plt.xlabel("Decoder")
    plt.legend(loc='upper left')

    plt.subplot(142)
    plt.bar([0, 1, 2, 3, 4], avg_innov_contr_rel1, color='#2166AC', label='Innovative Pkts')
    plt.bar([0, 1, 2, 3, 4], avg_redund_rel1, bottom=avg_innov_contr_rel1, color='#B2182B', label='Redundant Pkts')
    plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5], ['Enc', 'Dec', 'R1', 'R2', 'R3'])
    plt.xlabel("Relay 1")
    plt.ylabel("Packets")

    plt.subplot(143)
    plt.bar([0, 1, 2, 3, 4], avg_innov_contr_rel2, color='#2166AC', label='Innovative Pkts')
    plt.bar([0, 1, 2, 3, 4], avg_redund_rel2, bottom=avg_innov_contr_rel2, color='#B2182B', label='Redundant Pkts')
    plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5], ['Enc', 'Dec', 'R1', 'R2', 'R3'])
    plt.xlabel("Relay 2")
    plt.ylabel("Packets")

    plt.subplot(144)
    plt.bar([0, 1, 2, 3, 4], avg_innov_contr_rel3, color='#2166AC', label='Innovative Pkts')
    plt.bar([0, 1, 2, 3, 4], avg_redund_rel3, bottom=avg_innov_contr_rel3, color='#B2182B', label='Redundant Pkts')
    plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5], ['Enc', 'Dec', 'R1', 'R2', 'R3'])
    plt.ylabel("Packets")
    plt.xlabel("Relay 3")

    plt.subplots_adjust(left=0.04, right=0.98)
    plt.show()


avg_statistics()