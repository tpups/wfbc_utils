import datetime
import SendRequest

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

standings = SendRequest.sendRequest(wfbcStandingsByDate)
standings = standings[2]

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