import sys
sys.path.append("./sturdycouscous")

from enum import Enum
from bs4 import BeautifulSoup
from pymongo import MongoClient, errors, results
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import requests
import string
import tldextract
import regex as re

DOMAIN = 'couscousmongo'
PORT = 27017
DB_NAME = "couscous_db"
COLLECTION = "Categories"
CATEGORIES = ['IT', 'government', 'education', 'news', 'other', 'commerce', 'social-media']
TAGS = ["body", 'title', 'h1', 'p', 'q', 'a', 'blockquote', 'imgsrc', 'map', 'table', 'tr', 'th', 'td', 'caption', 'base']
TLD_MAPPING = {
    'edu': 'education',
    'gov': 'government'
}

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

def clean_tokens(tags):
    tokens = []
    for tag in tags:
        tokens.extend(word_tokenize(str(tag.string)))
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
    TAG_FILTER = re.compile("meta|title|h1|p|q|a|blockquote|imgsrc|map|table|tr|th|td|caption|base")

    def __init__(self, url):
        self.url = url
        
        # First, get the page content and parse into a beautiful tree
        response = requests.get("https://www."+ url.replace('https://', '').replace('www.', ''))
        try:
            if response.status_code == 200:
                self.content = BeautifulSoup(response.content, 'lxml')
                # Look for the keywords indicated by author
                self.page_content = clean_tokens(self.content.findAll(self.TAG_FILTER))
            else:
                print(response.status_code, ": ", response.reason)
                raise Exception(response.status_code + response.reason)
        except BaseException as e:
            print(type(e))
            raise e
        # Extract and normalized keywords from <head>
        evaluation = {}
        # Count keywords in each category
        client = connect_client()
        db = client[DB_NAME]
        collection = db[COLLECTION]
        for category in CATEGORIES:
            category_keywords = collection.find_one({'_id': category}).get('keywords')
            counter = 0
            for word in self.page_content:
                if word in category_keywords:
                    counter += category_keywords[word] 
            evaluation[category] = counter/len(self.page_content)*100
        # Returns the category with the highest sco
        tld = tldextract.extract(self.url)
        evaluation["other"] = evaluation['other']/3
        categories = [max(evaluation.keys(), key=(lambda k: evaluation[k]))]
        if tld.suffix in TLD_MAPPING and TLD_MAPPING[tld.suffix] not in categories:
            categories.append(TLD_MAPPING[tld.suffix])
        self.classification = {
            'categories': categories,
            'data': evaluation
        }

c = Classifier("berkeley.edu")
print(c.classification)
