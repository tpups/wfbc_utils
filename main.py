import arrow
from pymongo import MongoClient
import datetime
import json
import csv
import pandas as pd
from io import StringIO
from datetime import date
from UpdateDB import updateBox, db
import GetMlbStats
from GetBoxScoresByDate import getAllLeagueBoxScores
from inputs import utcnow, pstnow, db
from BuildStandings import buildStandings
from GetRosters import getAllRosters

# create timezone-aware(double check this) date to pass in:
# dz = arrow.get(datetime(2020, 9, 24), 'US/Pacific').date()

# box = getAllLeagueBoxScores("2023")
# json_box = json.dumps(box)
# with open("2023.json", "w") as outfile:
#     outfile.write(json_box)

rosters = json.dumps(getAllRosters("2024"))
f = pd.read_json(StringIO(rosters))
keep_col = ['manager', 'player', 'team']
new_f = f[keep_col]
new_f.to_csv("rosters.csv", index=False)


# rosters_keys = rosters[0].keys()
# with open("rosters.csv", "w", encoding='utf8', newline='') as outfile:
#     fieldnames = ['manager', 'player', 'team']
#     writer = csv.DictWriter(outfile, rosters_keys)
#     writer.writeheader()
#     for player in rosters:
#         writer.writerow(player)


# if box is not False:
#     # pass in true updates league box, false for team box
#     updateResult = updateBox(box, True)
#     if updateResult['newEntry'] is True:
#         print('New box scores were added')
#     if updateResult['updateExisting'] is True:
#         print('Existing box scores were updated')
#     elif updateResult['newEntry'] is False and updateResult['updateExisting'] is False:
#         print('No box scores to update')

# # league stats
# hittingBox = db.league_box_hitting
# pitchingBox = db.league_box_pitching

# buildStandings(season_start, season_end, hittingBox, pitchingBox)

# firstPitch = GetMlbStats.getFirstPitch()
# if firstPitch is False:
#     print('No games on this day')