from inputs import getRosterEndpoint, pstnow, getTeams
import SendRequest

def getAllRosters(year = "2024"):
    teams = getTeams(year)
    # invert the team IDs dictionary so we can get managers by ID
    teamManagersByID = {v: k for k, v in teamIDs[year].items()}
    rosters = []
    for team in teams:
        teamID = team['team_id']
        endpoint = getRosterEndpoint(year, teamID)
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
        