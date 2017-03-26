import boto3
import sys

# Let's use Amazon S3
s3 = boto3.resource('s3',aws_access_key_id='AKIAJDUDA4LPBJRHNTXA',
         aws_secret_access_key='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')



# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)

#TODO: Make error handling
file_name = sys.argv[1]
file_to_upload = sys.argv[1]

# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)
# print sys.argv[1]


# Assumes bucket already exists
data = open(file_to_upload, 'rb')
s3.Bucket('buteamfourteen').put_object(Key=file_to_upload, Body=data)
