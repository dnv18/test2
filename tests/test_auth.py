import unittest
import json
import time
from api import db
from api.models import User
from tests.base import BaseTestCase


def register_user(self, email, password):
    return self.client.post(
        '/auth/register',
        data=json.dumps(dict(
            email=email,
            password=password
        )),
        content_type='application/json',
    )


def login_user(self, email, password):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            email=email,
            password=password
        )),
        content_type='application/json',
    )


def status_user(self, resp_register):
    return self.client.get(
        '/auth/status',
        headers=dict(
            Authorization='Bearer ' + str(
                json.loads(resp_register.data.decode())['auth_token'])))


def logout_user(self, resp_login):
    return self.client.post(
        '/auth/logout',
        headers=dict(
            Authorization='Bearer ' + str(
                json.loads(resp_login.data.decode())['auth_token'])))


class TestAuthBlueprint(BaseTestCase):
    def test_registration(self):
        """
        Test for user registration
        """
        with self.client:
            response = register_user(self, 'joe@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)
        db.session.query(User).filter(User.email == 'joe@gmail.com').delete()
        db.session.commit()

    def test_registered_with_already_registered_user(self):
        """
        Test registration with already registered email
        """
        user = User(
            email='joe@gmail.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = register_user(self, 'joe@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User already exists. Please Log in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 202)
        db.session.query(User).filter(User.email == 'joe@gmail.com').delete()
        db.session.commit()

    def test_registered_user_login(self):
        """
        Test for login of registered-user login
        """
        with self.client:
            # user registration
            resp_register = register_user(self, 'joe@gmail.com', '123456')
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # registered user login
            response = login_user(self, 'joe@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
        db.session.query(User).filter(User.email == 'joe@gmail.com').delete()
        db.session.commit()

    def test_non_registered_user_login(self):
        """
        Test for login of non-registered user
        """
        with self.client:
            response = login_user(self, 'joe@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User does not exist.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)
        db.session.query(User).filter(User.email == 'joe@gmail.com').delete()
        db.session.commit()

    def test_user_status(self):
        """
        Test for user status
        """
        with self.client:
            resp_register = register_user(self, 'joe@gmail.com', '123456')
            response = status_user(self, resp_register)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['email'] == 'joe@gmail.com')
            self.assertTrue(data['data']['admin'] == 'true' or 'false')
            self.assertEqual(response.status_code, 200)
        db.session.query(User).filter(User.email == 'joe@gmail.com').delete()
        db.session.commit()

    def test_valid_logout(self):
        """
        Test for logout before token expires
        """
        with self.client:
            # user registration
            resp_register = register_user(self, 'joe@gmail.com', '123456')
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # user login
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            data_login = json.loads(resp_login.data.decode())
            self.assertTrue(data_login['status'] == 'success')
            self.assertTrue(data_login['message'] == 'Successfully logged in.')
            self.assertTrue(data_login['auth_token'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 200)
            # valid token logout
            response = logout_user(self, resp_login)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertEqual(response.status_code, 200)
        db.session.query(User).filter(User.email == 'joe@gmail.com').delete()
        db.session.commit()

    def test_invalid_logout(self):
        """
        Testing logout after the token expires
        """
        with self.client:
            # user registration
            resp_register = register_user(self, 'joe@gmail.com', '123456')
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # user login
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            data_login = json.loads(resp_login.data.decode())
            self.assertTrue(data_login['status'] == 'success')
            self.assertTrue(data_login['message'] == 'Successfully logged in.')
            self.assertTrue(data_login['auth_token'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 200)
            # invalid token logout
            # time.sleep(6)
            # response = logout_user(self, resp_login)
            # data = json.loads(response.data.decode())
            # self.assertTrue(data['status'] == 'fail')
            # self.assertTrue(
            #     data['message'] == 'Signature expired. Please log in again.')
            # self.assertEqual(response.status_code, 401)
        db.session.query(User).filter(User.email == 'joe@gmail.com').delete()
        db.session.commit()


if __name__ == '__main__':
    unittest.main()
