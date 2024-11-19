place_db = None


def setup(place_collection_name=None):
    pass


# Place functions
def get_place():
    return place_db


def update_place(new_place):
    global place_db
    place_db = new_place


def set_place(new_place):
    global place_db
    place_db = new_place
    return place_db
