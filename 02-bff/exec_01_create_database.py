from config import *
from model.room import *
from model.user import *

# Create the tables in the database
with app.app_context():
    db.create_all()

print("Database created")