import boto3

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

if __name__ == '__main__':
    pass
