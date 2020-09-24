import arrow
from pymongo import MongoClient
import datetime
from datetime import date
from UpdateDB import updateBox, db
import GetMlbStats
from GetBoxScoresByDate import getAllLeagueBoxScores
from inputs import utcnow, pstnow, season_start, season_end, db
from BuildStandings import buildStandings

# create timezone-aware(double check this) date to pass in:
# dz = arrow.get(datetime(2020, 9, 24), 'US/Pacific').date()


box = getAllLeagueBoxScores()

if box is not False:
    # pass in true updates league box, false for team box
    updateResult = updateBox(box, True)
    if updateResult['newEntry'] is True:
        print('New box scores were added')
    if updateResult['updateExisting'] is True:
        print('Existing box scores were updated')
    elif updateResult['newEntry'] is False and updateResult['updateExisting'] is False:
        print('No box scores to update')

# league stats
hittingBox = db.league_box_hitting
pitchingBox = db.league_box_pitching

buildStandings(season_start, season_end, hittingBox, pitchingBox)

firstPitch = GetMlbStats.getFirstPitch()
if firstPitch is False:
    print('No games on this day')