import boto3
import sys
import os.path

# Let's use Amazon S3
s3 = boto3.resource('s3')

# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)

#TODO: Make error handling

file_to_download = sys.argv[1]

# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)
# print sys.argv[1]

s3.Bucket('buteamfourteen').download_file(file_to_download, sys.argv[2])
print sys.argv[2]
writefile = open("/home/pi/emergentree/homepi/frontend/server/connection.log","w+")
writefile.write("True")
writefile.close()
"""except:
	writefile = open("/home/pi/emergentree/homepi/frontend/server/connection.log","w+")
	writefile.write("False")
	writefile.close()"""

