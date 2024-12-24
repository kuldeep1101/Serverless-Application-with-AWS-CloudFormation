# Serverless-Application-with-AWS-CloudFormation
Serverless Application: Greeting App with AWS CloudFormation

This document provides detailed documentation for the creation of a serverless application using AWS services. It leverages Infrastructure as Code (IaC) principles to provision resources through CloudFormation. The application takes a user’s name as input and responds with a greeting message. The architecture leverages a variety of AWS components including VPC, IAM roles, Lambda, S3, RDS, API Gateway, and others.


## Project Breakdown

### Stack 1: Core Infrastructure Provisioning

Resources Provisioned: VPC, IAM Role, S3 Bucket, S3 Bucket Policy, Internet Gateway.

Highlights:

- VPC: Allocated IP range 10.0.0.0/16 for private networking.

- IAM Role: Provides permissions to access S3, RDS, and networking interfaces.

- S3 Bucket: Stores the zipped Lambda function code.

- Internet Gateway: Facilitates external access to VPC resources.

### Stack 2: Compute and Database Resources

Resources Provisioned: Subnets, Security Group, RDS Instance, Lambda Function, NAT Gateway, Elastic IP.

Highlights:

- Subnets: Defined subnets for application tiers.

- Security Group: Allows TCP traffic on port 3306 for RDS.

- RDS Instance: MySQL database instance db-instance-1 with credentials.

- Lambda Function: Executes the greeting logic and interacts with RDS.

- NAT Gateway: Allows private subnets to access the internet securely.

### Stack 3: API Gateway

Resources Provisioned: API Gateway, Resources, Method, Deployment.

Highlights:

- API Gateway: REST API named MyServerlessAppAPI.

- Resource: /submit-name endpoint to accept POST requests.

- Integration: Connects API Gateway to Lambda with AWS_PROXY.

- Outputs: Provides the API endpoint URL.

### Lambda Function Code

The Lambda function interacts with RDS to store user information and return a greeting message.

    import json
    import pymysql
    
    # Database configuration
    rds_host = "db-instance-1.cbw6ga2km5bl.ap-south-1.rds.amazonaws.com"
    db_username = "root"
    db_password = "********"
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
            connection.close()'''


### Outputs

1. Stack 1 Outputs:

- IAM Role ARN: s3-MyIAMRole

- VPC ARN: s3-MyVPC1

- S3 Bucket ARN: s3-MyBucketSL1

2. Stack 2 Outputs:

- Lambda ARN: Lambda-ref

3. Stack 3 Outputs:

- API Gateway Endpoint: https://${MyApiGateway}.execute-api.${AWS::Region}.amazonaws.com/prod/submit-name

### Deployment Steps

1. Package Lambda Function:
- Zip the Python function code and dependencies (e.g., pymysql) into lambda_function_sl.zip.
2. Upload to S3 Bucket created in Stack 1.
3. Deploy CloudFormation Stacks:
- Execute Stack 1, followed by Stack 2, and then Stack 3.
4. Configured AWS Lambda to connect with the RDS database.

### Test API Endpoint:

Use a REST client (e.g., postman) to send a POST request to the API Gateway endpoint with name parameter.

**API URL** - https://pn72zqdjkb.execute-api.ap-south-1.amazonaws.com/prod/submit-name

![Testing Serverless Application](https://raw.githubusercontent.com/kuldeep1101/Serverless-Application-with-AWS-CloudFormation/master/Testing%20-%20Serverless%20Application.gif)

## Conclusion

This serverless application demonstrates AWS CloudFormation’s capabilities in provisioning and managing resources efficiently. The modular stack-based approach ensures scalability, security, and maintainability.
