import boto3
import random, os
from string import ascii_letters, digits

#environmental variables
my_domain = os.getenv('MY_DOMAIN')
region = os.getenv('REGION')

#62 letters from a-zA-Z0-9
string_62 = ascii_letters + digits


def url_shorten(event, context):
    
    '''
    associate each decimal time with a unique 62 base letter
    increase decimal time by 1 every time when generating a unique 62 base letter
    store the unique 62 base letter along with the user-provided long url into AWS dynamodb
    return: dict
    '''
    
    #get lattest id
    try:
        ddb = boto3.resource('dynamodb', region_name = region).Table('url_shortener_table')
        Url = event['url']       #get long url
        TinyId = ''.join([str(i) for i in random.choices(string_62,k=4)])      #Tiny id
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

if __name__ == '__main__':
    pass
