from datetime import time, timedelta
from typing import Dict

from events.event import Event, Score
from scores.running_score import RunningScore


class Running(Event):
    def __init__(self, name: str, event_date: str):
        super().__init__(name, event_date)

    def score_from_json(self, params: Dict) -> "Score":
        army_id = params["army_id"]
        distance = params["distance"]

        start_time = time.fromisoformat(params["start_time"])
        end_time = time.fromisoformat(params["end_time"])

        start_delta = timedelta(hours=start_time.hour, minutes=start_time.minute, seconds=start_time.second)
        end_delta = timedelta(hours=end_time.hour, minutes=end_time.minute, seconds=end_time.second)
        duration = end_delta - start_delta

        moed = params["moed"]

        return RunningScore(army_id, self.event_date, distance, duration, moed, self.name)
