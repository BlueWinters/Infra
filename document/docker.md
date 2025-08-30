# Docker

## 安装
- 镜像源加速
```yaml
{
    "registry-mirrors" : [
      "https://docker.registry.cyou",
      "https://docker-cf.registry.cyou",
      "https://dockercf.jsdelivr.fyi",
      "https://docker.jsdelivr.fyi",
      "https://dockertest.jsdelivr.fyi",
      "https://mirror.aliyuncs.com",
      "https://dockerproxy.com",
      "https://mirror.baidubce.com",
      "https://docker.m.daocloud.io",
      "https://docker.nju.edu.cn",
      "https://docker.mirrors.sjtug.sjtu.edu.cn",
      "https://docker.mirrors.ustc.edu.cn",
      "https://mirror.iscas.ac.cn",
      "https://docker.rainbond.cc"
  ]
}
```


## 运行
- 停止所有容器
```shell
docker stop $(docker ps -aq)
```

- 删除所有的容器
```shell
docker rm $(docker ps -aq)
```

- 删除所有的镜像
```shell
docker rmi $(docker images -q)
```