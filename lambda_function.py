import boto3
import json
import logging
from custom_encoder import CustomEncoder

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamo_tabe_name = 'YOUR_TABLE_NAME' 
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamo_tabe_name)

# Available Methods:
GetMethod = 'GET'
PostMethod = 'POST'
PatchMethod = 'PATCH'
DeleteMethod = 'DELETE'
HealthPath = '/health'
ProductPath = '/product'
ProductsPath = '/products'

def lambda_handler(event, context):
    logger.info(event)

    HTTPMethod = event['httpMethod']
    path = event['path']

    if HTTPMethod == GetMethod and path == HealthPath:
        response = Response(200, body = {'message': 'Health check passed'})

    elif HTTPMethod == GetMethod and path == ProductPath:
        response = getProduct(event['queryStringParameters']['productID'])

    elif  HTTPMethod == GetMethod and path == ProductsPath:
        response = getProducts()

    elif HTTPMethod == PostMethod and path == ProductPath:
        data = json.loads(event['body'])
        response = saveProduct(data)

    elif  HTTPMethod == PatchMethod and path == ProductPath:
        data = json.loads(event['body'])
        response = modifyProduct(data['productID'], data['updateKey'],  data['updateValue'])

    elif  HTTPMethod == DeleteMethod and path == ProductPath:
        data = json.loads(event['body'])
        response = deleteProduct(data['productID'])
    
    else:
        response = Response(404, 'Method Not Found')

    return response

def Response(status_code, body=None):
    response = {
        "isBase64Encoded": False,
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }

    if body is not None:
        response['body'] = json.dumps(body, cls=CustomEncoder)

    return response

# Get a specific product
def getProduct(productId):
    try:
        result = table.get_item(
            Key = {
                'productID': productId
            }
        )

        if 'Item' in result:
            return Response(200, result['Item'])
        
        else:
            return Response(404, {'Message': f'ProductID search: {productId} not found'})

    except ValueError as ve:
        logger.exception(f"An error occurred while fetching the item: {ve}")
        return Response(500, {'Message': f'An error occurred while fetching the item: {ve}'}) 

# Get all products in inventory. 
def getProducts():
    try:
        response = table.scan()
        results = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scam(ExclusiveStartKey=response['LastEvaluatedKey'])
            results.extend(response['Items'])

        body = {
            'products': results
        }

        return Response(200, body)
    except Exception as e:
        logger.exception(f'A exception ocurred: {e}')
        return Response(500, {'Message': 'An error occurred', "Error": f"{e}"}) 

def saveProduct(data):
    try:
        table.put_item(Item=data)
        body = {
            'Operation': 'SAVE',
            'Message': 'SUCCESS',
            'Item': data
        }

        return  Response(200, body)

    except Exception as e:
        logger.exception(f'An error occurred while saving the product: {e}')
        return Response(500, {'Message': 'An error occurred while saving the product', "Error": f"{e}"})

def modifyProduct(productId, updateKey, updateValue):
    try:
        response =  table.update_item(
            Key = {
                'productID': productId
            },
            UpdateExpression = f'set  {updateKey} = :value',
            ExpressionAttributeValues = {
                ':value': updateValue
            },
            ReturnValues = 'UPDATED_NEW'
        )

        body = {
            'Operation': 'UPDATE',
            'MESSAGE': 'SUCCESS',
            'UpdatedAttributes':  response
        }

        return Response(200, body)
    
    except KeyError as ke:
        logger.exception(f'Missing key: {ke}')
        return Response(400, {'MESSAGE': f'Missing key: {ke}'})
    except Exception as e:
        logger.exception(f'A exception ocurred: {e}')
        return Response(500, {'MESSAGE': f'A exception ocurred: {e}'})


def deleteProduct(productId):
    
    try:

        response = table.delete_item(
            Key = {
                'productID': productId
            },
            ReturnValues = 'ALL_OLD'
        )

        body = {
            'Operation': 'DELETE',
            'MESSAGE': 'SUCCESS',
            'DeletedItem':  response
        }

        return Response(200, body)
    
    except  KeyError as ke:
        if "NotFound" in str(ke):
            logger.exception(f'ProductID: {id} Not Found')
            return Response(404, {'MESSAGE': f'ProductID: {id} Not Found'})
            
    except  Exception as e:
        logger.exception(f'A exception ocurred: {e}')
        return Response(500, {'MESSAGE': f'A exception ocurred: {e}'})