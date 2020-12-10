import sys
sys.path.append("/usr/src/app/sturdy-couscous/sturdycouscous")

import Utils
from logging import ERROR
from bs4 import BeautifulSoup
import requests
#from sturdycouscous.bouneschlupp import errors
from . import errors
import logging as log

class Parser:
    """ Prases an HTML page and extracts data such a child-links
    
    Attributes:
        url -- the target page to parse
        links -- list of all the <a> tags and attributes each list element has 
                a dictionnary of attributes/values (element.attrs)
                a text content (element.text) 
        no_data -- list of the urls (self or descendent) that could not be evaluated
        tags -- list of all the <a> tags of the page
    """
    def __init__(self, url):
        self.url = url
        self.links = set()
        self.no_data = set()
        self.tags = set()
        children = set()
        try:
            response = requests.get("http://www." + url)
            if response.status_code == 200:
                self.tags = BeautifulSoup(response.content, 'lxml').find_all('a', { "href" : True })
                for link in self.tags:
                    children.add(Utils.grab_domain_name(link.attrs['href']))
            else:
                print(url, " responded with ", response.status_code, "- could not evaluate children")
        except Exception as e :
                print(url, " threw an exception ", e , "- could not evaluate children")
         
    def get_links(self):
        return self.links

    def get_links_from_child_pages(self):
        children = self.get_links()
        grand_children = set()
        for child in children:
            log.debug("creating child parser for ", child)
            child_page = Parser(child)
            grand_children = grand_children.union(child_page.get_links())
            log.debug("grand children now contain: ", grand_children)
        return children.union(grand_children)

    def get_link_from_descendent(self, depth):
        my_links = self.get_links()
        if depth < 0 :
            raise ValueError("depth of descendent should be greater than 1")
        elif depth == 0:
            return my_links
        elif depth == 1:
            return self.get_links_from_child_pages()
        else:
            descendents = set()
            for link in my_links:
                descendents = descendents.union(self.get_link_from_descendent(depth - 1))
            return descendents


