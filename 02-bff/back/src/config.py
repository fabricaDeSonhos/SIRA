from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_cors import CORS

from uuid import uuid4, UUID

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Uuid

from datetime import datetime, date, time

from typing import List, Optional

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

import os
class Base(DeclarativeBase):
  pass

DATABASE_URL = ""

# persistency of classes were tested in 
# sqlite and mysql, in 17/07/2025
# default configuration: sqlite
SIRA_DB = "SQLITE"
#SIRA_DB = "MYSQL"

# Accessing an environment variable directly
try:
    db_env = os.environ['SIRA_DB']
    if db_env == "SQLITE":
      pass # already defined
    if db_env == "MYSQL":
      SIRA_DB = "MYSQL"
except KeyError:
    print("SIRA_DB environment variable is not set, considering default database: SQLITE.")

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

# create the app
app = Flask(__name__)
CORS(app)

# Configure the SQLAlchemy URI (using SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable unnecessary modification tracking

# JWT configuration
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # <-- Add this line


# initialize the app with the extension
db = SQLAlchemy(app)

''' references:
https://flask-sqlalchemy.readthedocs.io/en/stable/models/#defining-models

for the pytest: (didnt work yet)
$ pip install pytest-flask-sqlalchemy --break-system-packages
$ pip install pytest-flask --break-system-packages

'''

print("Configuration loaded successfully.")
