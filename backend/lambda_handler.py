"""
AWS Lambda handler for Restaceratops API
Uses Mangum to adapt FastAPI for Lambda
"""

import os
import json
from mangum import Mangum
from api.main import app

# Create Mangum handler for AWS Lambda
handler = Mangum(app, lifespan="off")

# Lambda function handler
def lambda_handler(event, context):
    """
    AWS Lambda handler function
    """
    try:
        # Handle the request through Mangum
        response = handler(event, context)
        return response
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "error": "Internal server error",
                "message": str(e)
            })
        } 