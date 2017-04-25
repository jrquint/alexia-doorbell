## Create new Lambda Function for each Known guest in the format Greet_[name]

from __future__ import print_function
import boto3
import json
from urlparse import urljoin
from urllib import urlencode
import urllib2 as urlrequest
#lambda_function.lambda_handler
def lambda_handler(event, context):
    #Set Dynamo DB Table location and name
    dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
    table = dynamodb.Table('faces')
    #Set Guest Name
    guest = 'Brendan'
    #Set Custom Greeting
    greeting = 'Good Morning, ' + guest + '! How was your train ride?'

    try:
        response = table.get_item(
            Key={
                'name': guest
            }
        )
        print('response ' + str(response))
    except:
        print(guest + " Not Found")
    else:
        if 'Item' in response:
            #item = response['Item']

            print(guest + " Found")

            #Set Slack API URL
            slack = Slack(url='https://hooks.slack.com/services/xxxx')
            table = dynamodb.Table('guests')
            table.put_item(
             Item={
               'guest': guest,
               'greeting': greeting
            }
            )

            slack.notify(text='Good Morning, ' + guest )
            table = dynamodb.Table('faces')
            table.delete_item(
                Key={
                    'name': guest
                    }
            )
        else:
            print ("Face Not Found")



class Slack():

    def __init__(self, url=""):
        self.url = url
        self.opener = urlrequest.build_opener(urlrequest.HTTPHandler())

    def notify(self, **kwargs):
        """
        Send message to slack API
        """
        return self.send(kwargs)

    def send(self, payload):
        """
        Send payload to slack API
        """
        payload_json = json.dumps(payload)
        data = urlencode({"payload": payload_json})
        req = urlrequest.Request(self.url)
        response = self.opener.open(req, data.encode('utf-8')).read()
        return response.decode('utf-8')
