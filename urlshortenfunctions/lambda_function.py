import boto3
import os
import json
import decimal
from string import ascii_letters, digits

#environmental variables
my_domain = os.getenv('MY_DOMAIN')
region = os.getenv('REGION')

#62 letters from a-zA-Z0-9
string_62 = ascii_letters + digits

def changeBase(n,b):
    
    '''
    converting a decimal based number to 62 base
    n: int, a decimal based number
    b: int, new base, set b=62 for 62 base
    return: string
    '''
    
    x,y = divmod(n,b)
    if x>0:
        return changeBase(x,b) + string_62[y]
    else:             
        return string_62[y]

def url_shorten(event, context):
    
    '''
    associate each decimal time with a unique 62 base letter
    increase decimal time by 1 every time when generating a unique 62 base letter
    store the unique 62 base letter along with the user-provided long url into AWS dynamodb
    return: dict
    '''
    
    #get lattest id
    try:
        lattest_ddb = boto3.resource('dynamodb', region_name = region).Table('lattest_id_for_url_shortener_table')
        response = lattest_ddb.get_item(Key={'lattest': 'lattest'})
        counts = int(response.get('Item').get('counts',0))    #another possible way is self keys increase in database, global variables and decoration will not work!

        ddb = boto3.resource('dynamodb', region_name = region).Table('url_shortener_table')
        Url = event['url']       #get long url
        TinyId = changeBase(counts,62)       #Tiny id
        shorturl = my_domain + TinyId       #short url

        response = ddb.put_item(
            Item={
                'TinyId': TinyId,
                'Url': Url,
            }
        )
    except Exception as e:
        print('something wrong when getting long url',e)
    else:
        return{
        "statusCode": 200,
        "body": shorturl
        }


def url_direct(event, context):
    
    ddb = boto3.resource('dynamodb', region_name = region).Table('url_shortener_table')
    TinyId = event['path'][1:]
    
    try:
        response = ddb.get_item(Key={'TinyId': TinyId})
        Url = response.get('Item').get('Url')
    except:
        return {
            "statusCode": 301,
            "message": "Sorry there was something wrong, please check your link's availability"
        }
    
    return {
        "statusCode": 301,
        "body": '',
        "headers":{
            "Location": Url
        }
    }


def lattest_id_increment(event,context):
    '''
    involke counts increase by 1 every time storing a new item to url_shortener_table
    '''
    
    try:
        dynamodb = boto3.resource('dynamodb', region_name = region)
        table = dynamodb.Table('lattest_id_for_url_shortener_table')

        lattest = "lattest"

        response = table.update_item(
            Key={
            'lattest': lattest,
            },
            UpdateExpression="set counts = counts + :val",
            ExpressionAttributeValues={
            ':val': decimal.Decimal(1)
            },
            ReturnValues='UPDATED_NEW'
            )
    except Exception as e:
        print(e)
    else:
        print("UpdateItem succeeded:")


def lambda_handler(event,context):
    if event.get('url'):      # url for post method exists, then run url_shorten
        response = url_shorten(event, context)
        lattest_id_increment(event,context)     # add counts by 1, stort it in supplementary DynamoDB Table
        return response
    elif event.get('path'):     # short url path parameters are passed by
        return url_direct(event, context)
