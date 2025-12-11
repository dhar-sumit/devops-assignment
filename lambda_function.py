import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('lambda-dynamodb-stream')

def lambda_handler(event, context):
    detail = event["detail"]
    instance_id = detail["instance-id"]
    state = detail["state"]
    launch_time = event["time"]

    item = {
        'instance_id': instance_id,
        'instance_launch_time': launch_time,
        'instance_current_state': state
    }

    table.put_item(Item=item)

    return {"status": "ok"}
