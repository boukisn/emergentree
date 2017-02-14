import pyowm
import requests
import json

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




target = open('weather.config','w')
r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Boston&APPID=75288d4cb078b45034abd9b522bd4192')
jsonResponse=r.json()
############max temp min temp weather_description more_in_depth_description windspeed wind_direction##############

#temp is given in kelvin so I converted to celcius
#wind speed is in m/s
#wind direction is in degrees, does not return direction.  Still looking into that

target.write(str(float(jsonResponse["main"]["temp_max"]) - 273))
target.write(' ')
target.write(str(float(jsonResponse["main"]["temp_min"]) - 273))
target.write(' ')
target.write(jsonResponse["weather"][0]["main"])
target.write(' ')
target.write(jsonResponse["weather"][0]["description"])
target.write(' ')
target.write(str(jsonResponse["wind"]["speed"]))
target.write(' ')
target.write(str(jsonResponse["wind"]["deg"]))
target.close()
