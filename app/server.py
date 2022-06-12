from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import EmailStr
from .api import feature
from .api import timeserie

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

@app.post("/uploadfiles/")
async def create_upload_files(
    first_name:str, 
    last_name:str, 
    email:EmailStr, 
    institution:str,
    file: UploadFile = File(default=None)
):
    try:
        import geopandas as gpd
        gdf = gpd.read_file(file.file)
    except Exception as e:
        raise HTTPException(status_code=415, detail=str(e))
    return {
        "filenames": file.filename,
        "first_name":first_name, 
        "last_name":last_name, 
        "email":email, 
        "institution":institution,
        "columns":list(gdf.columns),
        "job_status":''
    }
