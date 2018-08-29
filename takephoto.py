# -*- coding: utf-8 -*
import time
from naoqi import ALProxy
import file_transport as ft

ip_robot = "10.0.7.63"
port_robot = 9559

#拍照接口
def takephoto():
    photo_apture = ALProxy("ALPhotoCapture", ip_robot, port_robot)
    cameraMap = {
        'Top': 0,
        'Bottom': 1
    }
    recordFolder = "/home/nao/recordings/cameras/"
    file_name = "pho"
    photo_apture.setCameraID(0)
    photo_apture.setPictureFormat("jpg")
    photo_apture.takePicture(recordFolder, file_name)
    ft.transit_to_c("/home/nao/recordings/cameras/pho.jpg","E:/work/CNLP/resource/pho.jpg")