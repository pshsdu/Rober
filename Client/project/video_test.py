import cv2
from socket import *
import numpy as np


#ip = '172.30.1.46'
class VideoClient:
    width = 240
    height = 320

    def __init__(self, ip, port, cam_num):
        self.ip = ip
        self.port = port
        self.cam_list = list()
        
        self.init_socket()
        self.init_cam(cam_num)
        
    def init_socket(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((self.ip, self.port))    # server ip : 192.168.1.8, port : 8485

    def init_cam(self, cam_num):
        cam = None
        base_id = -1
        video_loc = '/dev/video'

        for i in range(0, cam_num):
            cam = cv2.VideoCapture(video_loc + str(i*4))
            cam.set(3, VideoClient.width)
            cam.set(4, VideoClient.height)

            self.cam_list.append(cam)

        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        print(len(self.cam_list))
        
        # VideoClient.cam = cv2.VideoCapture(-1)
         
        # VideoClient.cam.set(3, VideoClient.width)
        # VideoClient.cam.set(4, VideoClient.height)

    def stream(self): 
        string_list = list()
        output = ''

        for i in range(0, len(self.cam_list)):
            ret, frame = self.cam_list[i].read()
            result, frame = cv2.imencode('.jpg', frame, self.encode_param)
            data = np.array(frame)
            stringData = data.tostring()
            output = output + (str(len(stringData))).encode().ljust(16) + stringData

        self.socket.sendall(output)
    
    def close(self):
        self.socket.close()
        for i in range (len(self.cam_list)):
            self.cam_list[i].close()
        
if __name__ == "__main__":
    client = VideoClient('192.168.0.19', 8485, 3)
    #client1 = VideoClient(8486)
    
    while True:
        client.stream()
        #client1.stream()
        
    client.close()
    #client1.cam.release()
