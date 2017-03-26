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
	
def beep_three(x):
	on()
	time.sleep(x)
	off()
	time.sleep(x)
	on()
	time.sleep(x)
	off()
	time.sleep(x)
	on()
	time.sleep(x)
	off()
	time.sleep(x)
	
def beep_once(x):
	on()
	time.sleep(x)
	off()
	
	
def destroy():
	GPIO.output(BuzzerPin, 1)
	GPIO.cleanup() # Release resource



sns = boto3.client('sns',aws_access_key_id='AKIAJDUDA4LPBJRHNTXA',
aws_secret_access_key='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')

#with open(sys.argv[1], "r") as ins:
#    array = []
#    for line in ins:
#        array.append(line)

#number = array[0]
#message = array[1]

sms_message = False
gpio_alarm = False
extreme_flag = False

s = sched.scheduler(time.time, time.sleep)


def severity_checker(sc,sms_message,gpio_alarm,sns,extreme_flag):

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


	if (severity_flag == "EXTREME"):
		#do the alarm and text message
		if (gpio_alarm == False):
			#Turn on the sound
			if(extreme_flag == False):
				beep_three(2)
				extreme_flag = True
			else:
				beep_once(4)
			gpio_alarm = True
		if(sms_message == False):
			sns.publish(PhoneNumber = phone_number, Message = 'EmergenTree Alert!\n\nYour tree is at EXTREME risk of potentially causing damage.')
			sms_message = True	
		
		print "FUCK!"

	elif (severity_flag == "HIGH"):
		#do the text message
		if(sms_message == False):
			sns.publish(PhoneNumber = phone_number, Message = 'EmergenTree Alert!\n\nYour tree is at HIGH risk of potentially causing damage.')
			sms_message = True
		#should probably turn on the alarm if its going	
		if(gpio_alarm == True):
			off()
			gpio_alarm = False

	else:
		#Turn off the settings
		sms_message = False
		gpio_alarm = False
		off()
		print "lol"
		#turn off stuff

	s.enter(5, 1, severity_checker, (sc,sms_message,gpio_alarm,sns,extreme_flag))


#Have main function that will not only set up GPIO
#But also start the loop

setup(Buzzer)
try:
	s.enter(5, 1, severity_checker, (s,sms_message,gpio_alarm,sns,extreme_flag))
	s.run()	
	
except (KeyboardInterrupt, SystemExit):
	destroy()

