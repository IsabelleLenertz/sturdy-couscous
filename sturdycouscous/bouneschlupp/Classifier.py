from enum import Enum
from bs4 import BeautifulSoup
from pymongo import MongoClient, errors
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

DOMAIN = 'couscousmongo'
PORT = 27017
DB_NAME = "couscous_db"
COLLECTION = "Categories"
CATEGORIES = ['IT', 'government', 'education', 'news', 'other', 'commerce', 'social-media']

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

def clean_tokens(text):
    tokens = word_tokenize(text)
    tokens = [w.lower() for w in tokens]
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    words = [word for word in stripped if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    # Stemming
    porter = PorterStemmer()
    return [porter.stem(word) for word in words]

class Classifier:
    DOMAIN = 'couscousmongo'
    PORT = 27017
    DB_NAME = "couscous_db"
    COLUMN_NAME = "tls_checks"
    USERNAME = "root"
    PASSWORD = "root"
    def __init__(self, url):
        self.url = url
        
        # First, get the page content and parse into a beautiful tree
        
        # Extract and normalized keywords from <head>
        keywords = None
        evaluation = {}
        # Count keywords in each category
        client = connect_client()
        db = client[DB_NAME]
        collection = db[COLLECTION]
        categories = collection.find()
        for category in CATEGORIES:
            category_keywords = collection.find({'_id': category}).get('keywords')
            counter = 0
            for word in keywords:
                if word in category_keywords:
                    counter += 1 
            evaluation.insert(category.id, counter)
        
        # Returns the category with the highest score