# read cvs file with schema url, classification
""" store keywords for each classification into table (or database) with keyaord and ocurrence
    <meta name="keyewords" content="<comma separated list of the keywords">
    <Title>: look for nouns
    <Body> <title>: 
    <Base>
    <h1>-<h6>
    <legend>
    <img alt="   ">"""

import csv
import requests
import errors
from bs4 import BeautifulSoup
import pprint
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import string
import json


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


def update_table(key_words, data, row):
    current_set =  data_table.get(row[1], set())
    data.update({row[1] : current_set.union(map(str.strip, key_words))})

    
    
with open("sturdycouscous/resources/keyword_training.csv") as csvfile:
    training_sample = csv.reader(csvfile, delimiter=',')
    data_table={}
    printer = pprint.PrettyPrinter()
    for row in training_sample:
        try:
            # Get and parse HTML content
            print("https://www."+ row[0].replace('https://', '').replace('www.', ''))
            response = requests.get("https://www."+ row[0].replace('https://', '').replace('www.', ''))
            if response.status_code == 200:
                content = BeautifulSoup(response.content, 'lxml')
                
                # Look for the keywords indicated by author
                metadata = content.head.find("meta", attrs = {'name':'keywords'})
                if not metadata: 
                    metadata = content.head.find("meta", attrs = {'name':'Keywords'})
                if metadata:
                    key_words = clean_tokens(metadata.get('content'))
                    update_table(key_words, data_table, row)
                
                # Look for description and extracts keywords
                description_tag = content.head.find("meta", attrs = {'name':'description'})
                if not description_tag:
                    description_tag = content.head.find("meta", attrs = {'name':'Description'})
                if description_tag:
                    key_words = clean_tokens(description_tag.get('content'))
                    update_table(key_words, data_table, row)
 
            else:
                print(response.status_code, ": ", response.reason)
                raise errors.BadResponseError(response.status_code)
        except BaseException as e:
            print(type(e))
    with open('classifier.txt', 'w') as out:
        out.write(json.dumps(data_table, indent=4, fsort_key = True))
