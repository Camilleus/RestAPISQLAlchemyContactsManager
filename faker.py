from faker import Faker

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

