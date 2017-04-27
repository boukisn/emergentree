Events_Data={
	'Flood' : [41776, 590, 336313194370.0, 467270],
	'Winter Weather' : [37178, 6972, 598050800.0, 385860],
	'Blizzard' : [8553, 860, 12305872050.0, 130931],
	'Heavy Snow' : [14450, 1284, 11572625569.999998, 655470],
	'Winter Storm' : [34065, 2990, 27171495230.0, 704720],
	'Lightning' : [63105, 476, 9857865340.0, 188835],
	'Heavy Rain' : [5085, 828, 8014299710.0, 186830],
	'Funnel Cloud' : [23, 0, 1666600.0, 82734],
	'Marine High Wind' : [63, 6, 78261070.0, 1774],
	'Drought' : [67, 0, 21766880750.0, 451608],
	'Ice Storm' : [11642, 1084, 72944744270.0, 136267],
	'Tropical Storm' : [5187, 258, 127576044050.0, 45047],
	'Frost/Freeze' : [133, 30, 946655000.0, 83702],
	'Strong Wind' : [5139, 560, 2807047840.0, 176670],
	'Wildfire' : [23117, 366, 119706213800.0, 59150],
	'Tornado' : [258573, 382, 291117453890.0, 319634],
	'High Wind' : [23308, 1046, 92108262600.0, 656908],
	'Cold/Wind Chill' : [3945, 146, 627923400.0, 168430],
	'Hurricane' : [21954, 452, 62492662000.0, 1494],
	'Coastal Flood' : [193, 52, 112278210600.0, 20933],
	'Thunderstorm Wind' : [78183, 758, 109148985950.0, 2913519],
	'Heat' : [117000, 732, 163320000.0, 215183],
	'Flash Flood' : [112984, 464, 240929082420.0, 767848],
	'Hail' : [10836, 60, 207748221950.0, 2848892]
	}

Events_Percent={
	'Wildfire' : [0,0,0],
	'Winter Weather': [0,0,0],
	'Strong Wind': [0,0,0],
	'Coastal Flood': [0,0,0],
	'Flood': [0,0,0],
	'Flash Flood': [0,0,0],
	'Thunderstorm Wind': [0,0,0],
	'Hail': [0,0,0],
	'Blizzard': [0,0,0],
	'Funnel Cloud': [0,0,0],
	'Heavy Snow': [0,0,0],
	'Cold/Wind Chill': [0,0,0],
	'Ice Storm': [0,0,0],
	'Marine High Wind': [0,0,0],
	'Winter Storm': [0,0,0],
	'Heavy Rain': [0,0,0],
	'Frost/Freeze': [0,0,0],
	'Lightning': [0,0,0],
	'Hurricane': [0,0,0],
	'Heat': [0,0,0],
	'Drought': [0,0,0],
	'Tropical Storm': [0,0,0],
	'High Wind': [0,0,0],
	'Tornado': [0,0,0]
}

Scaled_Data = {
	'Wildfire' : [0,0,0],
	'Winter Weather': [0,0,0],
	'Strong Wind': [0,0,0],
	'Coastal Flood': [0,0,0],
	'Flood': [0,0,0],
	'Flash Flood': [0,0,0],
	'Thunderstorm Wind': [0,0,0],
	'Hail': [0,0,0],
	'Blizzard': [0,0,0],
	'Funnel Cloud': [0,0,0],
	'Heavy Snow': [0,0,0],
	'Cold/Wind Chill': [0,0,0],
	'Ice Storm': [0,0,0],
	'Marine High Wind': [0,0,0],
	'Winter Storm': [0,0,0],
	'Heavy Rain': [0,0,0],
	'Frost/Freeze': [0,0,0],
	'Lightning': [0,0,0],
	'Hurricane': [0,0,0],
	'Heat': [0,0,0],
	'Drought': [0,0,0],
	'Tropical Storm': [0,0,0],
	'High Wind': [0,0,0],
	'Tornado': [0,0,0]
}

Scaled_Percent = dict()

Injury_Total =0
Death_Total =0
Damage_Total =0
Scaled_Damage = 0

for event in Events_Data:
	Injury_Total += Events_Data[event][0]
	Death_Total += Events_Data[event][1]
	Damage_Total += Events_Data[event][2]

print (Injury_Total)
print (Death_Total)
print (Damage_Total)

print(' ')
print(' ')

for event in Events_Data:
	Events_Percent[event][0] += ((Events_Data[event][0]/Injury_Total) *100)
	Events_Percent[event][1] += ((Events_Data[event][1]/Death_Total) *100)
	Events_Percent[event][2] += ((Events_Data[event][2]/Damage_Total) *100)
	Scaled_Data[event][0] = Events_Data[event][0]/Events_Data[event][3]
	Scaled_Data[event][1] = Events_Data[event][1]/Events_Data[event][3]
	Scaled_Data[event][2] = Events_Data[event][2]/Events_Data[event][3]

for event in Scaled_Data:
	if event != "Hurricane":
		Scaled_Damage += Scaled_Data[event][2]

for event in Scaled_Data:
	if event != "Hurricane":
		Scaled_Percent[event] = ((Scaled_Data[event][2]/ Scaled_Damage))
	


sorted_Death = sorted(Events_Percent.items(), key=lambda x: x[1][1], reverse = True)
sorted_Damage = sorted(Events_Percent.items(), key=lambda x: x[1][2], reverse = True)
sorted_Death_Scaled = sorted(Scaled_Data.items(), key=lambda x: x[1][1], reverse = True)
sorted_Damage_Scaled = sorted(Scaled_Data.items(), key=lambda x: x[1][2], reverse = True)
sorted_perc_scaled = sorted(Scaled_Percent.items(), key=lambda x: x[1], reverse = True)

for i in sorted_perc_scaled:
	print(i[0] +": " + str(i[1]))


'''Percent = dict()
print(' ')
print(' ')
for i in sorted_Death:
	print(i[0] +": " + str(i[1][1]))
	Percent[i[0]] = i[1][1]

print(' ')
print(' ')

for i in sorted_Damage:
	print(i[0] +": " + str(i[1][2]))
	Percent[i[0]] += i[1][2]

print(' ')
print(' ')

for i in sorted_Death_Scaled:
	print(i[0] +": " + str(i[1][1]))

print(' ')
print(' ')

for i in sorted_Damage_Scaled:
	print(i[0] +": " + str(i[1][2]))

print(' ')
print(' ')


sorted_perc = sorted(Percent.items(), key=lambda x: x[1], reverse = True)

#for i in sorted_perc:
#	print(i[0] +": " + str(i[1]))'''





