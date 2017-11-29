
import unittest

from entities import Events
from entities import Users

class ApiTest(unittest.TestCase):
    def setUp(self):
        self.api_yangu = my_apis()

    def test_index(self):
    	self.assertEqual(self.render_template, 'index.html', msg="Webpage not found")
    
    

    
