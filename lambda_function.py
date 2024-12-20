import json
import pymysql

# Database configuration
rds_host = "db-instance-1.cbw6ga2km5bl.ap-south-1.rds.amazonaws.com"
db_username = "root"
db_password = "root8440"
db_name = "db-instance-1"

def lambda_handler(event, context):
    connection = pymysql.connect(host=rds_host, user=db_username,
                                 password=db_password, database=db_name)
    try:
        name = event.get('queryStringParameters', {}).get('name', 'Guest')
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO users (name) VALUES (%s)", (name,))
            connection.commit()

        message = f"Hi {name}, Hope you are doing well!"
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"message": message})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
    finally:
        connection.close()