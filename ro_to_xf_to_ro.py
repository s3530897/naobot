# -*- coding: utf-8 -*
import str_tosound as tos
import weather
import paramiko
import re
import urllib2
import time
import urllib
import json
import hashlib
import base64
from naoqi import ALProxy
import takephoto as tph
import lzz_recognize_food as lzzf
import lzz_reference as lzzr
import ex_api.health_qa as health_qa

port_trans = 22
ip_robot = "10.46.105.41"
port_robot = 9559
c_path = "E:/work/CNLP/resource/test.wav"
r_path = "/home/nao/test.wav"
rer_path = "/home/nao/intest.wav"
rec_path = "E:/work/CNLP/resource/intest.wav"

#开起录音，并从nao获取语音文件
def integration_from_nao():
    aur = ALProxy("ALAudioRecorder", ip_robot, port_robot)
    channal_list = [0, 0, 1, 0]
    aur.startMicrophonesRecording("/home/nao/test.wav", "wav", 16000, channal_list)
    print("开始")
    time.sleep(5)
    aur.stopMicrophonesRecording()
    print("完成")
    transport = paramiko.Transport((ip_robot, port_trans))
    print ("test1")
    transport.connect(username="nao", password="nao")
    print ("test2")
    sftp = paramiko.SFTPClient.from_transport(transport)
    print ("test3")
    sftp.get(r_path, c_path)
    print ("test4")
    return sendfile_to_service(c_path)

#发送语音文件至nao并播放
def integration_to_nao():
    transport = paramiko.Transport((ip_robot, port_trans))
    print ("test1")
    transport.connect(username="nao", password="nao")
    print ("test2")
    sftp = paramiko.SFTPClient.from_transport(transport)
    print ("test3")
    sftp.put(rec_path, rer_path)
    print ("test4")
    aup = ALProxy("ALAudioPlayer", ip_robot, port_robot)
    file_id=aup.loadFile(rer_path)
    ti = aup.getFileLength(file_id)
    print("时间：",ti)
    aup.play(file_id)
    time.sleep(ti)

#发送指定语音文件至科大讯飞转译为文字返回字符串
def sendfile_to_service(file_path = c_path):
    f = open(file_path, 'rb')
    file_content = f.read()
    base64_audio = base64.b64encode(file_content)
    body = urllib.urlencode({'audio': base64_audio})

    url = 'http://api.xfyun.cn/v1/service/v1/iat'
    api_key = 'd3cff9f77f2a2d79898cfa153df15a3a'
    param = {"engine_type": "sms16k", "aue": "raw"}

    x_appid = '5b7fbe72'
    x_param = base64.b64encode(json.dumps(param).replace(' ', ''))
    x_time = int(int(round(time.time() * 1000)) / 1000)
    x_checksum = hashlib.md5(api_key + str(x_time) + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    flag=0
    while (True):
        try:
            print("显示次数")
            req = urllib2.Request(url, body, x_header)
            result = urllib2.urlopen(req)
            break
        except Exception:
            if(flag<2):
                flag+=1
                continue
            else:
                result="网络连接失败"
                break

    result = result.read()
    print result
    d1 = json.loads(result)
    print(d1['data'])
    return d1['data']

#对听到用户发出指令予以应答
def str_sclassification(strs):
    flag = re.search(u'我叫', strs)
    flag2 = re.search(u'天气', strs)
    flag_takephoto1 = re.search(u'拍照', strs)
    flag_takephoto2 = re.search(u'拍张照', strs)
    flag_lzz = re.search(u'记录',strs)
    flag_lzz_vit = re.search(u'营养',strs)
    flag_sayhi=re.search(u'你好',strs)
    flag_bye=re.search(u'再见',strs)
    flag_healthqa,health_str= health_qa.healthqa(strs)
    print(flag)
    print ("test5")
    if(
            flag_lzz_vit is not None):
        strs = lzzr.connect_lzz_reference(strs)
        net_connect(strs)
        return 1
    elif(
        flag_lzz is not None):
        strs = lzzf.connect_lzz_food_recognize(strs)
        net_connect(strs)
        return 1
    elif(
            flag is not None
    ):
        try:
            s1 = strs.split(u'我叫')
            strs = s1[1]
            print(strs)
            s1 = strs.split(u'。')
            strs = s1[0]
            print(strs)
            print("testN")
        except Exception:
            strs = ''
            pass
        print(strs)
        strs = u"你好"+strs+u",我叫闹闹,很高兴认识你"
        net_connect(strs)
        print (strs)
        return 1
    elif(
            flag2 is not None):
        weather_lo_flag=re.search(u'的天气',strs)
        if(weather_lo_flag is not None):
            if(re.search(u'查下', strs) is not None):
                ss = strs.split(u'查下')
                strs = ss[1]
            if (re.search(u'查查', strs) is not None):
                ss = strs.split(u'查查')
                strs = ss[1]
            if (re.search(u'查询', strs) is not None):
                ss = strs.split(u'查询')
                strs = ss[1]
            ss=strs.split(u'的天气')
            strs = weather.connect_weather(ss[0])
        else:
            strs = weather.connect_weather()
        net_connect(strs)
        return 1
    elif((flag_takephoto1 is not None) or (flag_takephoto2 is not None)):
        strs = "可以啊，给你拍个照，看着我正义的眼睛，3,2,1，咔嚓"
        net_connect(strs)
        print("拍照准备")
        tph.takephoto()
        return 1
    elif(flag_sayhi is not None):
        strs="你也好呀，有什么事情想问我的嘛？"
        net_connect(strs)
        return 1
    elif(flag_bye is not None):
        strs = "再见，不要太想我哦。"
        net_connect(strs)
        return 1
    elif(flag_healthqa):
        net_connect(health_str)
        return 1
    else:
        return 0
    print ("test7")
    return 1

#连接科大讯飞接口索取语音合成并播放
def net_connect(str):
    print(str)
    flag = 0
    while (
            flag < 3):
        flag += 1
        try:
            tos.txt_to_sound(str)
            integration_to_nao()
            break
        except Exception:
            print("网络连接错误")

if (
        __name__ == "__main__"):
    result = integration_from_nao()
    str_sclassification(result)