#!/bin/bash

# 启动Redis
docker run -d --rm --name redis-server -p 6379:6379 redis:7 redis-server --bind 0.0.0.0

# 启动Flask
docker run -d --rm --name app -p 5000:5000 app:latest

# 启动Celery-Worker
docker run -d --rm --name worker worker:latest

echo "All services started!"