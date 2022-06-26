from app.db import get_datetime_to_mongo, db_jobs
from app.model.functions import get_id
from fastapi import APIRouter, HTTPException

from json import loads

import pymongo
from app.functions import is_point, md5_for_file, read_file
from app.config import logger
from fastapi import File, UploadFile, HTTPException
from pydantic import EmailStr

router = APIRouter()

@router.post("/file", status_code=201)
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
    epsg = gdf.crs.to_epsg()
    features = loads(gdf.to_json())
    
    
    try:
        created_at = get_datetime_to_mongo()
        await db_jobs.insert_one({
            '_id':get_id(
                f'{md5_for_file(file.file)}{email}'
            )
            ,
            "file_name": file.filename,
            "first_name":first_name, 
            "last_name":last_name, 
            "email":email, 
            "institution":institution,
            "columns":list(gdf.columns),
            "features":features['features'],
            'epsg':epsg,
            "job_status":'IN_QUEUE',
            'created_at': created_at
        })
        return {
            "file_name": file.filename,
            "first_name":first_name, 
            "last_name":last_name, 
            "email":email, 
            "institution":institution,
            "columns":list(gdf.columns),
            'epsg':epsg,
            'created_at':created_at
        }
    except pymongo.errors.ServerSelectionTimeoutError as e:
        logger.error(f'Error in creating update file: {e}')
        raise HTTPException(status_code=521, detail=f'We had a problem with our server, please try later to upload the file.')
    except pymongo.errors.DuplicateKeyError as e:
        logger.error(f'File already exists in our base: {e}')
        raise HTTPException(status_code=409, detail=f'File already exists in our base.')
    except:
        logger.exception('Error in creating update file')
        raise HTTPException(status_code=500, detail="Error in server")