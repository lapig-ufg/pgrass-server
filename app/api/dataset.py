from datetime import datetime
from typing import List
from bson import ObjectId
from fastapi import APIRouter, HTTPException
from pydantic import EmailStr, Field


from app.db import PyObjectId, db_dataset, MongoModel
from app.config import logger
from app.errors import ErrorsRoute
from app.model.models import ListId

router = APIRouter(route_class=ErrorsRoute)


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



@router.get('/', response_description="List all Dataset", response_model=List[ListId])
async def get_datasets():
    try:
        dataset = await db_dataset.find({},{'_id'}).to_list(10000)
        return dataset
    except Exception as e:
        logger.exception(f'Error! {e}')
        raise HTTPException(status_code=500, detail=f"Server Error!")

        
@router.get('/{_id}', response_description="Dataset", response_model=Dataset)
async def get_dataset(_id):
    if (dataset := await db_dataset.find_one({"_id": ObjectId(_id)})) is not None:
        return dataset
    raise HTTPException(status_code=404, detail=f"Dataset {_id} not found")
   