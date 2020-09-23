from decimal import Decimal
from pymongo import MongoClient
from datetime import date
import pprint
import GetStats
from TeamIDs import teamIDsByManager, teamManagersByID, teamNamesByID
from inputs import numTeams, season_start, season_end, db

# TODO
# 1) Build standings as they were on this date
# 2) Build standings after box scores from postponed games have been retroactively added

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
                for manager in teamIDsByManager:
                    team = teamTotals[teamIDsByManager[manager]]['hit']
                    hittingStat = None
                    if cat == 'AVG':
                        hittingStat = GetStats.getAVG(int(team['H']), int(team['AB']))
                    elif cat == 'OPS':
                        obp = GetStats.getOBP(int(team['AB']), int(team['H']), int(team['BB']), int(team['HBP']), int(team['SF']))
                        totalBases = GetStats.getTotalBases(int(team['H']), int(team['2B']), int(team['3B']), int(team['HR']))
                        slg = GetStats.getSLG(totalBases, int(team['AB']))
                        hittingStat = GetStats.getOPS(obp, slg)
                    else:
                        hittingStat = int(team[cat])
                    hitting[cat].append({ 'teamID': teamIDsByManager[manager], 'value': hittingStat, 'manager': manager, 'name': teamNamesByID[teamIDsByManager[manager]] })

            for cat in pitchingCats:
                pitching[cat] = []
                for manager in teamIDsByManager:
                    team = teamTotals[teamIDsByManager[manager]]['pitch']
                    pitchingStat = None
                    if cat == 'ERA':
                        pitchingStat = GetStats.getERA(int(team['ER']), Decimal(team['IP']))
                    elif cat == 'WHIP':
                        pitchingStat = GetStats.getWHIP(int(team['H']), int(team['BB']), Decimal(team['IP']))
                    elif cat == 'IP':
                        pitchingStat = Decimal(team[cat])
                    else:
                        pitchingStat = int(team[cat])
                    pitching[cat].append({ 'teamID': teamIDsByManager[manager], 'value': pitchingStat, 'manager': manager, 'name': teamNamesByID[teamIDsByManager[manager]] })
        except:
            return False

        hittingPoints = {}
        pitchingPoints = {}
        for cat in hittingCats:
            statTotals = hitting[cat]
            sortedTotals = sorted(statTotals, key = lambda i: i['value'], reverse=True)
            
            i = 0
            while i < len(sortedTotals):
                team = sortedTotals[i]
                nextValue = None
                n = i + 1
                count = 1
                while n < len(sortedTotals):
                    if sortedTotals[n] is not None:
                        nextValue = sortedTotals[n]['value']
                        if nextValue == team['value']:
                            count += 1
                            n += 1
                        else:
                            break

                if count > 1:
                    # print("found tie : " + str(count) + " tied teams")
                    tiedPointsTotal = 0
                    for p in range(count):
                        tiedPointsTotal += points[i + p]
                    pointsEach = Decimal(tiedPointsTotal / count)
                    onePlace = Decimal('1.1')
                    team['points'] = str(pointsEach.quantize(onePlace))
                    # assign points to the other tied teams as they will be skipped by i+= count
                    for t in range(count - 1):
                        idx = i + t + 1
                        sortedTotals[idx]['points'] = str(pointsEach.quantize(onePlace))
                else:
                    team['points'] = points[i]

                i += count
            hittingPoints[cat] = sortedTotals
        
        teamTotals = {}
        for cat in hittingPoints:
            for team in hittingPoints[cat]:
                if team['teamID'] in teamTotals:
                    teamTotals[team['teamID']]['total'] += Decimal(team['points'])
                else:
                    teamTotals[team['teamID']] = {'total': Decimal(team['points'])}
                teamTotals[team['teamID']][cat] = team['points']
        totalPoints = []
        # teamID is the key so we should add kv pair so it's not lost
        for team in teamTotals:
            teamTotals[team]['teamID'] = team
            totalPoints.append(teamTotals[team])
        
        hittingPoints['totals'] = sorted(totalPoints, key = lambda i: i['total'], reverse=True)
        for team in hittingPoints['totals']:
            print("ID: " + str(team['teamID']) + " ::: " + str(team['total']) + " Points")


        return True


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

    return totals