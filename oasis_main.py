import json
import os
import redis
import time

print("Working")
redisURL = os.environ.get("REDIS_URL")
timestamp = time.strftime(" %H:%M:%S")
r = redis.from_url(redisURL)
print(timestamp)
timeindex = time.strftime("%H%M%S")
print(timeindex)
r.append("TestSuite"+ timeindex,"From Virtualenv local: 2016-09-21 " + timestamp)
print("Redis at " + redisURL + " returned :" + r.get("TestSuite"+ timeindex))
