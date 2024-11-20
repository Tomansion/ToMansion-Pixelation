from services.place_services import get_place, place_pixel


from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List

router = APIRouter()


class Pixel(BaseModel):
    username: str = Field(...)
    x: int = Field(..., ge=0)
    y: int = Field(..., ge=0)
    color: str = Field(..., pattern=r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")


class PlaceGrid(BaseModel):
    pixels: List[List[Pixel]]


#############################################################################
# Place API
#############################################################################


@router.get("/place", response_model=PlaceGrid, tags=["Place"])
def get_place_route():
    return get_place()


@router.post("/place", tags=["Place"])
async def place_place_pixel(pixel: Pixel):
    await place_pixel(pixel)
