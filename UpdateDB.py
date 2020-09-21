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
                checkResult = checkPrevious(team[0], type="hit")
        hitting_result = hittingBox.insert_many(hit)
        pitching_result = pitchingBox.insert_many(pitch)
        if pitching_result is not None and hitting_result is not None:
            print("days of box scores retrieved: " + str(len(stats)))
            pprint.pprint(hittingBox.find_one())
            pprint.pprint(pitchingBox.find_one())
            
            return True
        else:
            return False


def checkPrevious(document, type = "", league = True):
    if type is "hit":
        hittingBox = db.league_box_hitting
        if league is False:
            hittingBox = db.team_box_hitting
        teamID = document['teamID']
        stats_date = document['stats_date']
        previous_document = hittingBox.find({"teamID": teamID, "stats_date": stats_date})
        print(str(previous_document.count()) + " matches found")
        cats = ['2B','3B','AB','AVG','BB','CS','GP','H','HBP','HR','K','OPS','PA','R','RBI','SB','SF']
        for cat in cats:
            if cat in document and cat in previous_document[0]:
                if document[cat] != previous_document[0][cat]:
                    print("mismatch - values do not match")
            elif cat in document or cat in previous_document[0]:
                print("mismatch - only one document contains key")
        # for cat in previous_document[0]:
        #     print(cat)

        return True
