from GetBoxScoresByDate import getAllLeagueBoxScores
from UpdateDB import updateBox

box = getAllLeagueBoxScores()

if box is not False:
    # pass in true updates league box
    if updateBox(box, True) is True:
        print('Great Success')
    else:
        print('Unfathomable failure')