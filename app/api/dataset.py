from datetime import datetime
from typing import List
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends
from pydantic import Field


from app.db import PyObjectId, db_dataset, MongoModel
from app.config import logger
from app.errors import ErrorsRoute
from app.model.auth import User
from app.model.models import ListId
from app.utils.auth import get_current_active_user, have_permission_access_dataset, secure_query_dataset


router = APIRouter(route_class=ErrorsRoute)


class Dataset(MongoModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    file_name: str
    username: str
    public: bool
    columns: List[str]
    epsg: int
    created_at: datetime



@router.get('/', response_description="List all Dataset", response_model=List[ListId])
async def get_datasets(current_user: User = Depends(get_current_active_user)):
    try:
        dataset = await db_dataset.find({ **secure_query_dataset(current_user) },{'_id'}).to_list(10000)
        return dataset
    except Exception as e:
        logger.exception(f'Error! {e}')
        raise HTTPException(status_code=500, detail=f"Server Error!")

        
@router.get('/{_id}', response_description="Dataset", response_model=Dataset)
async def get_dataset(_id,current_user: User = Depends(get_current_active_user)):
    await have_permission_access_dataset(current_user)
    if (dataset := await db_dataset.find_one({"_id": ObjectId(_id)})) is not None:
        return dataset
    raise HTTPException(status_code=404, detail=f"Dataset {_id} not found")
   