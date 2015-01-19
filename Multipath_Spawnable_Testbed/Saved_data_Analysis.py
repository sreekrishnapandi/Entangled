__author__ = 'Krish'
from Multipath_Socket_Testbed2 import *
import scipy as sp
from scipy import interpolate
import plotly.plotly as py
from plotly.graph_objs import *
import pylab


map_total_pkt = np.load('/Users/Krish/Google Drive/Notes/Project - Network Coding/Terminal_op/2dmap.npy')
index = [_ for _ in range(1, 19)]

z = np.array(map_total_pkt)
intrp_data = interpolate.interp2d(index, index, z, kind='cubic')

pylab.figure(1)
pylab.clf()
pylab.imshow(map_total_pkt, cmap=plt.cm.jet)
pylab.colorbar()
plt.clim(180, 260)
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
plt.clim(180, 260)
pylab.gca().invert_yaxis()
pylab.show()