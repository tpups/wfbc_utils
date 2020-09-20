from datetime import datetime
from datetime import date
import SendRequest
from TeamIDs import teamIDs

# 2020 season start = July 23
# 2020 season end = September 27
season_start = date(2020, 7, 23)
season_end = date(2020, 9, 27)
today = date.today()
now = datetime.now()
end = today
if today > season_end:
    end = season_end


def getAllLeagueBoxScores(start = season_start, end = end):

    date = start
    oneDay = datetime.timedelta(1)
    while date <= end:
        if hittingStats is not None:
            for team in hittingStats:
                team['stats_date'] = date
                team['download_date'] = str(now)

        if pitchingStats is not None:
            for team in pitchingStats:
                team['stats_date'] = date
                team['download_date'] = str(now)


# default is get today's league box scores
def getBoxScores(boxDate = today, teamID = "0"):

    # make date string
    year = str(boxDate.year)
    month = str(boxDate.month)
    day = str(boxDate.day)
    if len(month) is 1:
        month = "0" + month
    if len(day) is 1:
        day = "0" + day
    date = year + "-" + month + "-" + day

    # API endpoints
    pitching = "https://www.rotowire.com/mlbcommish20/tables/box.php?leagueID=163&teamID=" + teamID + "&date=" + date + "&borp=P"
    hitting = "https://www.rotowire.com/mlbcommish20/tables/box.php?leagueID=163&teamID=" + teamID + "&date=" + date + "&borp=B"

    # get them stats
    pitchingStats = SendRequest.sendRequest(pitching, "getBoxScores - pitching")
    hittingStats = SendRequest.sendRequest(hitting, "getBoxScores - hitting")

    if hittingStats is not None:
        for team in hittingStats:
            team['stats_date'] = boxDate
            team['download_date'] = str(now)
            for stat in team:
                print(stat + " : " + str(team[stat]))

    if pitchingStats is not None:
        for team in pitchingStats:
            team['stats_date'] = boxDate
            team['download_date'] = str(now)
            for stat in team:
                print(stat + " : " + str(team[stat]))



getBoxScores()