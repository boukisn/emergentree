import sys
import math
import numpy as np

avg_slopes = []
dev_slopes = []

days =[]
counter = 0

home_dir = "/home/pi/emergentree/homepi/frontend/server/"
data_file = home_dir + "output.log"
slopes = open (sys.argv[1], 'r' )
config = open(sys.argv[2], 'w')
output = open(data_file, 'a')

for line in slopes:
	avg_slopes.append(float(line))
	#print(float(line))
	#dev_slopes.append(float(info[1]))
	days.append(counter)
	counter +=1
	"""if counter == 0:
		avg_max = float(info[0])
		avg_min = float(info[0])
		dev_max = float(info[1])
		dev_min = float(info[1])
		
	
	if float(info[0]) > avg_max: #logic for finding min and maxes
		avg_max = float(info[0])
	elif float(info[0]) < avg_min:
		avg_min = float(info[0])
	if float(info[1]) > dev_max:
		avg_max = float(info[0])
	elif float(info[1]) < dev_min:
		avg_min = float(info[0])"""
	

	
#print("----------------------")

avg_of_avg= np.mean(avg_slopes)
dev_of_avg= np.std(avg_slopes, ddof=1)
#avg_of_dev= np.mean(dev_slopes)
#dev_of_dev= np.std(dev_slopes)
new_slopes=[]
for slope in avg_slopes:
	slope1 = slope
	slope = (slope - avg_of_avg)/(dev_of_avg)
	new_slopes.append(slope)
	#print(str(slope1) + " " +str(slope))

x = np.array(days)

y = np.array(new_slopes)

# Our model is y = a * x, so things are quite simple, in this case...
# x needs to be a column vector instead of a 1D vector for this, however.
x = x[:,np.newaxis]
a, _, _, _ = np.linalg.lstsq(x, y)

# Write to risk.config file
config.write(str(a[0]))
output_float = str(a[0]) + "\n"
output.write(output_float)

print
print "Standard deviation increase per 6 hours:  " + str(a[0])
print "Standard deviation increase per day:      " + str(a[0]*4)
print "Standard deviation increase per week:     " + str(a[0]*4*7)
print


