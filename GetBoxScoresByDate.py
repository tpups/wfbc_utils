import datetime
from datetime import date
from time import sleep
import arrow
import SendRequest
from inputs import getStartDate, getEndDate, getBoxEndpoint, utcnow, pstnow, today
from teams import teamIDs



def getAllLeagueBoxScores(year = "2023"):
    start = getStartDate(year)
    end = getEndDate(year)
    if today < end:
        print("getting box scores through today")
        end = today
    oneDay = datetime.timedelta(1)

    combinedBoxScores = []
    for team in teamIDs[year].values():
        boxScores = []
        date = start
        while date <= end:
            box = getBoxScores(year, date, team)
            if box is not False:
                # add as a list of two lists [hit, pitch]
                boxScores.append(box)
                date = date + oneDay
                # wait half a sec
                sleep(0.125)
            else:
                print("did not get box scores")
        combinedBoxScores.append(boxScores)
    return combinedBoxScores


# default is get today's league box scores
def getBoxScores(year, boxDate = today, teamID = "0"):

    # make date string
    year = str(boxDate.year)
    month = str(boxDate.month)
    day = str(boxDate.day)
    if len(month) == 1:
        month = "0" + month
    if len(day) == 1:
        day = "0" + day
    date = year + "-" + month + "-" + day

    print(date + " team ID: " + teamID)

    pitching = getBoxEndpoint(year, teamID, date, "pitching")
    hitting = getBoxEndpoint(year, teamID, date, "hitting")

    # get them stats
    pitchingStats = SendRequest.sendRequest(pitching, "getBoxScores - pitching")
    hittingStats = SendRequest.sendRequest(hitting, "getBoxScores - hitting")
    if pitchingStats is False or hittingStats is False:
        return False
    new_hittingStats = []
    new_pitchingStats = []

    # add to lists
    if hittingStats is not None:
        for item in hittingStats:
            item['teamID'] = teamID
            item['stats_date'] = str(boxDate)
            item['download_date'] = str(pstnow)
            new_hittingStats.append(item)
    else:
        return False
    if pitchingStats is not None:
        for item in pitchingStats:
            item['teamID'] = teamID
            item['stats_date'] = str(boxDate)
            item['download_date'] = str(pstnow)
            new_pitchingStats.append(item)
    else:
        return False

    # returns list of two lists
    return [new_hittingStats, new_pitchingStats]