# -*- coding: utf-8 -*
from naoqi import ALProxy
import time
import json

ip_robot = "10.0.7.63"
port_robot = 9559

class sound_recognize:
    def __init__(self):
        self.checkdata=0

    #基于机器人本体的语音辨析测试+声音甄别测试
    def sound_recognize(self,t=10):
        self.asr = ALProxy("ALSpeechRecognition", ip_robot, port_robot)
        self.asr.pause(True)
        self.vocabulary = ["hello", "bye", "how are you", "nothing", "good morning","nao"]
        self.asr.setVocabulary(self.vocabulary, False)
        self.asr.subscribe(ip_robot)
        print "Speech start"
        self.am = ALProxy("ALMemory", ip_robot, port_robot)
        self.am.subscribeToEvent('WordRecognized',ip_robot,'wordRecognized')
        self.am.subscribeToEvent("SoundDetected",ip_robot,"onSoundDetected")
        self.asr.pause(False)
        time.sleep(50)
        self.asr.unsubscribe(ip_robot)
        self.data=self.am.getData("WordRecognized")
        print("data: %s" % self.data)
        print(self.data)
        if(self.data[0]=='nao' and self.data[1]>0.37 and self.data[1] != self.checkdata):
            print("成功")
            self.checkdata = self.data[1]
            return True
        else:
            return False
    def onSoundDetected(self, eventName, value, subscriberIdentifier):
        print("这是最后的波纹")
        print(eventName)
        print(value)
        print(subscriberIdentifier)

if __name__=="__main__":
    sound_recognize().sound_recognize()