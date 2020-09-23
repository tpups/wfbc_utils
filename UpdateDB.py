from pymongo import MongoClient
import pprint
import datetime
from datetime import date
import arrow
from BuildStandings import buildStandings

utcnow = arrow.utcnow()
pstnow = utcnow.to('US/Pacific')
season_start = date(2020, 7, 23)
season_end = date(2020, 9, 27)

# mongo stuff
client = MongoClient()
db = client.wfbc2020
# league stats
hittingBox = db.league_box_hitting
pitchingBox = db.league_box_pitching

# todo - how to insert so can retrieve to compare with most recent pull

def updateBox(stats, isLeagueStats = True):

    if stats is not None:
        pprint.pprint(stats)
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
        updateExisting = False
        newEntry = False
        for doc in hit:
            checkResult = checkPrevious(doc, "hit", isLeagueStats)
            if checkResult['newEntry'] is True:
                hitToUpdate.append(doc)
            if checkResult['updateExisting'] is True:
                updateExisting = True
        for doc in pitch:
            checkResult = checkPrevious(doc, "pitch", isLeagueStats)
            if checkResult['newEntry'] is True:
                pitchToUpdate.append(doc)
            if checkResult['updateExisting'] is True:
                updateExisting = True

        hitting_result = None
        pitching_result = None
        if len(hitToUpdate) > 0:
            hitting_result = hittingBox.insert_many(hitToUpdate)
            newEntry = True
        if len(pitchToUpdate):
            pitching_result = pitchingBox.insert_many(pitchToUpdate)
            newEntry = True

        # delete all docs in collections
        # hitting_result = hittingBox.delete_many({})
        # pitching_result = pitchingBox.delete_many({})

        print("days of box scores retrieved: " + str(len(stats)))
        return {'newEntry': newEntry,
                'updateExisting': updateExisting}


def checkPrevious(document, side = "", league = True):

    if side != "":
        status = { "hit": {}, "pitch": {} }
        # is this the first time data has been entered for this date?
        newEntry = True
        updateExisting = False
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
            newEntry = False
            # print("found " + str(previous_count) + " previous (" + side + ") data for this date")
            previous_document = previous_documents[previous_count - 1]
            for cat in cats:
                # check the last document
                if cat in document and cat in previous_document:
                    if document[cat] != previous_document[cat]:
                        status["hit"][cat] = "values do not match"
                        updateExisting = True
                        update_result = updateDocument(collection, previous_document['_id'], cat, previous_document[cat], document[cat])
                        # print("number of documents updated: " + str(update_result))
                elif cat in document or cat in previous_document:
                    status["hit"][cat] = "only one document contains key"
                    updateExisting = True

        return {'newEntry': newEntry,
                'updateExisting': updateExisting}
    else:
        return


def updateDocument(db, _id, cat, old_value = None, new_value = None):

    # let's make updates a list of strings
    updates = []
    doc = db.find_one({"_id": _id})
    if 'updates' in doc:
        updates = doc['updates']
    # add something about the update
    updates.append(str(pstnow) + " ::: changed " + str(cat) + " from " + str(old_value) + " to " + str(new_value))
    # make the update
    result = db.update_one( {"_id": _id}, {"$set": {cat:new_value, "updates": updates}}, upsert=True )
    # return the number of documents updated
    return result.modified_count

def updateStandings(startDate = season_start, endDate = season_end):
    standings = buildStandings(startDate, endDate, hittingBox, pitchingBox)