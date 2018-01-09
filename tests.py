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
        self.assertIn("1234", str(response.data))
    
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
        response = tester.post('/api/v2/auth/login',
                               data=dict(username = "Admin", password = "admin"))
        self.assertEqual(response.status_code, 202)
        self.assertIn("Logged in", str(response.data))

    def test_logout_json(self):
        """Test the logout user endpoint"""
        tester = self.app.test_client(self)
        tester.post('/api/v2/auth/login', data=dict(username = "Admin", password = "admin"))
        response = tester.post('/api/v2/auth/logout')
        self.assertEqual(response.status_code, 202)
        self.assertIn("logged out", str(response.data))
#
#    def test_reset_password_json(self):
#        """Test the reset password endpoint"""
#        tester = self.app.test_client(self)
#        tester.post('/api/v2/auth/login', data=dict(username = "user", password = "password"))
#        response = tester.post('/api/v2/auth/reset-password', data=dict(username = "user", 
#                                                                        password = "password", 
#                                                                        new_password = "somethingnew"))
#        self.assertEqual(response.status_code, 205)
#        self.assertIn("Password changed", str(response.data))
#
#    def test_new_event_json(self):
#        """Test the create new event endpoint"""
#        tester = self.app.test_client(self)
#        tester.post('/api/v2/auth/login', data=dict(username = "user", password = "password"))
#        response = tester.post('/api/v2/events', data=dict(eventid = "myevent", 
#                                                           location = "mylocation", 
#                                                           date = "mydate", 
#                                                           category = "mycategory"))
#        self.assertEqual(response.status_code, 201)
#        self.assertIn("events", str(response.data))
#
#    def test_update_event_json(self):
#        """Test the update existing event endpoint"""
#        tester = self.app.test_client(self)
#        tester.post('/api/v2/auth/login', data=dict(username = "user", password = "password"))
#        response = tester.put('/api/v2/events/MyParty', data=dict(eventid = "myevent", 
#                                                                  location = "mylocation", 
#                                                                  date = "mydate", 
#                                                                  category = "mycategory"))
#        self.assertEqual(response.status_code, 202)
#        self.assertIn("edited to", str(response.data))
#
#    def test_delete_event_json(self):
#        """Test the delete event endpoint"""
#        tester = self.app.test_client(self)
#        tester.post('/api/v2/auth/login', data=dict(username = "user", password = "password"))
#        response = tester.delete('api/v2/events/Friends')
#        self.assertEqual(response.status_code, 205)
#        self.assertIn("User events", str(response.data))
#
#    def test_view_events_json(self):
#        """Test the view all events endpoint"""
#        tester = self.app.test_client(self)
#        response = tester.get('/api/v2/events')
#        self.assertEqual(response.status_code, 200)
#        self.assertIn("user events", str(response.data))
#
#    def test_send_rsvp_json(self):
#        """Test the send rsvp endpoint"""
#        tester = self.app.test_client(self)
#        tester.post('/api/v2/auth/login', data=dict(username = "user", password = "password"))
#        response = tester.post('/api/v2/events/MyParty/rsvp')
#        self.assertEqual(response.status_code, 201)
#        self.assertIn("RSVPs sent", str(response.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main(exit=False)
