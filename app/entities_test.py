
import unittest

from entities import Events
from entities import Users
from app import my_apis

class TestUsers(unittest.TestCase):
    def setUp(self):
        self.user_yangu = Users()

    def test_index(self):
    	self.assertEqual(self.render_template, 'index.html', msg="Webpage not found")
        
class TestEvents(unittest.TestCase):
    def setUp(self):
        self.event_yangu = Events()

    def test_index(self):
    	self.assertEqual(self.render_template, 'index.html', msg="Webpage not found")     
        
        
        
        
        
        
if __name__=='__main__':
    unittest.main(exit=False)