
import os,sys
currDir = os.path.dirname(os.path.realpath(__file__))
rootDir = os.path.abspath(os.path.join(currDir, '..'))
if rootDir not in sys.path: # add parent dir to paths
    sys.path.append(rootDir)

from src.config import *
from src.model.room import *
from src.model.user import *
from src.model.reservation import *

# Create the tables in the database
with app.app_context():
    db.create_all()

# create a default admin user if not exists
    if not User.query.filter_by(email='admin').first():
        hashed_password = User.gen_password("admin")
        admin_user = User(name='Admin', email='admin', password=hashed_password, admin=True)
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created with email 'admin' and password 'admin'")
    else:
        print("Admin user already exists")
print("Database created")
