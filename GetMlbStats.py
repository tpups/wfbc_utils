import statsapi
import arrow
from datetime import datetime

utcnow = arrow.utcnow()
pstnow = utcnow.to('US/Pacific')
today = pstnow.date()
formatToday = pstnow.format('MMMM Do, YYYY')

# TODO : any way to get MLB league-wide stats? Need to calculate cFIP


# returns a list of games
def getSchedule(gamesDate = today, rangeEndDate = None):

    if rangeEndDate is None:
        schedule = statsapi.schedule(gamesDate)
        return schedule
    if rangeEndDate is not None:
        schedule = statsapi.schedule(start_date=gamesDate,end_date=rangeEndDate)
        return schedule


def getFirstPitch(gamesDate = today):

    schedule = getSchedule(gamesDate)
    dayFirstPitch = None
    firstGames = []
    for game in schedule:
        # second game in a double header seems to get a game_datetime of 8:33 PM PST the previous day (12:33 AM EST the same day)
        # - makes second game of doubleheaders appear as earliest game if we don't filter them out
        # scheduled playoff games w/o a start time appear to get 12:33AM PST the same day (7:33ET)
        gameFirstPitch = arrow.get(game['game_datetime'])
        pstGameFirstPitch = gameFirstPitch.to('US/Pacific')
        if pstGameFirstPitch.date() == arrow.get(gamesDate).date():
            if dayFirstPitch is None or gameFirstPitch <= dayFirstPitch:
                dayFirstPitch = arrow.get(game['game_datetime'])
                # we need to remove all other games added to firstGames if this game is earlier
                if gameFirstPitch < dayFirstPitch:
                    firstGames = []
                firstGames.append(game)
        # print('*******************') 
        # print('first pitch : ' + str(gameFirstPitch))
        # print('first pitch : ' + str(pstGameFirstPitch))
        # print('status : ' + game['status'])
        # print('game_type : ' + game['game_type'])
        # print('doubleheader : ' + game['doubleheader'])
        # print('current_inning : ' + str(game['current_inning']))
        # print('away_name : ' + game['away_name'])
        # print('home_name : ' + game['home_name'])
        # print('*******************') 
    if dayFirstPitch is not None:
        pstFirstPitch = dayFirstPitch.to('US/Pacific')
        formatFirstPitch = pstFirstPitch.format('h:mm A ZZZ')
        formatGamesDate = pstFirstPitch.format('MMMM Do, YYYY')
        print('First pitch on ' + formatGamesDate + ' is at ' + formatFirstPitch)
        print('First games count: ' + str(len(firstGames)))
        return pstFirstPitch
    else:
        return False




