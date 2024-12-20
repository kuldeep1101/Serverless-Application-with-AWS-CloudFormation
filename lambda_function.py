import json

def lambda_handler(event, context):
    # Extract the name from the API Gateway event
    name = event.get('queryStringParameters', {}).get('name', 'Guest')
    
    # Generate a personalized message
    message = f"Hi {name}, Hope you are doing well!"
    
    # Return the response
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({"message": message})
    }