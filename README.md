# API Serverless
> REST API developed entirely in Python and based on AWS cloud services. Uses AWS Lambda to run your application code without managing servers, Amazon API Gateway to expose the API over HTTP, Amazon DynamoDB to store and manage application data, and Amazon CloudWatch to monitor and debug performance and application functionality. Serverless architecture allows developers to focus on application development rather than infrastructure management, resulting in reduced costs, greater scalability, and faster deployment. Additionally, by using AWS cloud services, your application benefits from the security and reliability of a proven, high-performance platform.
>
> ![API-Serverless](https://th.bing.com/th/id/OIG4.JpN4AjvdNISX0KEIi2Sz?w=270&h=270&c=6&r=0&o=5&pid=ImgGn)

## First Steps
1. Create a New IAM Role with the following polices:
 - CloudWacthFullAcces (to access AWS CloudWatch)
 - AmazonDynamoDBFullAccess (to manage DynamoDB tables and items).

2. Create a New Lambda Function with the following configuration:

 • Author from scratch
 • Runtime: Python 
 • Execution Role with the new IAM Role was created in step one.
 • Memory 500MB
 • Timeout 1 Min.

3. Create a New Data Base in Amazon DynamoDB with `Partition Key: productID`

4. Create a New REST API using Amazon API Gateway with the following configurations:
 • Endpoint Type: Regional
 • Resources (all with enabled API Gateway CORS and Integrated with Lambda Function was created in step two) with the following methods:
   ```
   /health
     GET 
     OPTIONS
   /product
     DELETE
     GET
     OPTIONS
     PATCH
     POST
   /products
     GET
     OPTIONS
   ```

5. Replace the code in  your lambda function with the content of [lambda_function.py](./lambda_function.py) file.

6. Create a new file named custom_encoder.py in your lambda function folder, copy & paste the code provided below into [custom_encoder.py](./custom_encoder.py) file

> [!NOTE]
> If everything is working correctly, when accessing the API invocation URL, for example: https://mtp9f7cdta3.execute-api.us-east-1.amazonaws.com/your_stage_name/health returned with Status Code 200
