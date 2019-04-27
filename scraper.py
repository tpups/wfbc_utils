import requests
from lxml import html

cookies = {
    'ASPSESSIONIDQWSSSTQB': 'LIDLJNHAKIKBNJOKFFGDLNHF',
    'ASPSESSIONIDAUCDADBQ': 'IFGJHNHAEFLBKFIDNDEJDAKD',
    'ASPSESSIONIDCWBABBCQ': 'KKFCEJEBMBHJBJCODICMKJFI',
    'ASPSESSIONIDSWRQSQQA': 'OPDCEJEBHNHPIDECCPCCKBEG',
    'ASPSESSIONIDQWTTTTRB': 'ICGLFJEBPAJJJHCCOJKHCFBM',
    'dmxRegion': 'false',
    'PHPSESSID': 'e92878914690072b8c881a16add3b08f',
    'amplitude_id_54aab4fcc9f6be803de938d75c287ee9rotowire.com': 'eyJkZXZpY2VJZCI6IjEwYTM4NWIyLTEyMzgtNDNkNC04YmQ2LWU4NTEyNTE3OTYwMlIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU1NjI2MTg1MzkzOSwibGFzdEV2ZW50VGltZSI6MTU1NjI2MTg1Mzk0NCwiZXZlbnRJZCI6MSwiaWRlbnRpZnlJZCI6MSwic2VxdWVuY2VOdW1iZXIiOjJ9'
}

login = {
    "username": "USERNAME",
    "password": "PASSWORD",
    "landingPage": "/mlbcommish19/index2.htm"
}

session_requests = requests.session()

jar = requests.cookies.RequestsCookieJar()

login_url = "https://www.rotowire.com/users/login.php"

result = session_requests.post(
    login_url,
    data = login,
)
print(result.ok)
print(result.status_code)
url = "https://www.rotowire.com/mlbcommish19/standings.htm?leagueid=56"
result = session_requests.get(
    url,
    cookies=cookies
)
result2 = session_requests.get(
    url,
    cookies=cookies
)
print(result.ok)
print(result.status_code)
tree = html.fromstring(result.content)
find_date = "Download"
date = tree.xpath('.//a[starts-with(text(),"Download")]')

print(date)
print("working")
print(result2.content)
