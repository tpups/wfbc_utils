## Windows setup:
'py -m venv env'
'env\Scripts\activate'

**if denied:**
'Get-ExecutionPolicy'
'set-executionpolicy remotesigned'

##Starting Mongo (OSX):
**from project dir:**
'mongod --dbpath data/db'
*^ deprecated?*

**installed brew tap**
now:
'brew services start mongodb-community'
'mongo'

##Categories:
- cat_4 = HR
- cat_5 = RBI
- cat_6 = SB
- cat_13 = R
- cat_16 = AVG
- cat_21 = OPS
- cat_30 = SV
- cat_32 = IP
- cat_33 = K
- cat_45 = WHIP
- cat_46 = ERA
- cat_86 = QS