from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import uvicorn
import json
import os

OLLAMA_URL = "http://localhost:11434/v1/chat/completions"
USED_MODEL = 'mistral'

DEV_ROLE = 'system'

def load_rules():
    """Load rules from rules.txt into a list of developer messages."""
    developer_messages = []
    if os.path.exists("rules.txt"):
        with open("rules.txt", encoding="utf-8") as f:
            for line in f:
                text_rule = line.strip()
                if text_rule:
                    developer_messages.append({'role': DEV_ROLE, 'content': text_rule})
    return developer_messages


class ChatRequest(BaseModel):
    messages: list


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def root():
    return 'Hi!'


@app.post("/chat")
async def chat_with_ollama(request: ChatRequest):
    try:
        developer_messages = load_rules()

        request_data = request.model_dump()

        request_data['model'] = USED_MODEL
        request_data['messages'] = developer_messages + request_data['messages']


        response = requests.post(OLLAMA_URL, json=request_data)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        
        response_json = response.json()

        if "messages" in response_json:
            response_json["messages"] = [
                msg for msg in response_json["messages"] if msg.get("role") != DEV_ROLE
            ]

        return response_json

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
