__author__ = 'Krish'

from Multipath_Socket_Testbed2 import *
# from Multipath_Soc_TB_Dynamic_FloCtrl import *

"""------- n-Equidistant Relays (Text report) --------"""


def n_Equidistant_Relays(no_of_relays, decoder_pos):
    Node.RECODE = True
    Node.RelayOnlyWhenRecieved = True
    Node.relayz = no_of_relays
    Node.staticPause = 0

    avg_time_taken = 0
    avg_encoded_packets = 0
    avg_decoded_packets = 0
    avg_relayed_packets = 0
    avg_dec_LD_profile = [0 for _ in range(101)]

    avg_indiv_relayed_pkts = [0 for _ in range(Node.relayz+2)]

    iterations = 50

    interval = 0
    if no_of_relays > 0:
        interval = decoder_pos * 1.0 / (no_of_relays + 1)

    for i in range(iterations):

        initialize()

        src = Node(10, 0)
        snk = Node(10, decoder_pos)

        relays = []
        position = 0
        for _ in range(no_of_relays):
            position += interval
            #print(position)
            relays.append(Node(10, position))
            relays[-1].relay()

        src.source("")
        snk.sink()

        while not Node.DECODED: pass
        print("==================------------------------- Encoded Pkts : " + str(Node.encoded_packets))
        # print(Node.R_relays)

        avg_time_taken += Node.time_taken
        avg_encoded_packets += Node.encoded_packets
        avg_decoded_packets += Node.decoded_packets
        avg_relayed_packets += Node.relayed_pkts

        for i in range(101):
            avg_dec_LD_profile[i] += Node.Dec_LD_profile[i]


        # print(snk.contribution)
        # print(snk.innov_contribution)
        for i in range(Node.relayz+2):          # To average the Contribution values
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

    for i in range(Node.relayz+2):
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

    for i in range(101):
        avg_dec_LD_profile[i] = avg_dec_LD_profile[i] * 1.0 / iterations

    return avg_encoded_packets/iterations, avg_relayed_packets/iterations, \
           (avg_relayed_packets/iterations)+(avg_encoded_packets/iterations)


"""--------------------------------------------"""

def normalize(v):
    #norm=np.linalg.norm(v)
    norm = np.amax((v))
    print "norm = ", norm
    if norm==0:
       return v
    return v*1./norm

def tot_pkt_equidist_rel(max_rel, dec_pos):
    max_relays = max_rel
    decoder_pos = dec_pos

    lst_Encodedpkts = []
    lst_RelayedPkts = []
    lst_TotalPkts = []
    index = []

    for i in range(max_relays + 1):
        if decoder_pos / (i+1) > 19:
            continue
        enc, rel, tot = n_Equidistant_Relays(i, decoder_pos)
        lst_Encodedpkts.append(enc)
        lst_RelayedPkts.append(rel)
        lst_TotalPkts.append(tot)
        index.append(i)

    print(lst_TotalPkts)
    v = np.array(lst_TotalPkts)
    norm_totalPkts = normalize(v)

    return norm_totalPkts, index

plt.figure(1)

color = 'rmbcg'
markers = '+o*.x'

i = 0
for position in [15, 25, 30, 35, 45]:
    tot_pkt, index = tot_pkt_equidist_rel(15, position)
    plt.plot(index, tot_pkt, marker=markers[i], color=color[i], label=("Sink Position: "+str(position)))
    plt.ylabel("Normalized Total Packets")
    plt.xlabel("No. Of Relays")
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    i += 1

plt.show()


# plt.figure(2)
#
# plt.subplot(131)
# plt.plot(index, lst_Encodedpkts, marker='o', color='b', label='Encoded Packets')
# plt.ylabel("Encoded Packets")
# plt.xlabel("No. Of Relays")
#
# plt.subplot(132)
# plt.plot(index, lst_RelayedPkts, marker='o', color='b', label='Relayed Packets')
# plt.ylabel("Relayed Packets")
# plt.xlabel("No. Of Relays")
#
# plt.subplot(133)
# plt.plot(index, lst_TotalPkts, marker='o', color='b', label='Total Packets')
# plt.ylabel("Total Packets")
# plt.xlabel("No. Of Relays")
#
# plt.show()