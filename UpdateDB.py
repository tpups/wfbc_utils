from pymongo import MongoClient

# mongo stuff
client = MongoClient()
db = client.wfbc2020
pitchingBox = db.league_box_pitching
hittingBox = db.league_box_hitting