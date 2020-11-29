from enum import Enum
from bs4 import BeautifulSoup

""" Constents used  by the Classifier module"""
class Catregories(Enum):
    EDUCATION = 0
    GOVERNMENT = 1
    IT = 2
    OTHER = 3
    SHOPPING = 4
    SOCIAL_MEDIA = 5

class Classifier:
    """ Classifies websites in 6 categories:  social media, education, government, IT/dev, shopping, other

    Attributes: 
        url -- URL of the page to classify
        html content -- HTML tags of the page to classify
        analyse_report -- Json returned to the caller

            { 
                URL:https://github.com/IsabelleLenertz/sturdy-couscous
                Title: sturdy-couscous,
                Domain: Github,
                Classification: {
                Categories: [social media, IT/dev],
                Data: {
                    Keywords: [...., ...]
                    Extention: [".com"]
                    Tags: [ {tag:...., attributes [..] } , {.....} ]
                }
    """
    def __init__(self, url, html):
        self.url = url
        self.html = html
        
        # look for key words in the html
        