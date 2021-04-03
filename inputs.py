from pymongo import MongoClient
from datetime import date
import arrow

# 2020 season start = July 23
# 2020 season end = September 27
# season_start = date(2020, 7, 23)
# season_end = date(2020, 9, 27)

# 2021 season start = April 1
# 2021 season end = October 3
season_start = date(2021, 4, 1)
season_end = date(2021, 10, 3)

# DATES AND TIMES
utcnow = arrow.utcnow()
pstnow = utcnow.to('US/Pacific')
today = pstnow.date()

# League Size
numTeams = 12

# mongo stuff
client = MongoClient()
db = client.wfbc2021
