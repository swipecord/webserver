## Main swipecord server
Server written in FastAPI, use MySQL database and sqlalchemy orm.

# Installation

```
git clone https://github.com/swipecord/webserver
cd webserver
docker-compose build
sudo docker-compose up
```

After that, the server will be available on localhost:8000.
It will also generate a documentation page at localhost:8000/docs and localhost:8000/redoc
