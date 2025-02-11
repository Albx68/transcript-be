import requests
import json
from datetime import datetime, timedelta

def test_webhook():
    # Local FastAPI server URL
    url = "http://localhost:8000/webhook"
    
    # Current time for start_time
    current_time = datetime.utcnow()
    
    # Sample payload matching the Pokemon meeting format
    payload = {
    "session_id": "02BACKEND123SECURE456",
    "trigger": "meeting_end",
    "title": "Enhancing API Security",
    "start_time": "2025-02-11T14:00:00Z",
    "end_time": "2025-02-11T14:45:00Z",
    "participants": [
        {
            "name": "David Wright",
            "first_name": "David",
            "last_name": "Wright",
            "email": "david@securetech.com"
        },
        {
            "name": "Eve Carter",
            "first_name": "Eve",
            "last_name": "Carter",
            "email": "eve@securetech.com"
        },
        {
            "name": "Frank Lee",
            "first_name": "Frank",
            "last_name": "Lee",
            "email": "frank@securetech.com"
        }
    ],
    "owner": {
        "name": "David Wright",
        "first_name": "David",
        "last_name": "Wright",
        "email": "david@securetech.com"
    },
    "summary": "Discussing best practices to secure APIs, including authentication strategies, rate limiting, and logging.",
    "action_items": [
        {"text": "Eve to implement OAuth2.0 for third-party API authentication."},
        {"text": "Frank to research API rate-limiting strategies."}
    ],
    "key_questions": [
        {"text": "Are JWTs sufficient for securing API requests?"},
        {"text": "How do we handle failed authentication attempts efficiently?"}
    ],
    "topics": [
        {"text": "Authentication"},
        {"text": "Rate Limiting"},
        {"text": "Logging"}
    ],
    "report_url": "https://app.read.ai/analytics/meetings/APISECURITY456",
    "chapter_summaries": [
        {
            "title": "OAuth vs. API Key Security",
            "description": "Comparing different authentication methods.",
            "topics": [
                {"text": "Security risks of API keys"}
            ]
        },
        {
            "title": "Handling Failed Authentication",
            "description": "How to manage repeated login attempts safely.",
            "topics": [
                {"text": "Brute force protection"}
            ]
        }
    ],
    "transcript": {
        "speaker_blocks": [
            {
                "start_time": 1707658800,
                "end_time": 1707658805,
                "speaker": {"name": "David Wright"},
                "words": "We've had some security concerns with our API authentication."
            },
            {
                "start_time": 1707658806,
                "end_time": 1707658810,
                "speaker": {"name": "Eve Carter"},
                "words": "I suggest we move to OAuth2.0. It's more secure than API keys."
            },
            {
                "start_time": 1707658811,
                "end_time": 1707658815,
                "speaker": {"name": "Frank Lee"},
                "words": "That makes sense. What about rate limiting to prevent abuse?"
            },
            {
                "start_time": 1707658816,
                "end_time": 1707658820,
                "speaker": {"name": "David Wright"},
                "words": "Yes, we should enforce rate limiting per user to prevent DoS attacks."
            },
            {
                "start_time": 1707658821,
                "end_time": 1707658825,
                "speaker": {"name": "Eve Carter"},
                "words": "I'll start implementing OAuth, and Frank, you can look into rate-limiting strategies."
            }
        ],
        "speakers": [
            {"name": "David Wright"},
            {"name": "Eve Carter"},
            {"name": "Frank Lee"}
        ]
    }
}

    # Test GET request
    print("Testing GET request...")
    get_response = requests.get(url)
    print(f"GET Response: {get_response.json()}\n")

    # Test POST request
    print("Testing POST request...")
    post_response = requests.post(
        url,
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print(f"POST Response: {json.dumps(post_response.json(), indent=2)}")

if __name__ == "__main__":
    test_webhook() 