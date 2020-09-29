import datetime
import random
from random import randint

from events.pushups import PushUps
from mongo.db_client import MongoDBClient

if __name__ == '__main__':
    db_client = MongoDBClient()
    persons = list(db_client.find_in_collection("persons", {}))

    pushups = PushUps()

    scores = []
    for person in persons:
        army_id = person["army_id"]

        start_date = datetime.date(2019, 1, 1)
        end_date = datetime.date(2020, 1, 1)

        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)

        score = {
            "army_id": army_id,
            "event_date": str(random_date),
            "name": "final",
            "pushups": randint(1, 80),
            "moed": random.choice(["a", "b", "other"])
        }
        scores.append(score)
    pushups.add_scores(scores)
    scores = pushups.publish_scores()

    db_client.insert_documents(scores, "pushups")
