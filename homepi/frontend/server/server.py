from flask import Flask, jsonify, render_template

app = Flask(__name__)

alerts = {"HUW":{"desc":"Hurricane Warning","mult": 5.0}, "TOR":{"desc":"Tornado Warning","mult": 5.0}, "EWW":{"desc":"Extreme Wind Warning","mult": 5.0}, "EQW":{"desc":"Earthquake Warning","mult": 5.0}, "FRW":{"desc":"Fire Warning","mult": 5.0}, "TSW":{"desc":"Tsunami Warning","mult": 5.0}, "HUA":{"desc":"Hurricane Watch","mult": 1.5}, "TOA":{"desc":"Tornado Watch","mult": 1.5}, "TSA":{"desc":"Tsunami Watch","mult": 1.5}, "SVR":{"desc":"Severe Thunderstorm Warning","mult": 1.5}, "TRW":{"desc":"Tropical Storm Warning","mult": 1.5}, "HWW":{"desc":"High Wind Warning","mult": 1.5}, "BZW":{"desc":"Blizzard Warning","mult": 1.5}, "SVA":{"desc":"Severe Thunderstorm Watch","mult": 1.3}, "TRA":{"desc":"Tropical Storm Watch","mult": 1.3}, "HWA":{"desc":"High Wind Watch","mult": 1.3}, "WSW":{"desc":"Winter Storm Warning","mult": 1.2}, "CFW":{"desc":"Coastal Flood Warning","mult": 1.2}, "FLW":{"desc":"Flood Warning","mult": 1.2}, "WSA":{"desc":"Winter Storm Watch","mult": 1.1}, "CFA":{"desc":"Coastal Flood Watch","mult": 1.1}, "FLA":{"desc":"Flood Watch","mult": 1.1}}
home_dir = "/home/pi/emergentree/homepi/frontend/server/"

@app.route("/")
def home():
	return render_template('index.html')

@app.route("/risk")
def risk():
	weather_dir = home_dir + "weather.config"
	risk_dir = home_dir + "risk.config"
	weather_info = open(weather_dir, 'r').readline().split(",")
	output = float(open(risk_dir, 'r').readline())
	
	base_risk = 0.0

	if output < 0.01:
		base_risk = 1.0
	elif output > 0.01 and output <= 0.02:
		base_risk = 2.0
	elif output > 0.02 and output <= 0.025:
		base_risk = 3.0
	elif output > 0.025 and output <= 0.03:
		base_risk = 4.0
	elif output > 0.03:
		base_risk = 5.0

	risk_float = base_risk
	reasons = []

	if len(weather_info) > 5:
		max_mult = 0.0
		for alert in weather_info[5:]:
			curr_mult = alerts[alert]["mult"]
			if curr_mult > max_mult:
				max_mult = curr_mult
			reasons.append(alerts[alert]["desc"])
		risk_float = risk_float * max_mult

	risk = ""

	if risk_float >= 1.0 and risk_float < 2.0:
		risk = "MINIMAL"
	elif risk_float >= 2.0 and risk_float < 3.0:
		risk = "LOW"
	elif risk_float >= 3.0 and risk_float < 4.0:
		risk = "MEDIUM"
	elif risk_float >= 4.0 and risk_float < 5.0:
		risk = "HIGH"
	elif risk_float >= 5.0:
		risk = "EXTREME"

	return jsonify(risk=risk,reasons=reasons)

@app.route("/current_weather")
def weather():
	weather_dir = home_dir + "weather.config"
	weather_info = open(weather_dir, 'r').readline().split(",")
	return jsonify(high=weather_info[0], low=weather_info[1], status=weather_info[2], wind_speed=weather_info[3], wind_dir=weather_info[4])

@app.route("/data")
def data():
    return "Hello World!"

if __name__ == "__main__":
	app.debug = True
	app.run()
