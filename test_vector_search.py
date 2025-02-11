import pymongo
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pprint import pprint
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

class EmbeddingService:
    def __init__(self):
        self.model = "models/embedding-001"
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

    def get_embedding(self, text: str) -> list:
        response = genai.embed_content(
            model=self.model,
            content=text,
            task_type="retrieval_document"
        )
        return response['embedding']

class DocumentDBClient:
    def __init__(self):
        self.client = None
        self.db = None
        self.embedding_service = EmbeddingService()
        
    def connect(self, database_name="your_database"):
        """Establish connection to DocumentDB"""
        try:
            # Get credentials from environment variables
            username = os.getenv('DOCDB_USERNAME', 'root')
            password = os.getenv('DOCDB_PASSWORD')
            host = "health2070-prod-docdb-cluster.cluster-cu4mn4dld2td.ap-south-1.docdb.amazonaws.com"
            
            # Debug print (mask password partially)
            print("Debug values:")
            print(f"Username: {username}")
            print(f"Password: {'*' * 8}{password[-4:] if password else ''}")
            print(f"Host: {host}")
            print(f"ENV file path: {os.path.abspath('.env')}")
            
            # URL encode after debugging print
            username = quote_plus(username)
            password = quote_plus(password)
            
            if not all([password, host]):
                raise ValueError("Missing required environment variables!")

            # Connection URI
            uri = f'mongodb://{username}:{password}@{host}:27017/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
            
            # Establish connection
            self.client = pymongo.MongoClient(uri)
            self.db = self.client[database_name]
            
            # Test connection
            self.client.admin.command('ismaster')
            print("Successfully connected to DocumentDB")
            
        except Exception as e:
            print(f"Connection error: {str(e)}")
            raise

    def close(self):
        """Close the database connection"""
        if self.client:
            self.client.close()
            print("Connection closed")

    def vector_search(self, query_text: str, collection_name: str = "transcripts", num_results: int = 5):
        """
        Perform vector search using text query
        :param query_text: Text to search for
        :param collection_name: Name of the collection to search in
        :param num_results: Number of results to return (k)
        """
        try:
            if not self.client:
                raise ConnectionError("Not connected to DocumentDB")

            # Get embedding for the query text
            query_vector = self.embedding_service.get_embedding(query_text)
            
            # Perform vector search with correct schema
            results = self.db[collection_name].aggregate([
                {
                    "$search": {
                        "vectorSearch": {
                            "vector": query_vector,
                            "path": "embedding",
                            "similarity": "cosine",
                            "k": num_results,
                            # Optional parameters for different index types
                            # "probes": 10,  # For IVFFlat index
                            # "efSearch": 100  # For HNSW index
                        }
                    }
                }
            ])
            
            return list(results)
            
        except Exception as e:
            print(f"Vector search error: {str(e)}")
            raise

def main():
    # Initialize client
    docdb = DocumentDBClient()
    
    try:
        # Connect to database
        docdb.connect(database_name="transcripts")
        
        # Example vector search
        query = "who were the speakers?"
        results = docdb.vector_search(query)
        
        print("\nVector Search Results:")
        for doc in results:
            pprint(doc)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        
    finally:
        docdb.close()

if __name__ == "__main__":
    main()

