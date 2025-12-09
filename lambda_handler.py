import boto3
import json

# Define the DynamoDB table that Lambda will connect to
table_name = "Emp_Master"

# Create the DynamoDB resource
dynamo = boto3.resource('dynamodb').Table(table_name)

def api_response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }


# Define some functions to perform the CRUD operations
def create(body):
    try:
        response = dynamo.put_item(Item=body)
        if(response['ResponseMetadata']['HTTPStatusCode'] == 200):
            return api_response(
                200, 
                {'message': f"Employee {body['Emp_id']} created successfully"}
            )
        else:
            return api_response(
                400,
                {'message': f"Employee {body['Emp_id']} creation failed"}
            )
            
    except Exception as e:
        return api_response(
            500,
            {'message': f"Error: {str(e)}"}
        )
        

def read(emp_id):
    try:
        response = dynamo.get_item(Key=emp_id)
        
        if 'Item' in response:
            return api_response(
                200,
                response['Item']
            )
            
        else:
            return api_response(
                400,
                {'message': f"Employee {emp_id} not found"}
            )
            
    except Exception as e:
        return api_response(
            500,
            {'message': f"Error: {str(e)}"}
        )

def lambda_handler(event, context):   
    method = event.get('httpMethod', {})

    if method == 'POST':
        body = event.get('body', '{}')
        try:
            print("Inside Post method try")
            body = json.loads(body)
            response = dynamo.put_item(Item=body)
        except Exception as e:
            return api_response(
                400,
                {'message': f"Error: {str(e)}"}
            )

        if "Emp_id" not in body:
            return api_response(
                400,
                {'message': f"Error: Emp_id is required"}
            )
        return create(body)

    elif method == 'GET':
        param = event.get('queryStringParameters', None)
        if not param.get('Emp_id'):
            return api_response(
                400,
                {'message': f"Error: Emp_id is required"}
            )
        return read(param)
    
    else:
        return api_response(
            400,
            {'message': f"Unrecognized operation: '{method}'"}
        )
