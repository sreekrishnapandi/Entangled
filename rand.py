__author__ = 'Krish'
import random

f = open('/Users/Krish/Desktop/sorc.txt', 'w')
for i in range(30000):
    f.write(str(random.randint(0,100)))

