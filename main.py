from fastapi import FastAPI
from db import init_db


app = FastAPI()


init_db()


from api import ContactCreateUpdate, ContactResponse, Contact, create_contact, get_all_contacts, get_contact, update_contact, delete_contact, get_birthdays_within_7_days


