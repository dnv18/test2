from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from api.views import api
app.register_blueprint(api)
from api.auth.views import auth_blueprint
app.register_blueprint(auth_blueprint)
