from flask import Flask
#from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
app = Flask(__name__)
cors = CORS(app) 
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

from app import routes, models
