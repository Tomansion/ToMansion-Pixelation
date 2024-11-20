from utils.database_utils import (
    get_place as db_get_place,
    update_place as db_update_place,
    set_place as db_set_place,
)

from utils.socket_utils import connection_manager
from config.init_config import config


def generate_empty_place():
    WIDTH = config["PLACE"]["PLACE_WIDTH"]
    HEIGHT = config["PLACE"]["PLACE_HEIGHT"]
    empty_place = {"pixels": []}

    for y in range(WIDTH):
        row = []
        for x in range(HEIGHT):
            row.append({"username": "", "x": x, "y": y, "color": "#FFFFFF"})
        empty_place["pixels"].append(row)

    return empty_place


def get_place():
    # Get the place
    place = db_get_place()

    if place is None:
        empty_place = generate_empty_place()
        return db_set_place(empty_place)

    return place


async def place_pixel(pixel):
    place = db_get_place()

    if place is None:
        empty_place = generate_empty_place()
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
