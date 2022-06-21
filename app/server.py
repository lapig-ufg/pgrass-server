from fastapi import FastAPI

from .api import feature
from .api import timeserie
from .api import upload




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

app.include_router(
    upload.router, 
    prefix='/api/upload', 
    tags=['Upload Files']
    )

@app.get('/')
async def root():
    return {'message': 'Hello World'}


        
        


