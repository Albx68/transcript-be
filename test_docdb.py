import pymongo
import os
from dotenv import load_dotenv
import datetime
from pprint import pprint  # For prettier printing of documents

# Load environment variables
load_dotenv()

##Create a MongoDB client, open a connection to Amazon DocumentDB as a replica set and specify the read preference as secondary preferred

def test_docdb_setup():
    password = os.getenv('DOCDB_PASSWORD')
    
    # Check if the password is set
    if not password:
        raise ValueError("Environment variable DOCDB_PASSWORD is not set!")

    # MongoDB connection URI
    uri = f'mongodb://root:{password}@health2070-prod-docdb-cluster.cluster-cu4mn4dld2td.ap-south-1.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'

    try:
        client = pymongo.MongoClient(uri)
        db = client['transcripts']  # Use the same database name as in mongo_service.py
        collection = db['embeddings']  # Use the same collection name as in mongo_service.py

        print("\nQuerying all documents in embeddings collection:")
        print("----------------------------------------------")
        
        # Find all documents
        cursor = collection.find({})
        
        # Print each document
        doc_count = 0
        for doc in cursor:
            doc_count += 1
            # print('doc', doc)
            print(f"\nDocument {doc_count}:")
            print("Session ID:", doc.get('session_id'))
            print("Created At:", doc.get('created_at'))
            print('participants', doc.get('participant_emails'))
            print("Participant Email:", doc.get('participant_email'))
            print("Owner Email:", doc.get('metadata', {}).get('owner_email'))
            print("Transcript Text:", doc.get('transcript_text')[:100] + "..." if doc.get('transcript_text') else None)
            print('1 embedding', doc.get('embedding')[0])
            print('2 embedding', doc.get('embedding')[1])
            print('3 embedding', doc.get('embedding')[2])
            print('4 embedding', doc.get('embedding')[3])
            print('5 embedding', doc.get('embedding')[4])
            print('6 embedding', doc.get('embedding')[5])
            
            print("Embedding Length:", len(doc.get('embedding', [])))
            print("Metadata:")
            pprint(doc.get('metadata'))
            print("-" * 50)

        if doc_count == 0:
            print("No documents found in the collection")
        else:
            print(f"\nTotal documents found: {doc_count}")

        # Close the connection
        client.close()
        print("\nConnection closed")

    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    test_docdb_setup()
