from utils.database_utils import (
    get_place as db_get_place,
    update_place as db_update_place,
    set_place as db_set_place,
)

from utils.socket_utils import connection_manager


WIDTH = 30
HEIGHT = 30
empty_place = {"pixels": []}

for y in range(HEIGHT):
    row = []
    for x in range(WIDTH):
        row.append({"username": "", "x": x, "y": y, "color": "#FFFFFF"})
    empty_place["pixels"].append(row)


def get_place():
    # Get the place
    place = db_get_place()

    if place is None:
        return db_set_place(empty_place)

    return place


async def place_pixel(pixel):
    place = db_get_place()

    if place is None:
        place = db_set_place(empty_place)

    # Replace the pixel
    place["pixels"][pixel.x][pixel.y]["username"] = pixel.username
    place["pixels"][pixel.x][pixel.y]["color"] = pixel.color

    # Update the place
    db_update_place(place)

    # Broadcast socket event
    print("Broadcasting new pixel")
    await connection_manager.broadcast(
        {
            "newPixelUpdate": {
                "x": pixel.x,
                "y": pixel.y,
                "color": pixel.color,
                "username": pixel.username,
            }
        }
    )
