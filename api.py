# api.py
from fastapi import FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from .models import Contact, Base
from .db import get_db
from pydantic import BaseModel
from datetime import date

app = FastAPI()

class ContactCreateUpdate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    additional_data: str = None

