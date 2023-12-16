from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import date
import arrow

load_dotenv()
mongopw = os.getenv("mongopw")

# DATES AND TIMES
utcnow = arrow.utcnow()
pstnow = utcnow.to('US/Pacific')
today = pstnow.date()

# League Size
numTeams = 12

# mongo stuff
uri = f"mongodb+srv://admin:{mongopw}@cluster0.nfj4j.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
def mongoConnect(year = "2023"):
    db = client["wfbc" + year]
    return db

# MLB regular season season start and end dates, league IDs
seasons = {
    "2019" : 
    {
        "start" : date(2019, 3, 20),
        "end" : date(2019, 9, 29),
        "leagueID" : "56"
    },
    "2020" : 
    {
        "start" : date(2020, 7, 23),
        "end" : date(2020, 9, 27),
        "leagueID" : "163"
    },
    "2021" : 
    {
        "start" : date(2021, 4, 1),
        "end" : date(2021, 10, 3),
        "leagueID" : "56"
    },
    "2022" : 
    {
        "start" : date(2022, 4, 7),
        "end" : date(2022, 10, 5),
        "leagueID" : "4"
    },
    "2023" : 
    {
        "start" : date(2023, 3, 30),
        "end" : date(2023, 10, 1),
        "leagueID" : "13"
    },
    "2024" :
    {
        "start" : date(2024, 3, 20),
        "end" : date(2024, 9, 29),
        "leagueID" : "62"
    }
}

def getStartDate(year):
    return seasons[year]["start"]

def getEndDate(year):
    return seasons[year]["end"]

# box score endpoint
# https://www.rotowire.com/mlbcommish24/tables/box.php?leagueID=62&teamID=601&borp=B
# roster endpoint
# https://www.rotowire.com/mlbcommish24/tables/rosters.php?leagueID=62&teamID=595

# API endpoints
endpoint = "https://www.rotowire.com/mlbcommish"

def getRosterEndpoint(year, teamID):
    shortYear = year[2:]
    rosterEndpoint = endpoint + shortYear + "/tables/rosters.php?leagueID=" + seasons[year]["leagueID"] + "&teamID=" + teamID
    return rosterEndpoint

def getBoxEndpoint(year, teamID, date, hittingOrPitching):
    shortYear = year[2:]
    boxEndpoint = endpoint + shortYear + "/tables/box.php?leagueID=" + seasons[year]["leagueID"] + "&teamID=" + teamID + "&borp=" + ("B" if hittingOrPitching == "hitting" else "P")
    return boxEndpoint