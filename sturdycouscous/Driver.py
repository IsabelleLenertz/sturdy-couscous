import sys
sys.path.append("/usr/src/app/sturdy-couscous/sturdycouscous")
import Utils, SecurityCrawler
from bouneschlupp import parser, ClassifierTraining
import csv


''' call to generate the txt file with the domains to evaluate
    if csv is set to True, an index needs to be specified
    if csv is set to False, the index will be ignored
    arguments:
        filename - string - file containing the borwsing history
        generations - positive integer - number of generations for the children url Default 1)
        csv - boolean - True is the file is a csv (Default false)
        index - positive integer - index of the url in the csv file (Default -1)
        separator - string/char - separator used in the csv (Default ',')
    return: (children, no_data)
        children - set of strings - url from the decsendents
        do_data - urls that could no be parsed
    side effect: creates 2 files (names defines in Utils.py)
        sturdycouscous/resources/children.txt
        sturdycouscous/resources/no_data_urls.txt
'''

def get_dataset(filename, generations = 1, is_csv = False, index = -1, separator=','):
    urls = set()
    if not is_csv:
        with open(filename) as file:
            lines = file.readlines()
            for line in lines:
                urls.add(Utils.grab_domain_name(line.strip()))
    else:
        with open(filename) as file:
            csv_content = csv.reader(file, delimiter=separator)            
            for line in csv_content:
                urls.add(line[index].strip())
    children = set()
    no_data = set()
    for url in urls:
        url_parser = parser.Parser(url)
        children.update(url_parser.get_link_from_descendent(generations))
        no_data.update(url_parser.no_data)

    with open(Utils.CHILDREN_FILE, 'w') as out:
        for url in children:
            out.write(url)
    
    with open (Utils.NO_DATA_FILE, 'w') as out:
        for url in no_data:
            out.write(url)

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

#train_classifier()
get_dataset(Utils.TRAINING_FILE, 1, True, 0)