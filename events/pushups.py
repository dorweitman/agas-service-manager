from typing import Dict

from events.event import Event, Score
from scores.pushups_score import PushUpsScore


class PushUps(Event):
    def __init__(self, name: str, event_date: str):
        super().__init__(name, event_date)

    def score_from_json(self, params: Dict) -> "Score":
        army_id = params["army_id"]
        moed = params["moed"]
        pushups = params["pushups"]

        return PushUpsScore(army_id, self.event_date, moed, pushups, self.name)
