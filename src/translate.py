import boto3
import todoList
import decimalencoder
import json


def translate(event, context):
    comprehendClient = boto3.client('comprehend')
    translateClient = boto3.client('translate')
    item = todoList.get_item(
        event['pathParameters']['id']
    )
    targetLangCode = event['pathParameters']['language']
    if item:
        itemText = item['text']
        comprehendResponse = comprehendClient.detect_dominant_language(
            Text=itemText
        )
        itemTextLangCode = comprehendResponse['Languages'][0]['LanguageCode']
        translate = translateClient.translate_text(
            Text=itemText,
            SourceLanguageCode=itemTextLangCode,
            TargetLanguageCode=targetLangCode
        )
        response = {
            "statusCode": 200,
            "body": json.dumps(translate, cls=decimalencoder.DecimalEncoder)
        }
    else:
        response = {
            "statusCode": 404,
            "body": "An error occurred while translating the text"
        }
    return response
