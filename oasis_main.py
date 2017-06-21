import json
import os
import redis
import time
from datetime import date
import billiard
import qrcode 
import base64
import io
import random
from __builtin__ import str, format


print("Working")
randyu = random.randint(1,16000000)
randt = random.randint(10,99999)
messageindexstorage = "To_FromTable"
messagelistlevel1 = ":indexes"
separatorDatePrefix = "/"
separatorSuffix = "|"
MessageTTL = 89
if randyu > 8000000:
    dest = "PNGReader"
else:
    dest = "JPGReader"
authtoken = base64.b64encode(str(randyu))
testcommand = "QR_ENCODE;Merchant,ID=79723683746862387464" \
     +separatorSuffix+"AUTHTOKEN;Token="+ authtoken.format("000000000000")

#strr = io.open("tinn.png",'a+b')
#judd = base64.encodestring("test")
#jaff = base64.decodestring(testbase64data)
#if strr.writable:
#    strr.write(jaff)
#    strr.flush() 
redisURL = os.environ.get("REDIS_URL")
redischannel = 'marc-channel'
timestamp = time.strftime(" %H:%M:%S")
datey = date.today()
r = redis.from_url(redisURL)
print(timestamp)
timeindex = time.strftime("%H%M%S")+separatorSuffix + format(randt,"000000")
print(timeindex)
#r.linsert('currentKeys',1,'T',('TestSuite' + timeindex))
r.publish(redischannel,'Wonderousthings' + timeindex)
r.setex("MessageIndex"+ timeindex +"FormattedDate","From Virtualenv local: "+ datey.isoformat() + "T" + timestamp + separatorSuffix + format(randt,"000000"),90)
r.setex("MessageIndex"+ timeindex + "ResultDataPayload","default",90)
r.setex("MessageIndex"+ timeindex + "AuthToken",authtoken,90)
r.setex("MessageIndex"+ timeindex + "Command",testcommand,90)
r.setex("MessageIndex"+ timeindex + "Status","PENDING",90)
r.hmset(messageindexstorage + messagelistlevel1 + ":"+timeindex, {'index':  timeindex,'TTL': MessageTTL,'StartLife': datey.isoformat() + 'T' + timestamp})
r.sadd(messageindexstorage + messagelistlevel1, datey.isoformat()+separatorDatePrefix+timeindex)
#r.hset("To_FromTable","To: "+ dest , "Index: "+ timeindex + format(randt,"000000")
#r.hset("To_FromTable","To: "+ dest )

#r.move("TestSuite"+ timeindex,"db1")


#p = r.pubsub()
#publishDict = p.get_message().copy()
##publishDict = {'data':555,'channel':'default'}
#p.subscribe(redischannel)

#PublishDataInitID = format(publishDict.get('data'),"000000")
#PublishChannelName = publishDict.get('channel')
#print("Subscription to " + PublishChannelName + " returned :" + PublishDataInitID + " put here")
#p.close()

