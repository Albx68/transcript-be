from pymongo import MongoClient
import os
from typing import Dict, Any
from datetime import datetime
import urllib.request

class DocumentDBService:
    def __init__(self):
        # Get DocumentDB connection details from environment
        password = os.getenv('DOCDB_PASSWORD')
        host = os.getenv('DOCDB_HOST')
        db_name = os.getenv('DOCDB_DATABASE', 'transcripts')
        collection_name = os.getenv('DOCDB_COLLECTION', 'embeddings')
        
        # Download CA certificate if it doesn't exist
        cert_path = 'global-bundle.pem'
        if not os.path.exists(cert_path):
            print("Downloading DocumentDB certificate...")
            urllib.request.urlretrieve(
                'https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem',
                cert_path
            )

        # Create connection string
        connection_string = (
            f"mongodb://root:{password}@{host}:27017/"
            f"?tls=true"
            f"&tlsCAFile={cert_path}"
            f"&replicaSet=rs0"
            f"&readPreference=secondaryPreferred"
            f"&retryWrites=false"
        )
        
        try:
            print(f"Attempting to connect to DocumentDB at {host}...")
            self.client = MongoClient(connection_string)
            
            # Test the connection
            self.client.admin.command('ismaster')
            print("Successfully connected to DocumentDB")
            
            # Get database and collection
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
            
            # Create simple index on session_id
            self.collection.create_index('session_id', unique=True)
            
        except Exception as e:
            print(f"Failed to connect to DocumentDB: {str(e)}")
            raise

    async def store_embedding(self, transcript_data: Dict[str, Any], embedding: list) -> bool:
        try:
            # Extract participant emails
            participants = transcript_data.get('participants', [])
            participant_emails = [p.get('email') for p in participants if p.get('email')]
            
            # Extract and join transcript text
            transcript_blocks = transcript_data.get('transcript', {}).get('speaker_blocks', [])
            transcript_text = ' '.join(block.get('words', '') for block in transcript_blocks)
            
            document = {
                'session_id': transcript_data.get('session_id'),
                'embedding': embedding,
                'created_at': datetime.now(),
                'transcript_text': transcript_text,
                'metadata': {
                    'title': transcript_data.get('title'),
                    'start_time': transcript_data.get('start_time'),
                    'end_time': transcript_data.get('end_time'),
                    'participant_emails': participant_emails
                }
            }
            
            self.collection.insert_one(document)
            print(f"Stored embedding for session {document['session_id']}")
            return True
            
        except Exception as e:
            print(f"DocumentDB storage error: {str(e)}")
            raise 