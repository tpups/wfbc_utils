from pymongo import MongoClient

# mongo stuff
client = MongoClient()
db = client.wfbc2020

def updateBox():
    pitchingBox = db.league_box_pitching
    hittingBox = db.league_box_hitting