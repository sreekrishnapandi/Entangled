__author__ = 'Krish'
import numpy as np
import matplotlib.pyplot as plt

dat = np.loadtxt('/Users/Krish/Desktop/plot.dat')
x = [1.5, 2, 2.5, 3, 3.5, 4]
y = [-1.81E+01,
    -1.81E+01,
    -1.80E+011,
    -1.80E+01,
    -1.78E+01,
    -1.78E+01,
    -1.77E+01,
    -1.83E+01,
    -1.77E+01,
    -1.84E+01,
    -1.76E+01,
    -1.79E+01,
    -1.77E+01]

plt.pcolor(x, y, dat)
plt.colorbar()
plt.show()
print(y)
print x





print dat
# wb2 = load_workbook('/Users/Krish/Desktop/Graphs.xlsx')
# print wb2.get_sheet_names()
# ws = wb2.get_sheet_by_name('ATM')
# x= ws['W51':'AB63']
# print x
#print(ws['W51':'AB63'])
