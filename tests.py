import os, sys, inspect
import unittest
import requests

from webapp.app import create_app
from webapp.entities import Users, Events

class TestAPIs(unittest.TestCase):
    """Enclose all tests"""
    def setUp(self):
        """Set up class containing test conditions"""
        self.app = create_app(config_name="testing")
        self.app.config['SECRET_KEY'] = 'my-secret-key'

    #Index Page 'GET'
    def test_index_page_loads(self):
        """Test if the index page loads up"""
        tester = self.app.test_client(self)
        response = tester.get('/', content_type='html/txt')
        self.assertEqual(response.status_code, 200, msg="Page Not Loaded")

    #Register page 'GET'
    def test_register_page_loads(self):
        """Test if the register page loads"""
        tester = self.app.test_client(self)
        response = tester.get('/api/v1/auth/register', content_type='html/txt')
        self.assertTrue(b"Sign Up" in response.data, msg="Register page didn't load properly")

    #Test if register behaves correctly given the correct input
    def test_correct_register_input(self):
        """Test if a correct register input is acknowledged"""
        tester = self.app.test_client(self)
        response = tester.post('/api/v1/auth/register',
                               data=dict(username='user', password='password'),
                               follow_redirects=True)
        self.assertIn(b"Log In", response.data, msg="Register api does not work")

    #Login page 'GET'
    def test_login_page_loads(self):
        """Test if login page loads"""
        tester = self.app.test_client(self)
        response = tester.get('/api/v1/auth/login', content_type='html/txt')
        self.assertTrue(b"Log In" in response.data, msg="Login page didn't load properly")

    #Test if login behaves correctly given the correct input
    def test_correct_login_input(self):
        """Test if a correct login is correctly responded to"""
        tester = self.app.test_client(self)
        response = tester.post('/api/v1/auth/login',
                               data=dict(username='user', password='password'),
                               follow_redirects=True)
        self.assertIn(b"Account Status", response.data, msg="Login api does not work")

    #Test if user log out works
    def test_logout(self):
        """Test if a user can log out"""
        tester = self.app.test_client(self)
        response = tester.post('/api/v1/auth/logout', follow_redirects=True)
        self.assertIn(b"Welcome to EventHub", response.data, msg="Logout api does not work")

    #Dashboard 'GET'
    def test_dashboard_loads(self):
        """Test if the dashboard loads up correctly"""
        tester = self.app.test_client(self)
        response = tester.get('/api/v1/auth/dashboard', content_type='html/txt')
        self.assertTrue(b"Account Status" in response.data, msg="Dashboard didn't load properly")

    #New Event page 'GET'
    def test_new_event_page_loads(self):
        """Test if the page for event creation loads"""
        tester = self.app.test_client(self)
        response = tester.get('/api/v1/new_event', content_type='html/txt')
        self.assertTrue(b"Create New" in response.data, msg="New Event Page didn't load properly")

    #Test if user create event works
    def test_create_new_event(self):#Review logic
        """Test if a user can create a new event"""
        tester = self.app.test_client(self)
        response = tester.post('/api/v1/new_event', follow_redirects=True)
        self.assertIn(b"Account Status", response.data, msg="Create event api does not work")

    #All Events page 'GET'
    def test_view_all_user_events(self):
        """Test if user can view all available events"""
        tester = self.app.test_client(self)
        response = tester.get('/api/v1/events/view', content_type='html/txt')
        self.assertTrue(b"Your Events" in response.data,
                        msg="User Events Page didn't load properly")

    #About Us page 'GET'
    def test_about_us(self):
        """Test if about us page loads correctly"""
        tester = self.app.test_client(self)
        response = tester.get('/api/v1/about', content_type='html/txt')
        self.assertTrue(b"EventHub is a Bright Events offshoot" in response.data,
                        msg="About Us Page didn't load properly")

#    #Test user send RSVP
#    def test_send_rsvp(self):
#        tester = app.test_client(self)
#        response = tester.post('/api/v1/send/<eventid>/RSVP', follow_redirects=True)
#        self.assertIn(b"Account Status", response.data, msg="Send RSVP api does not work")

if __name__ == '__main__':
    unittest.main(exit=False)