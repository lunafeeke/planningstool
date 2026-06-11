from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

app = FastAPI()

DATABASE_URL = "sqlite:///taken.db"
engine = create_engine(DATABASE_URL)

class Taak(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    titel: str
    klaar: bool = False

SQLModel.metadata.create_all(engine)

@app.get("/taken")
def get_taken():
    with Session(engine) as session:
        taken = session.exec(select(Taak)).all()
        return taken

@app.post("/taken")
def voeg_taak_toe(taak: Taak):
    with Session(engine) as session:
        session.add(taak)
        session.commit()
        session.refresh(taak)
        return taak


@app.put("/taken/{id}")
def vink_af(id: int):
    with Session(engine) as session:
        taak = session.get(Taak, id)
        if not taak:
            return {"bericht": "Taak niet gevonden"}
        taak.klaar = True
        session.add(taak)
        session.commit()
        session.refresh(taak)
        return taak