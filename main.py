from fastapi import FastAPI, HTTPException, Query, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import date, timedelta
from models import Contact
from db import init_db, get_db


app = FastAPI()


init_db()


from api import *

