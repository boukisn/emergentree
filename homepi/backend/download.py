import boto3
import sys

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


# Assumes bucket already exists
s3.Bucket('buteamfourteen').download_file(file_to_download, sys.argv[2])
