#!/bin/bash

source .env
ssh -p 2522 -fN root@$SERVER -L 27018:127.0.0.1:27017
cd /APP/pgrass-server
gunicorn -k  uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080 --reload -w 4 -t 0 app.server:app
