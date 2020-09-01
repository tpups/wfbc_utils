import json
import requests
import datetime
import pymongo

datetime_obj = datetime.datetime.now()
time_delta_1day = datetime.timedelta(1)
datetime_obj = datetime_obj - time_delta_1day
year = str(datetime_obj.year)
month = str(datetime_obj.month)
day = str(datetime_obj.day)
if len(month) is 1:
    month = "0" + month
if len(day) is 1:
    day = "0" + day
end_date = year + "-" + month + "-" + day

wfbcStandingsByDate = 'https://www.rotowire.com/mlbcommish20/tables/standings-by-date.php?leagueID=163&divisionID=0&start=2020-07-23&end=' + end_date
wfbcLiveStats = "https://www.rotowire.com/mlbcommish20/tables/standings-live.php?leagueID=163&type=S&divisionID=0"
wfbcLiveRanks = "https://www.rotowire.com/mlbcommish20/tables/standings-live.php?leagueID=163&type=R&divisionID=0"

print(wfbcStandingsByDate)

headers = {
    'Host': 'www.rotowire.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,mt;q=0.8',
    'Cookie': '*****'
}

def getStandings():
    response = requests.get(wfbcStandingsByDate, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        return response.json()
    else:
        return None

standings = getStandings()
standings = standings[0]

print(type(standings))

if standings is not None:
    print("Standings:")
    # for team in standings:
    #     print(team)
    print("teamname : " + standings["teamname"])
    print("teamID : " + standings["teamID"])
    print("owner : " + standings["owner"])
    print("cat_4 (HR) : " + standings["cat_4"])
    print("cat_5 (RBI) : " + standings["cat_5"])
    print("cat_6 (SB) : " + standings["cat_6"])
    print("cat_13 (R) : " + standings["cat_13"])
    print("cat_16 (AVG) : " + standings["cat_16"])
    print("cat_21 (OPS) : " + standings["cat_21"])
    print("cat_30 (SV) : " + standings["cat_30"])
    print("cat_32 (IP) : " + standings["cat_32"])
    print("cat_33 (K) : " + standings["cat_33"])
    print("cat_45 (WHIP) : " + standings["cat_45"])
    print("cat_46 (ERA) : " + standings["cat_46"])
    print("cat_86 (QS) : " + standings["cat_86"])
    print("TOT : " + standings["TOT"])



from pymongo import MongoClient
client = MongoClient()
db = client.wfbc


