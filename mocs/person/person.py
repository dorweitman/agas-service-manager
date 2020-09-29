import datetime
import random
import string
from random import randint

from mongo.db_client import MongoDBClient

if __name__ == '__main__':
    persons = []
    for i in range(200):
        start_date = datetime.date(1997, 1, 1)
        end_date = datetime.date(2000, 2, 1)

        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)

        person = {
            "army_id": randint(8000000, 8900000),
            "first_name": random.choice(["alon", "dor", "guy"]),
            "last_name": random.choice(["katz", "weitman", "ben bassat"]),
            "birth_date": str(random_date),
            "gender": random.choice(["male", "female"]),
            "team": random.choice(["Badly", "Sayag", "Geffen", "Vainer", "Marom"])
        }

        persons.append(person)
    db_client = MongoDBClient()
    db_client.insert_documents(persons, "persons")
