#Import dependancies
import unittest
import json

from webapi.routes import create_app, db

class TestEventEndpoints(unittest.TestCase):
    """Contains all user tests"""
    def setUp(self):
        """Set up the application with configurations for testing"""
        self.app = create_app(config_name="testing")
        self.tester = self.app.test_client(self)
        self.prefix = "/api/v2"
        with self.app.app_context():
            db.create_all()

    def register_and_login(self):
        self.tester.post('%s/auth/register' % self.prefix,
                                   data=dict(username = "admin",
                                         password = "12345678",
                                         confirmpassword = "12345678",
                                         email = "test@email.com"))
        tkn = self.tester.post('%s/auth/login' % self.prefix, data=dict(username = "admin",
                                                               password = "12345678"))
        self.token = json.loads(tkn.data.decode())['access_token']

    def create_new_event(self):
        return self.tester.post('%s/events' % self.prefix,
                                   data=dict(eventname="newevent", location="newlocation",
                                             date="2018/05/21", category="Social"),
                                   headers={'x-access-token':self.token})

    def test_new_event(self):
            """Test the create new event endpoint"""
            self.register_and_login()
            response = self.create_new_event()
            self.assertEqual(response.status_code, 201)
            self.assertIn("New event", str(response.data))

    def test_create_new_event_bad_category(self):
            """Test the create new event endpoint with a wrong category"""
            self.register_and_login()
            response = self.tester.post('%s/events' % self.prefix,
                                   data=dict(eventname="newevent", location="newlocation",
                                             date="2018/06/21", category="mycategory"),
                                   headers={'x-access-token':self.token})
            self.assertEqual(response.status_code, 406)
            self.assertIn("select a viable category", str(response.data))

    def test_same_event_different_date(self):
            """Test the creating the same event with a different date endpoint"""
            self.register_and_login()
            self.create_new_event()
            response = self.tester.post('%s/events' % self.prefix,
                                   data=dict(eventname="newevent", location="newlocation",
                                             date="2018/06/21", category="Social"),
                                   headers={'x-access-token':self.token})
            self.assertEqual(response.status_code, 201)
            self.assertIn("New event", str(response.data))

    def test_new_event_with_bad_format_input(self):
        """Test date or other input formatted wrong"""
        self.register_and_login()
        response = self.tester.post('%s/events' % self.prefix,
                               data=dict(eventname = "newevent", location = "newlocation",
                                         date = "21052018", category = "Social"),
                                         headers={'x-access-token':self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Wrong date", str(response.data))

    def test_new_event_already_exists(self):
        """Test creating an event that already exists"""
        self.register_and_login()
        self.create_new_event()
        response = self.create_new_event()
        self.assertEqual(response.status_code, 409)
        self.assertIn("Event already", str(response.data))

    def test_new_event_nologin(self):
        """Test the create new event endpoint with user not logged in"""
        self.register_and_login()
        self.tester.post('%s/auth/logout' % self.prefix, headers={'x-access-token':self.token})
        response = self.create_new_event()
        self.assertEqual(response.status_code, 401)
        self.assertIn("Please Log In", str(response.data))

    def test_update_event(self):
        """Test the update existing event endpoint"""
        self.register_and_login()
        self.create_new_event()
        response = self.tester.put('%s/events/newevent' % self.prefix,
                              data=dict(event_name = "myevent",
                                        location = "mylocation",
                                        date = "2018/03/19",
                                        category = "Social"),
                              headers={'x-access-token':self.token})
        self.assertEqual(response.status_code, 202)
        self.assertIn("updated to", str(response.data))

    def test_update_event_bad_category(self):
        """Test the update existing event endpoint"""
        self.register_and_login()
        self.create_new_event()
        response = self.tester.put('%s/events/newevent' % self.prefix,
                              data=dict(event_name = "myevent",
                                        location = "mylocation",
                                        date = "2018/03/19",
                                        category = "abc"),
                              headers={'x-access-token':self.token})
        self.assertEqual(response.status_code, 406)
        self.assertIn("a viable category", str(response.data))

    def test_update_event_bad_input(self):
        """Test date or other input formatted wrong"""
        self.register_and_login()
        self.create_new_event()
        response = self.tester.put('%s/events/newevent' % self.prefix,
                              data=dict(event_name = "myevent",
                                        location = "mylocation",
                                        date = "19032018",
                                        category = "Social"),
                              headers={'x-access-token':self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Wrong date", str(response.data))

    def test_update_event_does_not_exist(self):
        """Test update existing event if event does not exist"""
        self.register_and_login()
        response = self.tester.put('%s/events/newevent' % self.prefix,
                              data=dict(event_name = "myevent",
                                        location = "mylocation",
                                        date = "2018/03/19",
                                        category = "Social"),
                              headers={'x-access-token':self.token})
        self.assertEqual(response.status_code, 404)
        self.assertIn("does not exist", str(response.data))

    def test_delete_event(self):
        """Test the delete event endpoint"""
        self.register_and_login()
        self.create_new_event()
        response = self.tester.delete('%s/events/newevent' % self.prefix, headers={'x-access-token':self.token})
        self.assertEqual(response.status_code, 205)
        self.assertIn("Event(s)", str(response.data))

    def test_delete_event_does_not_exist(self):
        """Test the delete event does not exist"""
        self.register_and_login()
        response = self.tester.delete('%s/events/newevent' % self.prefix, headers={'x-access-token':self.token})
        self.assertEqual(response.status_code, 404)
        self.assertIn("does not exist", str(response.data))
#
    def test_view_one_event(self):
        """Test viewing a single event"""
        self.register_and_login()
        self.create_new_event()
        response = self.tester.get('%s/events/newevent' % self.prefix, headers={'x-access-token':self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn("eventname", str(response.data))

    def test_view_events(self):
        """Test the view all events endpoint"""
        self.register_and_login()
        self.create_new_event()
        response = self.tester.get('%s/events' % self.prefix)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Events", str(response.data))

    def test_view_current_user_events(self):
        """Test the view all events endpoint"""
        self.register_and_login()
        self.create_new_event()
        response = self.tester.get('%s/myevents' % self.prefix, headers={'x-access-token':self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Events", str(response.data))

    def test_search_events(self):
        """Test the view all events endpoint"""
        self.register_and_login()
        response = self.tester.get('%s/events?q=new' % self.prefix, headers={'x-access-token':self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Events", str(response.data))

    def test_send_rsvp(self):
        """Test the send rsvp endpoint"""
        self.register_and_login()
        self.create_new_event()
        response = self.tester.post('%s/events/newevent/rsvp' % self.prefix, headers={'x-access-token':self.token},
                                    data=(dict(owner="admin")))
        self.assertEqual(response.status_code, 201)
        self.assertIn("RSVP sent", str(response.data))

    def test_view_guests(self):
        """Test if users can view guests with rsvps to their events"""
        self.register_and_login()
        self.create_new_event()
        self.tester.post('%s/events/newevent/rsvp' % self.prefix, headers={'x-access-token':self.token},
                                    data=(dict(owner="admin")))
        response = self.tester.get('%s/events/newevent/rsvp' % self.prefix, headers={'x-access-token':self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Guests", str(response.data))

    def test_view_guests_no_guests(self):
        """Test an attempt to view guests if no one sent rsvp yet"""
        self.register_and_login()
        self.create_new_event()
        response = self.tester.get('%s/events/newevent/rsvp' % self.prefix, headers={'x-access-token':self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn("guests yet", str(response.data))

    def test_view_guests_no_event(self):
        """Test an attempt to view guests if the event does not exist"""
        self.register_and_login()
        self.create_new_event()
        self.tester.post('%s/events/newevent/rsvp' % self.prefix, headers={'x-access-token':self.token},
                                    data=(dict(owner="admin")))
        self.tester.delete('%s/events/newevent' % self.prefix, headers={'x-access-token':self.token})
        response = self.tester.get('%s/events/newevent/rsvp' % self.prefix, headers={'x-access-token':self.token})
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", str(response.data))

    def test_rsvp_already_sent(self):
        """Test rsvp sent twice"""
        self.register_and_login()
        self.create_new_event()
        self.tester.post('%s/events/newevent/rsvp' % self.prefix,
                         data=(dict(owner="admin")),
                         headers={'x-access-token':self.token})
        response = self.tester.post('%s/events/newevent/rsvp' % self.prefix,
                                    data=(dict(owner="admin")),
                                    headers={'x-access-token':self.token})
        self.assertEqual(response.status_code, 409)
        self.assertIn("already sent", str(response.data))

    def test_rsvp_event_does_not_exist(self):
        """Test rsvp to a non-existent event"""
        self.register_and_login()
        response = self.tester.post('%s/events/newevent/rsvp' % self.prefix,
                                    data=(dict(owner="admin")),
                                    headers={'x-access-token':self.token})
        self.assertEqual(response.status_code, 404)
        self.assertIn("does not exist", str(response.data))

    def test_rsvp_user_logged_out(self):
        """Test rsvp if a user is not logged in"""
        self.register_and_login()
        self.create_new_event()
        self.tester.post('%s/auth/logout' % self.prefix, headers={'x-access-token':self.token})
        response = self.tester.post('%s/events/newevent/rsvp' % self.prefix,
                                    data=dict(owner="admin"),
                                    headers={'x-access-token':self.token})
        self.assertEqual(response.status_code, 401)
        self.assertIn("log in", str(response.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
