#!/bin/bash
DATE=$(date +%m_%d_%H_%M)
SEC=$(date +%S)
echo $DATE
LOG=.log
python minute.py tester_$DATE$LOG 
#echo $(cat tester_$DATE$LOG)
if [ "$SEC" -ge 58 ]; then
	sudo python upload.py tester_$DATE$LOG 
fi
