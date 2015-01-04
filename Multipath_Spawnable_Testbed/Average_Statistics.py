__author__ = 'Krish'

from Multipath_Socket_Testbed import *

"""------- Average Statistics (Text report) --------"""


def avg_statistics():
    global RECODE
    RECODE = True
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

        src = Node(0, 0)
        snk = Node(0, 19)
        relay1 = Node(0, 16)
        relay2 = Node(7, 10)
        relay3 = Node(5, 15)

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

        # print(snk.contribution)
        # print(snk.innov_contribution)
        for i in range(Node.relayz+2):          # To average the Contribution values
            avg_contr_dec[i] += snk.contribution[i]
            avg_innov_contr_dec[i] += snk.innov_contribution[i]
            avg_redund_dec[i] += snk.redundant_pkts[i]

            avg_contr_rel1[i] += relay1.contribution[i]
            avg_innov_contr_rel1[i] += relay1.innov_contribution[i]
            avg_redund_rel1[i] += relay1.redundant_pkts[i]

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

    print("\nAverage of " + str(iterations) + " iterations")
    print("Time Taken    : " + str(avg_time_taken/iterations))
    print("Min req packets : " + str(src.symbols))
    print("Encoded Pkts : " + str(avg_encoded_packets/iterations))
    print("Relayed Pkts : " + str(avg_relayed_packets/iterations))
    print("Decoded Pkts : " + str(avg_decoded_packets/iterations))
    print("Contr. in Decoder : " + str(avg_contr_dec))
    print("Innov Contr. in Decoder : " + str(avg_innov_contr_dec))
    print("Redund. Pkts in Decoder : " + str(avg_redund_dec))
    print("Contribution in Relay 1 : " + str(avg_contr_rel1))
    print("Innov Contr. in Relay 1 : " + str(avg_innov_contr_rel1))
    print("Redund. Pkts in Relay 1 : " + str(avg_redund_rel1))


avg_statistics()