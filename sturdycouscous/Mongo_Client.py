from logging import error
from pymongo import MongoClient, collection, errors
import Utils

class Client:
    
    def __init__(self, collection_name):
        self.collection_name = collection_name

    def connect(self):
        try:
            self.client = Utils.connect_client()
            db = self.client[Utils.DB_NAME]
            self.collection = db[Utils.DOMAIN_COLLECTION]
            return True
        except errors.ServerSelectionTimeoutError as err:
            raise err
        except Exception:
            return False

    def insert(self, data):
        return self.collection.insert_one(data)

    def close(self):
        self.client.close()

    def drop(self):
        self.collection.drop()

    def print_all(self):
        print("******************TEST MONGO OUTPUT START******************")
        # Check DB read
        for each in self.collection.find():
            print(each)
        print("******************TEST MONGO OUTPUT END********************")
