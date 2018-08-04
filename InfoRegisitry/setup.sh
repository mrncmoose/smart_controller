#!/bin/bash
pip install -r requirements.txt

# add docker container for PostGRE
docker run --name sqlalchemy-orm-psql \
    -e POSTGRES_PASSWORD=Mo%902ose \
    -e POSTGRES_USER=mooseGre \
    -e POSTGRES_DB=sqlalchemy \
    -p 5432:54320 \
    -d postgres