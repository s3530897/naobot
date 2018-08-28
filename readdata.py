# -*- coding: utf-8 -*
from naoqi import ALProxy
import time
import json

ip_robot = "10.0.7.63"
port_robot = 9559

def sound_recognize():
    am=ALProxy("ALMemory", ip_robot, port_robot)
    ad=am.WordRecognized
    print(ad)
    print(ad[0])
    print(ad[1])

if __name__=="__main__":
    sound_recognize()