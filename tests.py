import os
import unittest
import json
import requests

from webapi.routes import create_app, db
from webapi.api_data import Users, Events

class TestAPIs(unittest.TestCase):
    """Contains all tests"""
    def setUp(self):
        """Set up the application with configurations for testing"""
        self.app = create_app(config_name="testing")
        with self.app.app_context():
            db.create_all()      

    def test_register_json(self):
        """Test the register user endpoint"""
        tester = self.app.test_client(self)
        response = tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        self.assertEqual(response.status_code, 201)
        self.assertIn("date_created", str(response.data))
    
    def test_register_noinput_json(self):
        """Test the register user endpoint"""
        tester = self.app.test_client(self)
        response = tester.post('/api/v2/auth/register',
                               data=dict(username = "", password = "1234", email = "test@email.com"))
        self.assertEqual(response.status_code, 409)
        self.assertIn("Please insert missing", str(response.data))

    def test_login_json(self):
        """Test the user login endpoint"""
        tester = self.app.test_client(self)
        tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        response = tester.post('/api/v2/auth/login',
                               data=dict(username="admin", password="1234"))
        self.assertEqual(response.status_code, 202)
        self.assertIn("Logged in", str(response.data))

#    def test_logout_json(self):
#        """Test the logout user endpoint"""
#        tester = self.app.test_client(self)
#        tester.post('/api/v2/auth/register',
#                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
#        tkn = tester.post('/api/v2/auth/login', data=dict(username = "admin", password = "1234"))
#        token = json.loads(tkn.data.decode())['access-token']
#        response = tester.post('/api/v2/auth/logout', headers=dict(Authorization="Bearer " + token))
#        self.assertEqual(response.status_code, 202)
#        self.assertIn("logged out", str(response.data))

#    def test_reset_password_json(self):
#        """Test the reset password endpoint"""
#        tester = self.app.test_client(self)
#        tester.post('/api/v2/auth/register',
#                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
#        tester.post('/api/v2/auth/login', data=dict(username = "admin", password = "1234"))
#        response = tester.post('/api/v2/auth/reset-password', data=dict(old_password = "1234", 
#                                                                        new_password = "somethingnew"))
#        self.assertEqual(response.status_code, 205)
#        self.assertIn("Password changed", str(response.data))
#
#    def test_new_event_json(self):
#        """Test the create new event endpoint"""
#        tester = self.app.test_client(self)
#        tester.post('/api/v2/auth/register',
#                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
#        tester.post('/api/v2/auth/login', data=dict(username = "admin", password = "1234"))
#        response = tester.post('/api/v2/events', data=dict(eventname = "newevent", 
#                                                           location = "newlocation", 
#                                                           date = "21/05/2018", 
#                                                           category = "newcategory"))
#        self.assertEqual(response.status_code, 201)
#        self.assertIn("New event", str(response.data))
#
#    def test_update_event_json(self):
#        """Test the update existing event endpoint"""
#        tester = self.app.test_client(self)
#        tester.post('/api/v2/auth/register',
#                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
#        tester.post('/api/v2/auth/login', data=dict(username = "admin", password = "1234"))
#        tester.post('/api/v2/events', data=dict(eventname = "newevent", 
#                                                           location = "newlocation", 
#                                                           date = "21/05/2018", 
#                                                           category = "newcategory"))
#        response = tester.put('/api/v2/events/newevent', data=dict(eventid = "myevent", 
#                                                                  location = "mylocation", 
#                                                                  date = "19/03/2018", 
#                                                                  category = "mycategory"))
#        self.assertEqual(response.status_code, 202)
#        self.assertIn("updated to", str(response.data))
#
#    def test_delete_event_json(self):
#        """Test the delete event endpoint"""
#        tester = self.app.test_client(self)
#        tester.post('/api/v2/auth/register',
#                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
#        tester.post('/api/v2/auth/login', data=dict(username = "admin", password = "1234"))
#        tester.post('/api/v2/events', data=dict(eventname = "newevent", 
#                                                           location = "newlocation", 
#                                                           date = "21/05/2018", 
#                                                           category = "newcategory"))
#        response = tester.delete('api/v2/events/newevent')
#        self.assertEqual(response.status_code, 205)
#        self.assertIn("Event(s)", str(response.data))
#
#    def test_view_events_json(self):
#        """Test the view all events endpoint"""
#        tester = self.app.test_client(self)
#        response = tester.get('/api/v2/events')
#        self.assertEqual(response.status_code, 200)
#        self.assertIn("Events", str(response.data))
#
#    def test_send_rsvp_json(self):
#        """Test the send rsvp endpoint"""
#        tester = self.app.test_client(self)
#        tester.post('/api/v2/auth/register',
#                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
#        tester.post('/api/v2/auth/login', data=dict(username = "admin", password = "1234"))
#        tester.post('/api/v2/events', data=dict(eventname = "newevent", 
#                                                           location = "newlocation", 
#                                                           date = "21/05/2018", 
#                                                           category = "newcategory"))
#        response = tester.post('/api/v2/events/newevent/rsvp')
#        self.assertEqual(response.status_code, 201)
#        self.assertIn("RSVP sent", str(response.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main(exit=False)
