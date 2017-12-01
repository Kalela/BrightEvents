import unittest

from routes import my_apis
from entities import entities


class TestAPIs(unittest.TestCase):
    def setUp(self):
        self.api_yangu = my_apis()
    #Perfoem Tests after using api once for correct output
    def test_register_page_json(self):
        expected =4
        result =len(users)
        self.assertEqual(expected, result, msg="Registration api not working")
        
    def test_login_json(self):
        expected = 'Logged In'
        result = login_json()
        self.assertEqual(expected, result, msg="Login api not working")
        
    def test_logout_json(self):
        expected ={}
        result =session.pop('username')
#        self.assertEqual(expected, result, msg="Logout api not working")
        
        
#    def test_reset_password_json(self):
#        expected = 
#        result =
#        self.assertEqual(expected, result, msg="Reset password api not working")
       
        
    def test_new_event_json(self):
        expected = 4
        result = len(events)
        print(len(events))
        self.assertEqual(expected, result, msg="Create new event api not working")
        
        
#    def test_event_update_json(self):
#        expected = 
#        result =
#        self.assertEqual(expected, result, msg="Update existing event api not working")
        
    def test_event_delete_json(self):
        expected = 2
        result = len(events)
        self.assertEqual(expected, result, msg="Delete event api not working")
    
#    def test_event_page_json(self):
#        expected = 
#        result = 
#        self.assertEqual(expected, result, msg="Open event page api not working")
    
#    def test_rsvp_json(self):
#        expected = eventid + ' RSVP Sent'
#        result = evn[0]['eventid'] += ' RSVP Sent'
#        self.assertEqual(expected, result, msg="Rsvp api not working")
        
        
        
        
        
               
    
if __name__=='__main__':
    unittest.main(exit=False)