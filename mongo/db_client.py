from typing import List, Dict

from mongo.config import _my_db


class MongoDBClient:
    def __init__(self):
        self.db = _my_db

    def create_collection(self, collection_name: str):
        return self.db[collection_name]

    def insert_documents(self, data: List[Dict], collection_name: str):
        self.db[collection_name].insert_many(data)

    def find_in_collection(self, collection_name: str, query: Dict):
        if collection_name == "run":
            return self.db[collection_name].find(query, {"_id": 0, "duration_in_minutes": 0})
        return self.db[collection_name].find(query, {"_id": 0})

    def find_one_in_collection(self, collection_name: str, query: Dict):
        return self.db[collection_name].find_one(query)


if __name__ == '__main__':
    db_client = MongoDBClient()

    persons_indexes = [("name", "text"), ("gender", "text"), ("army_id", "text"), ("team", "text"), ("phone", "text")]
    events_indexes = [("name", "text"), ("gender", "text"), ("army_id", "text"), ("team", "text")]

    persons = db_client.db["persons"]
    runs = db_client.db["run"]
    pushups = db_client.db["pushups"]

    persons.drop_indexes()
    runs.drop_indexes()
    pushups.drop_indexes()

    persons.create_index(persons_indexes)
    runs.create_index(events_indexes)
    pushups.create_index(events_indexes)
