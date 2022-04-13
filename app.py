from flask_migrate import Migrate
from api import app, db, models
import unittest

migrate = Migrate(app, db)


def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


def create_db():
    """Creates the db tables."""
    db.create_all()


def drop_db():
    """Drops the db tables."""
    db.drop_all()


if __name__ == '__main__':
    app.run()

