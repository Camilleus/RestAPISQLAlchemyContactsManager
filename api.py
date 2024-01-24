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
    

class ContactResponse(BaseModel):
    id: int
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


@app.get("/contacts/", response_model=list[Contact])
def get_all_contacts(
    q: str = Query(None, alias="search", description="Search contacts by first name, last name, or email"),
    db: Session = Depends(get_db)
):
    if q:
        contacts = db.query(Contact).filter(
            Contact.first_name.ilike(f"%{q}%")
            | Contact.last_name.ilike(f"%{q}%")
            | Contact.email.ilike(f"%{q}%")
        ).all()
    else:
        contacts = db.query(Contact).all()
    return contacts


@app.get("/contacts/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@app.put("/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact: ContactCreateUpdate, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact