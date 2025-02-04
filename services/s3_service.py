import os
import json
from datetime import datetime
import boto3
from typing import Dict

class S3Service:
    def __init__(self):
        self.client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        self.bucket_name = os.getenv('S3_BUCKET_NAME')
        self.region = os.getenv('AWS_REGION', 'us-east-1')

    async def store_transcript(self, payload: dict) -> Dict[str, str]:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"transcripts/transcript_{timestamp}.json"
        
        print(f"Storing file: {filename} in bucket: {self.bucket_name}")
        
        try:
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=json.dumps(payload, indent=2),
                ContentType='application/json'
            )
            
            s3_uri = f"s3://{self.bucket_name}/{filename}"
            s3_url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{filename}"
            
            return {"uri": s3_uri, "url": s3_url}
            
        except Exception as e:
            print(f"S3 storage error: {str(e)}")
            raise 