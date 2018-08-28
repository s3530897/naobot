# -*- coding: utf-8 -*
from naoqi import ALProxy
import time
import json

ip_robot = "10.0.7.63"
port_robot = 9559

def sound_recognize():
    asr = ALProxy("ALSpeechRecognition", ip_robot, port_robot)
    tts = ALProxy("ALTextToSpeech", ip_robot, port_robot)
    photo_apture = ALProxy("ALPhotoCapture", ip_robot, port_robot)
    aur = ALProxy("ALAudioRecorder", ip_robot, port_robot)
    aup = ALProxy("ALAudioPlayer", ip_robot, port_robot)
    channal_list = [0, 1, 0, 0]
    cameraMap = {
        'Top': 0,
        'Bottom': 1
    }
    camera_id = 0
    recordFolder = "/home/nao/recordings/cameras/"
    asr.pause(True)
    try:
        asr.setLanguage("Chinese")
        tts.setLanguage("Chinese")
    except Exception,e:
        print(e)

    vocabulary = ["你好", "再见", "拍照", "录音", "播放录音", "获取文件"]
    asr.setVocabulary(vocabulary, False)
    while(
            True):
        asr.subscribe("Test_ASR")
        print "Speech start"
        am = ALProxy("ALMemory", ip_robot, port_robot)
        am.subscribeToEvent('WordRecognized',ip_robot,'wordRecognized')
        asr.pause(False)
        time.sleep(10)
        asr.unsubscribe("Test_ASR")
        data=am.getData("WordRecognized")
        print("data: %s" % data)
        print(data)
        if(
                data[1]<0.4):
            tts.say("并不知道你在说什么")
        else:
            if(
                    data[0] == "再见"):
                break
            if(
                    data[0] == "拍照"):
                print "Aha, I saw a human!"
                camera_id += 1
                file_name = "pho" + str(camera_id)
                photo_apture.setCameraID(camera_id)
                photo_apture.setPictureFormat("jpg")
                tts.say("咔嚓")
                photo_apture.takePicture(recordFolder, file_name)
            if(
                    data[0] == "你好"):
                tts.say("你也好啊")
            if(
                    data[0] == "录音"):
                aur.startMicrophonesRecording("/home/nao/rectest.wav", "wav", 16000, channal_list)
                print("开始")
                time.sleep(10)
                aur.stopMicrophonesRecording()
                print("完成")
            if(
                    data[0] == "播放录音"):
                aup.post.playFile("/home/nao/rectest.wav")
            if(
                    data[0] == "获取文件"):
                pass

        time.sleep(10)
if(
        __name__ == "__main__"):
    sound_recognize()