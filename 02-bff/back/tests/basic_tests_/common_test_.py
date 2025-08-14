from src.config import *
from src.service.common_service import *

def generic_basic_test_(m_class, **kwargs):

    obj1 = create_object(m_class, **kwargs)
    
    # Retrieve and print all rooms
    all_objs = get_objects(m_class)
    print(all_objs)

    # Retrieve a specific object by ID
    print(get_object_by_id(m_class, obj1.id))

    # delete the room
    print("removing objects (expecting 1 'True')")
    print(soft_delete_object(obj1))

    # check if there are no rooms
    print("NO MORE OBJECTS: ")
    all_objs = get_objects(m_class)
    print(all_objs)
    
