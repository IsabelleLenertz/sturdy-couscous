from enum import Enum
from bs4 import BeautifulSoup
from pymongo import MongoClient, errors, results
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import requests
import string


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
        response = requests.get("https://www."+ url.replace('https://', '').replace('www.', ''))
        text_content = []
        try:
            if response.status_code == 200:
                content = BeautifulSoup(response.content, 'lxml')
                
                # Look for the keywords indicated by author
                metadata = content.head.find("meta", attrs = {'name':'keywords'})
                if not metadata: 
                    metadata = content.head.find("meta", attrs = {'name':'Keywords'})
                if metadata:
                    text_content = clean_tokens(metadata.get('content'))
    
                # Look for description and extracts keywords
                description_tag = content.head.find("meta", attrs = {'name':'description'})
                if not description_tag:
                    description_tag = content.head.find("meta", attrs = {'name':'Description'})
                if description_tag:
                    text_content = clean_tokens(description_tag.get('content'))
            else:
                print(response.status_code, ": ", response.reason)
                raise Exception()
        except BaseException as e:
            print(type(e))
        # Extract and normalized keywords from <head>
        evaluation = {}
        # Count keywords in each category
        client = connect_client()
        db = client[DB_NAME]
        collection = db[COLLECTION]
        categories = collection.find()
        for category in CATEGORIES:
            category_keywords = collection.find_one({'_id': category}).get('keywords')
            counter = 0
            for word in text_content:
                if word in category_keywords:
                    counter += 1 
            evaluation[category] = counter
        
        # Returns the category with the highest score
        self.classification = evaluation
