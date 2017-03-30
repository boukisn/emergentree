from flask import Flask, jsonify, render_template, request
import os

app = Flask(__name__)

alerts_dict={"HUW":5.0, "EQW":5.0, "TSW":5.0, "HUA":5.0, "TSA":5.0, "TRW":5.0, "TRA":1.5, "EWW":5.0, "TOR":1.6837404737707237, "FRW":1.3, "TOA":1.34187023688, "SVR":1.06731415302, "HWW":1.10526162097427432, "BZW":1.0705579451455787, "SVA":1.03365707651, "HWA":1.05263081048, "WSW":1.028944960089230676, "CFW":1.2661422233501, "FLW":1.02, "WSA":1.01447248004, "CFA":1.13307111167, "FLA":1.01}

root_dir = "/home/pi/emergentree/"
home_dir = root_dir + "homepi/frontend/server/"
root_weather_dir = root_dir + "homepi/weather/"

# For cache busting
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route("/")
def home():
	return render_template('index.html')

@app.route("/report")
def report():
	return render_template('report.html')

@app.route("/risk")
def risk():
	weather_dir = root_weather_dir + "advisories.log"
	risk_dir = home_dir + "risk.config"
	risk_value_dir = home_dir + "risk_value.config"
	weather_info = open(weather_dir, 'r').readline().split(",")
	output_file = open(risk_dir, 'r')
	output = float(output_file.readline().split(",")[0])
	output_file.close()
	
	base_risk = 0.0

	if output < 0.005:
		base_risk = 1.0
	elif output >= 0.005 and output <= 0.010:
		base_risk = 2.0
	elif output > 0.010 and output <= 0.015:
		base_risk = 3.0
	elif output > 0.015 and output <= 0.02:
		base_risk = 4.0
	elif output > 0.02:
		base_risk = 5.0

	risk_float = base_risk
	reasons = []

	"""
	if len(weather_info) > 5:
		max_mult = 0.0
		for alert in weather_info[5:]:
			curr_mult = alerts[alert]["mult"]
			if curr_mult > max_mult:
				max_mult = curr_mult
			reasons.append(alerts[alert]["desc"])
		risk_float = risk_float * max_mult
	"""

	if len(weather_info) == 2:
		risk_float = risk_float * alerts_dict[weather_info[0]]

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

	output_file_again = open(risk_value_dir, 'w')
	output_file_write_string = risk
	output_file_again.write(output_file_write_string)

	return jsonify(risk=risk,reasons=reasons)

@app.route("/current_weather")
def weather():
	weather_dir = home_dir + "weather.config"
	weather_info = open(weather_dir, 'r').readline().split(",")
	return jsonify(high=weather_info[0], low=weather_info[1], status=weather_info[2], wind_speed=weather_info[3], wind_dir=weather_info[4])

@app.route("/data")
def data():
	data_dir = home_dir + "output.log"
	data_array = []
	for line in open(data_dir, 'r').readlines():
		data_array.append(line[:-1])
	latest_value = data_array[-1]
	return jsonify(latest_value=latest_value,data=data_array)

@app.route("/angle")
def angle():
	angle_dir = home_dir + "angle.config"
	angle_info = open(angle_dir, 'r').readline().split(",")
	return jsonify(angle=angle_info[2])

@app.route('/tree_data', methods=['POST'])
def tree_data():
	tree_report_dir = home_dir + "tree_report.config"
	tree_values = "leaves=" + request.args.get("leaves") + "\nbark=" + request.args.get("bark") + "\nslimy_roots=" + request.args.get("slimy_roots") + "\nopen_wounds=" + request.args.get("open_wounds") + "\nfungus=" + request.args.get("fungus") + "\nbark_cracks=" + request.args.get("bark_cracks") + "\n"
	f = open(tree_report_dir, 'w')
	f.write(tree_values)
	f.close()
	return "done"

@app.route("/alerts")
def alerts():
	alerts_dir = home_dir + "alerts.config"
	alerts_list = open(alerts_dir, 'r').readlines()
	total_list = []
	for line in alerts_list:
		curr_dict = {}
		elements = line.split(",")
		curr_dict["type"] = elements[0]
		curr_dict["subject"] = elements[1]
		curr_dict["desc"] = elements[2][:-1]
		total_list.append(curr_dict)
	return jsonify(info=total_list)

@app.route("/alert_response", methods=['POST'])
def alert_response():
	alerts_dir = home_dir + "alerts.config"
	alerts_file_read = open(alerts_dir, 'r')
	alerts_list = alerts_file_read.readlines()
	alerts_file_read.close()
	alerts_list.pop(int(request.args.get("id")))
	alerts_file_write = open(alerts_dir, 'w')
	alerts_file_write.write(''.join(alerts_list))
	alerts_file_write.close()
	return "done"

@app.route('/get_tree_data')
def get_tree_data():
	tree_report_dir = home_dir + "tree_report.config"
	tree_file = open(tree_report_dir, 'r')
	tree_values = tree_file.readlines()
	fields = ["leaves","bark","slimy_roots","open_wounds","fungus","bark_cracks"]
	tree_values_dict = {}
	tree_values_dict["leaves"] = tree_values[0].split("=")[1][:-1];
	tree_values_dict["bark"] = tree_values[1].split("=")[1][:-1];
	tree_values_dict["slimy_roots"] = tree_values[2].split("=")[1][:-1];
	tree_values_dict["open_wounds"] = tree_values[3].split("=")[1][:-1];
	tree_values_dict["fungus"] = tree_values[4].split("=")[1][:-1];
	tree_values_dict["bark_cracks"] = tree_values[5].split("=")[1][:-1];
	tree_file.close()
	return jsonify(tree_values_dict)

@app.route('/settings', methods=['POST'])
def settings():
	settings_dir = home_dir + "settings.config"
	settings_values = "+1" + request.args.get("phone") + "," + request.args.get("date")
	f = open(settings_dir, 'w')
	f.write(settings_values)
	f.close()
	return "done"

@app.route('/get_settings')
def get_settings():
	settings_dir = home_dir + "settings.config"
	settings_file = open(settings_dir, 'r')
	settings_values = settings_file.readline().split(",")
	settings_dict = {}
	settings_dict["phone"] = settings_values[0][2:]
	settings_dict["date"] = settings_values[1]
	settings_file.close()
	return jsonify(settings_dict)

if __name__ == "__main__":
	app.debug = True
	app.run()
