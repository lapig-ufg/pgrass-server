from bson import ObjectId
from fastapi import APIRouter, HTTPException

from app.db import db_dataset

router = APIRouter()


@router.get('/', response_description="List all Dataset")
async def get_features():
    dataset = await db_dataset.find().to_list(100)
    return dataset

@router.get('/{_id}', response_description="Dataset")
async def get_features(_id):
    dataset = await db_dataset.find({'_id': ObjectId(_id)}).to_list(100)
    return dataset