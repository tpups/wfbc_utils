
import arrow
from pymongo import MongoClient
import datetime
import json
import csv
import pandas as pd
from io import StringIO
from datetime import date
from UpdateDB import updateBox, testConnection
import GetMlbStats
from GetBoxScoresByDate import getAllLeagueBoxScores
from inputs import utcnow, pstnow, client
from BuildStandings import buildStandings
from GetRosters import getAllRosters

def UpdateDB(box, year):
    if box is not False:
        # pass in true updates league box, false for team box
        for team in box:
            updateResult = updateBox(year, team, False)
            if updateResult['newEntry'] is True:
                print('New box scores were added')
            if updateResult['updateExisting'] is True:
                print('Existing box scores were updated')
            elif updateResult['newEntry'] is False and updateResult['updateExisting'] is False:
                print('No box scores to update')

# create timezone-aware(double check this) date to pass in:
# dz = arrow.get(datetime(2020, 9, 24), 'US/Pacific').date()

# file = open('2023.json')
# box = json.load(file)
                
box = getAllLeagueBoxScores("2021")
UpdateDB(box, "2021")
# box = getAllLeagueBoxScores("2020")
# UpdateDB(box, "2020")
# box = getAllLeagueBoxScores("2019")
# UpdateDB(box, "2019")

# CREATE BOX SCORE JSON
# json_box = json.dumps(box)
# with open("2023.json", "w") as outfile:
#     outfile.write(json_box)

# CREATE ROSTERS CSV
# rosters = json.dumps(getAllRosters("2024"))
# f = pd.read_json(StringIO(rosters))
# keep_col = ['manager', 'player', 'team']
# new_f = f[keep_col]
# new_f.to_csv("rosters.csv", index=False)

# # league stats
# hittingBox = db.league_box_hitting
# pitchingBox = db.league_box_pitching

# buildStandings(season_start, season_end, hittingBox, pitchingBox)

# firstPitch = GetMlbStats.getFirstPitch()
# if firstPitch is False:
#     print('No games on this day')

# TEST DB CONNECTION
# testConnection()