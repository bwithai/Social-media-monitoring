# Social Media Monitoring


```tree
.
├── server
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
```
### MongoDB
```bash
sudo docker pull mongo
sudo docker run --name mongodb -d -p 27017:27017 -v ~/mongo-data:/data/db mongo
# Verify that MongoDB is running
sudo docker ps
# to stop
sudo docker stop mongodb
# varify stop
sudo docker ps -a --filter "status=exited"
# again start
sudo docker start mongodb
```
### RabbitMQ
```bash
# pull
sudo docker pull rabbitmq:3-management 
# start
sudo docker run -d --rm --name rabbitmq -p 15672:15672 -p 5672:5672 rabbitmq:3-management
# stop
sudo docker stop rabbitmq
```