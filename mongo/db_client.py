from typing import List, Dict

from mongo.config import _my_db


class MongoDBClient:
    def __init__(self):
        self.db = _my_db

    def create_collection(self, collection_name: str):
        return self.db[collection_name]

    def drop_collection(self, data: List[Dict], collection_name: str):
        self.db[collection_name].insert_many(data)

    def find_in_collection(self, collection_name: str, query: Dict):
        return self.db[collection_name].find(query, {"_id": 0})

    def find_one_in_collection(self, collection_name: str, query: Dict):
        return self.db[collection_name].find_one(query)
