import redis
import json


class RedisPipeline(object):
    def __init__(self):
        self.db = redis.StrictRedis(host='localhost', port=6379, db=0)

    def save_data(self, item):
        self.db.lpush("detail", json.dumps(item))

