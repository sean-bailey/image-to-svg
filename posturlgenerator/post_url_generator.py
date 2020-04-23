# -*- coding: utf-8 -*-
import os
import boto3
import logging
import json

logger = logging.getLogger("handler_logger")
logger.setLevel(logging.DEBUG)

def handler(event, context):
    statuscode=200
    bodydata=None
    try:
        file_name = event.get('fileName')
        operation_type=event.get('operation')
        bucket_name=os.environ['bucket_name']
        timeout=int(os.environ['expire_time'])
        s3=boto3.client('s3')
        if operation_type=="upload":

            bodydata=json.dumps({
                'returndata' : s3.generate_presigned_post(Bucket=bucket_name,Key=file_name,ExpiresIn=timeout),
                #'returndata':{
                #'url':s3.generate_presigned_url(ClientMethod="put_object",Params={'Bucket':bucket_name,'Key':file_name}, ExpiresIn=30,HttpMethod="POST")
                #},
                'successcode':'0'
            })
        else:
            bodydata= json.dumps({
                'returndata' : s3.generate_presigned_url('get_object',
                                             Params={'Bucket':bucket_name,
                                                     'Key': file_name},
                                             ExpiresIn=3600),
                'successcode':'1'
            })
    except Exception as e:
        logger.error(e)
        bodydata = json.dumps({
        'returndata':"",
            'successcode': '2'
        })


    finalresponse={}
    finalresponse["headers"]={
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
    }
    finalresponse['statusCode']=statuscode
    finalresponse['body']=bodydata
    return finalresponse
