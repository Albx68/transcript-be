import os
import json
from datetime import datetime
import redshift_connector
from typing import Dict

class RedshiftService:
    def __init__(self):
        self.connection_params = {
            'host': os.getenv('REDSHIFT_HOST'),
            'database': os.getenv('REDSHIFT_DATABASE'),
            'user': os.getenv('REDSHIFT_USER'),
            'password': os.getenv('REDSHIFT_PASSWORD'),
            'port': int(os.getenv('REDSHIFT_PORT'))
        }

    def _extract_transcript_text(self, transcript_data: dict) -> str:
        transcript_blocks = transcript_data.get('transcript', {}).get('speaker_blocks', [])
        return ' '.join(block.get('words', '') for block in transcript_blocks)

    async def store_transcript(self, transcript_data: dict, s3_location: str) -> bool:
        conn = None
        cursor = None
        try:
            conn = redshift_connector.connect(**self.connection_params)
            cursor = conn.cursor()
            
            meeting_id = transcript_data.get('session_id', '')
            # transcript_text = self._extract_transcript_text(transcript_data)
            timestamp = datetime.now().isoformat()
            
            insert_query = """
                INSERT INTO talent.meeting_transcripts (
                    meeting_id, transcript_text, s3_location, created_at, raw_data
                ) VALUES (%s, %s, %s, %s, %s)
            """
            
            values = (
                meeting_id,
                # transcript_text,
                s3_location,
                timestamp,
                json.dumps(transcript_data)
            )
            
            cursor.execute(insert_query, values)
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Redshift storage error: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close() 