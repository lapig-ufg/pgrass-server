from datetime import datetime
from typing import List
from bson import ObjectId
from fastapi import APIRouter, HTTPException
from pydantic import EmailStr, Field


from app.db import PyObjectId, db_dataset, MongoModel, db_features
from app.config import logger
router = APIRouter()


class Dataset(MongoModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    file_name: str
    first_name: str
    last_name: str
    email: EmailStr
    institution: str
    columns: List[str]
    epsg: int
    created_at: datetime


@router.get('/', response_description="List all Dataset", response_model=List[Dataset])
async def get_datasets():
    try:
        dataset = await db_dataset.find().to_list(100)
        return dataset
    except Exception as e:
        logger.exception(f'Error! {e}')
        raise HTTPException(status_code=5000, detail=f"Server Error!")

        

@router.get('/{_id}', response_description="Dataset", response_model=Dataset)
async def get_dataset(_id):
    if (dataset := await db_dataset.find_one({"_id": ObjectId(_id)})) is not None:
        return dataset
    raise HTTPException(status_code=404, detail=f"Dataset {_id} not found")
