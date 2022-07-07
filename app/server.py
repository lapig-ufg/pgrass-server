from fastapi import FastAPI

from .routers import created_routes
from app.config import start_logger


start_logger()

app = FastAPI()
app = created_routes(app)



@app.get('/')
async def root():
    return {'message': 'Hello World'}


        
        

