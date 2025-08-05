from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()


contacts = {}

class Contact(BaseModel):
    name: str
    phone: str
    email: str

@app.post("/contacts/")
def add_contact(contact: Contact):
    if contact.name.lower() in contacts:
        raise HTTPException(status_code=400, detail="Contact already exists")
    contacts[contact.name.lower()] = {
        "phone": contact.phone,
        "email": contact.email
    }
    return {"message": "Contact added", "contact": contact}

@app.get("/contacts/")
def get_contact(name: str = Query(..., description="Name of contact")):
    contact = contacts.get(name.lower())
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"name": name, **contact}

@app.post("/contacts/{name}")
def update_contact(name: str, contact: Contact):
    if name.lower() not in contacts:
        raise HTTPException(status_code=404, detail="Contact not found")
    contacts[name.lower()] = {
        "phone": contact.phone,
        "email": contact.email
    }
    return {"message": "Contact updated", "contact": contact}

@app.post("/contacts/{name}/delete")
def delete_contact(name: str):
    if name.lower() not in contacts:
        raise HTTPException(status_code=404, detail="Contact not found")
    del contacts[name.lower()]
    return {"message": f"Contact '{name}' deleted"}
