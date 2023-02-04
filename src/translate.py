import boto3
import todoList


def translate(event, context):
    client = boto3.client('comprehend')
    item = todoList.get_item(
        event['pathParameters']['id']
    )
    if item:
        itemText = item['text']
        comprehendResponse = client.detect_dominant_language(
            Text=itemText
        )
        itemTextLangCode = comprehendResponse['Languages'][0]['LanguageCode']

        response = {
            "statusCode": 200,
            "body": itemTextLangCode
        }
    else:
        response = {
            "statusCode": 404,
            "body": "An error occurred while translating the text"
        }
    return response
