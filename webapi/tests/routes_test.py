import os, sys, inspect
import unittest
import json
import requests


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from routes import MyApis, app
from api_data import Users, Events


class TestAPIs(unittest.TestCase):
    def setUp(self):
        self.api_yangu = MyApis()

    def test_register_json(self):
        tester = app.test_client(self)
        response = tester.post('api/v2/auth/register',
                               data=dict(username = "admin", password = "1234"))
        self.assertEqual(response.status_code, 201, msg="Register api not working")

    def test_login_json(self):
        payload = {'username':'admin', 'password':'admin'}
        tester = app.test_client(self)
        response = tester.post('/api/v2/auth/login',
                               data=dict(username = "user", password = "password"))
        self.assertEqual(response.status_code, 201, msg="Login api not working")

    def test_logout_json(self):
        tester = app.test_client(self)
        tester.post('/api/v2/auth/login', data=dict(username = "user", password = "password"))
        response = tester.post('/api/v2/auth/logout')
        self.assertEqual(response.status_code, 201, msg="Logout api not working")

    def test_reset_password_json(self):
        tester = app.test_client(self)
        tester.post('/api/v2/auth/login', data=dict(username = "user", password = "password"))
        response = tester.post('/api/v2/auth/reset-password', data=dict(username = "user", 
                                                                        password = "password", 
                                                                        new_password = "somethingnew"))
        self.assertEqual(response.status_code, 201, msg="Reset password api not working")

    def test_new_event_json(self):
        tester = app.test_client(self)
        tester.post('/api/v2/auth/login', data=dict(username = "user", password = "password"))
        response = tester.post('/api/v2/events', data=dict(eventid = "myevent", 
                                                           location = "mylocation", 
                                                           date = "mydate", 
                                                           category = "mycategory"))
        self.assertEqual(response.status_code, 201, msg="Add new event api not working")

    def test_update_event_json(self):
        tester = app.test_client(self)
        tester.post('/api/v2/auth/login', data=dict(username = "user", password = "password"))
        response = tester.put('/api/v2/events/MyParty', data=dict(eventid = "myevent", 
                                                                  location = "mylocation", 
                                                                  date = "mydate", 
                                                                  category = "mycategory"))
        self.assertEqual(response.status_code, 201, msg="Update event api not working")

    def test_delete_event_json(self):
        tester = app.test_client(self)
        tester.post('/api/v2/auth/login', data=dict(username = "user", password = "password"))
        response = tester.delete('/api/v2/events/Friends')
        self.assertEqual(response.status_code, 201, msg="Delete event api not working")

    def test_view_events_json(self):
        tester = app.test_client(self)
        response = tester.get('/api/v2/events')
        self.assertEqual(response.status_code, 200, msg="View all events api not working")

    def test_send_rsvp_json(self):
        tester = app.test_client(self)
        tester.post('/api/v2/auth/login', data=dict(username = "user", password = "password"))
        response = tester.post('/api/v2/events/MyParty/rsvp')
        self.assertEqual(response.status_code, 201, msg="Send rsvp api not working")

if __name__ == '__main__':
    unittest.main(exit=False)
