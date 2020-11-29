from pymongo import MongoClient, errors

DOMAIN = 'mongotest'
PORT = 27017

database_names=[]

try:
    client = MongoClient(
            host = [ str(DOMAIN) + ":" + str(PORT) ],
            serverSelectionTimeoutMS = 3000, # 3 second timeout
            username = "root",
            password = "root"
    )

    print("Server version: ", client.server_info()["version"])

    database_names = client.list_database_names()

except errors.ServerSelectionTimeoutError as err:
    print("pymongo ERROR: ", err)
    
print ("\ndatabases:", database_names)

