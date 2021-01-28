import cv2
from socket import *
import numpy as np
import modbus
import threading
import time

class Client:
    
    # About Motor
    controller = None
    elements = None

    def __init__(self, ip, port, cam_num):
        self.ip = ip
        self.port = port
        self.init_socket()
        
        self.cam_num = cam_num
        self.cam_list = list()
        self.width = 320
        self.height = 240
        self.init_cam(self.cam_num)

        Client.controller = MotorController()

    def init_socket(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((self.ip, self.port))
        print("socket is initialized")

    def init_cam(self, cam_num):
        cam = None
        video_loc = '/dev/video'

        for i in range(0, cam_num):
            cam = cv2.VideoCapture(video_loc + str(i*4))
            cam.set(3, self.width)
            cam.set(4, self.height)

            self.cam_list.append(cam)

        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        print("camera " + str(len(self.cam_list)) + " initialized")

    def send_cam(self):
        string_list = list()
        output = ''

        while True:
            try:
                for i in range(0, self.cam_num):
                    ret, frame = self.cam_list[i].read()
                    result, frame = cv2.imencode('.jpg', frame, self.encode_param)
                    data = np.array(frame)
                    stringData = data.tostring()
                    output = output + (str(len(stringData))).encode().ljust(16) + stringData

                    self.socket.sendall(output)
            except:
                print("Connection Error : Broken Camera Connection")
                self.close()

    def recv(self):
        # while True:
        Client.elements = None
        try:
            data = self.socket.recv(1024)
        except:
            print("Disconnected!")
            self.close()
            return
        time.sleep(0.5)

        if not data:
            return
        
        recv_data = data.decode("utf-8")
        
        try:
            Client.elements = recv_data.replace("/", "%").split("%")
            Client.elements = [v for v in Client.elements if v]
            
            if len(Client.elements) < 2:
                raise Exception('Connection Error : Input list must have at least 2 args')
            
        except Exception as e:
            self.close()

    def motor_control(self):
        while True:
            self.recv()
            
            if Client.elements is not None:
                Client.controller.set_speed(Client.elements)
                
    def close(self):
        Client.controller.close()
        self.socket.close()
        for i in range (len(self.cam_list)):
            self.cam_list[i].close()


class MotorController:

    def __init__(self):
        self.motor_num = 2
        self.baudrate = 9600

        self.id1 = 0x64
        self.id2 = 0x65

        self.usb_port = '/dev/ttyUSB0'

        self.modbus1 = None
        self.modbus2 = None

        self.init_motor()

    def init_motor(self):
        self.modbus1 = modbus.Modbus(self.usb_port, self.baudrate, self.id1)
        self.modbus2 = modbus.Modbus(self.usb_port, self.baudrate, self.id2)

        self.modbus1.motor_enable()
        self.modbus2.motor_enable()
        self.modbus1.motor2_enable()
        self.modbus2.motor2_enable()

    def set_speed(self, data):
        self.modbus1.set_speed(int(data[0]))
        self.modbus2.set_speed(int(data[0]))
        self.modbus1.set_speed2(int(data[0]))
        self.modbus2.set_speed2(int(data[0]))

        self.modbus1.set_dir(int(data[1]))
        self.modbus2.set_dir(int(data[1]))
        self.modbus1.set_dir2(int(data[1]))
        self.modbus2.set_dir2(int(data[1]))
        
        print("speed : " + data[0] + ", dir : " + data[1]) 

    def close(self):
        self.modbus1.motor_disable()
        self.modbus2.motor_disable()
        self.modbus1.motor2_disable()
        self.modbus2.motor2_disable()

if __name__ == '__main__':
    # port = input("port : ")
    # ip = input("ip : ")
    client = Client('192.168.0.19', 8485, 3)
    
    camera_thread = threading.Thread(target=client.send_cam)
    motor_thread = threading.Thread(target=client.motor_control)
    
    camera_thread.start()
    motor_thread.start()