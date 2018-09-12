#-*- coding: utf-8 -*-
import requests
import re
import time
import hashlib
import base64
import struct

URL = "http://api.xfyun.cn/v1/service/v1/tts"
AUE = "raw"
APPID = "5b7fbe72"
API_KEY = "44a73a6b6f487ce4905431ad24b32ec6"
#语音合成
#头文件标准
def getHeader():
        curTime = str(int(time.time()))
        param = "{\"aue\":\""+AUE+"\",\"auf\":\"audio/L16;rate=16000\",\"voice_name\":\"xiaoyan\",\"engine_type\":\"intp65\"}"
        paramBase64 = base64.b64encode(param)
        m2 = hashlib.md5()
        m2.update(API_KEY + curTime + paramBase64)
        checkSum = m2.hexdigest()
        header ={
                'X-CurTime':curTime,
                'X-Param':paramBase64,
                'X-Appid':APPID,
                'X-CheckSum':checkSum,
                'X-Real-Ip':'127.0.0.1',
                'Content-Type':'application/x-www-form-urlencoded; charset=utf-8',
        }
        return header

#获取文字
def getBody(text):
        data = {'text':text}
        return data

#读写文件
def writeFile(file, content):
    with open(file, 'wb') as f:
        f.write(content)
    f.close()

#文字合成语音转译
def txt_to_sound(str):
    r = requests.post(URL,headers=getHeader(),data=getBody(str))
    contentType = r.headers['Content-Type']
    if contentType == "audio/mpeg":
        sid = r.headers['sid']
        if AUE == "raw":
            writeFile("E:/work/CNLP/resource/intest.wav", r.content)
        else :
            writeFile("audio/"+sid+".mp3", r.content)
        print "success, sid = " + sid
    else :
        print r.text

if (
        __name__ == "__main__"):
    txt_to_sound(u"干嘛？")