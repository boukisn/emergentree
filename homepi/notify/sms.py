import boto3
import sys

sns = boto3.client('sns')

with open(sys.argv[1], "r") as ins:
    array = []
    for line in ins:
        array.append(line)


number = array[0]
message = array[1]

sns.publish(PhoneNumber = array[0], Message = array[1])
