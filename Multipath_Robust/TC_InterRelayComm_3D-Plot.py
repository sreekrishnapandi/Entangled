__author__ = 'Krish'

from Multipath_robust import np, plt, multipath_switch_recoding

#FILE = '/Users/Krish/Office/FILES/randomBinary_10MB.bin'
#FILE = '/Users/Krish/Office/FILES/randomBinary_1480x60-1.bin'
#FILE = '/Users/Krish/Office/FILES/randomBinary_1MB.bin'
FILE = '/Users/Krish/Office/FILES/randomBinary_1Gen_120x60.bin'
#FILE = '/Users/Krish/Office/FILES/randomBinary_1Byte'



report1 = []
report2 = []
report3 = []
report4 = []
map1 = []
index = []
spmap = [0]


for i in range(5, 100, 5):
    spmap.append([])
    for j in range(5, 100, 5):
        map1.append(multipath_switch_recoding(FILE, 0, i, j, 100-i, 100-j, 100, 100))
        spmap[i/5].append(map1[len(map1)-1][1])
spmap.pop(0)

""""""

"""PLOT HEATMAP"""
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

M1 = np.array(map1)

print(len(spmap))
print spmap
print(M1[:, 5])
print(len(M1[:, 5]))

fig = plt.figure(1)
plt.xlabel("Loss Rate in Channel 1")
plt.ylabel("Loss Rate in Channel 2")
ax = fig.gca(projection='3d')
X = np.arange(5, 100, 5)
Y = np.arange(5, 100, 5)
#Y = Y[::-1]
X, Y = np.meshgrid(X, Y)
Z = spmap
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
#
# cset = ax.contour(X, Y, Z, zdir='z', offset=-100, cmap=cm.coolwarm)
# cset = ax.contour(X, Y, Z, zdir='x', offset=-40, cmap=cm.coolwarm)
# cset = ax.contour(X, Y, Z, zdir='y', offset=40, cmap=cm.coolwarm)
#
surf.set_clim(vmin=3500, vmax=11000)
ax.set_zlabel("Sent Packets")
#ax.set_zlim(min(Z[0]), max(Z[-1]))
ax.set_zlim(0, 11000)

ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
fig.colorbar(surf, shrink=0.5, aspect=5)





plt.show()


