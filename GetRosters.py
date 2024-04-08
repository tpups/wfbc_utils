from inputs import getRosterEndpoint, pstnow, getTeams
import SendRequest

def getAllRosters(year = "2024"):
    teams = getTeams(year)
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
                item['manager'] = str(team['manager'])
                rosters.append(item)
        else:
            return False
    return rosters
        