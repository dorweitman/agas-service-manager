from abc import ABC, abstractmethod
from typing import List, Dict

from scores.score import Score


class Event(ABC):
    def __init__(self):
        self.scores: List[Score] = []

    @abstractmethod
    def score_from_json(self, params: Dict) -> "Score":
        pass

    def _add_score(self, result: Dict) -> None:
        self.scores.append(self.score_from_json(result))

    def add_scores(self, results: List[Dict]) -> None:
        for result in results:
            self._add_score(result)

    def publish_scores(self) -> List[Dict]:
        return [score.to_json() for score in self.scores]
