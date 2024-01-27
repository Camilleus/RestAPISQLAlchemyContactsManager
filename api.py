from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta
from models import Contact
from db import get_db, database
from pydantic import BaseModel
from typing import List


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
@app.post("/contacts/", response_model=ContactResponse)
async def create_contact(contact: ContactCreateUpdate):
    query = Contact.__table__.insert().values(**contact.dict())
    contact_id = await database.execute(query)
    return {"id": contact_id, **contact.dict()}



@app.get("/contacts/", response_model=List[ContactResponse])
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


@app.delete("/contacts/{contact_id}", response_model=ContactResponse)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return contact


@app.get("/contacts/birthdays/", response_model=list[ContactResponse])
def get_birthdays_within_7_days(db: Session = Depends(get_db)):
    today = date.today()
    next_week = today + timedelta(days=7)

    contacts = db.query(Contact).filter(
        Contact.birth_date.between(today, next_week)
    ).all()

    return contacts
