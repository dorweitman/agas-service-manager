from typing import Dict

from scores.score import Score


GRADING = {"male": {"max": 36, "min": -16.5}, "female": {"max": 30, "min": -32.5}}


class PushUpsScore(Score):
    def __init__(self, army_id: str, score_date: str, moed: str, pushups: int, name: str):
        super().__init__(army_id, score_date, moed, name)
        self.pushups = pushups
        self.grade = self.calculate_grade(self.gender)
        self.passed = self.grade >= 60

    def to_json(self) -> Dict:
        return {
            "army_id": self.army_id,
            "date": self.score_date,
            "pushups": self.pushups,
            "moed": self.moed,
            "grade": self.grade,
            "passed": self.passed,
            "name": self.name
        }

    def calculate_grade(self, gender: str):
        grade = 100 * ((self.pushups - GRADING[gender]["min"]) / (GRADING[gender]["max"] - GRADING[gender]["min"]))
        if grade > 100:
            grade = 100
        if grade < 0:
            grade = 0
        return grade
