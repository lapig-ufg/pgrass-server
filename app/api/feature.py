from typing import List, Tuple
from bson import ObjectId


from fastapi import APIRouter, HTTPException
from pydantic import Field

from app.db import MongoModel, db_features, PyObjectId
from app.model.models import Feature
from app.config import logger
router = APIRouter()


@router.get('/dataset/{dataset_id}', response_description="List all features db_dataset", response_model=List[Feature])
async def get_features(dataset_id):
    features = await db_features.find({'dataset_id':ObjectId(dataset_id)}).to_list(1000)
    return features


@router.get(
    "/{_id}", response_description="Get a single feature", response_model=Feature
)
async def get_feature(_id:str):
    if (feature := await db_features.find_one({"_id": ObjectId(_id)})) is not None:
        return feature
    raise HTTPException(status_code=404, detail=f"Feature {id} not found")

class Point(MongoModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    point_id: PyObjectId = Field(default_factory=PyObjectId)
    lat: float
    lon: float
    epsg: int


@router.get('/dataset/{dataset_id}/points', response_description="List point in features", response_model=List[Point])
async def get_features_point(dataset_id:str):
    if (points := await db_features.find({'dataset_id':ObjectId(dataset_id)},
                                         {'point_id':1,'lat':1,'lon':1,'epsg':1}).to_list(1000)) is not None:
        return points
    raise HTTPException(status_code=404, detail=f"Feature {id} not found")
