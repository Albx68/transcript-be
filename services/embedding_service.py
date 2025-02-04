import google.generativeai as genai
import os

class EmbeddingService:
    def __init__(self):
        self.model = "models/embedding-001"
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

    def get_transcript_text(self, meeting_data: dict) -> str:
        transcript_blocks = meeting_data.get("transcript", {}).get("speaker_blocks", [])
        return " ".join(block.get("words", "") for block in transcript_blocks)

    def get_embedding(self, text: str) -> list:
        response = genai.embed_content(
            model=self.model,
            content=text,
            task_type="retrieval_document"
        )
        return response['embedding'] 