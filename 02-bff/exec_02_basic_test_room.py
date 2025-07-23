from config import *
from basic_test_.common_test_ import *
from model.room import *

with app.app_context():
    
    # room test
    generic_basic_test_(Room, name="Sala 01")
    
    # user test
    generic_basic_test_(User, name="John deep", email="jode@gmail.com", password="123")
    
    