from fastapi import FastAPI
from .db import init_db


app = FastAPI()


init_db()


from .api import *