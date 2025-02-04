import os
from dotenv import load_dotenv
import redshift_connector

# Load environment variables
load_dotenv()

def create_and_verify_table():
    conn = None
    cursor = None
    try:
        print("Connecting to Redshift...")
        conn = redshift_connector.connect(
            host=os.getenv('REDSHIFT_HOST'),
            database=os.getenv('REDSHIFT_DATABASE'),
            user=os.getenv('REDSHIFT_USER'),
            password=os.getenv('REDSHIFT_PASSWORD'),
            port=int(os.getenv('REDSHIFT_PORT'))
        )
        
        # Enable autocommit mode
        conn.autocommit = True
        cursor = conn.cursor()
        
        # First, verify if schema exists
        print("Checking schema...")
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.schemata 
                WHERE schema_name = 'talent'
            );
        """)
        schema_exists = cursor.fetchone()[0]
        
        if not schema_exists:
            print("Creating schema 'talent'...")
            cursor.execute("CREATE SCHEMA talent;")
            conn.commit()
        else:
            print("Schema 'talent' already exists")
        
        # Check if table exists
        print("Checking if table exists...")
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_schema = 'talent' 
                AND table_name = 'meeting_transcripts'
            );
        """)
        table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            # Create table only if it doesn't exist
            print("Creating table...")
            cursor.execute("""
                CREATE TABLE talent.meeting_transcripts (
                    meeting_id VARCHAR(255),
                    transcript_text TEXT,
                    s3_location VARCHAR(512),
                    created_at TIMESTAMP,
                    raw_data VARCHAR(MAX)
                );
            """)
            conn.commit()
            print("Table talent.meeting_transcripts created successfully")
        else:
            print("Table talent.meeting_transcripts already exists")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise
    finally:
        # Properly close cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    create_and_verify_table() 