import arrow
from datetime import datetime
from GetBoxScoresByDate import getAllLeagueBoxScores
from UpdateDB import updateBox
import GetMlbStats

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


# create date to pass in:
# games_date = arrow.get(datetime(2020, 9, 24), 'US/Pacific').date()
# end_date = arrow.get(datetime(2020, 10, 3), 'US/Pacific').date()

firstPitch = GetMlbStats.getFirstPitch()
if firstPitch is False:
    print('no games on this day')

# test = GetMlbStats.getSchedule(games_date, end_date)
# print('Got ' + str(len(test)) + ' games')