from pymongo import MongoClient
import pprint
import datetime

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

        if pitching_result is not None or hitting_result is not None:
            print("days of box scores retrieved: " + str(len(stats)))
            pprint.pprint(hittingBox.find_one())
            pprint.pprint(pitchingBox.find_one())
            return True
        else:
            return False


def checkPrevious(document, side = "", league = True):

    if side != "":
        status = { "hit": {}, "pitch": {} }
        # is this the first time data has been entered for this date?
        newDate = True
        unchanged = None
        collection = None

        if side is "hit":
            cats = ['2B','3B','AB','AVG','BB','CS','GP','H','HBP','HR','K','OPS','PA','R','RBI','SB','SF']
            collection = db.league_box_hitting
            if league is False:
                collection = db.team_box_hitting
        if side is "pitch":
            cats = ['BB','BS','ER','ERA','GP','H','HB','HR','IP','K','L','QS','R','SV','W','WHIP','WP']
            collection = db.league_box_pitching
            if league is False:
                collection = db.team_box_pitching

        teamID = document['teamID']
        stats_date = document['stats_date']
        previous_documents = collection.find({"teamID": teamID, "stats_date": stats_date})
        previous_document = None
        previous_count = previous_documents.count()

        if previous_count != 0:
            newDate = False
            # print("found " + str(previous_count) + " previous (" + side + ") data for this date")
            previous_document = previous_documents[previous_count - 1]
            for cat in cats:
                # check the last document
                if cat in document and cat in previous_document:
                    if document[cat] != previous_document[cat]:
                        status["hit"][cat] = "values do not match"
                        unchanged = False
                        update_result = updateDocument(collection, previous_document['_id'], cat, previous_document[cat], document[cat])
                        print("number of documents updated: " + str(update_result))
                elif cat in document or cat in previous_document:
                    status["hit"][cat] = "only one document contains key"
                    unchanged = False

        if newDate is True:
            return True
        else:
            return False
    else:
        return


def updateDocument(db, _id, cat, old_value = None, new_value = None):

    # let's make updates a list of strings
    updates = []
    doc = db.find_one({"_id": _id})
    if doc['updates']:
        updates = doc['updates']
    # add something about the update
    updates.append(datetime.datetime.now() + " ::: changed " + cat + " from " + old_value + " to " + new_value)
    # make the update
    result = db.update_one( {"_id": _id}, {"$set": {cat:new_value, "updates": updates}}, upsert=True )
    # return the number of documents updated
    return result['modifiedCount']