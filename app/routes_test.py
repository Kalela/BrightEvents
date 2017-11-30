import unittest

from routes import my_apis

class TestAPIs(unittest.TestCase):
    def setUp(self):
        self.api_yangu = my_apis()

    def test_register_page_json(self):
        expected = 
        result =
    	self.assertEqual(expected, result, msg="api not working")
        
    def test_login_json(self):
        expected = 
        result =
        self.assertEqual(self.login_json(), {}, msg="api not working")
        
    def test_logout_json(self):
        expected = 
        result =
        self.assertEqual(self.logout_json(), {}, msg="api not working")
        
        
    def test_reset_password_json(self):
        expected = 
        result =
        self.assertEqual(self.reset_password_json(), {}, msg="api not working")
       
        
    def test_new_event_json(self):
        expected = 
        result =
        self.assertEqual(self.new_event_json(), {}, msg="api not working")
        
        
    def test_event_update_json(self):
        expected = 
        result =
        self.assertEqual(self.event_update_json(), {}, msg="api not working")
        
    def test_event_delete_json(self):
        expected = 
        result =
        self.assertEqual(self.event_delete_json(), {}, msg="api not working")
    
    def test_event_page_json(self):
        expected = 
        result =
        self.assertEqual(self.event_page_json(), {}, msg="api not working")
    
    def test_rsvp_json(self):
        expected = 
        result =
        self.assertEqual(self.rsvp_json(), {}, msg="api not working")
        
        
        
        
        
               
    
if __name__=='__main__':
    unittest.main(exit=False)