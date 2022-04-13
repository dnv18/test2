import unittest

from api import db
from api.models import User
from tests.base import BaseTestCase


class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):
        user = User(
            email='test@test.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, str))
        db.session.query(User).filter(User.email == 'test@test.com').delete()
        db.session.commit()

    def test_decode_auth_token(self):
        user = User(
            email='test@test.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, str))
        self.assertTrue(User.decode_auth_token(
            auth_token) != 1)
        db.session.query(User).filter(User.email == 'test@test.com').delete()
        db.session.commit()


if __name__ == '__main__':
    unittest.main()
