# -*- coding: utf-8 -*
import time
from naoqi import ALProxy

ip_robot = "10.0.7.63"
port_robot = 9559
test="/home/nao/test.wav"

#录音播放功能测试
def sound_record(path=test):
    aur = ALProxy("ALAudioRecorder", ip_robot, port_robot)
    channal_list = [1, 1, 1, 1]
    aur.startMicrophonesRecording(path, "wav", 16000, channal_list)
    print("开始")
    time.sleep(10)
    aur.stopMicrophonesRecording()
    print("完成")
    time.sleep(10)
    print("播放")
    aup = ALProxy("ALAudioPlayer", ip_robot, port_robot)
    aup.post.playFile(path)

def sound_record_start(path=test):
    aur = ALProxy("ALAudioRecorder", ip_robot, port_robot)
    channal_list = [0, 0, 1, 0]
    aur.startMicrophonesRecording(path, "wav", 16000, channal_list)
    print("开始")

def sound_record_stop():
    aur = ALProxy("ALAudioRecorder", ip_robot, port_robot)
    aur.stopMicrophonesRecording()
    print("录音完成")

def sound_test(path = test):
    aup = ALProxy("ALAudioPlayer", ip_robot, port_robot)
    aup.post.playFile("/home/nao/test.wav")

if  __name__ == "__main__":
    sound_record_stop()