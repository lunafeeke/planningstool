from fastapi import FastAPI
from pydantic import BaseModel
import httpx

app = FastAPI()

@app.get("/pokemon/{naam}")
def get_pokemon(naam: str):
    response = httpx.get(f"https://pokeapi.co/api/v2/pokemon/{naam.lower()}")
    data = response.json()
    return {"naam": data["name"], "gewicht": data["weight"]}  