from pymongo import MongoClient, errors

class DBClient():
    def __init__(self):
        self.domain = 'couscousmongo'
        self.port = 27017
        self.db_name = "couscous_db"
        self.column_name = "domain_info"

        self.client = self.connect_client()
        self.collection = self.client[self.column_name]
        self.db = self.client[self.db_name]
        self.column = self.db[self.column_name]

    def connect_client(self):
        try:
            client = MongoClient(
                    host = [ str(self.domain) + ":" + str(self.port) ],
                    serverSelectionTimeoutMS = 3000, # 3 second timeout
                    username = "root",
                    password = "root"
            )
            return client
        except errors.ServerSelectionTimeoutError as err:
            print("pymongo ERROR: ", err)
            return None

    def insert(self, inputdict):
        return self.column.insert_one(inputdict, check_keys=False)

    def insert_rows(self, inputlist):
        return self.column.insert(inputlist, check_keys=False)
