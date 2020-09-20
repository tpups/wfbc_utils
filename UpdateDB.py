from pymongo import MongoClient
import pprint

# mongo stuff
client = MongoClient()
db = client.wfbc2020

# todo - how to insert so can retrieve to compare with most recent pull

def updateBox(stats, isLeagueStats = True):
    if stats is not None:
        # league stats
        hittingBox = db.league_box_hitting
        pitchingBox = db.league_box_pitching
        # team stats
        if isLeagueStats is False:
            hittingBox = db.team_box_hitting
            pitchingBox = db.team_box_pitching
        hit = []
        pitch = []
        for day in stats:
            for team in day:
                # hitting stats will be first in the list
                hit.append(team[0])
                pitch.append(team[1])
        hitting_result = hittingBox.insert_many(hit)
        pitching_result = pitchingBox.insert_many(pitch)
        if pitching_result is not None and hitting_result is not None:
            print("days of box scores retrieved: " + str(len(stats)))
            pprint.pprint(hittingBox.find_one())
            return True
        else:
            return False