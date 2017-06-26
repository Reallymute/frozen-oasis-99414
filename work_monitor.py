import json
import os
import redis
import time
import sys
from datetime import date
import billiard
import qrcode
import image
from PIL import Image
import base64
import binascii
import io
import random
from __builtin__ import str, format
import cStringIO
from _io import BytesIO


print("Working")
sys.stdout.flush()
time.sleep(0.3)


randyu = random.randint(1,16000000)
randt = random.randint(10,99999)
messageindexstorage = "To_FromTable"
messagelistlevel1 = ":indexes"
separatorDatePrefix = "/"
separatorSuffix = "|"
MessageTTL = 89
testbase64data = "iVBORw0KGgoAAAANSUhEUgAAAB0AAAAdCAIAAADZ8fBYAA \
AA60lEQVRIidWWwQ7EIAhElez/fzLZQ1MzHQYkTTyU08bV4Tkg6XT3cSDshOgHdX \
+PJCbSXAUwM3e/NqwfcqfQpf8o0xLd7hzSB7tDKtI67ax0YyBasy+7dbs8zZyNwf \
4WRHG9YGddbdZNikI1+Oz4Re3VOTIlQuFjVKd7aF5JFH2QnmzeRdaSqBh7ec+LJt \
D5gpd1JC8RZW2AN9u/Y5wApI5GI2OsW3eeUTBdOMh9VtuNyepebs2zAZ5EZ8bT6F \
Q3BtHJ8bbpBxkLCkkRNnqlC7VunXERfixMa54NKGn2Imi9Nc9exNe+H07p/gHwUP \
wkuJszgwAAAABJRU5ErkJggg=="
testbase64data = "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"
testbase64data = "iVBORw0KGgoAAAANSUhEUgAAAB0AAAAdCAYAAABWk2cPAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAEdSURBVEhL5ZbtrsIwDEPH3v+ZB1jiICuLOyhif3akKGma2q3gfty2bbsvJ7O+8qlcx3T3ma5rvsdz9r2vWmjt/Q5moZ3UUA3wulLPpNl4Pd2ccI5els45eecAjNNrRkyZ8pIZQxFNJUg4qQ9H+2Lq25tyQvvO1K9BDKrYp+yuJ0EPoFauZnWOYF3Zd55IFGEEtCY73uv2O1pTUQVGgtpTUGtOQa8STYULIJKE6hxoXdkp+CGvlasoPYe9Ee0E4tSe3YgM3SU6vv45BTfgjNZ+Pl1g+FIPB0NlNxF1tiM+C8EqCvS7S7FO56NpojNTrxqxJjtfmwoJId7BfmcooqkOEBU3Q7zrUVd++h/Ja+FmI6b+yvxKftYfuYrpsjwA2Zk40H5eeVkAAAAASUVORK5CYII="

redisURL = os.environ.get("REDIS_URL")
redischannel = 'marc-channel'
timestamp = time.strftime(" %H:%M:%S")
datey = date.today()
r = redis.from_url(redisURL)

while (not r.exists("STOP_HEROKU_WORKER")):
    time.sleep(2)
    #listofmessageindexs = r.hgetall(messageindexstorage+ messagelistlevel1 + ":"+timeindex)

    #for j in ["PNGReader","JPGReader"]:
    #    if r.exists:
    #        #listofmessageindexs = r.hgetall("To_FromTable")
    #        pass
    #    else :
    #        pass
    #fdee = ""
    #xerrt = ""
    #for pl in listofmessageindexs:
    #    if (pl.format("") == "index"):
    #        iggdd = r.hget(messageindexstorage+ messagelistlevel1 + ":"+timeindex,pl.format("")).format("")
    #        xfzzfz = r.get("MessageIndex"+iggdd.format("") + "Command",)
    #        print ("MessageIndex"+iggdd.format("") + "Command")
    #        print(xfzzfz)
    #    print("Redis at " + redisURL + " returned :" + pl.format("")  +  " with value of " + r.hget(messageindexstorage+ messagelistlevel1 + ":"+timeindex,pl.format("")).format("") )
    ##print("Message Payload is : " + r.hget(messageindexstorage,xerrt.format("")))
    #        #+ format(pl,"0")
    ouuz = r.smembers(messageindexstorage+ messagelistlevel1)
    tizz = "default"    
    #print ouuz
    #ouuz.sort()
    #print ouuz
    arruu = ["0"]
    kurre = ["0"]
    for indggg in ouuz:
        if (indggg.find(separatorDatePrefix) > 0):
            tindy = str.split(indggg,separatorDatePrefix)
        else:
            tindy = indggg
        #print (tindy[1])
        #if (tindy[1].find(separatorSuffix) > 0):
        #    der = tindy[1].index(separatorSuffix)
        #else:
        #    der = 5
        ##der = tindy.index(separatorSuffix)-1
        #tizz = tindy[1][:der]
        tizz = tindy[1]
        arruu.append(tizz)
        kurre.append(indggg)
        #print "extracted index: " +tizz 
        #tindy.sort()
    arruu.sort(reverse=True)
    #print arruu
    kurre.sort(reverse=True)
    #print kurre
    gzyy = 0
    while (len(arruu) > 1 or arruu[len(arruu)-1] <> "0"):
        gzyy =+ 1
        localuu = arruu.pop(0)
        localuee =  kurre.pop(0)
        if (r.exists("MessageIndex"+localuu + "Status")):
            CurQuery = r.get("MessageIndex"+localuu + "Command",)
            #finaldata = 
            print (" Assigning : MessageIndex"+localuu + "ResultDataPayload:")
            timestamp = time.strftime(" %H:%M:%S")
            r.setex("MessageIndex"+localuu + "Status","WORKER_PROCESSING_CONTENTS",90)
            r.setex("MessageIndex"+localuu + "Timestamp",datey.isoformat() + "T" + timestamp,90)
            print("Processing:" + CurQuery)
            sys.stdout.flush()
            time.sleep(0.3)
            qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=24,
            border=4,
            )

            #testing = Image.open("qrcode1.png")
            #testing.save(localuu[1:6]+"_asJPG.jpg","jpeg")
            #testing.save(localuu[1:6]+"_asPNG.png")
            qr.add_data(CurQuery)
            #qr.add_data("http://This is experiment.com")
            qr.make(fit=True)
            #myyfactory = qrcode.image.svg.SvgImage
            #image.models.
            img = qr.make_image()
            #print(img)
            #ssuy = open("Blu_QR"+localuu[1:6]+".txt","w")
            #img.save("Blu_QR"+localuu[1:6]+".png", format='PNG')
            #img.save("Blu_QR"+localuu[1:6]+"_RLE.bmp", format='BMP', compression="bmp_rle")
            #img.save("Blu_QR"+localuu[1:6]+".bmp", format='BMP')
            bbuu = BytesIO()
            uiee = BytesIO()
            img.save(bbuu, format='PNG')
            bbuu.seek(0)
            #ssuy.flush()
            #bytesobj = img.tobytes('raw')
            #bytesobj = img.tobytes('PNG')   FAILS
            bytesobj = bbuu.getvalue()
            #khyz = img.get_image()
            img_str = binascii.b2a_base64(bytesobj)
            #img_str = binascii.b2a_base64(ravdec.net_compression(bytesobj))
            #img_str = ravdec.net_compression(binascii.b2a_base64(bytesobj))
            #compresst = ravdec.net_compression(img_str)
            #compresst = ravdec.net_compression(img_str)
            #ssuy.writelines(img_str)
            #ssuy.flush()

        
            #img_str = bytesobj.format("02X")
            #img = qr.make(CurQuery,mfactory=myyfactory)        
            #testbase64data = "DEFAULT ERROR"
            testbase64data = img_str
            #testbase64data = base64.b64encode(img_str)
            #buffer = cStringIO.StringIO(yuinn)
            #img.save(buffer, format="JPEG")
            #bihhh = binascii.b2a_base64(yuinn)
            #img_str = base64.b64encode(yuinn)
            #print "%x" % {img[0]} + " " + format(img[1],"00")

            r.setex("MessageIndex"+localuu + "ResultDataPayload",testbase64data, MessageTTL)
            r.setex("MessageIndex"+localuu + "Status","DATA_DELIVERED",MessageTTL)
            r.sadd(messageindexstorage + ":finishedjobs", localuee)
        
        r.srem(messageindexstorage + messagelistlevel1,localuee)
        r.delete(messageindexstorage + messagelistlevel1+":"+localuu)
        print "Removed : SREM "+ messageindexstorage + messagelistlevel1 +  " "  + '[\"' +localuee +'\"]'
        #print localuu
rtt  = r.delete("STOP_HEROKU_WORKER")
time.sleep(5)
print "Worker Terminated with Redis key STOP_HEROKU_WORKER : Count of deleted: " + format(rtt,"000")

