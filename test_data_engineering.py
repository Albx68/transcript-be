data1 = {
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
data2 = {
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

pokemon_data = {
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
