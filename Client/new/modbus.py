import serial
import minimalmodbus as minimalmodbus


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
            
    def motor2_enable(self):
        try:
            self.instrument.write_register(0x2B, 0x01, functioncode=int('0x06', 16))
            print("Motor2 Enabled : " + str(self.instrument.read_register(0x0B, 0, functioncode=int('0x03', 16))))
        except IOError:
            print("Failed to enable the motor2")

    def set_speed(self, speed):
        try:
            self.instrument.write_register(0x09, speed, functioncode=int('0x06', 16))
            # print("Motor Speed : " + str(self.instrument.read_register(0x09, 0, functioncode=int('0x03', 16))))
        except IOError:
            print("Failed to send speed")
            
    def set_speed2(self, speed):
        try:
            self.instrument.write_register(0x29, speed, functioncode=int('0x06', 16))
            # print("Motor2 Speed : " + str(self.instrument.read_register(0x09, 0, functioncode=int('0x03', 16))))
        except IOError:
            print("Failed to send speed2")

    def set_dir(self, direction):    # 0 : CW, 1 : CCW
        try:
            self.instrument.write_register(0x0A, direction, functioncode=int('0x06', 16))
            # print("Motor Direction : " + str(self.instrument.read_register(0x0A, 0, functioncode=int('0x03', 16))))
        except IOError:
            print("Failed to send direction")
            
    def set_dir2(self, direction):    # 0 : CW, 1 : CCW
        try:
            self.instrument.write_register(0x2A, direction, functioncode=int('0x06', 16))
            # print("Motor Direction : " + str(self.instrument.read_register(0x0A, 0, functioncode=int('0x03', 16))))
        except IOError:
            print("Failed to send direction")

    def motor_disable(self):
            try:
                self.instrument.write_register(0x0B, 0, functioncode=int('0x06', 16))
            except IOError:
                print("Failed to send direction")
                
    def motor2_disable(self):
        try:
            self.instrument.write_register(0x2B, 0, functioncode=int('0x06', 16))
        except IOError:
            print("Failed to send direction")
                
    def set_id(self):
            try:
                self.instrument.write_register(0xF000, 0x64, functioncode=int('0x06', 16))
            except IOError:
                print("Failed to send ID")
            
