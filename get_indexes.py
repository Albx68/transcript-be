from services.mongo_service import DocumentDBService
from pprint import pprint

def main():
    docdb = DocumentDBService()
    
    try:
        # Get indexes for the embeddings collection
        print("\nGetting indexes for 'embeddings' collection:")
        print("-------------------------------------------")
        indexes = docdb.get_collection_indexes("embeddings")
        
        # Pretty print each index
        for idx, index in enumerate(indexes, 1):
            print(f"\nIndex {idx}:")
            pprint(index)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        
    finally:
        if docdb:
            docdb.close()

if __name__ == "__main__":
    main() 