from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
import boto3
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION', 'us-east-1')
)

BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

# Define the expected payload structure
class WebhookPayload(BaseModel):
    event_type: str
    data: dict
    timestamp: Optional[str] = None

async def store_transcript_in_s3(payload: dict):
    try:
        # Generate a unique filename using timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"transcript_{timestamp}.json"
        
        # Convert payload to JSON string
        json_data = json.dumps(payload, indent=2)
        
        # Upload to S3
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=json_data,
            ContentType='application/json'
        )
        
        return f"s3://{BUCKET_NAME}/{filename}"
    except Exception as e:
        print(f"Error storing in S3: {str(e)}")
        raise

@app.post("/webhook")
@app.get("/webhook")  # Adding GET method support
async def webhook_endpoint(request: Request):
    try:
        # Log the request method and headers
        print(f"Received {request.method} request")
        print(f"Headers: {request.headers}")
        
        # Handle GET requests (often used for verification)
        if request.method == "GET":
            return {
                "status": "success",
                "message": "Webhook endpoint verified"
            }
            
        # For POST requests, parse the payload
        payload = await request.json()
        print(f"Received payload: {payload}")
        
        # Store the transcript in S3
        s3_location = await store_transcript_in_s3(payload)
        
        return {
            "status": "success",
            "message": "Webhook received and stored successfully",
            "s3_location": s3_location
        }
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Webhook server is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 