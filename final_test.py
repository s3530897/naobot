# -*- encoding: UTF-8 -*-

import sys
import time
from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
import argparse
import sound_record
import file_transport
import ro_to_xf_to_ro as toxf


#综合版测试
ReactToTouch = None
memory = None
ip_robot = "10.0.7.63"
port_robot = 9559

class ReactToTouch(ALModule):
    """ A simple module able to react
        to touch events.
    """

    def __init__(self, name):
        ALModule.__init__(self, name)
        global memory
        self.onplay_flag=False
        self.Flag = True
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("FrontTactilTouched",
                                "ReactToTouch",
                                "onFrontTactilTouched")
        memory.subscribeToEvent("ALAudioSourceLocalization/SoundLocated",
                                "ReactToTouch",
                                "onSoundLocated")
        self.speech_reco = ALProxy("ALSpeechRecognition", ip_robot, port_robot)
        #self.speech_reco.setVocabulary(["yes", "no", "nao", "now now", "what are you talking"], False)
        self.speech_reco.subscribe("Test_ASR")

    def onFrontTactilTouched(self, strVarName, value):
        # to avoid repetitions
        print("还是不一样的")
        print(value)
        if(value>0.5):
            if(self.Flag):
                print("开始")
                self.Flag=False
                self.sound_record.sound_record_start()
            else:
                self.Flag=True
                print("结束")
                self.sound_record.sound_record_stop()
                file_transport.transit_to_c()
                s = toxf.sendfile_to_service()
                toxf.str_sclassification(s)

        data = memory.getData("WordRecognized")
        print("居然还检测到了数据data: %s" % data)
        print(data)
        print(strVarName)
        print(self.Flag)

    def onSoundLocated(self, eventName, value, subscriberIdentifier):
        print("已经检测到地理位置")
        print(eventName)
        print(value)
        print(subscriberIdentifier)
        if(self.onplay_flag):
            return
        else:
            self.onplay_flag = True
            self.sound_record.sound_record_stop()

            result = toxf.integration_from_nao()
            toxf.str_sclassification(result)

            self.sound_record.sound_record_start()
            self.onplay_flag = False

def main(ip, port):
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       ip,          # parent broker IP
       port)        # parent broker port

    global ReactToTouch
    ReactToTouch = ReactToTouch("ReactToTouch")


    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="10.0.7.63",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")
    args = parser.parse_args()
    main(args.ip, args.port)