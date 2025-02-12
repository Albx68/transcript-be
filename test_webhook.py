import requests
import json
from datetime import datetime, timedelta

def test_webhook():
    # Local FastAPI server URL
    url = "http://localhost:8000/webhook"
    
    # Current time for start_time
    current_time = datetime.utcnow()
    
    # Sample payload with new data but same schema
    payload = {
    "session_id": "03POKEMON789BATTLE3212xx",
    "trigger": "meeting_end",
    "title": "Pokemon Battle Strategy Discussion",
    "start_time": "2025-02-15T10:00:00Z",
    "end_time": "2025-02-15T10:45:00Z",
    "participants": [
        {
            "name": "Ash Ketchum",
            "first_name": "Ash",
            "last_name": "Ketchum",
            "email": "ash@pokemon.com"
        },
        {
            "name": "Misty Waters",
            "first_name": "Misty",
            "last_name": "Waters",
            "email": "misty@pokemon.com"
        },
        {
            "name": "Brock Stone",
            "first_name": "Brock",
            "last_name": "Stone",
            "email": "brock@pokemon.com"
        }
    ],
    "owner": {
        "name": "Ash Ketchum",
        "first_name": "Ash",
        "last_name": "Ketchum",
        "email": "ash@pokemon.com"
    },
    "summary": "Discussion about effective Pokemon battle strategies, type advantages, and team composition for upcoming tournaments.",
    "action_items": [
        {"text": "Misty to research counter-strategies against electric types."},
        {"text": "Brock to compile a list of rock-type Pokemon weaknesses."}
    ],
    "key_questions": [
        {"text": "What are the most effective type combinations in current meta?"},
        {"text": "How do we counter water-type Pokemon effectively?"}
    ],
    "topics": [
        {"text": "Type Advantages"},
        {"text": "Battle Strategy"},
        {"text": "Team Composition"}
    ],
    "report_url": "https://app.read.ai/analytics/meetings/POKEMON789",
    "chapter_summaries": [
        {
            "title": "Type Effectiveness Analysis",
            "description": "Detailed discussion of Pokemon type advantages and disadvantages.",
            "topics": [
                {"text": "Water type weaknesses"}
            ]
        },
        {
            "title": "Team Building Strategies",
            "description": "How to build a balanced Pokemon team.",
            "topics": [
                {"text": "Defensive core composition"}
            ]
        }
    ],
    "transcript": {
        "speaker_blocks": [
            {
                "start_time": 1707658800,
                "end_time": 1707658805,
                "speaker": {"name": "Ash Ketchum"},
                "words": "We need to discuss effective strategies against water-type Pokemon."
            },
            {
                "start_time": 1707658806,
                "end_time": 1707658810,
                "speaker": {"name": "Misty Waters"},
                "words": "Electric and grass types are strong against water, but we need to consider dual-typing."
            },
            {
                "start_time": 1707658811,
                "end_time": 1707658815,
                "speaker": {"name": "Brock Stone"},
                "words": "Rock types are weak to water, but they're strong against electric types."
            },
            {
                "start_time": 1707658816,
                "end_time": 1707658820,
                "speaker": {"name": "Ash Ketchum"},
                "words": "We should focus on Pokemon that can learn grass moves but aren't grass type."
            },
            {
                "start_time": 1707658821,
                "end_time": 1707658825,
                "speaker": {"name": "Misty Waters"},
                "words": "I'll research more about electric type counters, and Brock can look into rock type vulnerabilities."
            }
        ],
        "speakers": [
            {"name": "Ash Ketchum"},
            {"name": "Misty Waters"},
            {"name": "Brock Stone"}
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