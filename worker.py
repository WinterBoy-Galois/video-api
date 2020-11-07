import os

import redis
from rq import Worker, Queue, Connection

# setup connection
listen = ['high', 'default', 'low']
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)

# start django framework
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "videopath.settings")

# start worker
if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()