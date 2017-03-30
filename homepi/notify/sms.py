import boto3
import sys
import re
import sched
import time
import RPi.GPIO as GPIO


Buzzer = 7 # whatever pin on the Pi
home_dir = "/home/pi/emergentree/homepi/frontend/server/"
severity_file = home_dir + "risk.config"
settings_file = home_dir + "settings.config"

def setup(pin):
	global BuzzerPin
	BuzzerPin = pin
	GPIO.setmode(GPIO.BOARD) # Numbers GPIOs by physical location
	GPIO.setup(BuzzerPin, GPIO.OUT)
	GPIO.output(BuzzerPin, 1)

def on():
	GPIO.output(BuzzerPin, 0)

def off():
	GPIO.output(BuzzerPin, 1)
	
def beep_three(flag):
	if flag:
		on()
		time.sleep(1.0)
		off()
		time.sleep(1.0/2.0)
		on()
		time.sleep(1.0)
		off()
		time.sleep(1.0/2.0)
		on()
		time.sleep(1.0)
		off()
		time.sleep(1.0/2.0)
	
def beep_once(x):
	on()
	time.sleep(x)
	off()
	
	
def destroy():
	GPIO.output(BuzzerPin, 1)
	GPIO.cleanup() # Release resource

def send_sms(sns, phone, alert_type, flag):
	if flag:
		message = 'EmergenTree Alert!\n\nYour tree is at ' + alert_type +' risk of potentially causing damage.'
		sns.publish(PhoneNumber = phone, Message = message)

#Add these manually :/
#Or else Amazon will call you out
#sns = boto3.client('sns',aws_access_key_id='...',
#aws_secret_access_key='...')

sns = boto3.client('sns')

#with open(sys.argv[1], "r") as ins:
#    array = []
#    for line in ins:
#        array.append(line)

#number = array[0]
#message = array[1]

extreme_flag = False
high_flag = False
sms_message = False
gpio_alarm = False
last = "MINIMAL"

s = sched.scheduler(time.time, time.sleep)


def severity_checker(s, extreme_flag, high_flag, sms_message, gpio_alarm, last, sns):

#Do this shit every minute

	f = open(severity_file, "r")
	severity_info = f.readlines()
	f.close()

	severity_info = severity_info[0]
	pattern = re.compile("^\s+|\s*,\s*|\s+$")
	severity_array = [x for x in pattern.split(severity_info) if x]
	severity_number = float(severity_array[0])
	severity_flag = severity_array[1] 

	#Open the phone number/message file
	g = open(settings_file,"r")
	phone_configuration = g.readlines()
	g.close()

	phone_configuration_info = phone_configuration[0]
	pattern_2 = re.compile("^\s+|\s*,\s*|\s+$")
	phone_configuration_array = [x for x in pattern_2.split(phone_configuration_info) if x]
	phone_number = phone_configuration_array[0]

	alert_type = ""

	# State machine
	if (last != "EXTREME" and last != "HIGH") and (severity_flag == "EXTREME"):
		extreme_flag = True
		high_flag = False
		sms_message = True
		gpio_alarm = True
		alert_type = "EXTREME"
		last = severity_flag
	elif (last != "EXTREME" and last != "HIGH") and (severity_flag == "HIGH"):
		extreme_flag = False
		high_flag = True
		sms_message = True
		gpio_alarm = False
		alert_type = "HIGH"
		last = severity_flag
	elif (last != "EXTREME" and last != "HIGH") and (severity_flag != "EXTREME" and severity_flag != "HIGH"):
		extreme_flag = False
		high_flag = False
		sms_message = False
		gpio_alarm = False
		last = severity_flag
	elif (last == "EXTREME") and (severity_flag == "EXTREME"):
		extreme_flag = True
		high_flag = False
		sms_message = False
		gpio_alarm = False
		last = severity_flag
	elif (last == "EXTREME") and (severity_flag == "HIGH"):
		extreme_flag = False
		high_flag = True
		sms_message = True
		gpio_alarm = False
		alert_type = "HIGH"
		last = severity_flag
	elif (last == "EXTREME") and (severity_flag != "EXTREME" and severity_flag != "HIGH"):
		extreme_flag = False
		high_flag = False
		sms_message = False
		gpio_alarm = False
		last = severity_flag
	elif (last == "HIGH") and (severity_flag == "EXTREME"):
		extreme_flag = True
		high_flag = False
		sms_message = True
		gpio_alarm = True
		alert_type = "EXTREME"
		last = severity_flag
	elif (last == "HIGH") and (severity_flag == "HIGH"):
		extreme_flag = False
		high_flag = True
		sms_message = False
		gpio_alarm = False
		last = severity_flag
	elif (last == "HIGH") and (severity_flag != "EXTREME" and severity_flag != "HIGH"):
		extreme_flag = False
		high_flag = False
		sms_message = False
		gpio_alarm = False
		last = severity_flag

	print "Extreme: " + extreme_flag
	print "High: " + high_flag
	beep_three(gpio_alarm)
	send_sms(sns, phone_number, alert_type, sms_message)

	s.enter(60, 1, severity_checker, (s, extreme_flag, high_flag, sms_message, gpio_alarm, last, sns))


#Have main function that will not only set up GPIO
#But also start the loop

setup(Buzzer)
try:
	s.enter(60, 1, severity_checker, (s, extreme_flag, high_flag, sms_message, gpio_alarm, last, sns))
	s.run()	
	
except (KeyboardInterrupt, SystemExit):
	destroy()
	sms_message = False
	gpio_alarm = False
	extreme_flag = False

