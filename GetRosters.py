from teams import teamIDs
from inputs import getRosterEndpoint, pstnow
import SendRequest

def getAllRosters(year = "2024"):
    # invert the team IDs dictionary so we can get managers by ID
    teamManagersByID = {v: k for k, v in teamIDs[year].items()}
    rosters = []
    for team in teamIDs[year].values():
        endpoint = getRosterEndpoint(year, team)
        roster = SendRequest.sendRequest(endpoint, "getAllRosters")
        if roster is False:
            return False
        if roster is not None:
            for item in roster:
                item['date'] = str(pstnow)
                item['manager'] = str(teamManagersByID[team])
                rosters.append(item)
        else:
            return False
    return rosters
        