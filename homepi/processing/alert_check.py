import sys
import os.path
import datetime

filename = "/home/pi/emergentree/homepi/frontend/server/settings.config"
writefile = open("/home/pi/emergentree/homepi/frontend/server/alerts.config","w+")
if os.path.exists(filename):
	f = open(filename,"r")
	for line in f:
		oldTime = line
	oldTime = oldTime.split(",")[1]
	now2 = datetime.datetime.strptime(oldTime, "%Y-%m-%d")
	delta = (datetime.datetime.now() - now2)
	if delta.seconds // 3600 + delta.days*24 > 90:
		writefile.write("WARNING,Battery,Your Battery is going to die soon\n")
	f.close()

# else:
# 	f = open(filename,"w+")
# 	now = datetime.datetime.now()
# 	f.write(str(now))
# 	f.close()
	
alertfile ="/home/pi/emergentree/homepi/weather/advisories.log"
alertfile_read = open(alertfile,"r")
if os.stat(alertfile).st_size == 0:
	pass
else:
	warning=""
	for line in alertfile_read:
		warning = line
	my_list = warning.split(",")
	writefile.write("WARNING,Weather Alert,"+my_list[1]+"\n")

anglefile = open("/home/pi/emergentree/homepi/frontend/server/angle.config","r")
anglealert=""
for line in anglefile:
	anglealert = line
anglealert = anglealert.split(",")
if float(anglealert[2]) >= 20:
	writefile.write("WARNING,Tree Angle,Angle variance is >= 20\n")	

downloadfile = open("/home/pi/emergentree/homepi/frontend/server/connection.log","r")
errcode = ""
for line in downloadfile:
	errcode = line
if errcode == "False":
	writefile.write("WARNING,Connection,File not Available in AWS")

downloadfile.close()
writefile.close()
anglefile.close()
alertfile_read.close()
