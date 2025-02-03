from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()

# Define the expected payload structure
class WebhookPayload(BaseModel):
    event_type: str
    data: dict
    timestamp: Optional[str] = None

@app.post("/webhook")
async def webhook_endpoint(payload: WebhookPayload):
    try:
        # Process the webhook payload
        print(f"Received webhook event: {payload.event_type}")
        print(f"Payload data: {payload.data}")
        print(f"Timestamp: {payload.timestamp}")
        
        # Add your webhook processing logic here
        
        return {
            "status": "success",
            "message": "Webhook received successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Webhook server is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 