from abc import ABC, abstractmethod
from datetime import date
from typing import Dict

from mongo.db_client import MongoDBClient


class Score(ABC):
    def __init__(self, army_id: int, score_date: str, moed: str, name: str):
        self.army_id = army_id
        self.score_date = score_date
        self.moed = moed
        self.name = name
        self.gender = self._extract_gender()
        self.years_old = self._extract_years_old()
        self.team = self._extract_team()

    @abstractmethod
    def to_json(self) -> Dict:
        pass

    def _extract_gender(self) -> str:
        db_client = MongoDBClient()
        person = list(db_client.find_in_collection("persons", {"army_id": self.army_id}))[0]
        return person["gender"]

    def _extract_years_old(self) -> float:
        db_client = MongoDBClient()
        person = db_client.find_one_in_collection("persons", {"army_id": self.army_id})
        birth_date = person["birth_date"]
        birth_date = date.fromisoformat(birth_date)
        years_old = (date.today() - birth_date).days / 365
        return years_old

    def _extract_team(self) -> str:
        db_client = MongoDBClient()
        person = db_client.find_one_in_collection("persons", {"army_id": self.army_id})
        return person["team"]

    @abstractmethod
    def calculate_grade(self, gender: str) -> float:
        pass
