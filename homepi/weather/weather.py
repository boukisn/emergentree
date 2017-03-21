import pyowm
import requests
import json
import sys
import time

#AppID eTNLa2UVUaDHQZMFw8hP
#App Code F9gx8fA34F1sS5V1i3q1dQ
#client_id=SuAEvRZ31hmCxUhGx5o94
#client_secret=NHSPTJqz4EdfgwdwbcDvWSN5Pa5kP3Nrvp96b887

#owm = pyowm.OWM('75288d4cb078b45034abd9b522bd4192')  # You MUST provide a valid API key
#observation = owm.weather_at_place('Boston,US')
#w = observation.get_weather()
# print(w)  
# print (w.get_wind() )                 # {'speed': 4.6, 'deg': 330}
# print(w.get_humidity())              # 87

#print(w.get_temperature('fahrenheit'))

home_dir = "/home/pi/emergentree/homepi/warehouse/"
current_hour = int(time.strftime("%H"))
quarter = ""
if current_hour >= 0 and current_hour < 6:
    quarter = "1"
elif current_hour >= 6 and current_hour < 12:
    quarter = "2"
elif current_hour >= 12 and current_hour < 18:
    quarter = "3"
elif current_hour >= 18 and current_hour <= 23:
    quarter = "4"

wind_speed_file = home_dir + "wind_" + time.strftime("%Y_%m_%d_") + quarter + ".log"
wind_speed = open(wind_speed_file, 'a')
target = open(sys.argv[1],'w')
r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Boston,us&APPID=75288d4cb078b45034abd9b522bd4192')
jsonResponse=r.json()
rr = requests.get('http://api.openweathermap.org/data/2.5/forecast/daily?q=Boston,us&cnt=1&APPID=75288d4cb078b45034abd9b522bd4192')
jsonResponse2=rr.json()
#print(r.json())
############max temp min temp weather_description more_in_depth_description windspeed wind_direction##############

#temp is given in kelvin so I converted to celcius
#wind speed is in m/s
#wind direction is in degrees, does not return direction.  Still looking into that
max_temp=int(round((1.8)*(float(jsonResponse2["list"][0]["temp"]["max"])-273.15)+32.0))
target.write(str(max_temp))
target.write(',')
min_temp=int(round((1.8)*(float(jsonResponse2["list"][0]["temp"]["min"])-273.15)+32.0))
target.write(str(min_temp))
target.write(',')
target.write(str(jsonResponse["weather"][0]["id"]))
target.write(',')
target.write(str(int(round(jsonResponse["wind"]["speed"]))))
wind_float = str(float(jsonResponse["wind"]["speed"])) + "\n"
wind_speed.write(wind_float)
target.write(',')

def degToCompass(num):
    if num >= 337.5 or num < 22.5:
    	return "N"
    elif num >= 22.5  and num < 67.5:
    	return "NE"
    elif num >= 67.5  and num < 112.5:
    	return "E"
    elif num >= 112.5 and num < 157.5:
    	return "SE"
    elif num >= 157.5 and num < 202.5:
    	return "S"
    elif num >= 202.5 and num < 247.5:
    	return "SW"
    elif num >= 247.5 and num < 292.5:
    	return "W"
    elif num >= 292.5 and num < 337.5:
    	return "NW"

deg=int(jsonResponse["wind"]["deg"])
direction=degToCompass(deg)
target.write(direction)
target.close()
wind_speed.close()
