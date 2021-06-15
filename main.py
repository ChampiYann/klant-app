from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import UUID, uuid4

app = FastAPI()


class KlantBase(BaseModel):
    tafel: int
    rekening: UUID


class KlantIn(KlantBase):
    pass


class KlantOut(KlantBase):
    id: UUID


klant1 = KlantOut(id="550e8400-e29b-41d4-a716-446655440000",
                  tafel=1, rekening="650e8400-e29b-41d4-a716-446655440000")
klant2 = KlantOut(id="550e8400-e29b-41d4-a716-446655440001",
                  tafel=2, rekening="650e8400-e29b-41d4-a716-446655440001")
example_source = [klant1, klant2]


@app.get("/klanten", response_model=List[KlantOut])
def read_klanten():
    return example_source


@app.get("/klant/{klant_id}", response_model=KlantOut)
def read_klant(klant_id: UUID):
    result = [klant for klant in example_source if klant.id == klant_id]
    if not result:
        raise HTTPException(status_code=404, detail="Klant with id " + str(klant_id) + " not found")
    return result[0]


@app.get("/klantPerTafel/{tafelnummer}", response_model=List[KlantOut])
def read_klant_per_tafel(tafelnummer: int):
    result = [klant for klant in example_source if klant.tafel == tafelnummer]
    return result


@app.post("/klant", response_model=KlantOut)
def create_klant(klantIn: KlantIn):
    # Assign new ID to klant
    klantOut = KlantOut(**klantIn.dict(), id=uuid4())
    example_source.append(klantOut)
    return klantOut


@app.put("/klant/{klant_id}", response_model=KlantOut)
def update_klant(klant_id: UUID, klantIn: KlantIn):
    result = [klant for klant in example_source if klant.id == klant_id]
    if not result:
        raise HTTPException(
            status_code=404, detail="Klant with id " + str(klant_id) + " not found")
    example_source.remove(result[0])
    klantOut = KlantOut(**klantIn.dict(), id=klant_id)
    example_source.append(klantOut)
    return klantOut


@app.delete("/klant/{klant_id}", response_model=KlantOut)
def delete_klant(klant_id: UUID):
    result = [klant for klant in example_source if klant.id == klant_id]
    if not result:
        raise HTTPException(
            status_code=404, detail="Klant with id " + str(klant_id) + " not found")
    example_source.remove(result[0])
    return result[0]
