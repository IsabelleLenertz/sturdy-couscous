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


with open("sturdycouscous/resources/keyword_training.csv") as csvfile:
    training_sample = csv.reader(csvfile, delimiter=',')
    data_table={}
    response = requests.get('https://stackoverflow.com/')
    if response.status_code == 200:
        content = BeautifulSoup(response.content, 'html.parser')
        metadata = content.head.find_all("meta")
        for tag in metadata:
            print(tag)
    else:
        print(response.status_code)
    '''
    for row in training_sample:
        try:
            response = requests.get('https://stackoverflow.com/')
            if response.status_code == 200:
                content = BeautifulSoup(response.content, 'html.parser')
                metadata = content.head.find_all("metadata")
                for tag in metadata:
                    if tag.attrs['name'] == "keywords":
                        kw_list = tag.attrs["content"]
                        print(kw_list)
            else:
                raise errors.BadResponseError(response.status_code)
        except BaseException as e:
            print(type(e))
    '''
    