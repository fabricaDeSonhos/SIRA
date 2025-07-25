from src.config import *
from src.model.room import *
from src.model.user import *
from src.model.reservation import *

# Create the tables in the database
with app.app_context():
    db.create_all()

print("Database created")