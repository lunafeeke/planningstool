from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import anthropic
import os

load_dotenv()

app = FastAPI()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Bericht(BaseModel):
    berichten: list

@app.post("/chat")
def stel_vraag(data: Bericht):
    bericht = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        system="Jij bent een vriendelijke planningsassistent die mensen helpt productief te zijn. Je antwoordt altijd in het Nederlands.",
        messages=data.berichten
    )
    return {"antwoord": bericht.content[0].text}

