from faker import Faker
from models import Contact
from db import database, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


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


def generate_insert_queries(contacts):
    queries = []
    for contact in contacts:
        query = f"INSERT INTO contacts (first_name, last_name, email, phone_number, birth_date, additional_data) VALUES ('{contact['first_name']}', '{contact['last_name']}', '{contact['email']}', '{contact['phone_number']}', '{contact['birth_date']}', '{contact['additional_data']}');"
        queries.append(query)
    return queries


async def seed_fake_data():
    contacts = [create_fake_contact() for _ in range(20)]
    queries = generate_insert_queries(contacts)

    with open("data_for_db.sql", "w") as f:
        for query in queries:
            f.write(query + "\n")


    engine = create_engine("sqlite:///./contacts.db", connect_args={"check_same_thread": False})
    async with engine.begin() as conn:
        for query in queries:
            await conn.execute(query)


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(seed_fake_data())
    print("Fikcyjne dane zostały zapisane do data_for_db.sql i zaimportowane do bazy.")
