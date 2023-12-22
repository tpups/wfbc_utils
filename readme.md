## Secrets
create .env file and add:
`mongopw = "password"`

## User cookie:
create Cookie.py and include variable cookie = "cookie"

## Rotowire:
Box score stats must be customized to include all stats needed by UpdateDB. This way they will also be available in the API.

## Packages:
`pip install pymongo`  
`pip install MLB-StatsAPI`  
`pip install -U arrow`
`pip install python-dotenv`

## Windows setup:
`py -m venv env`  
`env\Scripts\activate`  

**if denied:**  
`Get-ExecutionPolicy`  
`set-executionpolicy remotesigned`  

## Starting Mongo (OSX):
**from project dir:**  
`mongod --dbpath data/db`  

*^deprecated?*  

**installed brew tap**  
now:  
`brew services start mongodb-community`  
`mongo`  
