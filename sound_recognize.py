# -*- coding: utf-8 -*
from naoqi import ALProxy
import time
import json

ip_robot = "10.0.7.63"
port_robot = 9559

def sound_recognize():
    asr = ALProxy("ALSpeechRecognition", ip_robot, port_robot)
    asr.pause(True)

    vocabulary = ["hello", "bye", "how are you", "nothing", "good morning"]
    asr.setVocabulary(vocabulary, False)
    asr.subscribe(ip_robot)
    print "Speech start"
    am = ALProxy("ALMemory", ip_robot, port_robot)
    am.subscribeToEvent('WordRecognized',ip_robot,'wordRecognized')
    asr.pause(False)
    time.sleep(10)
    asr.unsubscribe(ip_robot)
    data=am.getData("WordRecognized")
    print("data: %s" % data)
    print(data)

if __name__=="__main__":
    sound_recognize()