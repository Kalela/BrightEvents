import os, sys, inspect
import unittest
import requests

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from routes import MyApis
from routes import app
from entities import Users
from entities import Events


class TestAPIs(unittest.TestCase):
    def setUp(self):
        self.api_yangu = MyApis()

    def test_register_page_json(self):
        tester = app.test_client(self)
        response = tester.post('/api/v2/auth/register',data=dict(username='Abe',password='1234'), content_type='json')
        self.assertEqual(response.status_code, 201, msg="Register api not working")
        
#    def test_login_json(self):
#        expected = 'Logged In'
#        result = login_json()
#        self.assertEqual(expected, result, msg="Login api not working")
#        
#    def test_logout_json(self):
#        expected ={}
#        result =session.pop('username')
##        self.assertEqual(expected, result, msg="Logout api not working")
#        
#        
##    def test_reset_password_json(self):
##        expected = 
##        result =
##        self.assertEqual(expected, result, msg="Reset password api not working")
#       
#        
#    def test_new_event_json(self):
#        expected = 4
#        result = len(events)
#        print(len(events))
#        self.assertEqual(expected, result, msg="Create new event api not working")
#        
#        
##    def test_event_update_json(self):
##        expected = 
##        result =
##        self.assertEqual(expected, result, msg="Update existing event api not working")
#        
#    def test_event_delete_json(self):
#        expected = 2
#        result = len(events)
#        self.assertEqual(expected, result, msg="Delete event api not working")
#    
##    def test_event_page_json(self):
##        expected = 
##        result = 
##        self.assertEqual(expected, result, msg="Open event page api not working")
#    
##    def test_rsvp_json(self):
##        expected = eventid + ' RSVP Sent'
##        result = evn[0]['eventid'] += ' RSVP Sent'
##        self.assertEqual(expected, result, msg="Rsvp api not working")
#        
        
        
        
        
               
    
if __name__=='__main__':
    unittest.main(exit=False)