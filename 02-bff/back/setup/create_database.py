from src.config import *
from src.model.room import *
from src.model.user import *
from src.model.reservation import *

# Create the tables in the database
with app.app_context():
    db.create_all()

# create a default admin user if not exists
    if not User.query.filter_by(email='admin').first():
        admin_user = User(name='Admin', email='admin', password='admin', admin=True)
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created with email 'admin' and password 'admin'")
    else:
        print("Admin user already exists")
print("Database created")