#!/bin/bash

docker stop app
docker stop redis-server
docker stop worker
echo "All services stopped!"

docker rm app
docker rm redis-server
docker rm worker
echo "All services removed!"

docker ps -a