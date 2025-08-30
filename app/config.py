
import os

"""
查看容器实际IP
docker inspect redis-server | grep IPAddress
"""

REDIS_HOST = os.getenv('REDIS_HOST', '172.18.0.2')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

