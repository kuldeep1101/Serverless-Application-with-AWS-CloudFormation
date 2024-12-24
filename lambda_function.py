import json
import pymysql

# Database configuration
rds_host = "db-instance-1.cbw6ga2km5bl.ap-south-1.rds.amazonaws.com"
db_username = "root"
db_password = "root8440"
db_name = "db_instance_sl"

def lambda_handler(event, context):
    connection = pymysql.connect(host=rds_host, 
                                 user=db_username,
                                 password=db_password, 
                                 database=db_name,
                                 connect_timeout=10)
    try:
        # Check if the 'users' table exists, create if it does not
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.commit()
        
        # Get the 'name' parameter from the query string, default to 'Guest'
        name = event.get('queryStringParameters', {}).get('name', 'Guest')
        
        # Insert into the users table (for demonstration purposes)
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO users (username) VALUES (%s)", (name,))
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
