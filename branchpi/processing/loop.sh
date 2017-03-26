#!/bin/bash
DATE=$(date +%Y_%m_%d)
echo $DATE
YEST=$(date +%Y_%m_%d -d "yesterday")
LOG='.log'
HOUR=$(date +%H)
MIN=$(date +%M)
if [ "$HOUR" -lt 6 ]; then
	QUART='_1'
	PREV='_4'
elif [ "$HOUR" -lt 12 ]; then
	QUART='_2'
	PREV='_1'
elif [ "$HOUR" -lt 18 ]; then
	QUART='_3'
	PREV='_2'
else
	QUART='_4'
	PREV='_3'
fi

echo $(python /home/pi/Documents/read_sensor.py /home/pi/Documents/emergentree/branchpi/backend/sensor_$DATE$QUART$LOG)
echo $(cat /home/pi/Documents/emergentree/branchpi/backend/sensor_$DATE$QUART$LOG)
echo $HOUR$MIN

if [ "$HOUR" -eq 0 ] && [ "$MIN" -eq 00 ]; then
	#VOLT=$(python serial_fun.py)
	cd /home/pi/Documents/emergentree/branchpi/backend
	echo sensor_$YEST$PREV$LOG
	sudo python upload.py sensor_$YEST$PREV$LOG
elif [ "$HOUR" -eq 6 ] && [ "$MIN" -eq 00 ]; then
	#VOLT=$(python serial_fun.py)
	echo sensor_$DATE$PREV$LOG
	cd /home/pi/Documents/emergentree/branchpi/backend
	sudo python upload.py sensor_$DATE$PREV$LOG
elif [ "$HOUR" -eq 12 ] && [ "$MIN" -eq 00 ]; then
	#VOLT=$(python serial_fun.py)
	cd /home/pi/Documents/emergentree/branchpi/backend
	sudo python upload.py sensor_$DATE$PREV$LOG
elif [ "$HOUR" -eq 18 ] && [ "$MIN" -eq 00 ]; then
	#VOLT=$(python serial_fun.py)
	cd /home/pi/Documents/emergentree/branchpi/backend
	sudo python upload.py sensor_$DATE$PREV$LOG
fi

