# -*- coding: utf-8 -*
import time
from naoqi import ALProxy

ip_robot = "10.0.7.63"
port_robot = 9559

#简单的nao机器人发音测试
def botsay():
    try:
        tts=ALProxy("ALTextToSpeech",ip_robot,port_robot)
        tts.say(" \\ style = neutral \\Hi budy")
        tts.say(" \\ style = didactic \\Say some thing")
        tts.say(" \\ style = joyful \\Do not ignore me, please!")
    except Exception,e:
        print("连接失败")
        print str(e)

if __name__=="__main__":
    botsay()


