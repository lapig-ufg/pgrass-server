from typing import List

from fastapi import APIRouter, HTTPException

from app.db import db_timeseires, PyObjectId
from app.model.functions import get_id_by_lon_lat
from app.model.models import TimeSerie

router = APIRouter()

@router.get('/', response_description="List all TimeSeries", response_model=List[TimeSerie])
async def get_timeseires():
    timeseires = await db_timeseires.find().to_list(1000)
    return timeseires


@router.get('/{lon}/{lat}', response_description="List TimeSeries by lon lat", response_model=List[TimeSerie])
async def get_timeseires_by_lon_lat(lon:float,lat:float):
    if (timeseires := await db_timeseires.find({"point_id": get_id_by_lon_lat(lon,lat)}).to_list(1000)) is not None:
        return timeseires
    raise HTTPException(status_code=404, detail=f"Timeseires Point({lon}, {lat}) not found")

@router.get('/{point_id}', response_description="List TimeSeries by point_id", response_model=List[TimeSerie])
async def get_timeseires_by_point_id(point_id:str):
    if (timeseires := await db_timeseires.find({"point_id": PyObjectId(point_id)}).to_list(1000)) is not None:
        return timeseires
    raise HTTPException(status_code=404, detail=f"Timeseires point_id {point_id} not found")