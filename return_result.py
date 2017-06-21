import json
import os
import redis
import time
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


print("Working :")



randyu = random.randint(1,16000000)
randt = random.randint(10,99999)
messageindexstorage = "To_FromTable"
messagelistlevel1 = ":finishedjobs"
separatorDatePrefix = "/"
separatorSuffix = "|"
MessageTTL = 89

redisURL = os.environ.get("REDIS_URL")
redischannel = 'marc-channel'
timestamp = time.strftime(" %H:%M:%S")
datey = date.today()
r = redis.from_url(redisURL)

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
print ouuz
#ouuz.sort()
#print ouuz
arruu = ["9999999999"]
kurre = ["9999999999"]
for indggg in ouuz:
    if (indggg.find(separatorDatePrefix) > 0):
        tindy = str.split(indggg,separatorDatePrefix)
    else:
        tindy = indggg
    print (tindy[1])
    #if (tindy[1].find(separatorSuffix) > 0):
    #    der = tindy[1].index(separatorSuffix)
    #else:
    #    der = 5
    ##der = tindy.index(separatorSuffix)-1
    #tizz = tindy[1][:der]
    tizz = tindy[1]
    arruu.append(tizz)
    kurre.append(indggg)
    print "extracted index: " +tizz 
    #tindy.sort()
arruu.sort(reverse=False)
print arruu
kurre.sort(reverse=False)
print kurre
gzyy = 0
while (len(arruu) > 1 or arruu[len(arruu)-1] <> "9999999999"):
    gzyy =+ 1
    localuu = arruu.pop(0)
    localuee =  kurre.pop(0)
    if (r.exists("MessageIndex"+localuu + "Status")):
        CurStatus = r.get("MessageIndex"+localuu + "Status",)
        print (" Got Status : " + CurStatus + " for MessageIndex"+localuu + "Status:")
        timestamp = time.strftime(" %H:%M:%S")
        timestart = time.time()
        r.setex("MessageIndex"+localuu + "Status","CONTENT_EXTRACTION_STARTED",90)
        r.setex("MessageIndex"+localuu + "Timestamp",datey.isoformat() + "T" + timestamp,90)
        CurResult = r.get("MessageIndex"+localuu + "ResultDataPayload")
        timestamp = time.strftime(" %H:%M:%S")
        timefinished = time.time()
        timediff = timefinished - timestart
        r.setex("MessageIndex"+localuu + "ResultDataPayload","CONTENT REMOVED: " + "duration ; {%f}" % timediff,480)
        r.setex("MessageIndex"+localuu + "Status","FINISHED_CONTENT_EXTRACTION" ,90)
        r.setex("MessageIndex"+localuu + "Timestamp",datey.isoformat() + "T" + timestamp,90)
        #finaldata = base64.b64decode(CurResult)
        bin_fromstr = binascii.a2b_base64(CurResult)
        uiee = BytesIO()
        uiee.write(bin_fromstr)
        new_img = Image.open(uiee)
        new_img.save("Blu_QR_RESULT"+localuu[1:6]+".png", format='PNG')
        #new_qr = qrcode.QRCode(
        #version=1,
        #error_correction=qrcode.constants.ERROR_CORRECT_L,
        #box_size=24,
        #border=4,
        #)
        #newqr_i = new_qr.make()
        #finaldata = binascii.a2b_base64(CurResult)
        #fs = io.open('cn.txt','w')
        #print (finaldata)
        #fs.flush
        #fs.close
        #qr = qrcode.QRCode(
        #version=1,
        #error_correction=qrcode.constants.ERROR_CORRECT_L,
        #box_size=255,
        #border=4,
        #)
        #strr = io.open("tinn.raw",'a+b')
        #imobb = new PIL.Image.builtins.
        #imobb = Image.frombytes('RGB', (28,28),finaldata,'raw',"F;8B")
        #imobb = Image.frombytes('L', (21,21),data=finaldata)  FAILS
        #for uhzer in Image.MODES:
        #    print uhzer
#        The mode of an image defines the type and depth of a pixel in the image. The current release supports the following standard modes:

#1 (1-bit pixels, black and white, stored with one pixel per byte)
#L (8-bit pixels, black and white)
#P (8-bit pixels, mapped to any other mode using a colour palette)
#RGB (3x8-bit pixels, true colour)
#RGBA (4x8-bit pixels, true colour with transparency mask)
#CMYK (4x8-bit pixels, colour separation)
#YCbCr (3x8-bit pixels, colour video format)
#I (32-bit signed integer pixels)
#F (32-bit floating point pixels)
#PIL also provides limited support for a few special modes, including LA (L with alpha), RGBX (true colour with padding) and RGBa (true colour with premultiplied alpha).
        #imobb.save("tinn_live.png")
        #imobb.close()

        r.sadd(messageindexstorage + ":retrievedjobs", localuee)
        
    #r.srem(messageindexstorage + messagelistlevel1,localuee)
    #r.delete(messageindexstorage + messagelistlevel1+":"+localuu)
    #print "Removed : SREM "+ messageindexstorage + messagelistlevel1 +  " "  + '[\"' +localuee +'\"]'
    print localuu
