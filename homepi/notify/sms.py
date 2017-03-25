import boto3
import sys
import re
import sched
import time
import RPi.GPIO as GPIO


Buzzer = 4 # whatever pin on the Pi


def setup(pin):
	global BuzzerPin
	BuzzerPin = pin
	GPIO.setmode(GPIO.BOARD) # Numbers GPIOs by physical location
	GPIO.setup(BuzzerPin, GPIO.OUT)
	GPIO.output(BuzzerPin, 0)

def on():
	GPIO.output(BuzzerPin, 1)

def off():
	GPIO.output(BuzzerPin, 0)

def destroy():
	GPIO.output(BuzzerPin, 0)
	GPIO.cleanup() # Release resource



sns = boto3.client('sns')

#with open(sys.argv[1], "r") as ins:
#    array = []
#    for line in ins:
#        array.append(line)

#number = array[0]
#message = array[1]

sms_message = False
gpio_alarm = False

s = sched.scheduler(time.time, time.sleep)


def severity_checker(sc,sms_message,gpio_alarm,sns):

#Do this shit every minute

	f = open('serverity.log', "r")
	severity_info = f.readlines()
	f.close()

	severity_info = severity_info[0]
	pattern = re.compile("^\s+|\s*,\s*|\s+$")
	severity_array = [x for x in pattern.split(severity_info) if x]
	severity_number = float(severity_array[0])
	severity_flag = severity_array[1] 

	#Open the phone number/message file
	g = open('phone_config.log',"r")
	phone_configuration = g.readlines()
	g.close()

	phone_configuration_info = phone_configuration[0]
	pattern_2 = re.compile("^\s+|\s*,\s*|\s+$")
	phone_configuration_array = [x for x in pattern_2.split(phone_configuration_info) if x]
	phone_number = phone_configuration_array[0]


	if (severity_flag == "EXTREME"):
		#do the text message
		if (gpio_alarm == False):
			#Turn on the sound
			on()
			gpio_alarm = True
		if(sms_message == False):
			sns.publish(PhoneNumber = phone_number, Message = 'Howdy')
			sms_message = True	
		
		print "FUCK!"

	elif (severity_flag == "HIGH"):
		#do the text message
		if(sms_message == False):
			sns.publish(PhoneNumber = phone_number, Message = 'Howdy')
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

	s.enter(5, 1, severity_checker, (sc,sms_message,gpio_alarm,sns))


#Have main function that will not only set up GPIO
#But also start the loop

setup(Buzzer)
s.enter(5, 1, severity_checker, (s,sms_message,gpio_alarm,sns))
s.run()			

#except KeyboardInterrupt:
#	destroy()

