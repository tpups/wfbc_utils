
import arrow
from pymongo import MongoClient
import datetime
import json
import csv
import pandas as pd
from io import StringIO
from datetime import date
from UpdateDB import updateBox, testConnection, updateTeams
import GetMlbStats
from GetBoxScoresByDate import getAllLeagueBoxScores
from inputs import utcnow, pstnow, client, seasons, getBoxEndpoint, getTeams, mongoConnect
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

# box = getAllLeagueBoxScores("2019")
# UpdateDB(box, "2019")                
# box = getAllLeagueBoxScores("2020")
# UpdateDB(box, "2020")
# box = getAllLeagueBoxScores("2021")
# UpdateDB(box, "2021")
# box = getAllLeagueBoxScores("2022")
# UpdateDB(box, "2022")
# box = getAllLeagueBoxScores("2023")
# UpdateDB(box, "2023")

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

# league stats
db = mongoConnect("2023")
hittingBox = db.team_box_hitting
pitchingBox = db.team_box_pitching

buildStandings("2023", seasons["2023"]["start"], seasons["2023"]["end"], hittingBox, pitchingBox)

# firstPitch = GetMlbStats.getFirstPitch()
# if firstPitch is False:
#     print('No games on this day')

# TEST DB CONNECTION
# testConnection()
                
# endpoint = getBoxEndpoint("2022", "first", "2022-08-15", "hitting")
# print(endpoint)

# teams = {
#         "Jake" : {
#             "ID" : "600",
#             "TeamName" : "MA⋯CHE⋯TE"
#         },
#         "Joe" : {
#             "ID" : "595",
#             "TeamName" : "Any Given Everyday"
#         },
#         "Josh" : {
#             "ID" : "601",
#             "TeamName" : "Pony Express"
#         },
#         "Justin" : {
#             "ID" : "603",
#             "TeamName" : "Rye Bread and Mustard"
#         },
#         "Rocky" : {
#             "ID" : "602",
#             "TeamName" : "Pube Cruisers"
#         },
#         "Tyler" : {
#             "ID" : "598",
#             "TeamName" : "Chudley Cannons"
#         },
#         "Clint" : {
#             "ID" : "597",
#             "TeamName" : "BilderBillies Group"
#         },
#         "David" : {
#             "ID" : "594",
#             "TeamName" : "Big Ball Chunky Time"
#         },
#         "Mark" : {
#             "ID" : "596",
#             "TeamName" : "Babb Ruth"
#         },
#         "Andy" : {
#             "ID" : "604",
#             "TeamName" : "Series-bound in Seattle"
#         },
#         "Patrick" : {
#             "ID" : "605",
#             "TeamName" : "White Hardness"
#         },
#         "Kent" : {
#             "ID" : "599",
#             "TeamName" : "Kent's Dents"
#         }
# }
# response = updateTeams("2024", teams)