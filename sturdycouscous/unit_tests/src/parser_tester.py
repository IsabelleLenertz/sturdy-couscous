from sturdycouscous.bouneschlupp import parser as parser
from unittest.mock import patch, Mock
from unittest import TestCase
import requests


'''It is recommended that you use TestCase implementations to group 
tests together according to the features they test. unittest 
provides a mechanism for this: the test suite, represented by 
unittest’s TestSuite class. In most cases, calling unittest.main() 
will do the right thing and collect all the module’s test cases for
 you and execute them.'''

class Mock_Response:
    status_code = 200
    content = ""

    def __init__(self, url):
        with open('sturdycouscous/unit_tests/resources/links.html') as file:
            self.content = file.read()

class  ParserTestCase(TestCase):
    def setUp(sef):
        # Method called before every test
        pass
    def tearDown(self):
        pass
    @patch('sturdycouscous.bouneschlupp.parser.requests.get', new=Mock_Response)
    def test_get_links(self):
        my_parser = parser.Parser("http://not_a_url")
        links =  my_parser.get_links()
        self.assertIn("https://www.google.com/", links, msg="link missing")
        self.assertIn("https://www.w3.org/", links, msg="link missing")
        self.assertIn("html_images.asp", links, msg="link missing")
        self.assertIn("/css/default.asp", links, msg="link missing")
        self.assertTrue(len(links) == 4)

    def test_get_links_from_child_page(self):
        #define tests here
        pass
    def test_get_link_from_descendent(self):
        #define tests here
        pass

