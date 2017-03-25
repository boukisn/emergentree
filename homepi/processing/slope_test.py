import sys
import math
import numpy
import os.path



tree_stats = open (sys.argv[1], 'r' )
wind_speeds = open(sys.argv[2], 'r')
avg_var = open(sys.argv[3], 'ab')
x_acc=[]
y_acc=[]
z_acc=[]
wind = []
total_acc = []
anglesx=[]
anglesy=[]
angles=[]



currangles = ""
filename = "/home/pi/emergentree/homepi/frontend/server/angle.config"
if os.path.exists(filename):
	f = open(filename,'r')
	for line in f:
		currangles = line
	f.close()
	f = open(filename,'w')

	for line in tree_stats:
		anglesx.append(float(line.split(" ")[0]))
		anglesy.append(float(line.split(" ")[1]))

	avgx = float(numpy.mean(anglesx))
	avgy = float(numpy.mean(anglesy))
	variance = abs(numpy.mean((float(currangles.split(",")[0]) - avgx) + (float(currangles.split(",")[1]) - avgy)))
	f.write(currangles.split(",")[0]+","+currangles.split(",")[1]+","+str(variance))
	f.close()

else:
	for line in tree_stats:
		anglesx.append(float(line.split(" ")[0]))
		anglesy.append(float(line.split(" ")[1]))
	file_name = open('/home/pi/emergentree/homepi/frontend/server/angle.config','w+')
	file_name.write(str(numpy.mean(anglesx))+","+str(numpy.mean(anglesy))+","+"0")
	file_name.close()

for line in tree_stats:
	x_acc.append(float(line.split(" ")[2]))
	y_acc.append(float(line.split(" ")[3]))
	z_acc.append(float(line.split(" ")[4]))
	total_acc.append(math.sqrt((x_acc[-1]^2)+(y_acc[-1]^2)+(z_acc[-1]^2)))
 
for line in wind_speeds:
	wind.append(float(line))

avg_var.write(str(numpy.mean(total_acc)) +' ' + str(numpy.mean(wind)) +'\n') 
print
print ("Writing...")
print ("Average wind speed:            " + str(numpy.mean(wind)))
print ("Average overall acceleration:  " + str(numpy.mean(total_acc)))
print

	





