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

port_trans = 22
ip_robot = "10.0.7.63"
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
    aup.post.playFile(rer_path)

#发送指定语音文件至科大讯飞转译为文字返回字符串
def sendfile_to_service(file_path):
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
    print(flag)
    print ("test5")
    if (
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
        strs = u"你好"+strs+u",我叫闹闹"
        net_connect(strs)
        print (strs)
    elif(
            flag2 is not None):
        strs = weather.connect_weather()
        net_connect(strs)
    else:
        strs = "我没有听见你在说什么，不想做个自我介绍么？"
        net_connect(strs)
    print ("test7")

#连接科大讯飞接口索取语音合成并播放
def net_connect(str):
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