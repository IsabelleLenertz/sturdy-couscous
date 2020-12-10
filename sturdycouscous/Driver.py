import sys
sys.path.append("/usr/src/app/sturdy-couscous/sturdycouscous")
import Utils, SecurityCrawler
from bouneschlupp import parser, ClassifierTraining
import csv
import nltk; 
nltk.download('stopwords')
nltk.download('punkt')
import Printer
import ast

''' call to generate the txt file with the domains to evaluate
    if csv is set to True, an index needs to be specified
    if csv is set to False, the index will be ignored
    arguments:
        filename - string - file containing the borwsing history
        generations - positive integer - number of generations for the children url Default 1)
        csv - boolean - True is the file is a csv (Default True)
        index - positive integer - index of the url in the csv file (Default 5)
        separator - string/char - separator used in the csv (Default ',')
    return: (children, no_data)
        children - set of strings - url from the decsendents
        do_data - urls that could no be parsed
    side effect: creates 2 files (names defines in Utils.py)
        sturdycouscous/resources/children.txt
        sturdycouscous/resources/no_data_urls.txt
'''

def get_dataset(filename = Utils.HISTORY_CSV, generations = 1, is_csv = True, index = 5, separator=','):
    urls = set()
    children = set()
    if not is_csv:
        with open(filename) as file:
            lines = file.readlines()
            for line in lines:
                urls.add(line.strip())
                children.add(line[index].strip())
    else:
        with open(filename) as file:
            csv_content = csv.reader(file, delimiter=separator)            
            for line in csv_content:
                urls.add(line[index].strip())
                children.add(line[index].strip())
    no_data = set()
    for url in urls:
        url_parser = parser.Parser(url)
        children.update(url_parser.get_link_from_descendent(generations))
        no_data.update(url_parser.no_data)

    with open(Utils.CHILDREN_FILE, 'w') as out:
        for url in children:
            out.write(url + "\n")
    
    with open (Utils.NO_DATA_FILE, 'w') as out:
        for url in no_data:
            out.write(url + "\n")

    return (children, no_data)

'''
    training_set - string - name of the file with the training set. (Default  TRAINING_FILE)
        line sechma: <url>, <classification>
'''
def train_classifier(training_set = Utils.TRAINING_FILE):
    ClassifierTraining.train(training_set)

def run_analysis(filename = Utils.CHILDREN_FILE):
    urls = set()
    with open(filename) as content:
        lines = content.readlines()
        for line in lines:
            urls.add(line.strip())
    engine = SecurityCrawler.security_crawler(urls)
    engine.run()

def export_database():
    client = Utils.get_client()
    db = client[Utils.DB_NAME]
    domain_collection = db[Utils.DOMAIN_COLLECTION]
    class_collection = db[Utils.CLASSIFIER_COLLECTION]

    domains = list(domain_collection.find({}, {  "_id": 0 }))
    categories = list(class_collection.find())
    with open("db/domain_info.json", "w") as out:
        out.write(json.dumps(domains))
    with open("db/categories.json", "w") as out:
        out.write(json.dumps(categories))
    client.close()

def import_data(mongo_collection = Utils.DOMAIN_COLLECTION):
    client = Mongo_Client.Client(mongo_collection)
    try:
        if client.connect(): 
            with open('db_dump', 'r') as  data_file:
                data = ast.literal_eval(data_file.readline().replace('true','True').replace('false','False').replace('null','None'))
                for row in data:    
                    client.collection.insert(row)    
        else:
            print("Could not connect to database's ", mongo_collection)
    finally:
        client.close()
    

def import_classification_data(mongo_collection = Utils.CLASSIFIER_COLLECTION):
    import_data(mongo_collection)

def print_report():
    Printer().output_report()

def run_all():
    train_classifier()
    get_dataset(HISTORY_CSV, 0, True, 5)
    run_analysis(CHILDREN_FILE)
    Printer().output_report()
