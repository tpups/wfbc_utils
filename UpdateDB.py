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
        # hitting stats will be first in the list
        # TODO - stats are coming in with extra list wrapper
        hit = stats[0][0]
        pitch = stats[0][1]
        hitToUpdate = []
        pitchToUpdate = []
        for doc in hit:
            checkResult = checkPrevious(doc, "hit", isLeagueStats)
            if checkResult is True:
                hitToUpdate.append(doc)
        for doc in pitch:
            checkResult = checkPrevious(doc, "pitch", isLeagueStats)
            if checkResult is True:
                pitchToUpdate.append(doc)
        hitting_result = None
        pitching_result = None
        if hitToUpdate:
            hitting_result = hittingBox.insert_many(hitToUpdate)
        if pitchToUpdate:
            pitching_result = pitchingBox.insert_many(pitchToUpdate)

        # delete all docs in collections
        # hitting_result = hittingBox.delete_many({})
        # pitching_result = pitchingBox.delete_many({})

        if pitching_result is not None and hitting_result is not None:
            print("days of box scores retrieved: " + str(len(stats)))
            pprint.pprint(hittingBox.find_one())
            pprint.pprint(pitchingBox.find_one())
            # pprint.pprint(stats)
            return True
        else:
            return False


def checkPrevious(document, type = "", league = True):

    status = { "hit": {}, "pitch": {} }
    # is this the first time data has been entered for this date?
    newData = True
    unchanged = None

    if type is "hit":
        hittingBox = db.league_box_hitting
        if league is False:
            hittingBox = db.team_box_hitting
        teamID = document['teamID']
        stats_date = document['stats_date']
        previous_document = hittingBox.find({"teamID": teamID, "stats_date": stats_date})
        previous_count = str(previous_document.count())
        if previous_document:
            newData = False
            print("found " + previous_count + " previous hitting data for this date")
        cats = ['2B','3B','AB','AVG','BB','CS','GP','H','HBP','HR','K','OPS','PA','R','RBI','SB','SF']
        for cat in cats:
            # check the last document
            if cat in document and cat in previous_document[int(previous_count) - 1]:
                if document[cat] != previous_document[int(previous_count) - 1][cat]:
                    status["hit"][cat] = "values do not match"
                    unchanged = False
            elif cat in document or cat in previous_document[int(previous_count) - 1]:
                status["hit"][cat] = "only one document contains key"
                unchanged = False

    if type is "pitch":
        pitchingBox = db.league_box_pitching
        if league is False:
            pitchingBox = db.team_box_pitching
        teamID = document['teamID']
        stats_date = document['stats_date']
        previous_document = pitchingBox.find({"teamID": teamID, "stats_date": stats_date})
        previous_count = str(previous_document.count())
        if previous_document:
            newData = False
            print("found " + previous_count + " previous pitching data for this date")
        cats = ['BB','BS','ER','ERA','GP','H','HB','HR','IP','K','L','QS','R','SV','W','WHIP','WP']
        for cat in cats:
            if cat in document and cat in previous_document[int(previous_count) - 1]:
                if document[cat] != previous_document[int(previous_count) - 1][cat]:
                    status["pitch"][cat] = "values do not match"
                    unchanged = False
            elif cat in document or cat in previous_document[int(previous_count) - 1]:
                status["pitch"][cat] = "only one document contains key"
                unchanged = False

    if newData is True:
        return True
    else:
        return False