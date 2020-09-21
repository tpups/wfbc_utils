from GetBoxScoresByDate import getAllLeagueBoxScores
from UpdateDB import updateBox

box = getAllLeagueBoxScores()

if box is not False:
    # pass in true updates league box, false for team box
    if updateBox(box, True) is True:
        print('Box scores were updated')
    else:
        print('No box scores to update')