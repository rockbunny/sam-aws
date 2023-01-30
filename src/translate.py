import json
import boto3
import decimalencoder
import todoList


def get(event, context):
    # create a response
    item = todoList.get_item(event['pathParameters']['id'])
    if item:
        
        comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
        
        language = comprehend.detect_dominant_language(
            Text = item.text,
            sort_keys=True,
            indent=4
        )

        translate = boto3.client(
            service_name='translate',
            region_name='us-east-1',
            use_ssl=True
        )
        result = translate.translate_text(
            Text=item.text,
            SourceLanguageCode=language,
            TargetLanguageCode=event['pathParameters']['language'],
        )
        response = {
            "statusCode": 200,
            "body": json.dumps(
                item,
                cls=decimalencoder.DecimalEncoder
            )
        }
    else:
        response = {
            "statusCode": 404,
            "body": "An error occurred while translating the text"
        }
    return response
