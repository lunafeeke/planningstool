from fastapi import FastAPI
import json
from pydantic import BaseModel

class Taak(BaseModel):
    titel: str
    klaar: bool = False

app = FastAPI()

def lees_taken():
    with open("taken.json", "r") as f:
        taken = json.load(f)
    return taken

def sla_taken_op(taken):
    with open("taken.json", "w") as f:
        json.dump(taken, f)

@app.get("/taken")
def get_taken():
    taken = lees_taken()
    return taken


@app.post("/taken")
def voeg_taak_toe(taak: Taak):
    taken = lees_taken()
    id = len(taken) + 1
    nieuwe_taak = {"id": id, "titel": taak.titel, "klaar": taak.klaar}
    taken.append(nieuwe_taak)
    sla_taken_op(taken)
    return {"message": "Taak toegevoegd", "taak": nieuwe_taak}

@app.put("/taken/{id}")
def vink_af(id: int):
    taken = lees_taken()
    for taak in taken:
        if taak["id"] == id:
            taak["klaar"] = True
            sla_taken_op(taken)
            return {"bericht": f"Taak '{taak['titel']}' afgevinkt!"}
    return {"bericht": "Taak niet gevonden"}
