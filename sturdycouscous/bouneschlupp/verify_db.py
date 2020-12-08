from pymongo import MongoClient, errors

DOMAIN = 'couscousmongo'
PORT = 27017
DB_NAME = "couscous_db"
COLLECTION = "Categories"

def connect_client():
    try:
        client = MongoClient(
                host = [ str(DOMAIN) + ":" + str(PORT) ],
                serverSelectionTimeoutMS = 3000, # 3 second timeout
                username = "root",
                password = "root"
        )
        return client
    except errors.ServerSelectionTimeoutError as err:
        print("pymongo ERROR: ", err)
        return None

client = connect_client()
db = client[DB_NAME]
collection = db[COLLECTION]

print("******************TEST MONGO OUTPUT START******************")
# Check DB read
for each in collection.find():
    print(each)
print("******************TEST MONGO OUTPUT END********************")
