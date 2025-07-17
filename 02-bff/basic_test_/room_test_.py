from config import *
from service.room_service import *

# Example usage:
def basic_test_():

    # Create a new room
    room1 = create_room("Conference Room", True)
    room2 = create_room("Meeting Room", False)

    # Retrieve and print all rooms
    all_rooms = get_all_rooms()
    print(all_rooms)

    # Retrieve a specific room by ID
    print(get_room_by_id(room1.id))

    # delete the room
    print("removing rooms (expecting 2 'Trues')")
    print(delete_room(room1))
    print(delete_room(room2))

    # check if there are no rooms
    print("NO MORE ROOMS: ")
    all_rooms = get_all_rooms()
    print(all_rooms)

