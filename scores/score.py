from abc import ABC, abstractmethod
from typing import Dict

from mongo.db_client import MongoDBClient


class Score(ABC):
    def __init__(self, army_id: str, score_date: str, moed: str, name: str):
        self.army_id = army_id
        self.score_date = score_date
        self.moed = moed
        self.name = name
        self.gender = self._extract_gender()

    @abstractmethod
    def to_json(self) -> Dict:
        pass

    def _extract_gender(self) -> str:
        db_client = MongoDBClient()
        person = db_client.find_one_in_collection("persons", {"army_id": self.army_id})
        return person["gender"]

    @abstractmethod
    def calculate_grade(self, gender: str) -> float:
        pass
