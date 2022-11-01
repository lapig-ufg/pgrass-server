#!/bin/bash

ssh -p 2522 -fN root@200.137.215.71 -L 27020:127.0.0.1:27017
cd /APP/pgrass-server
gunicorn -k  uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080 -w 4 -t 0 app.server:app
