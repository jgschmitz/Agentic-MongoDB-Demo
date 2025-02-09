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
openai.api_key = os.getenv("OPENAI_API_KEY")

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
