# project/test_users.py


import os
import unittest

from config import basedir
from app import app, db
from app.models import User


TEST_DB = 'user.db'


class UsersTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    # executed after each test
    def tearDown(self):
        pass


    ########################
    #### helper methods ####
    ########################

    def register(self, email, password, confirm):
        return self.app.post(
            '/register',
            data=dict(email=email, password=password, password2=password, firstname=firstname, surname=surname),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def create_user(self):
        new_user = User(firstname="Dave", surname="Jones", email='nowhwere@gmail.com', password_hash='AdMiNpAsSwOrD')
        db.session.add(new_user)
        db.session.commit()


    ###############
    #### tests ####
    ###############

    def test_user_registration_form_displays(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please Register Your New Account', response.data)

    def test_valid_user_registration(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('sam@gmail.com', 'PleaseWork123', 'PleaseWork123', 'Sam','Matt')
        self.assertIn(b'Congratulations, you are now a registered user!', response.data)

    def test_duplicate_email_user_registration_error(self):
        self.app.get('/register', follow_redirects=True)
        self.register('heronakumura@gmail.com', 'PleaseWork123', 'PleaseWork123')
        self.app.get('/register', follow_redirects=True)
        response = self.register('heronakumura@gmail.com', 'ThisMustWork123', 'ThisMustWork123')
        self.assertIn(b'ERROR! Email (heronakumura@gmail.com) already exists.', response.data)

    def test_missing_field_user_registration_error(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('heronakumura@gmail.com', 'PleaseWork123', '')
        self.assertIn(b'This field is required.', response.data)


    def test_valid_login(self):
        self.app.get('/register', follow_redirects=True)
        self.register('heronakumura@gmail.com', 'PleaseWork123', 'PleaseWork123')
        self.app.get('/logout', follow_redirects=True)
        self.app.get('/login', follow_redirects=True)
        response = self.login('heronakumura@gmail.com', 'PleaseWork123')
        self.assertIn(b'heronakumura@gmail.com', response.data)

    def test_login_without_registering(self):
        self.app.get('/login', follow_redirects=True)
        response = self.login('heronakumura@gmail.com', 'PleaseWork123')
        self.assertIn(b'ERROR! Incorrect login credentials.', response.data)

    def test_valid_logout(self):
        self.app.get('/register', follow_redirects=True)
        self.register('heronakumura@gmail.com', 'PleaseWork123', 'PleaseWork123')
        self.app.get('/login', follow_redirects=True)
        self.login('heronakumura@gmail.com', 'PleaseWork123')
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'Goodbye!', response.data)

if __name__ == "__main__":
    unittest.main()
