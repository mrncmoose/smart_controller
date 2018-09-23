#pip3 install -r requirements.txt

# add docker container for PostGRE
docker run --name amort_pro_db \
    -e POSTGRES_PASSWORD=Mo%902ose \
    -e POSTGRES_USER=mooseGre \
    -e POSTGRES_DB=amort \
    -p 54321:5432 \
    -d postgres

# docker container for M$ SQL server
# TODO:  specify the DB name
#docker run --name amort_sql_server_db \
#	-p 14331:1433 \
#	-e "ACCEPT_EULA=Y" \
#	-e "SA_PASSWORD=Mo_902ose" \
#	-e "MSSQL_PID=Developer" \
#	-d microsoft/mssql-server-linux:latest
    
 docker build -f Dockerfile -t amort-pro/web-app .
# docker-compose up --build -d

# start the web app
#docker start amort_pro_db `
#docker start amort-pro/web-app

# stop instance
#docker stop amort_pro_db

# destroy instance
#docker rm informationRegistry_dbamort_pro_db