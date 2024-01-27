from faker import Faker
from datetime import datetime, timedelta
from models import Contact
from db import database

fake = Faker()

def create_fake_contact():
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "phone_number": fake.phone_number(),
        "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=90),
        "additional_data": fake.text() 
    }

async def seed_fake_data():
    contacts = [create_fake_contact() for _ in range(20)]
    
    for contact in contacts:
        query = Contact.__table__.insert().values(**contact)
        await database.execute(query)

if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(seed_fake_data())
    print("Fikcyjne dane zostały dodane do bazy.")
