
# 临时启动交互式启动服务

- flask服务
```shell
docker run --rm -p 5000:5000 --name debug_app app:latest gunicorn -b 0.0.0.0:5000 app:app

docker run -it --rm -p 5000:5000 --name debug_app --mount type=bind,source=/mnt/x/project/infra/app,target=/app app:latest bash
gunicorn -b 0.0.0.0:5000 app:app
```


- celery服务
```shell
docker run --rm --name debug_worker worker:latest celery -A tasks worker --loglevel=info

docker run -it --rm --name debug_worker --mount type=bind,source=/mnt/x/project/infra/worker,target=/worker worker:latest bash
celery -A tasks worker --loglevel=info
```


- 启动redis镜像
```shell
docker run -d --rm --name redis-server -p 6379:6379 redis:7-alpine
docker run -d --rm --name redis-server -p 6379:6379 redis:7 redis-server --bind 0.0.0.0 --protected-mode no
```

- 关闭并删除镜像
```shell
docker stop redis-server && docker rm redis-server
```

- 停止自启动redis
```shell
sudo systemctl disable redis-server
```


- 停止服务
```shell
sudo systemctl stop redis-server
```


