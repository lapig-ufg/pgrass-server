from fastapi import FastAPI
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
