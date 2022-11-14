from .api import feature
from .api import timeserie
from .api import upload
from .api import dataset
from .api import collections
from .api import auth
from .api import user
from app.utils.auth import get_current_user
from fastapi import Depends

def created_routes(app):
    
    app.include_router(
        auth.router, 
        prefix='/api/auth',
        tags=['Auth']
        )

    app.include_router(
        collections.router, 
        prefix='/api/collections', 
        dependencies=[Depends(get_current_user)],
        tags=['Collections']

        )


    app.include_router(
        dataset.router, 
        prefix='/api/dataset',
        dependencies=[Depends(get_current_user)],
        tags=['Dataset']
        )


    app.include_router(
        feature.router, 
        prefix='/api/features', 
        dependencies=[Depends(get_current_user)],
        tags=['Feature']
        )

    app.include_router(
        timeserie.router, 
        prefix='/api/timeserie', 
        dependencies=[Depends(get_current_user)],
        tags=['TimeSerie']
        )

    app.include_router(
        upload.router, 
        prefix='/api/upload', 
        dependencies=[Depends(get_current_user)],
        tags=['Upload Files']
        )

    app.include_router(
        user.router,
        prefix='/auth/user',
        dependencies=[Depends(get_current_user)],
        tags=['user']

    )
    return app