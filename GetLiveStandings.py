import json
import requests
import datetime
import pymongo
import GetStandings

wfbcLiveStats = "https://www.rotowire.com/mlbcommish20/tables/standings-live.php?leagueID=163&type=S&divisionID=0"
wfbcLiveRanks = "https://www.rotowire.com/mlbcommish20/tables/standings-live.php?leagueID=163&type=R&divisionID=0"

standings = GetStandings.getStandings(wfbcLiveStats)
standings = standings[0]

print(type(standings))

if standings is not None:
    print("Standings:")
    # for team in standings:
    #     print(team)
    print("teamname : " + standings["teamname"])
    print("teamID : " + standings["teamID"])
    print("owner : " + standings["owner"])
    print("cat_4 (HR) : " + str(standings["cat_4"]))
    print("cat_5 (RBI) : " + str(standings["cat_5"]))
    print("cat_6 (SB) : " + str(standings["cat_6"]))
    print("cat_13 (R) : " + str(standings["cat_13"]))
    print("cat_16 (AVG) : " + str(standings["cat_16"]))
    print("cat_21 (OPS) : " + str(standings["cat_21"]))
    print("cat_30 (SV) : " + str(standings["cat_30"]))
    print("cat_32 (IP) : " + str(standings["cat_32"]))
    print("cat_33 (K) : " + str(standings["cat_33"]))
    print("cat_45 (WHIP) : " + str(standings["cat_45"]))
    print("cat_46 (ERA) : " + str(standings["cat_46"]))
    print("cat_86 (QS) : " + str(standings["cat_86"]))
    print("TOT : " + str(standings["TOT"]))



from pymongo import MongoClient
client = MongoClient()
db = client.wfbc