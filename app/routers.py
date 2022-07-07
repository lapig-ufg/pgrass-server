from .api import feature
from .api import timeserie
from .api import upload
from .api import dataset

def created_routes(app):
    app.include_router(
        dataset.router, 
        prefix='/api/dataset', 
        tags=['Dataset']
        )


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
    return app