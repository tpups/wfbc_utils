import json
import requests
import datetime
import pymongo
import SendRequest

datetime_obj = datetime.datetime.now()
time_delta_1day = datetime.timedelta(1)
#datetime_obj = datetime_obj - time_delta_1day
year = str(datetime_obj.year)
month = str(datetime_obj.month)
day = str(datetime_obj.day)
if len(month) is 1:
    month = "0" + month
if len(day) is 1:
    day = "0" + day
end_date = year + "-" + month + "-" + day

pitching = "https://www.rotowire.com/mlbcommish20/tables/box.php?leagueID=163&teamID=0&date=2020-09-04&borp=P"
hitting = "https://www.rotowire.com/mlbcommish20/tables/box.php?leagueID=163&teamID=0&date=2020-09-04&borp=B"

pitchingStats = SendRequest.sendRequest(pitching)
hittingStats = SendRequest.sendRequest(hitting)

print(type(hittingStats))

if hittingStats is not None:
    for team in hittingStats:
        for stat in team:
            print(stat + " : " + str(team[stat]))

if pitchingStats is not None:
    for team in pitchingStats:
        print(team)
