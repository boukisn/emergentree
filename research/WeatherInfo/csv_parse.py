import csv
from collections import defaultdict
import sys

columns = defaultdict(list) # each value in each column is appended to a list
import os
import glob

path = '/Users/ethanwayda/Documents/WeatherInfo'
extension = 'csv'
os.chdir(path)
result = [i for i in glob.glob('*.{}'.format(extension))]
Events={
	'Wildfire' : [0,0,0,0],
	'Winter Weather': [0,0,0,0],
	'Strong Wind': [0,0,0,0],
	'Coastal Flood': [0,0,0,0],
	'Flood': [0,0,0,0],
	'Flash Flood': [0,0,0,0],
	'Thunderstorm Wind': [0,0,0,0],
	'Hail': [0,0,0,0],
	'Blizzard': [0,0,0,0],
	'Funnel Cloud': [0,0,0,0],
	'Heavy Snow': [0,0,0,0],
	'Cold/Wind Chill': [0,0,0,0],
	'Ice Storm': [0,0,0,0],
	'Marine High Wind': [0,0,0,0],
	'Winter Storm': [0,0,0,0],
	'Heavy Rain': [0,0,0,0],
	'Frost/Freeze': [0,0,0,0],
	'Lightning': [0,0,0,0],
	'Hurricane': [0,0,0,0],
	'Heat': [0,0,0,0],
	'Drought': [0,0,0,0],
	'Tropical Storm': [0,0,0,0],
	'High Wind': [0,0,0,0],
	'Tornado': [0,0,0,0]
}

for files in result:
	with open(files,'r', encoding='mac_roman', newline='') as f:
	    reader = csv.DictReader(f) # read rows into a dictionary format
	    counter = 0
	    for row in reader: # read a row as {column1: value1, column2: value2,...}
	        for (k,v) in row.items(): # go over each column name and value 
	            columns[k].append(v) # append the value into the appropriate list
	                                 # based on column name k


	for i in columns['EVENT_TYPE']:
		if i in Events:
			Events[i][0] += int(columns['INJURIES_DIRECT'][counter])
			Events[i][0] += int(columns['INJURIES_INDIRECT'][counter])
			Events[i][1] += int(columns['DEATHS_INDIRECT'][counter])
			Events[i][1] += int(columns['DEATHS_INDIRECT'][counter])
			Events[i][3] +=1
			damage = columns['DAMAGE_PROPERTY'][counter]
			if damage != '':
				if damage[-1] == 'K':
					try:
						Events[i][2] += (float(damage[:-1]) *1000)
					except  ValueError:
						pass
				elif damage[-1] == 'M':
					Events[i][2] += (float(damage[:-1]) *1000000)
				elif damage[-1] == 'B':
					Events[i][2] += (float(damage[:-1]) *1000000000)
		counter+=1

for i in Events:
	print("'" + i +"'"+ " : " + str(Events[i]) +',')

