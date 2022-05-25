from typing import List

from fastapi import APIRouter, HTTPException

from app.db import db_features, PyObjectId
from app.model.models import Feature

router = APIRouter()


@router.get('/', response_description="List all features", response_model=List[Feature])
async def get_features():
    features = await db_features.find().to_list(100)
    return features


@router.get(
    "/{id}", response_description="Get a single feature", response_model=Feature
)
async def get_feature(id:str):
    if (feature := await db_features.find_one({"_id": PyObjectId(id)})) is not None:
        return feature
    raise HTTPException(status_code=404, detail=f"Feature {id} not found")