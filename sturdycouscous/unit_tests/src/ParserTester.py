import parser
import unittest

'''It is recommended that you use TestCase implementations to group 
tests together according to the features they test. unittest 
provides a mechanism for this: the test suite, represented by 
unittest’s TestSuite class. In most cases, calling unittest.main() 
will do the right thing and collect all the module’s test cases for
 you and execute them.'''

class  ParserTestCase(unittest.TestCase):
    def setUp(sef):
        # Method called before every test
        pass
    def tearDown(self):
        pass
    def test_get_links(self):
        #define tests here
        pass
    def test_get_links_from_child_page(self):
        #define tests here
        pass
    def test_get_link_from_descendent(self):
        #define tests here
        pass

