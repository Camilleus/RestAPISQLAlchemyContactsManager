from fastapi import FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from .contact import Contact, Base
from .pg import get_db

app = FastAPI()