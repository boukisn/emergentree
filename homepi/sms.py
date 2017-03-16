import boto3

sns = boto3.client('sns')
number = '+15856430318'
sns.publish(PhoneNumber = number, Message='Tree Update: It is about to fall lol' )