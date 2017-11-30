
import unittest

from entities import Events
from entities import Users
from app import my_apis

class TestApi(unittest.TestCase):
    def setUp(self):
        self.api_yangu = my_apis()

    def test_index(self):
    	self.assertEqual(self.render_template, 'index.html', msg="Webpage not found")
        
if __name__=='__main__':
    unittest.main(exit=False)
    
    

    
