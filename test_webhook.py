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
        "session_id": "01PKMN123ASHKETCHUM456",
        "trigger": "meeting_end",
        "title": "Pokémon Gym Leader Strategy Meeting",
        "start_time": current_time.isoformat() + "Z",
        "end_time": (current_time + timedelta(minutes=30)).isoformat() + "Z",
        "participants": [
            {
                "name": "Ash Ketchum",
                "first_name": "Ash",
                "last_name": "Ketchum",
                "email": "ash.ketchum@pokemon.com"
            },
            {
                "name": "Misty Waterflower",
                "first_name": "Misty",
                "last_name": "Waterflower",
                "email": "misty@ceruleangym.com"
            }
        ],
        "owner": {
            "name": "Professor Oak",
            "first_name": "Samuel",
            "last_name": "Oak",
            "email": "prof.oak@pallettown.com"
        },
        "summary": "Discussion about upcoming Pokémon League championships and training strategies.",
        "action_items": [
            {"text": "Ash to work on Pikachu's Thunder attack accuracy"},
            {"text": "Misty to prepare Water-type strategy guide"}
        ],
        "key_questions": [
            {"text": "How can we improve type advantage strategies?"},
            {"text": "What's the best approach for the Elite Four?"}
        ],
        "topics": [
            {"text": "Battle Strategies"},
            {"text": "Pokémon Training Methods"}
        ],
        "report_url": "https://app.read.ai/analytics/meetings/POKEMON123",
        "chapter_summaries": [
            {
                "title": "Training Discussion",
                "description": "Review of current training methods",
                "topics": [
                    {"text": "Type advantage training"}
                ]
            },
            {
                "title": "Championship Preparation",
                "description": "Elite Four strategy planning",
                "topics": [
                    {"text": "Battle tactics review"}
                ]
            }
        ],
        "transcript": {
            "speaker_blocks": [
                {
                    "start_time": int(current_time.timestamp()),
                    "end_time": int(current_time.timestamp()) + 1,
                    "speaker": {"name": "Ash Ketchum"},
                    "words": "I choose you, Pikachu!"
                },
                {
                    "start_time": int(current_time.timestamp()) + 2,
                    "end_time": int(current_time.timestamp()) + 3,
                    "speaker": {"name": "Misty Waterflower"},
                    "words": "Water types are clearly the strongest!"
                },
                {
                    "start_time": int(current_time.timestamp()) + 4,
                    "end_time": int(current_time.timestamp()) + 5,
                    "speaker": {"name": "Ash Ketchum"},
                    "words": "Each Pokémon has its own strengths and weaknesses."
                },
                {
                    "start_time": int(current_time.timestamp()) + 6,
                    "end_time": int(current_time.timestamp()) + 7,
                    "speaker": {"name": "Misty Waterflower"},
                    "words": "True, we should focus on bringing out their individual potential."
                }
            ],
            "speakers": [
                {"name": "Ash Ketchum"},
                {"name": "Misty Waterflower"}
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