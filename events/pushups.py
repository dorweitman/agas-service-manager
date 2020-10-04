from typing import Dict

from events.event import Event, Score
from scores.pushups_score import PushUpsScore


class PushUps(Event):
    def __init__(self):
        super().__init__()

    def score_from_json(self, params: Dict) -> "Score":
        name = params["name"]
        event_date = params["event_date"]
        army_id = params["army_id"]
        moed = params["moed"]
        pushups = int(params["pushups"])

        return PushUpsScore(army_id, event_date, moed, pushups, name)
