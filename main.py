from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
from dotenv import load_dotenv
from services.s3_service import S3Service
from services.redshift_service import RedshiftService
from create_table import create_and_verify_table
from contextlib import asynccontextmanager
from services.embedding_service import EmbeddingService
from services.mongo_service import DocumentDBService

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        await create_and_verify_table()
    except Exception as e:
        print(f"Error during startup: {e}")
    yield
    # Shutdown
    pass

app = FastAPI(lifespan=lifespan)
s3_service = S3Service()
redshift_service = RedshiftService()
embedding_service = EmbeddingService()
docdb_service = DocumentDBService()

class WebhookPayload(BaseModel):
    event_type: str
    data: dict
    timestamp: Optional[str] = None

@app.post("/webhook")
@app.get("/webhook")
async def webhook_endpoint(request: Request):
    try:
        if request.method == "GET":
            return {"status": "success", "message": "Webhook endpoint verified"}
        
        payload = await request.json()
        
        # Store in S3 and Redshift
        s3_locations = await s3_service.store_transcript(payload)
        await redshift_service.store_transcript(payload, s3_locations['url'])
        
        # Generate embedding and store in MongoDB
        transcript_text = embedding_service.get_transcript_text(payload)
        embedding = embedding_service.get_embedding(transcript_text)
        await docdb_service.store_embedding(payload, embedding)
        
        return {
            "status": "success",
            "message": "Webhook received and stored successfully",
            "s3_location": s3_locations['url'],
            "s3_uri": s3_locations['uri']
        }
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Webhook server is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 