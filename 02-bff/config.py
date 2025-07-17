''' references:

https://flask-sqlalchemy.readthedocs.io/en/stable/models/#defining-models

for the pytest: (didnt work yet)
$ pip install pytest-flask-sqlalchemy --break-system-packages
$ pip install pytest-flask --break-system-packages


'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from uuid import uuid4, UUID

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Uuid

class Base(DeclarativeBase):
  pass

DATABASE_URL = ""

# TODO: get database definition from environment variable
# persistency of classes were tested in 
# sqlite and mysql, in 17/07/2025
SIRA_DB = "SQLITE"
#SIRA_DB = "MYSQL"

if SIRA_DB == "SQLITE":
    # some commands to make the database be created
    # at this folder
    import os
    this_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(this_path, 'sira.db')
    DATABASE_URL = f"sqlite:///{file_path}"

elif SIRA_DB == "MYSQL":
    # mysql connection
    DATABASE_URL = "mysql+pymysql://sira:minhasenha@localhost/sira"

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)

# Configure the SQLAlchemy URI (using SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable unnecessary modification tracking

# initialize the app with the extension
db.init_app(app)
