from enum import Enum
from bs4 import BeautifulSoup
from ClassifierTraining import Category
import mongoengine as me

""" Constents used  by the Classifier module"""
class Category(me.Document):
    id = me.StringField(required=True, unique = True, primary_key = True)
    keywords = me.ListField(field = me.StringField(), required=True)
class Classifier:

    def __init__(self, url):
        self.url = url
        
        # First, get the page content and parse into a beautiful tree
        
        # Extract and normalized keywords from <head>
        keywords = None
        evaluation = {}
        # Count keywords in each category
        me.connect('classifier_training_set', host='sss', port = 2222)
        for category in Category.objects:
            counter = 0;
            for word in keywords:
                if word in category.keywords:
                    counter += 1 
            evaluation.insert(category.id, counter)
        
        # Returns the category with the highest score