import boto3
import os
import json
from url_shorten import url_shorten
from url_direct import url_direct

#environmental variables
my_domain = os.getenv('MY_DOMAIN')
region = os.getenv('REGION')

def lambda_handler(event,context):
    if event.get('url'):      # url for post method exists, then run url_shorten
        response = url_shorten(event, context)
        return response
    elif event.get('path'):     # short url path parameters are passed by
        return url_direct(event, context)