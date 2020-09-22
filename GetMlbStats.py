import statsapi
import arrow

utcnow = arrow.utcnow()
pstnow = utcnow.to('US/Pacific')
today = pstnow.date()
formatToday = pstnow.format('MMMM Do, YYYY')

# TODO : any way to get MLB league-wide stats? Need to calculate cFIP


def getFirstPitch(gamesDate=today):

    schedule = statsapi.schedule(gamesDate)
    dayFirstPitch = None
    firstGames = []
    for game in schedule:
        gameFirstPitch = arrow.get(game['game_datetime'])
        if dayFirstPitch is None or gameFirstPitch <= dayFirstPitch:
            dayFirstPitch = arrow.get(game['game_datetime'])
            firstGames.append(game)
    pstFirstPitch = dayFirstPitch.to('US/Pacific')
    formatFirstPitch = pstFirstPitch.format('h:mm A ZZZ')
    print('First pitch on ' + formatToday + ' is at ' + formatFirstPitch)
    print('First games count: ' + str(len(firstGames)))

    return pstFirstPitch


getFirstPitch()