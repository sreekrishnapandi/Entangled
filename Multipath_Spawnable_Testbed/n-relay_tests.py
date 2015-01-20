__author__ = 'Krish'

# from Multipath_Socket_Testbed2 import *
from Multipath_Soc_TB_Dynamic_FloCtrl import *

"""------- Average Statistics (Text report) --------"""


def avg_statistics():
    Node.RECODE = True
    Node.RelayOnlyWhenRecieved = True
    Node.relayz = 25
    Node.staticPause = 0

    iterations = 10

    avg_time_taken = 0
    avg_encoded_packets = 0
    avg_decoded_packets = 0
    avg_relayed_packets = 0
    avg_dec_LD_profile = [0 for _ in range(65)]

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
    avg_list_tx_prob = [0 for _ in range(Node.relayz+2)]

    volume = [0 for _ in range(Node.relayz+2)]
    IQ = [0 for _ in range(Node.relayz+2)]
    rank = [0 for _ in range(Node.relayz+2)]
    rank2 = [0 for _ in range(Node.relayz+2)]

    for i in range(iterations):
        initialize()

        coord = [1]
        for _ in range(1, 5):coord.append(coord[-1] + 4.25)
        #print(coord)

        src = Node(10, 0)

        snk = Node(10, 19)

        src.source("")
        snk.sink()
        for x in coord:
            for y in coord:
                RelayXY = Node(x, y)
                RelayXY.relay()




        # relay1 = Node(5, 15)
        # relay2 = Node(10, 15)
        # relay3 = Node(15, 15)
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


        while not Node.DECODED: pass
        print("==================------------------------- Encoded Pkts : " + str(Node.encoded_packets))

        print chunk_transpose(Node.list_tx_prob[2:], 5)

        avg_time_taken += Node.time_taken
        avg_encoded_packets += Node.encoded_packets
        avg_decoded_packets += Node.decoded_packets
        avg_relayed_packets += Node.relayed_pkts

        for i in range(65):
            avg_dec_LD_profile[i] += Node.Dec_LD_profile[i]

        for i in range(Node.relayz+2):          # To average the Contribution values
            avg_contr_dec[i] += snk.contribution[i]
            avg_innov_contr_dec[i] += snk.innov_contribution[i]
            avg_redund_dec[i] += snk.redundant_pkts[i]

            # avg_contr_rel1[i] += relay1.contribution[i]
            # avg_innov_contr_rel1[i] += relay1.innov_contribution[i]
            # avg_redund_rel1[i] += relay1.redundant_pkts[i]
            #
            # avg_contr_rel2[i] += relay2.contribution[i]
            # avg_innov_contr_rel2[i] += relay2.innov_contribution[i]
            # avg_redund_rel2[i] += relay2.redundant_pkts[i]
            #
            # avg_contr_rel3[i] += relay3.contribution[i]
            # avg_innov_contr_rel3[i] += relay3.innov_contribution[i]
            # avg_redund_rel3[i] += relay3.redundant_pkts[i]

            avg_indiv_relayed_pkts[i] += Node.indiv_relayed_pkts[i]
            avg_list_tx_prob[i] += Node.list_tx_prob[i]

            #print(avg_redund_dec)
            #print(avg_redund_rel3)
        #print(snk.contribution)

        # print (chunk_transpose(Node.list_tx_prob[2:], 5))

        delay()
        delay()
        delay()
        delay()
        delay()                     # To wait for OS to close the sockets , so that its available for next iteration

    delay()
    print("Source  : (" + str(src.x) + ", " + str(src.y) + ")")
    print("Sink    : (" + str(snk.x) + ", " + str(snk.y) + ")")
    print("Relays  : " + str(Node.relayz))

    # print("Relay 1 : (" + str(relay1.x) + ", " + str(relay1.y) + ")")
    # print("Relay 2 : (" + str(relay2.x) + ", " + str(relay2.y) + ")")
    # print("Relay 3 : (" + str(relay3.x) + ", " + str(relay3.y) + ")")

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
        avg_list_tx_prob[i] /= iterations

    # for i in range(65):
    #         avg_dec_LD_profile[i] /= iterations

    for i in range(Node.relayz+2):
        try:
            volume[i] = round(avg_contr_dec[i]*1.0/avg_indiv_relayed_pkts[i], 2)
            IQ[i] = round(avg_innov_contr_dec[i]*1.0/avg_indiv_relayed_pkts[i], 2)
            #rank[i] = round(volume[i] * IQ[i], 2)
            rank[i] = round(avg_innov_contr_dec[i]*1.0/avg_contr_dec[i], 2)
            avg_list_tx_prob[i] = round(avg_list_tx_prob[i], 2)
        except ZeroDivisionError:
            volume[i] = 0
            IQ[i] = 0
            rank[i] = 0
            rank2[i] = 0
            pass




    print("\nAverage of " + str(iterations) + " iterations")
    print("Time Taken    : " + str(avg_time_taken/iterations))
    print("Min req packets : " + str(src.symbols))
    print("Encoded Pkts : " + str(avg_encoded_packets/iterations))
    print("Relayed Pkts : " + str(avg_relayed_packets/iterations))
    print("Decoded Pkts : " + str(avg_decoded_packets/iterations))
    print("TOTAL Pkts   : " + str((avg_relayed_packets + avg_encoded_packets)/iterations))

    print("Indiv. Relayed Pkts : " + str(chunk_transpose(avg_indiv_relayed_pkts[2:], 5)))

    print("\nContribution in Decoder : " + str(chunk_transpose(avg_contr_dec[2:], 5)))
    print("Innov Contr. in Decoder: " + str(chunk_transpose(avg_innov_contr_dec[2:], 5)))
    print("Redund. Pkts in Decoder : " + str(chunk_transpose(avg_redund_dec[2:], 5)))

    print("\nVolume : " + str(chunk_transpose(volume[2:], 5)))
    print("IQ     : " + str(chunk_transpose(IQ[2:], 5)))
    print("Rank   : " + str(chunk_transpose(rank[2:], 5)))

    print "\nTx-Prob: ", chunk_transpose(avg_list_tx_prob[2:], 5)



    # print("\nVolume : " + str(volume))
    # print("IQ     : " + str(IQ))
    # print("Rank   : " + str(rank))

    #print("Rank2  : " + str(chunk_transpose(rank2[2:], 5)))


    # print("\nContribution in Relay 1 : " + str(avg_contr_rel1))
    # print("Innov Contr. in Relay 1 : " + str(avg_innov_contr_rel1))
    # print("Redund. Pkts in Relay 1 : " + str(avg_redund_rel1))
    #
    # print("\nContribution in Relay 2 : " + str(avg_contr_rel2))
    # print("Innov Contr. in Relay 2 : " + str(avg_innov_contr_rel2))
    # print("Redund. Pkts in Relay 2 : " + str(avg_redund_rel2))
    #
    # print("\nContribution in Relay 3 : " + str(avg_contr_rel3))
    # print("Innov Contr. in Relay 3 : " + str(avg_innov_contr_rel3))
    # print("Redund. Pkts in Relay 3 : " + str(avg_redund_rel3))

    # plt.figure(1, figsize=(13, 4))
    # plt.subplot(141)
    # plt.bar([0, 1, 2, 3, 4], avg_innov_contr_dec, color='#2166AC', label='Innovative Pkts')
    # plt.bar([0, 1, 2, 3, 4], avg_redund_dec, bottom=avg_innov_contr_dec, color='#B2182B', label='Redundant Pkts')
    # plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5], ['Enc', 'Dec', 'R1', 'R2', 'R3'])
    # plt.ylabel("Packets")
    # plt.xlabel("Decoder")
    # #plt.legend(loc='upper left')
    #
    # plt.subplot(142)
    # plt.bar([0, 1, 2, 3, 4], avg_innov_contr_rel1, color='#2166AC', label='Innovative Pkts')
    # plt.bar([0, 1, 2, 3, 4], avg_redund_rel1, bottom=avg_innov_contr_rel1, color='#B2182B', label='Redundant Pkts')
    # plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5], ['Enc', 'Dec', 'R1', 'R2', 'R3'])
    # plt.xlabel("Relay 1")
    # plt.ylabel("Packets")
    #
    # plt.subplot(143)
    # plt.bar([0, 1, 2, 3, 4], avg_innov_contr_rel2, color='#2166AC', label='Innovative Pkts')
    # plt.bar([0, 1, 2, 3, 4], avg_redund_rel2, bottom=avg_innov_contr_rel2, color='#B2182B', label='Redundant Pkts')
    # plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5], ['Enc', 'Dec', 'R1', 'R2', 'R3'])
    # plt.xlabel("Relay 2")
    # plt.ylabel("Packets")
    #
    # plt.subplot(144)
    # plt.bar([0, 1, 2, 3, 4], avg_innov_contr_rel3, color='#2166AC', label='Innovative Pkts')
    # plt.bar([0, 1, 2, 3, 4], avg_redund_rel3, bottom=avg_innov_contr_rel3, color='#B2182B', label='Redundant Pkts')
    # plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5], ['Enc', 'Dec', 'R1', 'R2', 'R3'])
    # plt.ylabel("Packets")
    # plt.xlabel("Relay 3")
    #
    # plt.subplots_adjust(left=0.04, right=0.98)
    #
    # plt.figure(2,figsize=(8, 4))
    # plt.subplots_adjust(left=0.07, right=0.97)
    # plt.plot([i for i in range(65)], avg_dec_LD_profile)
    #
    # plt.show()


avg_statistics()