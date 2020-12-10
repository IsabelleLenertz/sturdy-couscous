from logging import root
import tldextract
from pymongo import MongoClient, errors

CHILDREN_FILE = "sturdycouscous/resources/children.txt"
NO_DATA_FILE = "sturdycouscous/resources/no_data_urls.txt"
TRAINING_FILE = "sturdycouscous/resources/keyword_training.csv"
HISTORY_CSV = "sturdycouscous/resources/keyword_training.csv"
#Constants for mongodb
DOMAIN = 'couscousmongo'
PORT = 27017
DB_NAME = "couscous_db"
CLASSIFIER_COLLECTION = "categories"
DOMAIN_COLLECTION = "domain_info"
TIMEOUT = 1000
USERNAME = "root"
PASSWORD = "root" #this is a proof of concept with a local temporary containerized bd, so we will allow ourselves bad secret management practicies

def grab_domain_name(url):
    url_split = tldextract.extract(url)
    return url_split.registered_domain

def grab_subdomain_name(url):
    url_split = tldextract.extract(url)
    if url_split.subdomain != "www":
        return '.'.join(part for part in url_split if part)
    return '.'.join([url_split.domain, url_split.suffix])

def grab_subdomain_url(url):
    url_split = tldextract.extract(url)
    return '.'.join(part for part in url_split if part)

def get_client():
    try:
        client = MongoClient(
                host = [ str(DOMAIN) + ":" + str(PORT) ],
                serverSelectionTimeoutMS = TIMEOUT,
                username = USERNAME,
                password = PASSWORD
        )
        return client
    except errors.ServerSelectionTimeoutError as err:
        print("connection timeout")
        return None
