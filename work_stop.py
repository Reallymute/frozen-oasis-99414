import os
import redis
import time
import sys
from datetime import date
from __builtin__ import str, format


print("Work Stop Dyno : Working")
sys.stdout.flush()
time.sleep(0.3)

redisURL = os.environ.get("REDIS_URL")
redischannel = 'marc-channel'
timestamp = time.strftime(" %H:%M:%S")
datey = date.today()
r = redis.from_url(redisURL)
rtt  = r.delete("STOP_HEROKU_WORKER")

r.setex("STOP_HEROKU_WORKER","True",90)

time.sleep(5)
print "Work Stop Dyno Terminated ; Worker Termination imminent: Redis key inserted :STOP_HEROKU_WORKER with 90 second TTL : Count of deleted: " + format(rtt,"000")
