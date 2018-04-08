import unittest
import json

from webapi.routes import create_app, db

class TestUserEndpoints(unittest.TestCase):
    """Contains all user tests"""
    def setUp(self):
        """Set up the application with configurations for testing"""
        self.app = create_app(config_name="testing")
        self.tester = self.app.test_client(self)
        self.prefix = "/api/v2"
        with self.app.app_context():
            db.create_all()

    def register_and_login(self, choice):
        if choice == "both":
            self.tester.post('%s/auth/register' % self.prefix,
                                       data=dict(username = "admin",
                                                 password = "12345678",
                                                 email = "test@email.com"))
            tkn = self.tester.post('%s/auth/login' % self.prefix, data=dict(username ="admin",
                                                                   password = "12345678"))
            self.token = json.loads(tkn.data.decode())['access_token']

        if choice == "login":
            return self.tester.post('%s/auth/login' % self.prefix, data=dict(username = "admin",
                                                                         password = "12345678"))

        if choice == "register":
            return self.tester.post('%s/auth/register' % self.prefix,
                                       data=dict(username = "admin",
                                             password = "12345678",
                                             email = "test@email.com"))

    def test_register(self):
        """Test the register user endpoint"""
        response = self.register_and_login("register")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Registration successful", str(response.data))

    def test_register_noinput(self):
        """Test a blank input on register endpoint"""
        response = self.tester.post('%s/auth/register' % self.prefix,
                               data=dict(username = "", password = "12345678",
                                         email = "test@email.com"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("Please insert", str(response.data))

    def test_register_bad_email_input(self):
        """Test if email input on register endpoint is not valid"""
        response = self.tester.post('%s/auth/register' % self.prefix,
                               data=dict(username = "admin", password = "1234",
                                         email = "testemail.com"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("insert a valid email", str(response.data))

    def test_already_registered(self):
        """Test a user registering twice"""
        self.register_and_login("register")
        response = self.register_and_login("register")
        self.assertEqual(response.status_code, 409)
        self.assertIn("email already", str(response.data))

    def test_register_with_weak_password(self):
        """Test a user with weak password can't register"""
        response = self.tester.post('%s/auth/register' % self.prefix,
                                   data=dict(username = "admin",
                                             password = "a",
                                             email = "test@email.com"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("At least 6", str(response.data))

    def test_login(self):
        """Test the user login endpoint"""
        self.register_and_login("register")
        response = self.register_and_login("login")
        self.assertEqual(response.status_code, 202)
        self.assertIn("Logged in", str(response.data))

    def test_login_noinput(self):
        """Test theres no input for login endpoint"""
        self.register_and_login("register")
        response = tester.post('%s/auth/login' % self.prefix,
                               data=dict(username = "", password = "1234"))
        self.assertEqual(response.status_code, 401)
        self.assertIn("Could not verify", str(response.data))

    def test_login_nouser(self):
        """Test the user is not registered"""
        response = self.register_and_login("login")
        self.assertEqual(response.status_code, 401)
        self.assertIn("Could not verify", str(response.data))

    def test_login_noinput(self):
        """Test theres no input for login endpoint"""
        self.register_and_login("register")
        response = self.tester.post('%s/auth/login' % self.prefix,
                               data=dict(username = "admin", password = "abcd"))
        self.assertEqual(response.status_code, 401)
        self.assertIn("Could not verify", str(response.data))

    def test_logout(self):
        """Test the logout user endpoint"""
        self.register_and_login("both")
        response = self.tester.post('%s/auth/logout' % self.prefix, headers={'x-access-token':self.token})
        self.assertEqual(response.status_code, 202)
        self.assertIn("logged out", str(response.data))

    def test_logout_twice(self):
        """Test the user is already logged out"""
        self.register_and_login("both")
        self.tester.post('%s/auth/logout' % self.prefix, headers={'x-access-token':self.token})
        response = self.tester.post('%s/auth/logout' % self.prefix, headers={'x-access-token':self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn("already logged out", str(response.data))

    def test_reset_password(self):
        """Test the reset password endpoint"""
        self.register_and_login("both")
        response = self.tester.post('%s/auth/reset-password' % self.prefix,
                               headers={'x-access-token':self.token},
                               data=dict(new_password = "somethingnew", confirm_password = "somethingnew"))
        self.assertEqual(response.status_code, 205)
        self.assertIn("Password reset!", str(response.data))

    def test_reset_password_wrongconfirm(self):
        """Test the reset password endpoint if confirm and new don't match"""
        self.register_and_login("both")
        response = self.tester.post('%s/auth/reset-password' % self.prefix,
                               headers={'x-access-token':self.token},
                               data=dict(new_password = "somethingnew", confirm_password = "omethingnew"))
        self.assertEqual(response.status_code, 409)
        self.assertIn("Passwords don", str(response.data))

    def test_reset_password_old(self):
        """Test the reset password endpoint if user input is same as old password"""
        self.register_and_login("both")
        response = self.tester.post('%s/auth/reset-password' % self.prefix,
                               headers={'x-access-token':self.token},
                               data=dict(new_password = "12345678", confirm_password = "12345678"))
        self.assertEqual(response.status_code, 409)
        self.assertIn("Password already set", str(response.data))

    def test_reset_password_nologin(self):
        """Test the reset password if user not logged in"""
        response = self.register_and_login("both")
        self.tester.post('/api/v2/auth/logout', headers={'x-access-token':self.token})
        response = self.tester.post('%s/auth/reset-password' % self.prefix,
                               headers={'x-access-token':self.token},
                               data=dict(new_password = "somethingnew", confirm_password = "somethingnew"))
        self.assertEqual(response.status_code, 401)
        self.assertIn("Please log in", str(response.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
