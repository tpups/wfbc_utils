## Rotowire:
Box score stats must be customized to include all stats needed by UpdateDB. This way they will also be available in the API.

## Add new team IDs:
Add a new db to Mongo cluster with teams collection by populating new team info in main.py then running the updateTeams() function in main.py

## Secrets
create .env file and add:
`mongopw = "password"`

## User cookie:
create Cookie.py and include variable cookie = "cookie"