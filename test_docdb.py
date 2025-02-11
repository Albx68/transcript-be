import pymongo
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pprint import pprint

# Load environment variables from .env file
load_dotenv()

class DocumentDBClient:
    def __init__(self):
        self.client = None
        self.db = None
        
    def connect(self, database_name="your_database"):
        """Establish connection to DocumentDB"""
        try:
            # Get credentials from environment variables
            username = os.getenv('DOCDB_USERNAME', 'root')
            password = os.getenv('DOCDB_PASSWORD')
            host ="health2070-prod-docdb-cluster.cluster-cu4mn4dld2td.ap-south-1.docdb.amazonaws.com"
            
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

    def query_collection(self, collection_name, query=None, limit=10):
        """
        Query documents from a collection
        :param collection_name: Name of the collection to query
        :param query: MongoDB query dict (default: None, returns all documents)
        :param limit: Maximum number of documents to return
        """
        try:
            if not self.client:
                raise ConnectionError("Not connected to DocumentDB")

            collection = self.db[collection_name]
            query = query or {}
            
            results = collection.find(query).limit(limit)
            return list(results)
            
        except Exception as e:
            print(f"Query error: {str(e)}")
            raise

def main():
    # Create .env file with these variables
    # """
    # DOCDB_USERNAME=your_username
    # DOCDB_PASSWORD=your_password
    # DOCDB_HOST=your-cluster-address.cluster-xxx.region.docdb.amazonaws.com
    # """
    
    # Initialize client
    docdb = DocumentDBClient()
    
    try:
        # Connect to database
        docdb.connect(database_name="transcripts")
        
        # Example queries
        # 1. Simple find all documents in a collection
        results = docdb.query_collection("embeddings")
        print("\nQuery Results:")
        for doc in results:
            print(f"Document: {doc}")
            if 'embedding' in doc:
                print(f"Embedding length: {len(doc['embedding'])}")
            
        # 2. Query with filter
        # query = {"field_name": "value"}
        # filtered_results = docdb.query_collection("your_collection", query=query)
        # print("\nFiltered Results:")
        # for doc in filtered_results:
        #     print(doc)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        
    finally:
        docdb.close()

if __name__ == "__main__":
    main()