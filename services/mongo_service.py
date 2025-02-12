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
        # cert_path = 'global-bundle.pem'
        # if not os.path.exists(cert_path):
        #     print("Downloading DocumentDB certificate...")
        #     urllib.request.urlretrieve(
        #         'https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem',
        #         cert_path
        #     )

        # Create connection string
        connection_string = (
            f"mongodb://root:{password}@{host}:27017/"
            f"?tls=true"
            f"&tlsCAFile=global-bundle.pem"
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
            # self.collection.create_index('session_id', unique=True)
            try:
                self.collection.create_index(
                    [("embedding", "vector")],
                    name="embedding_vector_index",
                    vectorOptions={
                        "type": "hnsw",
                        "dimensions": 768,  # Updated to match your embedding size
                        "similarity": "cosine",
                        "m": 16,
                        "efConstruction": 128  # Increased for better accuracy with larger vectors
                    }
                )
                # self.db.runCommand({
                #     'createIndexes':collection_name,
                #     'indexes': [{
                #         'key': { "embedding": "vector" },
                #         'vectorOptions': {
                #             'type': "hnsw",       # Vector search type
                #             'dimensions': 4,      # Must match your embedding size
                #             'similarity': "cosine",  # Choose 'euclidean', 'cosine', or 'dotProduct'
                #             'm': 16,              # Connectivity parameter (default 16)
                #             'efConstruction': 64   # Search quality (default 64)
                #         },
                #         'name': "transcript_embedding_index_v2"
                #     }]
                # });
                print("Successfully created transcript embedding index.")
            except Exception as e:
                print(f"Failed to create transcript embedding index: {str(e)}")
        except Exception as e:
            print(f"Failed to connect to DocumentDB: {str(e)}")
            raise

    async def store_embedding(self, transcript_data: Dict[str, Any], embedding: list) -> bool:
        try:
            print('transcript_data', transcript_data)
            # Extract participant emails
            participants = transcript_data.get('participants', [])
            owner_email = transcript_data.get('owner').get('email')  # Assuming owner's email is provided
            participant_emails = [p.get('email') for p in participants if p.get('email') and p.get('email') != owner_email]
            participant_email = participant_emails[0] if participant_emails else None  # New field added
 
            # Extract and join transcript text
            transcript_blocks = transcript_data.get('transcript', {}).get('speaker_blocks', [])
            transcript_text = ' '.join(block.get('words', '') for block in transcript_blocks)
            
            document = {
                'session_id': transcript_data.get('session_id'),
                'embedding': embedding,
                'created_at': datetime.now(),
                'transcript_text': transcript_text,
                'participant_email': participant_email,

                'metadata': {
                    'title': transcript_data.get('title'),
                    'start_time': transcript_data.get('start_time'),
                    'end_time': transcript_data.get('end_time'),
                    'participant_emails': participant_emails,
                    'owner_email': owner_email
                }
            }
            
            self.collection.insert_one(document)
            print(f"Stored embedding for session {document['session_id']}")
            return True
            
        except Exception as e:
            print(f"DocumentDB storage error: {str(e)}")
            raise 

    def get_collection_indexes(self, collection_name: str) -> list:
        """
        Get all indexes for a specific collection
        
        Args:
            collection_name: Name of the collection to check indexes for
            
        Returns:
            List of indexes in the collection
        """
        try:
            if not self.client:
                raise ConnectionError("Not connected to DocumentDB")
            
            collection = self.db[collection_name]
            indexes = list(collection.list_indexes())
            return indexes
        
        except Exception as e:
            print(f"Error getting indexes: {str(e)}")
            raise 

    def close(self):
        """Close the MongoDB connection"""
        if self.client:
            self.client.close()
            print("Connection to DocumentDB closed") 