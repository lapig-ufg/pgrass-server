#!/bin/bash
FOLDER=~/.ssh
if [ -f "poetry.lock" ]; then
    rm poetry.lock
fi

if [ -f "pyproject.toml" ]; then
    rm pyproject.toml
fi
if [ -d "$FOLDER" ]; then
    cp -rvp ~/.ssh ssh/
else
    echo "Directory ./ssh does not exist!"
fi
cp -rvp ../poetry.lock .

cp -rvp ../pyproject.toml .

docker-compose build 

docker-compose up -d 