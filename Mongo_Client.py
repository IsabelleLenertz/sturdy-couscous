from pymongo import MongoClient, errors

DOMAIN = 'couscousmongo'
PORT = 27017
DB_NAME = "couscous_db"
COLUMN_NAME = "tls_checks"

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

def insert(inputdict):
    return column.insert_one(inputdict)

client = connect_client()
db = client[DB_NAME]
column = db[COLUMN_NAME]

mock_tls_check = {
    "URL":"https://github.com/IsabelleLenertz/sturdy-couscous",
    "Title":"sturdy-couscous",
    "Domain":"`Github",
    "Classification": {
        "Categories":["social media", "IT/dev"],
        },
    "Data": {
        "Keywords": ['testkeyword1', 'testkeyword2'], 
        },
    "Extension": [".com"],
    "Tags": {
        "tag":"testtag1",
        }
    }
print("******************TEST MONGO OUTPUT START******************")
print(insert(mock_tls_check))
print("******************TEST MONGO OUTPUT END********************")

# Check DB read
for each in column.find():
    print(each)

