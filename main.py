from GetBoxScoresByDate import getAllLeagueBoxScores
from UpdateDB import updateBox
from GetMlbStats import getFirstPitch

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

getFirstPitch()