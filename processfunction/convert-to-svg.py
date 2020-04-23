# -*- coding: utf-8 -*-
import sys
from io import StringIO, BytesIO
from PIL import Image
import boto3
import logging
import json

logger = logging.getLogger("handler_logger")
logger.setLevel(logging.DEBUG)

def svg_header(width, height):
    return """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="%d" height="%d"
     xmlns="http://www.w3.org/2000/svg" version="1.1">
""" % (width, height)

def rgba_image_to_svg_pixels(im):
    opaque=True
    s = StringIO()
    s.write(svg_header(*im.size))

    xcounter=0

    width, height = im.size
    for x in range(width):
        xcounter+=1
        for y in range(height):
            here = (x, y)
            rgba = im.getpixel(here)
            if opaque and not rgba[3]:
                continue
            s.write("""  <rect x="%d" y="%d" width="1" height="1" style="fill:rgb%s; fill-opacity:%.3f; stroke:none;" />\n""" % (x, y, rgba[0:3], float(rgba[3]) / 255))
        currentpercent = (xcounter / width) * 100
        currentpercent = str(currentpercent) + "%"
        logger.info(currentpercent)
        #print(currentpercent)

    s.write("""</svg>\n""")
    return s.getvalue()


def convert_to_svg(filedata):
    try:
        im = Image.open(BytesIO(filedata))
    except IOError as e:
        logger.error("error in convert_to_svg")
        logger.error(e)
        sys.exit(1)
    im_rgba = im.convert('RGBA')

    return rgba_image_to_svg_pixels(im_rgba)


def cleanupfunction(bucket_name,file_name):
    s3_client = boto3.client('s3')
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=file_name)
    except Exception as e:
        logger.error("Error in cleanupfunction")
        logger.error(e)


def handler(event, context):
    statuscode=200
    bodydata=""
    try:
        logger.info(event)
        bucket_name=event.get('bucketName')
        logger.info("Bucket name is:")
        logger.info(bucket_name)
        file_name=event.get('fileName')
        logger.info("File name is: ")
        logger.info(file_name)
        s3_client=boto3.client('s3')
        try:
            try:
                s3_object_content = s3_client.get_object(Bucket=bucket_name, Key=file_name)['Body'].read()
            except Exception as objectcontenterror:
                logger.error("object content error")
                logger.error(objectcontenterror)
                cleanupfunction(bucket_name,file_name)
                bodydata = json.dumps({
                    'successcode': '2'
                })
            try:
                cleanupfunction(bucket_name,file_name)
                s3resource=boto3.resource('s3')
                s3resource.Bucket(bucket_name).put_object(Key=file_name,Body=(convert_to_svg(s3_object_content)))
                bodydata = json.dumps({
                    'successcode': '1'
                })
            except Exception as uploaderror:
                logger.error("upload error")
                logger.error(uploaderror)
                cleanupfunction(bucket_name,file_name)
                bodydata = json.dumps({
                    'successcode': '2'
                })


        except Exception as e:
            cleanupfunction(bucket_name,file_name)
            logger.error(e)
            bodydata=json.dumps({
                'successcode': '2'
            })
    except Exception as loaderror:
        logger.error("Error in getting bucket name or filename")
        logger.error(loaderror)
        bodydata = json.dumps({
            'successcode': '0'
        })
    finalresponse={}
    finalresponse["headers"]={
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
    }
    finalresponse['statusCode']=statuscode
    finalresponse['body']=bodydata
    return finalresponse
