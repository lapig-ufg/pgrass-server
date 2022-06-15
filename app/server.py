

from json import loads

import pymongo
from app.functions import is_point, read_file
from .config import logger
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import EmailStr
from .api import feature
from .api import timeserie
from app.db import get_datetime_to_mongo, db_jobs
from shapely.geometry.point import Point



app = FastAPI()


app.include_router(
    feature.router, 
    prefix='/api/features', 
    tags=['Feature']
    )

app.include_router(
    timeserie.router, 
    prefix='/api/timeserie', 
    tags=['TimeSerie']
    )

@app.get('/')
async def root():
    return {'message': 'Hello World'}

@app.post("/uploadfiles/", status_code=201)
async def create_upload_files(
    first_name:str, 
    last_name:str, 
    email:EmailStr, 
    institution:str,
    file: UploadFile = File(default=None)
):
    try:
        gdf = read_file(file)
    except Exception as e:
        logger.exception(f'type: {file.content_type}, {file.filename}')
        raise HTTPException(status_code=415, detail=f'{e}')
    
    if not all(gdf.geometry.apply(is_point)):
        raise HTTPException(status_code=406, detail='We only accept Point format geometry, there is one or more geometry that is not Point')
    crs = gdf.crs.to_epsg()
    features = loads(gdf.to_json())
    
    
    try:
        created_at = get_datetime_to_mongo()
        await db_jobs.insert_one({
            "filenames": file.filename,
            "first_name":first_name, 
            "last_name":last_name, 
            "email":email, 
            "institution":institution,
            "columns":list(gdf.columns),
            "features":features['features'],
            'crs':crs,
            "job_status":'IN_QUEUE',
            'created_at': created_at
        })
        return {
            "filenames": file.filename,
            "first_name":first_name, 
            "last_name":last_name, 
            "email":email, 
            "institution":institution,
            "columns":list(gdf.columns),
            'crs':crs,
            'created_at':created_at
        }
    except pymongo.errors.ServerSelectionTimeoutError as e:
        logger.error(f'Error in creating update file: {e}')
        raise HTTPException(status_code=521, detail=f'We had a problem with our server, please try later to upload the file.')
    except:
        logger.exception('Error in creating update file')
        raise HTTPException(status_code=500, detail="Error in server")
        
        


