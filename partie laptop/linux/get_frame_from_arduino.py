import cv2
import urllib
import numpy as np
import sys

from threading import Thread, RLock

class ArduinoCam(Thread):
    """docstring for """
    def __init__(self, ip):
        Thread.__init__(self)
        self.stopped = False
        self.ip = ip
        self.lock = RLock()
        self.frame = None

    def stop(self):
        with self.lock:
            self.stopped=True

    def isStopped(self):
        with self.lock:
            return self.stopped

    def get_frame(self):
        with self.lock:
            return self.frame

    def run(self):
        stream=urllib.urlopen('http://'+self.ip+':8080/?action=stream')
        bytes=''
        while (not self.isStopped()):
            bytes+=stream.read(512)
            a = bytes.find('\xff\xd8')
            b = bytes.find('\xff\xd9')
            if a!=-1 and b!=-1:
                jpg = bytes[a:b+2]
                bytes= bytes[b+2:]
                with self.lock:
                    self.frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR) #CV_LOAD_IMAGE_COLOR

def get_frame_from_ip(ip):
    stream=urllib.urlopen('http://'+ip+':8080/?action=stream')
    bytes=''
    frame=None

    while (True):
        bytes+=stream.read(512)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a!=-1 and b!=-1:
            jpg = bytes[a:b+2]
            bytes= bytes[b+2:]
            frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR) #CV_LOAD_IMAGE_COLOR
            return frame





if __name__ == '__main__':
    while True:
        i = get_frame_from_ip(sys.argv[1])
        if (i!=None):
            cv2.imshow("Frame" , i)
        if cv2.waitKey(1)==27:
            exit(0)
