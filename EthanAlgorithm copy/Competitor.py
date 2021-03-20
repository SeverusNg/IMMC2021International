import math
from typing import List


class Competitor:
    name: str
    rating: float
    matches: int
    started: bool
    records: List[float]

    def __init__(self, name: str, matches: int):
        self.name = name
        self.rating = 1
        self.started = False
        self.matches = matches
        self.records = []

    def updateRating(self, new_rating):
        self.matches -= 1
        self.rating = new_rating
        self.records.append(self.rating)
        self.started = True

    def depreciate(self, best_rating_in_match, mean_rating_in_match):
        if self.matches <= 0 or not self.started:
            self.records.append(0)
            return
        self.rating *= (1 - self.depreciation(best_rating_in_match, mean_rating_in_match))
        self.records.append(self.rating)

    def depreciation(self, best_rating_in_match, mean_rating_in_match) -> float:
        if self.rating < mean_rating_in_match:
            return 0.1
        elif self.rating > best_rating_in_match:
            x: float = (self.rating - mean_rating_in_match) / (best_rating_in_match - mean_rating_in_match)
            return 0.3 / (math.exp(10 * (x - 1)))
        else:
            x: float = (self.rating - mean_rating_in_match) / (best_rating_in_match - mean_rating_in_match)
            return 0.2 / (1 + math.exp(-10 * (x - 0.5))) + 0.1
