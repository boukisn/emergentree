#!/bin/bash
TODAY=$(date +%Y_%m_%d)
YESTERDAY=$(date +%Y:%m:%d -d "yesterday")

HOUR=$(date +%H)
MIN=$(date +%M)
LOG='.log'
HOME_DIR='/home/pi/emergentree/homepi'

if [ "$HOUR" -ge 0 ] && [ "$HOUR" -lt 6 ]; then
	DATE=$YESTERDAY
	QUARTER='4'
elif [ "$HOUR" -ge 6 ] && [ "$HOUR" -lt 12 ]; then
	DATE=$TODAY
	QUARTER='1'
elif [ "$HOUR" -ge 12 ] && [ "$HOUR" -lt 18 ]; then
	DATE=$TODAY
	QUARTER='2'
elif [ "$HOUR" -ge 18 ] && [ "$HOUR" -le 23 ]; then
	DATE=$TODAY
	QUARTER='3'
fi

# Download sensor data
python download.py sensor_$DATE_$QUARTER$LOG $HOME_DIR/warehouse/sensor_$DATE_$QUARTER$LOG

# Log wind speed vs. acceleration
python $HOME_DIR/processing/slope_test.py $HOME_DIR/warehouse/sensor_$DATE_$QUARTER$LOG $HOME_DIR/warehouse/wind_$DATE_$QUARTER$LOG $HOME_DIR/warehouse/output_slopes.log

# Calculate 1st regression
python regression.py $HOME_DIR/warehouse/output_slopes.log $HOME_DIR/warehouse/regress.log

# Calculate 2nd regression
python $HOME_DIR/processing/standard.py $HOME_DIR/warehouse/regress.log $HOME_DIR/frontend/server/risk.config
