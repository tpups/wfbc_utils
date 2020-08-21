import json
import requests
import datetime

datetime_obj = datetime.datetime.now()
year = str(datetime_obj.year)
month = str(datetime_obj.month)
if len(month) is 1:
    month = "0" + month
day = str(datetime_obj.day - 1)
if len(day) is 1:
    day = "0" + day
end_date = year + "-" + month + "-" + day

wfbc_url_base = 'https://www.rotowire.com/mlbcommish20/tables/standings-by-date.php?leagueID=163&divisionID=0&start=2020-07-23&end=' + end_date
print(wfbc_url_base)
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
    response = requests.get(wfbc_url_base, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

standings = getStandings()

if standings is not None:
    print("Standings:")
    for team in standings:
        print(team)

