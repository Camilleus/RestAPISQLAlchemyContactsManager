from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from datetime import date
from .models import Contact
from .db import get_db
from pydantic import BaseModel

app = FastAPI()

class ContactCreateUpdate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    additional_data: str = None
    
    
# CRUD operations
@app.post("/contacts/", response_model=Contact)
def create_contact(contact: ContactCreateUpdate, db: Session = Depends(get_db)):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


