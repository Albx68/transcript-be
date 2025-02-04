from sentence_transformers import SentenceTransformer

data = {
   "session_id":"01JK7KTHWY3PGDV82J79YN8YJ1",
   "trigger":"meeting_end",
   "title":"Meeting Title",
   "start_time":"2025-02-04T04:04:47.326869Z",
   "end_time":"2025-02-04T04:34:47.326869Z",
   "participants":[
      {
         "name":"Participant One",
         "first_name":"Participant",
         "last_name":"One",
         "email":"participant_one@company.com"
      },
      {
         "name":"Participant Two",
         "first_name":"Participant",
         "last_name":"Two",
         "email":"None"
      }
   ],
   "owner":{
      "name":"Participant One",
      "first_name":"Participant",
      "last_name":"One",
      "email":"participant_one@company.com"
   },
   "summary":"Meeting summary goes here...",
   "action_items":[
      {
         "text":"Action item one"
      },
      {
         "text":"Action item two"
      }
   ],
   "key_questions":[
      {
         "text":"Key question one?"
      },
      {
         "text":"Key question two?"
      }
   ],
   "topics":[
      {
         "text":"Topic one"
      },
      {
         "text":"Topic two"
      }
   ],
   "report_url":"https://app.read.ai/analytics/meetings/SESSIONID",
   "chapter_summaries":[
      {
         "title":"Chapter one",
         "description":"First chapter description",
         "topics":[
            {
               "text":"Topic one"
            }
         ]
      },
      {
         "title":"Chapter two",
         "description":"Second chapter description",
         "topics":[
            {
               "text":"Topic two"
            }
         ]
      }
   ],
   "transcript":{
      "speaker_blocks":[
         {
            "start_time":1738641887,
            "end_time":1738641888,
            "speaker":{
               "name":"Participant One"
            },
            "words":"Good morning everyone!"
         },
         {
            "start_time":1738641889,
            "end_time":1738641890,
            "speaker":{
               "name":"Participant Two"
            },
            "words":"Howdy!"
         },
         {
            "start_time":1738641890,
            "end_time":1738641892,
            "speaker":{
               "name":"Participant One"
            },
            "words":"I'm so excited to start this meeting."
         },
         {
            "start_time":1738641893,
            "end_time":1738641894,
            "speaker":{
               "name":"Participant Two"
            },
            "words":"Me too. I love meetings!"
         }
      ],
      "speakers":[
         {
            "name":"Participant One"
         },
         {
            "name":"Participant Two"
         }
      ]
   }
}   


def extract_emails(meeting_data):
    owner_email = meeting_data["owner"]["email"]
    participant_emails = [p["email"] for p in meeting_data["participants"] if p["email"] != "None"]
    
    return {"owner_email": owner_email, "participant_emails": participant_emails}

def get_transcript_text(meeting_data):
    transcript_blocks = meeting_data["transcript"]["speaker_blocks"]
    transcript_text = " ".join([block["words"] for block in transcript_blocks])
    return transcript_text

emails = extract_emails(data)
candidate = emails["participant_emails"][0]
transcript_text = get_transcript_text(data)

print("candidate: ", candidate)
print("transcript_text: ", transcript_text)

model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight model
vector_embedding = model.encode(transcript_text)

print('vector embedding: ', vector_embedding)