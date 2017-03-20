import sys
import math
import numpy


tree_stats = open (sys.argv[1], 'r' )
wind_speeds = open(sys.argv[2], 'r')
avg_var = open(sys.argv[3], 'ab')
x_deg =[]
y_deg=[]
x_acc=[]
y_acc=[]
z_acc=[]
wind = []
total_acc = []
for line in tree_stats:
	total_acc.append(float(line))
 
for line in wind_speeds:
	wind.append(float(line))

avg_var.write(str(numpy.mean(total_acc)) +' ' + str(numpy.mean(wind)) +'\n') 
print
print "Writing..."
print "Average wind speed:            " + str(numpy.mean(wind))
print "Average overall acceleration:  " + str(numpy.mean(total_acc))
print

	





