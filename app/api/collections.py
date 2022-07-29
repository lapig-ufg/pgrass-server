from typing import Dict, List
from fastapi import APIRouter, HTTPException


from app.db import db_collections

router = APIRouter()

@router.get('/', response_description="List collections _id ", response_model=List[Dict])
async def get_collections():
    if (collections := await db_collections.find({},{'_id':1}).to_list(1000)) is not None:
        return collections
    raise HTTPException(status_code=404, detail=f"Base error")


@router.get('/{collections_id}', response_description="Get collections by _id ", response_model=Dict)
async def get_collection(collections_id):
    if (collection := await db_collections.find_one({'_id':collections_id})) is not None:
        return collection
    raise HTTPException(status_code=404, detail=f"Base error")