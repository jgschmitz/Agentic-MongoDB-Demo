# Agentic-MongoDB-Demo
FastAPI + OpenAI + MongoDB setup forms the foundation of an agentic system, but let's break it down.

An agentic system is one that:

Stores Memory 🧠 → Your setup saves chat history in MongoDB.<br>
Retrieves Context 🔍 → It can recall past conversations per user.<br>
Makes Decisions 🧩 → OpenAI processes messages and generates responses dynamically.<br>
Acts Autonomously 🤖 → The system functions on its own without direct control.<br>

Lets get started!

Lets install dependencies 
```
pip install fastapi pymongo openai uvicorn
```
Now create the main.py (if you are running mongodb locally you only have to add your openAI key)
```
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
import openai
import os

# Load OpenAI API Key
openai.api_key = "OPENAI_API_KEY"

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017")
db = client["agentic_demo"]
collection = db["conversations"]

app = FastAPI()

# Define a Pydantic model to enforce JSON body input
class ChatRequest(BaseModel):
    user_id: str
    message: str

# Explicitly tell FastAPI to expect JSON in the request body
from fastapi import Body

@app.post("/chat/")
async def chat(request: ChatRequest = Body(...)):  # Now it forces a JSON body
    """Handles user messages and generates a response using OpenAI."""
    history = list(collection.find({"user_id": request.user_id}).sort("timestamp", 1))
    messages = [{"role": "system", "content": "You are an AI agent."}]

    for record in history:
        messages.append({"role": "user", "content": record["user_message"]})
        messages.append({"role": "assistant", "content": record["ai_response"]})

    messages.append({"role": "user", "content": request.message})

    response = openai.ChatCompletion.create(model="gpt-4", messages=messages)
    ai_response = response["choices"][0]["message"]["content"]

    collection.insert_one({"user_id": request.user_id, "user_message": request.message, "ai_response": ai_response})

    return {"response": ai_response}
```

Lets run the API
```
uvicorn main:app --reload
```
Now that its running to test the API in the browswer
```
Browser (Swagger UI) Go to:
📍 http://127.0.0.1:8000/docs (Interactive API docs)
```
or you can use cURL from CLI
```
curl -X 'POST' \
  'http://127.0.0.1:8000/chat/' \
  -H 'Content-Type: application/json' \
  -d '{"user_id": "123", "message": "Hello, how are you?"}'
```
You should get a response something like this
```
"response":"Hello! As an AI, I have the ability to perform various functions, based on my programming. Here are some of the things I can do:\n\n1. Informing: I can provide news, weather updates, sports scores, and more. \n2. Answering Questions: I can provide information on a wide range of topics based on my programming and learning algorithms.\n3. Setting Reminders and Alarms: I can help you manage your schedule and could remind you of important tasks.\n4. Language Processing: I can understand and respond in several languages.\n5. Assisting with Certain Tasks: Depending upon my programming, I may be able to assist with tasks such as booking appointments, sending messages, making reservations, or translating languages in real-time.\n6. Learning and Adapting: Depending on my design, I may have the ability to learn from interactions and improve my responses over time.\n7. Providing Entertainment: Some AIs can tell jokes, recommend movies or music, or even play games with you.\n\nIt's important to note that not every AI will be able to perform all these tasks—it depends on how they have been designed and programmed."
```
go and check your mongodb Agentic_Demo.conversations - all the answers will be stored in there!
have fun! 🍺
