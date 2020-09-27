from typing import Type

from events.event import Event
from events.pushups import PushUps
from events.running import Running

EVENT_TYPE_MAPPING = {"run": Running, "pushups": PushUps}


class EventMaker:
    def __init__(self, event_type: str):
        self.event_type: Type = EVENT_TYPE_MAPPING[event_type]

    def make_event(self, name: str, event_date: str) -> Event:
        event: Event = self.event_type(name, event_date)
        return event
