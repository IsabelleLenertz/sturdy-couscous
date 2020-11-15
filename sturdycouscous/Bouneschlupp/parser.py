from bs4 import BeautifulSoup
import requests

class Parser:
    """ Prases an HTML page and extracts data such a child-links
    
    Attributes:
        url -- the target page to parse
        links -- list of all the <a> tags and attributes each list element has 
                a dictionnary of attributes/values (element.attrs)
                a text content (element.text) 
    """


    def __init__(self, ulr):
        self.url = url
        response = request.get(url)
        if response.status_code == 200:
            self.links = BeautifulSoup(response.content, 'lxml').soup.find_all('a')
        else:
            raise BadResponseError(response.status_code)
    
    def get_links(self):
        children = {}
        for link in self.link:
            children.add(link.attrs['href'])
        return children

    def get_links_from_child_page(self):
        children = self.get_links()
        grand_children = {}
        for child in children:
            child_page = new Parser(child)
            grand_children = grandchildren.intersection(child_page.get_links())
        return children.intersection(grand_children)

    def get_link_from_descendent(self, depth):
        if depth < 0 :
            raise ValueError("depth of descendent should be greater than 1")
        first_generation = self.get_links()
        if depth == 1:
            return first_generation
        #recursive call to get the whole family tree  
        grand_children = {}
        for child in first_generation:
            child_page = new Parser(child)
            grand_children = grandchildren.intersection(child_page.get_links_from_descendent(depth-1))
        
    return first_generation.intersection(grand_children)
        


