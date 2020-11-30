from pymongo import MongoClient, errors

DOMAIN = 'mongotest'
PORT = 27017

database_names=[]

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
        
def create_db(client):
    db = client["garbanzodb"]

c = connect_client()
create_db(c)

if c:
    create_db(c)
    c.list_database_names()
print ("\ndatabases:", database_names)

