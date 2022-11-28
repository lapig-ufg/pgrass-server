from datetime import datetime
from typing import List, Dict, Optional
from bson import ObjectId
from bson.json_util import dumps
from fastapi import APIRouter, HTTPException, Depends
from pydantic import Field

from app.db import PyObjectId, db_dataset, db_features, MongoModel
from app.config import logger
from app.errors import ErrorsRoute
from app.model.auth import User
from app.model.models import Feature
from app.utils.auth import get_current_active_user, have_permission_access_dataset, secure_query_dataset

router = APIRouter(route_class=ErrorsRoute)


class Dataset(MongoModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    file_name: str
    username: str
    public: bool = False
    columns: List[str]
    epsg: int
    created_at: datetime

class DatasetFeatures(Dataset):
    features: Optional[List[Feature]] | None = None


@router.get('/', response_description="List all Dataset", response_model=List[Dataset])
async def get_datasets(current_user: User = Depends(get_current_active_user)):
    try:
        dataset = await db_dataset.find({**secure_query_dataset(current_user.username)}).to_list(10000)
        return dataset
    except Exception as e:
        logger.exception(f'Error! {e}')
        raise HTTPException(status_code=500, detail=f"Server Error!")


@router.get('/get/{_id}', response_description="Dataset", response_model=Dataset)
async def get_dataset(_id, current_user: User = Depends(get_current_active_user)):
    await have_permission_access_dataset(_id, current_user.username)
    if (dataset := await db_dataset.find_one({"_id": ObjectId(_id)})) is not None:
        return dataset
    raise HTTPException(status_code=404, detail=f"Dataset {_id} not found")


@router.get('/count-features/{dataset_id}', response_description="Count features of dataset-item", response_model=int)
async def count_features(dataset_id: str, current_user: User = Depends(get_current_active_user)):
    await have_permission_access_dataset(dataset_id, current_user.username)
    count = await db_features.count_documents({"dataset_id": ObjectId(dataset_id)})
    if count is not None:
        return count
    raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} not found")


@router.get('/features', summary="Get all collections of features by user", response_model=List[DatasetFeatures])
async def get_features(current_user: User = Depends(get_current_active_user)):
    try:
        aggregation_query = [
            {"$match": {**secure_query_dataset(current_user.username)}},
            {
                "$lookup": {
                    "from": "features",
                    "localField": "_id",
                    "foreignField": "dataset_id",
                    "as": "features",
                }
            }
        ]
        rows = []
        async for doc in db_dataset.aggregate(aggregation_query):
            try:
                rows.append(DatasetFeatures.from_mongo(doc))
            except Exception as e:
                logger.debug(doc)
                # logger.exception(e)

        if len(rows) > 0:
            # logger.debug(rows[1])
            return rows
        raise HTTPException(status_code=404, detail=f"Collections not found")
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, f'{e}')
