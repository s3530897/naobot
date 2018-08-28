# -*- coding: utf-8 -*
import time
from naoqi import ALProxy

ip_robot = "10.0.7.63"
port_robot = 9559


def sound_record():
    aur = ALProxy("ALAudioRecorder", ip_robot, port_robot)
    channal_list = [1, 1, 1, 1]
    aur.startMicrophonesRecording("/home/nao/rectest.wav", "wav", 16000, channal_list)
    print("开始")
    time.sleep(10)
    aur.stopMicrophonesRecording()
    print("完成")
    time.sleep(10)
    print("播放")
    aup = ALProxy("ALAudioPlayer", ip_robot, port_robot)
    aup.post.playFile("/home/nao/rectest.wav")


def sound_test():
    aup = ALProxy("ALAudioPlayer", ip_robot, port_robot)
    aup.post.playFile("/home/nao/test.wav")
    time.sleep(10)

if  __name__ == "__main__":
    sound_record()