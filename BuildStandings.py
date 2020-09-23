from decimal import Decimal
from pymongo import MongoClient
from datetime import date
import pprint
import GetStats
from TeamIDs import teamIDsByManager, teamManagersByID, teamNamesByID

numTeams = 12

def buildStandings(startDate, endDate, hitDB, pitchDB):

    teamTotals = getTeamTotals(startDate, endDate, hitDB, pitchDB)
    points = list(reversed(range(1, numTeams + 1)))

    if teamTotals is not False:
        hittingCats = ['AVG','OPS','R','SB','HR','RBI']
        pitchingCats = ['ERA','WHIP','IP','K','SV','QS']
        hitting = {}
        pitching = {}
        try:
            for cat in hittingCats:
                hitting[cat] = []
                for teamID in teamIDsByManager:
                    team = teamTotals[teamIDsByManager[teamID]]['hit']
                    hittingStat = None
                    if cat == 'AVG':
                        hittingStat = GetStats.getAVG(int(team['H']), int(team['AB']))
                        # print(hittingStat)
                    elif cat == 'OPS':
                        obp = GetStats.getOBP(int(team['AB']), int(team['H']), int(team['BB']), int(team['HBP']), int(team['SF']))
                        totalBases = GetStats.getTotalBases(int(team['H']), int(team['2B']), int(team['3B']), int(team['HR']))
                        slg = GetStats.getSLG(totalBases, int(team['AB']))
                        hittingStat = GetStats.getOPS(obp, slg)
                        # print(hittingStat)
                    else:
                        hittingStat = int(team[cat])
                        # print(hittingStat)
                    hitting[cat].append({ 'teamID': teamIDsByManager[teamID], 'value': hittingStat })

            for cat in pitchingCats:
                pitching[cat] = []
                for teamID in teamIDsByManager:
                    team = teamTotals[teamIDsByManager[teamID]]['pitch']
                    pitchingStat = None
                    if cat == 'ERA':
                        pitchingStat = GetStats.getERA(int(team['ER']), Decimal(team['IP']))
                        # print(pitchingStat)
                    elif cat == 'WHIP':
                        pitchingStat = GetStats.getWHIP(int(team['H']), int(team['BB']), Decimal(team['IP']))
                        # print(pitchingStat)
                    elif cat == 'IP':
                        pitchingStat = Decimal(team[cat])
                        # print(pitchingStat)
                    else:
                        pitchingStat = int(team[cat])
                        # print(pitchingStat)
                    pitching[cat].append({ 'teamID': teamIDsByManager[teamID], 'value': pitchingStat })
        except:
            return False

        hittingPoints = {}
        pitchingPoints = {}
        for cat in hittingCats:
            statTotals = hitting[cat]
            sortedTotals = sorted(statTotals, key = lambda i: i['value'], reverse=True)
            print(cat)
            print("###############")
            
            i = 0
            while i < len(sortedTotals):
                team = sortedTotals[i]
                owner = teamManagersByID[team['teamID']]
                name = teamNamesByID[team['teamID']]
                team['manager'] = owner
                team['name'] = name
                print(owner + "(" + name +  ") : " + str(team['value']))

                nextValue = None
                n = i + 1
                count = 1
                while n < len(sortedTotals):
                    if sortedTotals[n] is not None:
                        nextValue = sortedTotals[n]
                        if nextValue == team['value']:
                            count += 1
                            n += 1
                        else:
                            break
                if count > 1:
                    temp = "temp"
                i += count

            print("###############")
            print(points)





# Build standings as they were on this date

# Build standings after box scores from postponed games have been retroactively added

def getTeamTotals(startDate, endDate, hitDb, pitchDb):

    try:
        totals = {}
        for teamID in teamIDsByManager:
            totals[teamIDsByManager[teamID]] = { "hit" : {}, "pitch": {} }
        hitBoxScores = hitDb.find( { "$and": [ { "stats_date": { "$gte": str(startDate) } }, { "stats_date": { "$lte": str(endDate) } } ] } )
        pitchBoxScores = pitchDb.find( { "$and": [ { "stats_date": { "$gte": str(startDate) } }, { "stats_date": { "$lte": str(endDate) } } ] } )
        hStats = ['2B','3B','AB','BB','H','HBP','HR','PA','R','RBI','SB','SF']
        pStats = ['BB','ER','H','HB','IP','K','QS','SV']

        for score in hitBoxScores:
            team = totals[score["teamID"]]["hit"]
            for stat in hStats:
                if stat in score:
                    if stat not in team:
                        team[stat] = score[stat]
                    else:
                        currentTotal = team[stat]
                        newTotal = int(currentTotal) + int(score[stat])
                        team[stat] = newTotal
                        
        for score in pitchBoxScores:
            team = totals[score["teamID"]]["pitch"]
            for stat in pStats:
                if stat in score:
                    # we can't keep adding IP b/c they are inexact values and would cause issues
                    # multiply IP by 3 and round to nearest int = outs
                    # divide by 3 is innings
                    if stat == "IP":
                        innings = Decimal(score[stat])
                        if stat not in team:
                            team[stat] = score[stat]
                        else:
                            currentTotal = Decimal(team[stat])
                            newTotal = currentTotal + innings
                            outs = Decimal(newTotal * 3).to_integral_value()
                            twoPlaces = Decimal('0.01')
                            # round to two decimal places
                            newIP = (outs / 3).quantize(twoPlaces)
                            team[stat] = str(newIP)
                    elif stat not in team:
                        team[stat] = score[stat]
                    else:
                        currentTotal = team[stat]
                        newTotal = int(currentTotal) + int(score[stat])
                        team[stat] = str(newTotal)
    except:
        return False
    # josh = teamIDsByManager["Josh"]
    # print(josh)
    # joshTotals = totals[josh]["hit"]
    # runs = joshTotals["R"]
    # joshPitch = totals[josh]["pitch"]
    # er = joshPitch["ER"]
    # print(runs)
    # print(er)
    return totals




# mongo stuff
client = MongoClient()
db = client.wfbc2020
# league stats
hittingBox = db.league_box_hitting
pitchingBox = db.league_box_pitching
season_start = date(2020, 7, 23)
season_end = date(2020, 9, 24)

buildStandings(season_start, season_end, hittingBox, pitchingBox)