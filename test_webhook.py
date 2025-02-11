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
    "session_id": "01FRONTEND123OPTIMIZE456",
    "trigger": "meeting_end",
    "title": "Improving React App Performance",
    "start_time": "2025-02-11T10:00:00Z",
    "end_time": "2025-02-11T10:30:00Z",
    "participants": [
        {
            "name": "Alice Johnson",
            "first_name": "Alice",
            "last_name": "Johnson",
            "email": "alice@techcorp.com"
        },
        {
            "name": "Bob Smith",
            "first_name": "Bob",
            "last_name": "Smith",
            "email": "bob@techcorp.com"
        },
        {
            "name": "Charlie Doe",
            "first_name": "Charlie",
            "last_name": "Doe",
            "email": "charlie@techcorp.com"
        }
    ],
    "owner": {
        "name": "Charlie Doe",
        "first_name": "Charlie",
        "last_name": "Doe",
        "email": "charlie@techcorp.com"
    },
    "summary": "Discussion about optimizing frontend performance in a React application, covering lazy loading, memoization, and state management improvements.",
    "action_items": [
        {"text": "Alice to implement lazy loading for image-heavy pages."},
        {"text": "Bob to investigate Recoil vs. Redux for state management improvements."}
    ],
    "key_questions": [
        {"text": "How can we reduce unnecessary re-renders?"},
        {"text": "Should we implement React.memo in all components?"}
    ],
    "topics": [
        {"text": "Lazy Loading"},
        {"text": "State Management"},
        {"text": "Memoization"}
    ],
    "report_url": "https://app.read.ai/analytics/meetings/FRONTEND123",
    "chapter_summaries": [
        {
            "title": "Component Rendering Optimizations",
            "description": "Discussion on React.memo and useCallback usage.",
            "topics": [
                {"text": "Preventing unnecessary renders"}
            ]
        },
        {
            "title": "State Management Strategy",
            "description": "Comparison of Redux and Recoil for future implementation.",
            "topics": [
                {"text": "Performance trade-offs"}
            ]
        }
    ],
    "transcript": {
        "speaker_blocks": [
            {
                "start_time": 1707655200,
                "end_time": 1707655205,
                "speaker": {"name": "Alice Johnson"},
                "words": "We've noticed that our React app is lagging when rendering large data sets."
            },
            {
                "start_time": 1707655206,
                "end_time": 1707655210,
                "speaker": {"name": "Bob Smith"},
                "words": "Yeah, I think we should implement lazy loading for our images and large components."
            },
            {
                "start_time": 1707655211,
                "end_time": 1707655215,
                "speaker": {"name": "Charlie Doe"},
                "words": "Good idea. What about state management? Are we overusing Redux?"
            },
            {
                "start_time": 1707655216,
                "end_time": 1707655220,
                "speaker": {"name": "Bob Smith"},
                "words": "Maybe. We should explore Recoil. It has better performance for component-based state."
            },
            {
                "start_time": 1707655221,
                "end_time": 1707655225,
                "speaker": {"name": "Alice Johnson"},
                "words": "I agree. Let's also memoize our expensive calculations to avoid redundant re-renders."
            }
        ],
        "speakers": [
            {"name": "Alice Johnson"},
            {"name": "Bob Smith"},
            {"name": "Charlie Doe"}
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