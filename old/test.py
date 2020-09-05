import urllib

dls = "http://www.rotowire.com/mlbcommish17/standings.xls?leagueid=153&compSort=0"
urllib.urlretrieve(dls, "test.xls")
