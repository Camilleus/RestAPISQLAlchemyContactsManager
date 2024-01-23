from fastapi import FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from .models import Contact, Base
from .db import get_db

app = FastAPI()