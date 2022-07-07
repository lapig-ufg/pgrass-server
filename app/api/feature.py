from typing import List, Tuple


from fastapi import APIRouter, HTTPException

from app.db import MongoModel, db_features, PyObjectId
from app.model.models import Feature
from app.config import logger
router = APIRouter()


@router.get('/dataset/{dataset_id}', response_description="List all features db_dataset", response_model=List[Feature])
async def get_features(dataset_id):
    features = await db_features.find({'dataset_id':PyObjectId(dataset_id)}).to_list(100)
    return features


@router.get(
    "/{_id}", response_description="Get a single feature", response_model=Feature
)
async def get_feature(_id:str):
    if (feature := await db_features.find_one({"_id": PyObjectId(_id)})) is not None:
        return feature
    raise HTTPException(status_code=404, detail=f"Feature {id} not found")

class Point(MongoModel):
    point_id:PyObjectId
    coordinate: Tuple[float,float]


@router.get('/points/', response_description="List point in features", response_model=List[Point])
async def get_features_point():
    points = []
    async for feature  in db_features.find():
        points.append(
            Point(
                point_id = PyObjectId(feature['point_id']), 
                coordinate = (feature['lon'],feature['lat'])
                )
            )
    logger.debug(points)
    return points