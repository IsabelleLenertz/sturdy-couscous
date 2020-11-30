from pymongo import MongoClient, errors

DOMAIN = 'garbanzomongo'
PORT = 27017
DB_NAME = "garbanzodb"

def connect_client():
    try:
        client = MongoClient(
                host = [ str(DOMAIN) + ":" + str(PORT) ],
                serverSelectionTimeoutMS = 3000, # 3 second timeout
                username = "root",
                password = "root"
        )
        print("Server version: ", client.server_info()["version"])
        return client
    except errors.ServerSelectionTimeoutError as err:
        print("pymongo ERROR: ", err)
        return None
        
client = connect_client()
db = client["garbanzodb"]

if client:
    database_names=client.list_database_names()
print ("\ndatabases:", database_names)

