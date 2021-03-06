# read cvs file with schema url, classification
""" store keywords for each classification into table (or database) with keyaord and ocurrence
    <meta name="keyewords" content="<comma separated list of the keywords">
    <Title>: look for nouns
    <Body> <title>: 
    <Base>
    <h1>-<h6>
    <legend>
    <img alt="   ">"""
import sys
sys.path.append("/usr/src/app/sturdy-couscous/sturdycouscous")

import csv
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import string
import json
from pymongo import MongoClient, errors
import Utils
import time


'''
{
    _id: "IT"
    keywords: {word2: 3}, {word2:1}
}
'''
def update_db(category, collection, key_words):
    current_category = collection.find_one({'_id' : category})
    if current_category == None:
        weighted_keywords = {}
        for word in key_words:
            weighted_keywords[word] = weighted_keywords.get(word, 0) + 1
        collection.insert_one({ '_id' : category, 'keywords' : weighted_keywords})
    else:
        current_dic = current_category.get('keywords')
        weighted_keywords = {}
        for word in key_words:
            weighted_keywords[word] = current_dic.get(word, 0) + 1
        collection.update_one({'_id' : category}, {'$set': { 'keywords': weighted_keywords }})
   
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

def train(filename):
    with open(filename) as csvfile:
        training_sample = csv.reader(csvfile, delimiter=',')
        with Utils.get_client() as client:
            db = client[Utils.DB_NAME]
            collection = db[Utils.CLASSIFIER_COLLECTION]
            collection.drop()
            for row in training_sample:
                try:
                    # Get and parse HTML content
                    response = requests.get("https://www." + Utils.grab_domain_name(row[0]), timeout=2)
                    if response.status_code == 200:
                        content = BeautifulSoup(response.content, 'lxml')
                        
                        # Look for the keywords indicated by author
                        metadata = content.head.find("meta", attrs = {'name':'keywords'})
                        if not metadata: 
                            metadata = content.head.find("meta", attrs = {'name':'Keywords'})
                        if metadata:
                            key_words = clean_tokens(metadata.get('content'))
                            update_db(row[1], collection, key_words)
                        
                        # Look for description and extracts keywords
                        description_tag = content.head.find("meta", attrs = {'name':'description'})
                        if not description_tag:
                            description_tag = content.head.find("meta", attrs = {'name':'Description'})
                        if description_tag:
                            key_words = clean_tokens(description_tag.get('content'))
                            update_db(row[1], collection, key_words) 
                    else:
                        print(response.status_code, ": ", response.reason)
                except Exception as e:
                    print(type(e))
