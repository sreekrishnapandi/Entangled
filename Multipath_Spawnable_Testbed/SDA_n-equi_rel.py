__author__ = 'Krish'

from Multipath_Socket_Testbed2 import *

position = [15, 30, 45, 81]

i = 3

# index = [_ for _ in range(i, 16)]
index = [_ for _ in range(4, 21)]
tot_pkt = np.load('/Users/Krish/Google Drive/Notes/Project - Network Coding/Terminal_op/n-equid-rel_DEC-'+str(position[i])+'.npy')

color = 'rmbcg'
markers = '+o*.x'

plt.figure(1)
plt.subplots_adjust(left=0.17, right=0.97, bottom=0.12, top=0.96)
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)
plt.plot(index, tot_pkt, marker=markers[i], color=color[i], label=("Sink Position: "+str(position)))
plt.ylabel("Total Packets", size=23)
plt.xlabel("No. Of Relays", size=23)
plt.savefig('/Users/Krish/Dropbox/Official/ew2015-Sending_policy_ncmesh/jpeg/DEC-'+str(position[i]), dpi=100)

plt.xlim(0)
#plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
i += 1
# plt.show()


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