import traceback
import math
from decimal import Decimal
from pymongo import MongoClient
from datetime import date
import pprint
import sys
import GetStats
from inputs import numTeams, getTeams

# TODO
# 1) Build standings as they were on this date
# 2) Build standings after box scores from postponed games have been retroactively added

def buildStandings(year, startDate, endDate, hitDB, pitchDB):

    points = list(reversed(range(1, numTeams + 1)))
    teams = getTeams(year)
    teamTotals = getTeamTotals(year, teams, startDate, endDate, hitDB, pitchDB)


    if teamTotals is not False:
        hittingCats = ['AVG','OPS','R','SB','HR','RBI']
        pitchingCats = ['ERA','WHIP','IP','K','S' if year == '2019' else 'SV','QA']
        hitting = {}
        pitching = {}
        try:
            for cat in hittingCats:
                hitting[cat] = []
                for _team in teams:
                    team = teamTotals[_team['team_id']]['hit']
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
                    hitting[cat].append({ 'teamID': _team['team_id'], 'value': hittingStat, 'manager': _team['manager'], 'name': _team['team_name'] })

            for cat in pitchingCats:
                pitching[cat] = []
                for _team in teams:
                    team = teamTotals[_team['team_id']]['pitch']
                    pitchingStat = None
                    if cat == 'ERA':
                        pitchingStat = GetStats.getERA(int(team['ER']), Decimal(team['IP']))
                    elif cat == 'WHIP':
                        pitchingStat = GetStats.getWHIP(int(team['H']), int(team['BB']), Decimal(team['IP']))
                    elif cat == 'IP':
                        pitchingStat = Decimal(team[cat])
                    else:
                        pitchingStat = int(team[cat])
                    pitching[cat].append({ 'teamID': _team['team_id'], 'value': pitchingStat, 'manager': _team['manager'], 'name': _team['team_name'] })
        except:
            print("Unexpected error!!")
            traceback.print_exc()
            return False

        hittingPoints = {}
        pitchingPoints = {}
        # HITTING
        for cat in hittingCats:
            statTotals = hitting[cat]
            sortedTotals = sorted(statTotals, key = lambda i: i['value'], reverse=True)
            
            i = 0
            while i < len(sortedTotals):
                team = sortedTotals[i]
                nextValue = None
                n = i + 1
                count = 1
                # look for ties
                while n < len(sortedTotals):
                    if sortedTotals[n] is not None:
                        nextValue = sortedTotals[n]['value']
                        if nextValue == team['value']:
                            count += 1
                            n += 1
                        else:
                            break
                # if ties, figure out points
                if count > 1:
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
        # PITCHING
        for cat in pitchingCats:
            statTotals = pitching[cat]
            reverse = True
            if cat == "ERA" or cat == "WHIP":
                reverse = False
            sortedTotals = sorted(statTotals, key = lambda i: i['value'], reverse=reverse)
            
            i = 0
            while i < len(sortedTotals):
                team = sortedTotals[i]
                nextValue = None
                n = i + 1
                count = 1
                # look for ties
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
            pitchingPoints[cat] = sortedTotals
        # teamTotals will contain hitting & pitching totals
        teamTotals = {}
        for team in teams:
            teamTotals[team['team_id']] = {
                'totalHit': Decimal(0),
                'totalPitch': Decimal(0),
                'total': Decimal(0),
                'teamID': team['team_id']
            }
        # HITTING
        for cat in hittingPoints:
            for team in hittingPoints[cat]:
                _team = teamTotals[team['teamID']]
                points = team['points']
                _team['totalHit'] += Decimal(points)
                _team[cat] = points
        # PITCHING
        for cat in pitchingPoints:
            for team in pitchingPoints[cat]:
                _team = teamTotals[team['teamID']]
                points = team['points']
                _team['totalPitch'] += Decimal(points)
                _team[cat] = points

        # put teams into a list so we can sort them
        totalPoints = []
        for team in teamTotals:
            _team = teamTotals[team]
            hitPlusPitch = Decimal(_team['totalHit']) + Decimal(_team['totalPitch'])
            _team['hitPlusPitch'] = hitPlusPitch
            totalPoints.append(_team)

        teamManagersByID = {}
        for team in teams:
            teamManagersByID[team['team_id']] = team['manager']
        
        print('### HITTING ###')
        hittingPoints['totals'] = sorted(totalPoints, key = lambda i: i['totalHit'], reverse=True)
        for team in hittingPoints['totals']:
            print("ID: " + str(team['teamID']) + " ::: " + teamManagersByID[str(team['teamID'])] + " ::: " + str(team['totalHit']) + " Points")
        print('### PITCHING ###')
        pitchingPoints['totals'] = sorted(totalPoints, key = lambda i: i['totalPitch'], reverse=True)
        for team in pitchingPoints['totals']:
            print("ID: " + str(team['teamID']) + " ::: " + teamManagersByID[str(team['teamID'])] + " ::: " + str(team['totalPitch']) + " Points")
        print('### STANDINGS ###')
        standings = sorted(totalPoints, key = lambda i: i['hitPlusPitch'], reverse=True)
        for team in standings:
            print("ID: " + str(team['teamID']) + " ::: " + teamManagersByID[str(team['teamID'])] + " ::: " + str(team['hitPlusPitch']) + " Points")
        for cat in hittingPoints:
            if cat != "totals":
                print("---- " + str(cat) + " ---")
                for team in hittingPoints[cat]:
                    print("ID: " + str(team['teamID']) + " ::: " + teamManagersByID[str(team['teamID'])] + " ::: " + str(team['value']) + " ::: " + str(team['points']) + " Points")
        for cat in pitchingPoints:
            if cat != "totals":
                print("---- " + str(cat) + " ---")
                for team in pitchingPoints[cat]:
                    print("ID: " + str(team['teamID']) + " ::: " + teamManagersByID[str(team['teamID'])] + " ::: " + str(team['value']) + " ::: " + str(team['points']) + " Points")

        return {
            'hitting': hitting,
            'pitching': pitching,
            'standings': standings
        }


def getTeamTotals(year, teams, startDate, endDate, hitDb, pitchDb):
    try:
        totals = {}
        for team in teams:
            totals[team['team_id']] = { "hit" : {}, "pitch": {} }
        hitBoxScores = hitDb.find( { "player": "TOT", "position": "A", "$and": [ { "stats_date": { "$gte": str(startDate) } }, { "stats_date": { "$lte": str(endDate) } } ] } )
        pitchBoxScores = pitchDb.find( { "player": "TOT", "position": "A", "$and": [ { "stats_date": { "$gte": str(startDate) } }, { "stats_date": { "$lte": str(endDate) } } ] } )
        # hitBoxScores = hitDb.find( { "$and": [ { "stats_date": { "$gte": str(startDate) } }, { "stats_date": { "$lte": str(endDate) } } ] } )
        # pitchBoxScores = pitchDb.find( { "$and": [ { "stats_date": { "$gte": str(startDate) } }, { "stats_date": { "$lte": str(endDate) } } ] } )
        hStats = ['2B','3B','AB','BB','H','HBP','HR','PA','R','RBI','SB','SF']
        pStats = ['BB','ER','H','HB','IP','K','QS','QA','S' if year == '2019' else 'SV']

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
                        if year == "2019":
                            partialInnings = innings % 1 * Decimal(3.3)
                            _innings = math.floor(innings)
                            innings = _innings + partialInnings
                            # if Decimal.compare(partialInnings, Decimal(0.1)) == 0:
                            #     innings = Decimal(_innings + 0.33)
                            # elif Decimal.compare(partialInnings, Decimal(0.2)) == 0:
                            #     innings = Decimal(_innings + 0.67)
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
        print("Unexpected error!!")
        traceback.print_exc()
        return False

    totals = getQualityAppearances(pitchDb, startDate, endDate, totals)

    return totals

def getQualityAppearances(pitchDb, startDate, endDate, totals):
    pitchBoxScores = pitchDb.find( { "position": "P", "$and": [ { "stats_date": { "$gte": str(startDate) } }, { "stats_date": { "$lte": str(endDate) } } ] } )
    for score in pitchBoxScores:
        if score["player"] != "TOT":
            team = totals[score["teamID"]]["pitch"]
            qa = False
            if "IP" in score:
                ip = Decimal(score["IP"])
                if ip >= 5:
                    er = int(score["ER"])
                    era = GetStats.getERA(er, ip)
                    if era <= 4.5:
                        if "QA" not in team:
                            team["QA"] = 1
                        else:
                            currentTotal = team["QA"]
                            newTotal = int(currentTotal) + 1
                            team["QA"] = str(newTotal)
    return totals