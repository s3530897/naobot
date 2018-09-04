# -*- encoding: UTF-8 -*-
""" Say `My {Body_part} is touched` when receiving a touch event
"""

import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
import argparse

# Global variable to store the ReactToTouch module instance
ReactToTouch = None
memory = None

class ReactToTouch(ALModule):
    """ A simple module able to react
        to touch events.
    """
    def __init__(self, name):
        ALModule.__init__(self, name)
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("FrontTactilTouched",
                                "ReactToTouch",
                                "onFrontTactilTouched")
        memory.subscribeToEvent("SoundDetected",
                                "humanEventWatcher",
                                "onSoundDetected")
        memory.subscribeToEvent("ALAudioSourceLocalization/SoundLocated",
                                "humanEventWatcher",
                                "onSoundLocated")

    def onFrontTactilTouched(self, strVarName, value):
        # to avoid repetitions
        print("还是不一样的")
        print(value)
        print(strVarName)

    def onSoundLocated(self, eventName, value, subscriberIdentifier):
        print("检测不到也不能怪我啊")
        print(eventName)
        print(value)
        print(subscriberIdentifier)

    def onSoundDetected(self, eventName, value, subscriberIdentifier):
        print("这是最后的波纹")
        print(eventName)
        print(value)
        print(subscriberIdentifier)

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