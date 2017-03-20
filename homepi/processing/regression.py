import sys
import math
import numpy as np


tree_avgs = open (sys.argv[1], 'r' )
slopes = open(sys.argv[2], 'ab')

avg_acc = []
avg_wind = []


for line in tree_avgs:
	info = line.split(' ')
	avg_acc.append(float(info[0]))
	avg_wind.append(float(info[1]))

m1, c1 = np.polyfit(avg_wind, avg_acc, 1)

slopes.write(str(m1) + '\n')

print
print "Writing..."
print "Linear Regression Slope of Wind Speed vs. Overall Acceleration:  " + str(m1)
print
