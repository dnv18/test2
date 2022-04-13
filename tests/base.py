from flask_testing import TestCase

from api import app, db


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        db.session.commit()

    def tearDown(self):
        db.session.remove()
