__author__ = 'Krish'

import csv
import time
import datetime
from Multipath_Soc_TB2_Pause_list import *
# from Multipath_Soc_TB_Dynamic_FloCtrl import *


"""------- Average Statistics (Text report) --------"""


def avg_statistics(x1, y1):
    Node.RECODE = True
    Node.RelayOnlyWhenRecieved = True
    Node.relayz = 3
    Node.staticPause = 5

    avg_time_taken = 0
    avg_encoded_packets = 0
    avg_decoded_packets = 0
    avg_relayed_packets = 0
    avg_dec_LD_profile = [0 for _ in range(101)]

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

    avg_indiv_relayed_pkts = [0 for _ in range(Node.relayz+2)]

    prev_cumil_indiv_rel_pkts_ = [0 for _ in range(Node.relayz+2)]

    iterations = 75

    prev_rates = []

    Node.history_innov_pkts = [[0 for _ in range(Node.relayz+2)] for __ in range(Node.relayz+2)]

    for i in range(iterations):

        initialize()


        src = Node(10, 0)
        snk = Node(10, 19)
        relay1 = Node(5, 5)
        relay2 = Node(x1, y1)
        relay3 = Node(15, 15)
        #master = Node(0, 0)

        # src.txprob = 42
        # relay1.txprob = 42
        # relay2.txprob = 62
        # relay3.txprob = 46

        # src.txprob = 100
        # relay1.txprob = 100
        # relay2.txprob = 100
        # relay3.txprob = 100

        #master.master()

        src.source("")
        snk.sink()
        relay1.relay()
        relay2.relay()
        relay3.relay()


        while not Node.DECODED: pass
        # print("==================------------------------- Encoded Pkts : " + str(Node.encoded_packets) +
        #                                 " Total Pkts : " + str(Node.encoded_packets + Node.relayed_pkts))

        # print(Node.R_relays)

        # print "Tx Probs in avg : ", Node.list_tx_prob

        # prev_rates = Node.R_relays
        # prev_cumil_indiv_rel_pkts_ = Node.cumilative_indiv_relayed_pkts

        avg_time_taken += Node.time_taken
        avg_encoded_packets += Node.encoded_packets
        avg_decoded_packets += Node.decoded_packets
        avg_relayed_packets += Node.relayed_pkts

        for i in range(101):
            avg_dec_LD_profile[i] += Node.Dec_LD_profile[i]


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

            avg_indiv_relayed_pkts[i] += Node.indiv_relayed_pkts[i]

        delay()
        delay()
        delay()
        delay()
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

        avg_indiv_relayed_pkts[i] /= iterations

    # for i in range(65):
    #         avg_dec_LD_profile[i] /= iterations

    print("\nAverage of " + str(iterations) + " iterations")
    print("Time Taken    : " + str(avg_time_taken/iterations))
    print("Min req packets : " + str(src.symbols))
    print("Encoded Pkts : " + str(avg_encoded_packets/iterations))
    print("Relayed Pkts : " + str(avg_relayed_packets/iterations))
    print("Decoded Pkts : " + str(avg_decoded_packets/iterations))
    print("Total Pkts   : " + str((avg_relayed_packets/iterations)+(avg_encoded_packets/iterations)))

    print("Iniv. Relayed Pkts : " + str(avg_indiv_relayed_pkts))

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
    plt.ylim(0, 85)
    plt.ylabel("Packets")
    plt.xlabel("Decoder")
    #plt.legend(loc='upper left')

    plt.subplot(142)
    plt.bar([0, 1, 2, 3, 4], avg_innov_contr_rel1, color='#2166AC', label='Innovative Pkts')
    plt.bar([0, 1, 2, 3, 4], avg_redund_rel1, bottom=avg_innov_contr_rel1, color='#B2182B', label='Redundant Pkts')
    plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5], ['Enc', 'Dec', 'R1', 'R2', 'R3'])
    plt.ylim(0, 85)
    plt.xlabel("Relay 1")
    plt.ylabel("Packets")

    plt.subplot(143)
    plt.bar([0, 1, 2, 3, 4], avg_innov_contr_rel2, color='#2166AC', label='Innovative Pkts')
    plt.bar([0, 1, 2, 3, 4], avg_redund_rel2, bottom=avg_innov_contr_rel2, color='#B2182B', label='Redundant Pkts')
    plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5], ['Enc', 'Dec', 'R1', 'R2', 'R3'])
    plt.ylim(0, 85)
    plt.xlabel("Relay 2")
    plt.ylabel("Packets")

    plt.subplot(144)
    plt.bar([0, 1, 2, 3, 4], avg_innov_contr_rel3, color='#2166AC', label='Innovative Pkts')
    plt.bar([0, 1, 2, 3, 4], avg_redund_rel3, bottom=avg_innov_contr_rel3, color='#B2182B', label='Redundant Pkts')
    plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5], ['Enc', 'Dec', 'R1', 'R2', 'R3'])
    plt.ylim(0, 85)
    plt.ylabel("Packets")
    plt.xlabel("Relay 3")

    plt.subplots_adjust(left=0.04, right=0.98)

    for i in range(101):
        avg_dec_LD_profile[i] = avg_dec_LD_profile[i] * 1.0 / 100

    plt.figure(2)
    # plt.ylim(0, 0.5)
    print(avg_dec_LD_profile)
    plt.plot([i for i in range(101)], avg_dec_LD_profile)

    # plt.show()

    return (Node.staticPause, x1,\
           iterations,\
           (avg_encoded_packets/iterations),\
           (avg_relayed_packets/iterations),\
           (avg_relayed_packets/iterations)+(avg_encoded_packets/iterations),
            avg_indiv_relayed_pkts[2], avg_indiv_relayed_pkts[3], avg_indiv_relayed_pkts[4],
            avg_contr_dec[0], avg_contr_dec[2], avg_contr_dec[3], avg_contr_dec[4],
            avg_innov_contr_dec[0], avg_innov_contr_dec[2], avg_innov_contr_dec[3], avg_innov_contr_dec[4],
            avg_redund_dec[0], avg_redund_dec[2], avg_redund_dec[3], avg_redund_dec[4])



total_pkt = []
x_pos = []
# for x1 in range(60):
#     print "###########  Relay 2 Coord : (", x1, ', 10) #############'
#     total_pkt.append(avg_statistics(x1*1./3, 10))
#     x_pos.append(x1)

table = [["Pause cycles", "Relay 2 Position", "Iterations", "Encoded Pkts", "Relayed Pkts", "Total Pkts",
          "Relayed - R1", "Relayed - R2", "Relayed - R3", "Dec - Contr Enc", "Dec - Contr R1", "Dec - Contr R2",
          "Dec - Contr R3", "Dec - Innov Enc", "Dec - Innov R1", "Dec - Innov R2", "Dec - Innov R3",
          "Dec - Redundant Enc", "Dec - Redundant R1", "Dec - Redundant R2", "Dec - Redundant R3"]]


for x1 in range(20):
    print "###########  Relay 2 Coord : (", x1, ', 10) #############'
    data = avg_statistics(x1, 10)
    table.append(data)
    #total_pkt.append(avg_statistics(x1, 10))
    x_pos.append(x1)

table.append('SEND wen rec')
# plt.figure(0)
# plt.plot(x_pos, total_pkt)
# plt.show()

ts = time.time()
with open('/Users/Krish/Google Drive/Notes/Project - Network Coding/Terminal_op/'+
                  datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')+'MovRel_NO_RC.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    [writer.writerow(r) for r in table]

# # total_pkt = np.array(total_pkt)
# # np.save('/Users/Krish/Google Drive/Notes/Project - Network Coding/Terminal_op/Moving Relay_NO_rate_ctrl.npy', total_pkt)
#
# x = PrettyTable()
# x.add_column('Pos', x_pos)
# x.add_column('Tot Pkt', total_pkt)
# # x.add_column('Encoded Pkts', list_encoded_packets)
# # x.add_column('Decoded Pkts', list_decoded_packets)
# # x.add_column('Relayed Pkts', list_relayed_packets)
# print x
#
# data = x.get_string()
#
# with open('/Users/Krish/Google Drive/Notes/Project - Network Coding/Terminal_op/Moving Relay_NO_rate_ctrl.txt', 'wb') as f:
#     f.write(data)
