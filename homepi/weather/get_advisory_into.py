import pyowm
import requests
import json
#AppID eTNLa2UVUaDHQZMFw8hP
#App Code F9gx8fA34F1sS5V1i3q1dQ
#client_id=SuAEvRZ31hmCxUhGx5o94
#client_secret=NHSPTJqz4EdfgwdwbcDvWSN5Pa5kP3Nrvp96b887

target = open('advisory_info.config','w')
f = requests.get('https://api.aerisapi.com/advisories/closest?p=13201&limit=5&radius=50mi&client_id=SuAEvRZ31hmCxUhGx5o94&client_secret=NHSPTJqz4EdfgwdwbcDvWSN5Pa5kP3Nrvp96b887')
jsonResponse=f.json()
target.write(jsonResponse["response"][0]["details"]["body"])
# target.write(', ')
# target.write(jsonResponse["response"][0]["details"]["name"])
# target.close()
#print(jsonResponse)
target.close()