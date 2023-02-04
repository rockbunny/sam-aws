import json
import boto3
import decimalencoder
import todoList

def translate(event, context):

    client = boto3.client('comprehend')

    item = todoList.get_item(event['pathParameters']['id'])

    if item:

        itemText = item['text']
        comprehendResponse = client.detect_dominant_language(Text=itemText)
        itemTextLanguageCode = comprehendResponse['Languages'][0]['LanguageCode']

        response = {
            "statusCode": 200,
            "body": itemTextLanguageCode
        }

    else:

        response = {
            "statusCode": 404,
            "body": "An error occurred while translating the text"
        }

    return response
