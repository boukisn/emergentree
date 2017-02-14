import pyowm
import requests
import json
#AppID eTNLa2UVUaDHQZMFw8hP
#App Code F9gx8fA34F1sS5V1i3q1dQ
#client_id=SuAEvRZ31hmCxUhGx5o94
#client_secret=NHSPTJqz4EdfgwdwbcDvWSN5Pa5kP3Nrvp96b887

owm = pyowm.OWM('75288d4cb078b45034abd9b522bd4192')  # You MUST provide a valid API key
observation = owm.weather_at_place('Boston,US')
w = observation.get_weather()
# print(w)  
# print (w.get_wind() )                 # {'speed': 4.6, 'deg': 330}
# print(w.get_humidity())              # 87
# print(w.get_temperature('celsius'))



r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Boston&APPID=75288d4cb078b45034abd9b522bd4192')
#print(r.json())

# print('_____________________________________________________________________________________________')

# t = requests.get('http://api.openweathermap.org/data/2.5/forecast/daily?q=Boston&mode=json&units=metric&cnt=7&APPID=75288d4cb078b45034abd9b522bd4192')
# print(t.json())


# print('_____________________________________________________________________________________________')

# g = requests.get('http://api.openweathermap.org/data/2.5/forecast?q=Boston,us&mode=json&APPID=75288d4cb078b45034abd9b522bd4192')
# print(g.json())
#s = 'https://weather.api.here.com/weather/1.0/report.xml?app_id={cgCuPjZypPqVdgCFqntI}&app_code={F5rFR-CP1ds8Wnkrf3GV1A}&product=observation&name=Berlin'


#prints out all current winter storm watch advisories
target = open('advisories.log','w')
f = requests.get('https://api.aerisapi.com/advisories/closest?p=02134&limit=5&radius=50mi&client_id=SuAEvRZ31hmCxUhGx5o94&client_secret=NHSPTJqz4EdfgwdwbcDvWSN5Pa5kP3Nrvp96b887')
jsonResponse=f.json()
#target.write('\n')
target.write(jsonResponse["response"][0]["details"]["type"])
target.write(', ')
target.write(jsonResponse["response"][0]["details"]["name"])
#target.write('\n')
target.close()





