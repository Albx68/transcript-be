from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
import boto3
import json
from datetime import datetime
import os
from dotenv import load_dotenv
import redshift_connector
from create_table import create_and_verify_table

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
        filename = f"transcripts/transcript_{timestamp}.json"  # Added transcripts/ prefix
        
        print(f"Attempting to store file: {filename}")
        print(f"Using bucket: {BUCKET_NAME}")
        
        # Convert payload to JSON string
        json_data = json.dumps(payload, indent=2)
        
        # Upload to S3
        try:
            response = s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=filename,
                Body=json_data,
                ContentType='application/json'
            )
            print(f"S3 upload response: {response}")
        except Exception as s3_error:
            print(f"S3 upload error: {str(s3_error)}")
            raise
        
        s3_location = f"s3://{BUCKET_NAME}/{filename}"
        print(f"File stored successfully at: {s3_location}")
        return s3_location
        
    except Exception as e:
        print(f"Error storing in S3: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise

async def store_transcript_in_redshift(transcript_data: dict, s3_location: str):
    try:
        # Connect using redshift_connector
        conn = redshift_connector.connect(
            host=os.getenv('REDSHIFT_HOST'),
            database=os.getenv('REDSHIFT_DATABASE'),
            user=os.getenv('REDSHIFT_USER'),
            password=os.getenv('REDSHIFT_PASSWORD'),
            port=int(os.getenv('REDSHIFT_PORT'))
        )
        
        # Extract transcript data
        timestamp = datetime.now().isoformat()
        transcript_text = transcript_data.get('data', {}).get('transcript', '')
        meeting_id = transcript_data.get('data', {}).get('meeting_id', '')
        
        # Create cursor and execute insert
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO talent.meeting_transcripts (
                meeting_id,
                transcript_text,
                s3_location,
                created_at,
                raw_data
            ) VALUES (
                %s, %s, %s, %s, %s
            )
        """, (
            meeting_id,
            transcript_text,
            s3_location,
            timestamp,
            json.dumps(transcript_data)
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
            
        print(f"Successfully stored transcript in Redshift")
        return True
        
    except Exception as e:
        print(f"Error storing in Redshift: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise

async def create_transcript_table():
    try:
        await create_and_verify_table()
    except Exception as e:
        print(f"Error creating table: {str(e)}")
        raise

@app.post("/webhook")
@app.get("/webhook")
async def webhook_endpoint(request: Request):
    try:
        print(f"Received {request.method} request")
        print(f"Headers: {request.headers}")
        
        if request.method == "GET":
            return {
                "status": "success",
                "message": "Webhook endpoint verified"
            }
        
        # For POST requests, parse the payload
        payload = await request.json()
        print(f"Received payload: {payload}")
        
        # Store in S3 first
        print("Starting S3 storage process...")
        try:
            s3_location = await store_transcript_in_s3(payload)
            print(f"Successfully stored in S3 at: {s3_location}")
            
            # Store in Redshift
            print("Starting Redshift storage process...")
            await store_transcript_in_redshift(payload, s3_location)
            print("Successfully stored in Redshift")
            
        except Exception as storage_error:
            print(f"Failed to store data: {str(storage_error)}")
            raise HTTPException(status_code=500, detail=f"Failed to store data: {str(storage_error)}")
        
        return {
            "status": "success",
            "message": "Webhook received and stored successfully in S3 and Redshift",
            "s3_location": s3_location
        }
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Webhook server is running"}

@app.on_event("startup")
async def startup_event():
    print("Creating transcript table if it doesn't exist...")
    try:
        await create_transcript_table()
    except Exception as e:
        print(f"Error during startup: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 