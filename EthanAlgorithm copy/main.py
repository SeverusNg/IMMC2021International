from typing import List
import csv
from Competitor import Competitor
from compete import run
import os
import pandas as pd
from pandas import DataFrame

snapshot_file = 'snapshot.csv'


def getCompetitor(name, all_competitors):
    for c in all_competitors:
        if c.name == name:
            return c


def getCompetitors(names, all_competitors):
    result = []
    others = []
    for name in names:
        instance = getCompetitor(name, all_competitors)
        if instance is not None:
            result.append(instance)
    for c in all_competitors:
        if not result.__contains__(c):
            others.append(c)
    return result, others


def loadCompetitors():
    competitors_names = {}
    competitors: List[Competitor] = []
    dataset = os.listdir('./matches')
    dataset.sort()
    for file in dataset:
        if file.startswith('.') or not (file.endswith('.xls') or file.endswith('.xlsx')):
            continue
        df: DataFrame = pd.read_excel(os.path.join('./matches', file))
        tmp_names = list(df.iloc[:16, 0])
        for n in tmp_names:
            if not competitors_names.keys().__contains__(n):
                competitors_names[n] = 0
            competitors_names[n] += 1
    for name in competitors_names.keys():
        competitors.append(Competitor(name, competitors_names[name]))
    return competitors


class Match:
    name: str
    path: str
    all_competitors: List[Competitor]
    competitors: List[Competitor]
    rating_sum: float
    best_rating: float
    mean_rating: float

    def __init__(self, path, all_competitors, name="Unknown Match"):
        self.name = name
        self.path = path
        self.all_competitors = all_competitors
        self.competitors = []
        self.rating_sum = 0
        self.best_rating = 0
        self.mean_rating = 0

    def start(self):
        participants, result = run(self.path)
        self.competitors, others = getCompetitors(participants, self.all_competitors)
        for c in self.competitors:
            if self.best_rating < c.rating:
                self.best_rating = c.rating
            self.rating_sum += c.rating
        if len(self.competitors) > 0:
            self.mean_rating = self.rating_sum / len(self.competitors)
        else:
            print('Error no competitor')
        # update competitors
        total_score = 0
        for r in result.keys():
            total_score += result[r]
        for c in self.competitors:
            c.updateRating((result[c.name] / total_score) * self.rating_sum)
        for o in others:
            o.depreciate(self.best_rating, self.mean_rating)
        print(len(self.competitors) + len(others))


with open(snapshot_file, 'w+') as sf:
    recorder = csv.writer(sf)
    pool: List[Competitor] = loadCompetitors()
    matches: List[str] = os.listdir('./matches')
    matches.sort()
    index = 0
    match_names = []
    for match in matches:
        if match.startswith('.') or not (match.endswith('.xls') or match.endswith('.xlsx')):
            continue
        # print(match)
        index += 1
        match = os.path.join('./matches', match)
        m = Match(match, pool, os.path.splitext(os.path.basename(match))[0])
        match_names.append(m.name)
        m.start()
    recorder.writerow(['Competitors/Matches'] + match_names)
    for c in pool:
        # print(len(c.records))
        recorder.writerow([c.name] + c.records)

