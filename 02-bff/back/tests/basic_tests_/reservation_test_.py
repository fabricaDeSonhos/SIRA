from src.config import *
from src.service.common_service import *
from src.service.reservation_service import *
       
# Example usage:
def reservation_test_():

    # Create a new object
    room = create_object(Room, name="Lab A04")
    user = create_object(User, name="John Silva", 
                         email="jo@gmail.com", password="123")
    res = create_reservation(room, user, purpose="Matemática 201 info")   

    # Retrieve and print all objects
    all = get_reservations()
    print(all)

    # Retrieve a specific object by ID
    print(get_object_by_id(Reservation, res.id))

    # delete 
    print("removing object (expecting 1 'True')")
    print(soft_delete_reservation_by_id(user, res.id))
    
    # check if there are no rooms
    print("NO MORE objects: ")
    all = get_reservations()
    print(all)