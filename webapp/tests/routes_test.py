import os, sys, inspect
import unittest
import json
import requests


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from routes import MyApis
from routes import app
from entities import Users
from entities import Events


class TestAPIs(unittest.TestCase):
    def setUp(self):
        self.api_yangu = MyApis()

    def test_register_json(self):
        payload = {'username':'admin', 'password':'admin'}
        tester = app.test_client(self)
        response = tester.post('/api/v2/auth/register',
                               content_type="application/json",
                               data=json.dumps(payload))
        self.assertEqual(response.status_code, 201, msg="Register api not working")

    def test_login_json(self):
        payload = {'username':'admin', 'password':'admin'}
        tester = app.test_client(self)
        response = tester.post('/api/v2/auth/login',
                               content_type="application/json",
                               data=json.dumps(payload))
        self.assertEqual(response.status_code, 201, msg="Login api not working")

    def test_logout_json(self):
        tester = app.test_client(self)
        response = tester.post('/api/v2/auth/logout', content_type="application/json")
        self.assertEqual(response.status_code, 201, msg="Logout api not working")

    def test_reset_password_json(self):
        tester = app.test_client(self)
        response = tester.post('/api/v2/auth/reset-password', content_type="application/json")
        self.assertEqual(response.status_code, 201, msg="Reset password api not working")

    def test_new_event_json(self):
        tester = app.test_client(self)
        response = tester.post('/api/v2/events', content_type="application/json")
        self.assertEqual(response.status_code, 201, msg="Reset password api not working")

#    def test_update_event_json(self):
#        tester = app.test_client(self)
#        response = tester.put('/api/v2/events/<eventid>', content_type="application/json")
#        self.assertEqual(response.status_code, 201, msg="Update event api not working")

#    def test_delete_event_json(self):
#        tester = app.test_client(self)
#        response = tester.delete('/api/v2/events/<eventid>', content_type="application/json")
#        self.assertEqual(response.status_code, 201, msg="Update event api not working")

    def test_view_events_json(self):
        tester = app.test_client(self)
        response = tester.get('/api/v2/events', content_type="application/json")
        self.assertEqual(response.status_code, 200, msg="View all events api not working")

    def test_send_rsvp_json(self):
        tester = app.test_client(self)
        response = tester.post('/api/v2/events/<eventid>/rsvp', content_type="application/json")
        self.assertEqual(response.status_code, 201, msg="Send rsvp api not working")

##    def test_rsvp_json(self):
##        expected = eventid + ' RSVP Sent'
##        result = evn[0]['eventid'] += ' RSVP Sent'
##        self.assertEqual(expected, result, msg="Rsvp api not working")

if __name__ == '__main__':
    unittest.main(exit=False)
