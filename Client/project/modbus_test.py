import serial
import minimalmodbus as minimalmodbus
from socket import *

MAX_ELEMENT = 2

class SocketConnection:
    ip = '192.168.1.8'
    port = 0
    client = None
    
    def __init__(self, port):
        SocketConnection.port = port
        print(port)
        SocketConnection.client = socket(AF_INET, SOCK_STREAM)
        SocketConnection.client.connect((SocketConnection.ip, SocketConnection.port))
        print("Connected!")
            
    def send(self, data):
        SocketConnection.client.send(str(data).encode("utf-8"))
        
    def recv(self):
        data = SocketConnection.client.recv(1024)
        return data.decode("utf-8")
        
    def close(self):
        SocketConnection.client.close()
        
        
class Modbus:
    instrument = None

    def __init__(self, port, baudrate, id):
        self.instrument = minimalmodbus.Instrument(port, id, 'rtu')
        self.instrument.serial.baudrate = baudrate
        self.instrument.serial.bytesize = 8
        self.instrument.serial.parity = serial.PARITY_NONE
        self.instrument.serial.stopbits = 2
        self.instrument.serial.timeout = 1

    def motor_enable(self):
        try:
            self.instrument.write_register(0x0B, 0x01, functioncode=int('0x06', 16))
            print("Motor Enabled : " + str(self.instrument.read_register(0x0B, 0, functioncode=int('0x03', 16))))
        except IOError:
            print("Failed to enable the motor")

    def set_speed(self, speed):
        try:
            self.instrument.write_register(0x09, speed, functioncode=int('0x06', 16))
            print("Motor Speed : " + str(self.instrument.read_register(0x09, 0, functioncode=int('0x03', 16))))
        except IOError:
            print("Failed to send speed")

    def set_dir(self, direction):    # 0 : CW, 1 : CCW
        try:
            self.instrument.write_register(0x0A, direction, functioncode=int('0x06', 16))
            print("Motor Direction : " , str(self.instrument.read_register(0x0A, 0, functioncode=int('0x03', 16))))
        except IOError:
            print("Failed to send direction")

    def motor_disable(self):
            try:
                self.instrument.write_register(0x0B, 0, functioncode=int('0x06', 16))
            except IOError:
                print("Failed to send direction")
                
    def set_id(self):
            try:
                self.instrument.write_register(0xF000, 0x64, functioncode=int('0x06', 16))
            except IOError:
                print("Failed to send ID")

if __name__ == '__main__' :
    #socket = SocketConnection(8485)
    
    usb_port = '/dev/ttyUSB0'
    baud_rate = 9600
    id1 = 0x64
    id2 = 0x65

    modbus1 = Modbus(usb_port, baud_rate, id1)
    modbus2 = Modbus(usb_port, baud_rate, id2)

    modbus1.set_speed(200)
    modbus1.set_dir(1)
    modbus2.set_speed(200)
    modbus2.set_dir(0)
    
    modbus1.motor_disable()
    modbus2.motor_disable()
    
    exit(0)

"""
    while True:
        data = socket.recv()
        element = data.split(',')
        
        if(len(element) == MAX_ELEMENT):
            #print(element[0] + "   " + element[1])
            modbus1.set_speed(int(element[0]))
            modbus1.set_dir(int(element[1]))
            modbus2.set_speed(int(element[0]))
            modbus2.set_dir(1-int(element[1]))
        else:
            print("invalid data")
            break
    
    modbus1.motor_disable()
    modbus2.motor_disable()
    """
    #socket.close()
            
