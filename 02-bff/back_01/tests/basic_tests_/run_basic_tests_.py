from src.config import *
from common_test_ import *
from reservation_test_ import *
from src.model.room import *
from src.model.user import *

with app.app_context():
    
    # room test
    generic_basic_test_(Room, name="Sala 01")
    
    # user test
    generic_basic_test_(User, name="John deep", email="jode@gmail.com", password="123")
    
    # reservation test
    reservation_test_()
    
    