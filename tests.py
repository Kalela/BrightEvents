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
        self.assertIn("Registration successful", str(response.data))
    
    def test_register_noinput_json(self):
        """Test a blank input on register endpoint"""
        tester = self.app.test_client(self)
        response = tester.post('/api/v2/auth/register',
                               data=dict(username = "", password = "1234", email = "test@email.com"))
        self.assertEqual(response.status_code, 409)
        self.assertIn("Please insert missing", str(response.data))
        
    def test_already_registered_json(self):
        """Test a user registering twice"""
        tester = self.app.test_client(self)
        tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        response = tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        self.assertEqual(response.status_code, 409)
        self.assertIn("email already", str(response.data))

    def test_login_json(self):
        """Test the user login endpoint"""
        tester = self.app.test_client(self)
        tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        response = tester.post('/api/v2/auth/login',
                               data=dict(username="admin", password="1234"))
        self.assertEqual(response.status_code, 202)
        self.assertIn("Logged in", str(response.data))
    
    def test_login_noinput_json(self):
        """Test theres no input for login endpoint"""
        tester = self.app.test_client(self)
        tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        response = tester.post('/api/v2/auth/login',
                               data=dict(username="", password="1234"))
        self.assertEqual(response.status_code, 401)
        self.assertIn("Could not verify", str(response.data))

    def test_login_nouser_json(self):
        """Test the user is not registered"""
        tester = self.app.test_client(self)
        response = tester.post('/api/v2/auth/login',
                               data=dict(username="admin", password="1234"))
        self.assertEqual(response.status_code, 401)
        self.assertIn("Could not verify", str(response.data))
        
    def test_login_noinput_json(self):
        """Test theres no input for login endpoint"""
        tester = self.app.test_client(self)
        tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        response = tester.post('/api/v2/auth/login',
                               data=dict(username="admin", password="abcd"))
        self.assertEqual(response.status_code, 401)
        self.assertIn("Could not verify", str(response.data))

    def test_logout_json(self):
        """Test the logout user endpoint"""
        tester = self.app.test_client(self)
        tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        tkn = tester.post('/api/v2/auth/login', data=dict(username = "admin", password = "1234"))
        token = json.loads(tkn.data.decode())['access-token']
        response = tester.post('/api/v2/auth/logout', headers={'x-access-token':token})
        self.assertEqual(response.status_code, 202)
        self.assertIn("logged out", str(response.data))
        
    def test_logout_twice_json(self):
        """Test the user is already logged out"""
        tester = self.app.test_client(self)
        tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        tkn = tester.post('/api/v2/auth/login', data=dict(username = "admin", password = "1234"))
        token = json.loads(tkn.data.decode())['access-token']
        tester.post('/api/v2/auth/logout', headers={'x-access-token':token})
        response = tester.post('/api/v2/auth/logout', headers={'x-access-token':token})
        self.assertEqual(response.status_code, 200)
        self.assertIn("already logged out", str(response.data))

    def test_reset_password_json(self):
        """Test the reset password endpoint"""
        tester = self.app.test_client(self)
        tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        tkn = tester.post('/api/v2/auth/login', data=dict(username = "admin", password = "1234"))
        token = json.loads(tkn.data.decode())['access-token']
        response = tester.post('/api/v2/auth/reset-password', headers={'x-access-token':token}, data=dict(old_password = "1234", 
                                                                        new_password = "somethingnew"))
        self.assertEqual(response.status_code, 205)
        self.assertIn("Password reset!", str(response.data))
        
    def test_reset_password_nologin_json(self):
        """Test the reset password if user not logged in"""
        tester = self.app.test_client(self)
        tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        tkn = tester.post('/api/v2/auth/login', data=dict(username = "admin", password = "1234"))
        token = json.loads(tkn.data.decode())['access-token']
        tester.post('/api/v2/auth/logout', headers={'x-access-token':token})
        response = tester.post('/api/v2/auth/reset-password', headers={'x-access-token':token}, data=dict(old_password = "1234", 
                                                                        new_password = "somethingnew"))
        self.assertEqual(response.status_code, 401)
        self.assertIn("Please log in", str(response.data))

    def test_new_event_json(self):
        """Test the create new event endpoint"""
        tester = self.app.test_client(self)
        tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        tkn = tester.post('/api/v2/auth/login', data=dict(username = "admin", password = "1234"))
        token = json.loads(tkn.data.decode())['access-token']
        response = tester.post('/api/v2/events',
                               data=dict(eventname = "newevent", location = "newlocation", 
                                         date = "21/05/2018", category = "newcategory"), headers={'x-access-token':token})
        self.assertEqual(response.status_code, 201)
        self.assertIn("New event", str(response.data))
        
    def test_new_event_bad_format_input_json(self):
        """Test date or other input formatted wrong"""
        tester = self.app.test_client(self)
        tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        tkn = tester.post('/api/v2/auth/login', data=dict(username = "admin", password = "1234"))
        token = json.loads(tkn.data.decode())['access-token']
        response = tester.post('/api/v2/events',
                               data=(eventname = "newevent", location = "newlocation", 
                                         date = "21052018", category = "newcategory"),
                                         headers={'x-access-token':token})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Something went wrong", str(response.data))
        
    def test_new_event_already_exists_json(self):
        """Test creating an event that already exists"""
        tester = self.app.test_client(self)
        tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        tkn = tester.post('/api/v2/auth/login', data=dict(username = "admin", password = "1234"))
        token = json.loads(tkn.data.decode())['access-token']
        tester.post('/api/v2/events', data=dict(eventname = "newevent", 
                                                location = "newlocation", 
                                                date = "21/05/2018", 
                                                 category = "newcategory"),
                                      headers={'x-access-token':token})
        response = tester.post('/api/v2/events',
                               data=dict(eventname = "newevent", 
                                         location = "newlocation", 
                                         date = "21/05/2018", 
                                         category = "newcategory"),
                               headers={'x-access-token':token})
        self.assertEqual(response.status_code, 409)
        self.assertIn("Event already", str(response.data))
        
    def test_new_event_nologin_json(self):
        """Test the create new event endpoint with user not logged in"""
        tester = self.app.test_client(self)
        tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        tkn = tester.post('/api/v2/auth/login', data=dict(username = "admin", password = "1234"))
        token = json.loads(tkn.data.decode())['access-token']
        tester.post('/api/v2/auth/logout', headers={'x-access-token':token})
        response = tester.post('/api/v2/events',
                               data=dict(eventname = "newevent", 
                                         location = "newlocation", 
                                         date = "21/05/2018", 
                                         category = "newcategory"),
                               headers={'x-access-token':token})
        self.assertEqual(response.status_code, 401)
        self.assertIn("Please Log In", str(response.data))

    def test_update_event_json(self):
        """Test the update existing event endpoint"""
        tester = self.app.test_client(self)
        tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        tkn = tester.post('/api/v2/auth/login', data=dict(username = "admin", password = "1234"))
        token = json.loads(tkn.data.decode())['access-token']
        tester.post('/api/v2/events',
                    headers={'x-access-token':token},
                    data=dict(eventname = "newevent", 
                              location = "newlocation", 
                              date = "21/05/2018", 
                              category = "newcategory"))
        response = tester.put('/api/v2/events/newevent',
                              data=dict(eventid = "myevent", 
                                        location = "mylocation", 
                                        date = "19/03/2018", 
                                        category = "mycategory"),
                              headers={'x-access-token':token})
        self.assertEqual(response.status_code, 202)
        self.assertIn("updated to", str(response.data))
        
    def test_update_event_bad_input_json(self):
        """Test date or other input formatted wrong"""
        tester = self.app.test_client(self)
        tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        tkn = tester.post('/api/v2/auth/login', data=dict(username = "admin", password = "1234"))
        token = json.loads(tkn.data.decode())['access-token']
        tester.post('/api/v2/events',
                    headers={'x-access-token':token},
                    data=dict(eventname = "newevent", 
                              location = "newlocation", 
                              date = "21/05/2018", 
                              category = "newcategory"))
        response = tester.put('/api/v2/events/newevent',
                              data=dict(eventid = "myevent", 
                                        location = "mylocation", 
                                        date = "19032018", 
                                        category = "mycategory"),
                              headers={'x-access-token':token})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Something went wrong", str(response.data))
        
    def test_update_event_does_not_exist_json(self):
        """Test update existing event if event does not exist"""
        tester = self.app.test_client(self)
        tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        tkn = tester.post('/api/v2/auth/login', data=dict(username = "admin", password = "1234"))
        token = json.loads(tkn.data.decode())['access-token']
        response = tester.put('/api/v2/events/newevent',
                              data=dict(eventid = "myevent", 
                                        location = "mylocation", 
                                        date = "19/03/2018", 
                                        category = "mycategory"),
                              headers={'x-access-token':token})
        self.assertEqual(response.status_code, 404)
        self.assertIn("does not exist", str(response.data))

    def test_delete_event_json(self):
        """Test the delete event endpoint"""
        tester = self.app.test_client(self)
        tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        tkn = tester.post('/api/v2/auth/login', data=dict(username = "admin", password = "1234"))
        token = json.loads(tkn.data.decode())['access-token']
        tester.post('/api/v2/events',
                    data=dict(eventname = "newevent", 
                              location = "newlocation", 
                              date = "21/05/2018", 
                              category = "newcategory"),
                    headers={'x-access-token':token})
        response = tester.delete('api/v2/events/newevent', headers={'x-access-token':token})
        self.assertEqual(response.status_code, 205)
        self.assertIn("Event(s)", str(response.data))
        
    def test_delete_event_does_not_exist_json(self):
        """Test the delete event does not exist"""
        tester = self.app.test_client(self)
        tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        tkn = tester.post('/api/v2/auth/login', data=dict(username = "admin", password = "1234"))
        token = json.loads(tkn.data.decode())['access-token']
        response = tester.delete('api/v2/events/newevent', headers={'x-access-token':token})
        self.assertEqual(response.status_code, 404)
        self.assertIn("does not exist", str(response.data))

    def test_view_events_json(self):
        """Test the view all events endpoint"""
        tester = self.app.test_client(self)
        tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        tkn = tester.post('/api/v2/auth/login', data=dict(username = "admin", password = "1234"))
        token = json.loads(tkn.data.decode())['access-token']
        response = tester.get('/api/v2/events', headers={'x-access-token':token})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Events", str(response.data))
        
    def test_search_events_json(self):
        """Test the view all events endpoint"""
        tester = self.app.test_client(self)
        tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        tkn = tester.post('/api/v2/auth/login', data=dict(username = "admin", password = "1234"))
        token = json.loads(tkn.data.decode())['access-token']
        q = "the"
        response = tester.get('/api/v2/events', headers={'x-access-token':token})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Events", str(response.data))

    def test_send_rsvp_json(self):
        """Test the send rsvp endpoint"""
        tester = self.app.test_client(self)
        tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        tkn = tester.post('/api/v2/auth/login', data=dict(username = "admin", password = "1234"))
        token = json.loads(tkn.data.decode())['access-token']
        tester.post('/api/v2/events',
                    data=dict(eventname = "newevent", 
                              location = "newlocation", 
                              date = "21/05/2018", 
                              category = "newcategory"),
                    headers={'x-access-token':token})
        response = tester.post('/api/v2/events/newevent/rsvp', headers={'x-access-token':token})
        self.assertEqual(response.status_code, 201)
        self.assertIn("RSVP sent", str(response.data))
        
    def test_rsvp_already_sent_json(self):
        """Test rsvp sent twice"""
        tester = self.app.test_client(self)
        tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        tkn = tester.post('/api/v2/auth/login', data=dict(username = "admin", password = "1234"))
        token = json.loads(tkn.data.decode())['access-token']
        tester.post('/api/v2/events',
                    data=dict(eventname = "newevent", 
                              location = "newlocation", 
                              date = "21/05/2018", 
                              category = "newcategory"),
                    headers={'x-access-token':token})
        tester.post('/api/v2/events/newevent/rsvp', headers={'x-access-token':token})
        response = tester.post('/api/v2/events/newevent/rsvp', headers={'x-access-token':token})
        self.assertEqual(response.status_code, 409)
        self.assertIn("already sent", str(response.data))
        
    def test_rsvp_event_does_not_exist_json(self):
        """Test rsvp to a non-existent event"""
        tester = self.app.test_client(self)
        tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        tkn = tester.post('/api/v2/auth/login', data=dict(username = "admin", password = "1234"))
        token = json.loads(tkn.data.decode())['access-token']
        tester.post('/api/v2/events/newevent/rsvp', headers={'x-access-token':token})
        response = tester.post('/api/v2/events/newevent/rsvp', headers={'x-access-token':token})
        self.assertEqual(response.status_code, 404)
        self.assertIn("does not exist", str(response.data))
        
    def test_rsvp_user_logged_out_json(self):
        """Test rsvp if a user is not logged in"""
        tester = self.app.test_client(self)
        tester.post('/api/v2/auth/register',
                               data=dict(username = "admin", password = "1234", email = "test@email.com"))
        tkn = tester.post('/api/v2/auth/login', data=dict(username = "admin", password = "1234"))
        token = json.loads(tkn.data.decode())['access-token']
        tester.post('/api/v2/events',
                    data=dict(eventname = "newevent", 
                              location = "newlocation", 
                              date = "21/05/2018", 
                              category = "newcategory"),
                    headers={'x-access-token':token})
        tester.post('/api/v2/auth/logout', headers={'x-access-token':token})
        tester.post('/api/v2/events/newevent/rsvp', headers={'x-access-token':token})
        response = tester.post('/api/v2/events/newevent/rsvp', headers={'x-access-token':token})
        self.assertEqual(response.status_code, 401)
        self.assertIn("log in", str(response.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main(exit=False)
