from fastapi import APIRouter, HTTPException

from app.db import PyObjectId, db_dataset

router = APIRouter()


@router.get('/', response_description="List all Dataset")
async def get_datasets():
    dataset = await db_dataset.find().to_list(100)
    return dataset

@router.get('/{_id}', response_description="Dataset")
async def get_dataset(_id):
    if (dataset := await db_dataset.find_one({"_id": PyObjectId(_id)})) is not None:
        return dataset
    raise HTTPException(status_code=404, detail=f"Dataset {_id} not found")
