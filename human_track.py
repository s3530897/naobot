from naoqi import ALProxy, ALBroker, ALModule
import time
import sys

ip_robot = "10.0.7.63"
port_robot = 9559

# Global variable to store the humanEventWatcher module instance
humanEventWatcher = None
memory = None


class HumanTrackedEventWatcher(ALModule):
    """ A module to react to HumanTracked and PeopleLeft events """

    def __init__(self):
        ALModule.__init__(self, "humanEventWatcher")
        global memory
        memory = ALProxy("ALMemory", ip_robot, port_robot)
        memory.subscribeToEvent("ALBasicAwareness/HumanTracked",
                                "humanEventWatcher",
                                "onHumanTracked")
        memory.subscribeToEvent("ALBasicAwareness/PeopleLeft",
                                "humanEventWatcher",
                                "onPeopleLeft")
        #memory.subscribeToEvent('WordRecognized', ip_robot, 'wordRecognized')
        self.speech_reco = ALProxy("ALSpeechRecognition", ip_robot, port_robot)
        self.text_to_speech=ALProxy("ALTextToSpeech", ip_robot, port_robot)
        self.is_speech_reco_started = False
        self.photo_apture=ALProxy("ALPhotoCapture", ip_robot, port_robot)
        self.cameraMap = {
            'Top': 0,
            'Bottom': 1
        }
        self.camera_id=0
        self.recordFolder = "/home/nao/recordings/cameras/"

    def onHumanTracked(self, key, value, msg):
        """ callback for event HumanTracked """
        print "got HumanTracked: detected person with ID:", str(value)
        if value >= 0:  # found a new person
            self.start_speech_reco()
            position_human = self.get_people_perception_data(value)
            [x, y, z] = position_human
            print "The tracked person with ID", value, "is at the position:", \
                "x=", x, "/ y=",  y, "/ z=", z
            print "Aha, I saw a human!"
            self.camera_id+=1
            file_name = "pho"+str(self.camera_id)
            self.photo_apture.setCameraID(self.camera_id)
            self.photo_apture.setPictureFormat("jpg")
            self.photo_apture.takePicture( self.recordFolder, file_name )
            self.text_to_speech.say("Aha, I saw a human!")
            self.text_to_speech.say("Hi,there!")
            self.text_to_speech.say("Do you dream of sheep?")
        else:
            pass



    def onPeopleLeft(self, key, value, msg):
        """ callback for event PeopleLeft """
        print "got PeopleLeft: lost person", str(value)
        self.stop_speech_reco()

    def start_speech_reco(self):
        """ start asr when someone's detected in event handler class """
        if not self.is_speech_reco_started:
            try:
                data = memory.getData("WordRecognized")
                print(data)
            except RuntimeError:
                print "ASR already started"
            self.speech_reco.setVisualExpression(True)
            self.speech_reco.subscribe("BasicAwareness_Test")
            self.is_speech_reco_started = True
            print "start ASR"

    def stop_speech_reco(self):
        """ stop asr when someone's detected in event handler class """
        if self.is_speech_reco_started:
            self.speech_reco.unsubscribe("BasicAwareness_Test")
            self.is_speech_reco_started = False
            print "stop ASR"

    def get_people_perception_data(self, id_person_tracked):
        memory = ALProxy("ALMemory", ip_robot, port_robot)
        memory_key = "PeoplePerception/Person/" + str(id_person_tracked) + \
                     "/PositionInWorldFrame"
        return memory.getData(memory_key)


if __name__ == "__main__":
    event_broker = ALBroker("event_broker", "0.0.0.0", 0,
                            ip_robot, port_robot)
    global humanEventWatcher
    humanEventWatcher = HumanTrackedEventWatcher()
    basic_awareness = ALProxy("ALBasicAwareness", ip_robot, port_robot)
    motion = ALProxy("ALMotion", ip_robot, port_robot)

    #start
    motion.wakeUp()
    basic_awareness.setEngagementMode("FullyEngaged")
    basic_awareness.startAwareness()

    #loop on, wait for events until interruption
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print "Interrupted by user, shutting down"
        #stop
        basic_awareness.stopAwareness()
        motion.rest()
        event_broker.shutdown()
        sys.exit(0)