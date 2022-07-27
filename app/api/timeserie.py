from typing import Dict, List, Union
from bson import ObjectId

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

from app.db import db_timeseires
from app.model.models import CollectionsEnum, TimeSerie

router = APIRouter()






@router.get('/{point_id}', 
    response_description="List metadata TimeSeries by point_id", 
    response_model=Dict
    )
async def get_timeseires_by_point_id(point_id:str):
    collections = await db_timeseires.distinct('collection',{"point_id": ObjectId(point_id)})
    dict_metadata = {}
    for collection in collections:
        asset = await db_timeseires.distinct('asset',{
            "point_id": ObjectId(point_id) ,
            "collection":collection
            })
        dict_metadata[collection] = asset
    
    if len(dict_metadata) > 0:
        return dict_metadata
    raise HTTPException(status_code=404, detail=f"Timeseires point_id {point_id} not found")

class NGDatasets(BaseModel):
    label: str
    data: List[Union[int, float]]

class NGCharts(BaseModel):
    labels: List[datetime]
    datasets: List[NGDatasets]


@router.post(
    "/{point_id}/{collection}", 
    response_description="Get timeseires by point_id satellite band or index ", 
    response_model=NGCharts
)
async def get_timeseires_by_point_id_satellite_assets(
    point_id:str, 
    collection: CollectionsEnum, 
    assets: List[str]
    ):
    datasets = []
    labels_dates = []
    for asset in assets:
        if (timeseires := await db_timeseires.find({
            "point_id": ObjectId(point_id),
            "collection": collection,
            "asset":asset
            },{'value':1,'datetime':1,'_id':0}).sort('datetime').to_list(100000)) is not None:
            dates = []
            values = []
            for data in timeseires:
                dates.append(data['datetime'])
                values.append(data['value'])
            if len(labels_dates) == 0:
                labels_dates = dates
            elif labels_dates != dates:
                raise HTTPException(status_code=404, detail=f"Timeseires point_id:{point_id}, collection:{collection}, asset:{assets} not found")
            datasets.append(NGDatasets(label=asset,data=values))  
        else:
            raise HTTPException(status_code=404, detail=f"Timeseires point_id:{point_id}, collection:{collection}, asset:{assets} not found")
    return NGCharts(labels=labels_dates,datasets=datasets)