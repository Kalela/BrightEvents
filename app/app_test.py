
import unittest

from app import event
from app import user

class ApiTest(unittest.Testcase):
    def setUp(self):
        self.api_yangu = my_apis()

    def test_index(self):
    	self.assertEqual(self.render_template, 'index.html', msg="Webpage not found")
    
    

    
