
YESTERDAY=$(date +%Y:%m:%d -d "yesterday")
SEC=$(date +%S)
DATE=$(date +%m_%d_%H_)
MIN=$(date +%M)
PAST=$(expr $MIN - 1)
LOG=.log
echo $PAST
HOME_DIR='/home/pi/emergentree/homepi'
if [ $PAST -lt 10 ]; then
	PAST=0$PAST
fi
	
echo sensor_$DATE$PAST$LOG 
if [ $SEC -lt 30 ]; then

	# Download sensor data
	sudo python $HOME_DIR/backend/download.py sensor_$DATE$PAST$LOG $HOME_DIR/warehouse/sensor_$DATE$PAST$LOG
	sudo chown pi:pi $HOME_DIR/warehouse/sensor_$DATE$PAST$LOG
	# Log wind speed vs. acceleration
	python $HOME_DIR/processing/slope_test.py $HOME_DIR/warehouse/sensor_$DATE$PAST$LOG $HOME_DIR/warehouse/wind$LOG $HOME_DIR/warehouse/output_slopes.log

	# Calculate 1st regression
	sudo python $HOME_DIR/processing/regression.py $HOME_DIR/warehouse/output_slopes.log $HOME_DIR/warehouse/regress.log

	# Calculate 2nd regression
	sudo python $HOME_DIR/processing/standard.py $HOME_DIR/warehouse/regress.log $HOME_DIR/frontend/server/risk.config
fi
