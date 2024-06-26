from pymongo import MongoClient
import pprint
import datetime
from datetime import date
import arrow
from inputs import utcnow, pstnow, client, mongoConnect, today, getStartDate, getEndDate
from BuildStandings import buildStandings

def updateTeams(year, teamNames):
    db = mongoConnect(year)
    teams = db.teams
    response = ""
    if teamNames is not None:
        for manager, teamDetails in teamNames.items():
            team = {
                'manager': manager,
                'team_id': teamDetails['ID'],
                'team_name': teamDetails['TeamName']
            }
            team_existing = teams.find_one({'team_id': team['team_id']})
            if team_existing is not None and team['team_id'] is not None:
                result = teams.update_one( {'_id': team_existing['_id']}, {'$set': {'manager':team['manager'], 'team_name':team['team_name']}}, upsert=True )
                response = "updated existing team"
            else:
                result = teams.insert_one(team)
                response = "created new team"
            print(response)
    return

# def updateStandings(year):
#     db = mongoConnect(year)
#     teams = db.teams
#     standings = db.standings
#     hittingBox = db.team_box_hitting
#     pitchingBox = db.team_box_pitching
#     start = getStartDate(year)
#     end = getEndDate(year)
#     if today < end:
#         end = today
#     oneDay = datetime.timedelta(1)
#     date = start
#     while date <= end:
#         result = buildStandings(year, start, end, hittingBox, pitchingBox)
#         if result is not False:
#             update = 


# todo - how to insert so can retrieve to compare with most recent pull

def updateBox(year, stats, isLeagueStats = True):
    db = mongoConnect(year)
    if stats is not None:
        updateExisting = False
        newEntry = False
        # league stats
        hittingBox = db.league_box_hitting
        pitchingBox = db.league_box_pitching
        # team stats
        if isLeagueStats is False:
            hittingBox = db.team_box_hitting
            pitchingBox = db.team_box_pitching

        for day in stats:

            # hitting stats will be first in the list
            hit = day[0]
            pitch = day[1]
            hitToUpdate = []
            pitchToUpdate = []

            for doc in hit:
                checkResult = checkPrevious(doc, db, "hit", isLeagueStats)
                if checkResult['newEntry'] is True:
                    hitToUpdate.append(doc)
                if checkResult['updateExisting'] is True:
                    updateExisting = True
            for doc in pitch:
                checkResult = checkPrevious(doc, db, "pitch", isLeagueStats)
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

        print("days of box scores retrieved: " + str(len(stats)))
        return {'newEntry': newEntry,
                'updateExisting': updateExisting}


def checkPrevious(document, db, side = "", league = True):

    if side != "":
        status = { "hit": {}, "pitch": {} }
        # is this the first time data has been entered for this date?
        newEntry = True
        updateExisting = False
        collection = None

        if side == "hit":
            cats = ['2B','3B','AB','AVG','BB','CS','GP','H','HBP','HR','K','OPS','PA','R','RBI','SB','SF']
            collection = db.league_box_hitting
            if league is False:
                collection = db.team_box_hitting
        if side == "pitch":
            cats = ['BB','BS','ER','ERA','GP','H','HB','HR','IP','K','L','QS','R','SV','W','WHIP','WP']
            collection = db.league_box_pitching
            if league is False:
                collection = db.team_box_pitching

        teamID = document['teamID']
        stats_date = document['stats_date']
        player = document['player']
        position = document['position']
        previous_document = None
        previous_count = collection.count_documents({"teamID": teamID, "stats_date": stats_date, "player": player, "position": position})

        if previous_count != 0:
            previous_documents = collection.find({"teamID": teamID, "stats_date": stats_date, "player": player, "position": position})
            newEntry = False
            # print("found " + str(previous_count) + " previous (" + side + ") data for this date")
            previous_document = previous_documents[previous_count - 1]
            for cat in cats:
                # check the last document
                if cat in document and cat in previous_document:
                    if document[cat] != previous_document[cat]:
                        status["hit"][cat] = "values do not match"
                        updateExisting = True
                        update_result = updateDocument(collection, previous_document['_id'], cat, previous_document
                        [cat], document[cat])
                elif cat in document:
                    status["hit"][cat] = "only one document contains key"
                    updateExisting = True
                    update_result = updateDocument(collection, previous_document['_id'], cat, None, document[cat])

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
    if (old_value is None):
        updates.append(str(pstnow) + " ::: added " + str(cat) + " with value " + str(new_value))
    else:    
        updates.append(str(pstnow) + " ::: changed " + str(cat) + " from " + str(old_value) + " to " + str(new_value))
    # make the update
    result = db.update_one( {"_id": _id}, {"$set": {cat:new_value, "updates": updates}}, upsert=True )
    # return the number of documents updated
    return result.modified_count

# def updateStandings(startDate = season_start, endDate = season_end):
#     standings = buildStandings(startDate, endDate, hittingBox, pitchingBox)
#     return True

def testConnection():
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

def wipeCollection(collection, areYouSure=False):
    if collection is not None and areYouSure is True:
        # delete all docs in collection
        result = collection.delete_many({})
        return result
    else:
        return False
        