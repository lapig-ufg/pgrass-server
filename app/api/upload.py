from datetime import datetime

from app.db import get_datetime_to_mongo, db_dataset
from app.model.auth import User
from app.model.functions import get_id
from fastapi import APIRouter, HTTPException, File, UploadFile, Depends

from json import loads

import pymongo
from app.functions import id_to_gid, is_point, read_file
from app.config import logger
from app.db import db_features

from pydantic import EmailStr

from app.utils.auth import get_current_active_user

router = APIRouter()


@router.post("/file", status_code=201)
async def create_upload_files(
    public: bool = False,
    file: UploadFile = File(default=None),
    current_user: User = Depends(get_current_active_user)
):
    filename = file.filename
    file_content_type = file.content_type
    
    try:
        gdf = read_file(file)
    except Exception as e:
        logger.exception(f'type: {file_content_type}, {filename}')
        raise HTTPException(status_code=415, detail=f'{e}')
    
    logger.debug('validando gemetria')
    #TODO limintar a quantidade de features?
    #if len(gdf) > 10000:
    #    raise HTTPException()
    if not all(gdf.geometry.apply(is_point)):
        raise HTTPException(status_code=406, detail='We only accept Point format geometry, there is one or more geometry that is not Point')
    epsg = gdf.crs.to_epsg()
    features = loads(gdf.to_json())
    
    
    try:
        created_at = get_datetime_to_mongo()
        hash_file = get_id(str(datetime.now()))
        #hash_file = get_id(
        #        f'{md5_for_file(file_binary)}{email}'
        #    )
        logger.debug(f'email: {current_user.username} obid: {hash_file} ')
        columns = [name for name in gdf.columns if not name == 'geometry']
        await db_dataset.insert_one({
            '_id':hash_file,
            "file_name": filename,
            "username":current_user.username, 
            "columns":columns,
            'epsg':epsg,
            'created_at': created_at
        })
        meta_data = {
            'epsg':epsg,
            'dataset_id':hash_file,
        }

        features_to_db = [
            {   '_id':get_id(f'{hash_file}{feature["id"]}'),
                **meta_data, 
                **id_to_gid(feature,get_id(f'{hash_file}{feature["id"]}'))
            } for feature in features['features']]
        await db_features.insert_many(features_to_db)

        return {
            "file_name": filename,
            "username":current_user.username, 
            "public":public,
            "columns":columns,
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