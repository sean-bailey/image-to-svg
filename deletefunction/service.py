# -*- coding: utf-8 -*-
import boto3
from datetime import datetime

#delete everything not index.html which is older than 15 mins

s3=boto3.client('s3')

bucket_name=os.environ['bucket_name']
def handler(event, context):
    # Your code goes here!
    bucketobjects = s3.list_objects(Bucket=bucket_name)
    for objects in bucketobjects['Contents']:
        currenttime=datetime.now()
        if not objects["Key"]endswith('.html'):
            objectdate=objects["LastModified"].replace(tzinfo=None)
            currentdelta=currenttime-objectdate
            if currentdelta.seconds > 900:
                print("deleting "+objects["Key"])
                s3.delete_object(
                Bucket=bucket_name,
                Key=objects["Key"])
                )
