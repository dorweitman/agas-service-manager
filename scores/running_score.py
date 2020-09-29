from datetime import timedelta, datetime
from typing import Dict

from scores.score import Score

GRADING = {"male": {"max": timedelta(minutes=12, seconds=30), "min": timedelta(minutes=21, seconds=50)},
           "female": {"max": timedelta(minutes=14, seconds=40), "min": timedelta(minutes=28)}}


class RunningScore(Score):
    def __init__(self, army_id: int, score_date: str, distance: float, duration: timedelta, moed: str, name: str):
        super().__init__(army_id, score_date, moed, name)
        self.distance = distance
        self.duration = duration
        self.grade = self.calculate_grade(self.gender)
        self.passed = self.grade >= 60

    def to_json(self) -> Dict:
        return {
            "army_id": self.army_id,
            "date": self.score_date,
            "distance": self.distance,
            "duration": str((datetime.min + self.duration).time()),
            "duration_in_minutes": self.duration.total_seconds() / 60,
            "moed": self.moed,
            "grade": self.grade,
            "passed": self.passed,
            "name": self.name,
            "gender": self.gender,
            "years_old": self.years_old,
            "team": self.team
        }

    def calculate_grade(self, gender: str):
        grade = 100 * ((self.duration - GRADING[gender]["min"]) / (GRADING[gender]["max"] - GRADING[gender]["min"]))
        if grade > 100:
            grade = 100
        if grade < 0:
            grade = 0
        return grade
